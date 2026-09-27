
> Name

Spot-Selling-Has-Always-Occupied-One-Plugin

> Author

小草

> Strategy Description

Always occupying the position of buying one or selling one is also a way to slowly ship goods, which has a relatively small impact on the market. There are still some improvements to this strategy. You can manually change the minimum transaction volume or accuracy.
Buy: https://www.fmz.com/strategy/191582 Sell:https://www.fmz.com/strategy/191730

The plug-in can be started with one click on the trading terminal, free of charge, and convenient for manual trading. Detailed introduction:https://www.fmz.com/digest-topic/5051

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|SellAmount|2|Sell Quantity|Sell amount|
|Intervel|true|Sleep time (seconds))|


> Source (javascript)

``` javascript
function GetPrecision(){
    var precision = {price:0, amount:0}
    var depth = exchange.GetDepth()
    for(var i=0;i<depth.Asks.length;i++){
        var amountPrecision = depth.Asks[i].Amount.toString().indexOf('.') > -1 ? depth.Asks[i].Amount.toString().split('.')[1].length : 0
        precision.amount = Math.max(precision.amount,amountPrecision)
        var pricePrecision = depth.Asks[i].Price.toString().indexOf('.') > -1 ? depth.Asks[i].Price.toString().split('.')[1].length : 0
        precision.price = Math.max(precision.price,pricePrecision)
    }
    return precision
}

function main(){
    var initAccount = exchange.GetAccount()
    if(!initAccount){return 'Unable to obtain account information'}
    var precision = GetPrecision()
    var sellPrice = 0
    var lastId = 0
    var done = false
    while(true){
        var account = _C(exchange.GetAccount)
        var dealAmount = - account.Stocks + initAccount.Stocks
        var ticker = _C(exchange.GetTicker)
        if(SellAmount - dealAmount > 1/Math.pow(10,precision.amount) && ticker.Sell < sellPrice){
            if(lastId){exchange.CancelOrder(lastId)}
            var id = exchange.Sell(ticker.Sell, _N(SellAmount - dealAmount,precision.amount))
            if(id){
                lastId = id
            }else{
                done = true
            }
        }
        if(BuyAmount - dealAmount <= 1/Math.pow(10,precision.amount)){done = true}
        if(done){
            var avgCost = (-initAccount.Balance + account.Balance)/dealAmount
            return 'order is done, avg cost is ' + avgCost  // including fee cost
        }
        Sleep(Intervel*1000)
    }
}
```

> Detail

https://www.fmz.com/strategy/191730

> Last Modified

2020-06-09 15:06:15
