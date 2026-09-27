
> Name

Three-Line-Code-Implements-Argos-Machine-Learnings-Rapid-Interpretation-of-Industry-News-with-a-Counter-Pointing-Strategy

> Author

Zero

> Strategy Description

> Argos 

https://www.quantinfo.com/Argus/

> Notes

Argus (Argus Ἄργος) The hundred-eyed giant from Greek mythology
This system is a project of Quant Online, a subsidiary of the inventor. After five years of research and development, the entire network monitors price fluctuations and related information in futures, stocks, options, commodities, foreign exchange, etc.
Uses the most cutting-edge AI neural networks currently in technology, trained hundreds of millions of times
It can predict effective stock order quotations, predict financial asset price changes, predict S&P 500 index volatility, optimize investment portfolios, and predict price fluctuations based on news headlines.

 ![IMG](https://www.fmz.com/upload/asset/18bc0cc19ceb00d6bc9.png) 

> Implementation

Although the bullshit is fine, the embarrassing fact proves that it is better to counter-point with Argos, which uses AI technology. If it predicts a rise, we will sell, and if it predicts a fall, we will buy.
When others are greedy I am fearful, when others are fearful I am greedy, because it predicts public sentiment; to make money, you have to go against the crowd.

> Strategy

With the help of the powerful syntax support of the inventor platform, in order to display the most intuitive effect, the enhanced version of My language is selected. The data source returns a decimal from 0 to 1 to describe the probability of increase. If the user needs to obtain data of other varieties, just modify the name of the variety in the URL of the strategy code.

> Results

 ![IMG](https://www.fmz.com/upload/asset/2440e3472cba14cd778.png) 
 
> Finally

  If you want to define your own third-party data source, ReferenceAPI https://www.fmz.com/api#exchange.getdata
  This strategy only demonstrates how to call third-party data sources for backtesting and verification. Do not conduct live trading!!!




> Source (MyLanguage)

``` pascal
(*backtest
start: 2019-10-01 00:00:00
end: 2020-04-21 23:59:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Bitfinex","currency":"BTC_USD"}]
*)

Predicted value: DATA('https://www.quantinfo.com/API/Argus/history?symbol=Bitcoin');
Predicted value>HV(predicted value, 5)&&predicted value>0.6,SPK;
Predicted value < LV(predicted value, 10) && predicted value<0.4,BPK;
```

> Detail

https://www.fmz.com/strategy/201665

> Last Modified

2020-04-23 19:50:41
