
> Name

MyLanguage-Turtle-Strategy-Experience

> Author

Zero

> Strategy Description

> Quick start

* Based on the powerful lower layer of the inventor, it fully supports digital currency spot futures and domestic commodity futures.
* Automatic position rollover, truly reflecting the main contract switching process
* APIDocumentation https://www.fmz.com/bbs-topic/2569

>Language Enhancement

The inventor Quantified not only implemented the interpreter of the Mai language, but also enhanced it to enable mixed programming with the high-level language Javascript. Here is an example

```
%%
// Here you can call any of the inventor's quantifiedAPI 
scope.TEST = function(obj) {
    return obj.val * 100;
}
%%
Closing price:C;
Closing price multiplied by 100:TEST(C);
Magnify the previous closing price 100 times: TEST(REF(C, 1)); // Move the mouse to the candlestick of the backtest and the variable value will be prompted
```

 ![IMG](https://www.fmz.com/upload/asset/7c0bc45baa22107d6f.png)  

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|RATIO|0.01|Funding Ratio|


> Source (MyLanguage)

``` pascal
(*backtest
start: 2020-10-26 00:00:00
end: 2021-10-25 23:59:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Binance","currency":"BTC_USDT"}]
*)

//This demonstration mainly uses the Turtle Trading Rules to demonstrate"Position calculation, maximum position control, and other fund management"Compilation Method of
//In writing demonstrations, only key sentences are annotated; other sentences should be translated by yourself, or customer service may be consulted
//This model is for demonstration purposes only. Enter the market based on this at your own risk.
ATRPERIOD:=20; // ATRFluctuation cycle
SHORTPERIOD:=20; // Short-term Market Entry
LONGPERIOD:= 55; // Long-term Market Entry
VARIABLE:ISLASTFAILURE:=1; // Whether to stop loss and leave the market last time, global variables filter signals
TR:=MAX(MAX((HIGH-LOW),ABS(REF(CLOSE,1)-HIGH)),ABS(REF(CLOSE,1)-LOW));//True amplitude
ATR:MA(TR,ATRPERIOD); //Calculate the simple moving average of the true range over 20 periods, displayed in the attached chart
ZOOM:=IFELSE(ISCONTRACT('@Futures_(?!CTP).*'), CLOSE, 1); // Use digital currency futures as margin
LOT:=((MONEYTOT*RATIO*ZOOM)/(UNIT*ATR))*ZOOM;//Calculate the order quantity based on 1% of equity
TC..IFELSE(ISCONTRACT('@Futures.*'), INTPART(LOT), LOT); // Compatible with futures and spot. ISCONTRACT starting with @ indicates matching the exchange name, supports regex
MTC..4*TC; //Total Position
HH^^HV(H,SHORTPERIOD); // Attached to the main image display
LL^^LV(L,SHORTPERIOD);
HHH^^HV(H,LONGPERIOD);
LLL^^LV(L,LONGPERIOD);
ISEMPTY:=ISLASTBK=0&&ISLASTSK=0;
CROSSUP(C,HH)&&ISEMPTY&&ISLASTFAILURE,BK(TC);//If the latest price exceeds the highest value of the short period, buy to open for the first time, lots set to TC lots
CROSSDOWN(C,LL)&&ISEMPTY&&ISLASTFAILURE,SK(TC); //If the latest price falls below the lowest value of the short period, sell to open for the first time, lots set to TC lots
CROSSUP(C,HHH)&&ISEMPTY,BK(TC);//If the latest price exceeds the highest value of the long period, buy to open for the first time, lots set to TC lots
CROSSDOWN(C,LLL)&&ISEMPTY,SK(TC); //If the latest price falls below the lowest value of the long period, sell to open for the first time, lots set to TC lots
C>=BKPRICE+0.5*ATR&&BKVOL<MTC&&ISLASTBK,BK(TC);//The price increases by 0.5 times ATR based on the last position opened. When the lot size does not exceed 4 times TC, buy and add TC lots.
C<=SKPRICE-0.5*ATR&&SKVOL<MTC&&ISLASTSK,SK(TC);//The price drops by 0.5 times ATR based on the last position opened. When the lot size does not exceed 4 times TC, sell and add TC lots.
NEEDSTOP:=(C<=(BKPRICE-2*ATR)&&BKVOL>0) OR (C>=(SKPRICE+2*ATR)&&SKVOL>0);
NEEDLEAVE:=(CROSSUP(H,HV(H,10))&&SKVOL>0) OR (CROSSDOWN(L,LV(L,10))&&BKVOL>0);
NEEDSTOP OR NEEDLEAVE,CLOSEOUT;
ISLASTFAILURE..IF(NEEDSTOP OR NEEDLEAVE, NEEDSTOP, ISLASTFAILURE);
INFO(NEEDSTOP, 'Stop Loss Exit');
INFO(NEEDLEAVE, 'Successfully exited');
TRADE_AGAIN(10);
MULTSIG(1, 1, 10);
```

> Detail

https://www.fmz.com/strategy/126968

> Last Modified

2021-10-27 12:32:17
