
> Name

Multi-Timeframe-CPR-Breakout-Momentum-Trading-Strategy

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d81b1d6c45cd5f0bcd48.png)
![IMG](https://www.fmz.com/upload/asset/2d87b7937b938fd78164c.png)




#### Overview
This strategy is a multi-timeframe trading system that utilizes Central Pivot Range (CPR), Exponential Moving Average (EMA), and Relative Strength Index (RSI) for trading decisions. It identifies market trends and key support/resistance levels using daily CPR levels, weekly open prices, and 20-period EMA, combined with volume confirmation for trade execution.

#### Strategy Principles
The core principle revolves around analyzing price relationships with CPR levels. CPR consists of Pivot Point, Bottom Central (BC), and Top Central (TC) lines. Long signals are generated when price breaks above TC in bullish market phases, while short signals occur when price breaks below BC in bearish phases. The system employs a 20-period EMA as a trend filter and requires volume above the 20-period average to confirm breakouts. Additionally, RSI divergence can be optionally used for extra confirmation.

#### Strategy Advantages
1. Multiple confirmation mechanisms: Combines price action, trend direction, and volume triple confirmation to enhance signal reliability
2. Dynamic risk management: Sets dynamic stop-losses based on CPR width, adapting to different market conditions
3. Flexible customization options: Adjustable CPR timeframes, EMA length, and optional RSI divergence confirmation
4. Asymmetric reward ratios: Employs 1.5:1 reward-to-risk ratio for improved long-term profitability
5. Multi-timeframe analysis: Integrates daily and weekly data for a more comprehensive market perspective

#### Strategy Risks
1. False breakout risk: May generate false signals in ranging markets, suggesting stricter volume filtering
2. Trend reversal risk: Potential for larger drawdowns at trend turning points, manageable through tighter stops
3. Parameter sensitivity: Strategy performance is sensitive to EMA length and volume threshold parameters
4. Market environment dependency: May struggle to achieve target reward ratios in low volatility environments
5. Execution slippage: Can face significant slippage in fast-moving markets, affecting actual trading results

#### Strategy Optimization Directions
1. Implement volatility adaptation: Dynamically adjust stops and targets based on market volatility
2. Enhanced market state classification: Differentiate between trending and ranging markets with separate parameters
3. Refined volume filter: Consider relative volume changes instead of simple moving average comparison
4. Improved exit mechanics: Add trailing stops and partial profit-taking functionality
5. Time-based filtering: Avoid trading during specific periods like market open/close volatile sessions

#### Summary
This is a well-structured trend-following strategy with clear logic, effectively controlling trading risks through multiple technical indicators. Its main strengths lie in flexible parameter settings and comprehensive risk management mechanisms, though traders must remain attentive to changing market conditions and adjust parameters accordingly. Through the suggested optimization directions, the strategy's stability and profitability can be further enhanced.





> Source (PineScript)

``` pinescript
//@version=5
strategy("Ahmad Ali Khan CPR Strategy", overlay=true, margin_long=100, margin_short=100)

// ---- Inputs ----
use_daily_cpr = input.bool(true, "Use Daily CPR Levels")
ema_length = input.int(20, "EMA Trend Filter Length")
show_week_open = input.bool(true, "Show Weekly Open Price")
enable_divergence = input.bool(true, "Enable RSI Divergence Check")

// ---- Daily CPR Calculation ----
daily_high = request.security(syminfo.tickerid, "D", high[1], lookahead=barmerge.lookahead_on)
daily_low = request.security(syminfo.tickerid, "D", low[1], lookahead=barmerge.lookahead_on)
daily_close = request.security(syminfo.tickerid, "D", close[1], lookahead=barmerge.lookahead_on)

pivot = (daily_high + daily_low + daily_close) / 3
bc = (daily_high + daily_low) / 2
tc = pivot + (pivot - bc)

// ---- Weekly Open Price ----
weekly_open = request.security(syminfo.tickerid, "W", open, lookahead=barmerge.lookahead_on)

// ---- Trend Analysis ----
ema_trend = ta.ema(close, ema_length)
market_phase = close > ema_trend ? "Bullish" : "Bearish"

// ---- Momentum Confirmation ----
rsi_length = 14
rsi = ta.rsi(close, rsi_length)
bullish_div = ta.valuewhen(ta.crossover(rsi, 30), low, 0) > ta.valuewhen(ta.crossover(rsi, 30), low, 1)
bearish_div = ta.valuewhen(ta.crossunder(rsi, 70), high, 0) < ta.valuewhen(ta.crossunder(rsi, 70), high, 1)

// ---- Plotting ----
// CPR Levels
plot(pivot, "Pivot", color=color.blue, linewidth=2)
plot(bc, "BC", color=color.red, linewidth=2)
plot(tc, "TC", color=color.green, linewidth=2)
fill(plot(bc), plot(tc), color=color.new(color.purple, 90))

// Weekly Open
plot(show_week_open ? weekly_open : na, "Weekly Open", color=color.orange, linewidth=2)

// EMA Trend
plot(ema_trend, "EMA Trend", color=color.white, linewidth=2)

// ---- Strategy Logic ----
long_condition = 
  close > tc and 
  market_phase == "Bullish" and 
  (not enable_divergence or bullish_div) and
  volume > ta.sma(volume, 20)

short_condition = 
  close < bc and 
  market_phase == "Bearish" and 
  (not enable_divergence or bearish_div) and
  volume > ta.sma(volume, 20)

// ---- Risk Management ----
cpr_width = tc - bc
stop_loss_long = bc - (0.5 * cpr_width)
take_profit_long = tc + (1.5 * cpr_width)
stop_loss_short = tc + (0.5 * cpr_width)
take_profit_short = bc - (1.5 * cpr_width)

// ---- Execute Orders ----
if long_condition
    strategy.entry("Long", strategy.long)
    strategy.exit("XL", "Long", stop=stop_loss_long, limit=take_profit_long)
    
if short_condition
    strategy.entry("Short", strategy.short)
    strategy.exit("XS", "Short", stop=stop_loss_short, limit=take_profit_short)

// ---- Signal Plotting ----
plotshape(long_condition, "Buy", shape.labelup, location.belowbar, color=color.green, text="BUY", textcolor=color.white)
plotshape(short_condition, "Sell", shape.labeldown, location.abovebar, color=color.red, text="SELL", textcolor=color.white)
```

> Detail

https://www.fmz.com/strategy/483075

> Last Modified

2025-02-21 11:45:06
