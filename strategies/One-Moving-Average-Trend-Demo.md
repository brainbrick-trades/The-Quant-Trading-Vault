
> Name

One-Moving-Average-Trend-Demo

> Author

扁豆子



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Amount|100|Amount|


> Source (javascript)

``` javascript
// Define Object
var e = exchange
e.SetContractType('XBTUSD')
var LastBarTime = 0
Idle = -1
status = Idle

// Connect to exchange, Get relevant information
function UpdateInfo() {
    var account = exchange.GetAccount()
    records = exchange.GetRecords()
    ticker = exchange.GetTicker()
    balance = account.Stocks
    Bar = records[records.length - 1]
}

// Indicator calculation and acquisition
function Get_MA() {
    var MA = TA.MA(records, 30)
    MA_close = MA[MA.length - 1]
}

// Open and close position rules
function onTick() {
    if (LastBarTime !== Bar.Time) { // KExecute trades after the line ends
        if (status === Idle) {
            if (Bar.Close > MA_close) {
                exchange.SetDirection("buy") 
                exchange.Buy(ticker.Sell, Amount)
                status = PD_LONG
            }
            if (Bar.Close < MA_close) {
                exchange.SetDirection("sell") 
                exchange.Sell(ticker.Buy, Amount)
                status = PD_SHORT
            }
        }
        if (status === PD_LONG) {
            if (Bar.Close < MA_close) {
                exchange.SetDirection("closebuy")
                exchange.Sell(ticker.Buy, Amount)
                exchange.SetDirection("sell") 
                exchange.Sell(ticker.Buy, Amount)
                status = PD_SHORT
            }
        }
        if (status === PD_SHORT) {
            if (Bar.Close > MA_close) {
                exchange.SetDirection("closesell") 
                exchange.Buy(ticker.Sell, Amount)
                exchange.SetDirection("buy") 
                exchange.Buy(ticker.Sell, Amount)
                status = PD_LONG
            }
        }
        LastBarTime = Bar.Time
    }
}

function main() {
    // Main Function, Continuous Loop
    while (1) {
        // Connect to exchange, Get relevant information
        UpdateInfo()
        // Indicator calculation and acquisition
        Get_MA()
        // Open and close position rules
        onTick()
        // Printbalance
        LogStatus(balance)
        // PollingsleepTime
        Sleep(5 * 1000)
    }
}
```

> Detail

https://www.fmz.com/strategy/193609

> Last Modified

2020-04-11 21:28:30
