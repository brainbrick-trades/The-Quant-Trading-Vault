
> Name

TradingView-WebHook-Signal-Execution-Strategy-Lesson

> Author

发明者量化-小小梦

> Strategy Description

Related articles:https://www.fmz.com/bbs-topic/5533
BStation video link:https://www.bilibili.com/video/BV1Wk4y1k7zz/

- 2020.7.29 Update
  Add two instructions, SPK and BPK, corresponding respectively: sell to close a long position and then sell to open a short position; buy to close a short position and then buy to open a long position.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|IsMarketOrder|false|Whether to use market order|
|QuotePrecision|2|Order price accuracy|
|BasePrecision|2|Order quantity accuracy|
|Ct||Futures contract code|




|Button|Default|Description|
|----|----|----|
|buy|0.01|Test Buy|
|sell|0.01|Test Sell|


> Source (javascript)

``` javascript
/*
- Interaction command string format
  action:amount
  action: buy , sell , long , short , cover_long , cover_short, spk , bpk
- Exchange type
  eTypeVariable Values: 0 spot , 1 futures

- TVDocumentation Link
  https://www.tradingview.com/pine-script-docs/en/v4/Quickstart_guide.html
  https://cn.tradingview.com/chart/8xfTuX7F/

- TV webhook Send Request
  https://www.fmz.com/api/v1?access_key=xxx&secret_key=yyyy&method=CommandRobot&args=[186515,"action:amount"]

- Reference Library
  Reference cryptocurrency trading library
*/

// Parameters
// var IsMarketOrder = false 
// var QuotePrecision = 2
// var BasePrecision = 2

// Futures Parameters
// var Ct = ""


// Global Variables
var BUY = "buy"
var SELL = "sell"
var LONG = "long"
var SHORT = "short"
var COVER_LONG = "cover_long"
var COVER_SHORT = "cover_short"
var SPK = "spk"
var BPK = "bpk"


function main() {
    // Clear the logs, delete if not needed
    LogReset(1)

	// Set Precision
    exchange.SetPrecision(QuotePrecision, BasePrecision)

    // Identify futures or spot
    var eType = 0
    var eName = exchange.GetName()
    var patt = /Futures_/
    if (patt.test(eName)) {
        Log("The added exchange is a futures exchange:", eName, "#FF0000")
        eType = 1
        if (Ct == "") {
            throw "Ct Set contract to empty"
        } else {
        	Log(exchange.SetContractType(Ct), "Set Contract:", Ct, "#FF0000")
        }
    } else {
    	Log("The added exchange is a spot exchange:", eName, "#32CD32")
    }
    
    var lastMsg = ""
    var acc = _C(exchange.GetAccount)
    while(true) {
        var cmd = GetCommand()
        if (cmd) {
            // Detect interactive commands
            lastMsg = "Command:" + cmd + "Time:" + _D()
            var arr = cmd.split(":")
            if (arr.length != 2) {
                Log("cmdIncorrect Information:", cmd, "#FF0000")
                continue
            }

            var action = arr[0]
            var amount = parseFloat(arr[1])

            if (eType == 0) {
                if (action == BUY) {               
                    var buyInfo = IsMarketOrder ? exchange.Buy(-1, amount) : $.Buy(amount)
                    Log("buyInfo:", buyInfo)
                } else if (action == SELL) {        
                    var sellInfo = IsMarketOrder ? exchange.Sell(-1, amount) : $.Sell(amount)
                    Log("sellInfo:", sellInfo)
                } else {
                	Log("Not supported by spot exchange!", "#FF0000")
                }
            } else if (eType == 1) {
            	var tradeInfo = null
            	var ticker = _C(exchange.GetTicker)
                if (action == LONG) {
                	exchange.SetDirection("buy")
                    tradeInfo = IsMarketOrder ? exchange.Buy(-1, amount) : exchange.Buy(ticker.Sell, amount)
                } else if (action == SHORT) {        
                    exchange.SetDirection("sell")
                    tradeInfo = IsMarketOrder ? exchange.Sell(-1, amount) : exchange.Sell(ticker.Buy, amount)
                } else if (action == COVER_LONG) {        
                    exchange.SetDirection("closebuy")
                    tradeInfo = IsMarketOrder ? exchange.Sell(-1, amount) : exchange.Sell(ticker.Buy, amount)
                } else if (action == COVER_SHORT) {        
                	exchange.SetDirection("closesell")
                	tradeInfo = IsMarketOrder ? exchange.Buy(-1, amount) : exchange.Buy(ticker.Sell, amount)
                } else if (action == SPK) {   // Sell to close a long position, sell to open a short position
                    exchange.SetDirection("closebuy")
                    var tradeInfo1 = IsMarketOrder ? exchange.Sell(-1, amount) : exchange.Sell(ticker.Buy, amount)
                    exchange.SetDirection("sell")
                    var tradeInfo2 = IsMarketOrder ? exchange.Sell(-1, amount) : exchange.Sell(ticker.Buy, amount)
                    tradeInfo = [tradeInfo1, tradeInfo2]
                } else if (action == BPK) {   // Buy to close a short position, buy to open a long position
                    exchange.SetDirection("closesell")
                    var tradeInfo1 = IsMarketOrder ? exchange.Buy(-1, amount) : exchange.Buy(ticker.Sell, amount)
                    exchange.SetDirection("buy")
                    var tradeInfo2 = IsMarketOrder ? exchange.Buy(-1, amount) : exchange.Buy(ticker.Sell, amount)
                    tradeInfo = [tradeInfo1, tradeInfo2]
                } else {
                	Log("Futures exchange does not support!", "#FF0000")
                }
                if (tradeInfo) {
                    Log("tradeInfo:", tradeInfo)
                }
            } else {
            	throw "eType error, eType:" + eType
            }
            acc = _C(exchange.GetAccount)
        }
        var tbl = {
        	type : "table", 
        	title : "Status Information", 
        	cols : ["Data"], 
        	rows : []
        }
        tbl.rows.push([JSON.stringify(acc)])
        LogStatus(_D(), eName, "Last command received:", lastMsg, "\n", "`" + JSON.stringify(tbl) + "`")
    	Sleep(1000)
    }
}


```

> Detail

https://www.fmz.com/strategy/203063

> Last Modified

2020-07-29 17:10:43
