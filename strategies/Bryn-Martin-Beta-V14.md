
> Name

Bryn-Martin-Beta-V14

> Author

阿乐

> Strategy Description

myLanguage Strategy
The backtest results are okay. The real offer has been running for a while. Laqua, the real offer profit is about half of the backtest profit. It cannot beat the real offer fee. The risk is high and the return is small. If you use it, change it..

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|N|0.002|Fund Utilization or Lot Size|
|XX|true|Double the value|
|sssss|true|Live trading parameter coefficient2|
|TC|0.001|Initial Order Quantity|
|FB|4|Maximum multiplication times|
|CJ|2|Adding coefficient|
|BLD|false|1=Middle rail position opening-0=Upper and lower rail position opening|
|FX|2|0Long-1 Short-2 Both Open|
|len|26|Trend Line Period|
|CJ2|2|Closing coefficient|


> Source (MyLanguage)

``` pascal
(*backtest
start: 2022-04-01 00:00:00
end: 2022-04-09 00:00:00
period: 5m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT","balance":100}]
args: [["N",1],["BLD",1],["RunMode",1,126961],["MaxCacheLen",3000,126961],["ContractType","swap",126961],["MinLot",0.001,126961],["LoopInterval",1,126961],["SyncDelay",1,126961],["MarginLevel",50,126961]]
*)


//pictures


N := 26; // Parameter range 5, 300
M := 26; // Parameter range 1, 100
P := 2; // Parameter range 1, 10


MID:=MA(CLOSE,N);
TMP2:=STD(CLOSE,M);
TOP:=MID+P*TMP2;
BOTTOM:=MID-P*TMP2;


hh^^HHV(H,len);//Take the highest price within a certain period

ll^^LLV(L,len);//Take the lowest price within a certain period

hl2^^(hh+ll)/2;//Average of the highest price and lowest price

avg^^MA(hl2,5);//Calculate the smoothed moving average for the mean value

//Slope:SLOPE(avg,len);// Calculate the regression slope for the moving average





TR:=MAX(MAX((HIGH-LOW),ABS(REF(CLOSE,1)-HIGH)),ABS(REF(CLOSE,1)-LOW));
ATR:=WMA(TR,26); //Calculate the simple moving average of true range over 26 periods
//TC:0.002;//MAX(ROUND(0.002*MONEY/500,3),0.002);//trading fee0.023,leverage50times
Account amount:MONEY;
zongtc:=ABS(BKVOL+SKVOL);



//H20^^HHV(H,20)/2+LLV(L,20)/2;
//H10^^HHV(H,10)/2+LLV(L,10)/2;
BLD=0 AND FX=0 AND BKVOL=0 AND SKVOL=0 AND  CROSS(CLOSE,BOTTOM),BK(TC);//Go long when price crosses above the lower Bollinger Band
BLD=1 AND FX=0 AND BKVOL=0 AND SKVOL=0 AND  CROSS(CLOSE,MID),BK(TC);//Go long when price crosses above the middle Bollinger Band
FX=0 AND ISLASTBK AND C < BKPRICE-ATR*CJ , BK(ROUND(XX*BKVOL,3));
//Bidirectional
BLD=0 AND FX=2 AND BKVOL=0 AND SKVOL=0 AND  CROSS(CLOSE,BOTTOM),BK(TC);//Go long when price crosses above the lower Bollinger Band
BLD=1 AND FX=2 AND BKVOL=0 AND SKVOL=0 AND  CROSS(CLOSE,MID),BK(TC);//Go long when price crosses above the middle Bollinger Band
FX=2 AND ISLASTBK AND C < BKPRICE-ATR*CJ , BK(ROUND(XX*BKVOL,3));

//Long take profit
BKVOL>0 AND C > BKPRICEAV+ATR*CJ2 , SP(BKVOL);
BKVOL>=0.008 AND C > BKPRICEAV+(ATR*CJ2)/2 , SP(0.001);


 //Many=0Empty=1Bidirectional=2
BLD=0 AND FX=1 AND BKVOL=0 AND SKVOL=0 AND  CROSS(BOTTOM,CLOSE),SK(TC);//Go short when price crosses below the upper Bollinger Band
BLD=1 AND FX=1 AND  BKVOL=0 AND SKVOL=0 AND  CROSS(MID,CLOSE),SK(TC);//Go short when price crosses below the middle Bollinger Band
FX=1 AND ISLASTSK AND C > SKPRICE + CJ*ATR, SK(ROUND(XX*SKVOL,3));
//Bidirectional
BLD=0 AND FX=2 AND BKVOL=0 AND SKVOL=0 AND  CROSS(BOTTOM,CLOSE),SK(TC);//Go short when price crosses below the upper Bollinger Band
BLD=1 AND FX=2 AND  BKVOL=0 AND SKVOL=0 AND  CROSS(MID,CLOSE),SK(TC);//Go short when price crosses below the middle Bollinger Band
FX=2 AND ISLASTSK AND C > SKPRICE + CJ*ATR, SK(ROUND(XX*SKVOL,3));

SKVOL>0 AND C < SKPRICEAV - CJ2*ATR , BP(SKVOL);
SKVOL>=0.008 AND C < SKPRICEAV - (CJ2*ATR)/2 , BP(0.001);






TRADE_AGAIN(FB);
```

> Detail

https://www.fmz.com/strategy/345504

> Last Modified

2022-04-19 13:19:44
