# Quant Trading Vault — Strategy Catalog Index

Database: [`strategies_db.csv`](strategies_db.csv) — 5806 files, 5321 tradeable strategies, 100 columns per row. Column definitions: [SCHEMA.md](SCHEMA.md).

Rebuild with `python catalog/build_catalog.py`. Classification is rule-based (keyword + code analysis); treat tags as strong hints, not ground truth. Claimed performance figures come from author text and are unverified.

## Quick links

- [Top 300 most buildable strategies](index/top_buildable.md)
- [Strategies with claimed performance metrics](index/claimed_performance.md)
- [All files A-Z](index/all_strategies_A-Z.md)
- [Duplicate source groups](index/duplicates.md)

## By strategy family (primary)

| Group | Count | Index |
|---|---|---|
| trend_following | 1886 | [trend_following](index/by_family/trend_following.md) |
| mean_reversion | 1019 | [mean_reversion](index/by_family/mean_reversion.md) |
| momentum | 596 | [momentum](index/by_family/momentum.md) |
| breakout | 443 | [breakout](index/by_family/breakout.md) |
| support_resistance | 193 | [support_resistance](index/by_family/support_resistance.md) |
| moving_average | 177 | [moving_average](index/by_family/moving_average.md) |
| candlestick_pattern | 136 | [candlestick_pattern](index/by_family/candlestick_pattern.md) |
| statistical | 83 | [statistical](index/by_family/statistical.md) |
| seasonality_time | 81 | [seasonality_time](index/by_family/seasonality_time.md) |
| unclassified | 72 | [unclassified](index/by_family/unclassified.md) |
| oscillator | 70 | [oscillator](index/by_family/oscillator.md) |
| volatility | 66 | [volatility](index/by_family/volatility.md) |
| scalping | 55 | [scalping](index/by_family/scalping.md) |
| grid | 50 | [grid](index/by_family/grid.md) |
| dca | 42 | [dca](index/by_family/dca.md) |
| smart_money_concepts | 41 | [smart_money_concepts](index/by_family/smart_money_concepts.md) |
| divergence | 39 | [divergence](index/by_family/divergence.md) |
| chart_pattern | 35 | [chart_pattern](index/by_family/chart_pattern.md) |
| martingale | 33 | [martingale](index/by_family/martingale.md) |
| machine_learning | 25 | [machine_learning](index/by_family/machine_learning.md) |
| market_making | 23 | [market_making](index/by_family/market_making.md) |
| hedging | 20 | [hedging](index/by_family/hedging.md) |
| volume | 19 | [volume](index/by_family/volume.md) |
| signal_bot_execution | 19 | [signal_bot_execution](index/by_family/signal_bot_execution.md) |
| multi_timeframe | 19 | [multi_timeframe](index/by_family/multi_timeframe.md) |
| trailing_exit | 18 | [trailing_exit](index/by_family/trailing_exit.md) |
| arbitrage | 12 | [arbitrage](index/by_family/arbitrage.md) |
| renko_range_bars | 10 | [renko_range_bars](index/by_family/renko_range_bars.md) |
| channel | 8 | [channel](index/by_family/channel.md) |
| options | 8 | [options](index/by_family/options.md) |
| portfolio_rotation | 7 | [portfolio_rotation](index/by_family/portfolio_rotation.md) |
| swing_structure | 5 | [swing_structure](index/by_family/swing_structure.md) |
| news_sentiment | 5 | [news_sentiment](index/by_family/news_sentiment.md) |
| pairs_trading | 4 | [pairs_trading](index/by_family/pairs_trading.md) |
| pyramiding | 2 | [pyramiding](index/by_family/pyramiding.md) |

## By secondary strategy tag

A strategy can carry several tags (min 10 strategies per tag shown).

| Group | Count | Index |
|---|---|---|
| moving_average | 3132 | [moving_average](index/by_tag/moving_average.md) |
| oscillator | 1752 | [oscillator](index/by_tag/oscillator.md) |
| signal_bot_execution | 1740 | [signal_bot_execution](index/by_tag/signal_bot_execution.md) |
| volatility | 1208 | [volatility](index/by_tag/volatility.md) |
| mean_reversion | 1144 | [mean_reversion](index/by_tag/mean_reversion.md) |
| trend_following | 1093 | [trend_following](index/by_tag/trend_following.md) |
| channel | 863 | [channel](index/by_tag/channel.md) |
| momentum | 782 | [momentum](index/by_tag/momentum.md) |
| multi_timeframe | 719 | [multi_timeframe](index/by_tag/multi_timeframe.md) |
| volume | 637 | [volume](index/by_tag/volume.md) |
| breakout | 629 | [breakout](index/by_tag/breakout.md) |
| trailing_exit | 502 | [trailing_exit](index/by_tag/trailing_exit.md) |
| (none) | 400 | [_none_](index/by_tag/_none_.md) |
| support_resistance | 326 | [support_resistance](index/by_tag/support_resistance.md) |
| seasonality_time | 239 | [seasonality_time](index/by_tag/seasonality_time.md) |
| candlestick_pattern | 235 | [candlestick_pattern](index/by_tag/candlestick_pattern.md) |
| swing_structure | 185 | [swing_structure](index/by_tag/swing_structure.md) |
| chart_pattern | 168 | [chart_pattern](index/by_tag/chart_pattern.md) |
| statistical | 140 | [statistical](index/by_tag/statistical.md) |
| scalping | 128 | [scalping](index/by_tag/scalping.md) |
| smart_money_concepts | 68 | [smart_money_concepts](index/by_tag/smart_money_concepts.md) |
| divergence | 65 | [divergence](index/by_tag/divergence.md) |
| pyramiding | 45 | [pyramiding](index/by_tag/pyramiding.md) |
| machine_learning | 38 | [machine_learning](index/by_tag/machine_learning.md) |
| options | 25 | [options](index/by_tag/options.md) |
| portfolio_rotation | 18 | [portfolio_rotation](index/by_tag/portfolio_rotation.md) |
| news_sentiment | 18 | [news_sentiment](index/by_tag/news_sentiment.md) |
| grid | 17 | [grid](index/by_tag/grid.md) |
| dca | 16 | [dca](index/by_tag/dca.md) |
| martingale | 16 | [martingale](index/by_tag/martingale.md) |
| hedging | 15 | [hedging](index/by_tag/hedging.md) |
| market_making | 13 | [market_making](index/by_tag/market_making.md) |
| arbitrage | 12 | [arbitrage](index/by_tag/arbitrage.md) |
| renko_range_bars | 11 | [renko_range_bars](index/by_tag/renko_range_bars.md) |

## By trading style

| Group | Count | Index |
|---|---|---|
| intraday | 2268 | [intraday](index/by_style/intraday.md) |
| swing | 1657 | [swing](index/by_style/swing.md) |
| position | 590 | [position](index/by_style/position.md) |
| scalping | 445 | [scalping](index/by_style/scalping.md) |
| (none) | 193 | [_none_](index/by_style/_none_.md) |
| hft | 108 | [hft](index/by_style/hft.md) |
| dca_accumulation | 40 | [dca_accumulation](index/by_style/dca_accumulation.md) |
| overnight | 13 | [overnight](index/by_style/overnight.md) |
| day_trading | 7 | [day_trading](index/by_style/day_trading.md) |

## By timeframe

Primary timeframe: from the name, then description, then FMZ backtest header (`timeframe_source` column says which).

| Group | Count | Index |
|---|---|---|
| 1d | 1873 | [1d](index/by_timeframe/1d.md) |
| 1h | 1391 | [1h](index/by_timeframe/1h.md) |
| 1m | 263 | [1m](index/by_timeframe/1m.md) |
| 2h | 254 | [2h](index/by_timeframe/2h.md) |
| 4h | 237 | [4h](index/by_timeframe/4h.md) |
| (none) | 222 | [_none_](index/by_timeframe/_none_.md) |
| 5m | 215 | [5m](index/by_timeframe/5m.md) |
| 15m | 187 | [15m](index/by_timeframe/15m.md) |
| 3h | 140 | [3h](index/by_timeframe/3h.md) |
| 30m | 120 | [30m](index/by_timeframe/30m.md) |
| 10m | 89 | [10m](index/by_timeframe/10m.md) |
| 3m | 83 | [3m](index/by_timeframe/3m.md) |
| 2d | 70 | [2d](index/by_timeframe/2d.md) |
| 45m | 44 | [45m](index/by_timeframe/45m.md) |
| 2m | 24 | [2m](index/by_timeframe/2m.md) |
| 1w | 20 | [1w](index/by_timeframe/1w.md) |
| 6h | 19 | [6h](index/by_timeframe/6h.md) |
| 3d | 15 | [3d](index/by_timeframe/3d.md) |
| 12h | 13 | [12h](index/by_timeframe/12h.md) |
| 1mo | 9 | [1mo](index/by_timeframe/1mo.md) |
| 4d | 9 | [4d](index/by_timeframe/4d.md) |
| 8h | 6 | [8h](index/by_timeframe/8h.md) |
| 5h | 5 | [5h](index/by_timeframe/5h.md) |
| 5d | 3 | [5d](index/by_timeframe/5d.md) |
| 20m | 2 | [20m](index/by_timeframe/20m.md) |
| 4m | 2 | [4m](index/by_timeframe/4m.md) |
| 15h | 1 | [15h](index/by_timeframe/15h.md) |
| 7d | 1 | [7d](index/by_timeframe/7d.md) |
| 14m | 1 | [14m](index/by_timeframe/14m.md) |
| 6m | 1 | [6m](index/by_timeframe/6m.md) |
| 7h | 1 | [7h](index/by_timeframe/7h.md) |
| 6d | 1 | [6d](index/by_timeframe/6d.md) |

## By asset class (primary)

| Group | Count | Index |
|---|---|---|
| generic | 4416 | [generic](index/by_asset/generic.md) |
| crypto | 392 | [crypto](index/by_asset/crypto.md) |
| stocks | 209 | [stocks](index/by_asset/stocks.md) |
| commodities | 97 | [commodities](index/by_asset/commodities.md) |
| forex | 81 | [forex](index/by_asset/forex.md) |
| indices | 80 | [indices](index/by_asset/indices.md) |
| options | 20 | [options](index/by_asset/options.md) |
| futures | 14 | [futures](index/by_asset/futures.md) |
| spot | 12 | [spot](index/by_asset/spot.md) |

## By market tag

| Group | Count | Index |
|---|---|---|
| (none) | 4416 | [_none_](index/by_market_tag/_none_.md) |
| crypto | 405 | [crypto](index/by_market_tag/crypto.md) |
| stocks | 245 | [stocks](index/by_market_tag/stocks.md) |
| commodities | 105 | [commodities](index/by_market_tag/commodities.md) |
| indices | 104 | [indices](index/by_market_tag/indices.md) |
| forex | 101 | [forex](index/by_market_tag/forex.md) |
| futures | 56 | [futures](index/by_market_tag/futures.md) |
| options | 23 | [options](index/by_market_tag/options.md) |
| spot | 21 | [spot](index/by_market_tag/spot.md) |

## By instrument mentioned

| Group | Count | Index |
|---|---|---|
| (none) | 4908 | [_none_](index/by_instrument/_none_.md) |
| BTC | 163 | [BTC](index/by_instrument/BTC.md) |
| GOLD | 62 | [GOLD](index/by_instrument/GOLD.md) |
| USDT | 39 | [USDT](index/by_instrument/USDT.md) |
| ETH | 33 | [ETH](index/by_instrument/ETH.md) |
| NIFTY | 25 | [NIFTY](index/by_instrument/NIFTY.md) |
| SPX | 20 | [SPX](index/by_instrument/SPX.md) |
| XAUUSD | 18 | [XAUUSD](index/by_instrument/XAUUSD.md) |
| SPY | 17 | [SPY](index/by_instrument/SPY.md) |
| OIL | 14 | [OIL](index/by_instrument/OIL.md) |
| CRUDE | 10 | [CRUDE](index/by_instrument/CRUDE.md) |
| ES | 9 | [ES](index/by_instrument/ES.md) |
| SOL | 9 | [SOL](index/by_instrument/SOL.md) |
| SILVER | 8 | [SILVER](index/by_instrument/SILVER.md) |
| TSLA | 8 | [TSLA](index/by_instrument/TSLA.md) |
| NQ | 6 | [NQ](index/by_instrument/NQ.md) |
| BANKNIFTY | 6 | [BANKNIFTY](index/by_instrument/BANKNIFTY.md) |
| DOGE | 5 | [DOGE](index/by_instrument/DOGE.md) |
| BNB | 5 | [BNB](index/by_instrument/BNB.md) |
| XAU | 5 | [XAU](index/by_instrument/XAU.md) |
| EURUSD | 5 | [EURUSD](index/by_instrument/EURUSD.md) |

## By direction

| Group | Count | Index |
|---|---|---|
| long_short | 3859 | [long_short](index/by_direction/long_short.md) |
| long_only | 1281 | [long_only](index/by_direction/long_only.md) |
| unknown | 112 | [unknown](index/by_direction/unknown.md) |
| short_only | 69 | [short_only](index/by_direction/short_only.md) |

## By exit method

| Group | Count | Index |
|---|---|---|
| signal_based | 3290 | [signal_based](index/by_exit_method/signal_based.md) |
| (none) | 1076 | [_none_](index/by_exit_method/_none_.md) |
| fixed_percent | 862 | [fixed_percent](index/by_exit_method/fixed_percent.md) |
| atr_based | 749 | [atr_based](index/by_exit_method/atr_based.md) |
| trailing | 740 | [trailing](index/by_exit_method/trailing.md) |
| pips_ticks_points | 633 | [pips_ticks_points](index/by_exit_method/pips_ticks_points.md) |
| risk_reward_ratio | 504 | [risk_reward_ratio](index/by_exit_method/risk_reward_ratio.md) |
| partial_exits | 250 | [partial_exits](index/by_exit_method/partial_exits.md) |
| time_based | 130 | [time_based](index/by_exit_method/time_based.md) |
| grid_take_profit | 67 | [grid_take_profit](index/by_exit_method/grid_take_profit.md) |
| structure_based | 56 | [structure_based](index/by_exit_method/structure_based.md) |
| breakeven | 50 | [breakeven](index/by_exit_method/breakeven.md) |

## By risk level

Heuristic: martingale, no stop loss, leverage ≥5x, pyramiding, 100% equity sizing raise it; SL+TP, risk sizing, drawdown control lower it.

| Group | Count | Index |
|---|---|---|
| low | 1968 | [low](index/by_risk/low.md) |
| high | 1706 | [high](index/by_risk/high.md) |
| medium | 1288 | [medium](index/by_risk/medium.md) |
| very_high | 359 | [very_high](index/by_risk/very_high.md) |

## By market regime fit

| Group | Count | Index |
|---|---|---|
| trending | 2567 | [trending](index/by_regime/trending.md) |
| ranging | 1209 | [ranging](index/by_regime/ranging.md) |
| trending/volatile | 423 | [trending_volatile](index/by_regime/trending_volatile.md) |
| any | 393 | [any](index/by_regime/any.md) |
| (none) | 311 | [_none_](index/by_regime/_none_.md) |
| ranging/trending | 185 | [ranging_trending](index/by_regime/ranging_trending.md) |
| volatile | 65 | [volatile](index/by_regime/volatile.md) |
| liquid/volatile | 54 | [liquid_volatile](index/by_regime/liquid_volatile.md) |
| any(long bias) | 42 | [any_long_bias_](index/by_regime/any_long_bias_.md) |
| reversal | 38 | [reversal](index/by_regime/reversal.md) |
| ranging/low_volatility | 23 | [ranging_low_volatility](index/by_regime/ranging_low_volatility.md) |
| depends | 7 | [depends](index/by_regime/depends.md) |
| ranging(spread) | 4 | [ranging_spread_](index/by_regime/ranging_spread_.md) |

## By indicator

Min 25 strategies per indicator shown.

| Group | Count | Index |
|---|---|---|
| SMA | 2796 | [SMA](index/by_indicator/SMA.md) |
| EMA | 2357 | [EMA](index/by_indicator/EMA.md) |
| RSI | 1473 | [RSI](index/by_indicator/RSI.md) |
| ATR | 1256 | [ATR](index/by_indicator/ATR.md) |
| Highest/Lowest (channel) | 1119 | [Highest_Lowest_channel_](index/by_indicator/Highest_Lowest_channel_.md) |
| Volume | 758 | [Volume](index/by_indicator/Volume.md) |
| Std Dev / Z-Score | 735 | [Std_Dev_Z-Score](index/by_indicator/Std_Dev_Z-Score.md) |
| Session/Time | 679 | [Session_Time](index/by_indicator/Session_Time.md) |
| Bollinger Bands | 669 | [Bollinger_Bands](index/by_indicator/Bollinger_Bands.md) |
| MACD | 656 | [MACD](index/by_indicator/MACD.md) |
| WMA | 513 | [WMA](index/by_indicator/WMA.md) |
| Stochastic | 470 | [Stochastic](index/by_indicator/Stochastic.md) |
| Supertrend | 279 | [Supertrend](index/by_indicator/Supertrend.md) |
| ADX/DMI | 264 | [ADX_DMI](index/by_indicator/ADX_DMI.md) |
| HMA | 256 | [HMA](index/by_indicator/HMA.md) |
| VWMA | 236 | [VWMA](index/by_indicator/VWMA.md) |
| (none) | 221 | [_none_](index/by_indicator/_none_.md) |
| Pivot Points | 221 | [Pivot_Points](index/by_indicator/Pivot_Points.md) |
| DEMA/TEMA | 200 | [DEMA_TEMA](index/by_indicator/DEMA_TEMA.md) |
| LSMA/LinReg | 181 | [LSMA_LinReg](index/by_indicator/LSMA_LinReg.md) |
| Ichimoku | 170 | [Ichimoku](index/by_indicator/Ichimoku.md) |
| Donchian Channel | 163 | [Donchian_Channel](index/by_indicator/Donchian_Channel.md) |
| Volume Delta/CVD | 158 | [Volume_Delta_CVD](index/by_indicator/Volume_Delta_CVD.md) |
| Aroon | 157 | [Aroon](index/by_indicator/Aroon.md) |
| Candlestick Patterns | 145 | [Candlestick_Patterns](index/by_indicator/Candlestick_Patterns.md) |
| Momentum/ROC | 144 | [Momentum_ROC](index/by_indicator/Momentum_ROC.md) |
| VWAP | 138 | [VWAP](index/by_indicator/VWAP.md) |
| Heikin Ashi | 138 | [Heikin_Ashi](index/by_indicator/Heikin_Ashi.md) |
| StochRSI | 130 | [StochRSI](index/by_indicator/StochRSI.md) |
| Parabolic SAR | 115 | [Parabolic_SAR](index/by_indicator/Parabolic_SAR.md) |
| Fibonacci | 113 | [Fibonacci](index/by_indicator/Fibonacci.md) |
| CCI | 105 | [CCI](index/by_indicator/CCI.md) |
| Ehlers Filters | 62 | [Ehlers_Filters](index/by_indicator/Ehlers_Filters.md) |
| Keltner Channel | 62 | [Keltner_Channel](index/by_indicator/Keltner_Channel.md) |
| Fractals | 60 | [Fractals](index/by_indicator/Fractals.md) |
| MFI | 59 | [MFI](index/by_indicator/MFI.md) |
| OBV | 49 | [OBV](index/by_indicator/OBV.md) |
| ALMA | 49 | [ALMA](index/by_indicator/ALMA.md) |
| Williams %R | 47 | [Williams_R](index/by_indicator/Williams_R.md) |
| T3 | 43 | [T3](index/by_indicator/T3.md) |
| WaveTrend | 43 | [WaveTrend](index/by_indicator/WaveTrend.md) |
| Ma Ribbon | 41 | [Ma_Ribbon](index/by_indicator/Ma_Ribbon.md) |
| Range Filter | 40 | [Range_Filter](index/by_indicator/Range_Filter.md) |
| KAMA | 40 | [KAMA](index/by_indicator/KAMA.md) |
| TSI | 37 | [TSI](index/by_indicator/TSI.md) |
| CMO | 36 | [CMO](index/by_indicator/CMO.md) |
| Squeeze (TTM) | 35 | [Squeeze_TTM_](index/by_indicator/Squeeze_TTM_.md) |
| Order Blocks/FVG | 32 | [Order_Blocks_FVG](index/by_indicator/Order_Blocks_FVG.md) |
| Awesome Oscillator | 30 | [Awesome_Oscillator](index/by_indicator/Awesome_Oscillator.md) |
| Gaussian Filter | 29 | [Gaussian_Filter](index/by_indicator/Gaussian_Filter.md) |
| Elder Ray / Force Index | 28 | [Elder_Ray_Force_Index](index/by_indicator/Elder_Ray_Force_Index.md) |
| Percentile/Rank | 28 | [Percentile_Rank](index/by_indicator/Percentile_Rank.md) |
| ZigZag | 26 | [ZigZag](index/by_indicator/ZigZag.md) |
| Envelope/STARC | 25 | [Envelope_STARC](index/by_indicator/Envelope_STARC.md) |
| Renko | 25 | [Renko](index/by_indicator/Renko.md) |

## By language

| Group | Count | Index |
|---|---|---|
| pine | 5283 | [pine](index/by_language/pine.md) |
| javascript | 361 | [javascript](index/by_language/javascript.md) |
| python | 130 | [python](index/by_language/python.md) |
| mylanguage | 27 | [mylanguage](index/by_language/mylanguage.md) |
| cpp | 3 | [cpp](index/by_language/cpp.md) |
| (none) | 2 | [_none_](index/by_language/_none_.md) |

## By file kind

| Group | Count | Index |
|---|---|---|
| strategy | 5300 | [strategy](index/by_kind/strategy.md) |
| utility | 225 | [utility](index/by_kind/utility.md) |
| indicator | 158 | [indicator](index/by_kind/indicator.md) |
| tutorial | 38 | [tutorial](index/by_kind/tutorial.md) |
| template | 27 | [template](index/by_kind/template.md) |
| execution_tool | 24 | [execution_tool](index/by_kind/execution_tool.md) |
| tutorial_strategy | 21 | [tutorial_strategy](index/by_kind/tutorial_strategy.md) |
| library | 13 | [library](index/by_kind/library.md) |

## By author (15+ files)

| Group | Count | Index |
|---|---|---|
| ChaoZhang | 4674 | [ChaoZhang](index/by_author/ChaoZhang.md) |
| ianzeng123 | 537 | [ianzeng123](index/by_author/ianzeng123.md) |
| 发明者量化-小小梦 | 98 | [_-_](index/by_author/_-_.md) |
| Zer3192 | 78 | [Zer3192](index/by_author/Zer3192.md) |
| Zero | 52 | [Zero](index/by_author/Zero.md) |
| 小草 | 44 | [_](index/by_author/_.md) |
| 发明者量化 | 24 | [_](index/by_author/_.md) |

## By year

| Group | Count | Index |
|---|---|---|
| 2024 | 2225 | [2024](index/by_year/2024.md) |
| 2023 | 2110 | [2023](index/by_year/2023.md) |
| 2025 | 781 | [2025](index/by_year/2025.md) |
| 2022 | 312 | [2022](index/by_year/2022.md) |
| 2021 | 90 | [2021](index/by_year/2021.md) |
| 2020 | 89 | [2020](index/by_year/2020.md) |
| 2018 | 64 | [2018](index/by_year/2018.md) |
| 2019 | 62 | [2019](index/by_year/2019.md) |
| 2016 | 30 | [2016](index/by_year/2016.md) |
| 2017 | 25 | [2017](index/by_year/2017.md) |
| 2014 | 11 | [2014](index/by_year/2014.md) |
| 2015 | 5 | [2015](index/by_year/2015.md) |
| (none) | 2 | [_none_](index/by_year/_none_.md) |
