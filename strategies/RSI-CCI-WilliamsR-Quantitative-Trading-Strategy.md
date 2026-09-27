
> Name

RSI-CCI-WilliamsR-Quantitative-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/d145c1ffd030492c64.png)
 
## Strategy Overview  
This strategy combines three classification indicators: RSI, CCI and Williams%R to generate effective trading signals. It will issue buy or sell signals when all three indicators concurrently display overbought or oversold signals. Compared to using a single indicator, this composite strategy filters out more false signals and improves stability.  

The strategy is named "Three Trail Trawler Strategy". "Three Trail" refers to the combination of RSI, CCI and Williams%R. "Trawler" analogizes that this strategy trawls opportunities like a fishing trawler.  

## Strategy Logic   
The strategy mainly relies on the following indicators for trading decisions:

1. RSI indicator judging overbought/oversold levels   
2. CCI indicator identifying inflection points  
3. Williams%R indicator further confirming trading signals  

When RSI is below 25, it signals oversold status. When RSI is above 75, it signals overbought status. The same logic applies to CCI and Williams%R parameters. 

When all three indicators concurrently display buy signals, i.e. RSI < 25, CCI < -130, Williams %R < -85, the strategy will long. When all three indicators concurrently display sell signals, i.e. RSI > 75, CCI > 130, Williams %R > -15, the strategy will short.   

This avoids false signals from a single indicator and improves reliability. It also configures stop loss and take profit to control risks and returns per trade.

## Advantages
1. Multi-indicator combo filters false signals   
By combining RSI, CCI and Williams%R, the strategy filters out some false signals from individual indicators, improving accuracy.   

2. Auto stop loss/profit takes manages risks 
Inbuilt stop loss and take profit functions automatically set exit prices for each trade, effectively capping losses within tolerable thresholds.

3. Suits middle-term trading
The strategy works better for middle-term trades, clearly identifying middle-term inflection points via the indicator combo. It is weaker in spotting short-term noise and long-term trends.   

4. Solid backtest data  
The strategy uses 45-min bars of EUR/USD, a major forex pair with abundant liquidity and data, reducing overfit risks from insufficient data.

## Risks 
1. Weak long-term trend identification   
The strategy relies more on contrary signals. Its abilities to gauge and follow long-term trends are limited. During long-lasting one-way markets, profit potential is constrained.   

2. Missing short-term swings
With 45-min bars, the strategy misses profitable chances from more frequent short-term price swings. Greater volatility within the bar span could lead to missed opportunities.  

3. Systemic risks   
The strategy mainly applies to EUR/USD. In times of severe economic crisis that rocks the global forex market, its trading rules could fail, incurring huge losses.  

## Enhancement Areas
1. Adding trend-following indicators  
Try incorporating trending metrics like MA, Boll etc. to assist long-term trend recognition. Only taking positions along the general direction will improve win rate.  

2. Optimizing stop loss/profit parameters 
Backtest more historical data to assess the impact of various stop loss/profit parameters on final profitability, in order to find the optimum setting. Consider dynamic templating as well.  

3. Expanding products   
Currently mainly applies to EUR/USD. We can attempt to deploy it on other major currency pairs like GBP, JPY, AUD to examine its stability and transferability.  

## Conclusion
The "Three Trail Trawler Strategy" identifies price reversal points for overbought/oversold signals using a combination of RSI, CCI and Williams %R. Compared to individual metrics, this multi-indicator setup filters out more false signals and improves accuracy. The automated stop loss/profit taking functions also help cap trading risks. Overall, it is a stable strategy suitable for middle-term trading and can be a valuable module in our quantitative systems. Still we need to heed its deficiencies in long-term trend spotting and capturing short-term swings. Fine-tuning measures like adding trend metrics, optimizing exit parameters and expanding products will enhance the strategy as a steady profit engine for our quant systems.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|14|RSI Period|
|v_input_2|20|CCI Period|
|v_input_3|14|Williams %R Period|
|v_input_4|25|RSI Oversold Level|
|v_input_5|75|RSI Overbought Level|
|v_input_6|-130|CCI Oversold Level|
|v_input_7|130|CCI Overbought Level|
|v_input_8|-85|Williams %R Oversold Level|
|v_input_9|-15|Williams %R Overbought Level|
|v_input_10|1.2|Take Profit (%)|
|v_input_11|0.45|Stop Loss (%)|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-16 00:00:00
end: 2024-01-23 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("RSI CCI Williams %R Strategy with TP and SL", overlay=true)

// Input parameters for indicators
rsi_period = input(14, title="RSI Period")
cci_period = input(20, title="CCI Period")
williams_period = input(14, title="Williams %R Period")

// Thresholds for overbought and oversold conditions
rsi_oversold = input(25, title="RSI Oversold Level")
rsi_overbought = input(75, title="RSI Overbought Level")
cci_oversold = input(-130, title="CCI Oversold Level")
cci_overbought = input(130, title="CCI Overbought Level")
williams_oversold = input(-85, title="Williams %R Oversold Level")
williams_overbought = input(-15, title="Williams %R Overbought Level")

// Take profit and stop loss levels as a percentage
take_profit_pct = input(1.2, title="Take Profit (%)") / 100
stop_loss_pct = input(0.45, title="Stop Loss (%)") / 100

// Indicator calculations
rsi = ta.rsi(close, rsi_period)
cci = ta.cci(close, cci_period)
highestHigh = ta.highest(high, williams_period)
lowestLow = ta.lowest(low, williams_period)
williamsR = (highestHigh - close) / (highestHigh - lowestLow) * -100

// Entry conditions
longCondition = rsi < rsi_oversold and cci < cci_oversold and williamsR < williams_oversold and strategy.position_size == 0
shortCondition = rsi > rsi_overbought and cci > cci_overbought and williamsR > williams_overbought and strategy.position_size == 0

// Execute strategy entry orders
if (longCondition)
    strategy.entry("Long", strategy.long)
    strategy.exit("Take Profit or Stop Loss Long", "Long", limit=close * (1 + take_profit_pct), stop=close * (1 - stop_loss_pct))

if (shortCondition)
    strategy.entry("Short", strategy.short)
    strategy.exit("Take Profit or Stop Loss Short", "Short", limit=close * (1 - take_profit_pct), stop=close * (1 + stop_loss_pct))

// Plot the signals on the chart
plotshape(series=longCondition, title="Buy Signal", location=location.belowbar, color=color.green, style=shape.triangleup, text="BUY")
plotshape(series=shortCondition, title="Sell Signal", location=location.abovebar, color=color.red, style=shape.triangledown, text="SELL")

// Plot the indicators for visualization
plot(rsi, title="RSI", color=color.blue)
plot(cci, title="CCI", color=color.purple)
plot(williamsR, title="Williams %R", color=color.orange)
```

> Detail

https://www.fmz.com/strategy/439835

> Last Modified

2024-01-24 11:18:08
