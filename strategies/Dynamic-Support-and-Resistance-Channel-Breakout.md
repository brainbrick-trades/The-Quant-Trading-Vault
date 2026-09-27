
> Name

Dynamic-Support-and-Resistance-Channel-Breakout

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/172eebf5bfdee16735c.png)
 
## Overview  

The Dynamic Support and Resistance Channel Breakout Strategy is a powerful strategy to identify key support and resistance levels and breakout signals. It visualizes these critical levels on the chart, making it easy for traders to spot potential trading opportunities.  

## Strategy Logic  

The strategy dynamically calculates support and resistance levels based on user-defined left and right bars. This provides flexibility to adapt to changing market conditions. It generates buy and sell signals when the closing price crosses these support and resistance levels, together with volume confirmation. In addition, the strategy integrates automated execution of LONG/SHORT positions based on the defined support and resistance conditions, streamlining the overall trading process.   

Specifically, the strategy calculates the dynamic support and resistance levels using the ta.pivotlow and ta.pivothigh functions. These support and resistance lines are plotted in red and blue colors on the chart. When the closing price breaks through these levels, 'B' shape markings are drawn at the breakout locations. Meanwhile, the strategy incorporates a volume oscillator using 5-day and 10-day average volumes to gauge surges in volume. Breakout signals and alerts are only triggered when the volume is sufficiently large. Finally, the strategy integrates LONG/SHORT entry and exit strategies based on these support, resistance and volume conditions.

## Advantages  

The strategy has the following advantages:

1. Dynamic support and resistance levels adapt to market changes  
2. Volume confirmation ensures significance of breakouts
3. Graphical cues highlight critical points  
4. Integrated trading strategy simplifies workflow
5. Customizable parameters increase adaptability

Overall, the strategy comprehensively identifies, visualizes and capitalizes on key support and resistance breakout points, greatly facilitating traders in selecting optimal trading timing and significantly improving chances of trading success.  

## Risks

The potential risks of the strategy mainly include:

1. Invalid breakout risk. Breakout points may form false breakouts, leading to unnecessary losses. This can be mitigated by setting more strict volume and price fluctuation confirmation requirements.

2. Parameter optimization risk. Inaccurate support and resistance levels may be calculated if left/right bars etc. are set inappropriately. Suitable left/right bars should be selected according to trading characteristics of different products.  

3. Overoptimization risk. Excessive parameter optimization may lead to overfitting. Proper backtesting and validation should be undertaken to avoid overoptimization on limited data.

4. Transaction cost risk. Frequent trading may lead to higher commissions. Profit-taking factors or other means to control trading frequency should be considered.
 
## Enhancement Directions   

The strategy can be enhanced in the following aspects:

1. Add stop loss conditions to control single loss.  

2. Optimize profit-taking factors to determine optimal take-profit points.

3. Test different parameter combinations to determine optimum parameters.  

4. Adjust left/right bar settings based on different products.

5. Add other filters e.g. price volatility to better gauge breakout probability.  

6. Try different volume confirmation indicators, e.g. high-volume breakouts.

7. Incorporate other strategies or indicators to achieve better integration.

## Conclusion  

The Dynamic Support and Resistance Channel Breakout Strategy leverages the support and resistance concepts from technical chart analysis, together with volume analysis to confirm the significance of breakouts, to effectively uncover critical turning points in the market. Its simple yet elegant interface design, indicator plotting and signal prompts greatly lower technical barriers. Meanwhile, the customizable and integrable parameter settings make it easy to incorporate with traders' own strategies. In summary, this is a comprehensive and highly practical quantitative trading strategy.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Show Breaks|
|v_input_2|15|Left Bars|
|v_input_3|15|Right Bars|
|v_input_4|20|Volume Threshold|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-10 00:00:00
end: 2024-01-17 00:00:00
period: 30m
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Support and Resistance channel with Breaks p5", shorttitle="Support and Resistance channel with Breaks [cryptoonchain]", overlay=true, max_bars_back=1000)

// Input variables
toggleBreaks = input(true, title="Show Breaks")
leftBars = input(15, title="Left Bars")
rightBars = input(15, title="Right Bars")
volumeThresh = input(20, title="Volume Threshold")

// Calculate pivot levels
highUsePivot = fixnan(ta.pivothigh(leftBars, rightBars)[1])
lowUsePivot = fixnan(ta.pivotlow(leftBars, rightBars)[1])

// Plot resistance and support lines
r1 = plot(highUsePivot, color=color.new(na(highUsePivot) ? na : #FF0000, 0), linewidth=3, offset=-(rightBars + 1), title="Resistance")
s1 = plot(lowUsePivot, color=color.new(na(lowUsePivot) ? na : #233dee, 0), linewidth=3, offset=-(rightBars + 1), title="Support")

// Volume %
short = ta.ema(volume, 5)
long = ta.ema(volume, 10)
osc = 100 * (short - long) / long

// Plot shapes for breaks with volume
plotshape(toggleBreaks and ta.crossunder(close, lowUsePivot) and not (open - close < high - open) and osc > volumeThresh, title="Break", text='B', style=shape.labeldown, location=location.abovebar, color=color.red, textcolor=color.white, transp=0, size=size.tiny)
plotshape(toggleBreaks and ta.crossover(close, highUsePivot) and not (open - low > close - open) and osc > volumeThresh, title="Break", text='B', style=shape.labelup, location=location.belowbar, color=color.green, textcolor=color.white, transp=0, size=size.tiny)

// Alert conditions
alertcondition(ta.crossunder(close, lowUsePivot) and osc > volumeThresh, title="Support Broken", message="Support Broken")
alertcondition(ta.crossover(close, highUsePivot) and osc > volumeThresh, title="Resistance Broken", message="Resistance Broken")

// Strategy conditions with filter
longCondition = low > highUsePivot and osc > volumeThresh
shortCondition = high < lowUsePivot and osc > volumeThresh


// Strategy entries
strategy.entry("My Long Entry Id", strategy.long, when=longCondition)
strategy.entry("My Short Entry Id", strategy.short, when=shortCondition)

```

> Detail

https://www.fmz.com/strategy/439205

> Last Modified

2024-01-18 12:30:04
