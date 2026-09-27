
> Name

Single-Platform-Equilibrium-Strategy

> Author

Zero

> Strategy Description

This requires opening a position. For example, the account has 5,000 yuan and 1 coin. If the value of the coin is greater than the account balance of 5,000 and the price difference exceeds the threshold, for example, the currency is now worth 6,000 yuan, sell it (600 0-5000)/6000/2 coins, it means the currency has appreciated, exchange the money back. If the currency has depreciated, for example, 4000 yuan, buy (5000-4000)/4000/2 coins, When the currency falls, buy some back, and if it rises again, sell it again. It's like a balance, with different hedging on both sides, so I named it a balanced strategy.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|threshold|0.05|Threshold|
|Interval|2000|Error retry interval (milliseconds)|
|LoopInterval|60|Polling interval (seconds)|
|MinStock|0.001|Minimum transaction volume|
|XPrecision|4|quantity precision|
|ZPrecision|8|Price Precision|


> Source (javascript)

``` javascript
/*backtest
start: 2018-03-01 00:00:00
end: 2018-08-01 11:00:00
period: 15m
exchanges: [{"eid":"OKCoin_EN","currency":"BTC"}]
*/

function CancelPendingOrders() {
    var ret = false;
    while (true) {
        var orders = null;
        while (!(orders = exchange.GetOrders())) {
            Sleep(Interval);
        }

        if (orders.length == 0) {
            return ret;
        }

        for (var j = 0; j < orders.length; j++) {
            exchange.CancelOrder(orders[j].Id);
            ret = true;
            if (j < (orders.length-1)) {
                Sleep(Interval);
            }
        }
    }
    return ret;
}

var InitAccount = null;

function onTick() {
    var acc = _C(exchange.GetAccount);
    var ticker = _C(exchange.GetTicker);
    var spread = ticker.Sell - ticker.Buy;
    var diffAsset = (acc.Balance - (acc.Stocks * ticker.Sell)) / 2;
    var ratio = diffAsset / acc.Balance;
    LogStatus('ratio:', ratio, _D());
    if (Math.abs(ratio) < threshold) {
        return false;
    }
    if (ratio > 0) {
        var buyPrice = _N(ticker.Sell + spread, ZPrecision);
        var buyAmount = _N(diffAsset / buyPrice, XPrecision);
        if (buyAmount < MinStock) {
            return false;
        }
        exchange.Buy(buyPrice, buyAmount, diffAsset, ratio);
    } else {
        var sellPrice = _N(ticker.Buy - spread, ZPrecision);
        var sellAmount = _N(-diffAsset / sellPrice, XPrecision);
        if (sellAmount < MinStock) {
            return false;
        }
        exchange.Sell(sellPrice, sellAmount, diffAsset, ratio);
    }
    return true;
}

function main() {
    InitAccount = _C(exchange.GetAccount);
    LoopInterval = Math.max(LoopInterval, 1);
    while (1) {
        if (onTick()) {
            Sleep(1000);
            CancelPendingOrders();
            Log(_C(exchange.GetAccount));
        }
        Sleep(LoopInterval * 1000);
    }
}
```

> Detail

https://www.fmz.com/strategy/345

> Last Modified

2018-08-09 12:22:08
