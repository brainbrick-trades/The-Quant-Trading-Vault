
> Name

Dual-Technical-Indicator-Momentum-Reversal-Trading-Strategy-with-Risk-Management-System

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/bc2efdba42c3a7f666.png)


#### Overview
This strategy is a momentum reversal trading system combining RSI and Bollinger Bands indicators, designed to identify overbought and oversold areas. It implements a 1:2 risk-reward ratio with trailing stop loss for risk management. The core logic is to execute trades when both RSI and Bollinger Bands show oversold or overbought signals simultaneously, protecting capital through strict risk management.

#### Strategy Principles
The strategy utilizes a 14-period RSI and 20-period Bollinger Bands as primary indicators. Buy conditions require both: RSI below 30 (oversold) and price at or below the lower Bollinger Band. Sell conditions require both: RSI above 70 (overbought) and price at or above the upper Bollinger Band. The system uses 5-bar high/low points for trailing stops, with take profit set at twice the stop loss distance, strictly maintaining a 1:2 risk-reward ratio.

#### Strategy Advantages
1. Dual indicator filtering improves signal quality and reduces false signals
2. Combines momentum and volatility indicators for a comprehensive market perspective
3. Strict risk control mechanisms including trailing stops and fixed risk-reward ratio
4. Fully automated system eliminating emotional interference
5. Clear strategy logic that is easy to understand and maintain

#### Strategy Risks
1. May experience frequent stops in trending markets
2. Dual conditions might miss some trading opportunities
3. Fixed RSI and Bollinger Bands parameters may not suit all market conditions
4. Trailing stops might exit positions too early in volatile markets
5. Requires proper money management to handle consecutive losses

#### Optimization Directions
1. Implement adaptive parameters mechanism to dynamically adjust indicator settings based on market volatility
2. Add trend filter to pause reversal trading during strong trends
3. Develop dynamic risk-reward ratio system adjusting to market conditions
4. Incorporate volume confirmation to improve signal reliability
5. Implement more flexible stop loss mechanisms like trailing stops or time-based exits

#### Summary
This is a well-structured reversal trading strategy that enhances accuracy through dual technical indicators and employs strict risk management. While simple and intuitive, it contains all key elements required for a mature trading system. Through the suggested optimization directions, the strategy has room for further improvement. For live trading, thorough backtesting and parameter optimization are recommended.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-12-06 00:00:00
end: 2025-01-04 08:00:00
period: 3h
basePeriod: 3h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("RSI + Bollinger Bands with 1:2 Risk/Reward", overlay=true)

// Define Inputs
length_rsi = input.int(14, title="RSI Period")
oversold_level = input.int(30, title="RSI Oversold Level")
overbought_level = input.int(70, title="RSI Overbought Level")
length_bb = input.int(20, title="Bollinger Bands Period")
src = close
risk_to_reward = input.float(2.0, title="Risk-to-Reward Ratio", minval=1.0, step=0.1)

// Calculate Indicators
rsi_value = ta.rsi(src, length_rsi)
basis = ta.sma(src, length_bb)
dev = ta.stdev(src, length_bb)
upper_band = basis + 2 * dev
lower_band = basis - 2 * dev

// Define Buy and Sell Conditions
rsi_buy_condition = rsi_value < oversold_level // RSI below 30 (buy signal)
bollinger_buy_condition = close <= lower_band // Price at or near lower Bollinger Band (buy signal)

rsi_sell_condition = rsi_value > overbought_level // RSI above 70 (sell signal)
bollinger_sell_condition = close >= upper_band // Price at or near upper Bollinger Band (sell signal)

// Combine Buy and Sell Conditions
buy_condition = rsi_buy_condition and bollinger_buy_condition
sell_condition = rsi_sell_condition and bollinger_sell_condition

// Plot Buy and Sell Signals with white text and green/red boxes
plotshape(series=buy_condition, location=location.belowbar, color=color.green, style=shape.labelup, title="Buy Signal", text="BUY", textcolor=color.white, size=size.small)
plotshape(series=sell_condition, location=location.abovebar, color=color.red, style=shape.labeldown, title="Sell Signal", text="SELL", textcolor=color.white, size=size.small)

// Calculate Swing Points (for Stop Loss)
swing_low = ta.lowest(low, 5)  // Last 5 bars' low
swing_high = ta.highest(high, 5) // Last 5 bars' high

// Calculate Risk (Distance from Entry to SL)
long_risk = close - swing_low
short_risk = swing_high - close

// Calculate Take Profit using 1:2 Risk-to-Reward Ratio
take_profit_long = close + 2 * long_risk
take_profit_short = close - 2 * short_risk

// Strategy Execution: Enter Buy/Sell Positions
if buy_condition
    strategy.entry("Buy", strategy.long)
    strategy.exit("Take Profit", "Buy", limit=take_profit_long, stop=swing_low)  // Set TP and SL for Buy

if sell_condition
    strategy.entry("Sell", strategy.short)
    strategy.exit("Take Profit", "Sell", limit=take_profit_short, stop=swing_high)  // Set TP and SL for Sell

// Plotting the Indicators for Visualization (Optional - comment out if not needed)
plot(rsi_value, color=color.blue, title="RSI", linewidth=2, display=display.none)
plot(upper_band, color=color.red, title="Upper BB", display=display.none)
plot(lower_band, color=color.green, title="Lower BB", display=display.none)

```

> Detail

https://www.fmz.com/strategy/477609

> Last Modified

2025-01-06 16:45:01
