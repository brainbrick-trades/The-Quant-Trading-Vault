
> Name

Iceberg-Order-Buy

> Author

Zero

> Strategy Description

Iceberg order means that when investors conduct large-amount transactions, in order to avoid excessive impact on the market, the large order is automatically split into multiple orders, and small orders are automatically placed based on the current latest buy/sell price and the price strategy set by the customer. When the previous order is fully completed or the latest price deviates significantly from the current order price, the order is automatically re-entered.
example:
If the single average fluctuation points are set to 10 then:
The quantity of each order is 90% to 110% of the average value of a single order, and the order price is the latest buying price * (1 - order depth). A new order will be placed after all the previous orders are completed. When the latest transaction price is more than the order depth * 2 from the order, the order will be automatically canceled and the order will be re-entrusted. Stop placing orders when the strategy's total trading volume equals its total order quantity. Stop the order when the latest transaction price of the market is higher than the highest bid price, and resume the order when the latest transaction price is lower than the highest bid price again.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|TotalBuyNet|10000|Total purchase amount (yuan))|
|AvgBuyOnce|100|Average quantity per purchase (CNY))|
|FloatPoint|10|Single average floating point number (percentage)|
|EntrustDepth|0.1|Order depth (percentage)|
|MaxBuyPrice|20000|Highest buy price (yuan)|
|Interval|1000|Retry on failure (milliseconds))|
|MinStock|0.0001|Minimum transaction volume|
|LoopInterval|true|Price polling interval (seconds)|


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

var LastBuyPrice = 0;
var InitAccount = null;

function dispatch() {
    var account = null;
    var ticker = _C(exchange.GetTicker);
    // The distance between the latest transaction price and the order exceeds the order depth.*2Automatically cancel the order and place a new one
    if (LastBuyPrice > 0) {
        // Order not completed
        if (_C(exchange.GetOrders).length > 0) {
            if (ticker.Last > LastBuyPrice && ((ticker.Last - LastBuyPrice) / LastBuyPrice) > (2*(EntrustDepth/100))) {
                Log('Deviated too much, Latest transaction price:', ticker.Last, 'order price', LastBuyPrice);
                CancelPendingOrders();
            } else {
                return true;
            }
        } else {
            account = _C(exchange.GetAccount);
            Log("Buy order completed, Total cost:", _N(InitAccount.Balance - account.Balance), "Average buying price:", _N((InitAccount.Balance - account.Balance) / (account.Stocks - InitAccount.Stocks)));
        }
        LastBuyPrice = 0;
    }
    
    
    // Order price is the latest buy1price*(1-Commission Depth)
    var BuyPrice = _N(ticker.Buy * (1 - EntrustDepth/100));
    if (BuyPrice > MaxBuyPrice) {
        return true;
    }
    
    if (!account) {
        account = _C(exchange.GetAccount);
    }


    if ((InitAccount.Balance - account.Balance) >= TotalBuyNet) {
        return false;
    }
    
    var RandomAvgBuyOnce = (AvgBuyOnce * ((100 - FloatPoint) / 100)) + (((FloatPoint * 2) / 100) * AvgBuyOnce * Math.random());
    var UsedMoney = Math.min(account.Balance, RandomAvgBuyOnce, TotalBuyNet - (InitAccount.Balance - account.Balance));
    
    var BuyAmount = _N(UsedMoney / BuyPrice);
    if (BuyAmount < MinStock) {
        return false;
    }
    LastBuyPrice = BuyPrice;
    exchange.Buy(BuyPrice, BuyAmount, 'Cost: ', _N(UsedMoney), 'Last transaction price', ticker.Last);
    return true;
}

function main() {
    if (exchange.GetName().indexOf('Futures_') != -1) {
        throw "Spot only supported";
    }
    CancelPendingOrders();
    InitAccount = _C(exchange.GetAccount);
    Log(InitAccount);
    if (InitAccount.Balance < TotalBuyNet) {
        throw "Insufficient account balance";
    }
    LoopInterval = Math.max(LoopInterval, 1);
    while (dispatch()) {
        Sleep(LoopInterval * 1000);
    }
    Log("All commissions completed", _C(exchange.GetAccount));
}

```

> Detail

https://www.fmz.com/strategy/236

> Last Modified

2020-03-08 12:21:25
