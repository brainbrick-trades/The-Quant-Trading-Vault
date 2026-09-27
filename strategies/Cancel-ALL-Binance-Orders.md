
> Name

Cancel-ALL-Binance-Orders

> Author

小草

> Strategy Description

Binance cancels all outstanding orders for trading pairs and uses the IO interface. This can be used as an example of learning how to connect the IO interface to support the API interface.



> Source (javascript)

``` javascript
function cancellAll(){
    try{
        var openOrders = exchange.IO('api', 'GET', '/api/v3/openOrders');
        for (var i=0; i<openOrders.length; i++){
            var order = openOrders[i];
            var currency = '';
            if (order.symbol.endsWith('USDT')){
                currency = order.symbol.slice(0,order.symbol.length-4) + '_' + 'USDT';
            }
            else{
                currency = order.symbol.slice(0,order.symbol.length-3) + '_' + order.symbol.slice(order.symbol.length-3,order.symbol.length);
            }
            exchange.IO("currency", currency);
            exchange.CancelOrder(order.orderId);
        }
    }
    catch(err){
        Log('error');
    }
}
function main(){
    cancellAll()
}
```

> Detail

https://www.fmz.com/strategy/121549

> Last Modified

2019-07-03 16:36:05
