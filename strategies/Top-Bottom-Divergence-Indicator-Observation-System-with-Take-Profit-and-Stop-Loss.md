
> Name

Top-Bottom-Divergence-Indicator-Observation-System-with-Take-Profit-and-Stop-Loss

> Author

Zer3192



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Stop Loss Percentage|
|v_input_2|true|Take profit percentage|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-03-01 00:00:00
end: 2023-02-28 23:59:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
args: [["v_input_1",99]]
*/

//@version=5
strategy("Top/Bottom Divergence Indicator Observation System with Take-Profit and Stop-Loss.", overlay=true)

// Enter stop-loss percentage and take-profit percentage; set here respectively.1%
stop_loss_pct = input(title="Stop Loss Percentage", type=input.float, defval=1.0, step=0.1)
take_profit_pct = input(title="Take profit percentage", type=input.float, defval=1.0, step=0.1)

// CalculationMACDIndicator
fastline = ta.ema(close,12)  
slowline = ta.ema(close,26)
diff = fastline - slowline 
dea = ta.ema(diff,9) 
macd = 2*(diff - dea)

// Determine the top divergence and bottom divergence signals
top_diver = ta.crossunder(macd,0) and close[1] > close
bot_diver = ta.crossover(macd,0) and close[1] < close
plotchar(top_diver, char='Top divergence', location = location.abovebar, size = size.normal, overlay=true)
plotchar(bot_diver, char='Bottom divergence', location = location.belowbar, size = size.normal, overlay=true)
// Determine whether to open a position
if top_diver and strategy.position_size>= 0
    strategy.entry("top_diver_short", strategy.short, comment="Top divergence open long")
else if bot_diver and strategy.position_size <=0
    strategy.entry("bot_diver_long", strategy.long, comment="Bottom divergence open short")
// Calculate take-profit and stop-loss prices
//Long Position Stop Loss
long_stop_price = strategy.position_avg_price * (1 - stop_loss_pct / 100)
//Long Position Take Profit
long_take_profit_price = strategy.position_avg_price * (1 + take_profit_pct / 100)
// Short Position Stop Loss
short_stop_price = (strategy.position_avg_price) * (1 + stop_loss_pct / 100)
// Short Position Take Profit
short_take_profit_price =(strategy.position_avg_price) * (1 - take_profit_pct / 100)
// Determine whether to close a position
if strategy.position_size > 0
    // Long Position Stop Loss
    strategy.exit("long_stop","bot_diver_long", stop=long_stop_price, qty_percent=100)
    // Long Position Take Profit
    strategy.exit("long_tp", "bot_diver_long", limit=long_take_profit_price, qty_percent=100)
else if strategy.position_size < 0
    strategy.exit("short_stop", "top_diver_short", stop=short_stop_price, qty_percent=100)
    strategy.exit("short_tp", "top_diver_short", limit=short_take_profit_price, qty_percent=100)


```

> Detail

https://www.fmz.com/strategy/402455

> Last Modified

2023-03-02 22:39:32
