
> Name

Flash-Crash-Robot-Teaching

> Author

发明者量化-小小梦



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Spread|50|Order price interval|
|OrderSize|0.1|Order Size|
|SpreadTimes|true|Order size increment multiplier|
|TotalBuy|3|Total Buy Orders|
|TotalSell|3|Total Sell Orders|
|Interval|300|Dormant Time(ms)|
|fee|0.25|trading fee|


> Source (javascript)

``` javascript
function CancelPendingOrders(orders) {                             // Cancel All Orders
    for (var j = 0; j < orders.length; j++) {                      // cancel orders one by one according to the array of unfinished orders passed by parameters.
        exchange.CancelOrder(orders[j].Id, orders[j]);
        Sleep(300);                                                // Interval 300 milliseconds
    }
}
function LogOrders(orders){                                        // Organizes the data to be displayed, shown in the status bar on the Robot page.
    var buyString = '';                                            // String of buy order data for display
    var sellString = '';                                           // String of sell order data for display
    orders.sort(function(x, y){return x.Price - y.Price;});        // Sort , orders According to the order Price Attribute, from large to small
    for (var j = 0; j < orders.length; j++) {                      // Iterate orders  , Note that it has been sorted
        if (orders[j].Type == ORDER_TYPE_SELL){                    // If the order is a sell order, then execute{} Internal code.
            sellString += String(orders[j].Price) + ' ' + String(orders[j].Amount) + '｜';    // Stored in string sellString , Use | Interval
        }else{
            buyString += String(orders[j].Price) + ' ' + String(orders[j].Amount) + '｜';     // Stored in string buyString , Use | Interval
        }
    }
    LogStatus('Buy Order:' + buyString + '\n' + 'Sell Order:' + sellString);                             // Output these order details in the status bar.
}
function main() {                                           // Main Function
    while(true){                                            // Main loop
        var orders = _C(exchange.GetOrders);                // Get all uncompleted order information,orders Is an array.
        CancelPendingOrders(orders);                        // Cancel all outstanding pending orders
        var ticker = _C(exchange.GetTicker);                // Get the latest market information
        var account = _C(exchange.GetAccount);              // Get current account information
        var midPrice = (ticker.Buy + ticker.Sell) / 2;      // Calculate the price at the middle of the order book gap.
        var buyAmount  = 0;                                 // Statement buyAmount ,Used to accumulate the planned purchase quantity, initialize 0
        var sellAmount = 0;                                 // Statement sellAmount , is used to accumulate the planned selling quantity, initialized 0
        var amount = OrderSize;                             // OrderSize Order quantity per transaction, assigned to amount
        var buyPrice = midPrice  - Spread;                  // Place orders at certain price intervals above and below the middle of the order book, set the buy order price buyPrice
        var sellPrice = midPrice + Spread;                  // ....
        while((buyAmount < TotalBuy) && (account.Balance > amount*buyPrice) && buyPrice > 0){       // When the planned purchase quantity is less than the total purchase amount, and the available pricing currency (funds) in the account is greater than the funds used for this planned order, and the order price is greater than 0 (to prevent midPrice - Spread from being less than0)
            if(exchange.Buy(buyPrice, amount)){             // Place order, if returns null Execute else Inside the code block, if returnedid Execute if Code block
                buyAmount += amount;                        // Accumulated buy order volume
                account.Balance -= amount*buyPrice;         // Update account currency quantity
                buyPrice -= Spread;                         // Update order price
                amount = amount * SpreadTimes;              // Update order quantity, increment according to the parameter SpreadTimes setting.
            
            }else{                                          // Order failed, update account information for current while loop condition judgment
                account = _C(exchange.GetAccount);
            }
            Sleep(500);                                     // Used to control the frequency of pending orders
        }
        amount = OrderSize;                                 // Reset the amount variable to OrderSize
        while((sellAmount < TotalSell) && (account.Stocks*(1-fee/100) > amount)){        // When the planned selling amount is less than the total selling order amount, and the number of coins available in the account after deducting the transaction fee is greater than the number of each order, execute the while loop
            if(exchange.Sell(sellPrice, amount)){           // Place a sell order and return to the orderID ,Update relevant variables.
                sellAmount += amount;                       // Accumulated quantity of sell orders posted
                account.Stocks -= amount;                   // Update available coin amount
                sellPrice += Spread;                        // Update order price position
                amount = amount * SpreadTimes;              // Update order quantity, increment according to the parameter SpreadTimes setting.
            }else{
                account = _C(exchange.GetAccount);          // If placing the order fails, update account information
            }
            Sleep(500);
        }
        orders = _C(exchange.GetOrders);                    // Get order information
        LogOrders(orders);                                  // Output pending order information in the status bar
        Sleep(Interval*1000);                               // Polling interval, controls the strategy operation frequency
    }
}
```

> Detail

https://www.fmz.com/strategy/118939

> Last Modified

2021-01-15 17:41:59
