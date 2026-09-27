
> Name

TradingView-Signal-Execution-Strategy-Built-in-HTTP-Service-Version

> Author

发明者量化-小小梦

> Strategy Description

Related articles:

> https://www.fmz.com/digest-topic/10556

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|port|Port number used by the built-in HTTP service. | Port|
|ipWhiteList|IPAddress whitelist; if not set, verification is not enabled. | IP address whitelist|
|passPhrase|Do not verify if not set. | Verification password|
|serverIP|Server IP address. | ServerIP|
|SleepInterval|Main loop polling interval | polling interval|
|maxBuffSignalRowDisplay|Maximum number of signal display rows | Maximum number of signal display rows|
|initCode|Code for initialization and execution, for example, used to test simulated disk, switch Binance futures base address: exchange.SetBase("https://testnet.binancefuture.com"); switch OKX simulated disk: exchange.IO("simulate", true) | Code for initialization and execution|
|isResetLog|Reset log | Reset log|




|Button|Default|Description|
|----|----|----|
|TestSignal|Signal test.|Signal test|


> Source (javascript)

``` javascript
//Signal structure
var Template = {
    Flag: "45M103Buy",     // Logo, you can specify it at will
    Exchange: 1,           // Designated exchange trading pair
    Currency: "BTC_USDT",  // trading pair
    ContractType: "spot",  // Contract type, fill in swap, quarter, next_quarter, spotspot
    Price: "{{close}}",    // Opening or closing price, -1 for market price
    Action: "buy",         // Transaction type [buy: buy spot, sell: sell spot, long: go long in futures, short: go short in futures, closesell: buy short in futures, closebuy: sell long in futures]
    Amount: "1",           // Trading volume
}

var Success = "#5cb85c"    // Success color
var Danger = "#ff0000"     // Dangerous colors
var Warning = "#f0ad4e"    // Warning color
var buffSignal = []

// HttpService
function serverFunc(ctx, ipWhiteList, passPhrase) {
    var path = ctx.path()
    if (path == "/CommandRobot") {
        // VerificationIPAddress
        var fromIP = ctx.remoteAddr().split(":")[0]        
        if (ipWhiteList && ipWhiteList.length > 0) {
            var ipList = ipWhiteList.split(",")
            if (!ipList.includes(fromIP)) {
                ctx.setStatus(500)
                ctx.write("IP address not in white list")
                Log("500 Error: IP address not in white list", "#FF0000")
                return 
            }
        }

        // Verify password
        var pass = ctx.rawQuery().length > 0 ? ctx.query("passPhrase") : ""
        if (passPhrase && passPhrase.length > 0) {
            if (pass != passPhrase) {
                ctx.setStatus(500)
                ctx.write("Authentication failed")
                Log("500 Error: Authentication failed", "#FF0000")
                return 
            }
        }

        var body = JSON.parse(ctx.body())
        threading.mainThread().postMessage(JSON.stringify(body))
        ctx.write("OK")
        // 200
    } else {
        ctx.setStatus(404)
    }
}

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
    if (Signal.ContractType != "spot" && Signal.Action != "long" && Signal.Action != "short" && Signal.Action != "closesell" && Signal.Action != "closebuy") {
        Log("Instruction to operate futures,ActionError,Action:", Signal.Action, Danger)
        return 
    }
    return true
}

// Signal processing object
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
        
        // buy:Spot purchase , sell:Spot sale , long:Long futures , short:Short futures , closesell:Futures buy to close short , closebuy:Futures sell to close long
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
            }
            if (!direction || !tradeFunc) {
                task.error = "Trading direction error:" + task.Action
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

function main() {
    // Reset log information
    if (isResetLog) {
        LogReset(1)
    }

    Log("Transaction type [buy: buy spot, sell: sell spot, long: go long in futures, short: go short in futures, closesell: buy short in futures, closebuy: sell long in futures]", Danger)
    Log("Command template:", JSON.stringify(Template), Danger)    
    if (!passPhrase || passPhrase.length == 0) {
        Log("webhook url:", `http://${serverIP}:${port}/CommandRobot`)
    } else {
        Log("webhook url:", `http://${serverIP}:${port}/CommandRobot?passPhrase=${passPhrase}`)
    }

    // createHttpBuilt-in services
    __Serve("http://0.0.0.0:" + port, serverFunc, ipWhiteList, passPhrase)

    // Initialization execution code
    if (initCode && initCode.length > 0) {
        try {
            Log("Execute initialization code:", initCode)
            eval(initCode)
        } catch(error) {
            Log("e.name:", error.name, "e.stack:", error.stack, "e.message:", error.message)
        }
    }    

    // Create signal management object
    var manager = createManager()
    
    while (true) {
        try {
            // Detect interactive controls for testing
            var cmd = GetCommand()
            if (cmd) {
                // SendHttpRequest, simulation test
                var arrCmd = cmd.split(":", 2)
                if (arrCmd[0] == "TestSignal") {
                    // {"Flag":"TestSignal","Exchange":1,"Currency":"BTC_USDT","ContractType":"swap","Price":"10000","Action":"long","Amount":"1"}
                    var signal = cmd.replace("TestSignal:", "")
                    if (!passPhrase || passPhrase.length == 0) {
                        var ret = HttpQuery(`http://${serverIP}:${port}/CommandRobot`, {"method": "POST", "body": signal})
                        Log("Response to test request:", ret)
                    } else {
                        var ret = HttpQuery(`http://${serverIP}:${port}/CommandRobot?passPhrase=${passPhrase}`, {"method": "POST", "body": signal})
                        Log("Response to test request:", ret)
                    }                    
                }
            }

            // Detect built-inHttpAfter the service receives the request, it notifies the main thread of the message and writesmanagerTask queue of the object
            var msg = threading.mainThread().peekMessage(-1)
            if (msg) {
                Log("Message received msg:", msg)
                var objSignal = JSON.parse(msg)
                if (DiffObject(Template, objSignal)) {
                    Log("Received trade signal command:", objSignal)
                    buffSignal.push(objSignal)
                    
                    // Check trading volume and exchange number
                    if (!CheckSignal(objSignal)) {
                        continue
                    }
                    
                    // Create task
                    if (objSignal["Flag"] == "TestSignal") {
                        Log("Test message received:", JSON.stringify(objSignal))
                    } else {
                        manager.newTask(objSignal)
                    }                    
                } else {
                    Log("Unrecognizable command", signal)
                }
            } else {
                Sleep(1000 * SleepInterval)
            }

            // Processing tasks
            manager.process()
            
            // Status bar displays signal
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
        } catch (error) {
            Log("e.name:", error.name, "e.stack:", error.stack, "e.message:", error.message)
        }        
    }
}

```

> Detail

https://www.fmz.com/strategy/475235

> Last Modified

2024-12-17 16:05:06
