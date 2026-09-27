
> Name

Super-Trend-Strategy-SuperTrend

> Author

发明者量化

> Strategy Description


At the request of platform users, FMZ is compatible with TradingView's Pine language function library, which has now entered a stable version

* Syntax fully compatible with v5 version
* taAll indicators in the library fully implemented
* mathLibrary fully implemented
* stringLibrary fully implemented
* arrayLibrary fully implemented
* inputInput parameters automatically recognized by the interface
* request.securitySupport for heikinashi
* strategyLibrary implementation (supports stop-loss/take-profit/trailing take-profit/condition orders and full support)
* plot/plotchar/plotshape/plotcandle/alert/alertcondition And other compatible

Full support for language functions is an ongoing effort; this public release is made public early to facilitate user testing

In the future, FMZ will continue to add and improve the function library support for TradingView's Pine language. If you have any needs, you can leave a message on this policy.

Note: If you encounter an undefined variable that proves that this attribute is not supported, you can delete the relevant call, or send a work order to contact technical personnel to solve the problem.

 ![IMG](https://www.fmz.com/upload/asset/114b4feedd1ae4f8550.png) 




> Source (PineScript)

``` pinescript
/*backtest
start: 2022-08-17 08:00:00
end: 2024-08-29 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Binance","currency":"BTC_USDT"}]
*/

strategy("supertrend", overlay=true, default_qty_type = strategy.percent_of_equity, default_qty_value = 50)

[supertrend, direction] = ta.supertrend(input(5, "factor"), input.int(10, "atrPeriod"))

plot(direction < 0 ? supertrend : na, "Up direction", color = color.green, style=plot.style_linebr)
plot(direction > 0 ? supertrend : na, "Down direction", color = color.red, style=plot.style_linebr)

if direction < 0
    if supertrend > supertrend[2]
        strategy.entry("entry long", strategy.long)
    else if strategy.position_size < 0
        strategy.close_all()
else if direction > 0
    if supertrend < supertrend[3]
        strategy.entry("entry short", strategy.short)
    else if strategy.position_size > 0
        strategy.close_all()

```

> Detail

https://www.fmz.com/strategy/359806

> Last Modified

2024-08-30 18:24:36
