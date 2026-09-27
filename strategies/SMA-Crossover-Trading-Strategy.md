
> Name

SMA-Crossover-Trading-Strategy

> Author

ChaoZhang

> Strategy Description



SMA Crossover Trading Strategy

This strategy generates trading signals based on crossover between two SMA lines of different periods. A long signal is triggered when the faster SMA crosses above the slower SMA. A short signal occurs when the faster SMA crosses below the slower SMA.  

Some key benefits of this strategy:

- Identifies trend changes using SMA crossovers
- Simple and straightforward rules  
- Customizable SMA periods for optimization
- Applicable for any timeframe

However, some potential limitations exist:

- Prone to false signals during range-bound markets
- Lagging signals, late entry timing 
- No stop loss, can lead to large drawdowns
- Lack of filters, uncontrolled signal quality

Some ways to enhance the strategy:

- Add stop loss when price touches slower SMA
- Scale in based on bull/bear candle closes 
- Optimize SMA period combinations  
- Adjust position sizing and risk management

Overall, the SMA crossover method works well in trending markets but must be traded cautiously during choppy periods. Incorporating stop loss and proper risk management can reduce downside risks.




> Source (PineScript)

``` pinescript
/*backtest
start: 2023-08-11 00:00:00
end: 2023-09-10 00:00:00
period: 10m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy("SMA Crossover demo", overlay=true)

shortCondition = crossover(sma(close, 34), sma(close, 4))
if (shortCondition)
    strategy.entry("Sell/Short", strategy.short)

longCondition = crossunder(sma(close, 34), sma(close, 4))
if (longCondition)
    strategy.entry("Buy/Long", strategy.long)
    



    
```

> Detail

https://www.fmz.com/strategy/426335

> Last Modified

2023-09-11 11:42:52
