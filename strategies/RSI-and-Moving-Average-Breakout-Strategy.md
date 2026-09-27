
> Name

RSI-and-Moving-Average-Breakout-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/19c78e00dcb443de6fc.png)
 
#### Overview  

The RSI and Moving Average Breakout Strategy is a quantitative strategy that utilizes both the RSI indicator and moving average lines to determine trading opportunities. The core idea of this strategy is to seek better breakout points with the direction of moving averages when RSI reaches overbought or oversold levels.  

#### Strategy Logic

1. Calculate RSI indicator and Simple Moving Average lines based on user-defined parameters.

2. When RSI crosses above the oversold line (default 30), a long signal is generated if price is below the LONG exit Moving Average.  

3. When RSI crosses below the overbought line (default 70), a short signal is generated if price is above the SHORT exit Moving Average.

4. Users can choose to filter signals based on a trend Moving Average line. Signals are only generated when price is above or below the filtering Moving Average.  

5. Exits are determined by the LONG and SHORT exit Moving Average lines.

#### Advantage Analysis  

1. Dual indicator design improves accuracy by incorporating two major market factors.

2. Utilizes the mean-reversion characteristic of RSI effectively to locate turning points. 

3. Additional filter with Moving Averages increases logic rigor to avoid chasing tops and bottoms.  

4. Customizable parameters allow optimizations across different products and timeframes.

5. Simple logic makes it easy to comprehend and modify.

#### Risk Analysis

1. Whipsaws are common with RSI, Density indicator could help.  

2. RSI tends to fail on larger timeframes, parameters can be adjusted or additional indicators can assist.

3. Moving Averages have lagging effect, lengths could be shortened or indicators like MACD can assist.  

4. More indicators should be introduced to validate signals due to the basic logic.

#### Optimization Directions  

1. Optimize RSI parameters or introduce Density indicator to reduce false signals.

2. Incorporate trend and volatility indicators like DMI and BOLL to locate trends and supports.

3. Introduce MACD to replace or complement Moving Average judgements. 

4. Add more logic conditions on entry signals to avoid unfavorable breakouts.

#### Conclusion

The RSI and Moving Average Breakout Strategy combines the overbought-oversold detection of RSI and trend determination of Moving Averages to capitalize on mean-reversion opportunities theoretically. The strategy is intuitive and easy to use for beginners, and can be optimized across different products, making it a recommended starter quantitative strategy. More auxiliary indicators could be introduced to further validate signals and improve profitability.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|0|Long Only or Short Only or Both?: Both|Long Only|Short Only|
|v_input_2|14|RSI Length|
|v_input_3|70|Upper Threshold|
|v_input_4|30|Lower Threshold|
|v_input_5|5|Long Exit SMA Length|
|v_input_6|5|Short Exit SMA Length|
|v_input_7|0|Trend SMA Filter?: Above|Below|Don't Include|
|v_input_8|200|Trend SMA Length|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-16 00:00:00
end: 2024-01-23 00:00:00
period: 5m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//Global Market Signals: RSI Strategy.
//@version=4
strategy("GMS: RSI Strategy", overlay=true)

LongShort = input(title="Long Only or Short Only or Both?", type=input.string, defval="Both", options=["Both", "Long Only", "Short Only"])
RSILength = input(title="RSI Length", type = input.integer ,defval=14)
RSIUpper = input(title="Upper Threshold", type = input.float ,defval=70)
RSILower = input(title="Lower Threshold", type = input.float ,defval=30)
LongExit = input(title="Long Exit SMA Length", type = input.integer ,defval=5)
ShortExit = input(title="Short Exit SMA Length", type = input.integer ,defval=5)
AboveBelow = input(title="Trend SMA Filter?", type=input.string, defval="Above", options=["Above", "Below", "Don't Include"])
TrendLength = input(title="Trend SMA Length", type = input.integer ,defval=200)


//Long Side

if LongShort =="Long Only" and AboveBelow == "Above"
    strategy.entry("LONG", true, when = rsi(close,RSILength)<RSILower and close< sma(close,LongExit) and close>sma(close,TrendLength))
    strategy.close("LONG", when = close>sma(close,LongExit))
    
if LongShort =="Long Only" and AboveBelow == "Below"
    strategy.entry("LONG", true, when = rsi(close,RSILength)<RSILower and close< sma(close,LongExit) and close<sma(close,TrendLength))
    strategy.close("LONG", when = close>sma(close,LongExit))
    
if LongShort =="Long Only" and AboveBelow == "Don't Include"
    strategy.entry("LONG", true, when = rsi(close,RSILength)<RSILower and close< sma(close,LongExit))
    strategy.close("LONG", when = close>sma(close,LongExit))
    
if LongShort =="Both" and AboveBelow == "Above"
    strategy.entry("LONG", true, when = rsi(close,RSILength)<RSILower and close< sma(close,LongExit) and close>sma(close,TrendLength))
    strategy.close("LONG", when = close>sma(close,LongExit))
    
if LongShort =="Both" and AboveBelow == "Below"
    strategy.entry("LONG", true, when = rsi(close,RSILength)<RSILower and close< sma(close,LongExit) and close<sma(close,TrendLength))
    strategy.close("LONG", when = close>sma(close,LongExit))
    
if LongShort =="Both" and AboveBelow == "Don't Include"
    strategy.entry("LONG", true, when = rsi(close,RSILength)<RSILower and close< sma(close,LongExit))
    strategy.close("LONG", when = close>sma(close,LongExit))
    
    
//SHORT SIDE

if LongShort =="Short Only" and AboveBelow == "Above"
    strategy.entry("SHORT", false, when = rsi(close,RSILength)>RSIUpper and close> sma(close,ShortExit) and close>sma(close,TrendLength))
    strategy.close("SHORT", when = close<sma(close,ShortExit))
    
if LongShort =="Short Only" and AboveBelow == "Below"
    strategy.entry("SHORT", false, when = rsi(close,RSILength)>RSIUpper and close> sma(close,ShortExit) and close<sma(close,TrendLength))
    strategy.close("SHORT", when = close<sma(close,ShortExit))
    
if LongShort =="Short Only" and AboveBelow == "Don't Include"
    strategy.entry("SHORT", false, when = rsi(close,RSILength)>RSIUpper and close> sma(close,ShortExit))
    strategy.close("SHORT", when = close<sma(close,ShortExit))
    
if LongShort =="Both" and AboveBelow == "Above"
    strategy.entry("SHORT", false, when = rsi(close,RSILength)>RSIUpper and close> sma(close,ShortExit) and close>sma(close,TrendLength))
    strategy.close("SHORT", when = close<sma(close,ShortExit))
    
if LongShort =="Both" and AboveBelow == "Below"
    strategy.entry("SHORT", false, when = rsi(close,RSILength)>RSIUpper and close> sma(close,ShortExit) and close<sma(close,TrendLength))
    strategy.close("SHORT", when = close<sma(close,ShortExit))
    
if LongShort =="Both" and AboveBelow == "Don't Include"
    strategy.entry("SHORT", false, when = rsi(close,RSILength)>RSIUpper and close> sma(close,ShortExit))
    strategy.close("SHORT", when = close<sma(close,ShortExit))
    
    
    
    
    
    
   




```

> Detail

https://www.fmz.com/strategy/439860

> Last Modified

2024-01-24 14:31:01
