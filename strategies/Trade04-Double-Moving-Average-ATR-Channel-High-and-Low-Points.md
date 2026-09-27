
> Name

Trade04-Double-Moving-Average-ATR-Channel-High-and-Low-Points

> Author

作手君TradeMan

> Strategy Description

In order to give back to the FMZ platform and community, share strategies & codes & ideas & templates

Introduction:
Volume-price factor combination

✱Contact Information (Welcome to Discuss and Learn Together))
WECHAT: haiyanyydss
TEL: https://t.me/JadeRabbitcm
✱Fully automatic CTA & HFT trading system @2018 - 2023

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|percent|5|percent|
|LENGTH1|12|LENGTH1|


> Source (MyLanguage)

``` pascal
(*backtest
start: 2018-01-01 00:00:00
end: 2021-06-30 23:59:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_OKCoin","currency":"BTC_USD","stocks":10}]
args: [["percent",5],["ContractType","quarter",126961]]
*)


//Product Version
LENGTH2:=10*LENGTH1;//Long-term parameters
X:=3;//Range Coefficient

//Trading volume 
//LOTS:=MAX(1,INTPART(percent/100*MONEY/(C*MARGIN*UNIT)));//Gold principal
LOTS:=MAX(1,INTPART(percent/100*MONEY*C/(MARGIN*UNIT)));//Coin principal
	
TR:=MAX(MAX((HIGH-LOW),ABS(REF(CLOSE,1)-HIGH)),ABS(REF(CLOSE,1)-LOW));
ATR:=MA(TR,LENGTH1);
OO:=BARSLAST(DATE<>REF(DATE,1))+1;
OPD:=VALUEWHEN(OO=1,O);
					     	
L1:=MIN(LENGTH1,LENGTH2);
L2:=MAX(LENGTH1,LENGTH2);
MA1:=EMA(REF(C,1),L1);     
MA2:=EMA(REF(C,1),L2);
					     	
UPPERBAND^^OPD+X*ATR;
LOWERBAND^^OPD-X*ATR;
EXITLONG:=REF(L,L2);
EXITSHORT:=REF(H,L2);
	
//Long Entry 
BKVOL<=0 AND REF(C,1) >= REF(UPPERBAND,1) AND VOL > 0 AND MA1>MA2 AND REF(C,1) >=REF(H,L1) ,BPK(LOTS);
//Short Entry	
SKVOL<=0 AND REF(C,1) <= REF(LOWERBAND,1) AND VOL > 0 AND MA1<MA2 AND REF(C,1) <=REF(L,L1) ,SPK(LOTS);
//Long Exit
REF(C,1)>= BKPRICE  AND REF(C,1)<=EXITLONG AND BKVOL>0 AND BARPOS>0,SP(BKVOL); 
 //Short Entry
REF(C,1)<= SKPRICE  AND REF(C,1)>=EXITSHORT AND SKVOL>0 AND BARPOS>0,BP(SKVOL);
```

> Detail

https://www.fmz.com/strategy/425799

> Last Modified

2023-09-04 22:33:38
