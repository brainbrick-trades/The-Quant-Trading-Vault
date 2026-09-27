
> Name

Martingale-Test

> Author

Zer3192





> Source (javascript)

``` javascript
// Martingale strategy
var baseAmount = 0.001; // Initial order quantity
var martingaleFactor = 1.01; // Scaling Factor
var maxOrders = 100; // Maximum number of orders
var currentOrders = 0; // Current number of orders
var currentAmount = baseAmount; // Current order quantity

function main() {
    while (true) {
        var ticker = exchange.GetTicker();
        var price = ticker.Last;
        var buyPrice = price - 1000; // Set the buy price to current price minus1
        var sellPrice = price + 500; // Set the sell price to current price plus1
        if (currentOrders < maxOrders) {
            // Place Order
            if (currentOrders % 2 == 0) {
                // Place an even number of orders to buy
                var orderId = exchange.Buy(buyPrice, currentAmount);
                if (orderId) {
                    currentOrders++;
                    currentAmount *= martingaleFactor;
                }
            } else {
                // Place an odd number of orders to sell
                var orderId = exchange.Sell(sellPrice, currentAmount);
                if (orderId) {
                    currentOrders++;
                    currentAmount *= martingaleFactor;
                }
            }
        } else {
            // Reached the maximum number of order attempts, exit the loop
            break;
        }
        Sleep(1000); // Wait 1 second
    }
}
```

> Detail

https://www.fmz.com/strategy/416879

> Last Modified

2023-06-09 18:04:23
