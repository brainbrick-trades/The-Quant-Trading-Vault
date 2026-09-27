
> Name

Intelligent-Interval-Doubling-Strategy-Sale-Version

> Author

高频量化

> Strategy Description

Strategy introduction:

The intelligent multiplier strategy is an investment strategy based on artificial intelligence technology, with advantages mainly reflected in the following aspects:

Automated decision-making: The intelligent double investment strategy can automatically analyze market data, generate trading signals, and automatically execute transactions through artificial intelligence technology, thereby achieving fully automated trading decisions.

Accurate prediction ability: The intelligent multiplier strategy can use artificial intelligence technology to perform deep learning and analysis on market data, thereby improving prediction ability and more accurately forecasting market trends and trading signals.

Efficient risk control: The intelligent doubling strategy can monitor and control market risks in real time through artificial intelligence technology, thereby achieving efficient risk control and fund management.

Strong adaptability: The intelligent double investment strategy can be adaptively adjusted according to market conditions and investors' risk preferences, thereby better adapting to different market environments and investor needs.

Efficient execution capabilities: The intelligent doubling investment strategy can achieve efficient transaction execution through artificial intelligence technology, thereby improving transaction efficiency and execution capabilities.

It should be noted that the intelligent doubling investment strategy also has certain risks and needs to be adjusted and optimized according to the actual situation. It also requires a certain understanding and mastery of artificial intelligence technology.

The doubling strategy is a common investment strategy, and its basic idea is to increase the investment when experiencing a loss, with the expectation of making up for previous losses in future profits. The advantages of this strategy are mainly reflected in the following aspects.:

High flexibility: The doubling investment strategy can be adjusted according to market conditions, and the investment amount and frequency of investment can be flexibly adjusted according to the actual situation to achieve optimal results.

Strong risk control ability: The double investment strategy can control risks by gradually increasing investment. When the market suffers a loss, it can make up for the previous losses by increasing investment, thereby reducing risks.

High profit potential: The double investment strategy can obtain higher returns when the market conditions are good, because when the market conditions are good, higher returns can be obtained by increasing investment.

Wide applicability: The double investment strategy is suitable for various markets, including stocks, futures, foreign exchange, etc., and can be adjusted according to the characteristics of different markets to achieve optimal results.

It should be noted that the doubling investment strategy also has certain risks. If the market conditions continue to be bad, the investment amount may become larger and larger, eventually leading to losses. Therefore, when using the double investment strategy, you need to make adjustments according to market conditions and control risks to achieve optimal results.

ATR(Average True Range)is a commonly used technical indicator used to measure market volatility. In quantitative trading, adding the ATR adjustment interval can bring the following benefits::

More adaptable to market fluctuations: Market volatility is constantly changing. Adding the ATR adjustment interval can adjust the trading interval according to changes in market volatility, thereby becoming more adaptable to market fluctuations.

Control risks: Adding the ATR adjustment interval can control the frequency of transactions and thereby control risks. When the market volatility is high, the trading interval can be shortened to respond to market changes faster; when the market volatility is low, the trading interval can be extended to avoid the risks caused by frequent trading.

Increase returns: Adding the ATR adjustment interval can increase the number of transactions when market volatility is high, thereby increasing returns. When market volatility is low, the number of transactions is reduced, which can avoid the costs of frequent transactions.

It should be noted that adding the ATR adjustment interval needs to be adjusted according to the actual situation, and high-frequency trading or low-frequency trading cannot be pursued blindly. At the same time, the ATR indicator also has a certain lag, and it needs to be comprehensively analyzed in conjunction with other indicators and market conditions.

The main advantages and benefits of this strategy are as follows::

Use the ATR indicator to calculate volatility: This strategy uses the ATR indicator to calculate the true volatility, which can more accurately reflect market volatility, thereby more accurately controlling trading frequency and risk.

Use WMA indicator for moving average calculation: This strategy uses WMA indicator for moving average calculation, which can more accurately reflect market trends and thus judge trading signals more accurately.

Strict stop-loss and take-profit mechanisms: This strategy sets strict stop-loss and take-profit mechanisms, which can effectively control risks and losses while also protecting profits.

Flexible parameter settings: The parameter settings of this strategy are relatively flexible and can be adjusted according to the actual situation, thus making it more adaptable to different market conditions.

Wide applicability: This strategy is suitable for various markets, including stocks, futures, foreign exchange, etc., and can be adjusted according to the characteristics of different markets to achieve optimal results.

It should be noted that this strategy is for reference only, and specific application needs to be adjusted and optimized according to the actual situation. At the same time, quantitative trading involves multiple aspects of knowledge and skills, and requires certain programming and trading experience to better apply this strategy.


Backtesting Records
![IMG](https://www.fmz.com/upload/asset/16ff4e015669c86ce919a.png)

![IMG](https://www.fmz.com/upload/asset/16f9cef7ddbc29577c733.png)

![IMG](https://www.fmz.com/upload/asset/16fe3ffa965a4179bdd6a.png)

![IMG](https://www.fmz.com/upload/asset/16eb3353f3f016e779004.png)

![IMG](https://www.fmz.com/upload/asset/16f58685f1f57a3c14276.png)

The backtest record is too long; if interested, you can load the backtest yourself

Live Display
Has Fund Curve
Has Asset Display
Display positions with open orders

2023.05.15 Users reported that profit cannot cover the handling fees, and inspection found that the handling fees for each user are different. To solve this problem, quote the handling rate parameter



> Source (javascript)

``` javascript
/*backtest
start: 2023-04-01 00:00:00
end: 2023-05-01 00:00:00
period: 5m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT","balance":10000}]
args: [["TransactionVal",300,411371]]
*/


/*
0.Please refer to the tutorial for detailshttps://www.fmz.com/bbs-topic/4145
1.Add Exchange
2.Deploy Custodian
3.Create and modify parameters
4.Create and manage live accounts

5.Technical Support VX:18826683356 OKEX live trading is free

5.1 Binance real trading permission fees are as follows:
6.TRC(20)Mainnet CollectionUSDTAddress: TFZn8YGYRVuE5CPLsSieaKgPbwJrG3E8e7
7 Pay via Binance Mobile Number 18826683356 (No Fees) It is recommended to use this payment method
8.Binance requires payment of 100 USDT/3 months
  Binance needs to pay 500 USDT/perpetual

9.No guarantee on strategy profit; can run by referencing backtesting parameter settings
10.Unauthorized permission, time is precious, please do not contact us
*/

/*
Parameter Analysis

Set leverage: Set the multiple of funds used for the contract. The greater the leverage, the less margin is needed to open a position
Stop loss value: if the loss reaches a certain percentage of the total account funds, liquidate the position forcibly
Initial opening value USDT: The value of the first order opening. If it is set to 300, the current trading product is BTC_USDT, and the quotation is 30000, then the opening amount is 300/30000=0.01
Double value: If there is already a position order, the position will be added to level the position cost. Set to 1, then the added position amount is consistent with the position amount. This parameter needs to be set to a positive integer
ATRCycle amplitude days: parameters of indicator ATR
Long-term moving average: parameters of indicator MA
Short-term moving average: parameters of indicator MA
Moving average reversal closing: Check, if long-term moving average > short-term moving average, all long orders will be fully closed; if long-term moving average < short-term moving average, all short orders will be fully closed
Maximum number of open orders: The number of times you can add to your position if you meet the conditions. After one cycle, the count will be reset
ATRCoefficient: used to modify the ATR value and adjust the volatility interval
*/
//2023.05.15 Users reported that profit cannot cover the handling fees, and inspection found that the handling fees for each user are different. To solve this problem, quote the handling rate parameter
//Bidirectional position

function main() {
    Log("Strategy Confidential,Copying allows you to directly load the Binance Futures backtest andOKEXFree real trading at futures exchange"); 
    Log("Strategy Confidential,Copying can directly load the real trading of Binance Futures Exchange. You need to pay a fee to activate the permission.");   
    $.main1()
}
```

> Detail

https://www.fmz.com/strategy/417138

> Last Modified

2023-06-11 20:07:40
