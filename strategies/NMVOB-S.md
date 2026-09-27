
> Name

NMVOB-S

> Author

ChaoZhang

> Strategy Description

**backtest**

 ![IMG](https://www.fmz.com/upload/asset/198ea25e0b20cb3e586.png) 

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_float_1|50000|Starting Capital|
|v_input_int_1|5|leverage|
|v_input_1|false|Number of Stop-Loss Bars|
|v_input_float_2|true|Take Profit Ratio|
|v_input_2|13|MACD Fast MA|
|v_input_3|21|MACD Slow MA|
|v_input_4|9|MACD Trigger|
|v_input_5|50|MACD Normalize|
|v_input_int_2|true|(MACD) 1=Ema, 2=Wma, 3=Sma|
|v_input_6|100|VS timeframe|
|v_input_int_3|34|Bollinger Bands Period|
|v_input_7_close|0|Boollinger Bands Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_float_3|2|StdDev|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-04-10 00:00:00
end: 2022-05-09 23:59:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5

// # ========================================================================= #
// #                   |   STRATEGY  |
// # ========================================================================= #
strategy(title = "NMVOB-S", shorttitle = "NMVOB-S", overlay = true , calc_on_every_tick = false , initial_capital = 0)
// # ========================================================================= #
// #                   |  Global Variables START  |
// # ========================================================================= #
var current_trend = int(na)
var open_order_type = int(na)
var stop_loss_price = float(na)
var stop_profit_price = float(na)
var sl = float(na)
var open_order_price = float(na)
var open_type_flag = int(na)
var stop_profit_flag = 0

var macd_signal_position = 0
var macd_signal_type = int(na)

var start_price = input.float(50000, "Starting Capital")
var gg = input.int(5, "leverage")

// # ========================================================================= #
// #                   |  Global Variables END  |
// # ========================================================================= #

// # ========================================================================= #
// #                   |  Custom Function START  |
// # ========================================================================= #
stop_loss_pillars = input(defval = 0, title = "Number of Stop-Loss Bars")
stop_profit_proportion = input.float(1,"Take Profit Ratio")
//Calculate Stop-Loss Price
calculate_stop_loss() =>
    if current_trend == 1
        stop_loss_price_buy = low
        if stop_loss_pillars == 0
            stop_loss_price_buy
        else
            for i = 1 to stop_loss_pillars 
                if low[i] < stop_loss_price_buy
                    stop_loss_price_buy := low[i]
                else if low[i] > stop_loss_price_buy
                    stop_loss_price_buy
            stop_loss_price_buy
    else
        stop_loss_price_sell = high
        if stop_loss_pillars == 0
            stop_loss_price_sell
        else
            for i = 1 to stop_loss_pillars 
                if high[i] < stop_loss_price_sell
                    stop_loss_price_sell
                else if high[i] > stop_loss_price_sell
                    stop_loss_price_sell := high[i]
            stop_loss_price_sell

//Calculate Take Profit
calculate_stop_profit(cur_stop_loss_price) =>
    value = math.abs(close - cur_stop_loss_price) * stop_profit_proportion
    if current_trend == 1
        close + value
    else
        close - value   

// # ========================================================================= #
// #                   |  Custom Function END  |
// # ========================================================================= #


// # ========================================================================= #
// #                   |   Normalized MACD  |
// # ========================================================================= #
sma = input(13,title='MACD Fast MA')
lma = input(21,title='MACD Slow MA')
tsp = input(9,title='MACD Trigger')
np = input(50,title='MACD Normalize')
type = input.int(1,minval=1,maxval=3,title="(MACD) 1=Ema, 2=Wma, 3=Sma")

sh = type == 1 ? ta.ema(close,sma)  
 : type == 2 ? ta.wma(close, sma)
 : ta.sma(close, sma)

lon=type == 1 ? ta.ema(close,lma) 
 : type == 2 ? ta.wma(close, lma)
 : ta.sma(close, lma)

ratio = math.min(sh,lon)/math.max(sh,lon)

Mac = if sh>lon
    2 - ratio - 1
else
    ratio - 1
//Fast line
MacNorm = ((Mac-ta.lowest(Mac, np)) /(ta.highest(Mac, np)-ta.lowest(Mac, np)+.000001)*2)- 1

MacNorm2 = if np < 2
    Mac
else
    MacNorm
//Slow line    
Trigger = ta.wma(MacNorm2, tsp)

if ta.crossover(source1 = MacNorm, source2 = Trigger) 
    macd_signal_position := 0
    macd_signal_type := 1
else if ta.crossunder(source1 = MacNorm, source2 = Trigger) 
    macd_signal_position := 0
    macd_signal_type := 0
else
    macd_signal_position += 1

// # ========================================================================= #
// #                   |   Normalized MACD  |
// # ========================================================================= #


// # ========================================================================= #
// #                   |  Volatility Oscillator START  |
// # ========================================================================= #
length = input(100, title="VS timeframe")
spike = close - open
vs_up_line = ta.stdev(spike,length)
vs_low_line = ta.stdev(spike,length) * -1
// # ========================================================================= #
// #                   |  Volatility Oscillator END  |
// # ========================================================================= #


// # ========================================================================= #
// #                   |  Bollinger Bands  |
// # ========================================================================= #
b_length = input.int(34, minval=1 , title="Bollinger Bands Period")
src = input(close, title="Boollinger Bands Source")
mult = input.float(2.0, minval=0.001, maxval=50, title="StdDev")
basis = ta.sma(src, b_length)
dev = mult * ta.stdev(src, b_length)
upper = basis + dev
lower = basis - dev
offset = 0
plot(basis, "Bollinger Bands Middle Line", color=color.white, offset = offset)
plot(upper, "Bollinger Band is on track", color=color.red, offset = offset)
plot(lower, "Bollinger Bands are off track", color=color.blue, offset = offset)
// # ========================================================================= #
// #                   |  Bollinger Bands  |
// # ========================================================================= #

if true
    if strategy.opentrades == 0 and barstate.isnew
        //macdUp/Down Condition
        long_macd_conditions = macd_signal_type == 1 and macd_signal_position <= 10
        short_macd_conditions = macd_signal_type == 0 and macd_signal_position <= 10
        // Volatility Oscillator Up/Down Condition
        long_vs_conditions = ta.crossover(source1 = spike, source2 = vs_up_line) 
        short_vs_conditions = ta.crossunder(source1 = spike, source2 = vs_low_line) 
        //Bollinger Bands rise and fall conditions
        long_bollinger_conditions = low < basis and close > basis and high < upper
        short_bollinger_conditions = high > basis and close < basis and low > lower
      
        //Conditions for opening long orders
        open_long_order_conditions = long_macd_conditions and long_vs_conditions and long_bollinger_conditions 
        //Conditions for opening short orders
        open_short_order_conditions = short_macd_conditions and short_vs_conditions and short_bollinger_conditions 

        if open_long_order_conditions
            current_trend := 1
            stop_loss_price := calculate_stop_loss()
            stop_profit_price := calculate_stop_profit(stop_loss_price)
            open_order_type := 1
            sl := (start_price * gg) / close
            open_order_price := close
            open_type_flag := 1
            if sl > 0
                strategy.order(id = "long order", direction = strategy.long , qty = sl, limit = close, stop = stop_loss_price, comment = "Long position", when = open_long_order_conditions)
        else if open_short_order_conditions
            current_trend := 0
            stop_loss_price := calculate_stop_loss()
            stop_profit_price := calculate_stop_profit(stop_loss_price)
            open_order_type := 0
            sl := (start_price * gg) / close
            open_order_price := close
            open_type_flag := 0
            if sl > 0
                strategy.order(id = "short order", direction = strategy.short , qty = sl, limit = close, stop = stop_loss_price, comment = "Short position", when = open_short_order_conditions)
        
    else if strategy.opentrades == 1
        if open_order_type == 1 
            if close <= stop_loss_price or close >= stop_profit_price
                stop_loss_price := float(na)
                stop_profit_price := float(na)
                lr = (close - open_order_price) * sl
                start_price := start_price + lr
                strategy.close_all(when = true, comment = "close long")
            
        if open_order_type == 0 
            if close >= stop_loss_price or close <= stop_profit_price 
                stop_loss_price := float(na)
                stop_profit_price := float(na)
                lr = (open_order_price - close) * sl
                start_price := start_price + lr
                strategy.close_all(when = true, comment = "close short")
           

plot(series = current_trend, title = "Current Trend", color = color.orange, style = plot.style_circles)
plot(series = strategy.opentrades, title = "Unclosed order quantity", color = color.orange, style = plot.style_circles)
plot(series = open_order_type, title = "Order Type", color = color.orange, style = plot.style_circles)
plot(series = open_order_price, title = "Opening price", color = color.orange, style = plot.style_circles)
plot(series = stop_loss_price, title = "Stop loss price", color = color.orange, style = plot.style_circles)
plot(series = stop_profit_price, title = "Take-profit price", color = color.orange, style = plot.style_circles)
plot(series = sl, title = "Order Quantity", color = color.orange, style = plot.style_circles)
plot(series = start_price, title = "Remaining Amount", color = color.orange, style = plot.style_circles)

```

> Detail

https://www.fmz.com/strategy/362503

> Last Modified

2022-05-11 22:29:36
