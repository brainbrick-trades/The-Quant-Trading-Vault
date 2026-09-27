
> Name

Get-Weekly-K-Line

> Author

数·狂

> Strategy Description

Combine daily candlesticks into weekly candlesticks, with the default week starting on Sunday (adjustable).).

Usage Method:
$.GetRecordsWeek(exchange)

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|weekStarts|0|The week starts on: Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|


> Source (javascript)

``` javascript
$.GetRecordsWeek = function(exchange) {
    var rec1 = exchange.GetRecords(PERIOD_D1);
    if (!rec1) return null;
    if (rec1.length === 0) return [];
    var recN = [];
    var tmp = {
        Time: rec1[0].Time,
        Open: rec1[0].Open,
        High: rec1[0].High,
        Low: rec1[0].Low,
        Close: rec1[0].Close,
        Volume: rec1[0].Volume
    };
    for (var i = 1; i < rec1.length; i++) {
        if (Math.floor((rec1[i].Time / 86400000 - 3 - weekStarts + 1/3) / 7 + 1e-6) > Math.floor((rec1[i-1].Time / 86400000 - 3 - weekStarts - 1/3) / 7 + 1e-6)) { // new week
            recN.push({
                Time: tmp.Time,
                Open: tmp.Open,
                High: tmp.High,
                Low: tmp.Low,
                Close: tmp.Close,
                Volume: tmp.Volume
            });
            tmp.Time = rec1[i].Time;
            tmp.Open = rec1[i].Open;
            tmp.High = rec1[i].High;
            tmp.Low = rec1[i].Low;
            tmp.Close = rec1[i].Close;
            tmp.Volume = rec1[i].Volume;
        } else if (tmp.Time) { // same week
            tmp.High = Math.max(tmp.High, rec1[i].High);
            tmp.Low = Math.min(tmp.Low, rec1[i].Low);
            tmp.Close = rec1[i].Close;
            tmp.Volume += rec1[i].Volume;
        }
    }
    recN.push({
        Time: tmp.Time,
        Open: tmp.Open,
        High: tmp.High,
        Low: tmp.Low,
        Close: tmp.Close,
        Volume: tmp.Volume
    });
    return recN;
};

function main() {
    var rec = $.GetRecordsWeek(exchange);
    Log(new Date(rec[rec.length-1].Time).toString());
}
```

> Detail

https://www.fmz.com/strategy/20226

> Last Modified

2016-08-17 18:22:52
