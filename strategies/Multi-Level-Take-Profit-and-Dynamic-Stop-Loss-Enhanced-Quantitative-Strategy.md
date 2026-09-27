
> Name

Multi-Level-Take-Profit-and-Dynamic-Stop-Loss-Enhanced-Quantitative-Strategy

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d8cd913eb58bcf6d9486.png)
![IMG](https://www.fmz.com/upload/asset/2d85f01cc048e631330a8.png)




#### Overview
This is an enhanced quantitative trading strategy developed based on metrobonez1ty's strategy tester. The strategy's main features include multiple take-profit targets and dynamic stop-loss mechanisms while maintaining flexibility for integration with external indicator signals. It supports up to three profit targets and optionally uses indicator-based stop-loss triggers, filtering trade entries through additional signal confirmation.

#### Strategy Principles
The strategy's core logic revolves around a multi-layered exit mechanism. For entry, the strategy uses longEntry and shortEntry input sources to trigger long and short trading signals. For each trading direction, the strategy sets up three independent take-profit targets (TP1, TP2, TP3), each of which can be dynamically adjusted based on external indicator signals. Additionally, the strategy incorporates a dynamic stop-loss mechanism that can flexibly adjust stop-loss positions according to market conditions. The strategy also implements confluence-based filtering, requiring multiple indicator confirmations to trigger trades.

#### Strategy Advantages
1. Flexible Exit Mechanism: Supports multiple profit target positions, allowing gradual position exits based on market conditions.
2. Dynamic Risk Management: Adjusts stop-loss positions dynamically through external indicator signals, providing smarter risk control.
3. High Customizability: Entry and exit conditions can be customized through external indicators, adapting to different trading styles.
4. Comprehensive Filtering: Reduces the impact of false signals by requiring multiple signal confirmations.

#### Strategy Risks
1. Signal Dependency Risk: The strategy heavily relies on the quality of external indicator signals; inaccurate signals may lead to incorrect trades.
2. Parameter Optimization Risk: Multiple profit targets and stop-loss parameters require careful optimization; over-optimization may lead to overfitting.
3. Market Environment Adaptability Risk: Fixed multiple profit targets may not be flexible enough in different market environments.

#### Strategy Optimization Directions
1. Dynamic Parameter Adjustment: Introduce adaptive mechanisms to automatically adjust profit targets and stop-loss parameters based on market volatility.
2. Signal Quality Assessment: Add quality assessment mechanisms for entry and exit signals to further improve trading accuracy.
3. Position Management Optimization: Set different position allocation ratios for different profit targets.
4. Market Environment Recognition: Add market environment recognition modules to adopt different parameter settings under different market conditions.

#### Summary
The strategy provides a comprehensive trading framework through multiple profit targets and dynamic stop-loss mechanisms. Its strengths lie in its flexibility and customizability, but careful attention must be paid to parameter optimization and market adaptability issues. Through the suggested optimization directions, the strategy can further enhance its stability and adaptability to become a more refined trading system.




> Source (PineScript)

``` pinescript
/*backtest
start: 2025-02-04 00:00:00
end: 2025-02-18 08:00:00
period: 4h
basePeriod: 4h
exchanges: [{"eid":"Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("Enhanced Strategy Tester with multi TP and SL Trigger", overlay=true, margin_long=100, margin_short=100)

// Entry Signals
longEntry = input.source(close, 'Long Entry Trigger', 'long signal source')
shortEntry = input.source(close, 'Short Entry Trigger', 'short signal source')

// Exit Triggers
activateLongExit = input.bool(false, 'Activate Long Exit Signals')
longExit1 = input.source(high, 'Long Exit TP1')
longExit2 = input.source(high, 'Long Exit TP2')
longExit3 = input.source(high, 'Long Exit TP3')

activateShortExit = input.bool(false, 'Activate Short Exit Signals')
shortExit1 = input.source(low, 'Short Exit TP1')
shortExit2 = input.source(low, 'Short Exit TP2')
shortExit3 = input.source(low, 'Short Exit TP3')

// Stop Loss from External Indicator
useSLSignal = input.bool(false, 'Activate SL Signal')
slSignal = input.source(low, 'SL', 'SL Signal Source')

// Long Entry Condition
longCondition = not na(longEntry) and longEntry > 0
if (longCondition and strategy.opentrades == 0)
    strategy.entry('long', strategy.long)
    strategy.exit('exit_long_tp1', 'long', limit=longExit1, comment='TP1 hit')
    strategy.exit('exit_long_tp2', 'long', limit=longExit2, comment='TP2 hit')
    strategy.exit('exit_long_tp3', 'long', limit=longExit3, comment='TP3 hit')
    strategy.exit('exit_long_sl', 'long', stop=useSLSignal ? slSignal : na, comment='SL hit')

// Long Exit Condition
if (activateLongExit)
    if (not na(longExit1) and longExit1 > 0)
        strategy.close('long', comment='TP1 at Exit')
    if (not na(longExit2) and longExit2 > 0)
        strategy.close('long', comment='TP2 at Exit')
    if (not na(longExit3) and longExit3 > 0)
        strategy.close('long', comment='TP3 at Exit')

// Short Entry Condition
shortCondition = not na(shortEntry) and shortEntry > 0
if (shortCondition and strategy.opentrades == 0)
    strategy.entry('short', strategy.short)
    strategy.exit('exit_short_tp1', 'short', limit=shortExit1, comment='TP1 hit')
    strategy.exit('exit_short_tp2', 'short', limit=shortExit2, comment='TP2 hit')
    strategy.exit('exit_short_tp3', 'short', limit=shortExit3, comment='TP3 hit')
    strategy.exit('exit_short_sl', 'short', stop=useSLSignal ? slSignal : na, comment='SL hit')

// Short Exit Condition
if (activateShortExit)
    if (not na(shortExit1) and shortExit1 > 0)
        strategy.close('short', comment='TP1 at Exit')
    if (not na(shortExit2) and shortExit2 > 0)
        strategy.close('short', comment='TP2 at Exit')
    if (not na(shortExit3) and shortExit3 > 0)
        strategy.close('short', comment='TP3 at Exit')

```

> Detail

https://www.fmz.com/strategy/482802

> Last Modified

2025-02-20 14:56:34
