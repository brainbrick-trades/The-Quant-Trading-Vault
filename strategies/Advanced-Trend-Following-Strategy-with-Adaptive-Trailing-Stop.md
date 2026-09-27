
> Name

Advanced-Trend-Following-Strategy-with-Adaptive-Trailing-Stop

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/cc3f655937e4e31865.png) 


#### Overview
This is a trend following strategy based on the Supertrend indicator, combined with an adaptive trailing stop loss mechanism. The strategy primarily uses the Supertrend indicator to identify market trend direction and employs dynamically adjusted trailing stops to manage risk and optimize exit timing. It supports multiple stop loss methods, including percentage-based, ATR-based, and fixed-point stops, allowing flexible adjustment according to different market conditions.

#### Strategy Principles
The core logic of the strategy is based on the following key elements:
1. Uses the Supertrend indicator as the primary basis for trend determination, which combines ATR (Average True Range) to measure market volatility
2. Entry signals are triggered by Supertrend direction changes, supporting long, short, or bilateral trading
3. Stop loss mechanism employs adaptive trailing stops that automatically adjust based on market volatility
4. Trade management system includes position sizing (default 15% of account equity) and time filtering mechanisms

#### Strategy Advantages
1. Strong trend capture capability: Effectively identifies major trends through the Supertrend indicator, reducing false signals
2. Comprehensive risk control: Employs diverse stop loss mechanisms suitable for different market environments
3. High flexibility: Supports configuration of multiple trading directions and stop loss methods
4. Strong adaptability: Trailing stops automatically adjust according to market volatility, enhancing strategy adaptability
5. Complete backtesting system: Built-in time filtering functionality for historical performance analysis

#### Strategy Risks
1. Trend reversal risk: False signals may occur in highly volatile markets
2. Slippage risk: Trailing stop execution may be affected by market liquidity
3. Parameter sensitivity: Supertrend factor and ATR period settings significantly impact strategy performance
4. Market environment dependency: Frequent trading in ranging markets may increase costs

#### Strategy Optimization Directions
1. Signal filtering optimization: Additional technical indicators can be added to filter false signals
2. Position management optimization: Position size can be dynamically adjusted based on market volatility
3. Stop loss mechanism enhancement: More complex stop loss logic can be designed incorporating cost average price
4. Entry timing optimization: Price structure analysis can be added to improve entry accuracy
5. Backtesting system improvement: More statistical indicators can be added to evaluate strategy performance

#### Summary
This is a well-designed trend following strategy with controllable risk. By combining the Supertrend indicator with flexible stop loss mechanisms, the strategy can maintain high profitability while effectively controlling risk. The strategy is highly configurable and suitable for use in different market environments, but requires thorough parameter optimization and backtesting verification. Future improvements can be made by adding more technical analysis tools and risk control measures to further enhance strategy stability and profitability.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-12-18 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("Supertrend Strategy with Adjustable Trailing Stop [Bips]", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=15)

// Inputs
atrPeriod = input(10, "ATR Länge", "Average True Range „wahre durchschnittliche Schwankungsbreite" und stammt aus der technischen Analyse. Die ATR misst die Volatilität eines Instruments oder eines Marktes. Mit ihr kann die Wahrscheinlichkeit für einen Trendwechsel bestimmt werden.", group="Supertrend Settings")
factor = input.float(3.0, "Faktor", step=0.1, group="Supertrend Settings")
tradeDirection = input.string("Long", "Trade Direction", options=["Both", "Long", "Short"], group="Supertrend Settings")
sl_type    = input.string("%", "SL Type", options=["%", "ATR", "Absolute"])
// Parameter für ST nur für einstieg -> Beim Ausstieg fragen ob der bool WWert true ist -> Für weniger und längere Trädes 

sl_perc    = input.float(4.0, "% SL", group="Stop Loss Einstellung")
atr_length = input.int(10, "ATR Length", group="Stop Loss Einstellung")
atr_mult   = input.float(2.0, "ATR Mult", group="Stop Loss Einstellung")
sl_absol   = input.float(10.0, "Absolute SL", group="Stop Loss Einstellung")

//-------------------------//
// BACKTESTING RANGE
fromDay   = input.int(defval=1, title="From Day", minval=1, maxval=31, group="Backtesting Einstellung")
fromMonth = input.int(defval=1, title="From Month", minval=1, maxval=12, group="Backtesting Einstellung")
fromYear  = input.int(defval=2016, title="From Year", minval=1970, group="Backtesting Einstellung")
toDay     = input.int(defval=1, title="To Day", minval=1, maxval=31, group="Backtesting Einstellung")
toMonth   = input.int(defval=1, title="To Month", minval=1, maxval=12, group="Backtesting Einstellung")
toYear    = input.int(defval=2100, title="To Year", minval=1970, group="Backtesting Einstellung")

startDate  = timestamp(fromYear, fromMonth, fromDay, 00, 00)
finishDate = timestamp(toYear, toMonth, toDay, 00, 00)
time_cond  = time >= startDate and time <= finishDate

//-------------------------//
// Supertrend calculation
[_, direction] = ta.supertrend(factor, atrPeriod)

// SL values
sl_val = sl_type == "ATR"      ? atr_mult * ta.atr(atr_length) : 
         sl_type == "Absolute" ? sl_absol : 
         close * sl_perc / 100
         
// Init Variables
var pos         = 0
var float trailing_sl = 0.0

// Signals
long_signal  = nz(pos[1]) !=  1 and high > nz(trailing_sl[1])
short_signal = nz(pos[1]) != -1 and low  < nz(trailing_sl[1]) 

// Calculate SL
trailing_sl := short_signal     ? high + sl_val : 
               long_signal      ? low  - sl_val : 
               nz(pos[1]) ==  1 ? math.max(low  - sl_val, nz(trailing_sl[1])) :  
               nz(pos[1]) == -1 ? math.min(high + sl_val, nz(trailing_sl[1])) : 
               nz(trailing_sl[1])
               
// Position var               
pos := long_signal  ? 1 : short_signal ? -1 : nz(pos[1]) 

// Entry logic
if ta.change(direction) < 0 and time_cond
    if tradeDirection == "Both" or tradeDirection == "Long"
        strategy.entry("Long", strategy.long, stop=trailing_sl)
    else
        strategy.close_all("Stop Short")

if ta.change(direction) > 0 and time_cond
    if tradeDirection == "Both" or tradeDirection == "Short"
        strategy.entry("Short", strategy.short, stop=trailing_sl)
    else
        strategy.close_all("Stop Long")

// Exit logic: Trailing Stop and Supertrend
//if strategy.position_size > 0 and not na(trailing_sl)
    //strategy.exit("SL-Exit Long", from_entry="Long", stop=trailing_sl)

//if strategy.position_size < 0 and not na(trailing_sl)
    //strategy.exit("SL-Exit Short", from_entry="Short", stop=trailing_sl)

// Trailing Stop visualization
plot(trailing_sl, linewidth = 2, color = pos == 1 ? color.green : color.red)
//plot(not na(trailing_sl) ? trailing_sl : na, color=pos == 1 ? color.green : color.red, linewidth=2, title="Trailing Stop")

```

> Detail

https://www.fmz.com/strategy/475591

> Last Modified

2024-12-20 14:12:05
