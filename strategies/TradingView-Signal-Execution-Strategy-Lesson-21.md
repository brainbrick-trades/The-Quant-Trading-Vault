
> Name

TradingView-Signal-Execution-Strategy-Lesson-21

> Author

发明者量化-小小梦

> Strategy Description

Related articles:https://www.fmz.com/digest-topic/9794

## 2024.7.7

Add reverse instruction.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|SleepInterval|Seconds|Loop interval|
|FMZ_AccessKey|Note: this is the AccessKey for the FMZ platform, not the exchange KEY | FMZ platformAccessKey|
|FMZ_SecretKey|Note: this is the SecretKey for the FMZ platform, not the exchange KEY | FMZ platformSecretKey|
|maxBuffSignalRowDisplay|The maximum number of lines displayed in the status bar, setting 20 shows the last 20 signal records | Maximum number of lines displayed for signals|
|isLogReset|Check reset | Reset all logs|




|Button|Default|Description|
|----|----|----|
|TestSignal|Only used to simulate the webhook request sent by TradingView | test signals|
|evalCode|Directly execute Javascript code, which can be used for testing, switching simulation disks, etc. | Execute Javascript code|


> Source (javascript)

``` javascript
//Signal structure
var Template = {
    Flag: "45M103Buy",     // Logo, you can specify it at will
    Exchange: 1,           // Designated exchange trading pair
    Currency: "BTC_USDT",  // trading pair
    ContractType: "swap",  // Contract type, fill in swap, quarter, next_quarter, spotspot
    Price: "{{close}}",    // Opening or closing price, -1 for market price
    Action: "buy",         // Transaction types [buy: spot buy, sell: spot sell, long: futures long, short: futures short, closesell: futures buy to close short, closebuy: futures sell to close long, bpk: buy to close short position and then buy to open long position, spk: sell to close long position and then sell to open short position]]
    Amount: "0",           // Trading volume
}

var BaseUrl = "https://www.fmz.com/api/v1"   // FMZExtendAPIInterface address 
var RobotId = _G()                           // Current real offerID
var Success = "#5cb85c"    // Success color
var Danger = "#ff0000"     // Dangerous colors
var Warning = "#f0ad4e"    // Warning color
var buffSignal = []

// Verification signal message format
function DiffObject(object1, object2) {
    const keys1 = Object.keys(object1)
    const keys2 = Object.keys(object2)
    if (keys1.length !== keys2.length) {
        return false
    }
    for (let i = 0; i < keys1.length; i++) {
        if (keys1[i] !== keys2[i]) {
            return false
        }
    }
    return true
}

function CheckSignal(Signal) {
    Signal.Price = parseFloat(Signal.Price)
    Signal.Amount = parseFloat(Signal.Amount)
    if (Signal.Exchange <= 0 || !Number.isInteger(Signal.Exchange)) {
        Log("The minimum exchange number is1,And must be an integer", Danger)
        return
    }
    if (Signal.Amount <= 0 || typeof(Signal.Amount) != "number") {
        Log("Trading volume cannot be less than0,And must be a numeric type", typeof(Signal.Amount), Danger)
        return
    }
    if (typeof(Signal.Price) != "number") {
        Log("Price must be numeric", Danger)
        return
    }
    if (Signal.ContractType == "spot" && Signal.Action != "buy" && Signal.Action != "sell") {
        Log("Instruction is to operate spot trading,ActionError,Action:", Signal.Action, Danger)
        return 
    }
    if (Signal.ContractType != "spot" && Signal.Action != "long" && Signal.Action != "short" && Signal.Action != "closesell" && Signal.Action != "closebuy" &&
        Signal.Action != "bpk" && Signal.Action != "spk") {
        Log("Instruction to operate futures,ActionError,Action:", Signal.Action, Danger)
        return 
    }
    return true
}

function commandRobot(url, accessKey, secretKey, robotId, cmd) {
    // https://www.fmz.com/api/v1?access_key=xxx&secret_key=xxx&method=CommandRobot&args=[xxx,+""]
    url = url + '?access_key=' + accessKey + '&secret_key=' + secretKey + '&method=CommandRobot&args=[' + robotId + ',+""]'
    var postData = {
        method:'POST', 
        data:cmd
    }
    var headers = "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36\nContent-Type: application/json"
    var ret = HttpQuery(url, postData, "", headers)
    Log("SimulationTradingViewofwebhookRequest, sent for testingPOSTRequest:", url, "body:", cmd, "Response:", ret)
}

function createManager() {
    var self = {}
    self.tasks = []
    
    self.process = function() {
        var processed = 0
        if (self.tasks.length > 0) {
            _.each(self.tasks, function(task) {
                if (!task.finished) {
                    processed++
                    self.pollTask(task)
                }
            })
            if (processed == 0) {
                self.tasks = []
            }
        }
    }
    
    self.newTask = function(signal) {
        // {"Flag":"45M103Buy","Exchange":1,"Currency":"BTC_USDT","ContractType":"swap","Price":"10000","Action":"buy","Amount":"0"}
        var task = {}
        task.Flag = signal["Flag"]
        task.Exchange = signal["Exchange"]
        task.Currency = signal["Currency"]
        task.ContractType = signal["ContractType"]
        task.Price = signal["Price"]
        task.Action = signal["Action"]
        task.Amount = signal["Amount"]
        task.exchangeIdx = signal["Exchange"] - 1
        task.pricePrecision = null
        task.amountPrecision = null 
        task.error = null 
        task.exchangeLabel = exchanges[task.exchangeIdx].GetLabel()
        task.finished = false 
        
        Log("Create task:", task)
        self.tasks.push(task)
    }
    
    self.getPrecision = function(n) {
        var precision = null 
        var arr = n.toString().split(".")
        if (arr.length == 1) {
            precision = 0
        } else if (arr.length == 2) {
            precision = arr[1].length
        } 
        return precision
    }
    
    self.cover = function(task) {
        var e = exchanges[task.exchangeIdx]
        var action = task.Action
        var pos = e.GetPosition()
        if (pos === null) {
            task.error = "Position data abnormal"
            return false
        }
        
        _.each(pos, function(p) {  
            if (action == "bpk" && p.Type == PD_SHORT) {
                e.SetDirection("closesell")
                e.Buy(-1, p.Amount)
            } else if (action == "spk" && p.Type == PD_LONG) {
                e.SetDirection("closebuy")
                e.Sell(-1, p.Amount)
            }
        })

        return true 
    }

    self.pollTask = function(task) {
        var e = exchanges[task.exchangeIdx]
        var name = e.GetName()
        var isFutures = true
        e.SetCurrency(task.Currency)
        if (task.ContractType != "spot" && name.indexOf("Futures_") != -1) {
            // If not spot trading, set the contract
            e.SetContractType(task.ContractType)
        } else if (task.ContractType == "spot" && name.indexOf("Futures_") == -1) {
            isFutures = false 
        } else {
            task.error = "The ContractType in the instruction does not match the configured exchange object type."
            task.finished = true
            return 
        }
        
        var depth = e.GetDepth()
        if (!depth || !depth.Bids || !depth.Asks) {
            task.error = "Order book data anomaly"
            return 
        }
        
        if (depth.Bids.length == 0 && depth.Asks.length == 0) {
            task.error = "No orders on the market"
            return 
        }
        
        _.each([depth.Bids, depth.Asks], function(arr) {
            _.each(arr, function(order) {
                var pricePrecision = self.getPrecision(order.Price)
                var amountPrecision = self.getPrecision(order.Amount)
                if (Number.isInteger(pricePrecision) && !Number.isInteger(self.pricePrecision)) {
                    self.pricePrecision = pricePrecision
                } else if (Number.isInteger(self.pricePrecision) && Number.isInteger(pricePrecision) && pricePrecision > self.pricePrecision) {
                    self.pricePrecision = pricePrecision
                }
                if (Number.isInteger(amountPrecision) && !Number.isInteger(self.amountPrecision)) {
                    self.amountPrecision = amountPrecision
                } else if (Number.isInteger(self.amountPrecision) && Number.isInteger(amountPrecision) && amountPrecision > self.amountPrecision) {
                    self.amountPrecision = amountPrecision
                }
            })
        })

        if (!Number.isInteger(self.pricePrecision) || !Number.isInteger(self.amountPrecision)) {
            task.err = "Failed to get precision"
            return 
        }
        
        e.SetPrecision(self.pricePrecision, self.amountPrecision)
        
        // buy:Spot purchase , sell:Spot sale , long:Long futures , short:Short futures , closesell:Futures buy to close short , closebuy:Futures sell to close long, bpk:Buy to close long, spk:Sell to close short
        var direction = null 
        var tradeFunc = null 
        if (isFutures) {
            switch (task.Action) {
                case "long": 
                    direction = "buy"
                    tradeFunc = e.Buy 
                    break
                case "short": 
                    direction = "sell"
                    tradeFunc = e.Sell
                    break
                case "closesell": 
                    direction = "closesell"
                    tradeFunc = e.Buy 
                    break
                case "closebuy": 
                    direction = "closebuy"
                    tradeFunc = e.Sell
                    break
                case "bpk":
                    // Process closing position
                    if (!self.cover(task)) {
                        Log("Failed to close position")
                    }
                    direction = "buy"
                    tradeFunc = e.Buy 
                    break
                case "spk":
                    // Process closing position
                    if (!self.cover(task)) {
                        Log("Failed to close position")
                    }
                    direction = "sell"
                    tradeFunc = e.Sell 
                    break
            }
            if (!direction || !tradeFunc) {
                task.error = "Trading direction error:" + task.Action
                task.finished = true
                return 
            }
            e.SetDirection(direction)
        } else {
            if (task.Action == "buy") {
                tradeFunc = e.Buy 
            } else if (task.Action == "sell") {
                tradeFunc = e.Sell 
            } else {
                task.error = "Trading direction error:" + task.Action
                task.finished = true
                return 
            }
        }
        var id = tradeFunc(task.Price, task.Amount)
        if (!id) {
            task.error = "Order failed"
        }
        
        task.finished = true
    }
    
    return self
}

var manager = createManager()
function HandleCommand(signal) {
    // Detect whether an interactive command is received
    if (signal) {
        Log("Received interaction command:", signal)     // Received interaction command, print the interaction command
    } else {
        return                            // Return immediately if not received, do not process
    }
    
    // Detect whether the interactive command is a test command; test commands can be issued by the current strategy interaction control for testing.
    if (signal.indexOf("TestSignal") != -1) {
        signal = signal.replace("TestSignal:", "")
        // CallFMZExtendAPIInterface, simulationTrading Viewofwebhook,Interaction buttonTestSignalMessage sent:{"Flag":"45M103Buy","Exchange":1,"Currency":"BTC_USDT","ContractType":"swap","Price":"10000","Action":"buy","Amount":"0"}
        commandRobot(BaseUrl, FMZ_AccessKey, FMZ_SecretKey, RobotId, signal)
    } else if (signal.indexOf("evalCode") != -1) {
        var js = signal.split(':', 2)[1]
        Log("Execute debug code:", js)
        eval(js)
    } else {
        // Process signal instruction
        objSignal = JSON.parse(signal)
        if (DiffObject(Template, objSignal)) {
            Log("Received trade signal command:", objSignal)
            buffSignal.push(objSignal)
            
            // Check trading volume and exchange number
            if (!CheckSignal(objSignal)) {
                return
            }
            
            // Create task
            manager.newTask(objSignal)
        } else {
            Log("Unrecognizable command", signal)
        }
    }
}

function main() {
    if (isLogReset) {
        LogReset(1)
    }
    
    Log("WebHookAddress:", "https://www.fmz.com/api/v1?access_key=" + FMZ_AccessKey + "&secret_key=" + FMZ_SecretKey + "&method=CommandRobot&args=[" + RobotId + ',+""]', Danger)
    Log("Transaction types [buy: spot buy, sell: spot sell, long: futures long, short: futures short, closesell: futures buy to close short, closebuy: futures sell to close long, bpk: buy to close short position and then buy to open long position, spk: sell to close long position and then sell to open short position]]", Danger)
    Log("Command template:", JSON.stringify(Template), Danger)
    
    while (true) {
        try {
            // Handle Interaction
            HandleCommand(GetCommand())
            
            // Processing tasks
            manager.process()
            
            if (buffSignal.length > maxBuffSignalRowDisplay) {
                buffSignal.shift()
            }
            var buffSignalTbl = {
                "type" : "table",
                "title" : "Signal record",
                "cols" : ["Flag", "Exchange", "Currency", "ContractType", "Price", "Action", "Amount"],
                "rows" : []
            }
            for (var i = buffSignal.length - 1 ; i >= 0 ; i--) {
                buffSignalTbl.rows.push([buffSignal[i].Flag, buffSignal[i].Exchange, buffSignal[i].Currency, buffSignal[i].ContractType, buffSignal[i].Price, buffSignal[i].Action, buffSignal[i].Amount])
            }
            LogStatus(_D(), "\n", "`" + JSON.stringify(buffSignalTbl) + "`")
            Sleep(1000 * SleepInterval)
        } catch (error) {
            Log("e.name:", error.name, "e.stack:", error.stack, "e.message:", error.message)
            Sleep(1000 * 10)
        }
    }
}

```

> Detail

https://www.fmz.com/strategy/392048

> Last Modified

2024-07-07 10:48:13
