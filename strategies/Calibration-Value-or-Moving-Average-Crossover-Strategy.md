
> Name

Calibration-Value-or-Moving-Average-Crossover-Strategy

> Author

cyberking

> Strategy Description

Benchmark value
 Sell if the high point > btc 10000 || MA(10) < MA(30).;
 Buy if the mid support point < btc 6725 || MA(10) > MA(30).;
 StoplossStop-loss point set at 8, 8%.
 Cycle according to daily line. Backtest data is acceptable; backtest data below the daily cycle is poor..
 This strategy uses trend indicators.
*Take10000and6725The reason is based on Gann's idea.
 ![IMG](https://www.fmz.com/upload/asset/149338fe3f9011badc20c.png)  ![IMG](https://www.fmz.com/upload/asset/14947231d56707e5f7e8c.png) 

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|HGH|10000|High point|
|MMD|6725|Core point|
|STOPLOSS|8|Stop-loss quantity|


> Source (MyLanguage)

``` pascal
(*backtest
start: 2019-01-05 00:00:00
end: 2020-02-29 00:00:00
period: 1d
exchanges: [{"eid":"Huobi","currency":"BTC_USDT"}]
*)
//
MA10:=MA(C,10);
MA30:=MA(C,30);

Buy Opening Price:=VALUEWHEN(BARSBK=1,O);
Sell Opening Price:=VALUEWHEN(BARSSK=1,O);
//Conditions for opening a position

BUYCONDITION:=REF(C,1) < MMD OR CROSSUP(MA10,MA30);
SELLCONDITION:=REF(C,1) > HGH OR CROSSDOWN(MA10,MA30);

BKVOL=0 AND BUYCONDITION,BK;
SKVOL=0 AND SELLCONDITION,SK;

//Exit conditions
BKVOL>0 AND SELLCONDITION,SP;
SKVOL>0 AND BUYCONDITION,BP;
// Start stop loss
SKVOL>0 AND HIGH>=Sell Opening Price*(1+STOPLOSS*0.01),BP;
BKVOL>0 AND LOW<=Buy Opening Price*(1-STOPLOSS*0.01),SP;
AUTOFILTER;
```

> Detail

https://www.fmz.com/strategy/187874

> Last Modified

2020-03-02 11:22:35
