
> Name

Dynamic-Balance-Alpha

> Author

中本大料



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|threshold|0.05|threshold|
|LoopInterval|60|Loop Time|
|Minstock|0.001|Minimum transaction volume|
|XPrecision|4|quantity precision|
|YPrecision|8|Price precision|


> Source (javascript)

``` javascript
var threshold = 0.05
var LoopInterval = 60
var Minstock = 0.001
var XPrecision = 4
var ZPrecision = 8

//Cancel Order Function
function CancelPendingOrders() {
    Sleep(1000);
    var ret = false;
    while (true) {
        var orders = null;
        while (!(orders = exchange.GetOrders())) {
            Sleep(1000);
        }
        if(orders.length == 0){
            return ret;
        }
        for (var j = 0; j< orders.length; j++){
            exchange.CancelOrder(orders[j].Id);
            ret = true;
            if(j<(orders.length-1)){
                Sleep(1000);
            }
        }
    }
}

//Order Function
function onTick() {
    var acc = _C(exchange.GetAccount); //Get account information
    var ticker = _C(exchange.GetTicker); //ObtainTickerData
    var spread = ticker.Sell - ticker.Buy; //ObtainTickerData bid-ask spread
    var diffAsset = (acc.Balance - (acc.Stocks * ticker.Sell)) / 2;//The difference between the account balance and the current value of the position0.5times
    var ratio = diffAsset / acc.Balance;
    LogStatus('ratio:'.ratio, _D()); //Print ratio and current time
    if (Math.abs(ratio) < threshold) { //IfratioAbsolute value is less than the specified threshold
        print("spread")
        return false; //Returnfalse
    }
    if (ratio > 0) { //IfratioGreater than0;
        var buyPrice = _N(ticker.Sell + spread, ZPrecision);
        var buyAmount = _N(diffAsset / buyPrice, XPrecision);
        if (buyAmount < Minstock) { //If the order quantity is less than the minimum trading volume
            return false;
        }
        exchange.Buy(buyPrice, buyAmount, diffAsset, ratio);//Buy Order
    }else{
        var sellPrice = _N(ticker.Buy - spread, ZPrecision);//Calculate order price
        var sellAmount = _N(-diffAsset / sellPrice, XPrecision);//Calculate order quantity
        if(sellAmount < Minstock){
            return false;
        }
        exchange.Sell(sellPrice, sellAmount, diffAsset, ratio); //Sell Order
    }
    return true;
}

//Main Function
function main() {
    //SetErrorFilter("GetRecords:|GetOrders:|GetDepth:|GetAccount|:Buy|Sell|timeout"); //Filter non-essential information
    while (true) {
        if (onTick()) {
            CancelPendingOrders();
            Log(_C(exchange.GetAccount));
        }
        Sleep(LoopInterval * 1000);
    }
}
```

> Detail

https://www.fmz.com/strategy/115321

> Last Modified

2018-09-06 09:50:43
