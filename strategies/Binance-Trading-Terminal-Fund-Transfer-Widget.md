
> Name

Binance-Trading-Terminal-Fund-Transfer-Widget

> Author

高频量化



> Strategy Arguments





|Button|Default|Description|
|----|----|----|
|assets|USDT|Transfer Currency|
|amount|10|Transfer Quantity|
|typeIndex|0|Transfer type: Transfer from spot account to USDT contract account | Transfer from USDT contract account to spot account | Transfer from spot account to currency-standard contract account | Transfer from currency-standard contract account to spot account|


> Source (javascript)

``` javascript
var type = 1;
assets = "USDT" //Prevent missing parameters
amount = "10" //Prevent missing parameters
//var type = [1, 2, 3, 4][typeIndex]

function UsdtTransfer(e, cur, amount, type) {
    try {
        var base = ''
        var params = ''
        var Currency = cur
        var Transfer Quantity = amount
        var exname = e.GetName() //Obtain the marker of the exchange interface
        if (exname == 'Binance') {
            Log("exname=", exname)
            // 1: Spot account toUSDTContract account transfer 
            // 2: USDTTransfer from contract account to spot account
            // 3: Transfer from spot account to currency-based contract account 
            // 4: Transfer from currency-based contract account to spot account
            var Transfer type = type
            //Transfer to spot
            //POST /sapi/v1/futures/transfer
            base ="https://api.binance.com"
            e.SetBase(base)
            var timestamp = new Date().getTime()
            params = "asset=" + Currency + "&amount=" + Transfer Quantity + "&type=" + Transfer type + "&timestamp" + timestamp
            Log("trading pair:", Currency, "Transfer Quantity:", Transfer Quantity, "Transfer type:", Transfer type)
            var ret1 = e.IO("api", "POST", "/sapi/v1/futures/transfer", params)
            Log(ret1)
            return ret1
        } else if (exname == 'Futures_Binance') {
            Log("exname=", exname)
            // 1: Spot account toUSDTContract account transfer 
            // 2: USDTTransfer from contract account to spot account
            // 3: Transfer from spot account to currency-based contract account 
            // 4: Transfer from currency-based contract account to spot account
            var xTransfer type = type
            //Transfer to spot
            //POST /sapi/v1/futures/transfer
            base ="https://api.binance.com"
            e.SetBase(base) //Set in the spot interface
            var xtimestamp = new Date().getTime()
            params = "asset=" + Currency + "&amount=" + Transfer Quantity + "&type=" + xTransfer type + "&xtimestamp" + xtimestamp
            Log("trading pair:", Currency, "Transfer Quantity:", Transfer Quantity, "xTransfer type:", xTransfer type)
            //var ret1 = e.IO("api", "POST", "/sapi/v1/futures/transfer" ,"",  JSON.stringify( params ) )
            var ret2 = e.IO("api", "POST", "/sapi/v1/futures/transfer", params) //Send transfer
            Log(ret2)
            //Need to switch back to the originalAPIInterface, otherwise it may affect subsequent account trading
            base = "https://fapi.binance.com" //Futures interface  
            e.SetBase(base)
            return ret2
        }
        //Log("Loop once")
    } catch (error) {
        Log(error)
    }
}

function GetCom() {
    var cmd = GetCommand()
    if (cmd) {
        var arr = cmd.split(":")
        Log(arr)
        if (arr[0] == "assets") {
            assets = arr[1]
            Log("Switch toassets:", assets)
        }
        if (arr[0] == "amount") {
            amount = arr[1]
            Log("Switch toamount:", amount)
        }
        if (arr[0] == "typeIndex") {
            type = Number(arr[1]) + 1
            Log("Switch totype:", type)
            var feedback = UsdtTransfer(exchange, assets, amount, type)
            if(feedback){
                Log("Fund transfer successful")
                //Sleep(1000 * 3); // Sleep for 3 seconds
            }
        }
    }
}


function main() {
    while (true) {
        GetCom()
        Sleep(1000 * 1); // Sleep for 3 seconds
    }
}
```

> Detail

https://www.fmz.com/strategy/336595

> Last Modified

2021-12-24 15:56:36
