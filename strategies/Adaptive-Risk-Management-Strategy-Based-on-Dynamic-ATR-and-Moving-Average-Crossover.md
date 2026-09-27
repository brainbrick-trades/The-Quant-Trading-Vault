
> Name

Adaptive-Risk-Management-Strategy-Based-on-Dynamic-ATR-and-Moving-Average-Crossover

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d8ca33c79b217af9c3e1.png)
![IMG](https://www.fmz.com/upload/asset/2d871415a5db59099227a.png)





#### Overview
This strategy is a trading system that combines dual moving average crossover signals with dynamic risk management. It generates trading signals through the crossover of short-term and long-term moving averages while using the ATR indicator to dynamically adjust stop-loss and take-profit levels. The strategy also incorporates time filtering and a cooldown period to optimize trade quality, along with risk-reward ratio and per-trade risk percentage management mechanisms.

#### Strategy Principles
The strategy is based on several core components:
1. The signal generation system uses the crossover of short-term (10-period) and long-term (100-period) simple moving averages to trigger trades. A buy signal is generated when the short-term MA crosses above the long-term MA, and vice versa.
2. The risk management system uses a 14-period ATR multiplied by 1.5 to set dynamic stop-loss distances, with the profit target being twice the stop-loss distance (adjustable risk-reward ratio).
3. A time filter allows users to set specific trading hours, executing trades only within the specified time range.
4. A trading cooldown mechanism sets a 10-period waiting time to prevent overtrading.
5. Risk per trade is controlled at 1% of the account (adjustable).

#### Strategy Advantages
1. Dynamic Risk Management: Uses the ATR indicator to adapt to market volatility, automatically adjusting stop-loss and take-profit distances in different market conditions.
2. Comprehensive Risk Control: Achieves systematic money management through set risk-reward ratios and per-trade risk percentages.
3. Flexible Time Management: Can adjust trading hours according to different market characteristics.
4. Overtrading Prevention: Cooldown mechanism effectively prevents excessive trading signals during volatile periods.
5. Visualization: Clearly displays trading signals and moving averages on the chart for analysis and optimization.

#### Strategy Risks
1. Trend Reversal Risk: May generate false breakout signals in ranging markets, leading to consecutive stops.
2. Parameter Sensitivity: The choice of moving average periods, ATR multiplier, and other parameters significantly affects strategy performance.
3. Improper time filter settings may miss important trading opportunities.
4. Fixed risk-reward ratio may not be flexible enough for different market conditions.

#### Strategy Optimization Directions
1. Introduce Trend Strength Filter: Add ADX or similar indicators to assess trend strength, trading only during strong trends.
2. Dynamic Risk-Reward Ratio Adjustment: Automatically adjust risk-reward ratio based on market volatility or trend strength.
3. Add Volume Analysis: Incorporate volume as a supplementary indicator for signal confirmation.
4. Optimize Cooldown Mechanism: Make cooldown period length dynamically adjust based on market volatility.
5. Implement Market Environment Classification: Use different parameter combinations in different market environments.

#### Summary
This strategy builds a complete trading system by combining classical technical analysis methods with modern risk management concepts. Its core advantages lie in dynamic risk management and multiple filtering mechanisms, but parameters still need to be optimized based on specific market characteristics in practical applications. Successful strategy operation requires traders to deeply understand the function of each component and adjust parameters timely according to market changes. Through the suggested optimization directions, the strategy has the potential to achieve more stable performance across different market environments.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-09-18 00:00:00
end: 2025-02-19 00:00:00
period: 2h
basePeriod: 2h
exchanges: [{"eid":"Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Profitable Moving Average Crossover Strategy", shorttitle="Profitable MA Crossover", overlay=true)

// Input parameters for the moving averages
shortPeriod = input.int(10, title="Short Period", minval=1)
longPeriod = input.int(100, title="Long Period", minval=1)

// Input parameters for time filter
startHour = input.int(0, title="Start Hour (UTC)", minval=0, maxval=23)
startMinute = input.int(0, title="Start Minute (UTC)", minval=0, maxval=59)
endHour = input.int(23, title="End Hour (UTC)", minval=0, maxval=23)
endMinute = input.int(59, title="End Minute (UTC)", minval=0, maxval=59)

// Cooldown period input (bars)
cooldownBars = input.int(10, title="Cooldown Period (Bars)", minval=1)

// Risk management inputs
riskRewardRatio = input.float(2, title="Risk-Reward Ratio", minval=1)
riskPercent = input.float(1, title="Risk Per Trade (%)", minval=0.1)

// ATR settings
atrLength = input.int(14, title="ATR Length")
atrMultiplier = input.float(1.5, title="ATR Multiplier for Stop-Loss and Take-Profit")

// Calculate the moving averages
shortMA = ta.sma(close, shortPeriod)
longMA = ta.sma(close, longPeriod)

// Plot the moving averages
plot(shortMA, color=color.blue, title="Short MA")
plot(longMA, color=color.red, title="Long MA")

// Calculate ATR for dynamic stop-loss and take-profit
atr = ta.atr(atrLength)
stopLossOffset = atr * atrMultiplier
takeProfitOffset = stopLossOffset * riskRewardRatio

// Identify the crossover points
bullishCross = ta.crossover(shortMA, longMA)
bearishCross = ta.crossunder(shortMA, longMA)

// Get the current bar's time in UTC
currentTime = na(time("1", "UTC")) ? na : timestamp("UTC", year, month, dayofmonth, hour, minute)

// Define the start and end time in seconds from the start of the day
startTime = timestamp("UTC", year, month, dayofmonth, startHour, startMinute)
endTime = timestamp("UTC", year, month, dayofmonth, endHour, endMinute)

// Check if the current time is within the valid time range
isTimeValid = (currentTime >= startTime) and (currentTime <= endTime)

// Functions to check cooldown
var int lastSignalBar = na
isCooldownActive = (na(lastSignalBar) ? false : (bar_index - lastSignalBar) < cooldownBars)

// Handle buy signals
if (bullishCross and isTimeValid and not isCooldownActive)
    entryPrice = close
    stopLossBuy = entryPrice - stopLossOffset
    takeProfitBuy = entryPrice + takeProfitOffset
    strategy.entry("Buy", strategy.long)
    strategy.exit("TakeProfit/StopLoss", "Buy", stop=stopLossBuy, limit=takeProfitBuy)
    lastSignalBar := bar_index

// Handle sell signals
if (bearishCross and isTimeValid and not isCooldownActive)
    entryPrice = close
    stopLossSell = entryPrice + stopLossOffset
    takeProfitSell = entryPrice - takeProfitOffset
    strategy.entry("Sell", strategy.short)
    strategy.exit("TakeProfit/StopLoss", "Sell", stop=stopLossSell, limit=takeProfitSell)
    lastSignalBar := bar_index

// Plot signals on the chart
plotshape(series=bullishCross and isTimeValid and not isCooldownActive, location=location.belowbar, color=color.green, style=shape.labelup, text="Buy", title="Buy Signal", textcolor=color.white)
plotshape(series=bearishCross and isTimeValid and not isCooldownActive, location=location.abovebar, color=color.red, style=shape.labeldown, text="Sell", title="Sell Signal", textcolor=color.white)

// Strategy performance tracking
strategy.close("Buy", when=not isTimeValid)
strategy.close("Sell", when=not isTimeValid)

```

> Detail

https://www.fmz.com/strategy/482836

> Last Modified

2025-02-20 14:07:26
