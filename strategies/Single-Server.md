
> Name

Single-Server

> Author

发明者量化-小小梦

> Strategy Description

Related articles:
https://www.fmz.com/digest-topic/8932
https://www.fmz.com/digest-topic/8946

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|config1||Copy Trading Configuration1|
|config2||Copy Trading Configuration2|
|config3||Copy Trading Configuration3|
|config4||Copy Trading Configuration4|
|config5||Copy Trading Configuration5|
|amountPrecision|3|Copy Trade Volume Precision|


> Source (javascript)

``` javascript
// Global Variables
var keyName_label = "label"
var keyName_robotId = "robotId"
var keyName_extendAccessKey = "extendAccessKey"
var keyName_extendSecretKey = "extendSecretKey"
var fmzExtendApis = parseConfigs([config1, config2, config3, config4, config5])
var mapInitRefPosAmount = {}

function parseConfigs(configs) {
    var arr = []
    _.each(configs, function(config) {
        if (config == "") {
            return 
        }
        var strArr = config.split(",")
        if (strArr.length != 4) {
            throw "configs error!"
        }
        var obj = {}
        obj[keyName_label] = strArr[0]
        obj[keyName_robotId] = strArr[1]
        obj[keyName_extendAccessKey] = strArr[2]
        obj[keyName_extendSecretKey] = strArr[3]
        arr.push(obj)
    })
    return arr 
}

function getPosAmount(pos, ct) {
    var longPosAmount = 0
    var shortPosAmount = 0
    _.each(pos, function(ele) {
        if (ele.ContractType == ct && ele.Type == PD_LONG) {
            longPosAmount = ele.Amount
        } else if (ele.ContractType == ct && ele.Type == PD_SHORT) {
            shortPosAmount = ele.Amount
        }
    })
    var timestamp = new Date().getTime()
    return {ts: timestamp, long: longPosAmount, short: shortPosAmount}
}

function sendCommandRobotMsg (robotId, accessKey, secretKey, msg) {
    // https://www.fmz.com/api/v1?access_key=xxx&secret_key=yyyy&method=CommandRobot&args=[186515,"ok12345"]
    var url = "https://www.fmz.com/api/v1?access_key=" + accessKey + "&secret_key=" + secretKey + "&method=CommandRobot&args=[" + robotId + ',"' + msg + '"]'
    Log(url)
    var ret = HttpQuery(url)
    return ret 
}

function follow(nowPosAmount, symbol, ct, type, delta) {
    var msg = ""
    var nowAmount = type == PD_LONG ? nowPosAmount.long : nowPosAmount.short
    if (delta > 0) {
        // Open Position
        var tradeDirection = type == PD_LONG ? "buy" : "sell"
        // Send Signal
        msg = symbol + "," + ct + "," + tradeDirection + "," + Math.abs(delta)        
    } else if (delta < 0) {
        // Close Position
        var tradeDirection = type == PD_LONG ? "closebuy" : "closesell"
        if (nowAmount <= 0) {
            Log("No Position Detected")
            return 
        }
        // Send Signal
        msg = symbol + "," + ct + "," + tradeDirection + "," + Math.abs(delta)
    } else {
        throw "Error"
    }
    if (msg) {
        _.each(fmzExtendApis, function(extendApiConfig) {
            var ret = sendCommandRobotMsg(extendApiConfig[keyName_robotId], extendApiConfig[keyName_extendAccessKey], extendApiConfig[keyName_extendSecretKey], msg)
            Log("CallCommandRobotInterface,", "label:", extendApiConfig[keyName_label], ", msg:", msg, ", ret:", ret)
            Sleep(1000)
        })
    }
}

$.PosMonitor = function(exIndex, symbol, ct) {    
    // fmzExtendApis If it is an empty array, meaning there is no configuration to push, monitoring is not required, return directly
    if (fmzExtendApis.length == 0) {
        return 
    }

    var ts = new Date().getTime()
    var ex = exchanges[exIndex]
    // JudgmentexType
    var exName = ex.GetName()
    var isFutures = exName.includes("Futures_")
    var exType = isFutures ? "futures" : "spot"
    if (!isFutures) {
        throw "Only supports futures copy trading"
    }

    if (exType == "futures") {
        // Cache symbol ct
        var buffSymbol = ex.GetCurrency()
        var buffCt = ex.GetContractType()

        // Switch to the corresponding trading pair and contract code
        ex.SetCurrency(symbol)
        if (!ex.SetContractType(ct)) {
            throw "SetContractType failed"
        }

        // Monitor Positions
        var keyInitRefPosAmount = "refPos-" + exIndex + "-" + symbol + "-" + ct    // refPos-exIndex-symbol-contractType
        var initRefPosAmount = mapInitRefPosAmount[keyInitRefPosAmount]
        if (!initRefPosAmount) {
            // No initialization data, initialize          
            mapInitRefPosAmount[keyInitRefPosAmount] = getPosAmount(_C(ex.GetPosition), ct)
            initRefPosAmount = mapInitRefPosAmount[keyInitRefPosAmount]
        }

        // Monitoring
        var nowRefPosAmount = getPosAmount(_C(ex.GetPosition), ct)
        // Calculate position changes
        var longPosDelta = _N(nowRefPosAmount.long - initRefPosAmount.long, amountPrecision)
        var shortPosDelta = _N(nowRefPosAmount.short - initRefPosAmount.short, amountPrecision)

        // Detect changes
        if (!(longPosDelta == 0 && shortPosDelta == 0)) {
            // Execute long action
            if (longPosDelta != 0) {
                Log(ex.GetName(), ex.GetLabel(), symbol, ct, "Execute long position copy, change amount:", longPosDelta)
                follow(nowRefPosAmount, symbol, ct, PD_LONG, longPosDelta)
            }
            // Execute short action
            if (shortPosDelta != 0) {
                Log(ex.GetName(), ex.GetLabel(), symbol, ct, "Execute short position copy, change amount:", shortPosDelta)
                follow(nowRefPosAmount, symbol, ct, PD_SHORT, shortPosDelta)
            }

            // After executing copy action, update
            mapInitRefPosAmount[keyInitRefPosAmount] = nowRefPosAmount
        }

        // Restore symbol ct
        ex.SetCurrency(buffSymbol)
        ex.SetContractType(buffCt)
    } else if (exType == "spot") {
        // spot
        ct = "spot"  // Set as Spot
    }
}

$.getTbl = function() {
    var tbl = {
        "type" : "table", 
        "title" : "Sync Data", 
        "cols" : [], 
        "rows" : []
    }
    // Construct Table Header
    tbl.cols.push("Monitor Account:refPos-exIndex-symbol-contractType")
    tbl.cols.push(`Monitor Positions:{"timestamp":xxx,"Long Position Volume":xxx,"Short Position Volume":xxx}`)
    _.each(fmzExtendApis, function(extendApiData, index) {
        tbl.cols.push(keyName_robotId + "-" + index)
    })
    
    // Write data
    _.each(mapInitRefPosAmount, function(initRefPosAmount, key) {
        var arr = [key, JSON.stringify(initRefPosAmount)]
        _.each(fmzExtendApis, function(extendApiData) {
            arr.push(extendApiData[keyName_robotId])
        })
        tbl.rows.push(arr)
    })

    return tbl
}

// Reference example of strategy call for this template library
function main() {
    // Clear all logs
    LogReset(1)

    // Switch toOKEX Demo Account Test
    // exchanges[0].IO("simulate", true)

    // Set Contract
    exchanges[0].SetCurrency("ETH_USDT")
    exchanges[0].SetContractType("swap")

    // Scheduled transaction time interval
    var tradeInterval = 1000 * 60 * 3        // Trade once every three minutes, used to observe copy trading signals
    var lastTradeTS = new Date().getTime()
    
    while (true) {
        // Other logic of the strategy...

        // Test simulated trading triggered
        var ts = new Date().getTime()
        if (ts - lastTradeTS > tradeInterval) {
            Log("Simulate the signal-following strategy transactions and position changes", "#FF0000")
            exchanges[0].SetDirection("closesell")
            exchanges[0].Buy(-1, 0.003)
            lastTradeTS = ts
        }

        // Interface function using templates
        $.PosMonitor(0, "ETH_USDT", "swap")    // You can set multiple monitors to monitor different order strategies.exchangeObject  
        var tbl = $.getTbl()
        
        // Show Status Bar
        LogStatus(_D(), "\n" + "`" + JSON.stringify(tbl) + "`")
        Sleep(1000)
    }
}

```

> Detail

https://www.fmz.com/strategy/345171

> Last Modified

2022-02-16 14:47:15
