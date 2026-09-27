
> Name

Trend-Following-Strategy-Based-on-Moving-Average-439858

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/139bbc2beb5c3cdd556.png)
 
## Overview  

This is a simple trend following strategy based on moving average. It judges the current trend direction and duration by comparing the size relationship between moving averages of different cycles. It goes long when the short cycle moving average crosses above the long cycle one, and goes short when the opposite happens. At the same time, stop loss and take profit points are set to control risks.  

## Strategy Logic

The strategy uses 4 moving averages with different cycles: 5-day, 10-day, 15-day and 25-day lines. They are called MA1, MA2, MA3 and MA4. Among them, MA1 is the shortest and MA4 is the longest.

When MA1>MA2>MA3>MA4, it indicates an upward trend and goes long. When MA1<MA2<MA3<MA4, it indicates a downward trend and goes short.

The open position conditions for both long and short need to satisfy the ATR stop loss filter at the same time, that is, the ATR value should be greater than the 40-day SMA of ATR. This avoids generating wrong signals when the price fluctuation is too small.

## Advantage Analysis 

The strategy has the following advantages:

1. The logic is simple and easy to implement.  
2. Using multiple moving averages to determine the trend direction is reliable.
3. Setting stop loss and take profit points can effectively control the maximum loss per trade.  
4. The ATR stop loss filter avoids wrong signals when the price fluctuation is small.

## Risk Analysis   

The strategy also has the following risks:

1. It is easy to generate wrong signals in a largely shock market.  
2. Improper parameter settings (cycle of moving average, etc) may lead to poor strategy performance.
3. It does not consider the impact of fundamentals and significant news on prices.  

To reduce these risks, parameters can be optimized appropriately, or additional filter conditions can be added to improve strategy stability.

## Optimization Directions

The optimization directions of the strategy include:

1. Test different combinations of moving average cycle parameters to find the optimal parameters.  
2. Add other technical indicators filters such as MACD and KDJ to judge the reliability of signals.
3. Add trading volume filter, only trade when trading volume expands.  
4. Fine-tune parameters based on differences between varieties. 
5. Add machine learning algorithms to judge signals.

## Conclusion  

In general, this is a relatively simple trend following strategy. It judges the trend direction through moving averages and sets reasonable stop loss and take profit to control risk levels. There is still much room for optimization, such as adjusting parameters, adding filters etc. to further improve the stability and profitability of the strategy.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|timestamp(20 Jan 1990 00:00 +0900)|(?Time)Start Date|
|v_input_2|timestamp(20 Dec 2030 00:00 +0900)|End Date|
|v_input_bool_1|true|(?Long / Short)Long?|
|v_input_bool_2|true|Short?|
|v_input_bool_3|true|(?Filters)ATR Filter On?|
|v_input_int_1|40|SMA Length for ATR SMA|
|v_input_bool_4|true|(?Shared Inputs)Enable SL & TP?|
|v_input_bool_5|false|Enable Trailing SL?|
|v_input_string_1|0|Stop Loss Type: ATR|Percent|
|v_input_int_2|14|ATR Length|
|v_input_string_2|0|Take Profit Type: R:R|ATR|Percent|
|v_input_float_1|50|Take Profit Quantity %|
|v_input_float_2|3|(?Long Stop Loss / Take Profit)SL Percent|
|v_input_float_3|3|TP Percent|
|v_input_float_4|3|SL ATR Multiplier|
|v_input_float_5|3|TP ATR Multiplier|
|v_input_float_6|1.8|R:R Ratio|
|v_input_float_7|3|(?Short Stop Loss / Take Profit)SL Percent|
|v_input_float_8|3|TP Percent|
|v_input_float_9|3|SL ATR Multiplier|
|v_input_float_10|3|TP ATR Multiplier|
|v_input_float_11|1.8|R:R Ratio|
|v_input_string_3|0|(?Strategy)MA Type: RMA|EMA|WMA|HMA|SMA|VWMA|SWMA|ALMA|VWAP|
|v_input_int_3|5|MA 1 Length|
|v_input_int_4|10|MA 2 Length|
|v_input_int_5|15|MA 3 Length|
|v_input_int_6|25|MA 4 Length|
|v_input_float_12|0.7|ALMA Offset Value|
|v_input_float_13|7|ALMA Sigma Value|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-01-17 00:00:00
end: 2024-01-23 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © fpemehd
// @version=5

// # ========================================================================= #
// #                   |   STRATEGY  |
// # ========================================================================= #

strategy(title = 'MA Simple Strategy with SL & TP & ATR Filters',
      shorttitle = 'MA Strategy',
      overlay = true,
      pyramiding = 0,
      default_qty_type = strategy.percent_of_equity,
      default_qty_value = 100,
      commission_type  = strategy.commission.percent,
      commission_value = 0.1,
      initial_capital = 100000,
      max_lines_count = 150,
      max_labels_count = 300)

// # ========================================================================= #
// #                          Inputs
// # ========================================================================= #

// 1. Time
i_start = input (defval = timestamp("20 Jan 1990 00:00 +0900"), title = "Start Date", tooltip = "Choose Backtest Start Date", inline = "Start Date", group = "Time" ) 
i_end = input (defval = timestamp("20 Dec 2030 00:00 +0900"), title = "End Date", tooltip = "Choose Backtest End Date", inline = "End Date", group = "Time" ) 
c_timeCond = true

// 2. Inputs for direction: Long? Short? Both? 
i_longEnabled = input.bool(defval = true , title = "Long?", tooltip = "Enable Long Position Trade?", inline = "Long / Short", group = "Long / Short" )
i_shortEnabled = input.bool(defval = true , title = "Short?", tooltip = "Enable Short Position Trade?", inline = "Long / Short", group = "Long / Short" )

// 3. Use Filters? What Filters?
i_ATRFilterOn = input.bool(defval = true , title = "ATR Filter On?", tooltip = "ATR Filter On?", inline = "ATR Filter", group =  "Filters") 
i_ATRSMALen = input.int(defval = 40 , title = "SMA Length for ATR SMA", minval = 1 , maxval = 100000 , step = 1 , tooltip = "ATR should be bigger than this", inline = "ATR Filter", group = "Filters") 

// 3. Shared inputs for Long and Short
//// 3-1. Inputs for Stop Loss Type: normal? or trailing? 
//// If trailing, always trailing or trailing after take profit order executed?
i_useSLTP = input.bool(defval =  true, title = "Enable SL & TP?", tooltip = "", inline = "Enable SL & TP & SL Type", group = "Shared Inputs") 
i_tslEnabled = input.bool(defval = false , title = "Enable Trailing SL?", tooltip = "Enable Stop Loss & Take Profit? \n\Enable Trailing SL?", inline = "Enable SL & TP & SL Type", group = "Shared Inputs") 
// i_tslAfterTP = input.bool(defval = true , title = "Enable Trailing SL after TP?", tooltip = "Enable Trailing SL after TP?", inline = "Trailing SL Execution", group = "Shared Inputs") 
i_slType = input.string(defval = "ATR", title = "Stop Loss Type", options = ["Percent", "ATR"], tooltip = "Stop Loss based on %? ATR?", inline = "Stop Loss Type", group = "Shared Inputs") 
i_slATRLen = input.int(defval = 14, title = "ATR Length", minval = 1 , maxval = 200 , step = 1, inline = "Stop Loss ATR", group = "Shared Inputs")  
i_tpType = input.string(defval = "R:R", title = "Take Profit Type", options = ["Percent", "ATR", "R:R"], tooltip = "Take Profit based on %? ATR? R-R ratio?", inline = "Take Profit Type", group = "Shared Inputs") 

//// 3-2. Inputs for Quantity
i_tpQuantityPerc = input.float(defval = 50, title = 'Take Profit Quantity %', minval = 0.0, maxval = 100, step = 1.0, tooltip = '% of position when tp target is met.', group = 'Shared Inputs')

// 4. Inputs for Long Stop Loss & Long Take Profit

i_slPercentLong = input.float(defval = 3, title = "SL Percent", tooltip = "", inline = "Percent > Long Stop Loss / Take Profit Percent", group = "Long Stop Loss / Take Profit") 
i_tpPercentLong = input.float(defval = 3, title = "TP Percent", tooltip = "Long Stop Loss && Take Profit Percent?", inline = "Percent > Long Stop Loss / Take Profit Percent", group = "Long Stop Loss / Take Profit") 
i_slATRMultLong = input.float(defval = 3, title = "SL ATR Multiplier", minval = 1 , maxval = 200 , step = 0.1, tooltip = "", inline = "Long Stop Loss / Take Profit ATR", group = "Long Stop Loss / Take Profit") 
i_tpATRMultLong = input.float(defval = 3, title = "TP ATR Multiplier", minval = 1 , maxval = 200 , step = 0.1, tooltip = "ATR > Long Stop Loss && Take Profit ATR Multiplier? \n\Stop Loss = i_slATRMultLong * ATR (i_slATRLen) \n\Take Profit = i_tpATRMultLong * ATR (i_tpATRLen)", inline = "Long Stop Loss / Take Profit ATR", group = "Long Stop Loss / Take Profit") 
i_tpRRratioLong = input.float(defval = 1.8, title = "R:R Ratio", minval = 0.1 , maxval = 200 , step = 0.1, tooltip = "R:R Ratio > Risk Reward Ratio? It will automatically set Take Profit % based on Stop Loss", inline = "R:R Ratio", group = "Long Stop Loss / Take Profit") 

// 5. Inputs for Short Stop Loss & Short Take Profit
i_slPercentShort = input.float(defval = 3, title = "SL Percent", tooltip = "", inline = "Percent > Short Stop Loss / Take Profit Percent", group = "Short Stop Loss / Take Profit") 
i_tpPercentShort = input.float(defval = 3, title = "TP Percent", tooltip = "Short Stop Loss && Take Profit Percent?", inline = "Percent > Short Stop Loss / Take Profit Percent", group = "Short Stop Loss / Take Profit") 
i_slATRMultShort = input.float(defval = 3, title = "SL ATR Multiplier", minval = 1 , maxval = 200 , step = 0.1, tooltip = "", inline = "ATR > Short Stop Loss / Take Profit ATR", group = "Short Stop Loss / Take Profit") 
i_tpATRMultShort = input.float(defval = 3, title = "TP ATR Multiplier", minval = 1 , maxval = 200 , step = 0.1, tooltip = "ATR > Short Stop Loss && Take Profit ATR Multiplier? \n\Stop Loss = i_slATRMultShort * ATR (i_slATRLen) \n\Take Profit = i_tpATRMultShort * ATR (i_tpATRLen)", inline = "ATR > Short Stop Loss / Take Profit ATR", group = "Short Stop Loss / Take Profit") 
i_tpRRratioShort = input.float(defval = 1.8, title = "R:R Ratio", minval = 0.1 , maxval = 200 , step = 0.1, tooltip = "R:R Ratio > Risk Reward Ratio? It will automatically set Take Profit % based on Stop Loss", inline = "R:R Ratio", group = "Short Stop Loss / Take Profit") 

// 6. Inputs for logic
i_MAType = input.string(defval = "RMA", title = "MA Type", options = ["SMA", "EMA", "WMA", "HMA", "RMA", "VWMA", "SWMA", "ALMA", "VWAP"], tooltip = "Choose MA Type", inline = "MA Type", group = 'Strategy') 
i_MA1Len = input.int(defval = 5, title = 'MA 1 Length', minval = 1, inline = 'MA Length', group = 'Strategy')
i_MA2Len = input.int(defval = 10, title = 'MA 2 Length', minval = 1, inline = 'MA Length', group = 'Strategy')
i_MA3Len = input.int(defval = 15, title = 'MA 3 Length', minval = 1, inline = 'MA Length', group = 'Strategy')
i_MA4Len = input.int(defval = 25, title = 'MA 4 Length', minval = 1, inline = 'MA Length', group = 'Strategy')
i_ALMAOffset = input.float(defval = 0.7 , title = "ALMA Offset Value", tooltip = "The Value of ALMA offset", inline = "ALMA Input", group = 'Strategy')
i_ALMASigma = input.float(defval = 7 , title = "ALMA Sigma Value", tooltip = "The Value of ALMA sigma", inline = "ALMA Input", group = 'Strategy')

// # ========================================================================= #
// #                          Entry, Close Logic
// # ========================================================================= #

bool i_ATRFilter = ta.atr(length = i_slATRLen) >= ta.sma(source = ta.atr(length = i_slATRLen), length = i_ATRSMALen) ? true : false

// calculate Technical Indicators for the Logic

getMAValue (source, length, almaOffset, almaSigma) => 
    switch i_MAType 
        'SMA' => ta.sma(source = source, length = length) 
        'EMA' => ta.ema(source = source, length = length) 
        'WMA' => ta.wma(source = source, length = length) 
        'HMA' => ta.hma(source = source, length = length) 
        'RMA' => ta.rma(source = source, length = length) 
        'SWMA' => ta.swma(source = source) 
        'ALMA' => ta.alma(series = source, length = length, offset = almaOffset, sigma = almaSigma) 
        'VWMA' => ta.vwma(source = source, length = length) 
        'VWAP' => ta.vwap(source = source)
        => na 

float c_MA1 = getMAValue(close, i_MA1Len, i_ALMAOffset, i_ALMASigma)
float c_MA2 = getMAValue(close, i_MA2Len, i_ALMAOffset, i_ALMASigma)
float c_MA3 = getMAValue(close, i_MA3Len, i_ALMAOffset, i_ALMASigma)
float c_MA4 = getMAValue(close, i_MA4Len, i_ALMAOffset, i_ALMASigma)

// Logic: 정배열 될 떄 들어가
var ma1Color = color.new(color.red, 0)
plot(series = c_MA1, title = 'SMA 1', color = ma1Color, linewidth = 1, style = plot.style_line)
var ma2Color = color.new(color.orange, 0)
plot(series = c_MA2, title = 'SMA 2', color = ma2Color, linewidth = 1, style = plot.style_line)
var ma3Color = color.new(color.yellow, 0)
plot(series = c_MA3, title = 'SMA 3', color = ma3Color, linewidth = 1, style = plot.style_line)
var ma4Color = color.new(color.green, 0)
plot(series = c_MA4, title = 'SMA 4', color = ma4Color, linewidth = 1, style = plot.style_line)

bool openLongCond = (c_MA1 >= c_MA2 and c_MA2 >= c_MA3 and c_MA3 >= c_MA4) 
bool openShortCond = (c_MA1 <= c_MA2 and c_MA2 <= c_MA3 and c_MA3 <= c_MA4)

bool openLong = i_longEnabled and openLongCond and (not i_ATRFilterOn or i_ATRFilter)
bool openShort = i_shortEnabled and openShortCond and (not i_ATRFilterOn or i_ATRFilter)

openLongCondColor = openLongCond ? color.new(color = color.blue, transp = 80) : na
bgcolor(color = openLongCondColor)
ATRFilterColor = i_ATRFilter ? color.new(color = color.orange, transp = 80) : na 
bgcolor(color = ATRFilterColor)

bool enterLong = openLong and not (strategy.opentrades.size(strategy.opentrades-1) > 0)
bool enterShort = openShort and not (strategy.opentrades.size(strategy.opentrades-1) < 0)

bool closeLong = i_longEnabled and (c_MA1[1] >= c_MA2[1] and c_MA2[1] >= c_MA3[1] and c_MA3[1] >= c_MA4[1]) and not (c_MA1 >= c_MA2 and c_MA2 >= c_MA3 and c_MA3 >= c_MA4) 
bool closeShort = i_shortEnabled and (c_MA1[1] <= c_MA2[1] and c_MA2[1] <= c_MA3[1] and c_MA3[1] <= c_MA4[1]) and not (c_MA1 <= c_MA2 and c_MA2 <= c_MA3 and c_MA3 <= c_MA4)

// # ========================================================================= #
// #                          Position, Status Conrtol
// # ========================================================================= #

// longisActive: New Long || Already Long && not closeLong, short is the same
bool longIsActive = enterLong or strategy.opentrades.size(strategy.opentrades - 1) > 0 and not closeLong
bool shortIsActive = enterShort or strategy.opentrades.size(strategy.opentrades - 1) < 0 and not closeShort

// before longTPExecution: no trailing SL && after longTPExecution: trailing SL starts
// longTPExecution qunatity should be less than 100% 
bool longTPExecuted = false
bool shortTPExecuted = false

// # ========================================================================= #
// #                          Long Stop Loss Logic
// # ========================================================================= #
float openAtr = ta.valuewhen(enterLong or enterShort, ta.atr(i_slATRLen), 0)

f_getLongSL (source) => 
    switch i_slType
        'Percent' => source * (1 - (i_slPercentLong/100))
        'ATR' => source - i_slATRMultLong * openAtr
        => na

var float c_longSLPrice = na
c_longSLPrice := if (longIsActive)
    if (enterLong)
        f_getLongSL(close)
    else
        c_stopPrice = f_getLongSL(i_tslEnabled ? high : strategy.opentrades.entry_price(trade_num = strategy.opentrades - 1))
        math.max(c_stopPrice, nz(c_longSLPrice[1]))
else
    na

// # ========================================================================= #
// #                          Short Stop Loss Logic
// # ========================================================================= #
f_getShortSL (source) => 
    switch i_slType
        'Percent' => source * (1 + (i_slPercentShort)/100)
        'ATR' => source + i_slATRMultShort * openAtr
        => na

var float c_shortSLPrice = na
c_shortSLPrice := if (shortIsActive)
    if (enterShort)
        f_getShortSL (close)
    else
        c_stopPrice = f_getShortSL(i_tslEnabled ? low : strategy.opentrades.entry_price(strategy.opentrades - 1))
        math.min(c_stopPrice, nz(c_shortSLPrice[1], 999999.9))
else
    na

// # ========================================================================= #
// #                          Long Take Profit Logic
// # ========================================================================= #

f_getLongTP () => 
    switch i_tpType
        'Percent' => close * (1 + (i_tpPercentLong/100))
        'ATR' => close + i_tpATRMultLong * openAtr
        'R:R' => close + i_tpRRratioLong * (close - f_getLongSL(close))
        => na

var float c_longTPPrice = na
c_longTPPrice := if (longIsActive and not longTPExecuted)
    if (enterLong)
        f_getLongTP()
    else 
        nz(c_longTPPrice[1], f_getLongTP())
else
    na

longTPExecuted := strategy.opentrades.size(strategy.opentrades - 1) > 0 and (longTPExecuted[1] or strategy.opentrades.size(strategy.opentrades - 1) < strategy.opentrades.size(strategy.opentrades - 1)[1] or strategy.opentrades.size(strategy.opentrades - 1)[1] == 0 and high >= c_longTPPrice)

// # ========================================================================= #
// #                          Short Take Profit Logic
// # ========================================================================= #

f_getShortTP () => 
    switch i_tpType
        'Percent' => close * (1 - (i_tpPercentShort/100))
        'ATR' => close - i_tpATRMultShort * openAtr
        'R:R' => close - i_tpRRratioShort * (close - f_getLongSL(close))
        => na

var float c_shortTPPrice = na
c_shortTPPrice := if (shortIsActive and not shortTPExecuted)
    if (enterShort)
        f_getShortTP()
    else
        nz(c_shortTPPrice[1], f_getShortTP())
else
    na

shortTPExecuted := strategy.opentrades.size(strategy.opentrades - 1) < 0 and (shortTPExecuted[1] or strategy.opentrades.size(strategy.opentrades - 1) > strategy.opentrades.size(strategy.opentrades - 1)[1] or strategy.opentrades.size(strategy.opentrades - 1)[1] == 0 and low <= c_shortTPPrice)

// # ========================================================================= #
// #                          Make Orders
// # ========================================================================= #

if (c_timeCond)
    if (enterLong)
        strategy.entry(id = "Long Entry", direction = strategy.long , comment = 'Long(' + syminfo.ticker + '): Started', alert_message = 'Long(' + syminfo.ticker + '): Started')

    if (enterShort)
        strategy.entry(id = "Short Entry", direction = strategy.short , comment = 'Short(' + syminfo.ticker + '): Started', alert_message = 'Short(' + syminfo.ticker + '): Started')

    if (closeLong)
        strategy.close(id = 'Long Entry', comment = 'Close Long', alert_message = 'Long: Closed at market price')

    if (closeShort)
        strategy.close(id = 'Short Entry', comment = 'Close Short', alert_message = 'Short: Closed at market price')

    if (longIsActive and i_useSLTP)
        strategy.exit(id = 'Long Take Profit / Stop Loss', from_entry = 'Long Entry', qty_percent = i_tpQuantityPerc, limit = c_longTPPrice, stop = c_longSLPrice, alert_message = 'Long(' + syminfo.ticker + '): Take Profit or Stop Loss executed')
        strategy.exit(id = 'Long Stop Loss', from_entry = 'Long Entry', stop = c_longSLPrice, alert_message = 'Long(' + syminfo.ticker + '): Stop Loss executed')
    
    if (shortIsActive and i_useSLTP)
        strategy.exit(id = 'Short Take Profit / Stop Loss', from_entry = 'Short Entry', qty_percent = i_tpQuantityPerc, limit = c_shortTPPrice, stop = c_shortSLPrice, alert_message = 'Short(' + syminfo.ticker + '): Take Profit or Stop Loss executed')
        strategy.exit(id = 'Short Stop Loss', from_entry = 'Short Entry', stop = c_shortSLPrice, alert_message = 'Short(' + syminfo.ticker + '): Stop Loss executed')

// # ========================================================================= #
// #                          Plot
// # ========================================================================= #

var posColor = color.new(color.white, 0)
plot(series = strategy.opentrades.entry_price(strategy.opentrades - 1), title = 'Position', color = posColor, linewidth = 1, style = plot.style_linebr)

var stopLossColor = color.new(color.maroon, 0)
plot(series = c_longSLPrice, title = 'Long Stop Loss', color = stopLossColor, linewidth = 1, style = plot.style_linebr, offset = 1)
plot(series = c_shortSLPrice, title = 'Short Stop Loss', color = stopLossColor, linewidth = 1, style = plot.style_linebr, offset = 1)

longTPExecutedColor = longTPExecuted ? color.new(color = color.green, transp = 80) : na 
//bgcolor(color = longTPExecutedColor) 
shortTPExecutedColor = shortTPExecuted ? color.new(color = color.red, transp = 80) : na 
//bgcolor(color = shortTPExecutedColor) 
// isPositionOpenedColor = strategy.opentrades.size(strategy.opentrades-1) != 0 ? color.new(color = color.yellow, transp = 90) : na 
// bgcolor(color = isPositionOpenedColor) 

var takeProfitColor = color.new(color.teal, 0)
plot(series = c_longTPPrice, title = 'Long Take Profit', color = takeProfitColor, linewidth = 1, style = plot.style_linebr, offset = 1)
plot(series = c_shortTPPrice, title = 'Short Take Profit', color = takeProfitColor, linewidth = 1, style = plot.style_linebr, offset = 1)
```

> Detail

https://www.fmz.com/strategy/439858

> Last Modified

2024-01-24 14:24:36
