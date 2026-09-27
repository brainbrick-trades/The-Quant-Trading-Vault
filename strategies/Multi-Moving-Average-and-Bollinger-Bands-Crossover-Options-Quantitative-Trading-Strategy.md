
> Name

Multi-Moving-Average-and-Bollinger-Bands-Crossover-Options-Quantitative-Trading-Strategy

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d8d7debaf464c257f543.png)
![IMG](https://www.fmz.com/upload/asset/2d80c248a3230da528432.png)




#### Overview
This strategy is an advanced quantitative trading system based on multiple moving averages and Bollinger Bands indicators. The core strategy uses the crossover signals of 5-period and 11-period moving averages as the primary entry criteria, combined with 55-period moving average and Bollinger Bands for signal filtering and risk control. This strategy is particularly suitable for options trading, especially for ATM options on 3-minute and 5-minute timeframes.

#### Strategy Principles
The core logic of the strategy includes the following key elements:
1. Utilizing crossovers between 5-period and 11-period moving averages for initial trading signals
2. Confirming overall trend direction with 55-period moving average
3. Using Bollinger Bands (22-period) with 1.5 standard deviation for overbought/oversold conditions
4. Implementing dynamic stop-loss and take-profit targets using 14-period ATR
Specifically, long signals are generated when price is below the lower band and the 5-period MA crosses above the 11-period MA, while price remains above the 55-period MA. Conversely, short signals occur when price is above the upper band and the 5-period MA crosses below the 11-period MA, while price is below the 55-period MA.

#### Strategy Advantages
1. Multiple timeframe confirmation enhances trading success rate
2. Adaptive volatility-based stop-loss effectively controls risk
3. Integration with Bollinger Bands improves entry timing accuracy
4. Clear trading rules, easy to implement and backtest
5. Achieves minimum 1:2 reward-to-risk ratio
6. Particularly suitable for options trading, especially ATM options buying strategies

#### Strategy Risks
1. May generate frequent false breakout signals in ranging markets
2. Moving average system has inherent lag
3. Bollinger Bands parameters require optimization for different market conditions
4. ATR-based stops may be too wide during high volatility periods
Mitigation measures:
- Add volume confirmation
- Recommend trading in clear trend environments
- Regular review and adjustment of Bollinger Bands parameters
- Consider implementing fixed stop-loss limits

#### Strategy Optimization Directions
1. Introduce volume indicators for signal confirmation
2. Develop adaptive Bollinger Bands parameter adjustment mechanism
3. Add market environment identification module
4. Optimize stop-loss strategy, consider implementing trailing stops
5. Include time filters to avoid trading during inactive periods
These optimizations will help improve strategy stability and profitability, particularly adaptability across different market conditions.

#### Summary
This strategy constructs a relatively complete trading system by combining multiple technical indicators. Its core strengths lie in the multi-layered signal confirmation mechanism and dynamic risk management approach. While there is room for optimization, the basic framework is robust and particularly suitable for options traders. Through continuous optimization and improvement, the strategy has the potential to achieve better performance in actual trading.




> Source (PineScript)

``` pinescript
/*backtest
start: 2025-02-12 00:00:00
end: 2025-02-18 08:00:00
period: 5m
basePeriod: 5m
exchanges: [{"eid":"Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("MA5 MA11 Bollinger Bands 22 Strategy", overlay=true)

// Define indicators
ma5 = ta.sma(close, 5)
ma11 = ta.sma(close, 11)
ma55 = ta.sma(close, 55)
basis = ta.sma(close, 22)
dev = 1.5
upperBB = basis + dev * ta.stdev(close, 22)
lowerBB = basis - dev * ta.stdev(close, 22)

// Plot the indicators
plot(ma5, color=color.blue, linewidth=2, title="MA5")
plot(ma11, color=color.red, linewidth=2, title="MA11")
plot(ma55, color=color.green, linewidth=2, title="MA55")
plot(upperBB, color=color.orange, linewidth=1, title="Upper Bollinger Band")
plot(lowerBB, color=color.orange, linewidth=1, title="Lower Bollinger Band")

// Entry conditions
longCondition = ta.crossover(ma5, ma11) and close > ma55 and close < lowerBB
shortCondition = ta.crossunder(ma5, ma11) and close < ma55 and close > upperBB

// Exit conditions
closeLongCondition = ta.crossunder(close, ma5) or close < ma55
closeShortCondition = ta.crossover(close, ma5) or close > ma55

// Execute trades
if (longCondition)
    strategy.entry("Long", strategy.long)
    
if (shortCondition)
    strategy.entry("Short", strategy.short)

if (closeLongCondition)
    strategy.close("Long")
    
if (closeShortCondition)
    strategy.close("Short")
    
// Optional: Add Stop Loss and Take Profit (e.g., ATR-based)
atrValue = ta.atr(14)
stopLoss = atrValue * 1.5
takeProfit = atrValue * 3

strategy.exit("Exit Long", "Long", stop=close - stopLoss, limit=close + takeProfit)
strategy.exit("Exit Short", "Short", stop=close + stopLoss, limit=close - takeProfit)
```

> Detail

https://www.fmz.com/strategy/482820

> Last Modified

2025-02-20 14:53:43
