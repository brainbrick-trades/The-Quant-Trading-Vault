
> Name

Simple-Application-of-Talib-to-Find-Three-Crows

> Author

Zero





> Source (javascript)

``` javascript
/*backtest
start: 2017-12-05 00:00:00
end: 2017-12-06 12:00:00
period: 5m
exchanges: [{"eid":"OKCoin_EN","currency":"BTC"}]
*/

function main() {
    while (true) {
        var r = exchange.GetRecords();
        var pos = _.indexOf(talib.CDL3BLACKCROWS(r), -100);
        // Identify the Three Black Crows Pattern and Ensure It's the Most Recent OneKLine Formed
        if (pos != -1 && pos == r.length - 1) {
            Log("KLine index:", pos, r.length, "Time:", _D(r[pos].Time));
            // Next Sell Order, These backtest charts will have a buy order symbol
            exchange.Sell(_C(exchange.GetTicker).Buy, 0.1);
            throw "Find three crows";
        }
        Sleep(1000);
    }
}
```

> Detail

https://www.fmz.com/strategy/62163

> Last Modified

2018-04-07 11:47:38
