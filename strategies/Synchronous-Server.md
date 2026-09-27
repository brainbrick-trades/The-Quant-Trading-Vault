
> Name

Synchronous-Server

> Author

发明者量化-小小梦

> Strategy Description

Related articles:
https://www.fmz.com/digest-topic/8932
https://www.fmz.com/digest-topic/8946

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|specifiedAmount|-1|Specify Synchronization Volume|
|zoomAmountRatio|-1|Synchronization Volume Scaling|
|amountPrecision|2|Order quantity accuracy|
|pricePrecision|2|Price Precision|
|isSimulateOKEX|false|Use OKEX demo account?|




|Button|Default|Description|
|----|----|----|
|stop/restart||Stop Copy Trading|


> Source (javascript)

``` javascript
// Global Variables
var isStopFollow = false
var reStartPwd = null 

function trade(action) {
    // Switch trading pair, set contract
    exchange.SetCurrency(action.symbol)
    if (action.ct != "spot") {
        exchange.SetContractType(action.ct)        
    }    

    var retTrade = null 
    var amount = specifiedAmount == -1 ? action.amount : specifiedAmount
    amount = zoomAmountRatio == -1 ? amount : amount * zoomAmountRatio

    if (action.direction == "buy") {
        retTrade = action.ct == "spot" ? $.Buy(amount) : $.OpenLong(exchange, action.ct, amount)
    } else if (action.direction == "sell") {
    	retTrade = action.ct == "spot" ? $.Sell(amount) : $.OpenShort(exchange, action.ct, amount)
    } else if (action.direction == "closebuy") {
    	retTrade = action.ct == "spot" ? $.Sell(amount) : $.CoverLong(exchange, action.ct, amount)
    } else if (action.direction == "closesell") {
    	retTrade = action.ct == "spot" ? $.Buy(amount) : $.CoverShort(exchange, action.ct, amount)
    }
    return retTrade
}

function parseCmd(cmd) {
	var objAction = {}
	// Parsecmd ,For Example:ETH_USDT,swap,buy,1
    var arr = cmd.split(",")
    if (arr.length != 4) {
    	return null 
    }
    objAction.symbol = arr[0]
    objAction.ct = arr[1]
    objAction.direction = arr[2]
    objAction.amount = arr[3]
    return objAction
}

function main() {
	// Clear all logs
    LogReset(1)  

    if (isSimulateOKEX) {
    	exchange.IO("simulate", true)
    	Log("Switch toOKEXSimulation Account!")
    }

    // Set Precision
    exchange.SetPrecision(pricePrecision, amountPrecision)

    // Check scaling, cannot specify both at the same time
    if (specifiedAmount != -1 && zoomAmountRatio != -1) {
    	throw "Cannot specify sync amount and scaling amount at the same time"
    }

    while (true) {
        var cmd = GetCommand()
        if (cmd) {
            Log("cmd: ", cmd)
            var arr = cmd.split(":")

            // Determine interactive command
            if (arr.length == 2) {
            	// Buttons with controls
            	if (arr[0] == "stop/restart") {
            		// pause/Restart Copy Trading
            		if (!isStopFollow) {
            		    isStopFollow = true
            		    reStartPwd = arr[1]
            		    Log("has stopped copying,", "The reset password set is:", reStartPwd, "#FF0000")
            		} else if (isStopFollow && arr[1] == reStartPwd) {
            			isStopFollow = false 
            			reStartPwd = null 
            			Log("has resumed copy trading,", "Clear the restart password.", "#FF0000")
            		} else if (isStopFollow && arr[1] != reStartPwd) {
            			Log("Restart password error!")
            		}
            	}
            	continue 
            }
            
            // Allow Copy Trading
            if (!isStopFollow) {
                // Parse copy-trade signal interaction instructions
                var objAction = parseCmd(cmd)
                if (objAction) {
            	    // Parsed Correctly
            	    var ret = trade(objAction)
                } else {
                	Log("Invalid signal command cmd:", cmd)
                }
            }
        }
        
        // Displays copy trading status
        LogStatus(_D(), isStopFollow ? "Stop syncing : keep syncing", "\n")

        Sleep(1000)
    }
}
```

> Detail

https://www.fmz.com/strategy/345172

> Last Modified

2022-02-16 14:47:43
