
> Name

Iceberg-Commission-Sell

> Author

Zero

> Strategy Description

Iceberg order means that when investors conduct large-amount transactions, in order to avoid excessive impact on the market, the large order is automatically split into multiple orders, and small orders are automatically placed based on the current latest buy/sell price and the price strategy set by the customer. When the previous order is fully completed or the latest price deviates significantly from the current order price, the order is automatically re-entered.
example:
If the single average fluctuation points are set to 10 then:
The quantity of each order is 90% to 110% of the average value of a single order, and the order price is the latest selling price 1 * (1 + order depth). A new order will be placed after all the previous orders are completed. When the latest transaction price is more than the order depth * 2 from the order, the order will be automatically canceled and the order will be re-entrusted. Stop placing orders when the strategy's total trading volume equals its total order quantity. Stop the order when the latest transaction price of the market is lower than its lowest selling price, and resume the order when the latest transaction price is higher than the lowest selling price again.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|TotalSellStocks|10|Total quantity sold (coins))|
|AvgSellOnce|0.3|Average quantity per sale (Coin))|
|FloatPoint|10|Single average floating point number (percentage)|
|EntrustDepth|0.1|Order depth (percentage)|
|MinSellPrice|3800|Lowest sell price (yuan)|
|Interval|1000|Retry on failure (milliseconds))|
|MinStock|0.0001|Minimum transaction volume|
|LoopInterval|300|Price polling interval (milliseconds)|


> Source (javascript)

``` javascript


function CancelPendingOrders() {
    while (true) {
        var orders = _C(exchange.GetOrders);
        if (orders.length == 0) {
            return;
        }

        for (var j = 0; j < orders.length; j++) {
            exchange.CancelOrder(orders[j].Id);
            if (j < (orders.length-1)) {
                Sleep(Interval);
            }
        }
    }
}

var LastSellPrice = 0;
var InitAccount = null;

function dispatch() {
    var account = null;
    var ticker = _C(exchange.GetTicker);
    // The distance between the latest transaction price and the order exceeds the order depth.*2Automatically cancel the order and place a new one
    if (LastSellPrice > 0) {
        // Order not completed
        if (_C(exchange.GetOrders).length > 0) {
            if (ticker.Last < LastSellPrice && ((LastSellPrice - ticker.Last) / ticker.Last) > (2*(EntrustDepth/100))) {
                Log('Deviated too much, Latest transaction price:', ticker.Last, 'order price', LastSellPrice);
                CancelPendingOrders();
            } else {
                return true;
            }
        } else {
            account = _C(exchange.GetAccount);
            Log("Sell order completed, Total sold:", _N(InitAccount.Stocks - account.Stocks), "Average selling price:", _N((account.Balance - InitAccount.Balance) / (InitAccount.Stocks - account.Stocks))); }
            LastSellPrice = 0;
    }

    // Order price is the latest sell1price*(1+Commission Depth)
    var SellPrice = _N(ticker.Sell * (1 + EntrustDepth/100));
    if (SellPrice < MinSellPrice) {
        return true;
    }

    if (!account) {
        account = _C(exchange.GetAccount);
    }


    if ((InitAccount.Stocks - account.Stocks) >= TotalSellStocks) {
        return false;
    }

    var RandomAvgSellOnce = (AvgSellOnce * ((100 - FloatPoint) / 100)) + (((FloatPoint * 2) / 100) * AvgSellOnce * Math.random());
    var SellAmount = Math.min(TotalSellStocks - (InitAccount.Stocks - account.Stocks), RandomAvgSellOnce);
    if (SellAmount < MinStock) {
        return false;
    }
    LastSellPrice = SellPrice;
    exchange.Sell(SellPrice, SellAmount, 'Last transaction price', ticker.Last);
    return true;
}

function main() {
    if (exchange.GetName().indexOf('Futures_') != -1) {
        throw "Spot only supported";
    }
    CancelPendingOrders();
    InitAccount = _C(exchange.GetAccount);
    Log(InitAccount);
    if (InitAccount.Stocks < TotalSellStocks) {
        throw "Insufficient coins in the account";
    }
    LoopInterval = Math.max(LoopInterval, 1);
    while (dispatch()) {
        Sleep(LoopInterval);
    }
    Log("All commissions completed", _C(exchange.GetAccount));
}


```

> Detail

https://www.fmz.com/strategy/241

> Last Modified

2020-03-06 19:47:44
