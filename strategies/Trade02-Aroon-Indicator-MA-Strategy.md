
> Name

Trade02-Aroon-Indicator-MA-Strategy

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
|N|240|N|
|percent|5|percent|


> Source (MyLanguage)

``` pascal
(*backtest
start: 2018-01-01 09:00:00
end: 2021-07-30 15:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_OKCoin","currency":"BTC_USD","stocks":10,"fee":[0.05,0.05]}]
args: [["N",120],["SlideTick",0,126961],["ContractType","quarter",126961]]
*)



//LOTS:=MAX(1,INTPART(percent/100*MONEYTOT/(C*MARGIN*UNIT)));//Gold principal
LOTS:= MAX(1,INTPART(percent/100*MONEYTOT*C/(MARGIN*UNIT)));//Coin principal

MALONG:EMA(REF(C,1),N); //Calculate long-term moving average
HH_N:MIN(BARSLAST(HHV(H,N)>HHV(REF(H,1),N))+1,N);//Calculate the number of days after the highest price occurs within the lookback period
LL_N:MIN(BARSLAST(LLV(L,N)<LLV(REF(L,1),N))+1,N);//Calculate the number of days after the lowest price occurs within the lookback period
	
//	N: Look-back time window  HH_N: The number of days after the highest price during the lookback period  LL_N: The number of days after the lowest price during the lookback period

AROON_UP:=(N-HH_N)/N * 100;//Calculate the high price Aron indicator
AROON_DN:=(N-LL_N)/N * 100;//Calculate low price Aron indicator
AROON:=AROON_UP-AROON_DN;//Calculate the Aron indicator difference

//*Usage Method
//(1) when AROON_UP Break above 70,And AROON>0,Indicates the formation of an upward trend, generating a buy signal; 
//(2) when AROON_DOWN Break above 70,And AROON<0,Indicates the formation of a downward trend, generating a sell signal; 
//(3) when AROON_UP Break below 30,And AROON<0,Indicating the Uptrend Weakens, Possible Reversal Downward, Generating Sell Signal; 
//(4) when AROON_DOWN Break below 30,And AROON>0,Indicates that the downtrend is weakening and may reverse upwards, generating a buy signal.*/
	
DCOND1:=CROSSUP(AROON_UP,70) AND AROON>0;//Calculate long position opening condition one
DCOND2:=CROSSDOWN(AROON_DN,30) AND AROON>0;//Calculate long position opening condition two
KCOND1:=CROSSUP(AROON_DN,70) AND AROON<0;//Calculate first short opening
KCOND2:=CROSSDOWN(AROON_UP,30) AND AROON<0;//Calculate second short opening
	
PDCOND1:=AROON>0 AND CROSSDOWN(AROON_UP,50);//Calculate the conditions for closing long positions. When AROON is greater than 0 and AROON_UP a death cross of 50, close long;
PKCOND1:=AROON<0 AND CROSSDOWN(AROON_DN,50);//Calculate the conditions for short closing when AROON is less than 0 and AROON_DN death cross of 50, close the position;

(DCOND1 OR DCOND2) AND BKVOL<=0 AND C>MALONG, BPK(LOTS);//Conditions 1 or 2 for opening a long position are met, and there is no long position, and the price is above the long-term moving average, open a long position;
(KCOND1 OR KCOND2) AND SKVOL<=0 AND C<MALONG, SPK(LOTS);// Short Position Opening Condition: Either condition 1 or 2 is met, there is no existing short position, and the price is below the long-term moving average, then open a short;

PDCOND1,SP(BKVOL);//Close Long Condition
PKCOND1,BP(SKVOL);//Close Short Condition
```

> Detail

https://www.fmz.com/strategy/425796

> Last Modified

2023-09-04 22:33:13
