
> Name

Trading-Terminal-Plugin-Example

> Author

发明者量化-小小梦

> Strategy Description

For demonstrating trading terminal plugin embedding function.
https://www.fmz.com/api#%E4%BA%A4%E6%98%93%E6%8F%92%E4%BB%B6

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|TransactionTimes|Number of trades | Number of trades|
|Amount|Number of coins per trade | number of coins per trade|
|Side|Trading direction | Trading direction|


> Source (javascript)

``` javascript
function main() {
    var initAcc = _C(exchange.GetAccount)
    var tbl = {
        "type" : "table", 
        "title" : "Table",
        "cols" : ["Project', 'Content"],
        "rows" : [],     
    }
    
    for (var i = 0 ; i < TransactionTimes ; i++) {
        var info = null
        if (Side == 0) {
            info = $.Buy(Amount)
        } else if (Side == 1) {
            info = $.Sell(Amount)
        } else {
            throw "side error!"
        }
        
        tbl.rows.push([i + "Order number, transaction status:", JSON.stringify(info)])    
        Sleep(300)
    }
    
    var nowAcc = _C(exchange.GetAccount)
    Log("balance:", nowAcc.Balance)
    delete initAcc.Info
    delete nowAcc.Info
    tbl.rows.push(["Initial account:", JSON.stringify(initAcc)])
    tbl.rows.push(["Post-execution account:", JSON.stringify(nowAcc)])    
    return tbl
}
```

> Detail

https://www.fmz.com/strategy/187708

> Last Modified

2025-04-08 16:12:39
