
> Name

Adaptive-Moving-Average-Crossover-Strategy-Based-on-Uhl-MA

> Author

ChaoZhang

> Strategy Description



## Overview

Uhl MAThe system is an adaptive moving average crossover system, which is designed to make up for the shortcomings of the traditional moving average system. This system uses fast moving average and slow moving average crossovers to generate trading signals. The slow moving average uses the modified moving average (CMA) originally proposed by Uhl, and the fast moving average uses the corrected trend step (CTS) which is also based on the idea of ​​the modified moving average. The system achieves more stable and reliable trading signals by adaptively adjusting the moving average parameters.

## Principle Analysis  

The core of this strategy is the calculation of Uhl MA moving average and CTS moving average. Among them, the Uhl MA moving average is modified on the basis of the traditional SMA moving average, and is adaptively adjusted by introducing the variance VAR and the squared difference SECMA of the historical CMA. When VAR is smaller than SECMA, increase the proportion of SMA; when VAR is greater than SECMA, increase the proportion of CMA. This can filter out some noise and produce a more stable moving average. The calculation idea of CTS moving average is similar to that of Uhl MA moving average. It is adaptively adjusted based on the SRC price.  

The crossover principle is the same as the traditional moving average crossover system. When CTS crosses Uhl MA upward, a buy signal is generated, and when CTS crosses Uhl MA downward, a sell signal is generated. This forms an adaptive moving average trading system.

## Advantage Analysis

Compared to traditional moving average crossover systems, the biggest advantage of this strategy is the use of adaptive moving averages, which can filter out some noise and generate more reliable trading signals in ranging markets. Compared to death cross and golden cross signals, adaptive moving average crossovers reduce the probability of false trades. In addition, the combination of fast and slow lines can capture better trend trading opportunities. From the backtesting results, the strategy performs excellently in instruments with obvious trends.

## Risk Analysis  

Since the moving average is essentially a technical indicator used to determine trends, the biggest risk of this strategy is the high probability of generating false signals in volatile market conditions. This is mainly due to the adaptive calculation method of CMA moving average, which will also converge to the price area in a volatile market, generating unnecessary signals. In addition, finding a suitable parameter combination is also a big problem. If parameters are set improperly, good trading opportunities will be missed or the probability of false signals will increase.

## Optimization Suggestions

This strategy can mainly be optimized from the following aspects:

1. Improve the CMA adaptive calculation method to avoid its convergence in volatile market conditions and the generation of erroneous signals. You can consider introducing other indicators for correction.

2. Optimize parameter settings to find the best parameter combination. Multi-dimensional parameter optimization can be performed using genetic algorithms or other methods.

3. Add stop loss strategy to control single loss.

4. Combine with other indicators to filter signals to avoid frequent trading in volatile market conditions. For example, introduce volatility indicators, RFM indicators, etc.

5. Optimize capital management, such as risk measurement, position control, etc., to better control overall risk.

## Summary

Uhl MAThe system is a very innovative adaptive moving average crossover strategy. Compared with traditional strategies, its use of dynamic moving averages can reduce the probability of mistaken transactions and better capture trend opportunities. However, this strategy also has certain limitations, mainly underperforming under volatile market conditions. By further improving the calculation method and introducing other auxiliary indicators for filtering optimization, there is still a lot of room for improvement. At the same time, parameter optimization and risk control are also key. Overall, Uhl MA strategy has good development prospects and research value.



|| 

## Overview

The Uhl MA system is an adaptive moving average crossover system designed to overcome the deficiencies of traditional MA systems. It uses fast and slow moving averages to generate trading signals, with the slow MA being the corrected MA (CMA) originally proposed by Andreas Uhl and the fast MA being the corrected trend step (CTS) which is also based on the corrected MA. The system adaptively adjusts the MA parameters to achieve more reliable trading signals.

## Principle Analysis

The core of this strategy lies in the calculation of Uhl MA and CTS lines. Uhl MA line is an enhancement over the traditional SMA, using variance (VAR) and historical squared deviation (SECMA) to adaptively adjust the weights between SMA and previous CMA. When VAR is less than SECMA, more weight is put on SMA, otherwise more weight is put on CMA. This helps filter out some noise and generate smoother MA. CTS line uses similar adaptive calculation based on SRC price.

The crossover logic is the same as traditional MA systems. A buy signal is generated when CTS crosses above Uhl MA, and a sell signal when crossing below. This forms an adaptive MA trading system.

## Advantage Analysis

Compared to traditional MA crossover systems, the biggest advantage of this strategy is the use of adaptive MAs, which can filter some noise and generate more reliable signals in range-bound markets. The adaptive crossover reduces false signals compared to dead cross and golden cross. Also, the fast and slow MA combination allows catching some trend-trading opportunities. From backtest results we can see superior performance in assets with obvious trends.

## Risk Analysis

The major risk of this strategy comes from the increased false signals in ranging markets, as MAs are trend-following indicators in nature. This is largely due to the adaptive calculation of CMA, which converges to price ranges in consolidation, generating unnecessary signals. Proper parameter tuning is also a big challenge. Improper parameters may lead to missing good trades or increased false signals.

## Optimization Suggestions

The potential optimizations include:

1. Improve CMA calculation to avoid convergence in ranging markets, using other indicators for example.

2. Optimize parameters through multi-variate optimization algorithms like genetic algorithms. 

3. Introduce stop loss to control single trade loss.

4. Add filters using other indicators to avoid over-trading in consolidation, such as volatility measures, RFM index etc.

5. Optimize risk management including position sizing, risk metrics to better control overall risk.

## Conclusion

The Uhl MA system is a very innovative adaptive MA crossover strategy. Compared to traditional strategies, the dynamic MAs help reduce false signals and better capture trends. But limitations exist in ranging markets. Further improvements in calculation methodology and adding filters hold great potential. Meanwhile, parameter tuning and risk control are also critical. Overall, the Uhl MA strategy has good potential and research value worth further exploration.



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|100|length|
|v_input_2|true|mult|
|v_input_3_close|0|src: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-01-01 00:00:00
end: 2023-06-25 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © alexgrover

//@version=4
strategy("Uhl MA System - Strategy Analysis")
length = input(100),mult = input(1.),src = input(close)
//----
out = 0., cma = 0., cts = 0.
Var = variance(src,length)           ,sma = sma(src,length)
secma = pow(nz(sma - cma[1]),2)      ,sects = pow(nz(src - cts[1]),2) 
ka = Var < secma ? 1 - Var/secma : 0 ,kb = Var < sects ? 1 - Var/sects : 0
cma := ka*sma+(1-ka)*nz(cma[1],src)  ,cts := kb*src+(1-kb)*nz(cts[1],src)
//----
if crossover(cts,cma)
    strategy.entry("Buy", strategy.long)
if crossunder(cts,cma)
    strategy.entry("Sell", strategy.short)
//----
cap = 50000
eq = strategy.equity
rmax = 0.
rmax := max(eq,nz(rmax[1]))
//----
css = eq > cap ? #0cb51a : #e65100
a = plot(eq,"Equity",#2196f3,2,transp=0)
b = plot(rmax,"Maximum",css,2,transp=0)
fill(a,b,css,80)
```

> Detail

https://www.fmz.com/strategy/427312

> Last Modified

2023-09-19 22:06:42
