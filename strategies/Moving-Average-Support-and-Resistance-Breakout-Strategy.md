
> Name

Moving-Average-Support-and-Resistance-Breakout-Strategy

> Author

ChaoZhang

> Strategy Description


## Overview

This strategy identifies key support and resistance levels based on moving averages, and takes trades when price breaks through these levels. The strategy is simple and effective, easy to understand and implement.

## Strategy Logic

The strategy uses a Simple Moving Average (SMA) with a period of 50 to identify support and resistance zones. Specifically:

- When close price crosses above SMA from below, the highest high over the past 50 periods is taken as resistance R
- When close price crosses below SMA from above, the lowest low over the past 50 periods is taken as support S
- Go long when close exceeds resistance R
- Go short when close breaks support S

In other words, the strategy uses the 50-period SMA to divide price zones, and takes trades when price breaks out of these zones. It goes long on breakouts above resistance, and goes short on breakdowns below support. The strategy is straightforward and easy to execute.

## Advantage Analysis 

The strategy has the following advantages:

1. Using moving averages to identify support/resistance is reasonably reliable and can effectively filter false breakouts.
2. A period of 50 is neither too long nor too short, and can detect meaningful medium-term levels.
3. It uses only a single SMA indicator, resulting in low system overhead and easy implementation.
4. Breakout trading strategies are simple and effective. 
5. There are few tunable parameters, avoiding excessive optimization.

## Risk Analysis

The strategy also has the following risks:

1. There is still some risk of false breakouts that SMAs cannot completely filter out.
2. The fixed period cannot adapt to different market cycles, potentially missing shorter-term opportunities.  
3. There may be pullbacks and retests after initial breakouts, requiring prudent stop loss techniques.
4. Larger trend direction needs to be monitored for longer-term trades.

These risks can be addressed through optimizations like adjusting the SMA period, adding trend filter indicators, etc. Proper stop loss management is also very important.

## Optimization Directions

Some ways the strategy can be enhanced:

1. Add indicators like MACD to help gauge trend direction and momentum.  
2. Implement adaptive optimization of MA periods for dynamic adjustment.
3. Improve breakout detection, e.g. requiring concurrent break of MA and Bollinger Bands.
4. Incorporate stop loss mechanisms to control single trade loss.
5. Test different MA period parameters to find optimal combinations.

These improvements can make the strategy more robust across different market cycles.

## Summary

Overall, the strategy identifies support/resistance with SMAs and trades breakouts, keeping things simple and effective. There is also significant room for optimization across multiple dimensions. While false breakouts remain a risk, prudent stop loss usage can effectively control this. The strategy is easy to understand for beginners and great for gaining practical experience.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|50|Number of lookback periods|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-01-01 00:00:00
end: 2023-09-27 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//--------------------------*
//-- This source code is subject to the terms of the Mozilla Public License 2.0
//-- Open source codeMozillaPublic License Terms2.0Version Specification, URL ishttps://mozilla.org/MPL/2.0/
//
//@version=4
//
//  Work: [LunaOwl] Support and resistance strategy No.4Edition
//  English text: [LunaOwl] Support Resistance Strategy V4
//
////////////////////////////////
//     ~~!!*(๑╹◡╹๑) **       //
//  Production:  @LunaOwl Peng Peng      //
//  Date:  2019Year03Moon05day     //
//  Modify:  2019Year04Moon22day     //
//  Fourth edition:  2020Year06Moon16day     //
//  Publish:  2020Year06Moon17day     //
////////////////////////////////

//==Set strategy==//

strategy("[LunaOwl] Support and resistance strategy [backtest]",
     shorttitle          = "Support and resistance strategy [backtest]",
     overlay             = true,
     calc_on_order_fills = false,
     calc_on_every_tick  = false,
     pyramiding          = 0,
     currency            = currency.NONE,
     initial_capital     = 10000,
     slippage            = 5,
     default_qty_value   = 100,
     default_qty_type    = strategy.percent_of_equity,
     commission_type     = strategy.commission.percent,
     commission_value    = 0.05
     )

LB = input(50, title = "Number of lookback periods", type = input.integer)
R = valuewhen(cross(sma(close, LB),close), highest(high, LB), 1)
S = valuewhen(cross(close,sma(close, LB)),  lowest( low, LB), 1)

plot(R, title = "Pressure", color = color.green)
plot(S, title = "Support", color = color.red)

//==Define output results==//

Trend_up = crossover(close, R) ? 1 : 0
Trend_dn = crossunder(close, S) ? -1 : 0

//==Set appearance rules==//

Enter = Trend_up ==  1 and Trend_up[1] == 0 ? Trend_up : na
Exit  = Trend_dn == -1 and Trend_dn[1] == 0 ? Trend_dn : na
strategy.entry("Many", strategy.long, when = Enter)
strategy.entry("Empty", strategy.short, when = Exit)
```

> Detail

https://www.fmz.com/strategy/428086

> Last Modified

2023-09-28 15:20:47
