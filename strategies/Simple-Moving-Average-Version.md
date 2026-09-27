
> Name

Simple-Moving-Average-Version

> Author

sabar



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Amount|100|Amount|


> Source (javascript)

``` javascript
/*backtest
start: 2021-06-01 00:00:00
end: 2021-09-22 00:00:00
period: 5m
basePeriod: 1m
exchanges: [{"eid":"Futures_OKCoin","currency":"BTC_USD"}]
*/

// Define Object
var e = exchange
e.SetContractType('swap')
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
    
    var MA_10 = TA.MA(records, 10)
    MA_close_10 = MA_10[MA_10.length - 1]
    
    var MA_20 = TA.MA(records, 20)
    MA_close_20 = MA_20[MA_20.length - 1]

    var MA_30 = TA.MA(records, 30)
    MA_close_30 = MA_30[MA_30.length - 1]

}

// Open and close position rules
function onTick() {
    if (LastBarTime !== Bar.Time) { // KExecute trades after the line ends

        if (status === PD_LONG) {
            if (Bar.Close < MA_close_10) {
                exchange.SetDirection("closebuy")
                exchange.Sell(ticker.Buy, Amount)
                status = Idle
            }
        }

        if (status === PD_SHORT) {
            if (Bar.Close > MA_close_10) {
                exchange.SetDirection("closesell") 
                exchange.Buy(ticker.Sell, Amount)
                status = Idle
            }
        }
 Sleep(1 * 1000)
        if (status === Idle) {
            if (Bar.Close > MA_close_20 ) {
                exchange.SetDirection("buy") 
                exchange.Buy(ticker.Sell, Amount)
                status = PD_LONG
            }
            if (Bar.Close < MA_close_20 ) {
                exchange.SetDirection("sell") 
                exchange.Sell(ticker.Buy, Amount)
                status = PD_SHORT
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

https://www.fmz.com/strategy/318486

> Last Modified

2021-09-23 17:15:26
