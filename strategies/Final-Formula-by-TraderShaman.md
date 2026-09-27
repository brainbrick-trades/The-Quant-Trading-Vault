
> Name

Final-Formula-by-TraderShaman

> Author

TraderShaman

> Strategy Description

TWITTER: https://twitter.com/TraderShaman

TELEGRAM: https://t.me/tradershaman

Hello.

You see the performance of my trades in the charts.
For my all charts: https://www.fmz.com/user/6261c777972a854f5c0460520f9206bd

You can also see my different details and earnings rates on TraderWagon:
https://www.traderwagon.com/en/portfolio/3886?ref=zoh4wq9

By becoming a member of the trade platform called TraderWagon, which was established in partnership with Binance, it is possible to copy my positions with one click at the rate of your own volume.

For special - discount membership with reduced commission rates:
https://www.traderwagon.com/en/register?ref=zoh4wq9

With the slogan "Variable formulas for the volatile market", I update the values of the formula I have been working on for a long time on a daily basis. It is not possible for fixed formulas to remain healthy in this volatile market in the long run.

I make futures transactions on 4 or 5 coins that I have determined by examining detailed historical correlations. I also make changes in these coins when I deem necessary.

I update my volume and transaction rate daily according to the formulas I have created after careful and long-term studies.

I prevent liquidation to the maximum extent with carefully determined different profit taking and cost reduction points.


However, these transactions are not entirely risk-free.

I promise not high gains, but small, lossless and stable gains.

https://www.traderwagon.com/en/portfolio/3886?ref=zoh4wq9

TELEGRAM: https://t.me/tradershaman

TWITTER: https://twitter.com/TraderShaman

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|targetProfit|5|Target Profit|
|amount|0.05|Order Quantity|
|totalEq|-1|Initial Total Equity|
|isReset|false|Reset|
|pricePrecision|2|Price Precision|
|amountPrecision|2|Order quantity accuracy|
|isSimulate|false|OKEX_V5Simulation Account Options|
|SpecifyPosField||Specify the position fields to display|
|showLine|false|Show chart|


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

function getTotalEquity() {
    var exName = exchange.GetName()
    if (exName == "Futures_OKCoin") {
        return getTotalEquity_OKEX_V5()
    } else if (exName == "Futures_Binance") {
        return getTotalEquity_Binance()
    } else if (exName == "Futures_dYdX") {
        return getTotalEquity_dYdX()
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

    while (1) {
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

            buyOrderId = openLong(ticker.Last - targetProfit, amount)
            sellOrderId = openShort(ticker.Last + targetProfit, amount)
        } else if (pos[0].Type == PD_LONG) {   // Has Long Positions
            var n = 1
            var price = ticker.Last
            buyOrderId = openLong(price - targetProfit * n, amount)
            sellOrderId = coverLong(pos[0].Price + targetProfit, pos[0].Amount)
        } else if (pos[0].Type == PD_SHORT) {   // Has Short Positions
            var n = 1
            var price = ticker.Last
            buyOrderId = coverShort(pos[0].Price - targetProfit, pos[0].Amount)
            sellOrderId = openShort(price + targetProfit * n, amount)
        }

        if (!sellOrderId || !buyOrderId) {
            cancelAll()
            buyOrderId = null 
            sellOrderId = null
            continue
        } 

        while (1) {  // Monitor Orders
            var isFindBuyId = false 
            var isFindSellId = false
            var orders = _C(exchange.GetOrders)
            for (var i = 0 ; i < orders.length ; i++) {
                if (buyOrderId == orders[i].Id) {
                    isFindBuyId = true 
                }
                if (sellOrderId == orders[i].Id) {
                    isFindSellId = true 
                }               
            }
            if (!isFindSellId && !isFindBuyId) {    // Both buy and sell orders executed
                cancelAll()
                break
            } else if (!isFindBuyId) {   // Buy Order Filled
                Log("Buy Order Filled")
                cancelAll()
                break
            } else if (!isFindSellId) {  // Sell Order Filled
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
                    var buyOrder = null 
                    var sellOrder = null 
                    for (var orderIndex = 0 ; orderIndex < orders.length ; orderIndex++) {
                        if (orders[orderIndex].Type == ORDER_TYPE_BUY) {
                            buyOrder = orders[orderIndex]
                        } else {
                            sellOrder = orders[orderIndex]
                        }
                    }
                    var realProfit = currTotalEq - totalEq
                    if (exchange.GetName() == "Futures_Binance") {
                        _.each(pos, function(p) {
                            realProfit += parseFloat(p.Info.unRealizedProfit)
                        })                        
                    }
                    var t = exchange.GetTicker()
                    tbl.rows.push([currTotalEq, realProfit, t ? t.Last : "--", (buyOrder.Price + "/" + buyOrder.Amount), (sellOrder.Price + "/" + sellOrder.Amount)])
                    
                    // Update chart data             
                    if (t && showLine) {
                        _.each(pos, function(p) {
                            $.PlotLine(descType[p.Type] + "Position Price", p.Price)
                        })
                        $.PlotLine("Buy order listing price", buyOrder.Price)
                        $.PlotLine("Sell order listing price", sellOrder.Price)
                        $.PlotLine("Current Price", t.Last)
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

https://www.fmz.com/strategy/371272

> Last Modified

2022-11-20 02:07:07
