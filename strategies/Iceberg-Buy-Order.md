
> Name

Iceberg-Buy-Order

> Author

小草

> Strategy Description

Iceberg order means that when investors conduct large-amount transactions, in order to avoid excessive impact on the market, the large order is automatically split into multiple orders, and small orders are automatically placed based on the current latest buy/sell price and the price strategy set by the customer. When the previous order is fully completed or the latest price deviates significantly from the current order price, the order is automatically re-entered.
example:
If the single average fluctuation points are set to 10 then:
The quantity of each order is 90% to 110% of the average value of a single order, and the order price is the latest buying price * (1 - order depth). A new order will be placed after all the previous orders are completed. When the latest transaction price is more than the order depth * 2 from the order, the order will be automatically canceled and the order will be re-entrusted. Stop placing orders when the strategy's total trading volume equals its total order quantity. Stop the order when the latest transaction price of the market is higher than the highest bid price, and resume the order when the latest transaction price is lower than the highest bid price again.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|TotalBuyNet|10000|total buy value|
|AvgBuyOnce|100|avg buy value|
|FloatPoint|10|avg price float percent|
|EntrustDepth|0.1|buy depth percent|
|MaxBuyPrice|20000|Highest price to buy|
|Interval|1000|retry time(ms)|
|MinStock|0.0001|Min Stock|
|LoopInterval|true|loop time(second)|


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
    if (LastBuyPrice > 0) {
        if (_C(exchange.GetOrders).length > 0) {
            if (ticker.Last > LastBuyPrice && ((ticker.Last - LastBuyPrice) / LastBuyPrice) > (2*(EntrustDepth/100))) {
                Log('deviate to much, newest last price:', ticker.Last, 'order buy price', LastBuyPrice);
                CancelPendingOrders();
            } else {
                return true;
            }
        } else {
            account = _C(exchange.GetAccount);
            Log("order finised, total cost:", _N(InitAccount.Balance - account.Balance), "avg buy price:", _N((InitAccount.Balance - account.Balance) / (account.Stocks - InitAccount.Stocks)));
        }
        LastBuyPrice = 0;
    }
    
    var BuyPrice = _N(ticker.Buy * (1 - EntrustDepth/100),PricePerision);
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
    
    var BuyAmount = _N(UsedMoney / BuyPrice, 3);
    if (BuyAmount < MinStock) {
        return false;
    }
    LastBuyPrice = BuyPrice;
    exchange.Buy(BuyPrice, BuyAmount, 'Cost: ', _N(UsedMoney), 'last price', ticker.Last);
    return true;
}

function main() {
    CancelPendingOrders();
    InitAccount = _C(exchange.GetAccount);
    Log(InitAccount);
    if (InitAccount.Balance < TotalBuyNet) {
        throw "balance not enough";
    }
    LoopInterval = Math.max(LoopInterval, 1);
    while (dispatch()) {
        Sleep(LoopInterval * 1000);
    }
    Log("All Done", _C(exchange.GetAccount));
}

```

> Detail

https://www.fmz.com/strategy/103319

> Last Modified

2018-07-05 11:10:09
