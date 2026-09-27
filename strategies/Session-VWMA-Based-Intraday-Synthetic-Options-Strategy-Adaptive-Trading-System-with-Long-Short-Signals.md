
> Name

Session-VWMA-Based-Intraday-Synthetic-Options-Strategy-Adaptive-Trading-System-with-Long-Short-Signals

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d949cfff0080791834c4.png)
![IMG](https://www.fmz.com/upload/asset/2d8e3dedf323377f6974f.png)





#### Overview
This is an intraday trading strategy based on Volume Weighted Moving Average (VWMA) that implements long-short operations through synthetic options combinations. The core of the strategy is the daily-reset VWMA indicator, generating trading signals based on price position relative to VWMA, with automatic position closure before market close. The strategy incorporates robust risk control mechanisms, including position management and trade frequency limitations.

#### Strategy Principles
The core logic is based on the following points:
1. Using daily-reset VWMA as a dynamic trend indicator
2. Constructing bullish combinations (buy call + sell put) when price breaks above VWMA
3. Constructing bearish combinations (buy put + sell call) when price breaks below VWMA
4. Mandatory position closure at 15:29 (IST)
5. Implementing hasExited variable to control position adding frequency
6. Supporting pyramiding in the direction of breakthrough

#### Strategy Advantages
1. Strong Dynamic Adaptability - Daily VWMA reset ensures indicator reflects current market conditions
2. Balanced Risk-Reward - Synthetic options combinations limit risk while maintaining profit potential
3. Strict Trading Discipline - Clear entry, position adding, and forced exit mechanisms
4. Flexible Position Sizing - Supports percentage-based position management
5. Clear Operational Logic - Simple and intuitive signal generation conditions

#### Strategy Risks
1. Choppy Market Risk - VWMA breakouts may generate frequent false signals in ranging markets
2. Gap Risk - Overnight large price movements may lead to significant losses
3. Options Combination Risk - Synthetic options may have delta neutrality bias
4. Execution Slippage - High-frequency trading may face significant slippage
5. Capital Efficiency - Daily forced closure increases trading costs

#### Strategy Optimization Directions
1. Introduce volatility filters to adjust strategy parameters in high volatility environments
2. Add trend confirmation indicators to reduce losses from false breakouts
3. Optimize options combination structure, such as considering vertical spread strategies
4. Implement adaptive VWMA periods based on market conditions
5. Add more risk control indicators, such as maximum drawdown limits

#### Summary
This is a well-structured and logically sound intraday trading strategy. It captures short-term trends using the VWMA indicator, combined with synthetic options trading, featuring good risk control mechanisms. Strategy optimization potential mainly lies in reducing false signals, improving execution efficiency, and enhancing risk management systems. While it has certain limitations, it is overall a trading system with practical value.




> Source (PineScript)

``` pinescript
/*backtest
start: 2025-02-16 00:00:00
end: 2025-02-23 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Binance","currency":"SOL_USDT"}]
*/

//@version=5
strategy("Session VWMA Synthetic Options Strategy", overlay=true, initial_capital=100000, 
     default_qty_type=strategy.percent_of_equity, default_qty_value=10, pyramiding=10, calc_on_every_tick=true)

//──────────────────────────────
// Session VWMA Inputs
//──────────────────────────────
vwmaLen   = input.int(55, title="VWMA Length", inline="VWMA", group="Session VWMA")
vwmaColor = input.color(color.orange, title="VWMA Color", inline="VWMA", group="Session VWMA", tooltip="VWMA resets at the start of each session (at the opening of the day).")

//──────────────────────────────
// Session VWMA Calculation Function
//──────────────────────────────
day_vwma(_start, s, l) =>
    bs_nd = ta.barssince(_start)
    v_len = math.max(1, bs_nd < l ? bs_nd : l)
    ta.vwma(s, v_len)

//──────────────────────────────
// Determine Session Start
//──────────────────────────────
// newSession becomes true on the first bar of a new day.
newSession = ta.change(time("D")) != 0

//──────────────────────────────
// Compute Session VWMA
//──────────────────────────────
vwmaValue = day_vwma(newSession, close, vwmaLen)
plot(vwmaValue, color=vwmaColor, title="Session VWMA")

//──────────────────────────────
// Define Signal Conditions (only on transition)
//──────────────────────────────
bullCond = low > vwmaValue      // Bullish: candle low above VWMA
bearCond = high < vwmaValue     // Bearish: candle high below VWMA

// Trigger signal only on the bar where the condition first becomes true
bullSignal = bullCond and not bullCond[1]
bearSignal = bearCond and not bearCond[1]

//──────────────────────────────
// **Exit Condition at 15:29 IST**
//──────────────────────────────
sessionEnd = hour == 15 and minute == 29

// Exit all positions at 15:29 IST
if sessionEnd
    strategy.close_all(comment="Closing all positions at session end")

//──────────────────────────────
// **Trade Control Logic**
//──────────────────────────────
var bool hasExited = true  // Track if an exit has occurred since last entry

// Reset exit flag when a position is exited
if strategy.position_size == 0
    hasExited := true

//──────────────────────────────
// **Position Management: Entry & Exit**
//──────────────────────────────
if newSession
    hasExited := true  // Allow first trade of the day

// On a bullish signal: 
//   • If currently short, close the short position and then enter long
//   • Otherwise, add to any existing long position **only if an exit happened before**
if bullSignal and (hasExited or newSession)
    if strategy.position_size < 0
        strategy.close("Short", comment="Exit Short on Bull Signal")
        strategy.entry("Long", strategy.long, comment="Enter Long: Buy Call & Sell Put at ATM")
    else
        strategy.entry("Long", strategy.long, comment="Add Long: Buy Call & Sell Put at ATM")
    hasExited := false  // Reset exit flag

// On a bearish signal: 
//   • If currently long, close the long position and then enter short
//   • Otherwise, add to any existing short position **only if an exit happened before**
if bearSignal and (hasExited or newSession)
    if strategy.position_size > 0
        strategy.close("Long", comment="Exit Long on Bear Signal")
        strategy.entry("Short", strategy.short, comment="Enter Short: Buy Put & Sell Call at ATM")
    else
        strategy.entry("Short", strategy.short, comment="Add Short: Buy Put & Sell Call at ATM")
    hasExited := false  // Reset exit flag

//──────────────────────────────
// **Updated Alert Conditions**
//──────────────────────────────
// Alerts for valid trade entries
alertcondition(bullSignal and (hasExited or newSession), 
     title="Long Entry Alert", 
     message="Bullish signal: BUY CALL & SELL PUT at ATM. Entry allowed.")

alertcondition(bearSignal and (hasExited or newSession), 
     title="Short Entry Alert", 
     message="Bearish signal: BUY PUT & SELL CALL at ATM. Entry allowed.")


```

> Detail

https://www.fmz.com/strategy/483520

> Last Modified

2025-02-27 16:46:17
