
> Name

Multi-MA-Trend-Strength-Capture-with-Momentum-Profit-Taking-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/8922768d9efab5863f.png)


#### Overview
This strategy is a trend-following system based on multiple moving averages, combining trend strength confirmation and volatility capture mechanisms. It utilizes a triple moving average system of 5, 25, and 75 periods as its core, filters strong trends through the ADX indicator, and integrates a rapid volatility monitoring system for timely profit-taking. This multi-layered trading mechanism effectively identifies market trends and executes trades at appropriate times.

#### Strategy Principle
The strategy operates on three core mechanisms:
1. Multiple MA System: Uses 5SMA and 25SMA crossover as primary entry signals, with 75SMA as a trend filter to ensure trade direction aligns with the main trend.
2. Trend Strength Confirmation: Utilizes ADX indicator, requiring ADX values above 20 to ensure trading only in clear trends.
3. Volatility Monitoring System: Monitors price movement magnitude (0.6% threshold) to lock in profits during intense volatility.

Specific trading rules:
- Long Entry: 5SMA crosses above 25SMA, price above 75SMA, ADX>20
- Short Entry: 5SMA crosses below 25SMA, price below 75SMA, ADX>20
- Exit Conditions: Sudden moves exceeding 0.6% or opposing entry signals

#### Strategy Advantages
1. Multiple Confirmation Mechanism: Significantly reduces false breakout risks through multiple MAs and ADX
2. Trend Adaptability: Self-adapts to different market environments, suitable for medium to long-term trend trading
3. Comprehensive Risk Control: Timely profit-taking during market volatility through monitoring system
4. Clear Logic: Strategy logic is intuitive, easy to understand and maintain
5. Parameter Adjustability: Key parameters like MA periods and ADX threshold can be adjusted based on market characteristics

#### Strategy Risks
1. Choppy Market Risk: May generate frequent false signals in ranging markets
2. Lag Risk: MA system has inherent lag, potentially missing optimal entry points
3. Volatility Detection Sensitivity: 0.6% threshold needs optimization for different markets
4. Trend Reversal Risk: May face significant drawdown during sudden trend reversals
5. Parameter Dependency: Strategy performance heavily influenced by parameter selection

#### Strategy Optimization Directions
1. Introduce Adaptive Parameters:
   - Dynamically adjust MA periods based on market volatility
   - Use ATR for dynamic volatility detection threshold

2. Enhanced Trend Confirmation:
   - Integrate additional trend indicators like MACD
   - Add volume confirmation mechanism

3. Optimize Profit/Loss Taking:
   - Implement dynamic stop-loss positioning
   - Optimize position management based on risk-reward ratio

4. Market Environment Classification:
   - Add market environment identification mechanism
   - Apply different parameters for different market states

#### Summary
The strategy builds a complete trading system through multiple moving averages, trend strength confirmation, and volatility monitoring dimensions. Its core advantages lie in its multi-level confirmation mechanism and flexible risk control system. Through the provided optimization suggestions, the strategy can further enhance its adaptability and stability. In practical application, traders are advised to optimize parameters according to specific market characteristics and combine with reasonable money management strategies.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-10-01 00:00:00
end: 2024-10-31 23:59:59
period: 2h
basePeriod: 2h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("5SMA-25SMA Crossover Strategy with ADX Filter and Sudden Move Profit Taking", overlay=true)

// パラメータのSettings
sma5 = ta.sma(close, 5)
sma25 = ta.sma(close, 25)
sma75 = ta.sma(close, 75)

// ADXのCalculate
length = 14
tr = ta.tr(true)
plus_dm = ta.rma(math.max(ta.change(high), 0), length)
minus_dm = ta.rma(math.max(-ta.change(low), 0), length)
tr_sum = ta.rma(tr, length)
plus_di = 100 * plus_dm / tr_sum
minus_di = 100 * minus_dm / tr_sum
dx = 100 * math.abs(plus_di - minus_di) / (plus_di + minus_di)
adx = ta.rma(dx, length)

// ロングとショートのエントリーcondition
longCondition = ta.crossover(sma5, sma25) and close > sma75 and adx > 20
shortCondition = ta.crossunder(sma5, sma25) and close < sma75 and adx > 20

// SuddenなFluctuationをDetectionするcondition(ここでは,agoのローソクFootにCompareべて0.6%AboveのPrice movementきがあったCase)
suddenMove = math.abs(ta.change(close)) > close[1] * 0.006

// ポジションManage
if (longCondition)
    strategy.entry("Long", strategy.long)
if (shortCondition)
    strategy.entry("Short", strategy.short)

// SuddenなFluctuationがあったCase,ポジションをProfit Realization(クローズ)する
if (strategy.position_size > 0 and suddenMove)
    strategy.close("Long")
if (strategy.position_size < 0 and suddenMove)
    strategy.close("Short")

// エグジットcondition
if (strategy.position_size > 0 and shortCondition)
    strategy.close("Long")
if (strategy.position_size < 0 and longCondition)
    strategy.close("Short")

// SMAとADXのプロット
plot(sma5, color=color.blue, title="5SMA")
plot(sma25, color=color.red, title="25SMA")
plot(sma75, color=color.green, title="75SMA")
plot(adx, color=color.orange, title="ADX")
hline(20, "ADX Threshold", color=color.gray, linestyle=hline.style_dotted)

```

> Detail

https://www.fmz.com/strategy/471725

> Last Modified

2024-11-12 17:18:26
