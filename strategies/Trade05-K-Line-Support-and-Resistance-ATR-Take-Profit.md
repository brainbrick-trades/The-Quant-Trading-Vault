
> Name

Trade05-K-Line-Support-and-Resistance-ATR-Take-Profit

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
|LENTH|250|LENTH|
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


ATRS:=50;

//Trading volume 
//LOTS:=MAX(1,INTPART(percent/100*MONEY/(C*MARGIN*UNIT)));//Gold principal
LOTS:=MAX(1,INTPART(percent/100*MONEY*C/(MARGIN*UNIT)));//Coin principal

// Calculate CurrentKWeighted average of lines, resistance lines and support lines
AVGP:=(HIGH + LOW + (CLOSE * 2)) / 4;
RS^^HHV((AVGP * 2) - LOW,LENTH);
ST^^LLV((AVGP * 2) - HIGH,LENTH);

	// CalculationATR
TR:=MAX(MAX((HIGH-LOW),ABS(REF(CLOSE,1)-HIGH)),ABS(REF(CLOSE,1)-LOW));
ATRVAL:=MA(TR,LENTH);
	

	// Open Position
IF BKVOL<=1 AND HIGH >= REF(RS,1) AND VOL > 0 THEN BEGIN
		1,BPK(LOTS);
END
IF SKVOL<=1 AND LOW <= REF(ST,1) AND VOL > 0  THEN BEGIN
		1,SPK(LOTS);
END
	
	
// Determine entry based on openingBARofATRCalculate take-profit price
IF BKVOL>0 AND BARSBK>0 THEN BEGIN

MYEXITPRICE:=BKPRICE + ATRVAL * ATRS;

END
IF SKVOL>0 AND BARSSK>0 THEN BEGIN

MYEXITPRICE:=SKPRICE - ATRVAL * ATRS;

END
		
	// Close Position
IF BKVOL>0 AND BARSBK>0 AND VOL>0 THEN BEGIN
		// Take Profit Exit
		IF HIGH >= MYEXITPRICE THEN BEGIN
		1,SP(LOTS);
		END
END
	
IF SKVOL>0 AND BARSSK>0 AND VOL>0 THEN BEGIN
		// Take Profit Exit
		IF LOW <= MYEXITPRICE THEN BEGIN
		1,BP(LOTS);
		END
END
```

> Detail

https://www.fmz.com/strategy/425800

> Last Modified

2023-09-04 22:33:45
