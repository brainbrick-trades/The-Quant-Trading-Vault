
> Name

The-First-Place-Order-Robot-for-New-Coins-on-the-Exchange

> Author

小草

> Strategy Description

will place orders at fixed intervals and serve as the first place order bot for new coins listed on exchanges. Due to the simple logic, it has not been tested

## Principle:

Start running after adding a trading pair, and continue to try to obtain the market price. If the market price can be obtained, it means that trading has started, and the strategy will place an order. If it cannot be obtained, it means that it is not open. Continue to try again and wait.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Type|0|Order type: Buy order | Sell order|
|Start_Price|7000|Starting price|
|Spread|5|Interval|
|N|5|Number of orders placed|
|Amount|0.1|Amount of pending orders per order|
|Amount_Step|false|Pending order increment|


> Source (javascript)

``` javascript

function main() {
    exchange.SetTimeout(500) //Guaranteed faster returnnull,Continue retrying to get market quotes
    while(true){
        var ticker = exchange.GetTicker()
        if(!ticker){
            continue
        }else{
            Log('Get the market price,Start ordering')
            for(var i=0;i<N;i++){
               if(Type == 0){
                    exchange.Buy(Start_Price-i*Spread,Amount+i*Amount_Step)
               }else{
                    exchange.Sell(Start_Price+i*Spread,Amount+i*Amount_Step)
               }
            }
            Log('Complete order placement,Exit program')
            return
        }
    }
}

```

> Detail

https://www.fmz.com/strategy/194206

> Last Modified

2020-10-16 10:20:29
