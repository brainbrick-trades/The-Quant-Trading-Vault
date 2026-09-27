
> Name

Trade03-Double-Moving-Average-Volatility-Difference-Filtering

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
|S1|100|S1|
|percent|10|percent|


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

S2:=10*S1;
	
ST:=1;
	
//LOTS:=MAX(1,INTPART(percent/100*MONEYTOT/(C*MARGIN*UNIT)));//Gold principal
LOTS:= MAX(1,INTPART(percent/100*MONEYTOT*C/(MARGIN*UNIT)));//Coin principal

MA1^^EMA(REF(C,1),S2);//moving average1
MA2^^EMA(MA1,S1);//moving average2

DBF:=IF((HIGH+LOW)<=(REF(HIGH,1)+REF(LOW,1)),0,MAX(ABS(HIGH-REF(HIGH,1)),ABS(LOW-REF(LOW,1))));//If the sum of the high and low of the current BAR line is smaller than the sum of the previous BAR line, take 0. If it is larger, take the maximum value of HIGH-HIGH[1] and LOW-LOW[1].;
KBF:=IF((HIGH+LOW)>=(REF(HIGH,1)+REF(LOW,1)),0,MAX(ABS(HIGH-REF(HIGH,1)),ABS(LOW-REF(LOW,1))));//If the sum of the high and low of the current BAR line is greater than the sum of the previous BAR line, take 0. If it is smaller, take the maximum value of HIGH-HIGH[1] and LOW-LOW[1].;
DBL:=(DBF+S1)/((DBF+S1)+(KBF+S1));//Compare the difference calculated by DBF with the sum of DBF+KBF, which is the change rate;
KBL:=(KBF+S1)/((KBF+S1)+(DBF+S1));//Compare the difference calculated by KBL with the sum of KBF+DBF, which is the change rate;
CHANGE:=DBL-KBL;//Make the difference between the long and short change rates to get the volatility difference;
MACHANGE:=MA(CHANGE,S1);//Calculate the average value of the fluctuation difference S1 within the period;
MACHANGE2:=EMA(MACHANGE,S1);//Smooth the mean value of the fluctuation difference twice to obtain the moving average;

BUYK:=BARPOS>S2 AND REF(C,1)>MA1 AND MA1>MA2 AND CHANGE>0 AND MACHANGE>MACHANGE2;//Bullish opening conditions
SELLK:=BARPOS>S2 AND REF(C,1)<MA1 AND MA1<MA2 AND CHANGE<0 AND MACHANGE<MACHANGE2;//Bearish opening conditions

SELLY:=REF(C,1)<MA1 AND REF(C,1)>BKPRICE*(1+0.01*ST);//Long Take Profit
BUYY:=REF(C,1)>MA1 AND REF(C,1)<SKPRICE*(1-0.01*ST);//Short Take Profit


BKVOL<=0 AND REF(BUYK,1),BPK(LOTS);

SKVOL<=0 AND REF(SELLK,1),SPK(LOTS);
	
BKVOL>0 AND  REF(SELLY,1),SP(BKVOL);

SKVOL>0 AND  REF(BUYY,1),BP(SKVOL);

```

> Detail

https://www.fmz.com/strategy/425797

> Last Modified

2023-09-04 22:33:22
