
> Name

Quantitative-Typing-Rate-Trading-Strategy-by-Boyu-Quantification

> Author

homily



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|len|35|len|


> Source (MyLanguage)

``` pascal
(*backtest
start: 2019-01-01 00:00:00
end: 2021-01-31 00:00:00
period: 1h
exchanges: [{"eid":"Futures_OKCoin","currency":"BTC_USD","fee":[0.05,0.05]}]
args: [["TradeAmount",200,126961],["ContractType","quarter",126961]]
*)

//len:=35;//Design number of cycles
liang:=INTPART(MONEYTOT*REF(C,1)/100)*0.5;

hh^^HHV(H,len);//Take the highest price within a certain period
ll^^LLV(L,len);//Take the lowest price within a certain period
hl2^^(hh+ll)/2;//Average of the highest price and lowest price
avg^^MA(hl2,5);//Calculate the smoothed moving average for the mean value

ss:SLOPE(avg,len);// Calculate the regression slope for the moving average

ss<REF(ss,1),SPK(liang*2);//When the slope decreases, it indicates weakening market momentum, with a downward trend; close long positions and go short
ss>REF(ss,1),BPK(liang);//When the slope increases, it indicates that market momentum is continuously rising, showing an upward trend. Close short positions and go long.
AUTOFILTER;



```

> Detail

https://www.fmz.com/strategy/183416

> Last Modified

2021-02-08 13:47:31
