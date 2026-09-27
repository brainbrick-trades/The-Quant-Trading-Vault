
> Name

Typical-Price-Percentage-Channel-Keltner-and-Percentage-Channel-Variations

> Author

cyberking

> Strategy Description

Typical price percentage channel - Keltner and percentage channel variations.
DX^^EMA((H+L+C)/3,N);  //21Typical price moving average over days 
KRTHR^^EMA(DX,N)*1.05; //21Daily percentage channel upper
KRTXR^^EMA(DX,N)/1.05; //21Daily percentage channel lower



> Source (MyLanguage)

``` pascal
(*backtest
start: 2019-02-09 00:00:00
end: 2020-03-04 00:00:00
period: 1d
exchanges: [{"eid":"Huobi","currency":"BTC_USDT"}]
*)

//ZF:=H-C; //Amplitude
N:=21;
DX^^EMA((H+L+C)/3,N);  //21Typical price moving average over days 
KRTHR^^EMA(DX,N)*1.05; //21Daily percentage channel upper
KRTXR^^EMA(DX,N)/1.05; //21Daily percentage channel lower

C>DX AND (DX<KRTHR),BPK; //Typical upper breakout midline, midline less than upper line
//C>DX AND REF(DX,1)>REF(DX,2),BPK;
C<DX AND (DX>KRTXR),SPK; //Typical lower breakout midline, midline greater than lower line
//C<DX AND REF(DX,1)<REF(DX,2),SPK;
AUTOFILTER;
```

> Detail

https://www.fmz.com/strategy/188507

> Last Modified

2020-03-05 21:36:49
