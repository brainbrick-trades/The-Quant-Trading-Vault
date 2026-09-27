
> Name

Tutorial-on-Spot-Hedging-Strategies-for-Different-Denominated-Currencies

> Author

发明者量化-小小梦

> Strategy Description

## Spot hedging strategy for different quote currencies (tutorial))

Related articles:https://www.fmz.com/digest-topic/7593

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|keepBalanceCyc|300|Balance Cycle|
|diffAsPercentage|true|Use spread percentage|
|hedgeDiffPrice|20|Hedging the difference|
|hedgeDiffPercentage|0.04|Hedging spread percentage|
|minHedgeAmount|0.005|Minimum order amount for hedging|
|maxHedgeAmount|0.2|Hedging maximum order amount|
|rateA|true|AExchange exchange rate|
|rateB|true|BExchange exchange rate|
|isReset|false|Reset all information|
|pricePrecisionA|2|APrice Precision|
|amountPrecisionA|3|AOrder quantity accuracy|
|pricePrecisionB|2|BPrice Precision|
|amountPrecisionB|3|BOrder quantity accuracy|


> Source (javascript)

``` javascript
// Global Variables
var lastKeepBalanceTS = 0

function hedge(buyEx, sellEx, price, amount) {
    var buyRoutine = buyEx.Go("Buy", price, amount)
    var sellRoutine = sellEx.Go("Sell", price, amount)
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
            if (side == "Bids" && nowAccs[i].Stocks > Math.abs(diff)) {
                available.push(i)
            } else if (price && nowAccs[i].Balance / price > Math.abs(diff)) {
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
                } else if (priceIndex && priceI && priceI < priceIndex) {
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

        var targetDiffPrice = hedgeDiffPrice
        if (diffAsPercentage) {
            targetDiffPrice = (depthA.Bids[0].Price + depthB.Asks[0].Price + depthB.Bids[0].Price + depthA.Asks[0].Price) / 4 * hedgeDiffPercentage
        }

        if (depthA.Bids[0].Price - depthB.Asks[0].Price > targetDiffPrice && Math.min(depthA.Bids[0].Amount, depthB.Asks[0].Amount) >= minHedgeAmount) {          // A -> B Handicap conditions are met            
            var price = (depthA.Bids[0].Price + depthB.Asks[0].Price) / 2
            var amount = Math.min(depthA.Bids[0].Amount, depthB.Asks[0].Amount)
            if (nowAccs[0].Stocks > minHedgeAmount && nowAccs[1].Balance / price > minHedgeAmount) {
                amount = Math.min(amount, nowAccs[0].Stocks, nowAccs[1].Balance / price, maxHedgeAmount)
                Log("TriggerA->B:", depthA.Bids[0].Price - depthB.Asks[0].Price, price, amount, nowAccs[1].Balance / price, nowAccs[0].Stocks)  // Prompt Information
                hedge(exB, exA, price, amount)
                cancelAll()
                lastKeepBalanceTS = 0
                isTrade = true 
            }            
        } else if (depthB.Bids[0].Price - depthA.Asks[0].Price > targetDiffPrice && Math.min(depthB.Bids[0].Amount, depthA.Asks[0].Amount) >= minHedgeAmount) {   // B -> A Handicap conditions are met
            var price = (depthB.Bids[0].Price + depthA.Asks[0].Price) / 2
            var amount = Math.min(depthB.Bids[0].Amount, depthA.Asks[0].Amount)
            if (nowAccs[1].Stocks > minHedgeAmount && nowAccs[0].Balance / price > minHedgeAmount) {
                amount = Math.min(amount, nowAccs[1].Stocks, nowAccs[0].Balance / price, maxHedgeAmount)
                Log("TriggerB->A:", depthB.Bids[0].Price - depthA.Asks[0].Price, price, amount, nowAccs[0].Balance / price, nowAccs[1].Stocks)  // Prompt Information
                hedge(exA, exB, price, amount)
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
        }
        LogStatus(_D(), "A->B:", depthA.Bids[0].Price - depthB.Asks[0].Price, " B->A:", depthB.Bids[0].Price - depthA.Asks[0].Price, " targetDiffPrice:", targetDiffPrice, "\n", 
            "CurrentA,Stocks:", nowAccs[0].Stocks, "FrozenStocks:", nowAccs[0].FrozenStocks, "Balance:", nowAccs[0].Balance, "FrozenBalance", nowAccs[0].FrozenBalance, "\n", 
            "CurrentB,Stocks:", nowAccs[1].Stocks, "FrozenStocks:", nowAccs[1].FrozenStocks, "Balance:", nowAccs[1].Balance, "FrozenBalance", nowAccs[1].FrozenBalance, "\n", 
            "initialA,Stocks:", initAccs[0].Stocks, "FrozenStocks:", initAccs[0].FrozenStocks, "Balance:", initAccs[0].Balance, "FrozenBalance", initAccs[0].FrozenBalance, "\n", 
            "initialB,Stocks:", initAccs[1].Stocks, "FrozenStocks:", initAccs[1].FrozenStocks, "Balance:", initAccs[1].Balance, "FrozenBalance", initAccs[1].FrozenBalance)
        Sleep(1000)
    }
}
```

> Detail

https://www.fmz.com/strategy/298752

> Last Modified

2021-07-30 16:54:39
