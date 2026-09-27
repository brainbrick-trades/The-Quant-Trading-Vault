
> Name

Market-Making-Strategy-of-Seizing-the-Market-Counterattack

> Author

Zero

> Strategy Description

Market making strategy, the most basic market-making strategy: buy-sell-one-grab order to capture the market open, earning the price difference between buy and sell.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Interval|2000|Error retry interval (milliseconds)|
|LoopInterval|true|Polling interval (seconds)|
|SlidePrice|0.01|slippage|
|MaxDiff|0.8|Minimum spread on the market|
|Lot|0.2|Number of lots|
|MinStock|0.0001|Minimum transaction volume|


> Source (javascript)

``` javascript

function CancelPendingOrders(orderType) {
    while (true) {
        var orders = _C(exchange.GetOrders);
        var count = 0;
        if (typeof(orderType) != 'undefined') {
            for (var i = 0; i < orders.length; i++) {
                if (orders[i].Type == orderType) {
                    count++;
                }
            }
        } else {
            count = orders.length;
        }
        if (count == 0) {
            return;
        }

        for (var j = 0; j < orders.length; j++) {
            if (typeof(orderType) == 'undefined' || (orderType == orders[j].Type)) {
                exchange.CancelOrder(orders[j].Id, orders[j]);
                if (j < (orders.length-1)) {
                    Sleep(Interval);
                }
            }
        }
    }
}


function updateProfit(accountInit, accountNow, ticker) {
    var netNow = accountNow.Balance + accountNow.FrozenBalance + ((accountNow.Stocks + accountNow.FrozenStocks) * ticker.Buy);
    var netInit = accountInit.Balance + accountInit.FrozenBalance + ((accountInit.Stocks + accountInit.FrozenStocks) * ticker.Buy);
    LogProfit(netNow - netInit);
}

var InitAccount = null;
var LastBuyPrice = 0;
var LastSellPrice = 0;

function onTick() {
    var ticker = _C(exchange.GetTicker);
    var BuyPrice = ticker.Buy + SlidePrice;
    var SellPrice = ticker.Sell - SlidePrice;

    // Profit Disappears
    if ((SellPrice - BuyPrice) <= MaxDiff) {
        CancelPendingOrders();
        return;
    }
  
    var cancelType = null;
    
    if (LastBuyPrice > 0 && (ticker.Buy - LastBuyPrice) > SlidePrice) {
        cancelType = ORDER_TYPE_BUY;
    }
    
    if (LastSellPrice > 0 && (LastSellPrice - ticker.Sell) > SlidePrice) {
        if (cancelType == null) {
            cancelType = ORDER_TYPE_SELL;
        } else {
            cancelType = -1;
        }
    }
    
    if (cancelType == -1) {
        CancelPendingOrders();
    } else if (cancelType != null) {
        CancelPendingOrders(cancelType);
    }

    var orders = _C(exchange.GetOrders);
    if (orders.length == 2) {
        return;
    }
    var account = _C(exchange.GetAccount);
    var amountBuy = _N(Math.min(account.Balance / BuyPrice, Lot));
    var amountSell = Math.min(account.Stocks, Lot);

    if (amountBuy >= MinStock) {
        if (orders.length == 0 || orders[0].Type == ORDER_TYPE_SELL) {
            if (orders.length > 0) {
                updateProfit(InitAccount, account, ticker);
            }
            exchange.Buy(BuyPrice, amountBuy);
            LastBuyPrice = BuyPrice;
        }
    }
    if (amountSell >= MinStock) {
        if (orders.length == 0 || orders[0].Type == ORDER_TYPE_BUY) {
            if (orders.length > 0) {
                updateProfit(InitAccount, account, ticker);
            }
            exchange.Sell(SellPrice, amountSell);
            LastSellPrice = SellPrice;
        }
    }
}

function onexit() {
    CancelPendingOrders();
}

function main() {
    InitAccount = _C(exchange.GetAccount);
    Log(InitAccount);
    SetErrorFilter("502:|503:|unexpected|network|timeout|WSARecv|Connect|GetAddr|no such|reset|received|EOF");
    exchange.SetRate(1);
    LoopInterval = Math.max(LoopInterval, 1);
    Lot = Math.max(MinStock, Lot);
    while (true) {
        onTick();
        Sleep(LoopInterval * 1000);
    }
}

```

> Detail

https://www.fmz.com/strategy/304

> Last Modified

2018-03-27 16:28:46
