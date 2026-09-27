
> Name

Fibonacci-Sequence-Strategy

> Author

Zer3192

> Strategy Description

!!!!!!!Friendly reminder: this strategy is for learning purposes only; actual trading will certainly result in liquidation!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Simple Martingale
The principle is to double after losing until the desired profit is achieved
As it is for backtesting, all orders are market orders, not run in live trading!!



> Source (javascript)

``` javascript
/*
This strategy is for learning purposes only; real trading consequences are at your own risk 
*/
/*backtest
start: 2017-06-26 00:00:00
end: 2022-02-16 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

var n = 1 //Initial Order Quantity
var MarginLevel = 50 //Contract Leverage 
var profit = 1//Expected return, cannot be less than the handling fee 
var bet=1.1


//Get random number 
function sum(m, n) {  
    var num = Math.floor(Math.random() * (m - n) + n);  
    return num;
}

function main() {
    exchange.SetContractType("swap")
    exchange.SetMarginLevel(MarginLevel)
    var position = []
    while (true) {
        position = exchange.GetPosition()
        if (position.length == 0) {
            //Get random number0,1As direction
            var redom = sum(2, 0)
            Log(redom)
            if (redom == 0) {
                n=0.001
                exchange.SetDirection("sell")
                exchange.Sell(-1, n, "open short")
            }
            if (redom == 1) {
                n=0.001
                exchange.SetDirection("buy")
                exchange.Buy(-1, n, "open long")
            }

        }
        if (position.length > 0) {

            if (position[0].Type == 0) {
                //Profit greater than expected 
                if (position[0].Profit > profit) {
                    exchange.SetDirection("closebuy")
                    exchange.Sell(-1, position[0].Amount)
                }
                //If the negative profit is greater than the margin, increase the position

                if (position[0].Profit < position[0].Margin * -1) {
              function  fibonacci( n){

        if (n == 1 || n == 2) {             //Special case, discuss separately
            return 1;
        }
        if (n > 2) {
            return fibonacci(n - 1) + fibonacci(n - 2);     //Recursive call
        }
        return -1;              //If the input is wrongn,Always return-1
    }
                    
                    exchange.SetDirection("buy")
                    exchange.Buy(-1, n)
                }
            }
            if (position[0].Type == 1) {
                if (position[0].Profit > profit) {
                    exchange.SetDirection("closesell")
                    exchange.Buy(-1, position[0].Amount)
                }
                if (position[0].Profit < position[0].Margin * -1) {
                    
                    function    fibonacci( n){

        if (n == 1 || n == 2) {             //Special case, discuss separately
            return 1;
        }
        if (n > 2) {
            return fibonacci(n - 1) + fibonacci(n - 2);     //Recursive call
        }
        return -1;              //If the input is wrongn,Always return-1
    }
                    
                    exchange.SetDirection("sell")
                    exchange.Sell(-1, n)
                    
                }
            }
            Sleep(60000)
        }
    }

}
        
```

> Detail

https://www.fmz.com/strategy/353314

> Last Modified

2022-05-14 06:32:26
