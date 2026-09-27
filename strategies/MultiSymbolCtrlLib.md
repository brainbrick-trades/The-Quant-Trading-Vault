
> Name

MultiSymbolCtrlLib

> Author

发明者量化-小小梦

> Strategy Description

## Explanation

Articlehttps://www.fmz.com/digest-topic/7373Template used in
The code is for reference only, use it with caution in actual trading.



> Source (javascript)

``` javascript
// Exchange interface call implementation
// OKEX V3 contract
function funcConfigure_Futures_OKCoin(self) {
    // Built-in functions can be freely written according to requirements
    var formatSymbol = function(originalSymbol) {
        // originalSymbol : LINK-USD-210423
        var arr = originalSymbol.split("-")
        var baseCurrency = arr[0]
        var quoteCurrency = arr[1]
        return [(baseCurrency + "_" + quoteCurrency).toUpperCase(), baseCurrency.toUpperCase(), quoteCurrency.toUpperCase()]    // Return data:[currency, baseCurrency, quoteCurrency]
    }

    self.interfaceGetTickers = function interfaceGetTickers() {
        // Can recognize self.subscribeSymbols Determine whether the subscribed variety needs perpetual contract market data
        var url = "https://www.okex.com/api/futures/v3/instruments/ticker"
        self.routineGetTicker = HttpQuery_Go(url)
    }

    self.waitTickers = function waitTickers() {
        var ret = []
        var arr = JSON.parse(self.routineGetTicker.wait())
        _.each(arr, function(ele) {
            ret.push({
            	bid1: parseFloat(ele.best_bid), 
            	bid1Vol: parseFloat(ele.best_bid_size), 
            	ask1: parseFloat(ele.best_ask), 
            	ask1Vol: parseFloat(ele.best_ask_size), 
            	symbol: formatSymbol(ele.instrument_id)[0], 
            	type: "Futures", 
            	originalSymbol: ele.instrument_id
            })
        })
        return ret 
    }

    self.interfaceGetAcc = function interfaceGetAcc(symbol, updateTS) {
        // Can be based onsymbolIdentify whether it is a perpetual contract
        var arr = formatSymbol(symbol)
        var url = "/api/futures/v3/accounts/" + arr[1].toLowerCase() + "-" + arr[2].toLowerCase()        
        self.routineGetAcc = self.e.Go("IO", "api", "GET", url)
    }

    self.waitAcc = function waitAcc(symbol, updateTS) {
        var acc = null 
        var ret = self.routineGetAcc.wait()
        // Determine if fully invested
        if (ret.margin_mode != "crossed") {
            Log(self.name, "Position mode is not full position!")
            return 
        }
        var balance = parseFloat(ret.equity) - parseFloat(ret.margin)
        var frozenBalance = parseFloat(ret.margin_for_unfilled)
        if (ret.currency == "USDT") {
            acc = {symbol: symbol, Stocks: 0, FrozenStocks: 0, Balance: balance, FrozenBalance: frozenBalance, originalInfo: ret}
        } else if (ret.currency == "USD") {
            acc = {symbol: symbol, Stocks: balance, FrozenStocks: frozenBalance, Balance: 0, FrozenBalance: 0, originalInfo: ret}
        }
        return acc
    }

    self.interfaceGetPos = function interfaceGetPos(symbol, updateTS) {
    	var symbolInfo = self.getSymbolInfo(symbol)
    	var url = "/api/futures/v3/" + symbol + "/position"
    	if (symbol.includes("SWAP")) {
    		url = "/api/swap/v3/" + symbol + "/position"
    	}
    	var ret = self.e.IO("api", "GET", url)
    	var positions = []
    	_.each(ret.holding, function(ele) {
    		if (ele.instrument_id == symbol && parseFloat(ele.short_qty) > 0) {   // Hold short position
    			positions.push({symbol: symbol, amount: -parseFloat(ele.short_qty) * symbolInfo.multiplier, price: parseFloat(ele.short_avg_cost), marginLevel: parseFloat(ele.leverage), originalInfo: ele})
    		}
    		if (ele.instrument_id == symbol && parseFloat(ele.long_qty) > 0) {    // Hold long position
    			positions.push({symbol: symbol, amount: parseFloat(ele.long_qty) * symbolInfo.multiplier, price: parseFloat(ele.long_avg_cost), marginLevel: parseFloat(ele.leverage), originalInfo: ele})
    		}
    	})
        return positions
    }

    self.interfaceTrade = function interfaceTrade(symbol, type, price, amount) {
        // Determine contract: delivery or perpetual
        var url = "/api/futures/v3/order"
        if (symbol.includes("SWAP")) {
            url = "/api/swap/v3/order"
        }
        var tradeType = ""
        switch(type) {
        case self.OPEN_LONG:
            tradeType = "1"
            break
        case self.OPEN_SHORT:
            tradeType = "2"
            break
        case self.COVER_LONG:
            tradeType = "3"
            break
        case self.COVER_SHORT:
            tradeType = "4"
            break
        default:
            throw "type error, type:" + type
        }
        var params = {
            "instrument_id": symbol, 
            "type": tradeType,
            "order_type": "4",
            "size": String(amount)
        }
        self.routineTrade = self.e.Go("IO", "api", "POST", url, self.encodeParams(params))
    }

    self.waitTrade = function waitTrade() {
        return self.routineTrade.wait()
    }

    self.calcAmount = function calcAmount(symbol, type, price, amount) {
        // Handle Order Quantity
        var symbolInfo = self.getSymbolInfo(symbol)
        if (!symbolInfo) {
            throw symbol + ",Unable to query transaction pair information"
        }
        var tradeAmount = _N(amount / symbolInfo.multiplier, 0)
        // Determine minimum order quantity
        if (tradeAmount < parseFloat(symbolInfo.min)) {
            Log(self.name, " tradeAmount:", tradeAmount, "Less Than", parseFloat(symbolInfo.min))
            return false 
        }
        return [tradeAmount, tradeAmount * symbolInfo.multiplier]
    }

    self.interfaceSetMarginLevel = function interfaceSetMarginLevel(symbol, marginLevel) {
        var arr = formatSymbol(symbol)
        var underlying = arr[1] + "-" + arr[2]
        var url = "/api/futures/v3/accounts/" + underlying + "/leverage"
        var params = {
        	"leverage" : String(marginLevel)
        }
        if (symbol.includes("SWAP")) {
        	url = "/api/futures/v3/accounts/" + symbol + "/leverage"
        	params = {
        		"instrument_id" : symbol,
        		"leverage" : String(marginLevel), 
        		"side" : "3"
        	}
        } else {
            var ret  = self.e.IO("api", "GET", "/api/futures/v3/accounts/" + underlying + "/leverage")
            // If it is not a perpetual contract, you need to first switch to cross margin mode. Before setting it up, check whether it is not cross margin
            if (ret.margin_mode != "crossed") { 
                self.e.IO("api", "POST", "/api/futures/v3/accounts/margin_mode", self.encodeParams({"underlying" : underlying, "margin_mode" : "crossed"}))
            }
        }
        return self.e.IO("api", "POST", url, self.encodeParams(params))
    }

    self.interfaceCalcProfit = function interfaceCalcProfit(arrInitAcc, arrNowAcc) {
    	// Calculate the total equity difference, that is, profit and loss
    	var profit = 0
        _.each(arrInitAcc, function(initAcc) {
        	_.each(arrNowAcc, function(nowAcc) {
        		if (initAcc.symbol == nowAcc.symbol) {
        			profit += nowAcc.originalInfo.equity - initAcc.originalInfo.equity
        		}
        	})
        })
        return profit
    }

    self.init = function init() {
        // Can recognize self.subscribeSymbols Determine whether the subscribed variety needs perpetual contract information
        var ret = JSON.parse(HttpQuery("https://www.okex.com/api/futures/v3/instruments"))   // Only retrieves delivery contracts, perpetual contracts can be added
        _.each(ret, function(symbolInfo) {
            self.symbolsInfo.push({
                symbol: symbolInfo.instrument_id,
                amountPrecision: self.judgePrecision(parseFloat(symbolInfo.tick_size)),
                pricePrecision: self.judgePrecision(parseFloat(symbolInfo.trade_increment)),
                multiplier: parseFloat(symbolInfo.contract_val),
                min: 1,                                                                      // OKEX Minimum 1 contract
                originalInfo: symbolInfo
            })
        })
    }
}

// Binance contract
function funcConfigure_Futures_Binance(self) {
    var formatSymbol = function (originalSymbol) {
        // BTCUSD_200925
        originalSymbol = (originalSymbol.split("_")[0]).toLowerCase()
        var baseCurrency = originalSymbol.replace(/(btc|eth|usdt|husd|ht|trx)$/, "")
        var quoteCurrency = originalSymbol.replace(baseCurrency, "")
        return [(baseCurrency + "_" + quoteCurrency).toUpperCase(), baseCurrency.toUpperCase(), quoteCurrency.toUpperCase()]
    }

    self.interfaceGetTickers = function interfaceGetTickers() {
        self.routineGetTicker = HttpQuery_Go("https://fapi.binance.com/fapi/v1/ticker/bookTicker")
    }

    self.waitTickers = function waitTickers() {
        var ret = []
        var arr = JSON.parse(self.routineGetTicker.wait())
        _.each(arr, function(ele) {
            ret.push({
                bid1: parseFloat(ele.bidPrice), 
                bid1Vol: parseFloat(ele.bidQty), 
                ask1: parseFloat(ele.askPrice), 
                ask1Vol: parseFloat(ele.askQty), 
                symbol: formatSymbol(ele.symbol)[0],
                type: "Futures", 
                originalSymbol: ele.symbol
            })
        })
        return ret 
    }

    self.interfaceGetAcc = function interfaceGetAcc(symbol, updateTS) {
        if (self.updateAccsTS != updateTS) {      // Only create concurrent data if new round acquires account information
            self.routineGetAcc = self.e.Go("IO", "api", "GET", "/fapi/v2/account")
        }
    }

    self.waitAcc = function waitAcc(symbol, updateTS) {
        var ret = null 
        if (self.updateAccsTS != updateTS) {      // Only obtain concurrent data if new round acquires account information
            ret = self.routineGetAcc.wait()            
            self.bufferGetAccRet = ret            // Since the exchange's asset data interface returns all information, avoid repeated calls and caching 
        } else {                                  // If timestamps are equal, it indicates the same round; use cached data
            ret = self.bufferGetAccRet
        }
        if (!ret) {
            return null 
        }
        return {symbol: symbol, Stocks: 0, FrozenStocks: 0, Balance: ret.availableBalance, FrozenBalance: ret.totalOpenOrderInitialMargin, originalInfo: ret}
    }

    self.interfaceGetPos = function interfaceGetPos(symbol, updateTS) {
        // GET /fapi/v2/positionRisk
        var ret = null 
        if (self.updatePosTS != updateTS) {
            ret = self.e.IO("api", "GET", "/fapi/v2/positionRisk")
            self.bufferGetPosRet = ret 
        } else {
            ret = self.bufferGetPosRet
        }
        if (!ret) {
            return null 
        } 
        var positions = []
        _.each(ret, function(ele) {
            if (ele.symbol == symbol && parseFloat(ele.positionAmt) < 0) {   // Hold short position
                positions.push({symbol: symbol, amount: parseFloat(ele.positionAmt) * symbolInfo.multiplier, price: parseFloat(ele.entryPrice), marginLevel: parseFloat(ele.leverage), originalInfo: ele})
            }
            if (ele.symbol == symbol && parseFloat(ele.positionAmt) > 0) {   // Hold long position
                positions.push({symbol: symbol, amount: parseFloat(ele.positionAmt) * symbolInfo.multiplier, price: parseFloat(ele.entryPrice), marginLevel: parseFloat(ele.leverage), originalInfo: ele})
            }
        })
        return positions        
    }

    self.interfaceTrade = function interfaceTrade(symbol, type, price, amount) {
        // POST /fapi/v1/order  symbol  side type  quantity  
        var params = {"symbol": symbol, "type": "MARKET", quantity: String(amount)}
        switch(type) {
        case self.OPEN_LONG:
            params["side"] = "BUY"
            params["positionSide"] = "LONG"
            break
        case self.OPEN_SHORT:
            params["side"] = "SELL"
            params["positionSide"] = "SHORT"
            break
        case self.COVER_LONG:
            params["side"] = "SELL"
            params["positionSide"] = "LONG"
            break
        case self.COVER_SHORT:
            params["side"] = "BUY"
            params["positionSide"] = "SHORT"
            break
        default: 
            throw "type error, type:" + type
        }

        if (!self.dualSidePosition) {
            params["positionSide"] = "BOTH"
        }
        self.routineTrade = self.e.Go("IO", "api", "POST", "/fapi/v1/order", self.encodeParams(params))
    }

    self.waitTrade = function waitTrade() {
        return self.routineTrade.wait()
    }

    self.calcAmount = function calcAmount(symbol, type, price, amount) {
        // Handle Order Quantity
        var symbolInfo = self.getSymbolInfo(symbol)
        if (!symbolInfo) {
            throw symbol + ",Unable to query transaction pair information"
        }
        var tradeAmount = _N(amount / symbolInfo.multiplier, symbolInfo.amountPrecision)
        // Determine minimum order quantity
        var notional = null
        _.each(symbolInfo.originalInfo.filters, function(filter) {
            if (filter.filterType == "MIN_NOTIONAL") {
                notional = parseFloat(filter.notional)
            }
        })
        if (typeof(notional) != "number") {
            Log("Cannot findnotional")
            return false 
        }
        if (tradeAmount < parseFloat(symbolInfo.min) || tradeAmount * price < notional) {      // Binance has additional amount restrictions
            Log(self.name, " tradeAmount:", tradeAmount, "Less Than", parseFloat(symbolInfo.min), "or ", "Value:", tradeAmount * price, "Less Thannotional:", notional)
            return false 
        }
        return [tradeAmount, tradeAmount * symbolInfo.multiplier]
    }

    self.interfaceSetMarginLevel = function interfaceSetMarginLevel(symbol, marginLevel) {
        // POST /fapi/v1/leverage   symbol leverage
        var params = {"symbol": symbol, "leverage": String(marginLevel)}
        return self.e.IO("api", "POST", "/fapi/v1/leverage", self.encodeParams(params))
    }

    self.interfaceCalcProfit = function interfaceCalcProfit(arrInitAcc, arrNowAcc) {
        // Binance Futures assets are common to every trading pair
        var profit = 0
        var initOriginalInfo = null 
        var nowOriginalInfo = null 
        _.each(arrInitAcc, function(initAcc) {
            _.each(arrNowAcc, function(nowAcc) {
                if (!initOriginalInfo && !nowOriginalInfo && initAcc.symbol == nowAcc.symbol) {
                    initOriginalInfo = initAcc.originalInfo
                    nowOriginalInfo = nowAcc.originalInfo
                }
            })
        })
        return nowOriginalInfo.totalWalletBalance - initOriginalInfo.totalWalletBalance
    }

    self.init = function init() {
        var ret = JSON.parse(HttpQuery("https://fapi.binance.com/fapi/v1/exchangeInfo"))
        _.each(ret.symbols, function(symbolInfo) {
            var min = null 
            _.each(symbolInfo.filters, function(filter) {
                if (filter.filterType == "MARKET_LOT_SIZE") {
                    min = parseFloat(filter.minQty)
                }
            })
            self.symbolsInfo.push({
                symbol: symbolInfo.symbol,
                amountPrecision: parseFloat(symbolInfo.quantityPrecision),
                pricePrecision: parseFloat(symbolInfo.pricePrecision),
                multiplier: 1,
                min: min,
                originalInfo: symbolInfo
            })
        })
        // Query position mode GET /fapi/v1/positionSide/dual
        self.dualSidePosition = self.e.IO("api", "GET", "/fapi/v1/positionSide/dual")["dualSidePosition"]   // Add attributes to the encapsulated exchange objectdualSidePosition,trueFor Bi-Directional Positions
        Log("Binance futures position mode,dualSidePositionis:", self.dualSidePosition)
    }
}

// Huobi spot
function funcConfigure_Huobi(self) {
    var formatSymbol = function(originalSymbol) {
        var baseCurrency = originalSymbol.replace(/(btc|eth|usdt|husd|ht|trx)$/, "")
        var quoteCurrency = originalSymbol.replace(baseCurrency, "")
        return [(baseCurrency + "_" + quoteCurrency).toUpperCase(), baseCurrency.toUpperCase(), quoteCurrency.toUpperCase()]
    }

    self.interfaceGetTickers = function interfaceGetTickers() {
        self.routineGetTicker = HttpQuery_Go("https://api.huobi.pro/market/tickers")
    }

    self.waitTickers = function waitTickers() {
        var ret = []
        var arr = JSON.parse(self.routineGetTicker.wait()).data
        _.each(arr, function(ele) {
            ret.push({
            	bid1: parseFloat(ele.bid), 
            	bid1Vol: parseFloat(ele.bidSize),
            	ask1: parseFloat(ele.ask), 
            	ask1Vol: parseFloat(ele.askSize),
            	symbol: formatSymbol(ele.symbol)[0],
            	type: "Spot", 
            	originalSymbol: ele.symbol
            })
        })
        return ret 
    }

    self.interfaceGetAcc = function interfaceGetAcc(symbol, updateTS) {
        if (self.updateAccsTS != updateTS) {
            self.routineGetAcc = self.e.Go("GetAccount")
        }
    }

    self.waitAcc = function waitAcc(symbol, updateTS) {
        var arr = formatSymbol(symbol)
        var ret = null 
        if (self.updateAccsTS != updateTS) {
            ret = self.routineGetAcc.wait().Info
            self.bufferGetAccRet = ret 
        } else {
            ret = self.bufferGetAccRet
        }
        if (!ret) {
            return null 
        }
        var acc = {symbol: symbol, Stocks: 0, FrozenStocks: 0, Balance: 0, FrozenBalance: 0, originalInfo: ret}
        _.each(ret.data.list, function(ele) {
            if (ele.currency == arr[1].toLowerCase()) {
                // baseCurrency
                if (ele.type == "trade") {
                    acc.Stocks = parseFloat(ele.balance)
                } else if (ele.type == "frozen") {
                    acc.FrozenStocks = parseFloat(ele.balance)
                }
            } else if (ele.currency == arr[2].toLowerCase()) {
                // quoteCurrency
                if (ele.type == "trade") {
                    acc.Balance = parseFloat(ele.balance)
                } else if (ele.type == "frozen") {
                    acc.FrozenBalance = parseFloat(ele.balance)
                }
            }
        })
        return acc
    }

    self.interfaceGetPos = function interfaceGetPos(symbol, price, initSpAcc, nowSpAcc) {
        var symbolInfo = self.getSymbolInfo(symbol)
        var sumInitStocks = initSpAcc.Stocks + initSpAcc.FrozenStocks
        var sumNowStocks = nowSpAcc.Stocks + nowSpAcc.FrozenStocks
        var diffStocks = _N(sumNowStocks - sumInitStocks, symbolInfo.amountPrecision)
        if (Math.abs(diffStocks) < symbolInfo.min / price) {
        	return []
        }
        return [{symbol: symbol, amount: diffStocks, price: null, originalInfo: {}}]
    }

    self.interfaceTrade = function interfaceTrade(symbol, type, price, amount) {
        if (typeof(self.account_id) == "undefined") {
            var acc = self.e.GetAccount()
            self.account_id = acc.Info.data.id
        }

        var tradeType = ""
        if (type == self.OPEN_LONG || type == self.COVER_SHORT) {
            tradeType = "buy-market"
        } else {
            tradeType = "sell-market"
        }

        var params = {
            "account-id": String(self.account_id),
            "symbol": symbol,
            "type": tradeType,
            "amount": String(amount),
        }
        self.routineTrade = self.e.Go("IO", "api", "POST", "/v1/order/orders/place", self.encodeParams(params))
    }

    self.waitTrade = function waitTrade() {
        return self.routineTrade.wait()
    }

    self.calcAmount = function calcAmount(symbol, type, price, amount) {
        // Get trading pair information
        var symbolInfo = self.getSymbolInfo(symbol)
        if (!symbol) {
            throw symbol + ",Unable to query transaction pair information"
        }
        var tradeAmount = null 
        var equalAmount = null  // Record coin amount
        if (type == self.OPEN_LONG || type == self.COVER_SHORT) {
            tradeAmount = _N(amount * price, parseFloat(symbolInfo.originalInfo["value-precision"]))
            // Check minimum trading volume
            if (tradeAmount < symbolInfo.originalInfo["min-order-value"]) {
                Log(self.name, " tradeAmount:", tradeAmount, "Less Than", symbolInfo.originalInfo["min-order-value"])
                return false 
            }
            equalAmount = tradeAmount / price
        } else {
            tradeAmount = _N(amount, parseFloat(symbolInfo.originalInfo["amount-precision"]))
            // Check minimum trading volume
            if (tradeAmount < symbolInfo.originalInfo["sell-market-min-order-amt"]) {
                Log(self.name, " tradeAmount:", tradeAmount, "Less Than", symbolInfo.originalInfo["sell-market-min-order-amt"])
                return false 
            }
            equalAmount = tradeAmount
        }
        return [tradeAmount, equalAmount]
    }

    self.init = function init() {
        var ret = JSON.parse(HttpQuery("https://api.huobi.pro/v1/common/symbols"))
        _.each(ret.data, function(symbolInfo) {
            self.symbolsInfo.push({
                symbol: symbolInfo.symbol,
                amountPrecision: parseFloat(symbolInfo["amount-precision"]),
                pricePrecision: parseFloat(symbolInfo["price-precision"]),
                multiplier: 1,
                min: parseFloat(symbolInfo["min-order-value"]),
                originalInfo: symbolInfo
            })
        })        
    }
}

// Binance spot
function funcConfigure_Binance(self) {
    var formatSymbol = function(originalSymbol) {
        // LTCBTC
        var baseCurrency = originalSymbol.replace(/(BTC|ETH|USDT|BNB|XRP|TRX|BUSD|EUR)$/, "")
        var quoteCurrency = originalSymbol.replace(baseCurrency, "")
        return [baseCurrency + "_" + quoteCurrency, baseCurrency, quoteCurrency]
    }

    self.interfaceGetTickers = function interfaceGetTickers() {
        self.routineGetTicker = HttpQuery_Go("https://api.binance.com/api/v3/ticker/bookTicker")
    }

    self.waitTickers = function waitTickers() {
        var ret = []
        var arr = JSON.parse(self.routineGetTicker.wait())
        _.each(arr, function(ele) {
            ret.push({
                bid1: parseFloat(ele.bidPrice), 
                bid1Vol: parseFloat(ele.bidQty),
                ask1: parseFloat(ele.askPrice), 
                ask1Vol: parseFloat(ele.askQty),
                symbol: formatSymbol(ele.symbol)[0],
                type: "Spot", 
                originalSymbol: ele.symbol
            })
        })
        return ret 
    }

    self.interfaceGetAcc = function interfaceGetAcc(symbol, updateTS) {
        if (self.updateAccsTS != updateTS) {
            self.routineGetAcc = self.e.Go("GetAccount")
        }
    }

    self.waitAcc = function waitAcc(symbol, updateTS) {
        var arr = formatSymbol(symbol)
        var ret = null 
        if (self.updateAccsTS != updateTS) {
            ret = self.routineGetAcc.wait().Info
            self.bufferGetAccRet = ret 
        } else {
            ret = self.bufferGetAccRet
        }
        if (!ret) {
            return null 
        }
        var acc = {symbol: symbol, Stocks: 0, FrozenStocks: 0, Balance: 0, FrozenBalance: 0, originalInfo: ret}
        _.each(ret.balances, function(ele) {
            if (ele.asset == arr[1]) {
                // baseCurrency
                acc.Stocks = parseFloat(ele.free)
                acc.FrozenStocks = parseFloat(ele.locked)
            } else if (ele.asset == arr[2]) {
                // quoteCurrency
                acc.Balance = parseFloat(ele.free)
                acc.FrozenBalance = parseFloat(ele.locked)
            }
        })
        return acc
    }

    self.interfaceGetPos = function interfaceGetPos(symbol, price, initSpAcc, nowSpAcc) {
        var symbolInfo = self.getSymbolInfo(symbol)
        var sumInitStocks = initSpAcc.Stocks + initSpAcc.FrozenStocks
        var sumNowStocks = nowSpAcc.Stocks + nowSpAcc.FrozenStocks
        var diffStocks = _N(sumNowStocks - sumInitStocks, symbolInfo.amountPrecision)
        if (Math.abs(diffStocks) < symbolInfo.min / price) {
            return []
        }
        return [{symbol: symbol, amount: diffStocks, price: null, originalInfo: {}}]
    }

    self.interfaceTrade = function interfaceTrade(symbol, type, price, amount) {
        var tradeType = ""
        var amountKeyName = ""
        if (type == self.OPEN_LONG || type == self.COVER_SHORT) {
            tradeType = "BUY"
            amountKeyName = "quoteOrderQty"
        } else {
            tradeType = "SELL"
            amountKeyName = "quantity"
        }

        var params = {
            "symbol" : symbol,
            "side" : tradeType,
            "type" : "MARKET"
        }
        params[amountKeyName] = String(amount)
        // Log("params:", params, "encodeParams:", self.encodeParams(params))
        self.routineTrade = self.e.Go("IO", "api", "POST", "/api/v3/order", self.encodeParams(params))
    }

    self.waitTrade = function waitTrade() {
        return self.routineTrade.wait()
    }

    self.calcAmount = function calcAmount(symbol, type, price, amount) {
        var symbolInfo = self.getSymbolInfo(symbol)
        if (!symbolInfo) {
            throw symbol + ",Unable to query transaction pair information"
        }
        var tradeAmount = null 
        var equalAmount = null 
        if (type == self.OPEN_LONG || type == self.COVER_SHORT) {
            tradeAmount = _N(amount * price, symbolInfo.amountPrecision)
            if (tradeAmount < symbolInfo.min) {
                Log(self.name, " tradeAmount:", tradeAmount, "Less Than", symbolInfo.min)
                return false 
            }
            equalAmount = tradeAmount / price
        } else {
            tradeAmount = _N(amount, symbolInfo.amountPrecision)
            if (tradeAmount * price < symbolInfo.min) {
                Log(self.name, " tradeAmount:", tradeAmount, "Less Than", symbolInfo.min)
                return false 
            }
            equalAmount = tradeAmount
        }
        return [tradeAmount, equalAmount]
    }

    self.init = function init() {
        // GET /api/v3/exchangeInfo
        var ret = JSON.parse(HttpQuery("https://api.binance.com/api/v3/exchangeInfo"))
        _.each(ret.symbols, function(symbolInfo) {
            var min = null 
            var amountPrecision = null 
            var pricePrecision = null 
            _.each(symbolInfo.filters, function(filter) {
                if (filter.filterType == "PRICE_FILTER") {
                    pricePrecision = self.judgePrecision(parseFloat(filter.tickSize))
                } else if (filter.filterType == "LOT_SIZE") {
                    amountPrecision = self.judgePrecision(parseFloat(filter.minQty))
                    // min = parseFloat(filter.minQty)   // You may also consider the nominal value, which is the amount
                } else if (filter.filterType == "MIN_NOTIONAL") {
                    min = parseFloat(filter.minNotional)
                }
            })
            self.symbolsInfo.push({
                symbol : symbolInfo.symbol,
                amountPrecision : parseFloat(amountPrecision),
                pricePrecision : parseFloat(pricePrecision),
                multiplier : 1,
                min : min,
                originalInfo : symbolInfo
            })
        })
    }
}

function funcConfigure_WexApp(self) {
    var formatSymbol = function(originalSymbol) {
        // BTC_USDT
        var arr = originalSymbol.split("_")
        var baseCurrency = arr[0]
        var quoteCurrency = arr[1]
        return [originalSymbol, baseCurrency, quoteCurrency]
    }

    self.interfaceGetTickers = function interfaceGetTickers() {
        self.routineGetTicker = HttpQuery_Go("https://api.wex.app/api/v1/public/tickers")
    }

    self.waitTickers = function waitTickers() {
        var ret = []
        var arr = JSON.parse(self.routineGetTicker.wait()).data
        _.each(arr, function(ele) {
            ret.push({
                bid1: parseFloat(ele.buy), 
                bid1Vol: parseFloat(-1),
                ask1: parseFloat(ele.sell), 
                ask1Vol: parseFloat(-1),
                symbol: formatSymbol(ele.market)[0],
                type: "Spot", 
                originalSymbol: ele.market
            })
        })
        return ret 
    }

    self.interfaceGetAcc = function interfaceGetAcc(symbol, updateTS) {
        if (self.updateAccsTS != updateTS) {
            self.routineGetAcc = self.e.Go("GetAccount")
        }
    }

    self.waitAcc = function waitAcc(symbol, updateTS) {
        var arr = formatSymbol(symbol)
        var ret = null 
        if (self.updateAccsTS != updateTS) {
            ret = self.routineGetAcc.wait().Info
            self.bufferGetAccRet = ret 
        } else {
            ret = self.bufferGetAccRet
        }
        if (!ret) {
            return null 
        }        
        var acc = {symbol: symbol, Stocks: 0, FrozenStocks: 0, Balance: 0, FrozenBalance: 0, originalInfo: ret}
        _.each(ret.exchange, function(ele) {
            if (ele.currency == arr[1]) {
                // baseCurrency
                acc.Stocks = parseFloat(ele.free)
                acc.FrozenStocks = parseFloat(ele.frozen)
            } else if (ele.currency == arr[2]) {
                // quoteCurrency
                acc.Balance = parseFloat(ele.free)
                acc.FrozenBalance = parseFloat(ele.frozen)
            }
        })
        return acc
    }

    self.interfaceGetPos = function interfaceGetPos(symbol, price, initSpAcc, nowSpAcc) {
        var symbolInfo = self.getSymbolInfo(symbol)
        var sumInitStocks = initSpAcc.Stocks + initSpAcc.FrozenStocks
        var sumNowStocks = nowSpAcc.Stocks + nowSpAcc.FrozenStocks
        var diffStocks = _N(sumNowStocks - sumInitStocks, symbolInfo.amountPrecision)
        if (Math.abs(diffStocks) < symbolInfo.min / price) {
            return []
        }
        return [{symbol: symbol, amount: diffStocks, price: null, originalInfo: {}}]
    }

    self.interfaceTrade = function interfaceTrade(symbol, type, price, amount) {
        var tradeType = ""
        if (type == self.OPEN_LONG || type == self.COVER_SHORT) {
            tradeType = "bid"
        } else {
            tradeType = "ask"
        }
        var params = {
            "market": symbol,
            "side": tradeType,
            "amount": String(amount),
            "price" : String(-1),
            "type" : "market"
        }
        self.routineTrade = self.e.Go("IO", "api", "POST", "/api/v1/private/order", self.encodeParams(params))
    }

    self.waitTrade = function waitTrade() {
        return self.routineTrade.wait()
    }

    self.calcAmount = function calcAmount(symbol, type, price, amount) {
        // Get trading pair information
        var symbolInfo = self.getSymbolInfo(symbol)
        if (!symbol) {
            throw symbol + ",Unable to query transaction pair information"
        }
        var tradeAmount = null 
        var equalAmount = null  // Record coin amount
        if (type == self.OPEN_LONG || type == self.COVER_SHORT) {
            tradeAmount = _N(amount * price, parseFloat(symbolInfo.pricePrecision))
            // Check minimum trading volume
            if (tradeAmount < symbolInfo.min) {
                Log(self.name, " tradeAmount:", tradeAmount, "Less Than", symbolInfo.min)
                return false 
            }
            equalAmount = tradeAmount / price
        } else {
            tradeAmount = _N(amount, parseFloat(symbolInfo.amountPrecision))
            // Check minimum trading volume
            if (tradeAmount < symbolInfo.min / price) {
                Log(self.name, " tradeAmount:", tradeAmount, "Less Than", symbolInfo.min / price)
                return false 
            }
            equalAmount = tradeAmount
        }
        return [tradeAmount, equalAmount]
    }

    self.init = function init() {
        var ret = JSON.parse(HttpQuery("https://api.wex.app/api/v1/public/markets"))
        _.each(ret.data, function(symbolInfo) {
            self.symbolsInfo.push({
                symbol: symbolInfo.pair,
                amountPrecision: parseFloat(symbolInfo.basePrecision),
                pricePrecision: parseFloat(symbolInfo.quotePrecision),
                multiplier: 1,
                min: parseFloat(symbolInfo.minQty),
                originalInfo: symbolInfo
            })
        })        
    }
}

// OKEXfutures V5 
function funcConfigure_Futures_OKEX_V5(self) {
    var formatSymbol = function(originalSymbol) {        
        var arr = originalSymbol.split("-")               // LTC-USD-SWAP
        return [arr[0] + "_" + arr[1], arr[0], arr[1]]
    }

    var getInstType = function() {
        var isSwap = null
        for (var i = 0 ; i < self.subscribeSymbols.length ; i++) {            
            if (i == 0) {
                isSwap = self.subscribeSymbols[i].includes("-SWAP")
            } else if (isSwap != self.subscribeSymbols[i].includes("-SWAP")) {
                throw "The subscribed contracts mix delivery and perpetual"
            }
        }
        return isSwap ? "SWAP" : "FUTURES"
    }

    self.interfaceGetTickers = function interfaceGetTickers() {
        self.routineGetTicker = HttpQuery_Go("https://www.okex.com/api/v5/market/tickers?instType=" + getInstType())
    }  

    self.waitTickers = function waitTickers() {
        var ret = []
        var arr = JSON.parse(self.routineGetTicker.wait()).data
        _.each(arr, function(ele) {
            ret.push({
                bid1: parseFloat(ele.bidPx), 
                bid1Vol: parseFloat(ele.bidSz), 
                ask1: parseFloat(ele.askPx), 
                ask1Vol: parseFloat(ele.askSz), 
                symbol: formatSymbol(ele.instId)[0], 
                type: "Futures", 
                originalSymbol: ele.instId
            })
        })
        return ret 
    }

    self.interfaceGetAcc = function interfaceGetAcc(symbol, updateTS) {
        if (self.updateAccsTS != updateTS) {      // Only create concurrent data if new round acquires account information
            self.routineGetAcc = self.e.Go("IO", "api", "GET", "/api/v5/account/balance")
        }
    }  

    self.waitAcc = function waitAcc(symbol, updateTS) {
        var ret = null 
        if (self.updateAccsTS != updateTS) {      // Only obtain concurrent data if new round acquires account information
            ret = self.routineGetAcc.wait()    
            self.bufferGetAccRet = ret            // Since the exchange's asset data interface returns all information, avoid repeated calls and caching 
        } else {                                  // If timestamps are equal, it indicates the same round; use cached data
            ret = self.bufferGetAccRet
        }
        if (!ret) {
            return null 
        }
        var arrCurrencyName = formatSymbol(symbol)
        var quoteCurrency = arrCurrencyName[2]
        var baseCurrency = arrCurrencyName[1]
        var acc = null 
        _.each(ret.data, function(obj) {
            _.each(obj.details, function(detail) {
                if (detail.availEq == "") {
                    throw "Account-level too low"
                } else if (quoteCurrency == "USDT" && detail.ccy == quoteCurrency) {
                    acc = {symbol: symbol, Stocks: 0, FrozenStocks: 0, Balance: detail.availEq, FrozenBalance: detail.ordFrozen, originalInfo: ret}
                } else if (quoteCurrency == "USD" && detail.ccy == baseCurrency) {
                    acc = {symbol: symbol, Stocks: detail.availEq, FrozenStocks: detail.ordFrozen, Balance: 0, FrozenBalance: 0, originalInfo: ret}
                }
            })
        })
        return acc
    }  

    self.interfaceGetPos = function interfaceGetPos(symbol, updateTS) {    // The implementation of futures and spot is different
        var symbolInfo = self.getSymbolInfo(symbol)
        var arrCurrencyName = formatSymbol(symbol)
        var instType = "FUTURES"
        if (symbol.includes("-SWAP")) {
            instType = "SWAP"
        }
        var ret = self.e.IO("api", "GET", "/api/v5/account/positions", "instType=" + instType + "&instId=" + symbol)
        var positions = []
        // {"code":"0","data":[],"msg":""}
        _.each(ret.data, function(ele) {
            if (Math.abs(parseFloat(ele.pos)) > 0) {
                if (ele.posSide == "long" || (ele.posSide == "net" && parseFloat(ele.pos) > 0)) {
                    positions.push({symbol: ele.instId, amount: Math.abs(parseFloat(ele.pos)) * symbolInfo.multiplier, price: parseFloat(ele.avgPx), marginLevel: parseFloat(ele.lever), originalInfo: ele})
                } else if (ele.posSide == "short" || (ele.posSide == "net" && parseFloat(ele.pos) < 0)) {
                    positions.push({symbol: ele.instId, amount: -Math.abs(parseFloat(ele.pos)) * symbolInfo.multiplier, price: parseFloat(ele.avgPx), marginLevel: parseFloat(ele.lever), originalInfo: ele})
                }
            }         
        })
        return positions
    }

    self.interfaceTrade = function interfaceTrade(symbol, type, price, amount) {
    	var params = {
    		"instId" : symbol,
    		"tdMode" : "cross",
    		"ordType" : "market",
    		"sz" : String(amount)
    	}

    	switch(type) {
        case self.OPEN_LONG:
            params["side"] = "buy"
            params["posSide"] = "long"
            break
        case self.OPEN_SHORT: 
            params["side"] = "sell"
            params["posSide"] = "short"
            break
        case self.COVER_LONG: 
            params["side"] = "sell"
            params["posSide"] = "long"
            break        
        case self.COVER_SHORT:
            params["side"] = "buy"
            params["posSide"] = "short"
            break        
        default:
            throw "type error, type:" + type
    	}
        self.routineTrade = self.e.Go("IO", "api", "POST", "/api/v5/trade/order", self.encodeParams(params))
    }  

    self.waitTrade = function waitTrade() {
        return self.routineTrade.wait()
    }  

    self.calcAmount = function calcAmount(symbol, type, price, amount, isNotLog) {
        var symbolInfo = self.getSymbolInfo(symbol)
        if (!symbolInfo) {
        	throw symbol + ",Unable to query transaction pair information"
        }
        var tradeAmount = _N(amount / symbolInfo.multiplier, 0)        
        if (tradeAmount < parseFloat(symbolInfo.min)) {
            if (typeof(isNotLog) == "undefined") {
                Log(self.name, " tradeAmount:", tradeAmount, "Less Than", parseFloat(symbolInfo.min))
            }     	
        	return false 
        }
        return [tradeAmount, tradeAmount * symbolInfo.multiplier]
    }  
    // Implement set leverage interface
    self.interfaceSetMarginLevel = function interfaceSetMarginLevel(symbol, marginLevel) {
        return self.e.IO("api", "POST", "/api/v5/account/set-leverage", self.encodeParams({"instId" : symbol, "ccy" : "USDT", "lever" : String(marginLevel), "mgnMode" : "cross"}))
    }

    self.interfaceCalcProfit = function interfaceCalcProfit(arrInitAcc, arrNowAcc) {
    	var profit = 0
    	if (arrInitAcc.length > 0 && arrNowAcc.length > 0) {
    		var initEq = 0
    		_.each(arrInitAcc[0].originalInfo.data, function(obj) {
    			_.each(obj.details, function(detail) {
    				if (detail.availEq == "") {
    					throw "Account-level too low"
    				} else if (detail.ccy == "USDT") {
    					initEq = detail.eq
    				}
    			})
    		})
    		var nowEq = 0
    		_.each(arrNowAcc[0].originalInfo.data, function(obj) {
    			_.each(obj.details, function(detail) {
    				if (detail.availEq == "") {
    					throw "Account-level too low"
    				} else if (detail.ccy == "USDT") {
    					nowEq = detail.eq
    				}
    			})
    		})
    		return nowEq - initEq
    	} else {
    		Log("Failed to calculate profit", arrInitAcc, arrNowAcc)
    		return 
    	}
        return profit
    }  

    self.init = function init() {
        _.each(["SWAP", "FUTURES"], function(instType) {          // Obtain both perpetual and delivery contract information
            var ret = JSON.parse(HttpQuery("https://www.okex.com/api/v5/public/instruments?instType=" + instType))
            _.each(ret.data, function(symbolInfo) {
                self.symbolsInfo.push({
                    symbol: symbolInfo.instId,
                    amountPrecision: self.judgePrecision(parseFloat(symbolInfo.lotSz)),
                    pricePrecision: self.judgePrecision(parseFloat(symbolInfo.tickSz)),
                    multiplier: parseFloat(symbolInfo.ctVal),
                    min: parseFloat(symbolInfo.minSz),                                                                      // OKEX Minimum 1 contract
                    originalInfo: symbolInfo
                })
            })
        })
    }
}

// Exchange object constructor
function createBaseEx(e, funcConfigure) {
    var self = {}
    self.e = e 
    self.funcConfigure = funcConfigure
    self.name = e.GetName()
    self.type = self.name.includes("Futures_") ? "Futures" : "Spot"
    self.label = e.GetLabel()
    self.fuMarginLevel = null 

    // Data member
    self.subscribeSymbols = []     // Subscribed assets
    self.bufferTickers = []        // Cache all market data
    self.bufferAccs = []           // Cache subscribed account asset data
    self.bufferPositions = []      // Cache subscribed position data
    self.symbolsInfo = []          // An array that records all market subject information
    self.bufferGetAccRet = null    // Access asset information interface cache data
    self.bufferGetPosRet = null    // Access position information interface cache data

    // Update Timestamp
    self.updateAccsTS = 0          // Update timestamp of account information
    self.updatePosTS = 0           // Update timestamp of position information

    // Concurrent thread
    self.routineGetTicker = null 
    self.routineGetAcc = null 
    self.routineTrade = null 

    // Enumeration
    self.OPEN_LONG = 0
    self.OPEN_SHORT = 1
    self.COVER_LONG = 2
    self.COVER_SHORT = 3

    // List of interfaces that need to be implemented
    var configList = ["interfaceGetTickers", "interfaceGetAcc", "interfaceGetPos", "interfaceTrade", 
        "waitTickers", "waitAcc", "waitTrade", "calcAmount", "init"]
    if (self.type == "Futures") {
        configList.push("interfaceSetMarginLevel")   // Futures also need to set up a leverage interface
        configList.push("interfaceCalcProfit")       // Futures need to calculate profit interface
    }
    // Interface to be implemented
    self.interfaceGetTickers = null   // Create a function to asynchronously fetch aggregated market data threads
    self.interfaceGetAcc = null       // Create a function to asynchronously obtain account data threads
    self.interfaceGetPos = null       // Get a position
    self.interfaceTrade = null        // Create concurrent orders
    self.waitTickers = null           // Wait and publish market data 
    self.waitAcc = null               // Wait for account concurrent data
    self.waitTrade = null             // Wait for order concurrent data
    self.calcAmount = null            // Calculate order volume based on data such as trading pair accuracy
    self.init = null                  // Initialize work and obtain accuracy and other data

    // Callback function
    self.callBack_getTrade = null     // Callback needed when executing getTrade

    // Determine precision
    self.judgePrecision = function(p) {
        var arr = p.toString().split(".")
        if (arr.length != 2) {
            if (arr.length == 1) {
                return 0
            }
            throw "judgePrecision error, p:" + String(p)
        }
        return arr[1].length
    }

    // Get information of a specific trading pair
    self.getSymbolInfo = function(symbol) {
        var ret = null 
        _.each(self.symbolsInfo, function(info) {
            if (info.symbol == symbol) {
                ret = info
            }
        })
        return ret 
    }

    self.getExName = function() {    // Get the name of the exchange object
        return self.name
    }

    self.pushInArr = function(arr, obj, attributeName) {
        var isFind = false 
        _.each(arr, function(ele) {
        	if (obj[attributeName] == ele[attributeName]) {
        		ele = obj
        		isFind = true 
        	}
        })
        if (!isFind) {
        	arr.push(obj)
        }
    }

    // encodeParams
    self.encodeParams = function(params) {
        var ret = ""
        var index = 0
        for (var key in params) {
            if (index == 0) {
                ret += key + "=" + params[key]
            } else {
                ret += "&" + key + "=" + params[key]
            }            
            index++
        }
        return ret 
    }

    // Member function        
    self.tryProcess = function(tryFunc, args) {   // Returns a null value when an exception occurs, and returns the tryFunc function call result normally.
        var ret = null 
        try {
            ret = tryFunc.apply(this, args)
        } catch (err) {
            var funcName = tryFunc.toString().match(/function\s*([^(]*)\(/)[1]   // Get function name
            Log("Error:", err, " Error message:", typeof(err.message) == "string" ? err.message : "", " Exception Function Name:", funcName, " Parameters:", typeof(args) == "undefined" ? "without" : args)    // Output the function information that caused the exception
            return null
        }
        return ret 
    }

    // Write subscribed varieties to subscribeSymbols
    self.pushSubscribeSymbol = function(symbol) {    // Only called during initialization, written into the subscription contract, used to determine the subscription contract in the interface
        self.subscribeSymbols.push(symbol)
    }

    // Create concurrent market data retrieval
    self.goGetTickers = function() {                 
        self.interfaceGetTickers()
    }

    // Fetch and publish market data
    self.getTickers = function() {                   // Get the concurrent result. Using tryProcess will cause an error if an exception occurs and will not cause the program to stop
        var ret = self.tryProcess(self.waitTickers)
        // Cache data
        if (ret) {
            self.bufferTickers = ret
        }
        return ret 
    }

    // Create order concurrency
    self.goGetTrade = function(symbol, type, price, amount) {      // Create concurrent orders without detecting exceptions
        self.interfaceTrade(symbol, type, price, amount)
        // Set callback
        self.callBack_getTrade = function(ret) {
            if (self.type == "Futures") {
                if (type == self.OPEN_LONG || type == self.OPEN_SHORT) {    
                    self.e.SetDirection(type == self.OPEN_SHORT ? "sell" : "buy")                   // Arbitrage futures short
                } else {
                    self.e.SetDirection(type == self.COVER_SHORT ? "closesell" : "closebuy")        // Close long-short hedge futures
                }
            }
            self.e.Log((type == self.OPEN_LONG || type == self.COVER_SHORT) ? LOG_TYPE_BUY : LOG_TYPE_SELL, price, amount, symbol, ret)
        }
    }

    // Get order result
    self.getTrade = function() {
        var retTradeMsg = self.tryProcess(self.waitTrade)
        if (retTradeMsg) {
            self.callBack_getTrade(retTradeMsg)
        }
        return retTradeMsg
    }

    // Create concurrent fetch for a single asset
    self.goGetAcc = function(symbol, updateTS) {
        self.interfaceGetAcc(symbol, updateTS)
    }

    // Obtain asset information related to a single subject matter
    self.getAcc = function(symbol, updateTS) {
        var ret = self.tryProcess(self.waitAcc, [symbol, updateTS])
        // Cache data
        if (ret) {
            // Update bufferAccs In the data
            self.pushInArr(self.bufferAccs, ret, "symbol")
            self.updateAccsTS = updateTS    // Update, record timestamp, does not affect the interface for obtaining account information one by one (see the interface implementation for details))
        }
        return ret
    }

    self.getFuPos = function(symbol, updateTS) {                               // Get futures positions
        var ret = self.tryProcess(self.interfaceGetPos, [symbol, updateTS])
        if (ret) {
        	_.each(ret, function(pos) {
        		self.pushInArr(self.bufferPositions, pos, "symbol")
        	})
            self.updatePosTS = updateTS
        }
        return ret 
    }

    self.getSpPos = function(symbol, price, initSpAcc, nowSpAcc) {   // Get spot positions
    	var ret = self.tryProcess(self.interfaceGetPos, [symbol, price, initSpAcc, nowSpAcc])
        if (ret) {
        	// self.bufferPositions = ret        	
        	_.each(ret, function(pos) {
        		self.pushInArr(self.bufferPositions, pos, "symbol")
        	})
        }
        if (ret.length > 1) {
        	Log("Spot position returned data error!", JSON.stringify(ret))
        }
        return ret
    }

    self.setMarginLevel = function(symbol, marginLevel) {    	
    	var ret = self.tryProcess(self.interfaceSetMarginLevel, [symbol, marginLevel])
    	if (ret) {
    		self.fuMarginLevel = marginLevel
    	}
    	return ret 
    }

    self.calcProfit = function(arrInitAcc, arrNowAcc) {
    	if (self.type == "Futures") {    		
			return self.tryProcess(self.interfaceCalcProfit, [arrInitAcc, arrNowAcc])    		
    	} else {
    		throw "Call Error"
    	}
    }

    // Execute the configuration function to configure the object
    funcConfigure(self)

    // DetectconfigListWhether the stipulated interfaces are all implemented
    _.each(configList, function(funcName) {
        if (!self[funcName]) {
            throw "Interface" + funcName + "Unrealized"
        }
    })

    // self.tryProcess(self.init)    // Execute the interfaces implemented in the configurationinitFunction
    self.init()                      // No exception detection is performed. If an error occurs, the program stops and executes the functions implemented in the interface configuration.initFunction
    return self
}

// Export Function
$.createBaseEx = createBaseEx
$.getConfigureFunc = function(exName) {
    dicRegister = {
        "Futures_OKCoin" : funcConfigure_Futures_OKCoin,
        "Huobi" : funcConfigure_Huobi,
        "Futures_Binance" : funcConfigure_Futures_Binance,
        "Binance" : funcConfigure_Binance,
        "WexApp" : funcConfigure_WexApp,
        "Futures_OKCoin_V5" : funcConfigure_Futures_OKEX_V5,        // exchange.GetName() + "_V5"
    }
    if (typeof(exName) != "undefined" && !dicRegister[exName]) {
        throw "Matching exchange configuration function not found"
    }
    return dicRegister
}

// Test Function
function main() {
    // Switch to simulated account environment
    // exchange.IO("simulate", true)   // OKEX V5 Switch Demo Account

    var fuExName = exchange.GetName() + "_V5"    // Get the exchange name, set here asOKEX V5
    Log("The name of the exchange tested is:", fuExName)
    var fuConfigureFunc = $.getConfigureFunc()[fuExName]
    var ex = $.createBaseEx(exchange, fuConfigureFunc)

    var arrTestSymbol = ["ETH-USDT-211231"]
    var ts = new Date().getTime()
    // Set the contract that needs to be subscribed
    // /*
    _.each(arrTestSymbol, function(symbol) {
        ex.pushSubscribeSymbol(symbol)
    })
    // */

    _.each(arrTestSymbol, function(symbol) {
        // Test market data retrieval
        /*
        ex.goGetTickers()
        var tickers = ex.getTickers()
        Log("tickers:", tickers)
        _.each(tickers, function(ticker) {
            if (symbol == ticker.originalSymbol) {
                Log(symbol, ticker)
            }
        })
        */

        // Test retrieving account information
        // /*
        ex.goGetAcc(symbol, ts)
        var acc = ex.getAcc(symbol, ts)
        Log("acc:", acc.symbol, acc)

        var arr1 = [acc]
        var arr2 = [acc]
        Log(ex.interfaceCalcProfit(arr1, arr2))
        // */

        // Test retrieving position information
        /*
        var pos = ex.getFuPos(symbol)  // Futures Position
        Log("pos:", symbol, pos)
        // Print trading pair information
        _.each(ex.symbolsInfo, function(symbolInfo) {
            if (_.contains(arrTestSymbol, symbolInfo.symbol)) {
                Log("symbolInfo:", symbolInfo)
            }
        })
        */

        // Order Test
        /*
        if (symbol == "LTC-USDT-SWAP") {
            var price = 170 + 170 * 0.02
            var amount = 1
            var tradeType = ex.OPEN_LONG
            var retCalc = ex.calcAmount(symbol, tradeType, price, amount)
            if (retCalc) {
                Log("retCalc:", retCalc)
                Log("symbolInfo:", ex.getSymbolInfo(symbol))
                var setMarginLevelRet = ex.setMarginLevel(symbol, 5)
                Log("setMarginLevelRet:", setMarginLevelRet)  // Print position settings
                ex.goGetTrade(symbol, tradeType, price, retCalc[0])    // Test Long Open
                // ex.goGetTrade(symbol, ex.COVER_LONG, -1, 0.004)   // Test Long Close
                var ret = ex.getTrade()
                Log(symbol, "trade ret:", ret)
            }
        }
        */

        /* Test leverage separately
        var ret = ex.setMarginLevel(symbol, 35)
        Log(ret)
        */

        /*
        if (symbol == "LTCUSDT") {
            var price = 230
            var amount = 0.01
            var tradeType = ex.OPEN_SHORT
            var retCalc = ex.calcAmount(symbol, tradeType, price, amount)
            if (retCalc) {
                Log("symbolInfo:", ex.getSymbolInfo(symbol))
                // ex.setMarginLevel(symbol, 5)
                ex.goGetTrade(symbol, tradeType, price, retCalc[0])    // Test Long Open
                // ex.goGetTrade(symbol, ex.COVER_LONG, -1, 0.004)   // Test Long Close
                var ret = ex.getTrade()
                Log(symbol, "trade ret:", ret)
            }
        }
        */
    })
}


```

> Detail

https://www.fmz.com/strategy/276298

> Last Modified

2022-05-18 11:35:37
