
> Name

Simple-Cryptocurrency-Contract-Copy-Trading-Robot

> Author

发明者量化-小小梦

> Strategy Description

## Simple cryptocurrency contract copy trading robot

Related articles:https://www.fmz.com/bbs-topic/6821

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|refCurrency|ETH_USD|Copy Trading Pair|
|refCt|quarter|Copy contract|
|isSimulate|false|Use Demo Account|
|pricePrecision|2|Price Precision|
|amountPrecision|false|Order quantity accuracy|


> Source (javascript)

``` javascript
/*backtest
start: 2021-03-18 00:00:00
end: 2021-04-07 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_OKCoin","currency":"BTC_USD"},{"eid":"Futures_OKCoin","currency":"BTC_USD"},{"eid":"Futures_OKCoin","currency":"BTC_USD"}]
*/

function test() {
    // Test Function
    var ts = new Date().getTime()    
    if (ts % (1000 * 60 * 60 * 6) > 1000 * 60 * 60 * 5.5) {
        Sleep(1000 * 60 * 10)
    	var nowPosAmount = getPosAmount(_C(exchange.GetPosition), refCt)
    	var longPosAmount = nowPosAmount.long
    	var shortPosAmount = nowPosAmount.short
        var x = Math.random()
        if (x > 0.7) {
        	exchange.SetDirection("buy")
            exchange.Buy(-1, _N(Math.max(1, x * 10), 0), "Reference account test order opening#FF0000")
        } else if(x < 0.2) {
        	exchange.SetDirection("sell")
            exchange.Sell(-1, _N(Math.max(1, x * 10), 0), "Reference account test order opening#FF0000")
        } else if(x >= 0.2 && x <= 0.5 && longPosAmount > 4) {
        	exchange.SetDirection("closebuy")
        	exchange.Sell(-1, longPosAmount, "Reference account test order closing#FF0000")
        } else if(shortPosAmount > 4) {
        	exchange.SetDirection("closesell")
        	exchange.Buy(-1, _N(shortPosAmount / 2, 0), "Reference account test order closing#FF0000")
        }
    }
}

function getPosAmount(pos, ct) {
    var longPosAmount = 0
    var shortPosAmount = 0
    _.each(pos, function(ele) {
    	if (ele.ContractType == ct && ele.Type == PD_LONG) {
    		longPosAmount = ele.Amount
    	} else if (ele.ContractType == ct && ele.Type == PD_SHORT) {
    		shortPosAmount = ele.Amount
    	}
    })
    return {long: longPosAmount, short: shortPosAmount}
}

function trade(e, ct, type, delta) {
    var nowPosAmount = getPosAmount(_C(e.GetPosition), ct)
    var nowAmount = type == PD_LONG ? nowPosAmount.long : nowPosAmount.short
    if (delta > 0) {
        // Open Position
        var tradeFunc = type == PD_LONG ? e.Buy : e.Sell
        e.SetDirection(type == PD_LONG ? "buy" : "sell")
        tradeFunc(-1, delta)
    } else if (delta < 0) {
        // Close Position
        var tradeFunc = type == PD_LONG ? e.Sell : e.Buy
        e.SetDirection(type == PD_LONG ? "closebuy" : "closesell")
        if (nowAmount <= 0) {
        	Log("No Position Detected")
        	return 
        }
        tradeFunc(-1, Math.min(nowAmount, Math.abs(delta)))
    } else {
    	throw "Error"
    }
}

function main() {
    LogReset(1)
    if (exchanges.length < 2) {
        throw "Exchange without copy trading"
    }
    var exName = exchange.GetName()
    // Detect reference exchange
    if (!exName.includes("Futures_")) {
        throw "Only supports futures copy trading"
    }
    Log("Start monitoring", exName, "exchange", "#FF0000")
    
    // Detect copy trading exchange
    for (var i = 1 ; i < exchanges.length ; i++) {
        if (exchanges[i].GetName() != exName) {
            throw "The futures exchange followed by the order is different from the reference exchange.!"
        }
    }
    
    // Set trading pair, contract
    _.each(exchanges, function(e) {
    	if (!IsVirtual()) {
    		e.SetCurrency(refCurrency)
            if (isSimulate) {
                if (e.GetName() == "Futures_OKCoin") {
                    e.IO("simulate", true)
                }
            }
    	}
        e.SetContractType(refCt)
        // Set Precision
        e.SetPrecision(pricePrecision, amountPrecision)
        Log("Settings", e.GetName(), e.GetLabel(), "Price Precision:", pricePrecision, "Order quantity accuracy:", amountPrecision)
    })

    var initRefPosAmount = getPosAmount(_C(exchange.GetPosition), refCt)
    while(true) {
        if (IsVirtual()) {    // Simulate only during backtesting
        	test()            // Test function: simulate active trading of a reference account to trigger copy trading in the follower account        
        }
    	Sleep(5000)
        var nowRefPosAmount = getPosAmount(_C(exchange.GetPosition), refCt)
        var tbl = {
            type : "table", 
            title : "Open Position",
            cols : ["Name", "Tag", "Long Position", "Short Position", "Stocks", "Account Assets", "Account Assets."(Balance)"],
            rows : []
        }
        _.each(exchanges, function(e) {
            var pos = getPosAmount(_C(e.GetPosition), refCt)
            var acc = _C(e.GetAccount)
            tbl.rows.push([e.GetName(), e.GetLabel(), pos.long, pos.short, acc.Stocks, acc.Balance])
        })
        LogStatus(_D(), "\n`" + JSON.stringify(tbl) + "`")
        
        // Calculate position change amount
        var longPosDelta = nowRefPosAmount.long - initRefPosAmount.long
        var shortPosDelta = nowRefPosAmount.short - initRefPosAmount.short

        // Detect changes
        if (longPosDelta == 0 && shortPosDelta == 0) {
        	continue
        } else {
        	// Position change detected
        	for (var i = 1 ; i < exchanges.length ; i++) {
        		// Execute long action
        		if (longPosDelta != 0) {
        			Log(exchanges[i].GetName(), exchanges[i].GetLabel(), "Execute long position copy, change amount:", longPosDelta)
        		    trade(exchanges[i], refCt, PD_LONG, longPosDelta)
        		}
        		// Execute short action
        		if (shortPosDelta != 0) {
        			Log(exchanges[i].GetName(), exchanges[i].GetLabel(), "Execute short position copy, change amount:", shortPosDelta)
        		    trade(exchanges[i], refCt, PD_SHORT, shortPosDelta)
        		}
        	}
        }

        // After executing copy action, update
        initRefPosAmount = nowRefPosAmount
    }
}

```

> Detail

https://www.fmz.com/strategy/270012

> Last Modified

2022-09-28 18:24:28
