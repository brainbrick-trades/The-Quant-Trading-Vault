
> Name

Cryptocurrency-Futures-Martingale-Strategy

> Author

发明者量化-小小梦

> Strategy Description

## Cryptocurrency futures Martingale strategy

Related articles1:https://www.fmz.com/bbs-topic/7457
Related articles2:https://www.fmz.com/digest-topic/8902

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|targetProfit|10|Target Profit|
|amount|true|Order Quantity|
|totalEq|-1|Initial Total Equity|
|isReset|false|Reset|
|pricePrecision|2|Price Precision|
|amountPrecision|2|Order quantity accuracy|
|isSimulate|false|OKEX_V5Simulation Account Options|
|SpecifyPosField||Specify the position fields to display|
|showLine|false|Show chart|
|mode|0|Mode: Bidirectional|Long only|Short only|
|maxPendingDiff|60|Maximum order distance|
|increment|false|Position doubling coefficient increment|


> Source (javascript)

``` javascript
// OKEX V5 Get Total Equity
function getTotalEquity_OKEX_V5() {
    var totalEquity = null 
    var ret = exchange.IO("api", "GET", "/api/v5/account/balance", "ccy=USDT")
    if (ret) {
        try {
            totalEquity = parseFloat(ret.data[0].details[0].eq)
        } catch(e) {
            Log("Failed to obtain total account equity!")
            return null
        }
    }
    return totalEquity
}

// Binance Futures
function getTotalEquity_Binance() {
    var totalEquity = null 
    var ret = exchange.GetAccount()
    if (ret) {
        try {
            totalEquity = parseFloat(ret.Info.totalWalletBalance)
        } catch(e) {
            Log("Failed to obtain total account equity!")
            return null
        }
    }
    return totalEquity
}

// dYdX
function getTotalEquity_dYdX() {
    var totalEquity = null 
    var ret = exchange.GetAccount()
    if (ret) {
        totalEquity = ret.Balance
    }
    return totalEquity
}

// BitMEX
function getTotalEquity_BitMEX() {
    var currency = exchange.GetCurrency()
    var arr = currency.split("_")
    if (arr.length != 2) {
        throw "Trading pair configuration error"
    }
    var baseCurrency = arr[0]
    var quoteCurrency = arr[1]
    var coinName = ""
    var scale = 0.0
    if (quoteCurrency == "USDT") {
        coinName = "USDt"
        scale = 6
    } else if (quoteCurrency == "USD") {
        coinName = "XBt"
        scale = 8
    } else {
        throw "Not Supported"
    }

    var ret = exchange.IO("api", "GET", "/api/v1/user/margin", "currency=all")
    if (ret) {
        for (var i = 0 ; i < ret.length ; i++) {
            if (coinName == ret[i].currency) {
                var equity = ret[i]["marginBalance"]
                if (equity) {
                    return parseFloat(equity) / Math.pow(10, scale)
                }                
            }
        }
    } else {
        Log("Failed to obtain total account equity!")
        return null 
    }
}

function getTotalEquity() {
    var exName = exchange.GetName()
    if (exName == "Futures_OKCoin") {
        return getTotalEquity_OKEX_V5()
    } else if (exName == "Futures_Binance") {
        return getTotalEquity_Binance()
    } else if (exName == "Futures_dYdX") {
        return getTotalEquity_dYdX()
    } else if (exName == "Futures_BitMEX") {
        return getTotalEquity_BitMEX()
    } else {
        throw "This exchange is not supported"
    }
}

function cancelAll() {
    while (1) {
        var orders = _C(exchange.GetOrders)
        if (orders.length == 0) {
            break
        }
        for (var i = 0 ; i < orders.length ; i++) {
            exchange.CancelOrder(orders[i].Id, orders[i])
            Sleep(500)
        }
        Sleep(500)
    }
}

function trade(distance, price, amount) {
    var tradeFunc = null 
    if (distance == "buy") {
        tradeFunc = exchange.Buy
    } else if (distance == "sell") {
        tradeFunc = exchange.Sell
    } else if (distance == "closebuy") {
        tradeFunc = exchange.Sell
    } else {
        tradeFunc = exchange.Buy
    }
    exchange.SetDirection(distance)
    return tradeFunc(price, amount)
}

function openLong(price, amount) {
    return trade("buy", price, amount)
}

function openShort(price, amount) {
    return trade("sell", price, amount)
}

function coverLong(price, amount) {
    return trade("closebuy", price, amount)
}

function coverShort(price, amount) {
    return trade("closesell", price, amount)
}

var buyOrderId = null
var sellOrderId = null
var chartUpdateTS = 0 

function riskControl() {
    var ts = new Date().getTime()
    var data = _G("riskControData")
    if (!data) {
        // No risk control data, initialize
        data = {timeStamp : ts, tradeTimes : 0}
        _G("riskControData", data)
    }
    
    if (ts - data.timeStamp > 1000 * 60 * 60 * 24) {
        data.tradeTimes = 0 
        data.timeStamp = ts
        Log("Risk control module reset time:", data)
    }
    data.tradeTimes++
    _G("riskControData", data)
    
    if (data.tradeTimes > 10) {
        Log("Trigger Risk Control:", data)
        return false 
    }
    return true 
}

function main() {
    var exName = exchange.GetName()    
    // SwitchOKEX V5Simulation Account
    if (isSimulate && exName == "Futures_OKCoin") {
        exchange.IO("simulate", true)
    }

    if (isReset) {
        _G(null)
        LogReset(1)
        LogProfitReset()
        LogVacuum()
        Log("Reset all data", "#FF0000")
    }

    Log("Current Mode:", ["Bidirectional", "Only go long", "Only short"][mode])

    exchange.SetContractType("swap")
    exchange.SetPrecision(pricePrecision, amountPrecision)
    Log("Set Precision", pricePrecision, amountPrecision)

    if (totalEq == -1 && !IsVirtual()) {
        var recoverTotalEq = _G("totalEq")
        if (!recoverTotalEq) {
            var currTotalEq = getTotalEquity()
            if (currTotalEq) {
                totalEq = currTotalEq
                _G("totalEq", currTotalEq)
            } else {
                throw "Failed to get initial equity"
            }
        } else {
            totalEq = recoverTotalEq
        }
    }

    var n = 1   // Adding coefficient
    while (1) {
        // Risk Control
        /*
        if (!riskControl()) {
            Sleep(1000 * 60 * 30)
            continue
        }
        */
        
        var ticker = _C(exchange.GetTicker)
        var pos = _C(exchange.GetPosition)
        if (pos.length > 1) {
            Log(pos)
            throw "Holding both long and short positions simultaneously"
        }
        // Depends on the status
        if (pos.length == 0) {
            // No positions are held, and the income will be calculated once
            if (!IsVirtual()) {
                var currTotalEq = getTotalEquity()
                if (currTotalEq) {
                    LogProfit(currTotalEq - totalEq, "Current Total Equity:", currTotalEq)
                }
            }
            
            if (mode == 0) {
                buyOrderId = openLong(ticker.Last - targetProfit, amount)
                sellOrderId = openShort(ticker.Last + targetProfit, amount)
            } else if (mode == 1) {
                buyOrderId = openLong(ticker.Last - targetProfit, amount)
            } else if (mode == 2) {
                sellOrderId = openShort(ticker.Last + targetProfit, amount)
            }
            n = 1    // Initially1
        } else if (pos[0].Type == PD_LONG) {   // Has Long Positions
            n += increment
            var price = ticker.Last
            buyOrderId = openLong(price - targetProfit * n, amount)
            sellOrderId = coverLong(pos[0].Price + targetProfit, pos[0].Amount)
        } else if (pos[0].Type == PD_SHORT) {   // Has Short Positions
            n += increment
            var price = ticker.Last
            buyOrderId = coverShort(pos[0].Price - targetProfit, pos[0].Amount)
            sellOrderId = openShort(price + targetProfit * n, amount)
        }

        if (mode == 0 && (!sellOrderId || !buyOrderId)) {
            cancelAll()
            buyOrderId = null 
            sellOrderId = null
            continue
        } else if (mode == 1 && pos.length == 0 && !buyOrderId) {
            cancelAll()
            buyOrderId = null 
            sellOrderId = null
            continue
        } else if (mode == 2 && pos.length == 0 && !sellOrderId) {
            cancelAll()
            buyOrderId = null 
            sellOrderId = null
            continue
        } else if (pos.length != 0 && (!sellOrderId || !buyOrderId)) {
            cancelAll()
            buyOrderId = null 
            sellOrderId = null
            continue
        }

        while (1) {  // Monitor Orders
            var isFindBuyId = false 
            var isFindSellId = false
            var buyOrder = null 
            var sellOrder = null 
            var orders = _C(exchange.GetOrders)
            var t = exchange.GetTicker()
            for (var i = 0 ; i < orders.length ; i++) {
                if (buyOrderId == orders[i].Id) {
                    isFindBuyId = true 
                    buyOrder = orders[i]
                }
                if (sellOrderId == orders[i].Id) {
                    isFindSellId = true 
                    sellOrder = orders[i]
                }               
            }
            if (!isFindSellId && !isFindBuyId) {    // Both buy and sell orders executed
                cancelAll()
                break
            } else if (!isFindBuyId && (mode == 0 || (mode == 2 && pos.length != 0))) {   // Buy Order Filled
                // In dual mode, only short mode has positions; when a buy order cannot be found
                Log("Buy Order Filled")
                cancelAll()
                break
            } else if (!isFindSellId && (mode == 0 || (mode == 1 && pos.length != 0))) {  // Sell Order Filled
                // In dual mode, only long mode has positions; when a sell order cannot be found
                Log("Sell Order Filled")
                cancelAll()
                break
            } else if (mode == 1 && pos.length == 0 && isFindBuyId && t && buyOrder && t.Last - buyOrder.Price > maxPendingDiff) {
                // Long-only mode. No positions. If a buy order exists and the order price is exceeded
                Log("Current price exceeds the maximum distance, cancel the buy order! Current price:", t.Last, "Order price:", buyOrder.Price, "Maximum Distance:", maxPendingDiff)
                cancelAll()
                break
            } else if (mode == 2 && pos.length == 0 && isFindSellId && t && sellOrder && sellOrder.Price - t.Last > maxPendingDiff) {
                // Short-only mode. No positions. If a sell order exists and the order price is exceeded
                Log("Current price exceeds the maximum distance, cancel the sell order! Current price:", t.Last, "Order price:", buyOrder.Price, "Maximum Distance:", maxPendingDiff)
                cancelAll()
                break
            } else if (!isFindBuyId && pos.length != 0) {
                // When there are positions but no buy orders can be found, conditions can be combined
                Log("Buy Order Filled")
                cancelAll()
                break
            } else if (!isFindSellId && pos.length != 0) {
                // Holding position, when sell order not found
                Log("Sell Order Filled")
                cancelAll()
                break
            }
            
            if (!IsVirtual()) {
                var currTotalEq = getTotalEquity()
                var pos = exchange.GetPosition()
                if (currTotalEq && pos) {
                    // LogStatus(_D(), "Current Total Equity:", currTotalEq, "Open Position:", pos)
                    var tblPos = {
                        "type" : "table",
                        "title" : "Open Position",
                        "cols" : ["Position Quantity", "Position Direction", "Average position price", "Position Profit and Loss", "Contract Code", "Custom Field / " + SpecifyPosField],
                        "rows" : []
                    }
                    var descType = ["Long Position", "Short Position"]
                    for (var posIndex = 0 ; posIndex < pos.length ; posIndex++) {
                        tblPos.rows.push([pos[posIndex].Amount, descType[pos[posIndex].Type], pos[posIndex].Price, pos[posIndex].Profit, pos[posIndex].ContractType, SpecifyPosField == "" ? "--" : pos[posIndex].Info[SpecifyPosField]])
                    }
                    
                    var tbl = {
                        "type" : "table",
                        "title" : "Data",
                        "cols" : ["Current total equity, actual profit and loss, current price, buy price/quantity, sell price/quantity."],
                        "rows" : []
                    }
                    
                    /*
                    var buyOrder = null 
                    var sellOrder = null 
                    for (var orderIndex = 0 ; orderIndex < orders.length ; orderIndex++) {
                        if (orders[orderIndex].Type == ORDER_TYPE_BUY) {
                            buyOrder = orders[orderIndex]
                        } else {
                            sellOrder = orders[orderIndex]
                        }
                    }
                    */
                    var realProfit = currTotalEq - totalEq
                    if (exchange.GetName() == "Futures_Binance") {
                        _.each(pos, function(p) {
                            realProfit += parseFloat(p.Info.unRealizedProfit)
                        })                        
                    }
                    // var t = exchange.GetTicker()
                    tbl.rows.push([currTotalEq, realProfit, t ? t.Last : "--", buyOrder ? (buyOrder.Price + "/" + buyOrder.Amount) : "--/--", sellOrder ? (sellOrder.Price + "/" + sellOrder.Amount) : "--/--"])
                    
                    // Update chart data             
                    if (t && showLine) {
                        var ts = new Date().getTime()
                        if (ts - chartUpdateTS > 60 * 1000 * 5) {
                            chartUpdateTS = ts 
                            $.PlotLine("Current Price", t.Last)
                        }
                    }
                    
                    // Update status bar data
                    LogStatus("Time:" + _D() + "\n" + "`" + JSON.stringify(tblPos) + "`" + "\n" + "`" + JSON.stringify(tbl) + "`")
                }
            }            
            Sleep(5000)
        }
        Sleep(500)
    }
}

function onexit() {
    Log("Finish the deal and cancel all pending orders")
    cancelAll()
}
```

> Detail

https://www.fmz.com/strategy/294957

> Last Modified

2023-12-01 10:57:21
