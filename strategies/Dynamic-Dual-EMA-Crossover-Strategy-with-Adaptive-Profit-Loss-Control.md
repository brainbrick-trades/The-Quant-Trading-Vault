
> Name

Dynamic-Dual-EMA-Crossover-Strategy-with-Adaptive-Profit-Loss-Control

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/bb7c3cbf69f1936617.png)


#### Overview
This is a quantitative trading strategy based on dual EMA crossover signals, which uses the intersection of fast and slow Exponential Moving Averages (EMA) to determine market trends, combined with dynamic take-profit and stop-loss controls for risk management. The strategy employs percentage-based position management, defaulting to 10% of capital per trade, and implements dynamic profit targets and stop-loss levels for protection.

#### Strategy Principles
The core logic revolves around monitoring crossovers between 20-period and 50-period EMAs to identify trend changes. A long position is initiated when the fast EMA crosses above the slow EMA. Upon entry, the system automatically sets take-profit levels (1.3 times entry price) and stop-loss levels (0.95 times entry price). This dynamic profit/loss control design adapts to different market conditions, enhancing strategy flexibility.

#### Strategy Advantages
1. Signal Stability - Uses EMA instead of SMA, providing faster response to price changes while filtering market noise.
2. Comprehensive Risk Management - Implements dynamic take-profit and stop-loss mechanisms that adjust with entry prices.
3. Rational Capital Management - Uses fixed proportion position sizing, avoiding high-risk full position trading.
4. High Automation - Automates everything from signal generation to position management, reducing human intervention.
5. Strong Adaptability - Strategy can adapt to different market conditions with adjustable parameters.

#### Strategy Risks
1. EMA Lag - Despite being faster than SMA, EMA still has some inherent lag, potentially causing delayed entries.
2. Poor Performance in Ranging Markets - May generate frequent false breakout signals during sideways market conditions.
3. Fixed Multiplier for Profit/Loss - Using fixed multipliers for take-profit and stop-loss may not suit all market conditions.
4. Drawdown Risk - 5% stop-loss might not be sufficient in highly volatile markets.

#### Optimization Directions
1. Incorporate Volatility Indicators - Suggest adding ATR to dynamically adjust profit/loss multipliers for better market adaptation.
2. Add Trend Confirmation - Consider incorporating RSI, MACD for signal filtering to improve win rate.
3. Optimize Position Sizing - Implement dynamic position sizing based on market volatility for finer risk control.
4. Add Time Filters - Consider adding trading time windows to avoid highly volatile periods.
5. Enhance Profit-Taking - Implement trailing stops to capture more profit in strong trends.

#### Conclusion
This is a well-designed trend-following strategy with clear logic, using dual EMA crossovers for trend capture and dynamic profit/loss controls for risk management. The strategy's strengths lie in its clear rules and controlled risk, making it suitable as a foundation for medium to long-term trading systems. There's significant room for optimization through additional filters and enhanced profit/loss mechanisms. Traders should validate the strategy through backtesting across different market conditions and adjust parameters according to their risk tolerance before live implementation.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-12-09 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Pineify

//======================================================================//
//                    ____  _            _  __                          //
//                   |  _ \(_)_ __   ___(_)/ _|_   _                    //
//                   | |_) | | '_ \ / _ \ | |_| | | |                   //
//                   |  __/| | | | |  __/ |  _| |_| |                   //
//                   |_|   |_|_| |_|\___|_|_|  \__, |                   //
//                                             |___/                    //
//======================================================================//

//@version=5
strategy(title="TQQQ EMA Strategy", overlay=true)

//#region -------------------------------------------------- Common Dependence

p_comm_time_range_to_unix_time(string time_range, int date_time = time, string timezone = syminfo.timezone) =>
    int start_unix_time = na
    int end_unix_time = na
    int start_time_hour = na
    int start_time_minute = na
    int end_time_hour = na
    int end_time_minute = na
    if str.length(time_range) == 11
        // Format: hh:mm-hh:mm
        start_time_hour := math.floor(str.tonumber(str.substring(time_range, 0, 2)))
        start_time_minute := math.floor(str.tonumber(str.substring(time_range, 3, 5)))
        end_time_hour := math.floor(str.tonumber(str.substring(time_range, 6, 8)))
        end_time_minute := math.floor(str.tonumber(str.substring(time_range, 9, 11)))
    else if str.length(time_range) == 9
        // Format: hhmm-hhmm
        start_time_hour := math.floor(str.tonumber(str.substring(time_range, 0, 2)))
        start_time_minute := math.floor(str.tonumber(str.substring(time_range, 2, 4)))
        end_time_hour := math.floor(str.tonumber(str.substring(time_range, 5, 7)))
        end_time_minute := math.floor(str.tonumber(str.substring(time_range, 7, 9)))
    start_unix_time := timestamp(timezone, year(date_time, timezone), month(date_time, timezone), dayofmonth(date_time, timezone), start_time_hour, start_time_minute, 0)
    end_unix_time := timestamp(timezone, year(date_time, timezone), month(date_time, timezone), dayofmonth(date_time, timezone), end_time_hour, end_time_minute, 0)
    [start_unix_time, end_unix_time]

p_comm_time_range_to_start_unix_time(string time_range, int date_time = time, string timezone = syminfo.timezone) =>
    int start_time_hour = na
    int start_time_minute = na
    if str.length(time_range) == 11
        // Format: hh:mm-hh:mm
        start_time_hour := math.floor(str.tonumber(str.substring(time_range, 0, 2)))
        start_time_minute := math.floor(str.tonumber(str.substring(time_range, 3, 5)))
    else if str.length(time_range) == 9
        // Format: hhmm-hhmm
        start_time_hour := math.floor(str.tonumber(str.substring(time_range, 0, 2)))
        start_time_minute := math.floor(str.tonumber(str.substring(time_range, 2, 4)))
    timestamp(timezone, year(date_time, timezone), month(date_time, timezone), dayofmonth(date_time, timezone), start_time_hour, start_time_minute, 0)

p_comm_time_range_to_end_unix_time(string time_range, int date_time = time, string timezone = syminfo.timezone) =>
    int end_time_hour = na
    int end_time_minute = na
    if str.length(time_range) == 11
        end_time_hour := math.floor(str.tonumber(str.substring(time_range, 6, 8)))
        end_time_minute := math.floor(str.tonumber(str.substring(time_range, 9, 11)))
    else if str.length(time_range) == 9
        end_time_hour := math.floor(str.tonumber(str.substring(time_range, 5, 7)))
        end_time_minute := math.floor(str.tonumber(str.substring(time_range, 7, 9)))
    timestamp(timezone, year(date_time, timezone), month(date_time, timezone), dayofmonth(date_time, timezone), end_time_hour, end_time_minute, 0)

p_comm_timeframe_to_seconds(simple string tf) =>
    float seconds = 0
    tf_lower = str.lower(tf)
    value = str.tonumber(str.substring(tf_lower, 0, str.length(tf_lower) - 1))
    if str.endswith(tf_lower, 's')
        seconds := value
    else if str.endswith(tf_lower, 'd')
        seconds := value * 86400
    else if str.endswith(tf_lower, 'w')
        seconds := value * 604800
    else if str.endswith(tf_lower, 'm')
        seconds := value * 2592000
    else
        seconds := str.tonumber(tf_lower) * 60
    seconds

p_custom_sources() =>
    [open, high, low, close, volume]

//#endregion -----------------------------------------------------------------


//#region -------------------------------------------------- Ta Dependence


//#endregion -------------------------------------------------------------


//#region -------------------------------------------------- Constants

// Input Groups
string P_GP_1      =      ""

//#endregion ---------------------------------------------------------


//#region -------------------------------------------------- Inputs

// Default
int p_inp_1        =      input.int(defval=20, title="Fast EMA Length", group=P_GP_1)
int p_inp_2        =      input.int(defval=50, title="Slow EMA Length", group=P_GP_1)
float p_inp_3      =      input.float(defval=1.3, title="Take Profit Price Multiplier", group=P_GP_1, step=0.01)
float p_inp_4      =      input.float(defval=0.95, title="Stop Loss Price Multiplier", group=P_GP_1, step=0.01)


//#endregion -------------------------------------------------------


//#region -------------------------------------------------- Price Data



//#endregion -----------------------------------------------------------


//#region -------------------------------------------------- Indicators

p_ind_1      =      ta.ema(close, p_inp_1) // Fast EMA
p_ind_2      =      ta.ema(close, p_inp_2) // Slow EMA


//#endregion -----------------------------------------------------------


//#region -------------------------------------------------- Conditions

p_cond_1      =      (ta.crossover(p_ind_1, p_ind_2))


//#endregion -----------------------------------------------------------


//#region -------------------------------------------------- Strategy

// Strategy Order Variables
string p_st_name_1                       =      "Entry"
string p_st_name_2                       =      "Exit"
var float p_st_name_2_tp                 =      na
var bool p_st_name_2_tp_can_drawing      =      true
var float p_st_name_2_sl                 =      na
var bool p_st_name_2_sl_can_drawing      =      true

// Strategy Global
open_trades_number = strategy.opentrades
pre_bar_open_trades_number = na(open_trades_number[1]) ? 0 : open_trades_number[1]
var p_entry_order_id = 1
p_can_place_entry_order() =>
    strategy.equity > 0
get_entry_id_name(int current_order_id, string name) =>
    "[" + str.tostring(current_order_id) + "] " + name
is_entry_order(string order_id, string name) =>
    str.startswith(order_id, "[") and str.endswith(order_id, "] " + name)
get_open_trades_entry_ids() =>
    int p_open_trades_count = strategy.opentrades
    string[] p_entry_ids = array.new_string(0, "")
    if p_open_trades_count > 0
        for i = 0 to p_open_trades_count - 1
            array.push(p_entry_ids, strategy.opentrades.entry_id(i))
    p_entry_ids

// Entry (Entry)
if p_cond_1 and p_can_place_entry_order()
    p_st_name_1_id = get_entry_id_name(p_entry_order_id, p_st_name_1)
    p_entry_order_id := p_entry_order_id + 1
    string entry_message = ""
    strategy.entry(id=p_st_name_1_id, direction=strategy.long, alert_message=entry_message, comment=p_st_name_1_id)
    
    // TP/SL Exit (Exit)
    float p_st_name_2_limit = close * p_inp_3
    if p_st_name_2_tp_can_drawing
        p_st_name_2_tp_can_drawing := false
        p_st_name_2_tp := p_st_name_2_limit
    float p_st_name_2_stop = close * p_inp_4
    if p_st_name_2_sl_can_drawing
        p_st_name_2_sl_can_drawing := false
        p_st_name_2_sl := p_st_name_2_stop
    string p_st_name_2_alert_message = ""
    strategy.exit(id=p_st_name_1_id + "_0", from_entry=p_st_name_1_id, qty_percent=100, limit=p_st_name_2_limit, stop=p_st_name_2_stop, comment_profit=p_st_name_2 + " - TP", comment_loss=p_st_name_2 + " - SL", alert_message=p_st_name_2_alert_message)
    

if high >= p_st_name_2_tp or (pre_bar_open_trades_number > 0 and open_trades_number == 0)
    p_st_name_2_tp_can_drawing := true
    p_st_name_2_sl_can_drawing := true
    p_st_name_2_tp := na
    p_st_name_2_sl := na
plot(p_st_name_2_tp, title="Exit - TP", color=color.rgb(0, 150, 136, 0), linewidth=1, style = plot.style_circles)
if low <= p_st_name_2_sl or (pre_bar_open_trades_number > 0 and open_trades_number == 0)
    p_st_name_2_sl_can_drawing := true
    p_st_name_2_tp_can_drawing := true
    p_st_name_2_sl := na
    p_st_name_2_tp := na
plot(p_st_name_2_sl, title="Exit - SL", color=color.rgb(244, 67, 54, 0), linewidth=1, style = plot.style_circles)
//#endregion ---------------------------------------------------------


//#region -------------------------------------------------- Indicator Plots

// Fast EMA
plot(p_ind_1, "Fast EMA", color.rgb(33, 150, 243, 0), 1)

// Slow EMA
plot(p_ind_2, "Slow EMA", color.rgb(255, 82, 82, 0), 1)

//#endregion ----------------------------------------------------------------


//#region -------------------------------------------------- Custom Plots

//#endregion -------------------------------------------------------------


//#region -------------------------------------------------- Alert

//#endregion ------------------------------------------------------


```

> Detail

https://www.fmz.com/strategy/474636

> Last Modified

2024-12-11 11:23:54
