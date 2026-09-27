
> Name

Adaptive-Trading-Strategy-Combining-Dynamic-Trend-Reversal-and-Stochastic-Indicator

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d8f459cc908daf2dcce5.png)
![IMG](https://www.fmz.com/upload/asset/2d8f16a03a65cc00deed1.png)





#### Overview
This strategy is an adaptive trading system that combines ZigZag percentage reversal with the Stochastic indicator. It identifies key reversal points through dynamic market volatility calculation and determines trading opportunities using Stochastic overbought/oversold signals. The strategy incorporates automatic take-profit and stop-loss mechanisms for effective risk management.

#### Strategy Principles
The core mechanism uses percentage reversal method to dynamically track market trends. Users can choose between manual setting of reversal percentage or dynamic calculation based on ATR across different periods (5-250 days). Buy signals are generated when price breaks above the reversal line with Stochastic K value below 30; sell signals occur when price breaks below the reversal line with K value above 70. The system automatically sets take-profit and stop-loss levels to protect profits and control risks.

#### Strategy Advantages
1. Dynamic adaptive reversal calculation method better suits different market conditions
2. Integration of trend reversal and momentum indicators provides more reliable trading signals
3. Built-in take-profit and stop-loss mechanisms help traders manage risk automatically
4. Flexible parameter settings allow traders to optimize according to personal trading styles
5. Visualized trading signals facilitate analysis and decision-making

#### Strategy Risks
1. May generate frequent false signals in ranging markets
2. ATR period selection impacts strategy performance
3. Fixed take-profit and stop-loss levels may not suit all market conditions
4. Stochastic indicator may lag in certain market conditions
5. Requires proper parameter setting to avoid overtrading

#### Strategy Optimization Directions
1. Introduce multiple timeframe analysis to improve signal reliability
2. Implement dynamic adjustment of take-profit and stop-loss levels for better market adaptation
3. Add volume indicators as confirmation signals
4. Develop adaptive Stochastic indicator parameters
5. Include trend strength filters to reduce false signals

#### Summary
This is a modernized trading strategy combining classic technical analysis tools. By integrating ZigZag reversal, Stochastic indicator, and risk management, it provides traders with a comprehensive trading system. The strategy's high customizability makes it suitable for traders with different risk preferences. Continuous optimization and parameter adjustment can further enhance the strategy's stability and profitability.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-06-04 00:00:00
end: 2025-02-19 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("[RS]ZigZag Percent Reversal with Stochastic Strategy", overlay=true)

// ZigZag Settings
string percent_method = input.string(
         defval="MANUAL", 
         title="Method to use for the zigzag reversal range:", 
         options=[
             "MANUAL", 
             "ATR005 * X", "ATR010 * X", "ATR020 * X", "ATR050 * X", "ATR100 * X", "ATR250 * X"
             ]
         )

var float percent = input.float(
         defval=0.25, 
         title="Percent of last pivot price for zigzag reversal:", 
         minval=0.0, maxval=99.0
         ) / 100

float percent_multiplier = input.float(
         defval=1.0, 
         title="Multiplier to apply to ATR if applicable:"
         )
if percent_method == "ATR005 * X"
    percent := ta.atr(5) / open * percent_multiplier
if percent_method == "ATR010 * X"
    percent := ta.atr(10) / open * percent_multiplier
if percent_method == "ATR020 * X"
    percent := ta.atr(20) / open * percent_multiplier
if percent_method == "ATR050 * X"
    percent := ta.atr(50) / open * percent_multiplier
if percent_method == "ATR100 * X"
    percent := ta.atr(100) / open * percent_multiplier
if percent_method == "ATR250 * X"
    percent := ta.atr(250) / open * percent_multiplier

// Zigzag function
f_zz(_percent)=>
    // Direction
    var bool _is_direction_up = na
    var float _htrack = na
    var float _ltrack = na
    var float _pivot = na
    float _reverse_range = 0.0
    var int _real_pivot_time = na
    var int _htime = na
    var int _ltime = na
    var float _reverse_line = na
    
    if bar_index >= 1
        
        if na(_is_direction_up)
            _is_direction_up := true
        
        _reverse_range := nz(_pivot[1]) * _percent
        
        if _is_direction_up
            _ltrack := na
            _ltime := time
            
            if na(_htrack)
                if high > high[1]
                    _htrack := high
                    _htime := time
                else
                    _htrack := high[1]
                    _htime := time[1]
            else
                if high > _htrack
                    _htrack := high
                    _htime := time

            _reverse_line := _htrack - _reverse_range
            
            if close <= _reverse_line
                _pivot := _htrack
                _real_pivot_time := _htime
                _is_direction_up := false

        if not _is_direction_up
            _htrack := na
            _htime := na
            
            if na(_ltrack)
                if low < low[1]
                    _ltrack := low
                    _ltime := time
                else
                    _ltrack := low[1]
                    _ltime := time[1]
            else
                if low < _ltrack
                    _ltrack := low
                    _ltime := time
                
            _reverse_line := _ltrack + _reverse_range
            
            if close >= _reverse_line
                _pivot := _ltrack
                _real_pivot_time := _ltime
                _is_direction_up := true

    [_pivot, _is_direction_up, _reverse_line, _real_pivot_time]

[pivot, direction_up, reverse_line, pivot_time] = f_zz(percent)

// Reversal line
var float static_reverse_line = na
if (not na(reverse_line))
    static_reverse_line := reverse_line

plot(series=static_reverse_line, color=color.gray, style=plot.style_line, title="Reversal Line", trackprice=false)

// Stochastic Settings
K_length = input.int(9, title="Stochastic K Length", minval=1)  // User input
K_smoothing = input.int(3, title="Stochastic K Smoothing", minval=1)  // User input
stochK = ta.sma(ta.stoch(close, high, low, K_length), K_smoothing)

// User Input: Take Profit and Stop Loss Levels
stop_loss_pips = input.int(100, title="Stop Loss (pips)", minval=1)  // Stop Loss
take_profit_pips = input.int(300, title="Take Profit (pips)", minval=1)  // Take Profit

// Calculating levels
long_stop_loss = close - stop_loss_pips * syminfo.mintick
long_take_profit = close + take_profit_pips * syminfo.mintick
short_stop_loss = close + stop_loss_pips * syminfo.mintick
short_take_profit = close - take_profit_pips * syminfo.mintick

// Buy and Sell Conditions
buy_signal = close > static_reverse_line and stochK < 30  // K < 30 condition
sell_signal = close < static_reverse_line and stochK > 70  // K > 70 condition

if buy_signal
    strategy.entry("Buy", strategy.long)
    strategy.exit("TP/SL", "Buy", stop=long_stop_loss, limit=long_take_profit)

if sell_signal
    strategy.entry("Sell", strategy.short)
    strategy.exit("TP/SL", "Sell", stop=short_stop_loss, limit=short_take_profit)

// Signal Visualization
plotshape(series=buy_signal, location=location.belowbar, color=color.green, style=shape.labelup, title="Buy Signal", text="BUY", textcolor=color.white)
plotshape(series=sell_signal, location=location.abovebar, color=color.red, style=shape.labeldown, title="Sell Signal", text="SELL", textcolor=color.white)

```

> Detail

https://www.fmz.com/strategy/483102

> Last Modified

2025-02-27 17:00:50
