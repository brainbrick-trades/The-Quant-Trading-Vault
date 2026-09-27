
> Name

Brutal-Martingale-Suitable-for-ETH-and-BTC-Copy

> Author

Zer3192

> Strategy Description

ETH Set up 0.002 lots for every 600 US dollars, with a profit of 50% in one month. It is recommended to withdraw the profits every two months, because Martin's final destination is to liquidate his position. There is no Martin in the world who will not liquidate his position. It is recommended to have 3 funds, which is 1800 US dollars to use. BTC has not been tested. In short, it is very violent.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|N|0.002|Fund Utilization or Lot Size|
|XX|true|Double the value|
|sssss|true|Live trading parameter coefficient2|


> Source (MyLanguage)

``` pascal
(*backtest
start: 2022-01-01 08:00:00
end: 2022-02-02 00:00:00
period: 6h
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"ETH_USDT","balance":600,"fee":[0.008,0.025]}]
args: [["RunMode",1,126961],["TradeAmount",0.001,126961],["MaxCacheLen",3000,126961],["ContractType","swap",126961],["MinLot",0.001,126961],["LoopInterval",1,126961],["SyncDelay",1,126961],["MarginLevel",50,126961]]
*)




TR:=MAX(MAX((HIGH-LOW),ABS(REF(CLOSE,1)-HIGH)),ABS(REF(CLOSE,1)-LOW));
ATR:WMA(TR,10); //Calculate the simple moving average of true range over 26 periods
TC:N;//MAX(ROUND(5/C*MONEY/200,3),0.002);//Fee 0.023, leverage 50x
yue:ABS(BKVOL+SKVOL);
junjia:ABS(BKPRICEAV+SKPRICEAV);



CCC^^WMA(C,20);
AA^^WMA(C,10);



BKVOL=0 AND SKVOL=0 AND  REF(AA,1)>REF(CCC,1)  , BK(TC);


ISLASTBK AND C < BKPRICE-ATR*0.1 , BK(ROUND(XX*BKVOL,3));


BKVOL>0 AND C > BKPRICEAV+ATR*0.1 , SP(BKVOL);




REF(AA,1)<REF(CCC,1)    AND BKVOL>0,SP(BKVOL);
 INFO(REF(AA,1)<REF(CCC,1)    AND BKVOL>0, 'Stop Loss Exit');
 
 

SKVOL=0 AND BKVOL=0 AND  REF(AA,1)<REF(CCC,1)  , SK(TC);



ISLASTSK AND C > SKPRICE + 0.1*ATR, SK(ROUND(XX*SKVOL,3));


SKVOL>0 AND C < SKPRICEAV - 0.1*ATR , BP(SKVOL);





REF(AA,1)>REF(CCC,1)   AND SKVOL>0,BP(SKVOL);
 INFO(REF(AA,1)>REF(CCC,1)AND SKVOL>0  , 'Stop Loss Exit');
MULTSIG(0, 0, 50, 0);
TRADE_AGAIN(100);
```

> Detail

https://www.fmz.com/strategy/343745

> Last Modified

2022-02-06 07:08:49
