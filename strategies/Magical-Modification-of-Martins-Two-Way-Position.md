
> Name

Magical-Modification-of-Martins-Two-Way-Position

> Author

Zer3192





> Source (javascript)

``` javascript
/*backtest
start: 2017-06-26 00:00:00
end: 2022-02-16 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"xxx_USDT"}]
*/


var symbols = ['ETH_Usdt', 'BCH_Usdt', 'XRP_Usdt', 'EOS', 'LTC', 'TRX', 'ETC', 'LINK', 'XLM', 'ADA', 'XMR', 'DASH', 'ZEC', 'XTZ', 'BNB', 'ATOM', 'ONT', 'IOTA', 'BAT', 'VET', 'NEO', 'QTUM', 'IOST']
var n =0.5 //Initial Order Quantity
var MarginLevel = 20//Contract Leverage 
var profit = 0.4 //Expected return, cannot be less than the handling fee 
var bet=1//Multiplier


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
            //Take a random number as direction
            var redom = sum(0, 2)
            Log(redom)
            if (redom == 0,1,2,3,4,5) {
                n=0.5
                exchange.SetDirection("sell")
                exchange.Sell(-1, n, "open short")
            }
            if (redom == 5,6,7,8,9,10) {
                n=0.5
                exchange.SetDirection("buy")
                exchange.Buy(-1, n, "open long")
            }

                if (redom == 0) {
                n=0.5
                exchange.SetDirection("sell")
                exchange.Sell(-1, n, "open short")
            }
               if (redom == 1) {
                n=0.5
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
                    if (redom < 0.5) { 
                     n=0.5
                    exchange.SetDirection("buy")
                    exchange.Buy(-1, n, "long")
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
                   if (redom > 0.5) {  
                     n=0.5
                    exchange.SetDirection("sell")
                    exchange.Sell(-1, n, "short")
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

https://www.fmz.com/strategy/353904

> Last Modified

2022-04-16 11:38:03
