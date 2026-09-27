
> Name

Random-Number-Martingale-Strategy

> Author

Zer3192





> Source (javascript)

``` javascript
// Random Number Martingale Strategy
// Before each order, determine the order direction and quantity based on a random number

// Set initial capital and order quantity
var initCapital = 10000; // Initial capital
var initAmount = 1; // Initial order quantity

// Set random number range and order ratio
var minRand = 0; // Minimum random number
var maxRand = 100; // Maximum random number
var buyRatio = 0.5; // Buy Ratio
var sellRatio = 0.5; // Sell Ratio

// Define order function
function placeOrder(direction, amount) {
    if (direction == 'buy') {
        exchange.Buy(-1,amount);
    } else if (direction == 'sell') {
        exchange.Sell(-1,amount);
    }
}

// Define main function
function main() {
    var capital = initCapital; // Current funds
    var amount = initAmount; // Current order quantity
    var lastDirection = ''; // Last order direction

    while (true) {
        // Generate random number
        var rand = Math.floor(Math.random() * (maxRand - minRand + 1)) + minRand;

        // Determine the order direction and quantity based on a random number
        var direction = '';
        if (rand <= buyRatio * maxRand) {
            direction = 'buy';
        } else if (rand >= (1 - sellRatio) * maxRand) {
            direction = 'sell';
        }

        if (direction) {
            // Reset the order quantity if the direction changes
            if (direction != lastDirection) {
                amount = initAmount;
            }

            // Place Order
            placeOrder(direction, amount);

            // Update funds and order quantity
            var orderPrice = exchange.GetTicker().Last;
            var orderAmount = amount * orderPrice;
            if (direction == 'buy') {
                capital -= orderAmount;
            } else if (direction == 'sell') {
                capital += orderAmount;
            }
            amount *= 2;

            // Print Log
            Log('Order Direction:', direction, 'Order quantity:', amount, 'Current funds:', capital);

            // Update the direction of the last order
            lastDirection = direction;
        }

        Sleep(1000);
    }
}
```

> Detail

https://www.fmz.com/strategy/416881

> Last Modified

2023-06-09 18:22:17
