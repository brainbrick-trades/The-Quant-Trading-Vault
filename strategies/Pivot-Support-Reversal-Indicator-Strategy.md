
> Name

Pivot-Support-Reversal-Indicator-Strategy

> Author

ChaoZhang

> Strategy Description



## Strategy Logic

This strategy combines the Pivot Support Reversal indicator with support/resistance levels to track trends and manage profit/drawdown. 

The rules are:

1. Go long when the PSR indicator generates a buy signal

2. Take 25% partial profit at R1 

3. Take another 25% partial profit at R2

4. Use a moving stop loss below the 14-period moving average minus 3xATR

The PSR indicator synthesizes CMO, Bollinger Bands, volume and more into high-probability signals. Pivot points act as profit targets while having trend-following ability. The strategy's strength lies in its staged profit taking and disciplined stop loss to lock in profits while tightly controlling risk.

## Advantages 

- PSR combines multiple factors for high-quality signals

- Pivots act as profit targets and tracking tools

- Staged profit taking and trailing stop protects profits and manages risk

## Risks

- PSR parameters need optimization 

- Pivots can sometimes be breached

- Risk remains for residual position after partial profits

## Summary

This strategy capitalizes on the PSR indicator's syndicated signals and uses pivots as dynamic profit targets. By taking profits in batches and cutting losses fast, it aims to pragmatically book profits while tightly controlling risk.




> Source (PineScript)

``` pinescript
/*backtest
start: 2023-01-01 00:00:00
end: 2023-09-13 00:00:00
period: 3d
basePeriod: 1d
exchanges: [{"eid":"Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © ParaBellum68

//@version=4
strategy(title="SOJA PIVOT", shorttitle="SOJA PIVOT")
soja = ((cmo(close,5) > 25) and (cmo(close,5) < 70) and (close> close[1]) and (bbw(close,50,1) < 0.6) and (sum(volume,5)> 250000) and (obv[5]>15))
TP = 2.1 * hlc3[1]- high[1]
TP2 = TP + high[1] - low[1]
SL = avg(close,14) - 3*atr(14)
strategy.entry("buy", true, 1, when = soja == 1)
strategy.close("buy", when = close > TP)
strategy.close("buy", when = close > TP2)
strategy.exit("stop", "exit", when = close < SL)





```

> Detail

https://www.fmz.com/strategy/426785

> Last Modified

2023-09-14 15:49:31
