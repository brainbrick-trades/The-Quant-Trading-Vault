
> Name

Level-by-Level-Build-Up-Moving-Average-Strategy

> Author

ChaoZhang

> Strategy Description




## Overview

The Level by Level Build Up Moving Average Strategy is a trading strategy based on RENKO charts. It uses moving average indicators to smooth price and crossovers between moving averages of different timeframes as trading signals. Meanwhile, it also uses the ATR indicator to determine stop loss levels for more reasonable stops.

## Strategy Logic

The core logic of this strategy includes:

1. Use input to select RENKO timeframe and ATR period

2. Calculate RENKO price and color. Turn to up when price breaks above previous RENKO price plus current ATR. Turn to down when price falls below previous RENKO price minus current ATR.

3. Use two integers BUY and SELL to record current long and short positions. 

4. When up breakout, if no short position then go long. If already short then close short position.
   When down breakout, if no long position then go short. If already long then close long position.

5. Plot RENKO chart using plot.

With this logic, the strategy can open long or short when price breaks previous level, and close positions when price reverse. Using ATR to determine breakout range makes stop loss more reasonable based on current volatility.

## Advantage Analysis 

This strategy has the following advantages:

1. RENKO filters noise and identifies trends
RENKO can effectively filter price noise and identify significant trends. This combination is great for trend detection and following.

2. Moving average crossovers generate trading signals
Crossovers between moving averages of different timeframes can provide reliable trading signals and avoid false signals from noise.

3. Dynamic stops with ATR
Using ATR to dynamically set stop loss can make stops more reasonable based on current volatility, avoiding stops too wide or too tight.

4. Combination of trend and moving average
Combining trend and moving average indicators utilizes the strengths of both - catching trends with RENKO while ensuring reliable signals with moving averages.

## Risk Analysis

The strategy also has some risks:

1. Incorrect trend identification
The way RENKO determines trends may result in unnecessary longs or shorts. Parameters need to be optimized to reduce false signals.

2. False signals from moving average crossovers  
There can be false signals from moving average crossovers, causing unnecessary trades. Moving average periods could be optimized.

3. Improper ATR parameters
Improper ATR period setting can also lead to stops too wide or too tight. Different markets should be tested for optimal parameters.

4. Whipsaw markets
In sideways or strong whipsaw markets, RENKO may generate many unnecessary trades, occupying capital. Other filters are needed to avoid trading such markets.

## Optimization Directions

The strategy can be optimized in the following aspects:

1. Optimize RENKO and ATR parameters  
Adjust these parameters to minimize RENKO false signals and better catch trends.

2. Add moving average crossover filters
Add more moving averages and require most of them to align before generating signals, to filter false signals. 

3. Add other indicator filters
For example, add volume to only take trades when volume confirms price, avoiding traps.

4. Improve stop loss strategy
Research how to use trend-based stops instead of simply tracking ATR, for more logical stops.

5. Optimize money management
Research optimal capital allocation under this strategy to maximize returns while controlling risks.

## Conclusion

Overall this is a strategy worth optimizing and testing in live markets. The core idea of using RENKO for trend and moving average crossovers as filtered signals is sound. With dynamic ATR stops it can become a solid trend following system. The next step is to continue optimizing it based on the known risks to improve parameters and performance.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|D|TimeFrame|
|v_input_2|14|ATR length|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-09-19 00:00:00
end: 2023-09-25 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("Renko Level Strategy 2", shorttitle="RLS2", overlay=true, pyramiding=2, currency=currency.USD, default_qty_value=50, initial_capital=2000, default_qty_type=strategy.percent_of_equity) 

TF = input(title='TimeFrame', type=input.resolution, defval="D")
ATRlength = input(title="ATR length", type=input.integer, defval=14, minval=2, maxval=100)

HIGH = security(syminfo.tickerid, TF, high)
LOW = security(syminfo.tickerid, TF, low)
CLOSE = security(syminfo.tickerid, TF, close)
ATR = security(syminfo.tickerid, TF, atr(ATRlength))

float RENKO = na
color COLOR = na
int BUY = na
int SELL = na
bool UP = na
bool DN = na

RENKO := na(RENKO[1]) ? close : RENKO[1]
COLOR := na(COLOR[1]) ? color.white : COLOR[1]
BUY := na(BUY[1]) ? 0 : BUY[1]
SELL := na(SELL[1]) ? 0 : SELL[1]
UP := false
DN := false

if(close > RENKO[1]+ATR[1])
    UP := true
    RENKO := close
    COLOR := color.lime
    SELL := 0
    BUY := BUY+1

if(close < RENKO[1]-ATR[1])
    DN := true
    RENKO := close
    COLOR := color.red
    BUY := 0
    SELL := SELL+1
    

if(BUY[1]==1 and BUY==2)
    strategy.entry("long", strategy.long)//, limit = RENKODN)

if(DN)
    strategy.cancel_all()
    strategy.close_all(comment = "close")


plot(RENKO, style=plot.style_line, linewidth=2, color=COLOR)
```

> Detail

https://www.fmz.com/strategy/427886

> Last Modified

2023-09-26 16:00:20
