
> Name

Spot-Hedging-Strategy-with-Different-Quote-Currencies-Ver11

> Author

发明者量化-小小梦

> Strategy Description

## Spot hedging strategies for different denominated currencies Ver1.1

Related articles:https://www.fmz.com/digest-topic/7666

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|keepBalanceCyc|300|Balance Cycle|
|diffAsPercentage|true|Use spread percentage|
|hedgeDiffPriceA2B|20|Hedging the differenceAtoB|
|hedgeDiffPriceB2A|20|Hedging the differenceBtoA|
|hedgeDiffPercentageA2B|4|Hedging spread percentageAtoB|
|hedgeDiffPercentageB2A|4|Hedging spread percentageBtoA|
|minHedgeAmount|0.005|Minimum order amount for hedging|
|maxHedgeAmount|0.2|Hedging maximum order amount|
|rateA|true|AExchange exchange rate|
|rateB|true|BExchange exchange rate|
|isReset|false|Reset all information|
|pricePrecisionA|2|APrice Precision|
|amountPrecisionA|3|AOrder quantity accuracy|
|pricePrecisionB|2|BPrice Precision|
|amountPrecisionB|3|BOrder quantity accuracy|
|slidePrice|true|Order Slippage|
|marginType|0|Leverage type: Regular crypto|Isolated leverage|Cross leverage|




|Button|Default|Description|
|----|----|----|
|A2B|false|Modify parameters from A to B|
|B2A|false|Modify parameters from B to A|


> Source (javascript)

``` javascript
var lastKeepBalanceTS = 0

function hedge(buyEx, sellEx, priceBuy, priceSell, amount) {
    var buyRoutine = buyEx.Go("Buy", priceBuy, amount)
    var sellRoutine = sellEx.Go("Sell", priceSell, amount)
    Sleep(500)
    buyRoutine.wait()
    sellRoutine.wait()
}

function getDepthPrice(depth, side, amount) {
    var arr = depth[side]
    var sum = 0
    var price = null
    for (var i = 0 ; i < arr.length ; i++) {
        var ele = arr[i]
        sum += ele.Amount
        if (sum >= amount) {
            price = ele.Price
            break
        }
    }
    return price
}

function keepBalance(initAccs, nowAccs, depths) {
    var initSumStocks = 0
    var nowSumStocks = 0 
    _.each(initAccs, function(acc) {
        initSumStocks += acc.Stocks + acc.FrozenStocks
    })
    _.each(nowAccs, function(acc) {
        nowSumStocks += acc.Stocks + acc.FrozenStocks
    })
    
    var diff = nowSumStocks - initSumStocks
    // Calculate Coin Spread
    if (Math.abs(diff) > minHedgeAmount && initAccs.length == nowAccs.length && nowAccs.length == depths.length) {
        Log("Trigger balancing operation, balance amount:", Math.abs(diff))
        var index = -1
        var available = []
        var side = diff > 0 ? "Bids" : "Asks"
        for (var i = 0 ; i < nowAccs.length ; i++) {
            var price = getDepthPrice(depths[i], side, Math.abs(diff))
            if (side == "Bids" && nowAccs[i].Stocks * 0.9 > Math.abs(diff)) {
                available.push(i)
            } else if (side == "Asks" && price && nowAccs[i].Balance / price * 0.9 > Math.abs(diff)) {
                available.push(i)
            }
        }
        for (var i = 0 ; i < available.length ; i++) {
            if (index == -1) {
                index = available[i]
            } else {
                var priceIndex = getDepthPrice(depths[index], side, Math.abs(diff))
                var priceI = getDepthPrice(depths[available[i]], side, Math.abs(diff))
                if (side == "Bids" && priceIndex && priceI && priceI > priceIndex) {
                    index = available[i]
                } else if (side == "Asks" && priceIndex && priceI && priceI < priceIndex) {
                    index = available[i]
                }
            }
        }
        if (index == -1) {
            Log("Unable to Balance")            
        } else {
            // Balance Order
            var price = getDepthPrice(depths[index], side, Math.abs(diff))
            if (price) {
                var tradeFunc = side == "Bids" ? exchanges[index].Sell : exchanges[index].Buy
                tradeFunc(price, Math.abs(diff))
            } else {
                Log("Invalid Price", price)
            }
        }        
        return false
    } else if (!(initAccs.length == nowAccs.length && nowAccs.length == depths.length)) {
        Log("Error:", "initAccs.length:", initAccs.length, "nowAccs.length:", nowAccs.length, "depths.length:", depths.length)
        return true 
    } else {
        return true 
    }
}

function cancelAll() {
    _.each(exchanges, function(ex) {
        while (true) {
            var orders = _C(ex.GetOrders)
            if (orders.length == 0) {
                break
            }
            for (var i = 0 ; i < orders.length ; i++) {
                ex.CancelOrder(orders[i].Id, orders[i])
                Sleep(500)
            }
        }
    })
}

function updateAccs(arrEx) {
    var ret = []
    for (var i = 0 ; i < arrEx.length ; i++) {
        var acc = arrEx[i].GetAccount()
        if (!acc) {
            return null
        }
        ret.push(acc)
    }
    return ret 
}

function main() {
    var exA = exchanges[0]
    var exB = exchanges[1]
    // Precision, exchange rate settings
    if (rateA != 1) {
        // Set Exchange RateA
        exA.SetRate(rateA)
        Log("exchangeASet Exchange Rate:", rateA, "#FF0000")
    }
    if (rateB != 1) {
        // Set Exchange RateB
        exB.SetRate(rateB)
        Log("exchangeBSet Exchange Rate:", rateB, "#FF0000")
    }
    exA.SetPrecision(pricePrecisionA, amountPrecisionA)
    exB.SetPrecision(pricePrecisionB, amountPrecisionB)

    // Switch leverage mode
    for (var i = 0 ; i < exchanges.length ; i++) {
        if (exchanges[i].GetName() == "Binance" && marginType != 0) {
            if (marginType == 1) {
                Log(exchanges[i].GetName(), "Set to leverage isolated position")
                exchanges[i].IO("trade_margin")
            } else if (marginType == 2) {
                Log(exchanges[i].GetName(), "Set to leveraged full position")
                exchanges[i].IO("trade_super_margin")
            }
        }
    }
    
    if (isReset) {
        _G(null)
        LogReset(1)
        LogProfitReset()
        LogVacuum()
        Log("Reset all data", "#FF0000")
    }

    var nowAccs = _C(updateAccs, exchanges)
    var initAccs = _G("initAccs")
    if (!initAccs) {
        initAccs = nowAccs
        _G("initAccs", initAccs)
    }

    var isTrade = false 
    while (true) {
        var ts = new Date().getTime()
        var depthARoutine = exA.Go("GetDepth")
        var depthBRoutine = exB.Go("GetDepth")
        var depthA = depthARoutine.wait()
        var depthB = depthBRoutine.wait()
        if (!depthA || !depthB || depthA.Asks.length == 0 || depthA.Bids.length == 0 || depthB.Asks.length == 0 || depthB.Bids.length == 0) {
            Sleep(500)
            continue 
        }

        var targetDiffPriceA2B = hedgeDiffPriceA2B
        var targetDiffPriceB2A = hedgeDiffPriceB2A
        if (diffAsPercentage) {
            targetDiffPriceA2B = (depthA.Bids[0].Price + depthB.Asks[0].Price + depthB.Bids[0].Price + depthA.Asks[0].Price) / 4 * (hedgeDiffPercentageA2B / 100)
            targetDiffPriceB2A = (depthA.Bids[0].Price + depthB.Asks[0].Price + depthB.Bids[0].Price + depthA.Asks[0].Price) / 4 * (hedgeDiffPercentageB2A / 100)
        }

        // Drawing
        $.PlotHLine(targetDiffPriceA2B, "A->B")
        $.PlotHLine(targetDiffPriceB2A, "B->A")

        if (depthA.Bids[0].Price - depthB.Asks[0].Price > targetDiffPriceA2B && Math.min(depthA.Bids[0].Amount, depthB.Asks[0].Amount) >= minHedgeAmount) {          // A -> B Handicap conditions are met            
            var priceSell = depthA.Bids[0].Price - slidePrice
            var priceBuy = depthB.Asks[0].Price + slidePrice
            
            // Handling negative precision parameters
            if (pricePrecisionA < 0) {
                // priceSell = _N(priceSell, pricePrecisionA) - slidePrice
                priceSell = _N(priceSell - slidePrice, pricePrecisionA)
                // Log("priceSell:", priceSell, "priceSell - slidePrice:", priceSell - slidePrice, "pricePrecisionA:", pricePrecisionA, typeof(pricePrecisionA)) // Test
            }
            if (pricePrecisionB < 0) {
                // priceBuy = _N(priceBuy, pricePrecisionB) + slidePrice
                priceBuy = _N(priceBuy + slidePrice, pricePrecisionB)
                // Log("priceBuy:", priceBuy, "priceBuy + slidePrice:", priceBuy + slidePrice, "pricePrecisionB:", pricePrecisionB, typeof(pricePrecisionB)) // Test
            }
            
            var amount = Math.min(depthA.Bids[0].Amount, depthB.Asks[0].Amount)
            if (nowAccs[0].Stocks > minHedgeAmount && nowAccs[1].Balance * 0.8 / priceSell > minHedgeAmount) {
                amount = Math.min(amount, nowAccs[0].Stocks, nowAccs[1].Balance * 0.8 / priceSell, maxHedgeAmount)
                Log("TriggerA->B:", depthA.Bids[0].Price - depthB.Asks[0].Price, priceBuy, priceSell, amount, nowAccs[1].Balance * 0.8 / priceSell, nowAccs[0].Stocks)  // Prompt Information
                hedge(exB, exA, priceBuy, priceSell, amount)
                cancelAll()
                lastKeepBalanceTS = 0
                isTrade = true 
            }            
        } else if (depthB.Bids[0].Price - depthA.Asks[0].Price > targetDiffPriceB2A && Math.min(depthB.Bids[0].Amount, depthA.Asks[0].Amount) >= minHedgeAmount) {   // B -> A Handicap conditions are met
            var priceBuy = depthA.Asks[0].Price + slidePrice
            var priceSell = depthB.Bids[0].Price - slidePrice
            
            // Handling negative precision parameters
            if (pricePrecisionA < 0) {
                // priceBuy = _N(priceBuy, pricePrecisionA) + slidePrice
                priceBuy = _N(priceBuy  + slidePrice, pricePrecisionA)
                // Log("priceBuy:", priceBuy, "priceBuy  + slidePrice:", priceBuy  + slidePrice, "pricePrecisionA:", pricePrecisionA, typeof(pricePrecisionA))  // Test
            }
            if (pricePrecisionB < 0) {
                // priceSell = _N(priceSell, pricePrecisionB) - slidePrice
                priceSell = _N(priceSell - slidePrice, pricePrecisionB)
                // Log("priceSell:", priceSell, "priceSell - slidePrice:", priceSell - slidePrice, "pricePrecisionB:", pricePrecisionB, typeof(pricePrecisionB)) // Test
            }
            
            var amount = Math.min(depthB.Bids[0].Amount, depthA.Asks[0].Amount)
            if (nowAccs[1].Stocks > minHedgeAmount && nowAccs[0].Balance * 0.8 / priceBuy > minHedgeAmount) {
                amount = Math.min(amount, nowAccs[1].Stocks, nowAccs[0].Balance * 0.8 / priceBuy, maxHedgeAmount)
                Log("TriggerB->A:", depthB.Bids[0].Price - depthA.Asks[0].Price, priceBuy, priceSell, amount, nowAccs[0].Balance * 0.8 / priceBuy, nowAccs[1].Stocks)  // Prompt Information
                hedge(exA, exB, priceBuy, priceSell, amount)
                cancelAll()
                lastKeepBalanceTS = 0
                isTrade = true 
            }            
        }
        
        if (ts - lastKeepBalanceTS > keepBalanceCyc * 1000) {
            nowAccs = _C(updateAccs, exchanges)
            var isBalance = keepBalance(initAccs, nowAccs, [depthA, depthB])
            cancelAll()
            if (isBalance) {
                lastKeepBalanceTS = ts
                if (isTrade) {
                    var nowBalance = _.reduce(nowAccs, function(sumBalance, acc) {return sumBalance + acc.Balance}, 0)
                    var initBalance = _.reduce(initAccs, function(sumBalance, acc) {return sumBalance + acc.Balance}, 0)
                    LogProfit(nowBalance - initBalance, nowBalance, initBalance, nowAccs)
                    isTrade = false 
                }                
            }

            $.PlotLine("A2B", depthA.Bids[0].Price - depthB.Asks[0].Price)
            $.PlotLine("B2A", depthB.Bids[0].Price - depthA.Asks[0].Price)            
        }
        
        // Interaction
        var cmd = GetCommand()
        if (cmd) {
            Log("Command received:", cmd)
            var arr = cmd.split(":")
            if (arr[0] == "A2B") {
                Log("ModifyA2BParameters of,", diffAsPercentage ? "Parameter is the spread percentage" : "The parameter is the price difference:", arr[1])
                if (diffAsPercentage) {
                    hedgeDiffPercentageB2A = parseFloat(arr[1])
                } else {
                    hedgeDiffPriceA2B = parseFloat(arr[1])
                }
            } else if (arr[0] == "B2A") {                
                Log("ModifyB2AParameters of,", diffAsPercentage ? "Parameter is the spread percentage" : "The parameter is the price difference:", arr[1])
                if (diffAsPercentage) {
                    hedgeDiffPercentageA2B = parseFloat(arr[1])
                } else {
                    hedgeDiffPriceB2A = parseFloat(arr[1])
                }
            }
        }

        var tbl = {
            "type" : "table", 
            "title" : "Data", 
            "cols" : ["Exchange", "coin", "frozen coin", "priced coin", "frozen priced coin", "trigger spread", "current spread"], 
            "rows" : [], 
        }
        tbl.rows.push(["A:" + exA.GetName(), nowAccs[0].Stocks, nowAccs[0].FrozenStocks, nowAccs[0].Balance, nowAccs[0].FrozenBalance, "A->B:" + targetDiffPriceA2B, "A->B:" + (depthA.Bids[0].Price - depthB.Asks[0].Price)])
        tbl.rows.push(["B:" + exB.GetName(), nowAccs[1].Stocks, nowAccs[1].FrozenStocks, nowAccs[1].Balance, nowAccs[1].FrozenBalance, "B->A:" + targetDiffPriceB2A, "B->A:" + (depthB.Bids[0].Price - depthA.Asks[0].Price)])

        LogStatus(_D(), "\n", "`" + JSON.stringify(tbl) + "`")
        Sleep(1000)
    }
}
```

> Detail

https://www.fmz.com/strategy/302834

> Last Modified

2021-08-29 15:51:59
