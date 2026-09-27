
> Name

Tutorial-on-the-Strategy-of-New-Digital-Currency-Spot-Games-and-Grabbing-Coins

> Author

发明者量化-小小梦

> Strategy Description

Related articles:https://www.fmz.com/bbs-topic/9262

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|symbol|null|Monitored trading pair|
|ApiReqInterval|200|apiRequest Interval|
|pendingPrice|-1|Order Price|
|pendingAmount|-1|Pending order volume|
|deltaPrice|-1|Price Change|
|deltaAmount|-1|Order Quantity Change|
|ordersNum|10|Order Quantity|


> Source (javascript)

``` javascript
function pendingOrders(ordersNum, price, amount, deltaPrice, deltaAmount) {
    var routineOrders = []
    var ordersIDs = []
    for (var i = 0 ; i < ordersNum ; i++) {
        var routine = exchange.Go("Buy", price + i * deltaPrice, amount + i * deltaAmount)
        routineOrders.push(routine)
        Sleep(ApiReqInterval)        
    }
    for (var i = 0 ; i < routineOrders.length ; i++) {
        var orderId = routineOrders[i].wait()
        if (orderId) {
            ordersIDs.push(orderId)
            Log("Successfully Placed Order", orderId)
        }        
    }
    return ordersIDs
}

function main() {
    if (symbol == "null" || pendingPrice == -1 || pendingAmount == -1 || pendingPrice == -1 || deltaPrice == -1 || deltaAmount == -1) {
        throw "Parameter setting error"
    }
    exchange.SetCurrency(symbol)
    // Suppress error messages
    SetErrorFilter("GetDepth")
    while (true) {
        var msg = ""
        var depth = exchange.GetDepth()
        if (!depth || (depth.Bids.length == 0 && depth.Asks.length == 0)) {
            // No Depth
            msg = "No depth data, waiting!"
            Sleep(500)
        } else {
            // Obtain Depth
            Log("Concurrent Orders!")
            var ordersIDs = pendingOrders(ordersNum, pendingPrice, pendingAmount, deltaPrice, deltaAmount)
            while (true) {
                var orders = _C(exchange.GetOrders)
                if (orders.length == 0) {
                    Log("Current number of pending orders0,Stop Running")
                    return 
                }
                var tbl = {
                    type: "table",
                    title: "Current pending order",
                    cols: ["id", "Price, Quantity"], 
                    rows: []
                }
                _.each(orders, function(order) {
                    tbl.rows.push([order.Id, order.Price, order.Amount])
                })
                LogStatus(_D(), "\n`" + JSON.stringify(tbl) + "`")
                Sleep(500)
            }
        }
        LogStatus(_D(), msg)
    }
}


```

> Detail

https://www.fmz.com/strategy/358383

> Last Modified

2022-04-20 18:43:33
