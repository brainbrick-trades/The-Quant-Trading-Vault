
> Name

Momentum-Trend-Following-DMIADX-Crossover-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/e3875a107ce4773d34.png)


#### Overview
This strategy combines the DMI (Directional Movement Index) and ADX (Average Directional Index) indicators to identify strong market trends and capture trading opportunities. The strategy uses DMI's +DI and -DI line crossovers to determine trend direction while utilizing the ADX indicator to measure trend strength, only entering trades when trends are clearly established. This is a complete trend following trading system that includes entry signals and risk management features like stop-loss and take-profit levels.

#### Strategy Principles
The core logic includes several key elements:
1. Uses DMI indicator's +DI and -DI lines to judge trend direction, generating long signals when +DI crosses above -DI and short signals when +DI crosses below -DI
2. Uses ADX indicator to assess trend strength, with a default threshold of 25, only allowing trades when ADX exceeds the threshold to avoid false signals in choppy markets
3. Employs percentage-based stop-loss and take-profit levels for risk control, with default settings of 1% stop-loss and 2% take-profit from entry price
4. Strategy parameters are adjustable, including DMI period, ADX period and smoothing parameters, ADX threshold, and stop-loss/take-profit percentages

#### Strategy Advantages
1. Combines trend direction and strength assessment for more reliable trading signals
2. Only trades in strong trends, avoiding frequent trading in choppy markets
3. Complete risk control system with clear stop-loss and take-profit levels
4. Flexible parameters that can adapt to different market conditions
5. Clear and simple strategy logic that's easy to understand and execute
6. Suitable for medium to long-term trend following and short-term trading

#### Strategy Risks
1. Potential for significant drawdowns during trend reversals
2. DMI and ADX are lagging indicators, signals may be relatively delayed
3. Improper parameter settings can affect strategy performance
4. Consecutive stops possible in choppy markets
5. Need to consider impact of trading costs on strategy returns

Mitigation measures:
- Optimize parameter settings to balance signal lag and accuracy
- Combine with other technical indicators for signal confirmation
- Implement proper position sizing
- Regular backtesting to verify strategy effectiveness

#### Strategy Optimization Directions
1. Signal Optimization:
- Add trend confirmation indicators like moving averages
- Optimize dynamic adjustment mechanism for ADX threshold
- Consider incorporating volume indicators for auxiliary judgment

2. Risk Control Optimization:
- Introduce dynamic stop-loss mechanisms
- Optimize position management methods
- Add maximum drawdown controls

3. Parameter Optimization:
- Develop adaptive parameter adjustment mechanisms
- Set parameter combinations for different market environments
- Optimize stop-loss and take-profit ratio settings

#### Summary
The DMI+ADX crossover strategy is a classic trend following strategy that combines directional and strength indicators to find trading opportunities in strong trend markets. The strategy features clear logic, comprehensive risk control, and good practicality and scalability. Through continuous optimization and improvement, the strategy can better adapt to different market environments and enhance trading performance.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-19 00:00:00
end: 2024-10-25 08:00:00
period: 4h
basePeriod: 4h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("DMI + ADX Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=250)

// Nastavenie parametrov
adxLength = input.int(14, title="ADX Length")
adxSmoothing = input.int(14, title="ADX Smoothing")
dmiLength = input.int(14, title="DMI Length")
adxThreshold = input.float(25.0, title="ADX Threshold")
stopLossPerc = input.float(1.0, title="Stop Loss (%)")
takeProfitPerc = input.float(2.0, title="Take Profit (%)")

// Výpočet DMI a ADX pomocou ta.dmi
[plusDI, minusDI, adxValue] = ta.dmi(dmiLength, adxSmoothing)

// Nákupné podmienky
longCondition = ta.crossover(plusDI, minusDI) and adxValue > adxThreshold
if (longCondition)
    strategy.entry("Long", strategy.long)

// Predajné podmienky
shortCondition = ta.crossunder(plusDI, minusDI) and adxValue > adxThreshold
if (shortCondition)
    strategy.entry("Short", strategy.short)

// Definovanie Stop a Limit pre Long pozíciu
longStop = strategy.position_avg_price * (1 - stopLossPerc / 100)
longLimit = strategy.position_avg_price * (1 + takeProfitPerc / 100)
if (strategy.position_size > 0)
    strategy.exit("Long Exit", "Long", stop=longStop, limit=longLimit)

// Definovanie Stop a Limit pre Short pozíciu
shortStop = strategy.position_avg_price * (1 + stopLossPerc / 100)
shortLimit = strategy.position_avg_price * (1 - takeProfitPerc / 100)
if (strategy.position_size < 0)
    strategy.exit("Short Exit", "Short", stop=shortStop, limit=shortLimit)

// Vizualizácia indikátorov na grafe
plot(adxValue, title="ADX", color=color.blue)
hline(adxThreshold, "ADX Threshold", color=color.gray)
plot(plusDI, title="+DI", color=color.green)
plot(minusDI, title="-DI", color=color.red)

```

> Detail

https://www.fmz.com/strategy/482424

> Last Modified

2025-02-18 13:47:09
