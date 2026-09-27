
> Name

Timed-Order-Cancellation

> Author

亚瑟d

> Strategy Description

Timed Order Cancellation

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|LoopInterval|30|Polling interval (minutes)|


> Source (javascript)

``` javascript
// Backtesting Environment
/*backtest
start: 2018-01-01 00:00:00
end: 2018-08-01 11:00:00
period: 1m
exchanges: [{"eid":"Bitfinex","currency":"BTC_USD"}]
*/



// Cancel Order Function
function CancelPendingOrders() {
    Sleep(1000); // Sleep for 1 second
    var ret = false;
    while (true) {
        var orders = null;
        // Continuously fetch the array of unexecuted orders; if an exception is returned, continue fetching
        while (!(orders = exchange.GetOrders())) {
            Sleep(1000); // Sleep for 1 second
        }
        if (orders.length == 0) { // If the order array is empty
            return ret; // Return to order cancellation status
        }
        for (var j = 0; j < orders.length; j++) { // Iterate through the array of unfilled orders
            exchange.CancelOrder(orders[j].Id); // Cancel unfilled orders one by one
            ret = true;
            if (j < (orders.length - 1)) {
                Sleep(1000); // Sleep for 1 second
            }
        }
    }
}


// Main Function
function main() {
    while (true) { // Polling Mode
            CancelPendingOrders(); // Cancel unfilled orders
            Log(_C(exchange.GetAccount)); // Print current account information
        Sleep(LoopInterval * 60000); // Hibernate
    }
}
```

> Detail

https://www.fmz.com/strategy/284760

> Last Modified

2021-05-25 18:15:28
