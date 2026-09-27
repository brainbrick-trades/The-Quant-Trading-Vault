
> Name

Dual-Period-RSI-Trend-Momentum-Strategy-with-Pyramiding-Position-Management-System

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1226f32a7842f5a988b.png)


#### Overview
This strategy is a trend-following trading system based on dual-period RSI (Relative Strength Index) combined with pyramiding position management. The strategy compares RSI indicators of two different periods (14 and 30) to enter trades at trend initiation and adds positions through limit orders during trend continuation, maximizing trend capture. The system includes comprehensive risk control mechanisms, including position management and dynamic exit conditions.

#### Strategy Principle
The strategy employs dual-period RSI crossover signals as trading triggers combined with pyramiding position management. Specifically:
1. Entry signals: Uses 14-period RSI breakthrough of oversold (30) and overbought (70) levels as entry signals
2. Position adding: Implements secondary position adding through limit orders set at 1.5% price deviation after initial entry
3. Exit signals: Uses 30-period RSI as exit indicator, triggering closure when RSI falls from overbought or rebounds from oversold zones
4. Position control: System allows maximum of two positions (pyramiding=2) with independently configurable entry quantities

#### Strategy Advantages
1. Strong trend capture: Better identifies and tracks medium to long-term trends through dual-period RSI coordination
2. Optimized risk-reward ratio: Uses pyramiding strategy to amplify returns after trend confirmation
3. Flexible position management: Adjustable entry and additional position sizes based on market conditions and capital
4. Dynamic stop-loss design: Uses long-period RSI as exit indicator to avoid premature exits
5. Strong parameter adaptability: Key parameters can be optimized for different market characteristics

#### Strategy Risks
1. Choppy market risk: May incur losses from frequent trading in range-bound markets
2. Slippage risk: Additional position orders using limit orders may miss optimal entry timing in volatile markets
3. Capital management risk: Double positions may lead to significant drawdowns
4. Trend reversal risk: RSI indicator's inherent lag may delay stop-loss execution during trend reversals
5. Parameter optimization risk: Over-optimization may lead to poor real-trading performance

#### Strategy Optimization Directions
1. Introduce trend filters: Add moving averages or ADX indicators to improve entry signal reliability
2. Optimize position management: Design dynamic position sizing system based on volatility
3. Enhance stop-loss mechanism: Consider adding trailing stops or ATR-based stop-loss solutions
4. Add market environment filters: Incorporate volatility indicators to adjust strategy parameters in different market conditions
5. Improve position adding logic: Dynamically adjust position addition price deviation based on volatility

#### Summary
The strategy achieves effective trend capture through the combination of dual-period RSI and pyramiding positions. It implements a complete trading system including entry, position adding, stop-loss, and position management elements. Through parameter optimization and risk management improvements, the strategy shows promise for stable performance in actual trading. Traders are advised to thoroughly test and adjust parameters according to specific market characteristics before live implementation.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-12-17 00:00:00
end: 2025-01-16 00:00:00
period: 3h
basePeriod: 3h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT","balance":49999}]
*/

//@version=5
strategy("RSI Top Strategy", overlay=true, pyramiding=2)

qty1 = input( 1 , "Qty first entry", group="Strategy settings")
qty2 = input( 1 , "Qty second entry", group="Strategy settings")
avg1 = input.float( 1.5 , "% averaging ", group="Strategy settings")

overSold = input( 30 , group="open RSI Settings")
overBought = input( 70 , group="open RSI Settings")
rsi1len = input.int(14, minval=1, title="open RSI Length", group="open RSI Settings")

overSold2 = input( 30 , group="close RSI Settings")
overBought2 = input( 70 , group="close RSI Settings")
rsi2len = input.int(30, minval=1, title="close RSI Length", group="close RSI Settings")

price = close
vrsi = ta.rsi(price, rsi1len)
vrsi2 = ta.rsi(price, rsi2len)

sz=strategy.position_size	

co = ta.crossover(vrsi, overSold)
cu = ta.crossunder(vrsi, overBought)
if (not na(vrsi))
	if (co) and not (sz>0)
		strategy.entry("Long", strategy.long, qty = qty1, comment="Long")
		Avgl=close-close*0.01*avg1
		strategy.entry("AvgL", strategy.long, qty = qty2, limit=Avgl, comment="AvgL")
	if (cu) and not (sz<0)
		strategy.entry("Short", strategy.short, qty = qty1, comment="Short")
		Avgs=close+close*0.01*avg1
		strategy.entry("AvgS", strategy.short, qty = qty2, limit=Avgs, comment="AvgS")
//plot(strategy.equity, title="equity", color=color.red, linewidth=2, style=plot.style_areabr)

if sz[1]<0 and sz<0 and vrsi2<overBought2 and vrsi2[1]>=overBought2
    strategy.close_all("x")
if sz[1]>0 and sz>0 and vrsi2>overSold2  and vrsi2[1]<=overSold2 
    strategy.close_all("x")
    
plot(vrsi,'open rsi',color=color.green)        
plot(vrsi2,'close rsi',color=color.red)    

hline(overBought, "RSI Upper Band", color=#787B86)
hline(overSold, "RSI Upper Band", color=#787B86)

```

> Detail

https://www.fmz.com/strategy/478739

> Last Modified

2025-01-17 16:22:28
