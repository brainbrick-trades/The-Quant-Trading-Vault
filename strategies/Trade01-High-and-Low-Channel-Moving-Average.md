
> Name

Trade01-High-and-Low-Channel-Moving-Average

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
|LENGE|260|LENGE|
|percent|5|percent|


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

VARIABLE:LOWERAFTERENTRY:0;
VARIABLE:HIGHERAFTERENTRY:0;
VARIABLE:MYPRICE2:0;
VARIABLE:MYPRICE3:0;

TRS:=60; //Trailing stop ratio.	

// Indicator calculation
//Trading volume 
//LOTS:=MAX(1,INTPART(percent/100*MONEY/(C*MARGIN*UNIT)));//Gold principal
LOTS:=MAX(1,INTPART(percent/100*MONEY*C/(MARGIN*UNIT)));//Coin principal

MA1:=EMA(REF(C,1),240);
OPD:=BARSLAST(DATE<>REF(DATE,1))+1;
OO:=VALUEWHEN(OPD=1,O);  
RANGE1:= HIGH - LOW;
UPAVG^^HHV(((REF(HIGH,1)+REF(CLOSE,1))-(2*REF(CLOSE,1)))+OO, LENGE);     
LOWAVG^^LLV(((REF(CLOSE,1)+REF(LOW,1))-(2*REF(CLOSE,1)))+OO, LENGE);      
MEDIANPRICE:= (HIGH + LOW)*0.5;                  
UPBAND^^ MEDIANPRICE > REF(HIGH,1) AND RANGE1 > REF(RANGE1,1); 
DOWNBAND^^MEDIANPRICE < REF(LOW,1) AND RANGE1 > REF(RANGE1,1);  
	// Long Entry
BKVOL <> 1 AND 	REF(C,1)>MA1 AND REF(UPBAND,1) AND REF(CLOSE,1) > REF(UPAVG,1),BPK(LOTS);
IF BKVOL <> 1 AND REF(C,1)>MA1 AND REF(UPBAND,1) AND REF(CLOSE,1) > REF(UPAVG,1) THEN BEGIN
LOWERAFTERENTRY:=LOW;
END
	// Short Entry	
SKVOL <> -1 AND REF(C,1)<MA1 AND REF(DOWNBAND,1) AND REF(CLOSE,1) < REF(LOWAVG,1),SPK(LOTS);  
IF SKVOL <> -1 AND REF(C,1)<MA1 AND REF(DOWNBAND,1) AND REF(CLOSE,1) < REF(LOWAVG,1) THEN BEGIN
HIGHERAFTERENTRY:=HIGH;
END
	


	
 //------------------------------------------------------------------------------------------------
//Record the highest and lowest price after entry
//------------------------------------------------------------------------------------------------

	CLOSELP:=REF(CLOSE,1); 
    IF SKVOL = 1 AND  BKVOL=0 THEN BEGIN
	HIGHERAFTERENTRY:=MIN(HIGHERAFTERENTRY,H);
	END
	IF SKVOL = 1 AND  BKVOL=0 THEN BEGIN
	LOWERAFTERENTRY:=LOWERAFTERENTRY;
    END
	IF BKVOL =1 AND  SKVOL = 0 THEN BEGIN 
	LOWERAFTERENTRY:=MAX(LOWERAFTERENTRY,L);
	END 
	IF BKVOL =1 AND  SKVOL = 0 THEN BEGIN
	HIGHERAFTERENTRY:=HIGHERAFTERENTRY;
	END
	IF BKVOL > 0 OR SKVOL>0 AND BARPOS>0 THEN BEGIN
	HIGHERAFTERENTRY:=MIN(HIGHERAFTERENTRY,REF(HIGH,1));
	LOWERAFTERENTRY:=MAX(LOWERAFTERENTRY, REF(L,1));
	END
		 
		
 	IF  SKVOL=0 AND BKVOL=0 THEN BEGIN  // Adaptive parameter default value;
		LIQKA:= 1;
	END
	IF (SKVOL>0 OR BKVOL>0) THEN BEGIN				 //When there is a position, LIQKA will gradually decrease as the position time increases, that is, the stop loss and take profit range multiplier decreases.
		LIQKA:=LIQKA - 0.1; 
		LIQKA:=MAX(LIQKA,0.5);
	END

	IF BKVOL>0 THEN BEGIN 
	 
	DLIQPOINT:= LOWERAFTERENTRY - (OPEN*TRS/1000)*LIQKA; //After calculation, this chandelier exit line becomes increasingly sensitive as the holding period increases;
	
	END
	IF SKVOL>0 THEN BEGIN
	KLIQPOINT: HIGHERAFTERENTRY + (OPEN*TRS/1000)*LIQKA; //After calculation, this chandelier exit line becomes increasingly sensitive as the holding period increases;

	END
	//------------------------------------------------------------------------------------------------
	//Trailing Stop
	//------------------------------------------------------------------------------------------------
	// When holding a long order, the price falls below the adaptive moving average and close the long order.
 	IF BKVOL >0 AND BARSBK >0   AND C <= DLIQPOINT AND REF(C,1) >= REF(DLIQPOINT,1) AND DLIQPOINT>0 THEN BEGIN
		1,SP(BKVOL);
	END
	// When holding a short order, the price breaks above the adaptive field moving average and the short order is closed.
	IF SKVOL >0 AND BARSSK >0  AND C >= KLIQPOINT AND REF(C,1) <= REF(KLIQPOINT,1) AND KLIQPOINT>0 THEN BEGIN
		1,BP(SKVOL);
	END

```

> Detail

https://www.fmz.com/strategy/425798

> Last Modified

2023-09-04 22:33:31
