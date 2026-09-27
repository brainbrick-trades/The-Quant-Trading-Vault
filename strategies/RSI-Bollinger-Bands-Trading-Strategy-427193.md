
> Name

RSI-Bollinger-Bands-Trading-Strategy-427193

> Author

ChaoZhang

> Strategy Description


All English language content


## Overview

This strategy identifies trading signals by using the RSI indicator to determine overbought/oversold conditions and combining with the Bollinger Bands indicator to depict price oscillation range. It generates buy and sell signals when the RSI shows overbought or oversold levels, while price is approaching or touching the Bollinger Bands upper or lower bands. The strategy synthesizes trend analysis and oscillation judgment to dynamically seek opportunities.

## Strategy Logic

The strategy is based primarily on two indicators:

1. RSI indicator judging overbought/oversold

It calculates the RSI for a certain period and determines whether it enters overbought or oversold zones according to preset parameters, like overbought threshold at 40 and oversold threshold at 45.

2. Bollinger Bands indicating price oscillation range  

It calculates the Bollinger Bands for a period and uses the upper and lower bands to form a price channel, describing the range of price oscillations.

Based on the above, the trading rules are:

When RSI crosses above 45 into oversold zone, and price crosses above Bollinger lower band, generate buy signal.
When RSI crosses below 40 into overbought zone, and price crosses below Bollinger upper band, generate sell signal.

## Advantage Analysis

The advantages of combining RSI and Bollinger Bands include:

1. RSI identifies overbought/oversold levels, Bollinger Bands determine price trend direction, complementing each other.

2. Bollinger Bands can serve as stop loss levels for risk control. 

3. Simple parameters make it easy to implement and backtest.

4. RSI parameters can be optimized to determine the best overbought/oversold range.

5. Different price inputs can be used to adapt to various market environments.

## Risks and Solutions

There are also some risks with this strategy:

1. Excessive Bollinger Bands width leading to bad stop loss expectancy.

   - Adjust Bollinger Bands width parameter to optimize stop loss range.
   
2. Improper RSI parameter setting causing incorrect overbought/oversold level judgment.

   - Optimize RSI parameters through backtesting to determine the optimal trading range.
   
3. Unable to accurately determine trend reversal points, risk of missing signals.

   - Shorten Bollinger Bands period parameter to capture trend reversals earlier.
   
4. Unable to effectively control losses, risk of stop loss being hit by significant price swings.

   - Add moving or dynamic stop loss to optimize stop loss methods.

## Improvement Directions  

Some ways to optimize the strategy:

1. Optimize RSI parameters to determine the ideal overbought/oversold range.

2. Optimize Bollinger Bands width parameter to control stop loss range. 

3. Add other indicators to identify trend reversals and avoid missing signals.

4. Apply machine learning models to determine trading timing.

5. Use different parameter sets based on varying market environments. 

6. Add dynamic stop loss mechanisms.

7. Develop programs for automatic parameter optimization.

## Conclusion

In summary, by combining RSI and Bollinger Bands, this strategy forms relatively solid trading decisions. The logic is simple and clear, good for risk control, but has room for optimization. Further enhancing the strategy through parameter optimization, stop loss optimization, algorithm incorporation etc. can make it more adaptable to complex market environments. The strategy provides ideas for building trading systems and is worth further research and application.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|2|A|
|v_input_2|150|B|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-08-18 00:00:00
end: 2023-09-17 00:00:00
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Mdemoio


//@version=4
strategy("Madri", shorttitle="Madri", overlay=true)


// Version 1.1


///////////// RSI
RSIlength = input(2,title="A") 
RSIoverSold = 45
RSIoverBought = 40
price = close
vrsi = rsi(price, RSIlength)


///////////// Bollinger Bands
BBlength = input(150, minval=1,title="B")
BBmult = 2// input(2.0, minval=0.001, maxval=50,title="Bollinger Bands Standard Deviation")
BBbasis = sma(price, BBlength)
BBdev = BBmult * stdev(price, BBlength)
BBupper = BBbasis + BBdev
BBlower = BBbasis - BBdev
source = close
buyEntry = crossover(source, BBlower)
sellEntry = crossunder(source, BBupper)


///////////// Colors
//switch1=input(true, title="Enable Bar Color?")
//switch2=input(true, title="Enable Background Color?")
//TrendColor = RSIoverBought and (price[1] > BBupper and price < BBupper) and BBbasis < BBbasis[1] ? red : RSIoverSold and (price[1] < BBlower and price > BBlower) and BBbasis > BBbasis[1] ? green : na
//barcolor(switch1?TrendColor:na)
//bgcolor(switch2?TrendColor:na,transp=50)


///////////// RSI + Bollinger Bands Strategy
if (not na(vrsi))

    if (crossover(vrsi, RSIoverSold) and crossover(source, BBlower))
        strategy.entry("RSI_BB_L", strategy.long, stop=BBlower,  comment="Buy")
    else
        strategy.cancel(id="RSI_BB_L")
        
    if (crossunder(vrsi, RSIoverBought) and crossunder(source, BBupper))
        strategy.entry("RSI_BB_S", strategy.short, stop=BBupper, comment="Sell")
    else
        strategy.cancel(id="RSI_BB_S")

//plot(strategy.equity, title="equity", color=red, linewidth=2, style=areabr)
```

> Detail

https://www.fmz.com/strategy/427193

> Last Modified

2023-09-18 22:13:18
