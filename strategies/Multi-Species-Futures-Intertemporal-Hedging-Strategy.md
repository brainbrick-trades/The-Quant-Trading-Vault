
> Name

Multi-Species-Futures-Intertemporal-Hedging-Strategy

> Author

发明者量化-小小梦

> Strategy Description

Related articles:https://www.fmz.com/digest-topic/7373

## Support exchange

- OKEX Futures, need to use V5 interface.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|strNearContractType|BTC-USDT-SWAP,ETH-USDT-SWAP,TRX-USDT-SWAP,LTC-USDT-SWAP|Recent contract list|
|strFarContractType|BTC-USDT-210924,ETH-USDT-210924,TRX-USDT-210924,LTC-USDT-210924|Forward contract list|
|interval|8000|Polling Interval|
|diff|0.005|Grid spread percentage|
|hedgeAmount|true|Number of contracts hedged in each grid|
|isReset|false|Whether to reset|
|isSimulate|true|Switch to simulated account|


> Source (javascript)

``` javascript
var arrNearContractType = strNearContractType.split(",")
var arrFarContractType = strFarContractType.split(",")

var nets = null
var initTotalEquity = null 
var OPEN_PLUS = 1
var COVER_PLUS = 2


function createNet(begin, diff, initAvgPrice, diffUsagePercentage) {
    if (diffUsagePercentage) {
        diff = diff * initAvgPrice
    }
    var oneSideNums = 3
    var up = []
    var down = []
    for (var i = 0 ; i < oneSideNums ; i++) {
        var upObj = {
            sell : false, 
            price : begin + diff / 2 + i * diff
        }
        up.push(upObj)

        var j = (oneSideNums - 1) - i
        var downObj = {
            sell : false,
            price : begin - diff / 2 - j * diff
        }
        if (downObj.price <= 0) {  // Price cannot be less than or equal to0 
            continue
        }
        down.push(downObj)
    }
    return down.concat(up)
}

function createCfg(symbol) {
    var cfg = {
        extension: {
            layout: 'single', 
            height: 300,
            col: 6
        },
        title: {
            text: symbol
        },
        xAxis: {
            type: 'datetime'
        },
        series: [{
            name: 'plus',
            data: []
        }]
    }
    return cfg
}

function formatSymbol(originalSymbol) {
    var arr = originalSymbol.split("-")
    return [arr[0] + "_" + arr[1], arr[0], arr[1]]
}

function main() {	
    if (isSimulate) {
    	exchange.IO("simulate", true)  // Switch to simulation environment
    	Log("only supportOKEX V5 API,Switch toOKEX V5 Simulation Account:")
    } else {
    	exchange.IO("simulate", false)  // Switch to real offer
    	Log("only supportOKEX V5 API,Switch toOKEX V5 Live trading:")
    }    
    if (exchange.GetName() != "Futures_OKCoin") {
    	throw "Supports OKEX futures"
    }

    // Initialize
    if (isReset) {
        _G(null)
        LogReset(1)
        LogProfitReset()
        LogVacuum()
        Log("Reset all data", "#FF0000")
    }

    // Initialization tag
    var isFirst = true 

    // Income print cycle
    var preProfitPrintTS = 0
    // Total Equity
    var totalEquity = 0
    var posTbls = []   // Position table array

    // StatementarrCfg
    var arrCfg = []
    _.each(arrNearContractType, function(ct) {
        arrCfg.push(createCfg(formatSymbol(ct)[0]))
    })
    var objCharts = Chart(arrCfg)
    objCharts.reset()
    
    // Create object
    var exName = exchange.GetName() + "_V5"
    var nearConfigureFunc = $.getConfigureFunc()[exName]
    var farConfigureFunc = $.getConfigureFunc()[exName]
    var nearEx = $.createBaseEx(exchange, nearConfigureFunc)
    var farEx = $.createBaseEx(exchange, farConfigureFunc)

    // Pre-write contracts that need to be subscribed
    _.each(arrNearContractType, function(ct) {
        nearEx.pushSubscribeSymbol(ct)
    })
    _.each(arrFarContractType, function(ct) {
        farEx.pushSubscribeSymbol(ct)
    })

    while (true) {
        var ts = new Date().getTime()
        // Get market data
        nearEx.goGetTickers()
        farEx.goGetTickers()
        var nearTickers = nearEx.getTickers()
        var farTickers = farEx.getTickers()  
        if (!farTickers || !nearTickers) {
            Sleep(2000)
            continue
        }

        var tbl = {
            type : "table",
            title : "Forward - recent price difference",
            cols : ["Trading pair, "forward", "near-term", "hedge", "reverse hedge""],
            rows : []
        }        
        
        var subscribeFarTickers = []
        var subscribeNearTickers = []
        _.each(farTickers, function(farTicker) {
            _.each(arrFarContractType, function(symbol) {
                if (farTicker.originalSymbol == symbol) {
                    subscribeFarTickers.push(farTicker)
                }
            })
        })

        _.each(nearTickers, function(nearTicker) {
            _.each(arrNearContractType, function(symbol) {
                if (nearTicker.originalSymbol == symbol) {
                    subscribeNearTickers.push(nearTicker)
                }
            })
        })

        var pairs = []        
        _.each(subscribeFarTickers, function(farTicker) {
            _.each(subscribeNearTickers, function(nearTicker) {                
                if (farTicker.symbol == nearTicker.symbol) {
                    var pair = {symbol: nearTicker.symbol, nearTicker: nearTicker, farTicker: farTicker, plusDiff: farTicker.bid1 - nearTicker.ask1, minusDiff: farTicker.ask1 - nearTicker.bid1}
                    pairs.push(pair)
                    tbl.rows.push([pair.symbol, farTicker.originalSymbol, nearTicker.originalSymbol, pair.plusDiff, pair.minusDiff])
                    for (var i = 0 ; i < arrCfg.length ; i++) {
                        if (arrCfg[i].title.text == pair.symbol) {
                            objCharts.add([i, [ts, pair.plusDiff]])
                        }                        
                    }
                }
            })
        })

        // Initialize
        if (isFirst) {
            isFirst = false 
            var recoveryNets = _G("nets")
            var recoveryInitTotalEquity = _G("initTotalEquity")
            if (!recoveryNets) {
                // Check positions
                _.each(subscribeFarTickers, function(farTicker) {
                    var pos = farEx.getFuPos(farTicker.originalSymbol, ts)
                    if (pos.length != 0) {
                        Log(farTicker.originalSymbol, pos)
                        throw "There is a position during initialization"
                    }
                })
                _.each(subscribeNearTickers, function(nearTicker) {
                    var pos = nearEx.getFuPos(nearTicker.originalSymbol, ts)
                    if (pos.length != 0) {
                        Log(nearTicker.originalSymbol, pos)
                        throw "There is a position during initialization"
                    }
                })                
                // Constructionnets
                nets = []
                _.each(pairs, function (pair) {
                    farEx.goGetAcc(pair.farTicker.originalSymbol, ts)
                    nearEx.goGetAcc(pair.nearTicker.originalSymbol, ts)
                    var obj = {
                        "symbol" : pair.symbol, 
                        "farSymbol" : pair.farTicker.originalSymbol,
                        "nearSymbol" : pair.nearTicker.originalSymbol,
                        "initPrice" : (pair.nearTicker.ask1 + pair.farTicker.bid1) / 2, 
                        "prePlus" : pair.farTicker.bid1 - pair.nearTicker.ask1,                        
                        "net" : createNet((pair.farTicker.bid1 - pair.nearTicker.ask1), diff, (pair.nearTicker.ask1 + pair.farTicker.bid1) / 2, true), 
                        "initFarAcc" : farEx.getAcc(pair.farTicker.originalSymbol, ts), 
                        "initNearAcc" : nearEx.getAcc(pair.nearTicker.originalSymbol, ts),
                        "farTicker" : pair.farTicker,
                        "nearTicker" : pair.nearTicker,
                        "farPos" : null, 
                        "nearPos" : null,
                    }
                    nets.push(obj)
                })
                var currTotalEquity = getTotalEquity()
                if (currTotalEquity) {
                	initTotalEquity = currTotalEquity
                } else {
                	throw "Failed to initialize total equity!"
                }                
            } else {
                // Restore
                nets = recoveryNets
                initTotalEquity = recoveryInitTotalEquity
            }
        }

        // Retrieve the grid and check if a trade is triggered
        _.each(nets, function(obj) {
            var currPlus = null
            _.each(pairs, function(pair) {
                if (pair.symbol == obj.symbol) {
                    currPlus = pair.plusDiff
                    obj.farTicker = pair.farTicker
                    obj.nearTicker = pair.nearTicker
                }
            })
            if (!currPlus) {
                Log("Not found", obj.symbol, "price difference")
                return 
            }

            // Check grid, add dynamically
            while (currPlus >= obj.net[obj.net.length - 1].price) {
                obj.net.push({
                    sell : false,
                    price : obj.net[obj.net.length - 1].price + diff * obj.initPrice,
                })
            }
            while (currPlus <= obj.net[0].price) {
                var price = obj.net[0].price - diff * obj.initPrice
                if (price <= 0) {
                    break
                }
                obj.net.unshift({
                    sell : false,
                    price : price,
                })
            }
            
            // Retrieve Grid
            for (var i = 0 ; i < obj.net.length - 1 ; i++) {
                var p = obj.net[i]
                var upP = obj.net[i + 1]
                if (obj.prePlus <= p.price && currPlus > p.price && !p.sell) {
                    if (hedge(nearEx, farEx, obj.nearSymbol, obj.farSymbol, obj.nearTicker, obj.farTicker, hedgeAmount, OPEN_PLUS)) {   // Opening a hedging position
                        p.sell = true 
                    }
                } else if (obj.prePlus >= p.price && currPlus < p.price && upP.sell) {
                    if (hedge(nearEx, farEx, obj.nearSymbol, obj.farSymbol, obj.nearTicker, obj.farTicker, hedgeAmount, COVER_PLUS)) {   // Hedging and closing positions
                        upP.sell = false 
                    }
                }
            }
            obj.prePlus = currPlus  // Record this price difference as a cache for future judgment of crossovers
            // Add other table outputs
        })        

        if (ts - preProfitPrintTS > 1000 * 60 * 5) {   // 5Print once per minute       
        	var currTotalEquity = getTotalEquity()
        	if (currTotalEquity) {
        		totalEquity = currTotalEquity
        		LogProfit(totalEquity - initTotalEquity, "&")   // Print dynamic equity returns
        	}

        	// Check positions
        	posTbls = []  // Reset, update
            _.each(nets, function(obj) {
                var currFarPos = farEx.getFuPos(obj.farSymbol)
                var currNearPos = nearEx.getFuPos(obj.nearSymbol)
                if (currFarPos && currNearPos) {
                	obj.farPos = currFarPos
                	obj.nearPos = currNearPos
                }
                var posTbl = {
                	"type" : "table", 
                	"title" : obj.symbol, 
                	"cols" : ["Contract code, Quantity, Price"], 
                	"rows" : [] 
                }
                _.each(obj.farPos, function(pos) {
                    posTbl.rows.push([pos.symbol, pos.amount, pos.price])
                })  
                _.each(obj.nearPos, function(pos) {
                	posTbl.rows.push([pos.symbol, pos.amount, pos.price])
                })
                posTbls.push(posTbl)
            })

            preProfitPrintTS = ts
        }

        // Show grid
        var netTbls = []
        _.each(nets, function(obj) {
            var netTbl = {
            	"type" : "table",
            	"title" : obj.symbol,
            	"cols" : ["grid"],
            	"rows" : []
            }
            _.each(obj.net, function(p) {
            	var color = ""
            	if (p.sell) {
            		color = "#00FF00"
            	}
            	netTbl.rows.push([JSON.stringify(p) + color])
            })
            netTbl.rows.reverse()
            netTbls.push(netTbl)
        })

        LogStatus(_D(), "Total equity: ", totalEquity, "Initial total equity:", initTotalEquity, "Floating profit and loss:", totalEquity - initTotalEquity, 
        	"\n`" + JSON.stringify(tbl) + "`" + "\n`" + JSON.stringify(netTbls) + "`" + "\n`" + JSON.stringify(posTbls) + "`")
        Sleep(interval)
    }
}

function getTotalEquity() {
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

function hedge(nearEx, farEx, nearSymbol, farSymbol, nearTicker, farTicker, amount, tradeType) {
    var farDirection = null
    var nearDirection = null
    if (tradeType == OPEN_PLUS) {
        farDirection = farEx.OPEN_SHORT
        nearDirection = nearEx.OPEN_LONG
    } else {
        farDirection = farEx.COVER_SHORT
        nearDirection = nearEx.COVER_LONG
    }
    var nearSymbolInfo = nearEx.getSymbolInfo(nearSymbol) 
    var farSymbolInfo = farEx.getSymbolInfo(farSymbol)
    nearAmount = nearEx.calcAmount(nearSymbol, nearDirection, nearTicker.ask1, amount * nearSymbolInfo.multiplier)
    farAmount = farEx.calcAmount(farSymbol, farDirection, farTicker.bid1, amount * farSymbolInfo.multiplier)
    if (!nearAmount || !farAmount) {
        Log(nearSymbol, farSymbol, "Order quantity calculation error:", nearAmount, farAmount)
        return 
    }
    nearEx.goGetTrade(nearSymbol, nearDirection, nearTicker.ask1, nearAmount[0])
    farEx.goGetTrade(farSymbol, farDirection, farTicker.bid1, farAmount[0])
    var nearIdMsg = nearEx.getTrade()
    var farIdMsg = farEx.getTrade()
    return [nearIdMsg, farIdMsg]
}

function onexit() {
	Log("Execute cleanup function", "#FF0000")
    _G("nets", nets)
    _G("initTotalEquity", initTotalEquity)
    Log("Save data:", _G("nets"), _G("initTotalEquity"))
}

```

> Detail

https://www.fmz.com/strategy/288559

> Last Modified

2022-02-24 09:07:55
