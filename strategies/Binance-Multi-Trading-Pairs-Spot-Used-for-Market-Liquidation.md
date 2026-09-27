
> Name

Binance-Multi-Trading-Pairs-Spot-Used-for-Market-Liquidation

> Author

轻轻的云

> Strategy Description

This is used to clear stock.,
For example, running multi-pair spot grids or Martingale strategies-if you no longer want to run them, but you hold numerous coins, selling them one by one is too troublesome,
Just use this; input the currency into the parameters, and all market prices will automatically be sold.
However, sometimes after selling out, there will still be assets with a valuation less than 0.0012 BTC. At this time, you need to use [Small Assets Exchange for BNB] in the spot wallet.,
In other words, if you have BNB, it is best to sell it at the market price.

 ![IMG](https://www.fmz.com/upload/asset/59622a6123c4e006c00e.png) 
 
 ![IMG](https://www.fmz.com/upload/asset/5a004355bd61ce2b0d93.png) 
 
  ![IMG](https://www.fmz.com/upload/asset/5a3ccbbe2eb4ff9bee47.png) 

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|B_Sleep_time|5|Polling interval (seconds))|
|B_symbols|TRX_BUSD,LTC_BUSD,BCH_BUSD|trading pair|
|B_chongzhi|false|Reset|


> Source (javascript)

``` javascript
//Global Variables
var arrSymbols = B_symbols.split(",") // Comma-separated transaction symbol string

//Get price precision quantity precision function
function GetPrecision() {
    var precision = {
        price: 0, //Precision-price
        amount: 0 //Accuracy-quantity
    }
    var depth = _C(exchange.GetDepth)
    if (!depth) {
        throw 'Cannot connect to exchange market, need overseas custodian'
    }
    for (var i = 0; i < depth.Asks.length; i++) {
        var amountPrecision = depth.Asks[i].Amount.toString().indexOf('.') > -1 ? depth.Asks[i].Amount.toString().split('.')[1].length : 0
        precision.amount = Math.max(precision.amount, amountPrecision) //Quantity Precision
        var pricePrecision = depth.Asks[i].Price.toString().indexOf('.') > -1 ? depth.Asks[i].Price.toString().split('.')[1].length : 0
        precision.price = Math.max(precision.price, pricePrecision) //Price Precision
    }
    return precision
}

//Function to cancel all pending orders
//Parametere Yes/Is exchange.SetCurrency()  of exchange
function cancelAll(e) {
    while (true) {
        var orders = _C(e.GetOrders)
        if (orders.length == 0) {
            break
        } else {
            for (var i = 0; i < orders.length; i++) {
                e.CancelOrder(orders[i].Id, orders[i])
                Sleep(200)
            }
        }
        Sleep(200)
    }
}

function Trad() {
    for (var i = 0; i < arrSymbols.length; i++) {
        Sleep(500)
        symbol = arrSymbols[i]
        exchange.SetCurrency(symbol)
        var ticker = _C(exchange.GetTicker).Last //Latest price
        var precision = GetPrecision() //Get quantity accuracy and price accuracy
        var acc = _C(exchange.GetAccount)
        var base_balance = acc.Stocks //Currency, available balance
        var base_FrozenStocks = acc.FrozenStocks //The amount of currency frozen in pending orders
        var holdAmount = _N(parseFloat(base_balance + base_FrozenStocks), precision.amount) //Position = Currency balance+Freeze quantity
        if (holdAmount == 0 || holdAmount * ticker < 10) { //No position means the initial state,10USDTThe value is the minimum trading amount on Binance spot, less than10cannot be traded
            cancelAll(exchange)
            Log(symbol, "There is no position, or the number of positions is not enough for trading, the number of positions:", holdAmount)
        }
        if (holdAmount * ticker >= 10) { //Position Value >= USDTValue, then there is a position.
            Log(symbol, "Has positions, position quantity:", holdAmount, "Market price clearance", "#B15BFF")
            cancelAll(exchange)
            Sleep(500)
            var clearsell = exchange.Sell(-1, holdAmount) //close all positions
            Sleep(500)
            acc = _C(exchange.GetAccount)
            base_balance = acc.Stocks //Currency, available balance
            base_FrozenStocks = acc.FrozenStocks //The amount of currency frozen in pending orders
            holdAmount = _N(parseFloat(base_balance + base_FrozenStocks), precision.amount) //Reacquire position quantity
            Log(symbol, "Position Quantity:", holdAmount, "#B15BFF")
        }
    }
}

//Exit and cancel all pending orders 
function onexit() {
    Log("Stop the bot and cancel all pending orders", "#6F00D2")
    for (var i = 0; i < arrSymbols.length; i++) {
        symbol = arrSymbols[i]
        exchange.SetCurrency(symbol)
        cancelAll(exchange)
        Sleep(200)
    }
    Sleep(200)
}

//Exit on error and cancel all pending orders
function onerror() {
    Log("Bot error, cancel all pending orders", "#00BB00")
    for (var i = 0; i < arrSymbols.length; i++) {
        symbol = arrSymbols[i]
        exchange.SetCurrency(symbol)
        cancelAll(exchange)
        Sleep(200)
    }
    Sleep(200)
}

function main() {
    if (B_chongzhi) {
        // LogProfitReset() //Clear the income chart, only clear the chart, but not the log information
        LogReset() //Clear logs. Only clear logs, do not clear charts.
        LogVacuum()
        Log("Reset all data", "#FF0000")
    }
    while (true) {
        Trad()
        Sleep(B_Sleep_time * 1000)
    }
}


```

> Detail

https://www.fmz.com/strategy/360782

> Last Modified

2022-05-02 10:23:01
