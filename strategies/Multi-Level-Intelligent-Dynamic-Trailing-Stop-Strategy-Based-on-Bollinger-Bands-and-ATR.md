
> Name

Multi-Level-Intelligent-Dynamic-Trailing-Stop-Strategy-Based-on-Bollinger-Bands-and-ATR

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/d09af77c51a3ac030e.png)


#### Overview
This strategy is an intelligent trading system based on Bollinger Bands and ATR indicators, incorporating multi-level profit-taking and stop-loss mechanisms. The strategy primarily enters long positions by identifying reversal signals near the lower Bollinger Band and manages risk using dynamic trailing stops. The system is designed with a 20% profit target and 12% stop-loss level, while incorporating ATR-based dynamic trailing stops to protect profits while allowing trends sufficient room to develop.

#### Strategy Principles
The core logic includes several key components:
1. Entry conditions: Requires a green candle following a red candle touching the lower Bollinger Band, typically indicating a potential reversal signal.
2. Moving average selection: Supports multiple types (SMA, EMA, SMMA, WMA, VWMA), with default 20-period SMA.
3. Bollinger Bands parameters: Uses 1.5 standard deviations for bandwidth, more conservative than traditional 2 standard deviations.
4. Profit-taking mechanism: Sets initial 20% profit target.
5. Stop-loss mechanism: Implements 12% fixed stop-loss to protect capital.
6. Dynamic trailing stop:
   - Activates ATR trailing stop after reaching profit target
   - Initiates ATR dynamic trailing stop after touching upper Bollinger Band
   - Uses ATR multiplier to dynamically adjust trailing stop distance

#### Strategy Advantages
1. Multi-level risk control:
   - Fixed stop-loss protects principal
   - Dynamic trailing stop locks in profits
   - Upper Bollinger Band triggered dynamic stop provides additional protection
2. Flexible moving average selection allows adaptation to different market conditions
3. ATR-based dynamic trailing stop automatically adjusts based on market volatility, preventing premature exits
4. Entry signals combine price patterns and technical indicators, improving signal reliability
5. Supports position management and transaction cost settings, closer to real trading conditions

#### Strategy Risks
1. Rapid oscillating markets may lead to frequent trading, increasing transaction costs
2. 12% fixed stop-loss might be too tight in high-volatility markets
3. Bollinger Bands signals may generate false signals in trending markets
4. ATR trailing stop may result in larger drawdowns during severe volatility
Mitigation measures:
- Recommended use on larger timeframes (30min-1hour)
- Adjust stop-loss percentage based on specific instrument characteristics
- Consider adding trend filters to reduce false signals
- Dynamically adjust ATR multiplier for different market environments

#### Strategy Optimization Directions
1. Entry optimization:
- Add volume confirmation mechanism
- Incorporate trend strength indicators for signal filtering
- Consider adding momentum indicators for confirmation

2. Stop-loss optimization:
- Convert fixed stop-loss to ATR-based dynamic stop
- Develop adaptive stop-loss algorithm
- Dynamically adjust stop distance based on volatility

3. Moving average optimization:
- Test different period combinations
- Research adaptive period methods
- Consider using price action instead of moving averages

4. Position management optimization:
- Develop volatility-based position sizing system
- Implement scaled entry and exit mechanisms
- Add risk exposure control

#### Summary
The strategy constructs a multi-level trading system using Bollinger Bands and ATR indicators, employing dynamic management methods for entry, stop-loss, and profit-taking. Its strengths lie in its comprehensive risk control system and ability to adapt to market volatility. Through the suggested optimization directions, the strategy has significant room for improvement. It is particularly suitable for use on larger timeframes and can help investors holding quality assets optimize their entry and exit timing.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-12-09 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Demo GPT - Bollinger Bands Strategy with Tightened Trailing Stops", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=100, commission_value=0.1, slippage=3)

// Input settings
length = input.int(20, minval=1)
maType = input.string("SMA", "Basis MA Type", options=["SMA", "EMA", "SMMA (RMA)", "WMA", "VWMA"])
src = input(close, title="Source")
mult = 1.5 // Standard deviation multiplier set to 1.5
offset = input.int(0, "Offset", minval=-500, maxval=500)
atrMultiplier = input.float(1.0, title="ATR Multiplier for Trailing Stop", minval=0.1) // ATR multiplier for trailing stop

// Time range filters
start_date = input(timestamp("2018-01-01 00:00"), title="Start Date")
end_date = input(timestamp("2069-12-31 23:59"), title="End Date")
in_date_range = true

// Moving average function
ma(source, length, _type) =>
    switch _type
        "SMA" => ta.sma(source, length)
        "EMA" => ta.ema(source, length)
        "SMMA (RMA)" => ta.rma(source, length)
        "WMA" => ta.wma(source, length)
        "VWMA" => ta.vwma(source, length)

// Calculate Bollinger Bands
basis = ma(src, length, maType)
dev = mult * ta.stdev(src, length)
upper = basis + dev
lower = basis - dev

// ATR Calculation
atr = ta.atr(length) // Use ATR for trailing stop adjustments

// Plotting
plot(basis, "Basis", color=#2962FF, offset=offset)
p1 = plot(upper, "Upper", color=#F23645, offset=offset)
p2 = plot(lower, "Lower", color=#089981, offset=offset)
fill(p1, p2, title="Background", color=color.rgb(33, 150, 243, 95))

// Candle color detection
isGreen = close > open
isRed = close < open

// Flags for entry and exit conditions
var bool redTouchedLower = false
var float targetPrice = na
var float stopLossPrice = na
var float trailingStopPrice = na

if in_date_range
    // Entry Logic: First green candle after a red candle touches the lower band
    if close < lower and isRed
        redTouchedLower := true
    if redTouchedLower and isGreen
        strategy.entry("Long", strategy.long)
        targetPrice := close * 1.2       // Set the target price to 20% above the entry price
        stopLossPrice := close * 0.88   // Set the stop loss to 12% below the entry price
        trailingStopPrice := na         // Reset trailing stop on entry
        redTouchedLower := false

    // Exit Logic: Trailing stop after 20% price increase
    if strategy.position_size > 0 and not na(targetPrice) and close >= targetPrice
        if na(trailingStopPrice)
            trailingStopPrice := close - atr * atrMultiplier // Initialize trailing stop using ATR
        trailingStopPrice := math.max(trailingStopPrice, close - atr * atrMultiplier) // Tighten dynamically based on ATR

    // Exit if the price falls below the trailing stop after 20% increase
    if strategy.position_size > 0 and not na(trailingStopPrice) and close < trailingStopPrice
        strategy.close("Long", comment="Trailing Stop After 20% Increase")
        targetPrice := na // Reset the target price
        stopLossPrice := na // Reset the stop loss price
        trailingStopPrice := na // Reset trailing stop

    // Stop Loss: Exit if the price drops 12% below the entry price
    if strategy.position_size > 0 and not na(stopLossPrice) and close <= stopLossPrice
        strategy.close("Long", comment="Stop Loss Triggered")
        targetPrice := na // Reset the target price
        stopLossPrice := na // Reset the stop loss price
        trailingStopPrice := na // Reset trailing stop

    // Trailing Stop: Activate after touching the upper band
    if strategy.position_size > 0 and close >= upper and isGreen
        if na(trailingStopPrice)
            trailingStopPrice := close - atr * atrMultiplier // Initialize trailing stop using ATR
        trailingStopPrice := math.max(trailingStopPrice, close - atr * atrMultiplier) // Tighten dynamically based on ATR

    // Exit if the price falls below the trailing stop
    if strategy.position_size > 0 and not na(trailingStopPrice) and close < trailingStopPrice
        strategy.close("Long", comment="Trailing Stop Triggered")
        trailingStopPrice := na // Reset trailing stop
        targetPrice := na // Reset the target price
        stopLossPrice := na // Reset the stop loss price

```

> Detail

https://www.fmz.com/strategy/474668

> Last Modified

2024-12-11 14:52:24
