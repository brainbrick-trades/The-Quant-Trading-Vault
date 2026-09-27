
> Name

Classic-Moving-Average-Strategy

> Author

Zero

> Strategy Description

"Talk is cheap. Show me the code"

For teaching purposes, use with caution in real trading.


Note: ` Strategy uses a trading template library`

`I hope that novices can get started with this strategy, learn to write strategies step by step, and experience the impact of simulation and real environments on the trading system.`

https://dn-filebox.qbox.me/fb4d0c7d773ca83e9d0230927705d419dc0bbeaa.png

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|FastPeriod|5|Market Entry Express Cycle|
|SlowPeriod|15|Slow market entry cycle|
|EnterPeriod|2|Market Entry Observation Period|
|ExitFastPeriod|7|Exit express cycle|
|ExitSlowPeriod|15|Exit slow cycle|
|ExitPeriod|true|Market Exit Observation Period|
|PositionRatio|0.8|Position ratio|
|StopLossRatio|0.05|Stop loss ratio|
|Interval|10|Polling interval (seconds))|


> Source (javascript)

``` javascript
/*backtest
start: 2019-01-01 00:00:00
end: 2019-07-01 00:00:00
period: 1d
exchanges: [{"eid":"Bitfinex","currency":"BTC_USD"}]
*/

function main() {
    var STATE_IDLE  = -1;
    var state = STATE_IDLE;
    var entryPrice = 0;
    var initAccount = _C(exchange.GetAccount);
    Log(initAccount);
    while (true) {
        if (state === STATE_IDLE) {
            var n = $.Cross(FastPeriod, SlowPeriod);
            if (Math.abs(n) >= EnterPeriod) {
                var account = _C(exchange.GetAccount);
                var ticker = _C(exchange.GetTicker);
                var obj = n > 0 ? $.Buy(_N(account.Balance * PositionRatio / ticker.Sell, 3)) : $.Sell(_N(account.Stocks * PositionRatio, 3));
                if (obj) {
                    opAmount = obj.amount;
                    entryPrice = obj.price;
                    state = n > 0 ? PD_LONG : PD_SHORT;
                    Log("Open position details", obj, "Cross period", n);
                }
            }
        } else {
            var n = $.Cross(ExitFastPeriod, ExitSlowPeriod);
            var needCover = Math.abs(n) >= ExitPeriod && ((state === PD_LONG && n < 0) || (state === PD_SHORT && n > 0));
            if (needCover) {
                Log("Close the position after exiting the market");
            } else {
                var ticker = _C(exchange.GetTicker);
                if (state === PD_LONG) {
                    if (ticker.Buy < entryPrice*(1-StopLossRatio)) {
                        needCover = true;
                        Log("Stop loss and close position");
                    }
                } else {
                    if (ticker.Sell > entryPrice*(1+StopLossRatio)) {
                        needCover = true;
                        Log("Stop loss and close position");
                    }
                }
            }
            if (needCover) {
                var nowAccount = _C(exchange.GetAccount);
                var obj = state === PD_LONG ? $.Sell(_N(nowAccount.Stocks - initAccount.Stocks, 3)) : $.Buy(_N(initAccount.Stocks - nowAccount.Stocks, 3));
                state = STATE_IDLE;
                nowAccount = _C(exchange.GetAccount);
                LogProfit(nowAccount.Balance - initAccount.Balance, 'Money:', nowAccount.Balance, 'Coins:', nowAccount.Stocks, 'Close details:', obj, "Cross cycle", n);
            }
        }
        Sleep(Interval*1000);
    }
}
```

> Detail

https://www.fmz.com/strategy/12348

> Last Modified

2019-10-08 17:00:12
