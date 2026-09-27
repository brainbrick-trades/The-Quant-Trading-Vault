
> Name

Market-Making-Strategy-of-Grabbing-the-Market-Position-High-Frequency-Approaching-Type

> Author

Zero

> Strategy Description

Market making strategy, the most basic market-making strategy: buy-sell-one-grab order to capture the market open, earning the price difference between buy and sell. 
For example, if you sell 1 for 60 and buy 1 for 70, this strategy will use 65 as the middle boundary. Below 65, there will be buy orders, and above 65, there will be sell orders. Because the order layout needs to be constantly adjusted, it is temporarily named high-frequency approaching type.
Note: In simulated testing, GetTicker's bid-ask fixed spread is 1.6; actual results need live trading testing.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Interval|2000|Error retry interval (milliseconds)|
|LoopInterval|60|Polling interval (seconds)|
|Step|0.1|Grid interval (yuan))|
|Lot|0.05|Number of lots|
|MaxNets|20|Maximum number of grids|
|DisableLog|false|Close order tracking|
|MinStock|0.01|Minimum trading coin quantity|


> Source (javascript)

``` javascript
function adjustFloat(v) {
    return Math.floor(v*100)/100;
}

function GetOrders() {
    var orders = null;
    while (!(orders = exchange.GetOrders())) {
        Sleep(Interval);
    }
    return orders;
}

function GetAccount() {
    var account;
    while (!(account = exchange.GetAccount())) {
        Sleep(Interval);
    }
    return account;
}

function GetTicker(e) {
    if (typeof(e) == 'undefined') {
        e = exchange;
    }
    var ticker;
    while (!(ticker = e.GetTicker())) {
        Sleep(Interval);
    }
    return ticker;
}

function updateProfit(accountInit, accountNow, ticker) {
    var netNow = accountNow.Balance + accountNow.FrozenBalance + ((accountNow.Stocks + accountNow.FrozenStocks) * ticker.Buy);
    var netInit = accountInit.Balance + accountInit.FrozenBalance + ((accountInit.Stocks + accountInit.FrozenStocks) * ticker.Buy);
    LogProfit(adjustFloat(netNow - netInit));
}

var InitAccount = null;
var LastOrdersLength = null;

function onTick() {
    var ticker = GetTicker();
    var account = GetAccount();
    var orders = GetOrders();
    if (LastOrdersLength != null && LastOrdersLength != orders.length) {
        updateProfit(InitAccount, account, ticker);
    }
    LastOrdersLength = orders.length;
    
    var mid = adjustFloat(ticker.Buy + ((ticker.Sell - ticker.Buy) / 2));
    var numBuy = parseInt(Math.min(MaxNets / 2 , (mid - ticker.Buy) / Step, account.Balance / ticker.Buy / Lot));
    var numSell = parseInt(Math.min(MaxNets / 2, account.Stocks / Lot));
    var num = Math.max(numBuy, numSell);
    var ordersKeep = [];
    var queue = [];
    for (var i = 1; i < num; i++) {
        var buyPrice = adjustFloat(mid - (i * Step));
        var sellPrice = adjustFloat(mid + (i * Step));
        var alreadyBuy = false;
        var alreadySell = false;
        for (j = 0; j < orders.length; j++) {
            if (orders[j].Type == ORDER_TYPE_BUY) {
                if (Math.abs(orders[j].Price - buyPrice) < (Step / 2)) {
                    alreadyBuy = true;
                    ordersKeep.push(orders[j].Id);
                }
            } else {
                if (Math.abs(orders[j].Price - sellPrice) < (Step / 2)) {
                    alreadySell = true;
                    ordersKeep.push(orders[j].Id);
                }
            }
        }
        if ((!alreadyBuy) && (i < numBuy)) {
            queue.push([buyPrice, ORDER_TYPE_BUY]);
        }
        if ((!alreadySell) && (i < numSell)) {
            queue.push([sellPrice, ORDER_TYPE_SELL]);
        }
    }

    for (var i = 0; i < orders.length; i++) {
        var keep = false;
        for (var j = 0; j < ordersKeep.length; j++) {
            if (orders[i].Id == ordersKeep[j]) {
                keep = true;
            }
        }
        if (!keep) {
            exchange.CancelOrder(orders[i].Id);
            LastOrdersLength--;
        }
    }

    for (var i = 0; i < queue.length; i++) {
        if (queue[i][1] == ORDER_TYPE_BUY) {
            exchange.Buy(queue[i][0], Lot);
        } else {
            exchange.Sell(queue[i][0], Lot);
        }
        LastOrdersLength++;
    }
}

function main() {
    if (DisableLog) {
        EnableLog(false);
    }
    InitAccount = GetAccount();
    Log(InitAccount);
    LoopInterval = Math.max(LoopInterval, 1);
    Lot = Math.max(MinStock, Lot);
    while (true) {
        onTick();
        Sleep(LoopInterval * 1000);
    }
}
```

> Detail

https://www.fmz.com/strategy/348

> Last Modified

2018-06-05 16:24:29
