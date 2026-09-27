
> Name

Index-Equilibrium-Strategy-Tutorial

> Author

发明者量化-小小梦



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Ratio|0.25|0.25|0.25|Proportion of total assets|
|BaseAsset|BTC|Base Currency|
|ToBuy|0.1|0.1|0.1|Replenishment decline ratio|
|ToSell|0.1|0.1|0.1|Reduction rise ratio|
|Interval|10|Check Interval(s)|
|diff|0.01|Slippage|


> Source (javascript)

``` javascript
var coinValue = {};                             // Declare global variables coinValue  ,Assign an empty object
var totalValue = 0;                             // Total value
function updateValue(){                         // Update value
    var logString = 'Time: '+ _D() + '\n';      // Declare a variable, log string, and initialize the record at the current time
    var account = _C(exchanges[0].GetAccount);  // Get in order to give coinValueof BaseAsset Account data initialized by attributes (that is, base currency assets).
    coinValue[BaseAsset] = {amount:account.Balance + account.FrozenBalance, value:account.Balance + account.FrozenBalance};  // amount , value Attribute Initialization is all the total denominated currency. BaseAsset is the base currency
    totalValue = coinValue[BaseAsset].value;    // Update total value 
    logString += BaseAsset + ': ' + _N(coinValue[BaseAsset].value,5) + '\n';    // Add the current base currency total value data to the log string
    for(var i=0;i<exchanges.length;i++){                                        // Iterate through the exchange object
        var account = _C(exchanges[i].GetAccount);                              // Update account information of current index
        coinValue[BaseAsset] = {amount:account.Balance + account.FrozenBalance, value:account.Balance + account.FrozenBalance};  // amount , value Attribute Initialization is all the total denominated currency. BaseAsset is the base currency
        var ticker = _C(exchanges[i].GetTicker);                                // Update account market information for the current index
        var symbol = exchanges[i].GetCurrency().split('_')[0];                  // Get the name of the operating coin
        coinValue[symbol].amount = account.Stocks + account.FrozenStocks;       // Record the quantity of the operating coin
        coinValue[symbol].value = coinValue[symbol].amount * ticker.Last;       // Record the value of the operation currency (BaseAsset pricing)
        totalValue += coinValue[symbol].value;                                  // Cumulative total value
        coinValue[symbol].buyPrice = ticker.Buy;                                // Update the buy one price data on the exchange object of the current index
        coinValue[symbol].sellPrice = ticker.Sell;                              // Update the sell one price data on the exchange object of the current index
        logString += symbol + ': ' + _N(coinValue[symbol].value,5) + '\n'       // Add the value of the operation currency of the current exchange index to the log string.
        Sleep(1000)
    }
    LogStatus(logString);                                                       // Output in the status bar
}
var keepPercent = Ratio.split('|').map(Number);                                 // using characters "|" Split Ratio Parameters, then call map Function, convert string to Number Type Returns a new array.
if(math.sum(keepPercent) > 1){                                                  // Statistics keepPercent Sum of element values in the array
    throw 'sum of keep percent should be lower than 1';                         // The total proportion of each asset cannot exceed 100%
}
var buyPercent = ToBuy.split('|').map(Number);                                  // Process the string according to the parameters to construct a buy ratio array
var sellPercent = ToSell.split('|').map(Number);                                // ... Construct sell ratio array
for(var i=0;i<exchanges.length;i++){                                            // Traverse the array of exchange objects
    var symbol = exchanges[i].GetCurrency().split('_')[0];                      // Get the name of the trading currency in the trading pair and assign it to symbol 
    coinValue[symbol] = {amount:0, value:0, buyPrice:0, sellPrice:0, keepPercent:0, buyPercent:0, sellPercent:0};  // Construct relevant data of each trading pair object trading currency: quantity, value, buying price, selling price, holding percentage, buying percentage, selling percentage
    coinValue[symbol].keepPercent = keepPercent[i];   // Initialize holding percentage
    coinValue[symbol].buyPercent = buyPercent[i];     // Initialize buying percentage
    coinValue[symbol].sellPercent = sellPercent[i];   // Initialize selling percentage
}
function CancelPendingOrders(e) {                     // Cancel all pending orders
    var orders = _C(e.GetOrders);
    for (var j = 0; j < orders.length; j++) {
        e.CancelOrder(orders[j].Id, orders[j]);
        Sleep(300);
    }
}
function onTick(){    // Main logic function implementation
    updateValue();    // Update net value of operation currency
    for(var i=0;i<exchanges.length;i++){                                              // Traverse exchanges
        var symbol = exchanges[i].GetCurrency().split('_')[0];                        // Get the operation currency name of the current exchange object
        if(coinValue[symbol].value > (1+coinValue[symbol].sellPercent)*totalValue*coinValue[symbol].keepPercent){
           var sellAmount = (coinValue[symbol].value - totalValue*coinValue[symbol].keepPercent)/coinValue[symbol].buyPrice
           exchanges[i].Sell(coinValue[symbol].buyPrice, sellAmount)
           CancelPendingOrders(exchanges[i]);
           }
        else if(coinValue[symbol].value < (1-coinValue[symbol].buyPercent)*totalValue*coinValue[symbol].keepPercent){
            var buyAmount = (totalValue*coinValue[symbol].keepPercent - coinValue[symbol].value)/coinValue[symbol].sellPrice
            exchanges[i].Buy(coinValue[symbol].sellPrice, buyAmount);
            CancelPendingOrders(exchanges[i]);
        }        
    }
}
function main() {
    while(true){    // Main loop
        onTick();   // Main logic function
        Sleep(Interval*1000);
    }
}
```

> Detail

https://www.fmz.com/strategy/120581

> Last Modified

2021-04-21 09:14:03
