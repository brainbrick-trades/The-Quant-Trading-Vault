
> Name

Flexible-Long-Short-Trading-Strategy-Based-on-Keltner-Channels

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/143421f9039a37868d9.png)


#### Overview
This is a flexible trading strategy based on Keltner Channels, supporting both long and short trading by monitoring price breakouts of the channel's upper and lower bands. The strategy's core lies in using Moving Averages (MA) to construct price channels and combining Average True Range (ATR) to dynamically adjust channel width, maintaining strategy adaptability across different market conditions.

#### Strategy Principles
The strategy is based on the following core principles:
1. Calculating price's central tendency using EMA or SMA to form the channel's middle line
2. Using ATR, TR, or Range to calculate volatility for constructing upper and lower bands
3. Triggering long signals when price breaks above the upper band, and short signals when breaking below the lower band
4. Implementing stop-entry orders for both entry and exit to improve trade execution reliability
5. Supporting flexible trading modes: long-only, short-only, or bidirectional trading

#### Strategy Advantages
1. High Adaptability - Dynamically adjusts channel width through ATR to adapt to different market volatility environments
2. Comprehensive Risk Control - Uses stop-entry orders for trading to effectively manage risk
3. Operational Flexibility - Supports multiple trading modes, adjustable based on market characteristics and trading preferences
4. Proven Effectiveness - Performs well in cryptocurrency and stock markets, especially in high-volatility markets
5. Clear Visualization - Provides intuitive display of trading signals and position status

#### Strategy Risks
1. Choppy Market Risk - May generate frequent false breakout signals in ranging markets
2. Slippage Risk - Stop-entry orders may face significant slippage in markets with insufficient liquidity
3. Trend Reversal Risk - May suffer larger losses during sudden trend reversals
4. Parameter Sensitivity - Strategy performance is significantly influenced by channel parameter selection

#### Strategy Optimization Directions
1. Introduce Trend Filters - Add trend identification indicators to reduce false breakout signals
2. Dynamic Parameter Optimization - Adjust channel parameters dynamically based on market volatility conditions
3. Improve Stop-Loss Mechanism - Add trailing stop functionality for better profit protection
4. Add Volume Confirmation - Incorporate volume indicators to improve signal reliability
5. Optimize Position Management - Introduce dynamic position sizing for better risk control

#### Summary
This strategy is a well-designed, logically clear trading system that effectively captures market opportunities through flexible use of Keltner Channels and various technical indicators. The strategy's high customizability makes it suitable for traders with different risk preferences. Through continuous optimization and improvement, this strategy has the potential to maintain stable performance across various market conditions.




> Source (PineScript)

``` pinescript
/*backtest
start: 2022-02-11 00:00:00
end: 2025-02-08 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy(title = "Jaakko's Keltner Strategy", overlay = true, initial_capital = 10000, default_qty_type = strategy.percent_of_equity, default_qty_value = 100)

// ──────────────────────────────────────────────────────────────────────────────
// ─── USER INPUTS ─────────────────────────────────────────────────────────────
// ──────────────────────────────────────────────────────────────────────────────
length      = input.int(20,     minval=1,  title="Keltner MA Length")
mult        = input.float(2.0,             title="Multiplier")
src         = input(close,                 title="Keltner Source")
useEma      = input.bool(true,             title="Use Exponential MA")
BandsStyle  = input.string(title = "Bands Style", defval  = "Average True Range", options = ["Average True Range", "True Range", "Range"])
atrLength   = input.int(10,                title="ATR Length")

// Choose which side(s) to trade
tradeMode = input.string(title   = "Trade Mode", defval  = "Long Only", options = ["Long Only", "Short Only", "Both"])

// ──────────────────────────────────────────────────────────────────────────────
// ─── KELTNER MA & BANDS ───────────────────────────────────────────────────────
// ──────────────────────────────────────────────────────────────────────────────
f_ma(source, length, emaMode) =>
    maSma = ta.sma(source, length)
    maEma = ta.ema(source, length)
    emaMode ? maEma : maSma

ma    = f_ma(src, length, useEma)
rangeMa = BandsStyle == "True Range" ? ta.tr(true) : BandsStyle == "Average True Range" ? ta.atr(atrLength) : ta.rma(high - low, length)

upper = ma + rangeMa * mult
lower = ma - rangeMa * mult

// ──────────────────────────────────────────────────────────────────────────────
// ─── CROSS CONDITIONS ─────────────────────────────────────────────────────────
// ──────────────────────────────────────────────────────────────────────────────
crossUpper = ta.crossover(src, upper) // potential long signal
crossLower = ta.crossunder(src, lower) // potential short signal

// ──────────────────────────────────────────────────────────────────────────────
// ─── PRICE LEVELS FOR STOP ENTRY (LONG) & STOP ENTRY (SHORT) ─────────────────
// ──────────────────────────────────────────────────────────────────────────────
bprice = 0.0
bprice := crossUpper ? high + syminfo.mintick : nz(bprice[1])

sprice = 0.0
sprice := crossLower ? low - syminfo.mintick : nz(sprice[1])

// ──────────────────────────────────────────────────────────────────────────────
// ─── BOOLEAN FLAGS FOR PENDING LONG/SHORT ─────────────────────────────────────
// ──────────────────────────────────────────────────────────────────────────────
crossBcond = false
crossBcond := crossUpper ? true : crossBcond[1]

crossScond = false
crossScond := crossLower ? true : crossScond[1]

// Cancel logic for unfilled orders (same as original)
cancelBcond = crossBcond and (src < ma or high >= bprice)
cancelScond = crossScond and (src > ma or low <= sprice)

// ──────────────────────────────────────────────────────────────────────────────
// ─── LONG SIDE ────────────────────────────────────────────────────────────────
// ──────────────────────────────────────────────────────────────────────────────
if (tradeMode == "Long Only" or tradeMode == "Both")  // Only run if mode is long or both
    // Cancel unfilled long if invalid
    if cancelBcond
        strategy.cancel("KltChLE")

    // Place long entry
    if crossUpper
        strategy.entry("KltChLE", strategy.long, stop=bprice, comment="Long Entry")

    // If we are also using "Both," we rely on short side to flatten the long.
    // But if "Long Only," we can exit on crossLower or do nothing.
    // Let's do a "stop exit" if in "Long Only" (like the improved version).
    if tradeMode == "Long Only"
        // Cancel unfilled exit
        if cancelScond
            strategy.cancel("KltChLX")

        // Place exit if crossLower
        if crossLower
            strategy.exit("KltChLX", from_entry="KltChLE", stop=sprice, comment="Long Exit")

// ──────────────────────────────────────────────────────────────────────────────
// ─── SHORT SIDE ───────────────────────────────────────────────────────────────
// ──────────────────────────────────────────────────────────────────────────────
if (tradeMode == "Short Only" or tradeMode == "Both") // Only run if mode is short or both
    // Cancel unfilled short if invalid
    if cancelScond
        strategy.cancel("KltChSE")

    // Place short entry
    if crossLower
        strategy.entry("KltChSE", strategy.short, stop=sprice, comment="Short Entry")

    // If "Short Only," we might do a symmetrical exit approach for crossUpper
    // Or if "Both," going long automatically flattens the short in a no-hedge account.
    // Let's replicate "stop exit" for short side if "Short Only" is chosen:
    if tradeMode == "Short Only"
        // Cancel unfilled exit
        if cancelBcond
            strategy.cancel("KltChSX")

        // Place exit if crossUpper
        if crossUpper
            strategy.exit("KltChSX", from_entry="KltChSE", stop=bprice, comment="Short Exit")

// ──────────────────────────────────────────────────────────────────────────────
// ─── OPTIONAL VISUALS ─────────────────────────────────────────────────────────
// ──────────────────────────────────────────────────────────────────────────────
barcolor(strategy.position_size > 0 ? color.green : strategy.position_size < 0 ? color.red : na)

plotshape(    strategy.position_size > 0 and strategy.position_size[1] <= 0, title     = "BUY",  text      = '?',  style     = shape.labelup,    location  = location.belowbar,     color     = color.green,     textcolor = color.white,      size      = size.small)

plotshape(    strategy.position_size <= 0 and strategy.position_size[1] > 0,     title     = "SELL",     text      = '☄️',     style     = shape.labeldown,     location  = location.abovebar,     color     = color.red,       textcolor = color.white,     size      = size.small)

plotshape(crossLower, style=shape.triangledown, color=color.red, location=location.abovebar, title="CrossLower Trigger")

```

> Detail

https://www.fmz.com/strategy/481366

> Last Modified

2025-02-10 15:07:12
