
> Name

Copy-Trading-Bot-V10-Requires-the-Same-Exchange-Supports-Multiple-Users-Following-and-Allows-Setting-Copy-Multiples

> Author

guohwa



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|refCurrency|ETH_USDT|Copy Trading Pair|
|refCt|swap|Copy contract|
|isSimulate|false|Whether to use a simulated account|
|pricePrecision|2|Price Precision|
|amountPrecision|2|Order quantity accuracy|


> Source (javascript)

``` javascript
/*backtest
start: 2021-03-18 00:00:00
end: 2021-04-07 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_OKCoin","currency":"BTC_USD"},{"eid":"Futures_OKCoin","currency":"BTC_USD"},{"eid":"Futures_OKCoin","currency":"BTC_USD"}]
*/

//var followRatio = 2; // Set the proportion and range of following orders0-100Custom
var followRatios = [1, 3, 4]; //Multiple copy accounts, set different copy ratios respectively. The first one is the reference account and the default is1

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
    	Sleep(500)
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
        } else if(nowRefPosAmount.long == 0 && nowRefPosAmount.short == 0){
            // Refer to accounts where both long and short positions are0,The copy trading account is ready to execute a market full close operation
            for (var i = 1; i < exchanges.length; i++) {
                // Get the position information of the copy trading account
                var followPos = getPosAmount(_C(exchanges[i].GetPosition), refCt);
                // If there is a long position, perform a full market price operation
                if (followPos.long > 0) {
                    //exchanges[i].SetDirection("closesell");
                    exchanges[i].SetDirection("closebuy");
                    exchanges[i].Sell(-1, followPos.long, "Refer to exchange position as 0, copy-trading exchange closes all at market price");
                }
                // If there is a short position, perform a full market price operation
                if (followPos.short > 0) {
                    //exchanges[i].SetDirection("closebuy");
                    exchanges[i].SetDirection("closesell");
                    exchanges[i].Buy(-1, followPos.short, "Refer to exchange position as 0, copy-trading exchange closes all at market price");
                }
            }
        } else {
        	// Position change detected
        	for (var i = 1 ; i < exchanges.length ; i++) {
        		// Execute long action
        		if (longPosDelta != 0) {
        			var longDelta = Math.round(longPosDelta * followRatio);
        			Log(exchanges[i].GetName(), exchanges[i].GetLabel(), "Execute long position copy, change amount:", longDelta)
        		    trade(exchanges[i], refCt, PD_LONG, longDelta)
        		}
        		// Execute short action
        		if (shortPosDelta != 0) {
        			var shortDelta = Math.round(shortPosDelta * followRatio);
        			Log(exchanges[i].GetName(), exchanges[i].GetLabel(), "Execute short position copy, change amount:", shortDelta)
        		    trade(exchanges[i], refCt, PD_SHORT, shortDelta)
        		}                
        	}
        }

        // After executing copy action, update
        initRefPosAmount = nowRefPosAmount

    }
}

```

> Detail

https://www.fmz.com/strategy/423776

> Last Modified

2023-08-14 10:57:29
