
> Name

Improved-RSI-Breakout-Strategy-with-Stop-Loss-and-Take-Profit

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/177ff32b5af0907f550.png)

## Overview

The Modified RSI Breakout Strategy is a trend following strategy that uses the Relative Strength Index (RSI) indicator to determine entry and exit points. It adds stop-loss and take-profit orders to the basic RSI strategy to manage risk.

This strategy goes long when the RSI crosses 70 (overbought level). This strategy goes short when the RSI crosses below 30 (oversold level). This allows it to go with the flow, go with the flow, go with the flow, and go with the flow. Then use stop loss and take profit orders to lock in profits and limit losses.

## Working principle

The core mechanism of this strategy relies on the RSI indicator crossing its overbought level (default is 70) or oversold level (default is 30) to trigger an entry.

- When the RSI crosses above 70, it indicates the asset is overbought and may reverse, so the strategy is to open a long position.

- When the RSI crosses below 30, it indicates the asset is oversold and may rebound, so the strategy opens short positions.

This allows the strategy to profit from reversals at extreme RSI levels.

The key improvement is the introduction of stop-loss and take-profit orders to manage risk.

After entering the market, set a certain percentage of stop loss and take profit orders above and below the entry price (the default is 2% stop loss and 10% take profit). This locks in a fixed risk-to-reward ratio for each trade.

If the position moves favorably, a take-profit limit order will close the position at a profit. If the trend is unfavorable, a stop loss order will eliminate the trade with a small loss. This maximizes profits on winning positions and minimizes losses on losing positions.

## Advantage 

- Go with the trend, buy low, sell high
- Take profit greater than stop loss to achieve an asymmetric risk-reward ratio 
- Stop-loss minimizes losses from trades moving in the wrong direction
- The concept is simple and easy to understand and implement  
- Compared with the basic RSI strategy, it adds risk management advantages

## Risk

- If the RSI level crosses up and down multiple times, error signals may occur
- Stop loss position can be further optimized
- Take profit levels need to be fine-tuned for better performance  
- Performs best in trending markets, and weaker in range-bound markets.

## Optimization Direction 

Some ideas on how this strategy can be further improved:

- Add other filters before entering, such as price breakout
- Trace stop-loss to lock in more profit
- Expand your take-profit target for greater profit potential 
- Optimize RSI levels, stop loss percentage, take profit percentage for each market
- Set the stop-loss range based on ATR to adapt to market volatility

## Summary

The improved RSI breakout strategy brings together several positive factors - using RSI to identify potential turning points, judging direction based on momentum, achieving asymmetric risk-return ratio by taking profit greater than stop loss, and reducing risk through exit orders.

By combining these factors, the aim is to maximize returns and minimize risks in each transaction. Properly optimizing the position size can make it operate stably in different market environments. The built-in risk control system gives it an edge over the basic RSI strategy.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|70|overbought value|
|v_input_2|30|oversold value|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-04 00:00:00
end: 2024-02-03 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// @version=4
// Improved RSI Simple Strategy
// Added Risk Management System: SL & TP
// © Bitduke
// All scripts: https://www.tradingview.com/u/Bitduke/#published-scripts

strategy("Simple RSI Buy/Sell at a level", shorttitle="Simple RSI Strategy (SL/TP)", overlay=false )
overbought = input(70, title="overbought value")
oversold = input(30, title="oversold value")

lenght = 14
rsi = rsi(close, lenght)
myrsi = rsi > overbought
myrsi2 = rsi < oversold

barcolor(myrsi ? color.black : na)
barcolor(myrsi2 ? color.blue : na)

// Risk Management Sysyem
convert_percent_to_points(percent) =>
    strategy.position_size != 0 ? round(percent / 100 * strategy.position_avg_price / syminfo.mintick) : float(na)
    
setup_percent(percent) =>
    convert_percent_to_points(percent)

STOP_LOSS = 2
TAKE_PROFIT = 10

plot(rsi)
plot(overbought, color = color.red)
plot(oversold, color = color.green)

//STRATEGY
if (myrsi)
    strategy.entry("Long", strategy.long)
    
if (myrsi2)
    strategy.entry("Short", strategy.short)

strategy.exit("Exit", qty_percent = 100, profit = setup_percent(STOP_LOSS), loss = setup_percent(TAKE_PROFIT))


```

> Detail

https://www.fmz.com/strategy/440990

> Last Modified

2024-02-04 15:27:50
