
> Name

Simple-Martingale-Long-and-Short-Trading-Strategy

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
/*backtest
start: 2017-06-26 00:00:00
end: 2022-02-16 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT","currency":"eth_USDT""currency":"bch_USDT"}]
*/

var n =0.001 //Initial Order Quantity
var MarginLevel = 50 //Contract Leverage 
var profit = 0.05 //Expected return, cannot be less than the handling fee 
var bet=1//Multiplier


//Get random number 
function sum(m, n) {  
    var num = Math.floor(Math.random() * (m - n) + n);  
    return num;
}

function main() {
    var ret = exchange.IO("api", "POST", "/fapi/v1/positionSide/dual", "dualSidePosition=true")
    // ret : {"code":200,"msg":"success"}
    Log(ret)
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
                n=0.002
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
                    
                    let redom = Math.random()
                    n=0.002
                    if (redom < 0.5) {  
                     n=0.003
                    exchange.SetDirection("sell")
                    exchange.Sell(-1, n, "short")
                }
                    }
                //If the negative profit is greater than the margin, increase the position

                if (position[0].Profit < position[0].Margin * -1) {
                    n=n*bet
                    exchange.SetDirection("buy")
                    exchange.Buy(-1, position[0].Amount=n)
                   
                }
            }
            if (position[0].Type == 1) {
                if (position[0].Profit > profit) {
                    exchange.SetDirection("closesell")
                    exchange.Buy(-1, position[0].Amount)
                    let redom = Math.random()
                    n=0.004
                    if (redom > 0.5) {  
                    exchange.SetDirection("buy")
                    exchange.Buy(-1, n, "long")
                }
                }
                if (position[0].Profit < position[0].Margin * -1) {
                    n=n*bet
                    exchange.SetDirection("sell")
                    exchange.Sell(-1, position[0].Amount=n)
                }
            }
            Sleep(60000)
        }
    }

}
```

> Detail

https://www.fmz.com/strategy/353603

> Last Modified

2022-03-31 19:15:01
