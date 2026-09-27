
> Name

Step-by-Step-Position-Adding-Trading-Strategy-Based-on-EMA-Trend-Filtering-Tutorial

> Author

发明者量化-小小梦



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|targetProfit|Target Profit|Target Profit|
|amount|Order volume | Order volume|
|totalEq|Initial total equity|Initial total equity|
|isReset|Reset | Reset|
|pricePrecision|Price Precision|Price Precision|
|amountPrecision|Order quantity accuracy|Order quantity accuracy|
|isSimulate|If the added exchange object is the API KEY of OKEX_V5 simulated disk, check this option to switch to simulated disk | OKEX_V5 simulated disk option|
|ratio|Add/close position distance ratio | Add/close position distance ratio|
|contractType|Contract Code|Contract Code|
|isAmountForUSDT|Press U to place an order. Writing 100 means the open position is worth 100 U | Press U to place the order|
|oneCtValue|One contract is worth one coin on Binance. For example, one contract on OKX ETH is worth 0.1 coins. |One contract value|
|setAddCounter|Forced number of positions to be added, used for recovery when migrating equipment | Forced number of additions|
|reserve|Margin reserve percentage | Margin reserve percentage|
|marginLevel||Leverage value|
|maxAddCounter|Maximum add-on times | Maximum add-on times|
|isDoubling|Whether to double and increase the position, check Double and increase the position | Whether to double and increase the position|
|interval|Polling Interval|Polling Interval|
|isMaxAddCounterClear|Reach the maximum number of positions to clear | Whether to reach the maximum number of positions to clear|


> Source (javascript)

``` javascript
/*backtest
start: 2024-10-01 00:00:00
end: 2025-04-23 00:00:00
period: 1h
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"ETH_USDT"}]
args: [["targetProfit",20],["amount",20],["amountPrecision",3],["isAmountForUSDT",true]]
*/

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

function getTotalEquity() {
    var exName = exchange.GetName()
    if (exName == "Futures_OKCoin") {
        return getTotalEquity_OKEX_V5()
    } else if (exName == "Futures_Binance") {
        return getTotalEquity_Binance()
    } else {
        throw "This exchange is not supported"
    }
}

function ceilToDecimals(value, decimals) {
    const factor = Math.pow(10, decimals);
    return Math.ceil(value * factor) / factor;
}

function cancelAll() {
    while (1) {
        var orders = _C(exchange.GetOrders)
        if (orders.length == 0) {
            break
        }
        for (var i = 0 ; i < orders.length ; i++) {
            exchange.CancelOrder(orders[i].Id, orders[i])
            Sleep(interval)
        }
        Sleep(interval)
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

function plotRecords(c, buyOrder, sellOrder, pos) {
    var bars = _C(exchange.GetRecords)
    if (bars.length == 0) {
        return  
    }

    bars.forEach(function(bar, index) {
        c.begin(bar)
        if (index == bars.length - 1) {
            if (buyOrder) {
                c.hline(buyOrder.Price, "buy", "rgba(255, 0, 0, 0.2)", "dotted")
            }
            if (sellOrder) {
                c.hline(sellOrder.Price, "sell", "rgba(0, 255, 0, 0.2)", "dotted")
            }
            if (pos && pos.length == 1) {
                c.hline(pos[0].Price, "pos", "rgba(0, 0, 255, 0.2)", "dashed")
            }
        }
        c.close()
    })
}

var buyOrderId = null
var sellOrderId = null
var logStatusMsgBuff = ""

function main() {
    var exName = exchange.GetName()    
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

    exchange.SetContractType(contractType)
    exchange.SetPrecision(pricePrecision, amountPrecision)
    Log("Set Precision", pricePrecision, amountPrecision)
    exchange.SetMarginLevel(marginLevel)

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

    var addCounter = _G("addCounter")
    if (!addCounter) {
        addCounter = 1
        if (setAddCounter != -1) {
            addCounter = setAddCounter
        }
        _G("addCounter", addCounter)
    } else {
        addCounter -= 1
    }

    let c = KLineChart({
        overlay: true
    })
    
    var isLock = false 
    while (true) {
        var ticker = _C(exchange.GetTicker)        
        var pos = _C(exchange.GetPosition)
        if (pos.length > 1) {
            Log(pos)
            throw "Holding both long and short positions simultaneously"
        }

        var r = _C(exchange.GetRecords, 60 * 60)
        var ema = TA.EMA(r, 60)
        if (Math.abs(ticker.Last - ema[ema.length - 2]) / ema[ema.length - 2] > 0.03) {
            cancelAll()
            isLock = true 
        }
        if (Math.abs(ticker.Last - ema[ema.length - 2]) / ema[ema.length - 2] < 0.02) {
            isLock = false 
        }
        if (isLock) {
            LogStatus(_D(), "pause, Detection threshold:", _N(Math.abs(ticker.Last - ema[ema.length - 2]) / ema[ema.length - 2], 3), logStatusMsgBuff)
            plotRecords(c, null, null, pos)
            Sleep(interval)
            continue 
        }

        var currentAcc = _C(exchange.GetAccount)
        if (currentAcc.Balance < totalEq * reserve) {
            throw "no money, stop"
        }

        if (addCounter > maxAddCounter) {
            LogStatus(_D(), "Added positions have reached the limit", logStatusMsgBuff)
            if (isMaxAddCounterClear && pos.length >= 1) {
                Log("Add-ons have reached the limit, cancel order, clear position")
                cancelAll()
                if (pos[0].Type == PD_LONG) {
                    var coverId = coverLong(-1, pos[0].Amount)
                } else if (pos[0].Type == PD_SHORT) {
                    var coverId = coverShort(-1, pos[0].Amount)
                }
                addCounter = 1
            }
            continue
        }

        if (pos.length == 0) {
            if (!IsVirtual()) {
                var currTotalEq = getTotalEquity()
                if (currTotalEq) {
                    LogProfit(currTotalEq - totalEq, "Current Total Equity:", currTotalEq)
                }
            }

            var tradeAmountLong = amount
            var tradeAmountShort = amount
            if (isAmountForUSDT) {
                tradeAmountLong = ceilToDecimals(tradeAmountLong * 1.01 / (ticker.Last - targetProfit / 5) / oneCtValue, amountPrecision)
                tradeAmountShort = ceilToDecimals(tradeAmountShort * 1.01 / (ticker.Last + targetProfit / 5) / oneCtValue, amountPrecision)
            }

            buyOrderId = openLong(ticker.Last - targetProfit / 5, tradeAmountLong)
            sellOrderId = openShort(ticker.Last + targetProfit / 5, tradeAmountShort)

            addCounter = 1
            _G("addCounter", addCounter)
        } else if (pos[0].Type == PD_LONG) {
            var n = ratio
            var price = ticker.Last
            var addAmount = isDoubling ? pos[0].Amount : (isAmountForUSDT ? (ceilToDecimals(amount * 1.01 / (price - targetProfit * n) / oneCtValue, amountPrecision)) : amount)
            buyOrderId = openLong(price - targetProfit * n, addAmount)
            sellOrderId = coverLong(pos[0].Price + targetProfit, pos[0].Amount)

            addCounter++
            _G("addCounter", addCounter)
        } else if (pos[0].Type == PD_SHORT) {
            var n = ratio
            var price = ticker.Last
            var addAmount = isDoubling ? pos[0].Amount : (isAmountForUSDT ? (ceilToDecimals(amount * 1.01 / (price + targetProfit * n) / oneCtValue, amountPrecision)) : amount)
            buyOrderId = coverShort(pos[0].Price - targetProfit, pos[0].Amount)
            sellOrderId = openShort(price + targetProfit * n, addAmount)

            addCounter++
            _G("addCounter", addCounter)
        }

        if (!sellOrderId || !buyOrderId) {
            cancelAll()
            buyOrderId = null 
            sellOrderId = null
            continue
        } 

        while (1) { 
            var isFindBuyId = false 
            var isFindSellId = false
            var orders = _C(exchange.GetOrders)
            var buyOrder = null 
            var sellOrder = null 
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
            if (!isFindSellId && !isFindBuyId) {    
                cancelAll()
                break
            } else if (!isFindBuyId) {   
                Log("Buy Order Filled")
                cancelAll()
                break
            } else if (!isFindSellId) {  
                Log("Sell Order Filled")
                cancelAll()
                break
            }

            var acc = _C(exchange.GetAccount)
            var tbl = {"type": "table", "title": "data", "cols": ["data", "symbol", "type", "price", "amount"], "rows": []}
            if (buyOrder) {
                tbl.rows.push(["Order", buyOrder.Symbol, buyOrder.Type == ORDER_TYPE_BUY ? "buy" : "sell", buyOrder.Price, buyOrder.Amount])
            }
            if (sellOrder) {
                tbl.rows.push(["Order", sellOrder.Symbol, sellOrder.Type == ORDER_TYPE_BUY ? "buy" : "sell", sellOrder.Price, sellOrder.Amount])
            }
            if (pos && pos.length == 1) {
                tbl.rows.push(["Open Position", pos[0].Symbol, pos[0].Type == PD_LONG ? "Many" : "Empty", pos[0].Price, pos[0].Amount])
            }

            logStatusMsgBuff = "Current Equity:" + acc.Equity + ", Initial Equity:" + totalEq + (!IsVirtual() ? ", Floating profit and loss:" + (acc.Equity - totalEq) : "") + ", Number of positions added:" + addCounter + "\n`" + JSON.stringify(tbl) + "`"
            LogStatus(_D(), "Current Equity:", acc.Equity, ", Initial Equity:", totalEq, !IsVirtual() ? ", Floating profit and loss:" + (acc.Equity - totalEq) : "", ", Number of positions added:" + addCounter, 
                "\n`" + JSON.stringify(tbl) + "`")

            plotRecords(c, buyOrder, sellOrder, pos)            
            Sleep(interval)
        }
        Sleep(interval)
    }
}

function onexit() {
    Log("Finish the deal and cancel all pending orders")
    cancelAll()
}
```

> Detail

https://www.fmz.com/strategy/492116

> Last Modified

2025-04-27 13:32:36
