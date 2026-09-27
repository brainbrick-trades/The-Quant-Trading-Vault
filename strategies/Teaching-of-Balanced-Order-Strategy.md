
> Name

Teaching-of-Balanced-Order-Strategy

> Author

发明者量化-小小梦

> Strategy Description

## The strategy principle is very simple
Essentially a dynamic balancing strategy, just designed as pre-placed orders. Strategy is for teaching purposes, it has not been tested extensively in live trading, use caution in live trading.
2020.09.04 OKEXQuantitative Trading Premium Club Zhengzhou session topic explanation strategy.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|IsReset|false|Restore Data|
|BalanceDistance|500|Balanced asset value (pricing currency))|




|Button|Default|Description|
|----|----|----|
|stop|__button__|pause|
|continue|__button__|Continue|


> Source (javascript)

``` javascript
var Shannon = {
	// member
    e : exchanges[0],
    arrPlanOrders : [],
    distance : BalanceDistance,
    account : null,
    ticker : null, 
    initAccount : null,
    isAskPending : false,
    isBidPending : false,

    // function 
    CancelAllOrders : function (e) {
        while(true) {
            var orders = _C(e.GetOrders)
            if(orders.length == 0) {
                return 
            }
            Sleep(500)
            for(var i = 0; i < orders.length; i++) {
                e.CancelOrder(orders[i].Id, orders[i])
                Sleep(500)
            }
        }
    },

    Balance : function () {
        if (this.arrPlanOrders.length == 0) {
            this.CancelAllOrders(this.e)
            var acc = _C(this.e.GetAccount)
            this.account = acc
            var askPendingPrice = (this.distance + acc.Balance) / acc.Stocks
            var bidPendingPrice = (acc.Balance - this.distance) / acc.Stocks
            var askPendingAmount = this.distance / 2 / askPendingPrice
            var bidPendingAmount = this.distance / 2 / bidPendingPrice

            this.arrPlanOrders.push({tradeType : "ask", price : askPendingPrice, amount : askPendingAmount}) 
            this.arrPlanOrders.push({tradeType : "bid", price : bidPendingPrice, amount : bidPendingAmount})
        } else if(this.isAskPending == false && this.isBidPending == false) {
            for(var i = 0; i < this.arrPlanOrders.length; i++) {
                var tradeFun = this.arrPlanOrders[i].tradeType == "ask" ? this.e.Sell : this.e.Buy
                var id = tradeFun(this.arrPlanOrders[i].price, this.arrPlanOrders[i].amount)
                if(id) {
                	this.isAskPending = this.arrPlanOrders[i].tradeType == "ask" ? true : this.isAskPending
                	this.isBidPending = this.arrPlanOrders[i].tradeType == "bid" ? true : this.isBidPending
                } else {
                	Log("Pending order failed, clearing!")
                	this.CancelAllOrders(this.e)
                	return 
                }
            }
        }

        if(this.isBidPending || this.isAskPending) {
            var orders = _C(this.e.GetOrders)
            Sleep(1000)
            var ticker = _C(this.e.GetTicker)
            this.ticker = ticker
            if(this.isAskPending) {
                var isFoundAsk = false 
                for (var i = 0; i < orders.length; i++) {
                    if(orders[i].Type == ORDER_TYPE_SELL) {
                        isFoundAsk = true
                    }
                }
                if(!isFoundAsk) {
                    Log("Sell order completed, order cancelled, reset")
                    this.CancelAllOrders(this.e)
                    this.arrPlanOrders = []
                    this.isAskPending = false 
                    this.isBidPending = false 
                    LogProfit(this.CalcProfit(ticker))
                    return 
                }
            }
            if(this.isBidPending) {
                var isFoundBid = false 
                for(var i = 0; i < orders.length; i++) {
                    if(orders[i].Type == ORDER_TYPE_BUY) {
                        isFoundBid = true
                    }
                }
                if(!isFoundBid) {
                    Log("Buy order completed, order cancelled, reset")
                    this.CancelAllOrders(this.e)
                    this.arrPlanOrders = []
                    this.isAskPending = false 
                    this.isBidPending = false 
                    LogProfit(this.CalcProfit(ticker))
                    return 
                }
            }        
        }
    }, 
    ShowTab : function() {
        var tblPlanOrders = {
            type : "table", 
            title : "Planned Orders", 
            cols : ["Direction", "Price", "Quantity""], 
            rows : []
        }
        for(var i = 0; i < this.arrPlanOrders.length; i++) {
            tblPlanOrders.rows.push([this.arrPlanOrders[i].tradeType, this.arrPlanOrders[i].price, this.arrPlanOrders[i].amount])
        }

        var tblAcc = {
            type : "table", 
            title : "Account Information", 
            cols : ["type", "Stocks", "FrozenStocks", "Balance", "FrozenBalance"], 
            rows : []            
        }
        tblAcc.rows.push(["initial", this.initAccount.Stocks, this.initAccount.FrozenStocks, this.initAccount.Balance, this.initAccount.FrozenBalance])
        tblAcc.rows.push(["Current", this.account.Stocks, this.account.FrozenStocks, this.account.Balance, this.account.FrozenBalance])
        
        return "Time:" + _D() + "\n `" + JSON.stringify([tblPlanOrders, tblAcc]) + "`" + "\n" + "ticker:" + JSON.stringify(this.ticker)
    },
    CalcProfit : function(ticker) {
        var acc = _C(this.e.GetAccount)
        this.account = acc
        return (this.account.Balance - this.initAccount.Balance) + (this.account.Stocks - this.initAccount.Stocks) * ticker.Last
    },
    Init : function() {
        this.initAccount = _C(this.e.GetAccount)
        if(IsReset) {
            var acc = _G("account")
            if(acc) {
                this.initAccount = acc 
            } else {
                Log("Failed to restore initial account information! Running in initial state!")
                _G("account", this.initAccount)
            }
        } else {
            _G("account", this.initAccount)
            LogReset(1)
            LogProfitReset()
        }
    },
    Exit : function() {
        Log("Before stopping, cancel all pending orders...")
        this.CancelAllOrders(this.e)
    }
}

function main() {
    // Initialize
    Shannon.Init()

    // Main loop
	while(true) {
		Shannon.Balance()		
        LogStatus(Shannon.ShowTab())
        // Interaction
        var cmd = GetCommand()
        if(cmd) {
            if(cmd == "stop") {
                while(true) {
                    LogStatus("pause", Shannon.ShowTab())
                    cmd = GetCommand()
                    if(cmd) {
                        if(cmd == "continue") {
                            break
                        }
                    }
                    Sleep(1000)
                }
            }
        }
		Sleep(5000)
	}
}

function onexit() {
    Shannon.Exit()
}
```

> Detail

https://www.fmz.com/strategy/225746

> Last Modified

2020-09-04 23:17:03
