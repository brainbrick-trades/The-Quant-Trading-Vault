
> Name

Simple-Digital-Currency-Spot-Copy-Robot-Strategy

> Author

发明者量化-小小梦

> Strategy Description

## Simple digital currency spot copy robot strategy

Reference article:https://www.fmz.com/bbs-topic/6528

- test The function is for backtesting; it randomly triggers order placement on a reference exchange for copy-trading test.
- Add exchange objects, the first exchange object is the reference exchange, others are copy-trading exchanges.

The strategy only provides ideas for copy trading strategy design; if there are any issues, please leave a comment.



> Source (javascript)

``` javascript
function test() { 
    // Test Function
    var ts = new Date().getTime()    
    if (ts % (1000 * 60 * 60 * 6) > 1000 * 60 * 60 * 5.5) {
        Sleep(1000 * 60 * 10)
        var x = Math.random()
        if (x > 0.5) {
            $.Buy(exchange, x / 10)    
        } else {
            $.Sell(exchange, x / 10)    
        }        
    }
}

function main() {
    LogReset(1)
    if (exchanges.length < 2) {
        throw "Exchange without copy trading"
    }
    var exName = exchange.GetName()
    // Detect reference exchange
    if (exName.includes("Futures_")) {
        throw "Only supports spot copy trading"
    }
    Log("Start monitoring", exName, "exchange", "#FF0000")
    
    // Detect copy trading exchange
    for (var i = 1 ; i < exchanges.length ; i++) {
        if (exchanges[i].GetName().includes("Futures_")) {
            throw "Copy trading on futures exchanges is not supported"
        }
    }
    
    var initAcc = _C(exchange.GetAccount)
    while(1) {
        if(IsVirtual()) {
           // Test Function
           test()  
        }  
        Sleep(5000)
        
        // Update the reference account's current account information
        var nowAcc = _C(exchange.GetAccount)
        
        // Reference exchange account information
        var refTbl = {
            type : "table", 
            title : "Reference exchange",
            cols : ["Name", "Coin", "Frozen Coin", "Money", "Frozen Money""],
            rows : []
        }
        refTbl.rows.push([exName, nowAcc.Stocks, nowAcc.FrozenStocks, nowAcc.Balance, nowAcc.FrozenBalance])
        
        // Copy trading exchange account information
        var followTbl = {
            type : "table", 
            title : "Copy trading exchange",
            cols : ["Name", "Coin", "Frozen Coin", "Money", "Frozen Money""],
            rows : []        
        }
        for (var i = 1 ; i < exchanges.length ; i++) {
            var acc = _C(exchanges[i].GetAccount)
            var name = exchanges[i].GetName()
            followTbl.rows.push([name, acc.Stocks, acc.FrozenStocks, acc.Balance, acc.FrozenBalance])
        }
        
        // Display in status bar
        LogStatus(_D(), "\n`" + JSON.stringify(refTbl) + "`", "\n`" + JSON.stringify(followTbl) + "`")
        
        // Detect and follow orders
        var amount = (nowAcc.Stocks + nowAcc.FrozenStocks) - (initAcc.Stocks + initAcc.FrozenStocks)
        var func = null 
        if (amount > 0) {
            func = $.Buy
        } else if (amount < 0) {
            func = $.Sell
        } else {
            continue
        }
        
        // Execute order
        Log("Copy trading! Quantity:", Math.abs(amount), "#FF0000")
        for (var i = 1 ; i < exchanges.length ; i++) {            
            func(exchanges[i], Math.abs(amount))
        }
        
        // After executing follow-trading, update the reference exchange account information record
        initAcc = nowAcc
    }
}
```

> Detail

https://www.fmz.com/strategy/255182

> Last Modified

2021-04-08 16:38:12
