#!/usr/bin/env python3
"""
Build the strategy catalog database (CSV) and navigation indexes for the
Quant Trading Vault.

Reads every strategies/*.md file, parses the structured FMZ export format
(> Name / > Author / > Strategy Description / > Strategy Arguments /
> Source (lang) / > Detail / > Last Modified), extracts the backtest header
and Pine `strategy()` declaration, then applies rule-based classification:

  * kind            strategy / indicator / library / template / utility / tutorial
  * strategy family trend_following, momentum, mean_reversion, breakout, grid,
                    martingale, dca, arbitrage, hedging, market_making, scalping,
                    candlestick_pattern, chart_pattern, support_resistance,
                    smart_money_concepts, volatility, volume, oscillator,
                    statistical, machine_learning, seasonality_time,
                    multi_timeframe, portfolio_rotation, options, divergence,
                    channel, pairs_trading, swing_structure, pyramiding, ...
  * trading style   hft / scalping / intraday / day_trading / swing / position /
                    overnight / dca_accumulation
  * market tags     crypto / futures / perpetual / forex / stocks / indices /
                    commodities / options / spot
  * timeframes      1m 3m 5m 15m 30m 1h 2h 4h 1d 1w 1mo (+ MTF timeframes)
  * mechanics       direction, SL/TP/trailing, sizing, pyramiding, MTF, filters
  * scores          risk_level, leverage, complexity, risk_mgmt_score,
                    buildability_score, repaint_risk
  * claimed KPIs    win rate, profit factor, drawdown, net profit, sharpe, R:R

Usage:  python catalog/build_catalog.py        (run from repo root or anywhere)
Output: catalog/strategies_db.csv, catalog/INDEX.md, catalog/index/*.md,
        catalog/SCHEMA.md
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
STRAT_DIR = ROOT / "strategies"
CAT_DIR = ROOT / "catalog"
IDX_DIR = CAT_DIR / "index"

KNOWN_HEADERS = {
    "Name", "Author", "Strategy Description", "Strategy Arguments",
    "Detail", "Last Modified",
}

# --------------------------------------------------------------------------
# Parsing
# --------------------------------------------------------------------------

def split_sections(text: str) -> dict:
    """Split FMZ markdown export into sections keyed by header."""
    sections: dict[str, list[str]] = {}
    current = "_preamble"
    sections[current] = []
    in_fence = False
    for line in text.splitlines():
        stripped = line.rstrip()
        if stripped.startswith("```"):
            in_fence = not in_fence
        if not in_fence and stripped.startswith("> "):
            hdr = stripped[2:].strip()
            if hdr in KNOWN_HEADERS or hdr.startswith("Source ("):
                current = hdr
                sections.setdefault(current, [])
                continue
        sections.setdefault(current, []).append(line)
    return {k: "\n".join(v).strip() for k, v in sections.items()}


def extract_code(section_text: str) -> str:
    m = re.search(r"```[^\n]*\n(.*?)```", section_text, re.S)
    return m.group(1) if m else section_text


def parse_backtest_header(code: str) -> dict:
    out = {}
    m = re.search(r"/\*backtest\s*(.*?)\*/", code, re.S)
    if not m:
        return out
    body = m.group(1)
    for line in body.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        out[k.strip()] = v.strip()
    ex = out.get("exchanges", "")
    eid = re.search(r'"eid"\s*:\s*"([^"]+)"', ex)
    cur = re.search(r'"currency"\s*:\s*"([^"]+)"', ex)
    bal = re.search(r'"balance"\s*:\s*([\d.]+)', ex)
    stocks = re.search(r'"stocks"\s*:\s*([\d.]+)', ex)
    out["_eid"] = eid.group(1) if eid else ""
    out["_currency"] = cur.group(1).upper() if cur else ""
    out["_balance"] = bal.group(1) if bal else ""
    out["_stocks"] = stocks.group(1) if stocks else ""
    return out


def parse_pine_strategy_decl(code: str) -> dict:
    """Find strategy(...) / indicator(...) / study(...) declaration and parse kwargs."""
    out = {"decl_type": "", "decl_title": ""}
    m = re.search(r"^\s*(strategy|indicator|study)\s*\(", code, re.M)
    if not m:
        return out
    out["decl_type"] = m.group(1)
    # balanced paren scan
    i = m.end()
    depth = 1
    buf = []
    while i < len(code) and depth > 0:
        c = code[i]
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                break
        buf.append(c)
        i += 1
    args = "".join(buf)
    t = re.search(r'(?:title\s*=\s*)?"([^"]*)"', args)
    if t:
        out["decl_title"] = t.group(1)
    for k, v in re.findall(r"(\w+)\s*=\s*([^,\n]+)", args):
        v = v.strip().strip('"')
        out[k] = v
    return out


def parse_arguments_table(section: str) -> list[tuple[str, str, str]]:
    rows = []
    for line in section.splitlines():
        if not line.startswith("|") or line.startswith("|----") or line.startswith("|Argument"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2:
            rows.append((cells[0], cells[1], " ".join(cells[2:]) if len(cells) > 2 else ""))
    return rows


def desc_subsection(desc: str, names: tuple[str, ...]) -> str:
    """Return body of the first '## <name>' subsection matching any name."""
    parts = re.split(r"^#{1,4}\s+", desc, flags=re.M)
    for part in parts[1:]:
        head, _, body = part.partition("\n")
        h = head.strip().lower()
        if any(n in h for n in names):
            return body.strip()
    return ""


def clean_excerpt(text: str, limit: int) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)  # images
    text = re.sub(r"`", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > limit:
        text = text[:limit].rsplit(" ", 1)[0] + "…"
    return text


# --------------------------------------------------------------------------
# Classification dictionaries
# --------------------------------------------------------------------------

FAMILY_KEYWORDS = {
    "trend_following": [
        "trend following", "trend-following", "trend tracking", "trend-tracking",
        "trend trading", "follow the trend", "trend continuation", "trend strategy",
        "trend confirmation", "moving average cross", "ma cross", "ema cross",
        "sma cross", "golden cross", "death cross", "crossover", "cross over",
        "supertrend", "super trend", "adx", "ichimoku", "parabolic sar", "psar",
        "dual moving average", "triple moving average", "trend direction",
        "trend filter", "hull", "trend-based", "trend based", "trending", "trendline", "trend line",
        "trend strength", "trend detection", "trend identification",
    ],
    "momentum": [
        "momentum", "rate of change", "roc ", "macd", "impulse", "acceleration",
        "squeeze momentum", "relative strength", "strength index", "velocity",
        "tsi", "awesome oscillator",
    ],
    "mean_reversion": [
        "mean reversion", "mean-reversion", "mean reverting", "revert", "reversion",
        "overbought", "oversold", "counter-trend", "countertrend", "contrarian",
        "pullback", "pull back", "buy the dip", "dip buying", "range trading",
        "range-bound", "oscillation", "oscillating", "bollinger", "z-score",
        "zscore", "reversal", "retracement", "bounce", "rebound", "envelope",
        "standard deviation", "deviation from", "rsi 2", "rsi(2)", "extreme",
    ],
    "breakout": [
        "breakout", "break out", "break-out", "breakthrough", "break through",
        "breaks above", "breaks below", "donchian", "channel break", "new high",
        "new low", "52 week", "52-week", "opening range", "orb", "box",
        "highest high", "lowest low", "range expansion", "turtle", "n-day high",
        "price channel", "penetrat",
    ],
    "grid": ["grid", "gridbot", "grid bot", "grid trading", "ladder", "laddering"],
    "martingale": ["martingale", "martin", "doubling", "double down", "double-down", "anti-martingale", "gambler", "gambling"],
    "dca": [
        "dollar cost", "dollar-cost", "dca", "regular investment", "fixed investment",
        "recurring buy", "accumulation strategy", "accumulate", "invested every",
        "periodic investment", "auto-invest", "buy and hold", "hodl",
    ],
    "arbitrage": [
        "arbitrage", "spread trading", "cross-exchange", "cross exchange",
        "triangular", "funding rate", "basis trading", "cash and carry",
        "statistical arbitrage", "stat arb", "spot-futures", "futures-spot",
        "price difference", "inter-exchange", "intertemporal", "term spread",
    ],
    "pairs_trading": ["pairs trading", "pair trading", "cointegration", "cointegrat", "spread between", "ratio trading", "relative value"],
    "hedging": ["hedge", "hedging", "delta neutral", "delta-neutral", "market neutral", "market-neutral", "balanced strategy", "balance strategy"],
    "market_making": ["market making", "market-making", "market maker", "bid-ask", "bid ask", "order book", "orderbook", "liquidity provid", "maker order", "quote", "iceberg", "depth"],
    "scalping": ["scalp", "scalper", "scalping", "tick", "high frequency", "high-frequency", "hft", "ultra short", "ultra-short", "micro"],
    "candlestick_pattern": [
        "candlestick", "candle pattern", "engulfing", "hammer", "doji", "pin bar",
        "pinbar", "harami", "three white soldiers", "three black crows",
        "morning star", "evening star", "inside bar", "outside bar", "marubozu",
        "shooting star", "hanging man", "piercing", "dark cloud", "tweezer",
        "three bar", "3 bar", "red green", "green red", "candle body", "wick",
        "spinning top", "heikin", "heiken", "candle direction", "candle color", "candle colour",
        "bar color", "green candle", "red candle", "bullish candle", "bearish candle",
        "consecutive candles", "consecutive bars", "candle close", "bar pattern",
    ],
    "chart_pattern": [
        "head and shoulders", "double top", "double bottom", "triple top",
        "wedge", "flag pattern", "pennant", "triangle pattern", "cup and handle",
        "123 reversal", "1-2-3", "1 2 3", "zigzag", "zig zag", "fractal",
        "elliott", "harmonic", "gartley", "butterfly", "abcd", "wolfe",
        "rounding", "w pattern", "m pattern", "chart pattern",
    ],
    "support_resistance": [
        "support", "resistance", "pivot", "fibonacci", "fib ", "supply", "demand zone",
        "key level", "price level", "s/r", "swing high", "swing low", "structure",
        "price action", "golden ratio", "retest", "camarilla", "floor pivot",
    ],
    "smart_money_concepts": [
        "order block", "smart money", "ict ", "fair value gap", "fvg", "liquidity sweep",
        "liquidity grab", "market structure", "break of structure", "bos ", "choch",
        "change of character", "imbalance", "mitigation", "kill zone", "killzone",
        "silver bullet", "displacement", "inducement", "premium and discount",
        "smc", "wyckoff", "stop hunt",
    ],
    "volatility": [
        "volatility", "atr", "average true range", "keltner", "squeeze", "expansion",
        "contraction", "vix", "bollinger band width", "bbw", "true range", "chaikin volatility",
        "volatility breakout", "std dev", "garch", "range filter",
    ],
    "volume": [
        "volume", "obv", "on balance", "vwap", "money flow", "mfi", "cvd",
        "volume delta", "order flow", "orderflow", "accumulation/distribution",
        "accumulation distribution", "chaikin", "volume profile", "vpvr",
        "footprint", "tick volume", "volume weighted", "klinger", "ease of movement",
        "force index", "vwma", "turnover",
    ],
    "oscillator": [
        "rsi", "stochastic", "stoch", "kdj", "cci", "williams", "%r", "oscillator",
        "wave trend", "wavetrend", "fisher", "ultimate oscillator", "cmo", "chande",
        "relative strength index", "commodity channel", "dmi", "trix", "ppo",
        "dpo", "coppock", "kst", "aroon", "vortex", "rvi", "schaff", "stc",
    ],
    "statistical": [
        "regression", "statistical", "statistic", "z-score", "zscore", "kalman",
        "hurst", "correlation", "probability", "bayesian", "monte carlo",
        "autocorrelation", "percentile", "quantile", "distribution", "variance",
        "polynomial", "least squares", "linear reg", "linreg", "fourier",
        "entropy", "half-life", "ornstein", "stochastic process", "markov", "random", "randomness", "coin flip",
        "hidden markov", "kurtosis", "skew", "gaussian", "curve fitting",
    ],
    "machine_learning": [
        "machine learning", "neural network", "neural net", "lstm", "random forest",
        "k-nearest", "knn", "kmeans", "k-means", "svm", "deep learning",
        "reinforcement learning", "artificial intelligence", "genetic algorithm",
        "lorentzian", "classifier", "classification", "logistic regression",
        "perceptron", "gradient boost", "xgboost", "decision tree", "clustering",
        "training", "prediction model", "predictive model", "ai-", "ai ", "gpt",
        "openai", "chatgpt", "llm", "tensorflow", "pytorch", "sklearn",
    ],
    "seasonality_time": [
        "seasonal", "seasonality", "day of week", "day-of-week", "time of day",
        "time-of-day", "session", "opening", "market open", "market close",
        "close of day", "monday", "friday", "weekend", "overnight", "gap ",
        "calendar", "month end", "turn of the month", "halving", "end of day",
        "eod", "time filter", "time window", "trading hours", "london", "new york",
        "asian session", "tokyo", "holiday", "intraday time", "hour of day",
        "specific time", "time-based", "time based", "scheduled", "moon", "lunar", "astro", "astrological",
        "quarterly", "yearly", "annual",
    ],
    "multi_timeframe": ["multi-timeframe", "multi timeframe", "multitimeframe", "mtf", "higher timeframe", "higher time frame", "multiple timeframes", "two timeframes", "dual timeframe", "timeframe synergy", "htf", "ltf"],
    "portfolio_rotation": ["rotation", "portfolio", "rebalanc", "multi-asset", "multi asset", "allocation", "basket", "multi-symbol", "multi symbol", "multiple assets", "multiple symbols", "multi-currency", "multiple currencies", "screener", "ranking", "top n", "risk parity", "weighting", "index tracking"],
    "options": ["option strategy", "options strategy", "options trading", "straddle", "strangle", "iron condor", "implied volatility", "delta hedg", "gamma", "theta", "call option", "put option", "strike", "expiry", "expiration", "covered call", "wheel strategy", "butterfly spread", "vertical spread"],
    "divergence": ["divergence", "diverg", "hidden divergence", "convergence"],
    "channel": ["channel", "envelope", "band", "keltner", "donchian", "regression channel", "linear regression channel", "trend channel", "price channel", "starc", "envelop"],
    "pyramiding": ["pyramid", "scale in", "scaling in", "add to position", "add position", "position building", "averaging down", "average down", "averaging up", "dollar averaging", "step in"],
    "swing_structure": ["swing", "higher high", "higher low", "lower low", "lower high", "hh", "hl", "lh", "ll", "swing point", "swing failure", "sfp"],
    "trailing_exit": ["trailing stop", "trailing", "trail stop", "chandelier", "ratchet", "atr trailing", "parabolic stop", "profit protection", "lock in profit"],
    "moving_average": ["moving average", "ema", "sma", "wma", "hma", "dema", "tema", "alma", "kama", "vidya", "jma", "jurik", "t3", "smma", "lsma", "zlema", "frama", "mama", "ma "],
    "renko_range_bars": ["renko", "range bar", "kagi", "point and figure", "line break", "three line break"],
    "news_sentiment": ["news", "sentiment", "twitter", "fear and greed", "fear & greed", "social", "on-chain", "onchain", "whale", "economic calendar"],
    "signal_bot_execution": ["webhook", "alert", "bot", "3commas", "telegram", "auto trading", "automated trading", "signal", "execution", "api", "websocket"],
}

# Families that count as "strategic logic" for primary selection (others are supporting tags)
PRIMARY_FAMILY_ORDER = [
    "martingale", "grid", "dca", "arbitrage", "pairs_trading", "market_making",
    "hedging", "options", "machine_learning", "smart_money_concepts",
    "portfolio_rotation", "breakout", "mean_reversion", "trend_following",
    "momentum", "scalping", "candlestick_pattern", "chart_pattern",
    "support_resistance", "divergence", "volatility", "volume", "oscillator",
    "statistical", "seasonality_time", "multi_timeframe", "channel",
    "swing_structure", "renko_range_bars", "news_sentiment", "moving_average",
    "pyramiding", "trailing_exit", "signal_bot_execution",
]
SUPPORTING_FAMILIES = {"moving_average", "pyramiding", "trailing_exit", "signal_bot_execution", "channel", "multi_timeframe", "swing_structure"}
# What the strategy IS (logic family) vs. which ingredient it uses
CORE_FAMILIES = [
    "martingale", "grid", "dca", "arbitrage", "pairs_trading", "market_making",
    "hedging", "options", "machine_learning", "smart_money_concepts",
    "portfolio_rotation", "breakout", "mean_reversion", "trend_following",
    "momentum", "scalping", "candlestick_pattern", "chart_pattern",
    "support_resistance", "divergence", "statistical", "seasonality_time",
    "renko_range_bars", "news_sentiment",
]
INGREDIENT_FAMILIES = ["volatility", "volume", "oscillator", "channel", "multi_timeframe", "swing_structure", "moving_average"]

INDICATOR_PATTERNS = {
    # name : (regex over code, regex over text)
    "EMA": (r"\bta\.ema\(|\bema\(|\bEMA\b", r"\bema\b|exponential moving average"),
    "SMA": (r"\bta\.sma\(|\bsma\(|\bSMA\b", r"\bsma\b|simple moving average"),
    "WMA": (r"\bta\.wma\(|\bwma\(", r"\bwma\b|weighted moving average"),
    "HMA": (r"\bta\.hma\(|\bhma\(|hullma", r"\bhma\b|hull moving average|\bhull\b"),
    "VWMA": (r"\bta\.vwma\(|\bvwma\(", r"\bvwma\b|volume weighted moving average"),
    "DEMA/TEMA": (r"\bdema\b|\btema\b", r"\bdema\b|\btema\b|double exponential|triple exponential"),
    "ALMA": (r"\bta\.alma\(|\balma\(", r"\balma\b|arnaud legoux"),
    "KAMA": (r"\bkama\b", r"\bkama\b|kaufman"),
    "JMA": (r"\bjma\b|jurik", r"\bjma\b|jurik"),
    "T3": (r"\bt3\b", r"\bt3 moving\b|tillson"),
    "LSMA/LinReg": (r"\bta\.linreg\(|\blinreg\(|\blsma\b", r"\blsma\b|linear regression|least squares"),
    "MACD": (r"\bta\.macd\(|\bmacd\(|\bmacd\b", r"\bmacd\b|convergence divergence"),
    "RSI": (r"\bta\.rsi\(|\brsi\(|\brsi\b", r"\brsi\b|relative strength index"),
    "Stochastic": (r"\bta\.stoch\(|\bstoch\(|\bstoch\b", r"stochastic|\bstoch\b"),
    "StochRSI": (r"stochrsi|stoch_rsi|stochasticrsi", r"stoch(?:astic)?\s*rsi"),
    "KDJ": (r"\bkdj\b", r"\bkdj\b"),
    "CCI": (r"\bta\.cci\(|\bcci\(|\bcci\b", r"\bcci\b|commodity channel index"),
    "Williams %R": (r"\bta\.wpr\(|\bwpr\(|williams", r"williams\s*%?r|\bwpr\b|williams percent"),
    "MFI": (r"\bta\.mfi\(|\bmfi\(|\bmfi\b", r"\bmfi\b|money flow index"),
    "OBV": (r"\bta\.obv\b|\bobv\b", r"\bobv\b|on[- ]balance volume"),
    "ADX/DMI": (r"\bta\.dmi\(|\bdmi\(|\badx\b", r"\badx\b|\bdmi\b|directional movement|directional index"),
    "ATR": (r"\bta\.atr\(|\batr\(|\batr\b", r"\batr\b|average true range"),
    "Bollinger Bands": (r"\bta\.bb\(|\bbb\(|bollinger|\bbbands?\b", r"bollinger|\bbb\b|\bbbands?\b"),
    "Keltner Channel": (r"\bta\.kc\(|\bkc\(|keltner", r"keltner"),
    "Donchian Channel": (r"donchian", r"donchian"),
    "Supertrend": (r"\bta\.supertrend\(|supertrend", r"super\s*trend"),
    "Parabolic SAR": (r"\bta\.sar\(|\bsar\(|\bpsar\b", r"parabolic|\bpsar\b|\bsar\b"),
    "Ichimoku": (r"ichimoku|tenkan|kijun|senkou", r"ichimoku|tenkan|kijun|kumo"),
    "VWAP": (r"\bta\.vwap\b|\bvwap\b", r"\bvwap\b|volume weighted average price"),
    "TWAP": (r"\btwap\b", r"\btwap\b"),
    "Pivot Points": (r"\bta\.pivothigh\(|\bta\.pivotlow\(|pivothigh|pivotlow|\bpivot", r"\bpivot"),
    "Fibonacci": (r"\bfib", r"fibonacci|\bfib\b"),
    "Heikin Ashi": (r"heikin|heiken|ticker\.heikinashi", r"heikin|heiken"),
    "Renko": (r"renko|ticker\.renko", r"renko"),
    "ZigZag": (r"zigzag|zig_zag", r"zigzag|zig zag"),
    "Momentum/ROC": (r"\bta\.mom\(|\bta\.roc\(|\bmom\(|\broc\(", r"rate of change|\broc\b"),
    "TSI": (r"\bta\.tsi\(|\btsi\b", r"\btsi\b|true strength index"),
    "Awesome Oscillator": (r"\bao\b.*sma\(hl2|awesome", r"awesome oscillator"),
    "CMO": (r"\bta\.cmo\(|\bcmo\b", r"\bcmo\b|chande momentum"),
    "CMF": (r"\bcmf\b", r"\bcmf\b|chaikin money flow"),
    "Chaikin Oscillator": (r"chaikin", r"chaikin oscillator"),
    "Aroon": (r"aroon", r"aroon"),
    "Vortex": (r"vortex|\bvi\+|\bvip\b", r"vortex"),
    "TRIX": (r"\btrix\b", r"\btrix\b"),
    "PPO": (r"\bppo\b", r"\bppo\b|percentage price oscillator"),
    "DPO": (r"\bdpo\b", r"\bdpo\b|detrended"),
    "KST": (r"\bkst\b", r"\bkst\b|know sure thing"),
    "Coppock": (r"coppock", r"coppock"),
    "Ultimate Oscillator": (r"\buo\b|ultimate", r"ultimate oscillator"),
    "Fisher Transform": (r"fisher", r"fisher transform|\bfisher\b"),
    "WaveTrend": (r"wavetrend|wave_trend|\bwt1\b", r"wave\s*trend"),
    "Schaff Trend Cycle": (r"schaff|\bstc\b", r"schaff|\bstc\b"),
    "Choppiness Index": (r"\bchop\b|choppiness", r"choppiness|\bchop\b"),
    "Squeeze (TTM)": (r"squeeze", r"squeeze"),
    "Range Filter": (r"range\s*filter", r"range filter"),
    "Kalman Filter": (r"kalman", r"kalman"),
    "Hurst Exponent": (r"hurst", r"hurst"),
    "Std Dev / Z-Score": (r"\bta\.stdev\(|\bstdev\(|zscore|z_score", r"standard deviation|z-score|zscore"),
    "Correlation": (r"\bta\.correlation\(|correlation\(", r"correlation"),
    "Percentile/Rank": (r"percentrank|percentile", r"percentile|percent rank"),
    "Highest/Lowest (channel)": (r"\bta\.highest\(|\bta\.lowest\(|\bhighest\(|\blowest\(", r"highest high|lowest low"),
    "Volume": (r"\bvolume\b", r"\bvolume\b"),
    "Volume Delta/CVD": (r"\bcvd\b|delta", r"volume delta|cumulative volume delta|\bcvd\b"),
    "Volume Profile": (r"volume\s*profile|vpvr", r"volume profile|\bvpvr\b|point of control|\bpoc\b"),
    "Elder Ray / Force Index": (r"elder|force\s*index|bull\s*power|bear\s*power", r"elder|force index|bull power|bear power"),
    "Mass Index": (r"mass\s*index", r"mass index"),
    "Balance of Power": (r"\bbop\b", r"balance of power"),
    "RVI": (r"\brvi\b", r"\brvi\b|relative vigor"),
    "Envelope/STARC": (r"envelope|starc", r"envelope|starc"),
    "Chandelier Exit": (r"chandelier", r"chandelier"),
    "Gann": (r"\bgann\b", r"\bgann\b"),
    "Elliott Wave": (r"elliott", r"elliott"),
    "Harmonic Patterns": (r"harmonic|gartley|\bbat\b|butterfly|crab", r"harmonic|gartley|butterfly pattern"),
    "Order Blocks/FVG": (r"order\s*block|fvg|fair\s*value", r"order block|fair value gap|\bfvg\b"),
    "Candlestick Patterns": (r"engulf|doji|hammer|harami|marubozu|pinbar|pin_bar", r"engulfing|doji|hammer|harami|marubozu|pin bar"),
    "Session/Time": (r"\btime\(|session|\bhour\b|dayofweek|\bminute\b|timeframe\.", r"session|time filter|trading hours"),
    "Lorentzian Classification": (r"lorentzian", r"lorentzian"),
    "KNN / ML model": (r"\bknn\b|k-nearest|nearest_neighbor|neural|lstm|random_forest|sklearn|tensorflow|torch", r"\bknn\b|k-nearest|neural|lstm|random forest"),
    "Kernel Regression": (r"kernel|nadaraya", r"kernel|nadaraya"),
    "Gaussian Filter": (r"gaussian", r"gaussian"),
    "Ehlers Filters": (r"ehlers|\bmama\b|\bfama\b|cyber\s*cycle|roofing|super\s*smoother|decycler|instantaneous", r"ehlers|super smoother|roofing filter|\bmama\b"),
    "Laguerre": (r"laguerre", r"laguerre"),
    "McGinley": (r"mcginley", r"mcginley"),
    "Alligator/Williams": (r"alligator|\bjaw\b|\bteeth\b|\blips\b", r"alligator"),
    "Fractals": (r"fractal", r"fractal"),
    "Camarilla": (r"camarilla", r"camarilla"),
    "Ma Ribbon": (r"ribbon", r"ribbon"),
    "Open Interest": (r"open\s*interest|\boi\b", r"open interest"),
    "Funding Rate": (r"funding", r"funding rate"),
    "Williams VIX Fix": (r"vix\s*fix|wvf", r"vix fix|wvf"),
}

INSTRUMENT_TICKERS = [
    # crypto
    "BTC", "XBT", "ETH", "SOL", "BNB", "DOGE", "XRP", "ADA", "LTC", "BCH", "EOS",
    "TRX", "AVAX", "MATIC", "DOT", "LINK", "ATOM", "SHIB", "PEPE", "TRUMP", "TRB",
    "USDT", "USDC", "BUSD", "DIA",
    # index / futures
    "SPY", "QQQ", "IWM", "DIA", "ES", "NQ", "YM", "RTY", "MES", "MNQ", "SPX",
    "NDX", "DJI", "DAX", "FTSE", "CAC", "HSI", "NIFTY", "BANKNIFTY",
    "SENSEX", "NIKKEI", "N225", "KOSPI", "ASX", "US30", "US100", "US500", "NAS100", "GER40",
    # commodities
    "CL", "GC", "SI", "NG", "HG", "ZB", "ZN", "XAUUSD", "XAGUSD", "XAU", "XAG",
    "WTI", "BRENT",
    # forex
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "USDCHF", "NZDUSD", "EURJPY",
    "GBPJPY", "EURGBP", "USDINR",
    # stocks
    "AAPL", "TSLA", "NVDA", "MSFT", "AMZN", "GOOG", "GOOGL", "META", "AMD", "NFLX",
    "COIN", "MSTR", "GME", "AMC", "BABA", "TQQQ", "SQQQ", "SOXL", "TLT", "GLD", "SLV", "USO",
]
INSTRUMENT_WORDS = {
    "bitcoin": "BTC", "ethereum": "ETH", "solana": "SOL", "dogecoin": "DOGE",
    "gold": "GOLD", "silver": "SILVER", "crude oil": "CRUDE", "oil": "OIL",
    "natural gas": "NATGAS", "nasdaq": "NASDAQ", "s&p 500": "SPX", "s&p500": "SPX",
    "sp500": "SPX", "dow jones": "DJI", "nikkei": "NIKKEI", "hang seng": "HSI",
    "nifty": "NIFTY", "bank nifty": "BANKNIFTY", "dax": "DAX", "rebar": "REBAR",
    "soybean": "SOYBEAN", "iron ore": "IRONORE", "copper": "COPPER", "euro": "EUR",
    "yen": "JPY", "pound": "GBP", "a-share": "A-SHARES", "a share": "A-SHARES",
    "csi 300": "CSI300", "沪深300": "CSI300", "treasury": "TREASURY", "bond": "BONDS",
}

MARKET_KEYWORDS = {
    "crypto": [
        "bitcoin", "btc", "eth", "ethereum", "crypto", "cryptocurrency", "cryptocurrencies",
        "altcoin", "altcoins", "binance", "usdt", "perpetual", "perpetuals", "perp", "perps",
        "bybit", "okx", "okex", "huobi", "coin", "coins", "token", "tokens", "defi", "uniswap",
        "funding rate", "bitmex", "deribit", "bitfinex", "kucoin", "coinbase", "kraken",
        "gate.io", "sol", "doge", "bnb", "blockchain", "web3", "satoshi", "digital asset",
        "digital assets", "digital currency", "digital currencies", "btcusdt", "ethusdt",
        "btcusd", "ethusd", "xrp", "solana", "dogecoin", "memecoin", "stablecoin",
    ],
    "forex": [
        "forex", "fx", "eurusd", "gbpusd", "usdjpy", "audusd", "usdcad", "usdchf",
        "nzdusd", "currency pair", "currency pairs", "pip", "pips", "eur/usd", "gbp/usd",
        "usd/jpy", "lot size", "metatrader", "mt4", "mt5", "oanda", "fxcm",
        "currency trading", "major pairs", "exchange rate", "xauusd",
    ],
    "stocks": [
        "stock", "stocks", "equity market", "equities", "nasdaq", "nyse", "spy", "qqq",
        "aapl", "tsla", "nvda", "nifty", "banknifty", "sensex", "a-share", "a-shares",
        "a share", "a shares", "hong kong", "hsi", "s&p", "s&p 500", "sp500",
        "dividend", "dividends", "earnings", "ipo", "blue chip", "small cap", "large cap",
        "etf", "etfs", "shanghai", "shenzhen", "listed company", "listed companies",
        "stock market", "share price", "csi 300",
    ],
    "indices": [
        "index futures", "indices", "nifty", "banknifty", "spx", "s&p", "s&p 500", "sp500",
        "nasdaq 100", "nasdaq100", "ndx", "dax", "dow", "dow jones", "nikkei", "hang seng",
        "ftse", "us30", "us100", "us500", "nas100", "ger40", "stock index", "vix index", "volatility index",
        "csi 300", "e-mini", "es futures", "nq futures", "mes", "mnq",
    ],
    "futures": [
        "futures", "futures contract", "futures contracts", "mes", "mnq", "ctp",
        "commodity futures", "rebar", "soybean", "iron ore", "quarterly contract",
        "delivery contract", "perpetual", "perpetual contract", "perpetual contracts",
        "coin-margined", "usdt-margined", "swap contract", "cta", "open interest",
        "e-mini", "micro e-mini", "tick size", "basis trading", "futures market",
        "futures trading", "contract trading", "leveraged contract", "cross margin",
        "isolated margin", "funding rate", "margin trading",
    ],
    "commodities": [
        "gold", "xau", "xauusd", "silver", "xag", "xagusd", "oil", "crude", "crude oil",
        "wti", "brent", "natural gas", "copper", "commodity", "commodities",
        "agricultural", "soybean", "soybeans", "corn", "wheat", "sugar", "rebar",
        "iron ore", "coal", "metals", "precious metals", "energy market",
    ],
    "options": [
        "options trading", "option strategy", "options strategy", "call option",
        "put option", "call options", "put options", "straddle", "strangle", "iron condor",
        "strike price", "implied volatility", "expiry date", "expiration date",
        "covered call", "option chain", "delta hedging", "theta decay", "gamma",
        "vega", "premium decay", "option premium", "options market",
    ],
    "spot": ["spot", "spot market", "spot trading", "cash market", "no leverage", "unleveraged", "spot account"],
}

TIMEFRAME_CANON = {
    "1": "1m", "2": "2m", "3": "3m", "5": "5m", "10": "10m", "15": "15m",
    "20": "20m", "30": "30m", "45": "45m", "60": "1h", "90": "90m", "120": "2h",
    "180": "3h", "240": "4h", "360": "6h", "480": "8h", "720": "12h", "1440": "1d",
    "D": "1d", "1D": "1d", "W": "1w", "1W": "1w", "M": "1mo", "1M": "1mo",
    "2D": "2d", "3D": "3d",
}
TF_ORDER = ["1m", "2m", "3m", "5m", "10m", "15m", "20m", "30m", "45m", "1h", "90m",
            "2h", "3h", "4h", "6h", "8h", "12h", "1d", "2d", "3d", "4d", "5d", "1w", "1mo"]

STYLE_BY_TF = {
    "1m": "scalping", "2m": "scalping", "3m": "scalping", "5m": "scalping",
    "10m": "intraday", "15m": "intraday", "20m": "intraday", "30m": "intraday",
    "45m": "intraday", "1h": "intraday", "90m": "intraday", "2h": "intraday",
    "3h": "swing", "4h": "swing", "6h": "swing", "8h": "swing", "12h": "swing",
    "1d": "swing", "2d": "position", "3d": "position", "4d": "position",
    "5d": "position", "1w": "position", "1mo": "position",
}

STYLE_KEYWORDS = {
    "hft": ["hft", "high frequency", "high-frequency", "tick level", "tick-level", "tick data", "ultra-high", "microsecond", "millisecond", "latency"],
    "scalping": ["scalp", "scalping", "scalper", "ultra short", "ultra-short", "quick profit", "small profit", "fast profit", "quick in and out"],
    "intraday": ["intraday", "intra-day", "within the day", "same day", "within a day", "short-term", "short term"],
    "day_trading": ["day trading", "daytrading", "day trade", "day-trading", "close all positions at end", "no overnight", "flat by close", "end of day exit", "eod exit", "close before market close", "session close"],
    "swing": ["swing trading", "swing trade", "swing-trading", "swing", "multi-day", "several days", "days to weeks", "medium-term", "medium term", "mid-term", "mid term"],
    "position": ["position trading", "long-term", "long term", "weekly chart", "monthly chart", "weeks to months", "buy and hold", "hodl", "investment", "investor", "longer-term", "months"],
    "overnight": ["overnight", "hold overnight", "gap trading", "gap up", "gap down", "opening gap", "close-to-open", "close to open", "next day open"],
    "dca_accumulation": ["dollar cost", "dca", "regular investment", "fixed investment", "recurring", "accumulat", "invested every"],
}


# --------------------------------------------------------------------------
# Classification helpers
# --------------------------------------------------------------------------

_KW_RE_CACHE: dict = {}


def kw_regex(keywords: list[str]) -> re.Pattern:
    """One alternation regex per keyword list; word-bounded so 'll' never matches 'all'."""
    key = tuple(keywords)
    if key not in _KW_RE_CACHE:
        parts = []
        for kw in keywords:
            k = kw.strip()
            if not k:
                continue
            pre = r"(?<![a-z0-9])" if re.match(r"[a-z0-9]", k) else ""
            post = r"(?![a-z0-9])" if re.search(r"[a-z0-9]$", k) else ""
            parts.append(pre + re.escape(k) + post)
        _KW_RE_CACHE[key] = re.compile("|".join(parts))
    return _KW_RE_CACHE[key]


def kw_score(text: str, keywords: list[str]) -> tuple[int, list[str]]:
    c = Counter(m.group(0) for m in kw_regex(keywords).finditer(text))
    score = sum(min(n, 5) for n in c.values())
    return score, list(c.keys())


def canon_tf(token: str) -> str | None:
    token = token.strip().strip('"')
    if token in TIMEFRAME_CANON:
        return TIMEFRAME_CANON[token]
    if token.isdigit():
        return TIMEFRAME_CANON.get(token)
    m = re.fullmatch(r"(\d+)([smhdwHDWS])", token)
    if m:
        n, u = m.groups()
        if u in ("S", "s"):
            return None
        if u == "m":
            return TIMEFRAME_CANON.get(n)
        if u in ("h", "H"):
            return TIMEFRAME_CANON.get(str(int(n) * 60))
        if u in ("d", "D"):
            return f"{n}d" if n != "1" else "1d"
        if u in ("w", "W"):
            return "1w"
    if re.fullmatch(r"\d+M", token):
        return "1mo"
    return None


MINUTE_OK = {1, 2, 3, 5, 10, 15, 20, 30, 45, 60, 90, 120, 180, 240}
HOUR_OK = {1, 2, 3, 4, 6, 8, 12}


def detect_timeframes_text(text: str, is_name: bool) -> list[str]:
    tfs = []
    low = text.lower()
    for n in re.findall(r"\b(\d{1,3})\s*[- ]?\s*(?:min|mins|minute|minutes)\b", low):
        n = int(n)
        if n in MINUTE_OK:
            tfs.append(TIMEFRAME_CANON.get(str(n)) or f"{n}m")
    for n in re.findall(r"\b(\d{1,2})\s*[- ]?\s*(?:h|hr|hrs|hour|hours)\b", low):
        n = int(n)
        if n in HOUR_OK:
            tfs.append(TIMEFRAME_CANON.get(str(n * 60)) or f"{n}h")
    # compact forms like 15M / 3m / 4H / 1D / 1W - only in the name / title
    if is_name:
        for n, u in re.findall(r"\b(\d{1,3})\s?([mMhHdDwW])\b", text):
            n_i = int(n)
            u = u.upper()
            if u == "M" and n_i in MINUTE_OK:
                tfs.append(TIMEFRAME_CANON.get(str(n_i)) or f"{n_i}m")
            elif u == "H" and n_i in HOUR_OK:
                tfs.append(TIMEFRAME_CANON.get(str(n_i * 60)))
            elif u == "D" and n_i in (1, 2, 3, 4, 5):
                tfs.append("1d" if n_i == 1 else f"{n_i}d")
            elif u == "W" and n_i == 1:
                tfs.append("1w")
    # daily / weekly / monthly chart or timeframe wording
    if re.search(r"\b(daily|1d|d1)\b[- ]?(timeframe|time frame|chart|candle|bar|period|basis)", low) or \
       re.search(r"\bon (the )?daily\b", low) or re.search(r"\bdaily (candles?|bars?|close|timeframe|chart)\b", low) or \
       (is_name and re.search(r"\bdaily\b", low)):
        tfs.append("1d")
    if re.search(r"\bweekly\b[- ]?(timeframe|time frame|chart|candle|bar|period)", low) or (is_name and re.search(r"\bweekly\b", low) and "invest" not in low):
        tfs.append("1w")
    if re.search(r"\bmonthly\b[- ]?(timeframe|time frame|chart|candle|bar|period)", low):
        tfs.append("1mo")
    return [t for t in tfs if t]


def detect_timeframes_code(code: str) -> list[str]:
    tfs = []
    for tok in re.findall(r'security\s*\([^,]+,\s*"([^"]*)"', code):
        c = canon_tf(tok)
        if c:
            tfs.append(c)
    for tok in re.findall(r'input\.timeframe\s*\(\s*(?:defval\s*=\s*)?"([^"]*)"', code):
        c = canon_tf(tok)
        if c:
            tfs.append(c)
    for tok in re.findall(r'input\s*\([^)]*type\s*=\s*input\.resolution[^)]*defval\s*=\s*"([^"]*)"', code):
        c = canon_tf(tok)
        if c:
            tfs.append(c)
    for tok in re.findall(r'input\s*\(\s*"([^"]*)"\s*,\s*(?:title\s*=\s*)?"[^"]*(?:timeframe|resolution)[^"]*"', code, re.I):
        c = canon_tf(tok)
        if c:
            tfs.append(c)
    return tfs


def uniq(seq):
    seen = set()
    out = []
    for s in seq:
        if s and s not in seen:
            seen.add(s)
            out.append(s)
    return out


def sort_tfs(tfs):
    return sorted(uniq(tfs), key=lambda t: TF_ORDER.index(t) if t in TF_ORDER else 99)


def first_num(pattern: str, text: str, flags=re.I) -> str:
    m = re.search(pattern, text, flags)
    if not m:
        return ""
    for g in m.groups():
        if g:
            return g
    return ""


# --------------------------------------------------------------------------
# Main per-file analysis
# --------------------------------------------------------------------------

def analyze(path: Path) -> dict | None:
    raw = path.read_text(encoding="utf-8", errors="replace")
    sec = split_sections(raw)
    if "Name" not in sec:
        return None

    name = sec.get("Name", "").strip().splitlines()[0] if sec.get("Name", "").strip() else path.stem
    author = sec.get("Author", "").strip().splitlines()[0] if sec.get("Author", "").strip() else ""
    desc = sec.get("Strategy Description", "")
    args_sec = sec.get("Strategy Arguments", "")
    detail = sec.get("Detail", "").strip()
    last_mod = sec.get("Last Modified", "").strip()

    lang = ""
    code = ""
    for k in sec:
        if k.startswith("Source ("):
            lang = k[len("Source ("):-1]
            code = extract_code(sec[k])
            break
    lang_norm = {"PineScript": "pine", "javascript": "javascript", "python": "python",
                 "MyLanguage": "mylanguage", "cpp": "cpp"}.get(lang, lang.lower())

    bt = parse_backtest_header(code)
    decl = parse_pine_strategy_decl(code) if lang_norm == "pine" else {}
    args = parse_arguments_table(args_sec)

    name_spaced = name.replace("-", " ")
    title = decl.get("decl_title", "")
    name_text = f"{name_spaced} {title}"
    desc_clean = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", desc)
    text_low = f"{name_text}\n{desc_clean}".lower()
    name_low = name_text.lower()
    code_low = code.lower()
    code_nocomment = re.sub(r"//[^\n]*", "", code) if lang_norm in ("pine", "javascript", "cpp") else re.sub(r"#[^\n]*", "", code)
    code_nc_low = code_nocomment.lower()
    args_text = " ".join(f"{a} {d}" for a, _, d in args).lower()
    all_low = text_low + "\n" + args_text
    # Text that describes what the strategy DOES. Excludes "Risks" / "Optimization
    # Directions" sections, which are wish-lists ("add a stop loss") and would
    # otherwise create false positives for mechanics detection.
    sec_overview = desc_subsection(desc, ("overview", "summary", "introduction"))
    sec_logic = desc_subsection(desc, ("principle", "logic", "how it works", "mechanism", "rules", "implementation"))
    sec_adv = desc_subsection(desc, ("advantage", "strength", "benefit", "pros"))
    feature_desc = f"{sec_overview}\n{sec_logic}\n{sec_adv}" if (sec_overview or sec_logic) else desc_clean
    feat_low = f"{name_text}\n{feature_desc}\n{args_text}".lower()
    txt = feat_low + "\n" + code_nc_low

    # ---------------- kind ----------------
    kind = "strategy"
    decl_type = decl.get("decl_type", "")
    if lang_norm == "pine":
        if decl_type in ("indicator", "study"):
            kind = "indicator"
        elif decl_type == "strategy":
            kind = "strategy"
        elif "strategy.entry" in code or "strategy.order" in code:
            kind = "strategy"
        else:
            kind = "indicator"
    else:
        trade_calls = bool(re.search(r"\.(Buy|Sell|CreateOrder|OpenLong|OpenShort|CloseLong|CloseShort|Trade)\s*\(|strategy\.entry|exchange\.(Buy|Sell)", code))
        if trade_calls:
            kind = "strategy"
        else:
            kind = "utility"
    if re.search(r"\b(library|class library|lib)\b", name_low) or "library(" in code[:400]:
        kind = "library"
    elif re.search(r"\btemplate\b", name_low):
        kind = "template"
    elif re.search(r"\b(tutorial|teaching|lesson|course|example|demo|quick start|explanation|explained|guide)\b", name_low) and kind != "strategy":
        kind = "tutorial"
    elif re.search(r"\b(tutorial|teaching|lesson|course)\b", name_low):
        kind = "tutorial_strategy"
    if kind == "utility" and re.search(r"\b(monitor|alert|notification|data|api|interface|tool|utility|precision|test|plot|chart|drawing|websocket|helper|manager|panel|dashboard|sync|export|import|backup|log)\b", name_low):
        kind = "utility"

    # ---------------- families ----------------
    fam_scores = {}
    fam_hits = {}
    for fam, kws in FAMILY_KEYWORDS.items():
        s_name, h_name = kw_score(name_low, kws)
        s_desc, h_desc = kw_score(feat_low, kws)
        s_code, h_code = kw_score(code_nc_low, kws) if fam not in ("signal_bot_execution",) else (0, [])
        score = s_name * 4 + s_desc + min(s_code, 6) * 0.5
        fam_scores[fam] = score
        fam_hits[fam] = uniq(h_name + h_desc)
    # some code-based boosts
    if "grid" in code_nc_low and re.search(r"grid", name_low):
        fam_scores["grid"] += 5
    if re.search(r"pyramiding\s*=\s*([2-9]|\d{2,})", code):
        fam_scores["pyramiding"] += 2
    if re.search(r"security\s*\(", code) or "request.security" in code:
        fam_scores["multi_timeframe"] += 3
    if re.search(r"trail_(points|offset|price)|trailing", code_nc_low):
        fam_scores["trailing_exit"] += 2
    tags = [f for f, s in fam_scores.items() if s >= 3]
    tags_sorted = sorted(tags, key=lambda f: (-fam_scores[f], PRIMARY_FAMILY_ORDER.index(f) if f in PRIMARY_FAMILY_ORDER else 99))

    def _rank(f):
        return (fam_scores[f], -PRIMARY_FAMILY_ORDER.index(f) if f in PRIMARY_FAMILY_ORDER else -99)

    # Primary family: prefer CORE logic families (what the strategy *is*) over
    # ingredient families (which indicator it happens to use). Name mentions win.
    name_core = [f for f in CORE_FAMILIES if fam_scores[f] > 0 and kw_score(name_low, FAMILY_KEYWORDS[f])[0] > 0]
    name_ingr = [f for f in INGREDIENT_FAMILIES if fam_scores[f] > 0 and kw_score(name_low, FAMILY_KEYWORDS[f])[0] > 0]
    desc_core = [f for f in CORE_FAMILIES if fam_scores[f] >= 3]
    if name_core:
        primary = max(name_core, key=_rank)
    elif desc_core and (not name_ingr or max(fam_scores[f] for f in desc_core) >= 5):
        primary = max(desc_core, key=_rank)
    elif name_ingr:
        primary = max(name_ingr, key=_rank)
    elif tags_sorted:
        primary = max([f for f in tags_sorted if f not in SUPPORTING_FAMILIES] or tags_sorted, key=_rank)
    else:
        primary = "moving_average" if fam_scores.get("moving_average", 0) > 0 else "unclassified"
    secondary = [f for f in tags_sorted if f != primary][:6]

    if kind == "strategy" and primary == "unclassified" and lang_norm != "pine" and re.search(
            r"one[- ]click|order|entrust|closing|market price|example|robot|bot|monitor|balance|transfer|test|demo|mining", name_low):
        kind = "execution_tool"

    # ---------------- indicators ----------------
    indicators = []
    for ind, (code_re, text_re) in INDICATOR_PATTERNS.items():
        hit = False
        if code and re.search(code_re, code_nocomment, re.I if ind not in ("EMA", "SMA") else 0):
            hit = True
        elif re.search(text_re, feat_low):
            hit = True
        if hit:
            indicators.append(ind)
    # drop generic "Volume" if more specific volume indicator found? keep; it's informative.

    # ---------------- timeframes ----------------
    tf_name = detect_timeframes_text(name_text, True)
    tf_desc = detect_timeframes_text(desc_clean[:4000], False)
    tf_code = detect_timeframes_code(code)
    bt_period = canon_tf(bt.get("period", "")) or bt.get("period", "")
    bt_base = canon_tf(bt.get("basePeriod", "")) or bt.get("basePeriod", "")
    if tf_name:
        tf_primary, tf_source = tf_name[0], "name"
    elif tf_desc:
        tf_primary, tf_source = Counter(tf_desc).most_common(1)[0][0], "description"
    elif bt_period:
        tf_primary, tf_source = bt_period, "backtest_header"
    else:
        tf_primary, tf_source = "", "none"
    tf_all = sort_tfs(tf_name + tf_desc + tf_code)
    tf_mtf = sort_tfs(tf_code)

    # ---------------- trading style ----------------
    style_scores = {}
    for st, kws in STYLE_KEYWORDS.items():
        s_n, _ = kw_score(name_low, kws)
        s_d, _ = kw_score(all_low, kws)
        style_scores[st] = s_n * 4 + s_d
    style_tags = [s for s, v in style_scores.items() if v >= 2]
    if tf_primary and tf_source != "backtest_header":
        tf_style = STYLE_BY_TF.get(tf_primary)
        if tf_style and tf_style not in style_tags:
            style_tags.append(tf_style)
    style_source = ""
    if style_tags:
        style_primary = max(style_tags, key=lambda s: style_scores.get(s, 0) + (3 if tf_primary and STYLE_BY_TF.get(tf_primary) == s else 0))
        style_source = "text" if style_scores.get(style_primary, 0) >= 2 else "timeframe"
    elif tf_primary:
        style_primary = STYLE_BY_TF.get(tf_primary, "")
        style_tags = [style_primary] if style_primary else []
        style_source = "backtest_header" if tf_source == "backtest_header" else "timeframe"
    else:
        style_primary = ""
    if primary in ("dca",) and "dca_accumulation" not in style_tags:
        style_tags.append("dca_accumulation")
        style_primary = "dca_accumulation"
    if "hft" in style_tags:
        style_primary = "hft"
    if bool(re.search(r"\b(close all|flat|exit) (positions? )?(at|before) (the )?(end of (the )?day|market close|session close|close of day)", all_low)) or "no overnight" in all_low:
        if "day_trading" not in style_tags:
            style_tags.append("day_trading")
    holding = {"hft": "seconds-minutes", "scalping": "minutes", "intraday": "minutes-hours",
               "day_trading": "hours (flat by close)", "swing": "days-weeks",
               "position": "weeks-months", "overnight": "overnight", "dca_accumulation": "long-term accumulation"}.get(style_primary, "")

    # ---------------- markets ----------------
    market_tags = []
    market_scores = {}
    for mk, kws in MARKET_KEYWORDS.items():
        s_n, _ = kw_score(name_low, kws)
        s_d, _ = kw_score(all_low, kws)
        market_scores[mk] = s_n * 4 + s_d
    # tickers (case-sensitive) in name / title / description
    inst = []
    src_for_tickers = f"{name_spaced} {title} {desc_clean[:5000]}"
    for tk in INSTRUMENT_TICKERS:
        if re.search(rf"(?<![A-Za-z]){re.escape(tk)}(?![A-Za-z])", src_for_tickers):
            inst.append(tk)
    for w, tk in INSTRUMENT_WORDS.items():
        if tk not in inst and re.search(r"(?<![a-z0-9])" + re.escape(w) + r"(?![a-z0-9])", all_low):
            inst.append(tk)
    # ticker -> market boosts
    crypto_tk = {"BTC", "XBT", "ETH", "SOL", "BNB", "DOGE", "XRP", "ADA", "LTC", "BCH", "EOS", "TRX", "AVAX", "MATIC", "DOT", "LINK", "ATOM", "SHIB", "PEPE", "TRUMP", "TRB", "USDT", "USDC", "BUSD"}
    fx_tk = {"EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "USDCHF", "NZDUSD", "EURJPY", "GBPJPY", "EURGBP", "USDINR", "EUR", "JPY", "GBP"}
    idx_tk = {"SPY", "QQQ", "IWM", "ES", "NQ", "YM", "RTY", "MES", "MNQ", "SPX", "NDX", "DJI", "VIX", "DAX", "FTSE", "CAC", "HSI", "NIFTY", "BANKNIFTY", "SENSEX", "NIKKEI", "N225", "KOSPI", "ASX", "US30", "US100", "US500", "NAS100", "GER40", "NASDAQ", "CSI300"}
    fut_tk = {"ES", "NQ", "YM", "RTY", "MES", "MNQ", "CL", "GC", "SI", "NG", "HG", "ZB", "ZN"}
    com_tk = {"CL", "GC", "SI", "NG", "HG", "XAUUSD", "XAGUSD", "XAU", "XAG", "WTI", "BRENT", "GOLD", "SILVER", "CRUDE", "OIL", "NATGAS", "COPPER", "REBAR", "SOYBEAN", "IRONORE"}
    stk_tk = {"AAPL", "TSLA", "NVDA", "MSFT", "AMZN", "GOOG", "GOOGL", "META", "AMD", "NFLX", "COIN", "MSTR", "GME", "AMC", "BABA", "TQQQ", "SQQQ", "SOXL", "TLT", "GLD", "SLV", "USO", "A-SHARES"}
    for tk in inst:
        if tk in crypto_tk: market_scores["crypto"] += 3
        if tk in fx_tk: market_scores["forex"] += 3
        if tk in idx_tk: market_scores["indices"] += 3
        if tk in fut_tk: market_scores["futures"] += 3
        if tk in com_tk: market_scores["commodities"] += 3
        if tk in stk_tk: market_scores["stocks"] += 3
    # options: avoid pine `options=` noise by only using text (already), but "expiration" etc. also occurs in crypto futures; require >=2
    for mk, sc in market_scores.items():
        thr = 2 if mk == "crypto" else 3
        if sc >= thr:
            market_tags.append(mk)
    if bt.get("_eid", "").lower().startswith("futures_") and "futures" not in market_tags and kind == "strategy":
        pass  # backtest header is an FMZ default; don't trust it for tagging
    if market_tags:
        asset_primary = max(market_tags, key=lambda m: market_scores[m])
        if asset_primary == "futures" and "crypto" in market_tags:
            asset_primary = "crypto"
    else:
        asset_primary = "generic"
    is_crypto_perp = ("crypto" in market_tags and ("perp" in all_low or "futures" in market_tags or "contract" in all_low)) or bool(re.search(r"perp|swap", name_low))
    bt_symbol = bt.get("_currency", "")

    # ---------------- direction ----------------
    n_long = len(re.findall(r"strategy\.long\b", code)) + len(re.findall(r"\b(OpenLong|Buy)\s*\(", code)) \
        + len(re.findall(r"strategy\.entry\s*\([^,]+,\s*(?:long\s*=\s*)?true", code))
    n_short = len(re.findall(r"strategy\.short\b", code)) + len(re.findall(r"\b(OpenShort|Sell)\s*\(", code)) \
        + len(re.findall(r"strategy\.entry\s*\([^,]+,\s*(?:long\s*=\s*)?false", code))
    if re.search(r"long[- ]only|only long|longs? only|buy[- ]only", all_low):
        direction = "long_only"
    elif re.search(r"short[- ]only|only short|shorts? only|sell[- ]only", all_low):
        direction = "short_only"
    elif lang_norm == "pine":
        if n_long and n_short:
            direction = "long_short"
        elif n_long:
            direction = "long_only"
        elif n_short:
            direction = "short_only"
        else:
            direction = "unknown"
    else:
        if re.search(r"OpenShort|\.Sell\s*\(", code) and re.search(r"OpenLong|\.Buy\s*\(", code):
            direction = "long_short"
        elif re.search(r"\.Buy\s*\(|OpenLong", code):
            direction = "long_only" if not re.search(r"\.Sell\s*\(", code) else "long_short"
        else:
            direction = "unknown"

    # ---------------- exits / risk mgmt ----------------
    has_sl = bool(re.search(r"stop[- _]?loss|\bsl\b|stoploss|strategy\.exit\([^)]*(loss|stop)\s*=|stop_level|stopprice|stop price|stop_price|\bstop\s*=", txt))
    has_tp = bool(re.search(r"take[- _]?profit|\btp\b|takeprofit|profit target|target price|strategy\.exit\([^)]*(profit|limit)\s*=|profit_level|\blimit\s*=", txt))
    has_trail = bool(re.search(r"trail(ing)?[- _]?(stop|sl|offset|points|price)|chandelier|trailing|trail_points|trail_offset", txt))
    has_breakeven = bool(re.search(r"break[- ]?even", txt))
    has_time_exit = bool(re.search(r"time[- ]based exit|exit after \d+|bars? since entry|max(imum)? (holding|bars|duration)|holding period|time stop|close at end of day|exit at \d|close after \d+ (bars|candles)", txt))
    has_partial_tp = bool(re.search(r"partial (profit|take|exit|close)|scale[- ]out|scaling out|tp1|tp2|first target|second target|qty_percent\s*=\s*[1-9]", txt))
    exit_methods = []
    if re.search(r"atr[- ]?(based|multiple|multiplier)?[- ]?(stop|sl|trailing|take|tp|target)|(stop|sl|target|tp)[^.\n]{0,40}\batr\b|\batr\b[^.\n]{0,40}(stop|sl|target|tp)", txt):
        exit_methods.append("atr_based")
    if re.search(r"(stop|sl|tp|take profit|target)[^.\n]{0,30}\d+(\.\d+)?\s*%|\d+(\.\d+)?\s*%\s*(stop|sl|take|tp|target)|stop_?loss_?perc|tp_?perc|(stop|profit|target)[^.\n]{0,20}percent", txt):
        exit_methods.append("fixed_percent")
    if (has_sl or has_tp) and re.search(r"\bpips?\b|\bticks?\b|(stop|target|tp|sl)[^.\n]{0,25}\bpoints?\b|\bpoints?\b[^.\n]{0,25}(stop|target|tp|sl)", txt):
        exit_methods.append("pips_ticks_points")
    if re.search(r"risk[- /]?reward|reward[- /]?risk|\brr\b|r:r|risk-to-reward|risk to reward", txt):
        exit_methods.append("risk_reward_ratio")
    if has_trail:
        exit_methods.append("trailing")
    if re.search(r"opposite signal|reverse signal|signal reversal|cross(es|ing)? (back|below|above)|exit (when|on|if) .*(cross|signal)|strategy\.close\(", txt):
        exit_methods.append("signal_based")
    if re.search(r"(swing|previous|recent|last)[- ](high|low)[^.\n]{0,40}(stop|sl)|(stop|sl)[^.\n]{0,40}(swing|previous|recent|last) (high|low)|structure[- ]based stop", txt):
        exit_methods.append("structure_based")
    if has_time_exit:
        exit_methods.append("time_based")
    if has_breakeven:
        exit_methods.append("breakeven")
    if has_partial_tp:
        exit_methods.append("partial_exits")
    if primary == "grid" or "grid" in tags:
        exit_methods.append("grid_take_profit")
    exit_methods = uniq(exit_methods)

    # position sizing
    qty_type = decl.get("default_qty_type", "").replace("strategy.", "")
    qty_value = decl.get("default_qty_value", "")
    risk_based_sizing = bool(re.search(r"risk (per|of|%)|% risk|percent risk|risk percent|position siz|kelly|fixed fractional|volatility[- ]adjusted (position|size)|risk-based (position|sizing)|account risk", txt))
    pyramiding_n = decl.get("pyramiding", "")
    try:
        pyramiding_n_i = int(float(pyramiding_n)) if pyramiding_n else 0
    except ValueError:
        pyramiding_n_i = 0
    has_pyramiding = pyramiding_n_i > 1 or bool(re.search(r"pyramid|add(ing)? to (the )?position|scale in|scaling in|averaging down|average down|add position", txt))
    max_dd_control = bool(re.search(r"max(imum)? (daily )?(drawdown|loss)|daily loss limit|loss limit|drawdown (limit|control|protection)|equity (stop|protection)|circuit breaker|strategy\.risk\.", txt))
    has_time_filter = bool(re.search(r"session|time filter|trading hours|dayofweek|time window|kill ?zone|\btime\(\s*timeframe|input\.session|input\.time\b|hour\s*[<>=]|start hour|end hour|market open|market close", txt))
    has_trend_filter = bool(re.search(r"trend filter|filter[^.\n]{0,30}trend|(above|below) (the )?\d+[- ]?(ema|sma|ma)\b|200[- ]?(ema|sma|ma)|higher timeframe trend|htf trend|only (long|buy) (when|if|above)|only (short|sell) (when|if|below)", txt))
    has_volume_filter = bool(re.search(r"volume (filter|confirmation|threshold|above|greater)|volume\s*>\s*|relative volume|rvol|volume spike", txt))
    has_volatility_filter = bool(re.search(r"volatility filter|atr filter|atr\s*>|adx\s*>|adx threshold|choppiness|chop filter|squeeze|range filter|bb ?width|bbw", txt))
    uses_mtf = bool(re.search(r"security\s*\(|request\.security", code)) or fam_scores.get("multi_timeframe", 0) >= 3
    uses_alerts = bool(re.search(r"\balert\s*\(|alertcondition\s*\(|webhook", code_nc_low))
    uses_external_api = bool(re.search(r"\bHttpQuery\b|requests\.|fetch\(|openai|api\.", code))

    # ---------------- leverage ----------------
    lev_vals = []
    for m in re.finditer(r"(\d+(?:\.\d+)?)\s*[xX×]\s*leverage", all_low):
        lev_vals.append(float(m.group(1)))
    for m in re.finditer(r"leverage\s*(?:of|:|=|is|at|to)?\s*(\d+(?:\.\d+)?)\s*[xX×]?", all_low):
        lev_vals.append(float(m.group(1)))
    for m in re.finditer(r"SetMarginLevel\s*\(\s*(\d+)", code):
        lev_vals.append(float(m.group(1)))
    for m in re.finditer(r"(\d+)\s*(?:times|x) (?:margin|leverage)", all_low):
        lev_vals.append(float(m.group(1)))
    ml = decl.get("margin_long", "")
    try:
        if ml and float(ml) > 0 and float(ml) < 100:
            lev_vals.append(round(100.0 / float(ml), 1))
    except ValueError:
        pass
    lev_vals = [v for v in lev_vals if 1 <= v <= 500]
    leverage_value = max(lev_vals) if lev_vals else ""
    leverage_mentioned = bool(lev_vals) or ("leverage" in all_low) or ("margin" in all_low and is_crypto_perp)

    # ---------------- claimed metrics ----------------
    win_rate = first_num(r"win(?:ning)? rate[^.\n\d%]{0,40}?(\d{1,3}(?:\.\d+)?)\s*%|(\d{1,3}(?:\.\d+)?)\s*%\s*win(?:ning)? rate|(\d{1,3}(?:\.\d+)?)\s*%\s*(?:of trades are )?profitable trades|percent profitable[^.\n\d%]{0,20}(\d{1,3}(?:\.\d+)?)", all_low)
    profit_factor = first_num(r"profit factor[^.\n\d]{0,30}(\d+(?:\.\d+)?)", all_low)
    max_dd = first_num(r"(?:max(?:imum)?\s+)?drawdown[^.\n\d%]{0,40}?(\d{1,3}(?:\.\d+)?)\s*%|(\d{1,3}(?:\.\d+)?)\s*%\s*(?:max(?:imum)?\s+)?drawdown", all_low)
    net_profit = first_num(r"(?:net profit|net return|total return|returns?|profit)[^.\n\d%]{0,30}?(\d{1,4}(?:\.\d+)?)\s*%|(\d{1,4}(?:\.\d+)?)\s*%\s*(?:net profit|return|profit)", all_low)
    sharpe = first_num(r"sharpe(?: ratio)?[^.\n\d]{0,30}(\d+(?:\.\d+)?)", all_low)
    rr = ""
    m = re.search(r"(?:risk[- /]?(?:to[- ])?reward|reward[- /]?(?:to[- ])?risk|r:r|rr)[^.\n\d]{0,30}(\d+(?:\.\d+)?)\s*[:/]\s*(\d+(?:\.\d+)?)", all_low)
    if m:
        rr = f"{m.group(1)}:{m.group(2)}"
    else:
        m = re.search(r"(\d+(?:\.\d+)?)\s*[:/]\s*(\d+(?:\.\d+)?)\s*(?:risk[- ]?reward|reward[- ]?risk|rr\b|r:r)", all_low)
        if m:
            rr = f"{m.group(1)}:{m.group(2)}"
    num_trades = first_num(r"(\d{2,5})\s*(?:trades|closed trades|total trades)", all_low)

    # profitability claim
    if re.search(r"not profitable|unprofitable|loses money|losing strategy|negative (return|expectancy)|does not work|doesn't work|no longer works|abandoned", all_low):
        claimed_profitable = "no"
    elif re.search(r"profitable|positive expect|high profit|good profit|consistent profit|steady profit|good results|excellent results|great results|outperform", all_low):
        claimed_profitable = "yes"
    else:
        claimed_profitable = "unknown"
    has_backtest_image = bool(re.search(r"!\[.*?\]\(", desc))
    has_backtest_header = bool(bt)

    # ---------------- regime ----------------
    regime_mentions = []
    if re.search(r"trending market|strong trend|trend market|in trends", all_low):
        regime_mentions.append("trending")
    if re.search(r"ranging|sideways|range-bound|oscillating market|choppy|consolidat|flat market", all_low):
        regime_mentions.append("ranging")
    if re.search(r"high volatility|volatile market|volatility expansion", all_low):
        regime_mentions.append("volatile")
    if re.search(r"low volatility|quiet market|calm market", all_low):
        regime_mentions.append("low_volatility")
    regime_fit = {
        "trend_following": "trending", "momentum": "trending", "breakout": "trending/volatile",
        "mean_reversion": "ranging", "grid": "ranging", "martingale": "ranging",
        "oscillator": "ranging", "arbitrage": "any", "pairs_trading": "ranging(spread)",
        "market_making": "ranging/low_volatility", "hedging": "any", "dca": "any(long bias)",
        "scalping": "liquid/volatile", "volatility": "volatile", "smart_money_concepts": "trending",
        "support_resistance": "ranging/trending", "candlestick_pattern": "any", "chart_pattern": "any",
        "seasonality_time": "any", "machine_learning": "any", "statistical": "any",
        "portfolio_rotation": "trending", "options": "depends", "divergence": "reversal",
        "volume": "any", "channel": "ranging", "swing_structure": "trending",
    }.get(primary, "")
    if re.search(r"(suitable|works? (best|well)|performs? (best|better|well)|ideal|designed) (for|in) (strong(ly)? )?trending", all_low):
        regime_fit = "trending"
    elif re.search(r"(suitable|works? (best|well)|performs? (best|better|well)|ideal|designed) (for|in) (ranging|sideways|range-bound|oscillating|choppy)", all_low):
        regime_fit = "ranging"

    # ---------------- repaint risk ----------------
    repaint_reasons = []
    if "lookahead_on" in code:
        repaint_reasons.append("lookahead_on")
    if re.search(r"security\s*\(", code) and not re.search(r"security\s*\([^)]*\[\s*1\s*\]", code) and "lookahead_off" not in code:
        repaint_reasons.append("security_without_offset")
    if "barstate.isrealtime" in code:
        repaint_reasons.append("barstate.isrealtime")
    if decl.get("calc_on_every_tick", "").lower() == "true":
        repaint_reasons.append("calc_on_every_tick")
    if re.search(r"\bhigh\b|\blow\b", code_nc_low) and re.search(r"strategy\.exit\([^)]*(limit|stop)\s*=", code) and decl.get("process_orders_on_close", "").lower() == "true":
        repaint_reasons.append("intrabar_fill_assumption")
    repaint_risk = "high" if "lookahead_on" in repaint_reasons else ("medium" if repaint_reasons else "low")

    # ---------------- risk mgmt score & risk level ----------------
    rm_score = sum([has_sl, has_tp, has_trail, risk_based_sizing, max_dd_control])
    risk_pts = 2
    reasons = []
    if primary == "martingale" or "martingale" in tags:
        risk_pts += 2; reasons.append("martingale")
    if primary == "grid" and not has_sl:
        risk_pts += 1; reasons.append("grid_no_sl")
    if kind == "strategy" and not has_sl:
        risk_pts += 1; reasons.append("no_stop_loss")
    if leverage_value and float(leverage_value) >= 5:
        risk_pts += 1; reasons.append(f"leverage_{leverage_value:g}x")
    if has_pyramiding:
        risk_pts += 0.5; reasons.append("pyramiding")
    try:
        if qty_type == "percent_of_equity" and qty_value and float(qty_value) >= 100:
            risk_pts += 0.5; reasons.append("100pct_equity_per_trade")
    except ValueError:
        pass
    if style_primary in ("hft", "scalping"):
        risk_pts += 1; reasons.append("execution_sensitive")
    if repaint_risk == "high":
        risk_pts += 1; reasons.append("repaint")
    if has_sl and has_tp:
        risk_pts -= 1; reasons.append("sl_and_tp")
    if risk_based_sizing:
        risk_pts -= 1; reasons.append("risk_sizing")
    if max_dd_control:
        risk_pts -= 1; reasons.append("dd_control")
    if primary in ("dca", "hedging", "arbitrage", "market_making") and not leverage_value:
        risk_pts -= 1; reasons.append("low_risk_family")
    risk_pts = max(0, risk_pts)
    risk_level = "low" if risk_pts < 2 else "medium" if risk_pts < 3 else "high" if risk_pts < 4 else "very_high"

    # ---------------- complexity ----------------
    code_lines = len([l for l in code.splitlines() if l.strip()])
    ind_count = len([i for i in indicators if i not in ("Volume", "Session/Time", "Highest/Lowest (channel)")])
    if code_lines < 60 and ind_count <= 2:
        complexity = "low"
    elif code_lines > 250 or ind_count >= 6:
        complexity = "high"
    else:
        complexity = "medium"

    # ---------------- buildability ----------------
    build = 0
    if code_lines > 10: build += 3
    if lang_norm in ("pine", "python", "javascript"): build += 1
    if desc.strip(): build += 1
    if "## " in desc or "##" in desc: build += 1
    if has_sl: build += 1
    if has_tp or has_trail: build += 1
    if tf_primary and tf_source != "none": build += 1
    if args: build += 1
    if kind in ("strategy", "tutorial_strategy"): build += 1
    if repaint_risk == "high": build -= 2
    build = max(0, min(10, build))

    # ---------------- excerpts ----------------
    overview = desc_subsection(desc, ("overview", "summary", "introduction"))
    if not overview:
        paras = [p for p in re.split(r"\n\s*\n", desc_clean) if p.strip() and not p.strip().startswith("#") and not p.strip().startswith("|")]
        overview = paras[0] if paras else ""
    logic = desc_subsection(desc, ("principle", "logic", "how it works", "mechanism", "rules"))
    advantages = desc_subsection(desc, ("advantage", "strength", "benefit", "pros"))
    risks = desc_subsection(desc, ("risk", "weakness", "limitation", "cons", "drawback"))
    optim = desc_subsection(desc, ("optimization", "improvement", "enhancement", "future"))
    entry_sent = ""
    exit_sent = ""
    for sent in re.split(r"(?<=[.!?])\s+|\n+", feature_desc):
        sl_ = sent.lower()
        if not entry_sent and re.search(r"\b(long|buy)\b", sl_) and re.search(r"\b(when|if|once|after)\b", sl_):
            entry_sent = clean_excerpt(sent, 300)
        if not exit_sent and re.search(r"\b(exit|close|stop[- ]loss|take[- ]profit)\b", sl_) and re.search(r"\b(when|if|once|after|at)\b", sl_):
            exit_sent = clean_excerpt(sent, 300)
        if entry_sent and exit_sent:
            break

    fmz_id = re.search(r"/strategy/(\d+)", detail)
    year = last_mod[:4] if last_mod else ""
    src_hash = hashlib.md5(re.sub(r"\s+", "", code).encode()).hexdigest()[:12] if code.strip() else ""

    # pine version
    pv = re.search(r"//@version=(\d+)", code)
    pine_version = pv.group(1) if pv else ""

    args_str = "; ".join(f"{a}={d}" + (f" ({t})" if t else "") for a, d, t in args)
    if len(args_str) > 600:
        args_str = args_str[:600].rsplit(";", 1)[0] + "; …"

    return {
        "id": "",
        "file": path.name,
        "name": name,
        "author": author,
        "fmz_id": fmz_id.group(1) if fmz_id else "",
        "fmz_url": detail if detail.startswith("http") else "",
        "last_modified": last_mod,
        "year": year,
        "language": lang_norm,
        "pine_version": pine_version,
        "kind": kind,
        "strategy_family": primary,
        "strategy_tags": "|".join(secondary),
        "all_family_scores": "|".join(f"{f}:{fam_scores[f]:g}" for f in tags_sorted),
        "trading_style": style_primary,
        "style_source": style_source,
        "style_tags": "|".join(uniq(style_tags)),
        "holding_period": holding,
        "timeframe": tf_primary,
        "timeframe_source": tf_source,
        "timeframes_all": "|".join(tf_all),
        "mtf_timeframes": "|".join(tf_mtf),
        "asset_class": asset_primary,
        "market_tags": "|".join(market_tags),
        "instruments": "|".join(inst[:12]),
        "crypto_perpetual": is_crypto_perp,
        "direction": direction,
        "indicators": "|".join(indicators),
        "indicator_count": ind_count,
        "has_stop_loss": has_sl,
        "has_take_profit": has_tp,
        "has_trailing_stop": has_trail,
        "has_breakeven": has_breakeven,
        "has_partial_exits": has_partial_tp,
        "has_time_exit": has_time_exit,
        "exit_methods": "|".join(exit_methods),
        "risk_based_sizing": risk_based_sizing,
        "max_dd_or_loss_control": max_dd_control,
        "pyramiding": has_pyramiding,
        "pyramiding_n": pyramiding_n_i if pyramiding_n_i else "",
        "has_time_filter": has_time_filter,
        "has_trend_filter": has_trend_filter,
        "has_volume_filter": has_volume_filter,
        "has_volatility_filter": has_volatility_filter,
        "uses_multi_timeframe": uses_mtf,
        "uses_alerts_webhook": uses_alerts,
        "uses_external_api": uses_external_api,
        "leverage_mentioned": leverage_mentioned,
        "leverage_value": leverage_value,
        "risk_mgmt_score": rm_score,
        "risk_level": risk_level,
        "risk_reasons": "|".join(reasons),
        "repaint_risk": repaint_risk,
        "repaint_reasons": "|".join(repaint_reasons),
        "regime_fit": regime_fit,
        "regime_mentions": "|".join(regime_mentions),
        "complexity": complexity,
        "code_lines": code_lines,
        "num_arguments": len(args),
        "buildability_score": build,
        "claimed_profitable": claimed_profitable,
        "claimed_win_rate_pct": win_rate,
        "claimed_profit_factor": profit_factor,
        "claimed_max_drawdown_pct": max_dd,
        "claimed_net_profit_pct": net_profit,
        "claimed_sharpe": sharpe,
        "claimed_risk_reward": rr,
        "claimed_num_trades": num_trades,
        "has_backtest_image": has_backtest_image,
        "has_backtest_header": has_backtest_header,
        "bt_start": bt.get("start", ""),
        "bt_end": bt.get("end", ""),
        "bt_period": bt_period,
        "bt_base_period": bt_base,
        "bt_exchange": bt.get("_eid", ""),
        "bt_symbol": bt_symbol,
        "bt_balance": bt.get("_balance", ""),
        "pine_initial_capital": decl.get("initial_capital", ""),
        "pine_qty_type": qty_type,
        "pine_qty_value": qty_value,
        "pine_commission_type": decl.get("commission_type", "").replace("strategy.commission.", ""),
        "pine_commission_value": decl.get("commission_value", ""),
        "pine_slippage": decl.get("slippage", ""),
        "pine_margin_long": decl.get("margin_long", ""),
        "pine_margin_short": decl.get("margin_short", ""),
        "pine_currency": decl.get("currency", "").replace("currency.", ""),
        "pine_overlay": decl.get("overlay", ""),
        "pine_calc_on_every_tick": decl.get("calc_on_every_tick", ""),
        "pine_process_orders_on_close": decl.get("process_orders_on_close", ""),
        "source_hash": src_hash,
        "description_words": len(desc_clean.split()),
        "overview": clean_excerpt(overview, 500),
        "logic_excerpt": clean_excerpt(logic, 500),
        "entry_rule_excerpt": entry_sent,
        "exit_rule_excerpt": exit_sent,
        "advantages_excerpt": clean_excerpt(advantages, 300),
        "risks_excerpt": clean_excerpt(risks, 300),
        "optimization_excerpt": clean_excerpt(optim, 300),
        "arguments": args_str,
    }


# --------------------------------------------------------------------------
# Index generation
# --------------------------------------------------------------------------

def md_link(row: dict) -> str:
    return f"[{row['name'][:90]}](../../strategies/{quote(row['file'])})"


def md_link_root(row: dict) -> str:
    return f"[{row['name'][:90]}](../strategies/{quote(row['file'])})"


def table(rows: list[dict], link_fn, cols: list[tuple[str, str]]) -> str:
    out = ["| " + " | ".join(h for h, _ in cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for r in rows:
        cells = []
        for h, key in cols:
            if key == "_link":
                cells.append(link_fn(r))
            else:
                v = str(r.get(key, "")).replace("|", ", ").replace("\n", " ")
                if len(v) > 60:
                    v = v[:57].rsplit(",", 1)[0] + "…"
                cells.append(v)
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


STD_COLS = [("Strategy", "_link"), ("Family", "strategy_family"), ("Style", "trading_style"),
            ("TF", "timeframe"), ("Asset", "asset_class"), ("Dir", "direction"),
            ("SL/TP/Trail", "_sltp"), ("Risk", "risk_level"), ("Build", "buildability_score"),
            ("Indicators", "indicators"), ("Lang", "language")]


def prep_rows(rows):
    for r in rows:
        r["_sltp"] = f"{'SL' if r['has_stop_loss'] else '-'}/{'TP' if r['has_take_profit'] else '-'}/{'TR' if r['has_trailing_stop'] else '-'}"
    return rows


def write_group_index(subdir: str, title: str, key: str, rows: list[dict], multi: bool = False, min_count: int = 1, link_root=False) -> list[tuple[str, int, str]]:
    d = IDX_DIR / subdir
    d.mkdir(parents=True, exist_ok=True)
    groups: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        vals = str(r.get(key, "")).split("|") if multi else [str(r.get(key, ""))]
        for v in vals:
            v = v.strip() or "(none)"
            groups[v].append(r)
    entries = []
    for g, grs in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        if len(grs) < min_count:
            continue
        safe = re.sub(r"[^A-Za-z0-9._-]+", "_", g)[:60] or "none"
        fn = d / f"{safe}.md"
        grs_sorted = sorted(grs, key=lambda r: (-int(r["buildability_score"]), r["name"].lower()))
        body = [f"# {title}: {g}", "", f"{len(grs)} strategies. Sorted by buildability score (desc), then name.", "",
                "[← Back to catalog index](../../INDEX.md)", "",
                table(grs_sorted, md_link, STD_COLS)]
        fn.write_text("\n".join(body), encoding="utf-8")
        entries.append((g, len(grs), f"index/{subdir}/{safe}.md"))
    return entries


def build_indexes(rows: list[dict]):
    rows = prep_rows(rows)
    IDX_DIR.mkdir(parents=True, exist_ok=True)
    strat_rows = [r for r in rows if r["kind"] in ("strategy", "tutorial_strategy")]

    fam = write_group_index("by_family", "Strategy family", "strategy_family", strat_rows)
    tagidx = write_group_index("by_tag", "Strategy tag", "strategy_tags", strat_rows, multi=True, min_count=10)
    style = write_group_index("by_style", "Trading style", "trading_style", strat_rows)
    tf = write_group_index("by_timeframe", "Timeframe", "timeframe", strat_rows)
    asset = write_group_index("by_asset", "Asset class", "asset_class", strat_rows)
    mkt = write_group_index("by_market_tag", "Market tag", "market_tags", strat_rows, multi=True)
    risk = write_group_index("by_risk", "Risk level", "risk_level", strat_rows)
    lang = write_group_index("by_language", "Language", "language", rows)
    kind = write_group_index("by_kind", "File kind", "kind", rows)
    ind = write_group_index("by_indicator", "Indicator", "indicators", strat_rows, multi=True, min_count=25)
    auth = write_group_index("by_author", "Author", "author", rows, min_count=15)
    direction = write_group_index("by_direction", "Direction", "direction", strat_rows)
    regime = write_group_index("by_regime", "Market regime fit", "regime_fit", strat_rows)
    year = write_group_index("by_year", "Year", "year", rows)
    inst = write_group_index("by_instrument", "Instrument", "instruments", strat_rows, multi=True, min_count=5)
    exitm = write_group_index("by_exit_method", "Exit method", "exit_methods", strat_rows, multi=True, min_count=5)

    # top buildable
    top = sorted(strat_rows, key=lambda r: (-int(r["buildability_score"]), -int(r["risk_mgmt_score"]), r["name"].lower()))[:300]
    (IDX_DIR / "top_buildable.md").write_text(
        "# Top 300 most buildable strategies\n\nRanked by buildability score, then risk-management score.\n\n[← Back](../INDEX.md)\n\n" +
        table(top, md_link_root, STD_COLS).replace("](../strategies/", "](../../strategies/"), encoding="utf-8")
    # strategies with claimed metrics
    claimed = [r for r in strat_rows if r["claimed_win_rate_pct"] or r["claimed_profit_factor"] or r["claimed_max_drawdown_pct"] or r["claimed_sharpe"]]
    claimed.sort(key=lambda r: r["name"].lower())
    cols = [("Strategy", "_link"), ("Family", "strategy_family"), ("TF", "timeframe"), ("Win%", "claimed_win_rate_pct"),
            ("PF", "claimed_profit_factor"), ("MaxDD%", "claimed_max_drawdown_pct"), ("Net%", "claimed_net_profit_pct"),
            ("Sharpe", "claimed_sharpe"), ("R:R", "claimed_risk_reward"), ("Trades", "claimed_num_trades"), ("Claims profitable", "claimed_profitable")]
    (IDX_DIR / "claimed_performance.md").write_text(
        "# Strategies with claimed performance metrics\n\nNumbers are extracted from the author's description text (unverified).\n\n[← Back](../INDEX.md)\n\n" +
        table(claimed, md_link, cols), encoding="utf-8")
    # A-Z
    az = sorted(rows, key=lambda r: r["name"].lower())
    (IDX_DIR / "all_strategies_A-Z.md").write_text(
        f"# All {len(rows)} files A-Z\n\n[← Back](../INDEX.md)\n\n" + table(az, md_link, [("Name", "_link"), ("Kind", "kind"), ("Family", "strategy_family"), ("Style", "trading_style"), ("TF", "timeframe"), ("Asset", "asset_class"), ("Risk", "risk_level"), ("Build", "buildability_score"), ("Lang", "language"), ("Author", "author")]),
        encoding="utf-8")
    # duplicates by source hash
    by_hash = defaultdict(list)
    for r in rows:
        if r["source_hash"]:
            by_hash[r["source_hash"]].append(r)
    dups = {h: g for h, g in by_hash.items() if len(g) > 1}
    lines = [f"# Duplicate source groups\n\n{len(dups)} groups of files share identical source code (whitespace-insensitive).\n\n[← Back](../INDEX.md)\n"]
    for h, g in sorted(dups.items(), key=lambda kv: -len(kv[1])):
        lines.append(f"\n## {h} ({len(g)} files)\n")
        for r in g:
            lines.append(f"- {md_link(r)} — {r['author']}, {r['last_modified'][:10]}")
    (IDX_DIR / "duplicates.md").write_text("\n".join(lines), encoding="utf-8")

    # ---- main INDEX.md
    def section(title, entries, note=""):
        s = [f"## {title}", ""]
        if note:
            s += [note, ""]
        s.append("| Group | Count | Index |")
        s.append("|---|---|---|")
        for g, n, fn in entries:
            s.append(f"| {g} | {n} | [{fn.split('/')[-1][:-3]}]({fn}) |")
        s.append("")
        return "\n".join(s)

    n_strat = len(strat_rows)
    md = [
        "# Quant Trading Vault — Strategy Catalog Index",
        "",
        f"Database: [`strategies_db.csv`](strategies_db.csv) — {len(rows)} files, {n_strat} tradeable strategies, "
        f"{len(rows[0]) - 1} columns per row. Column definitions: [SCHEMA.md](SCHEMA.md).",
        "",
        "Rebuild with `python catalog/build_catalog.py`. Classification is rule-based (keyword + code analysis); "
        "treat tags as strong hints, not ground truth. Claimed performance figures come from author text and are unverified.",
        "",
        "## Quick links",
        "",
        "- [Top 300 most buildable strategies](index/top_buildable.md)",
        "- [Strategies with claimed performance metrics](index/claimed_performance.md)",
        "- [All files A-Z](index/all_strategies_A-Z.md)",
        "- [Duplicate source groups](index/duplicates.md)",
        "",
        section("By strategy family (primary)", fam),
        section("By secondary strategy tag", tagidx, "A strategy can carry several tags (min 10 strategies per tag shown)."),
        section("By trading style", style),
        section("By timeframe", tf, "Primary timeframe: from the name, then description, then FMZ backtest header (`timeframe_source` column says which)."),
        section("By asset class (primary)", asset),
        section("By market tag", mkt),
        section("By instrument mentioned", inst),
        section("By direction", direction),
        section("By exit method", exitm),
        section("By risk level", risk, "Heuristic: martingale, no stop loss, leverage ≥5x, pyramiding, 100% equity sizing raise it; SL+TP, risk sizing, drawdown control lower it."),
        section("By market regime fit", regime),
        section("By indicator", ind, "Min 25 strategies per indicator shown."),
        section("By language", lang),
        section("By file kind", kind),
        section("By author (15+ files)", auth),
        section("By year", year),
    ]
    (CAT_DIR / "INDEX.md").write_text("\n".join(md), encoding="utf-8")


SCHEMA_DOC = """# strategies_db.csv — column reference

Multi-value columns are `|`-separated. Booleans are `True`/`False`. Empty = unknown / not detected.

## Identity
| Column | Meaning |
|---|---|
| id | Sequential row id |
| file | File name under `strategies/` |
| name | Strategy name (from `> Name`) |
| author | FMZ author |
| fmz_id / fmz_url | Original FMZ strategy id / URL |
| last_modified / year | FMZ last-modified timestamp |
| language | pine / javascript / python / mylanguage / cpp |
| pine_version | `//@version=N` |
| kind | strategy, tutorial_strategy, indicator, library, template, utility, tutorial |
| source_hash | md5 of whitespace-stripped source (find duplicates) |

## Classification
| Column | Meaning |
|---|---|
| strategy_family | Primary logic family (trend_following, momentum, mean_reversion, breakout, grid, martingale, dca, arbitrage, pairs_trading, hedging, market_making, scalping, candlestick_pattern, chart_pattern, support_resistance, smart_money_concepts, volatility, volume, oscillator, statistical, machine_learning, seasonality_time, multi_timeframe, portfolio_rotation, options, divergence, channel, swing_structure, renko_range_bars, news_sentiment, moving_average, unclassified) |
| strategy_tags | Up to 6 secondary families (incl. supporting: pyramiding, trailing_exit, signal_bot_execution, moving_average, channel, multi_timeframe, swing_structure) |
| all_family_scores | family:score pairs that passed threshold, descending |
| trading_style | hft, scalping, intraday, day_trading, swing, position, overnight, dca_accumulation |
| style_tags | All style tags detected |
| holding_period | Human-readable holding horizon implied by style |
| timeframe | Primary chart timeframe (1m…1mo; `1mo` = monthly, `1m` = one minute) |
| timeframe_source | name / description / backtest_header / none — backtest_header is an FMZ default and weak evidence |
| timeframes_all | Every timeframe mentioned in name, description or code |
| mtf_timeframes | Timeframes requested via `request.security` / timeframe inputs |
| asset_class | Primary: crypto, forex, stocks, indices, futures, commodities, options, spot, unspecified |
| market_tags | All market tags detected |
| instruments | Tickers / instruments named in text (BTC, ETH, ES, NQ, EURUSD, GOLD, NIFTY…) |
| crypto_perpetual | Mentions perpetual / swap / crypto futures |
| direction | long_only / short_only / long_short / unknown |
| regime_fit | Market regime the strategy is designed for (family default, overridden by explicit text) |
| regime_mentions | Regimes discussed in the text |

## Mechanics
| Column | Meaning |
|---|---|
| indicators / indicator_count | Technical indicators detected in code or text |
| has_stop_loss / has_take_profit / has_trailing_stop / has_breakeven / has_partial_exits / has_time_exit | Exit features |
| exit_methods | atr_based, fixed_percent, pips_ticks_points, risk_reward_ratio, trailing, signal_based, structure_based, time_based, breakeven, partial_exits, grid_take_profit |
| risk_based_sizing | Position size derived from risk % / volatility |
| max_dd_or_loss_control | Daily-loss / drawdown / equity-stop logic |
| pyramiding / pyramiding_n | Adds to open positions (`pyramiding=` in Pine or text) |
| has_time_filter / has_trend_filter / has_volume_filter / has_volatility_filter | Entry filters |
| uses_multi_timeframe | `request.security` or MTF wording |
| uses_alerts_webhook | Pine alerts / webhooks present |
| uses_external_api | HTTP / API calls in code |
| leverage_mentioned / leverage_value | Leverage discussed; max numeric leverage found (x) |

## Scores
| Column | Meaning |
|---|---|
| risk_mgmt_score | 0-5: SL, TP, trailing, risk sizing, drawdown control |
| risk_level / risk_reasons | low / medium / high / very_high with reasons |
| repaint_risk / repaint_reasons | low / medium / high (lookahead_on, security w/o offset, isrealtime, calc_on_every_tick) |
| complexity | low / medium / high from code length + indicator count |
| code_lines / num_arguments | Size metrics |
| buildability_score | 0-10: has source, mainstream language, description, structured description, SL, TP/trail, timeframe, args table, is a strategy; -2 if repaint high |

## Claimed performance (unverified, parsed from author text)
| Column | Meaning |
|---|---|
| claimed_profitable | yes / no / unknown based on wording |
| claimed_win_rate_pct, claimed_profit_factor, claimed_max_drawdown_pct, claimed_net_profit_pct, claimed_sharpe, claimed_risk_reward, claimed_num_trades | First numeric mention found |
| has_backtest_image | Description embeds a screenshot (usually a backtest) |

## Backtest header (FMZ `/*backtest ... */`) — mostly platform defaults
| Column | Meaning |
|---|---|
| has_backtest_header, bt_start, bt_end, bt_period, bt_base_period, bt_exchange, bt_symbol, bt_balance | As written in the header |

## Pine `strategy()` declaration
| Column | Meaning |
|---|---|
| pine_initial_capital, pine_qty_type, pine_qty_value, pine_commission_type, pine_commission_value, pine_slippage, pine_margin_long, pine_margin_short, pine_currency, pine_overlay, pine_calc_on_every_tick, pine_process_orders_on_close | Declaration kwargs |

## Text excerpts
| Column | Meaning |
|---|---|
| description_words | Length of description |
| overview | First 500 chars of Overview / Summary section |
| logic_excerpt | Strategy Principles / Logic section |
| entry_rule_excerpt / exit_rule_excerpt | First sentence describing entry / exit conditions |
| advantages_excerpt / risks_excerpt / optimization_excerpt | Section excerpts |
| arguments | `name=default (description); …` from the Strategy Arguments table (truncated at 600 chars) |
"""


def _safe_analyze(f: Path):
    try:
        return analyze(f)
    except Exception as e:  # keep going, report
        print(f"ERROR {f.name}: {e}", file=sys.stderr)
        return None


def main():
    files = [f for f in sorted(STRAT_DIR.glob("*.md")) if f.name.lower() != "readme.md"]
    from multiprocessing import Pool, cpu_count
    with Pool(max(1, cpu_count() - 1)) as pool:
        results = pool.map(_safe_analyze, files, chunksize=20)
    rows = [r for r in results if r]
    # author counts
    ac = Counter(r["author"] for r in rows)
    for i, r in enumerate(rows, 1):
        r["id"] = i
        r["author_file_count"] = ac[r["author"]]
    # column order: put author_file_count after author
    cols = list(rows[0].keys())
    cols.remove("author_file_count")
    cols.insert(cols.index("author") + 1, "author_file_count")

    CAT_DIR.mkdir(exist_ok=True)
    with open(CAT_DIR / "strategies_db.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    (CAT_DIR / "SCHEMA.md").write_text(SCHEMA_DOC, encoding="utf-8")
    build_indexes(rows)

    # stats
    def cnt(key, multi=False, top=15):
        c = Counter()
        for r in rows:
            if multi:
                for v in str(r[key]).split("|"):
                    if v:
                        c[v] += 1
            else:
                c[str(r[key])] += 1
        return c.most_common(top)

    print(f"rows: {len(rows)}  cols: {len(cols)}")
    for key, multi in [("kind", False), ("strategy_family", False), ("trading_style", False), ("timeframe", False),
                       ("timeframe_source", False), ("asset_class", False), ("market_tags", True), ("direction", False),
                       ("risk_level", False), ("repaint_risk", False), ("complexity", False), ("buildability_score", False),
                       ("exit_methods", True), ("indicators", True), ("claimed_profitable", False), ("language", False)]:
        print(f"\n{key}: {cnt(key, multi)}")


if __name__ == "__main__":
    main()
