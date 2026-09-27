
> Name

Simple-Iceberg-order-to-buy-Copy

> Author

小草

> Strategy Description

Very simple, just for learn.
Code is best annotation.

Iceberg entrusted buying, which divides the order into small M purchases to avoid impacting the market, is a good learning strategy for simple entry into Bitcoin quantitative trading.
The plug-in can be started with one click on the trading terminal, free of charge, and convenient for manual trading. Detailed introduction:https://www.fmz.com/digest-topic/5051

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|BUYAMOUNT|2|amount to buy|
|BUYSIZE|0.1|iceberg order size|
|INTERVAL|3|orders exist time(second)|


> Source (javascript)

``` javascript
function main(){
    var initAccount = _C(exchange.GetAccount)
    while(true){
        var account = _C(exchange.GetAccount)
        var dealAmount = account.Stocks - initAccount.Stocks
        var ticker = _C(exchange.GetTicker)
        if(BUYAMOUNT - dealAmount >= BUYSIZE){
            var id = exchange.Buy(ticker.Sell, BUYSIZE)
            Sleep(INTERVAL*1000)
            if(id){
                exchange.CancelOrder(id) // May cause error log when the order is completed, which is all right.
            }else{
                throw 'buy error'
            }
        }else{
            account = _C(exchange.GetAccount)
            var avgCost = (initAccount.Balance - account.Balance)/(account.Stocks - initAccount.Stocks)
            return 'Iceberg order to buy is done, avg cost is '+avgCost
        }
        
    }
}
```

> Detail

https://www.fmz.com/strategy/191771

> Last Modified

2020-03-24 10:50:51
