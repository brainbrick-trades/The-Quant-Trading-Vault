
> Name

Simple-Iceberg-order-to-sell

> Author

小草

> Strategy Description

Very simple, just for learn.
Code is best annotation.

Iceberg order selling, which divides orders into small sells to avoid market shocks, is a great strategy for beginners in Bitcoin quantitative trading

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|SELLAMOUNT|2|amount to sell|
|SELLSIZE|0.1|sell orders size|
|INTERVAL|3|order exist time(second)|


> Source (javascript)

``` javascript
function main(){
    var initAccount = _C(exchange.GetAccount)
    if (initAccount.Stocks < SELLAMOUNT){
        throw 'check your account amount to sell'
    }
    while(true){
        var account = _C(exchange.GetAccount)
        var dealAmount =  initAccount.Stocks - account.Stocks
        var ticker = _C(exchange.GetTicker)
        if(SELLAMOUNT - dealAmount > SELLSIZE){
            var id = exchange.Sell(ticker.Buy, SELLSIZE)
            Sleep(INTERVAL*1000)
            if(id){
                exchange.CancelOrder(id) // May cause error log when the order is completed, which is all right.
            }else{
                throw 'sell error'
            }
        }else{
            account = _C(exchange.GetAccount)
            var avgCost = (account.Balance - initAccount.Balance)/(initAccount.Stocks - account.Stocks)
            Log('Iceberg order to sell is done, avg price is ', avgCost) // including fee cost
            return
        }
    }
}
```

> Detail

https://www.fmz.com/strategy/121524

> Last Modified

2019-07-03 16:39:19
