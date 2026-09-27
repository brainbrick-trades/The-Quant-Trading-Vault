
> Name

Simple-Martingale-Long-and-Short-Position-Increase-Ratio-Modification

> Author

Zer3192

> Strategy Description

!!!!!!!Friendly reminder: this strategy is for learning purposes only; actual trading will certainly result in liquidation!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Simple Martingale
The principle is to double after losing until the desired profit is achieved
As it is for backtesting, all orders are market orders, not run in live trading!!

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|LongAmount|150|Initial long order quantity|
|ShortAmount|100|Initial short order quantity|
|MarginLevel|50|Set leverage|
|profit|0.5|Expected profit for long position|
|profits|0.4|Expected profit for short position|
|longbet|1.1|Turn on multiple magnifications|
|shortbet|true|Opening ratio|
|SetContractType|swap|Perpetual Contract|
|short|true|go short|
|long|false|go long|
|StopProfit|5|Take profit percentage|
|StopLoss|6|Stop Loss Percentage|


> Source (javascript)

``` javascript
/*backtest
start: 2017-06-26 00:00:00
end: 2022-02-16 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/
var m =LongAmount //Initial Order Quantity
var n = ShortAmount //Initial Order Quantity
var MarginLevel1 =MarginLevel  //Contract Leverage
var SetContractType1=SetContractType // Contract Type
var longprofit = profit //Expected return, long positions must not be less than the fee
var shortprofits = profits//Expected return, short positions must not be less than the fee
var longbet1 =longbet //Turn on multiple magnifications
var shortbet2=shortbet //Opening ratio
StopProfit /=StopProfit ;
StopLoss /=StopLoss ;
//Get random number 
function sum(m, n) {  
    var num = Math.floor(Math.random() * (m - n) + n);  
    return num;
}

function main(){
    while(true){
LogProfit(exchange.GetAccount().Balance)
        Sleep(2000)
    }
}
function main() {
    exchange.SetContractType(SetContractType1)
    exchange.SetMarginLevel(MarginLevel1)
    var position = []
    while (true) { 
         position = exchange.GetPosition()
        if (position.length == 0) {
            //Get random number0,1As direction
            var redom = sum(2, 0)
            Log(redom)
            redom=0==short //go short
            if (redom == 0) {
                n=ShortAmount
                exchange.SetDirection("sell")
                exchange.Sell(-1, n, "open short")
            }
            redom=1==long //go long
            if (redom == 1) {
                m=LongAmount
                exchange.SetDirection("buy")
                exchange.Buy(-1, m, "open long")
            }
        }
        if (position.length > 0) {

            if (position[0].Type == 0) {
                //Long profit greater than expected 
                if (position[0].Profit >profit) {
                    exchange.SetDirection("closebuy")
                    exchange.Sell(-1, position[0].Amount)
                    let redom = Math.random()
                    if (redom < 0.5) { 
                     m=LongAmount
                    exchange.SetDirection("buy")
                    exchange.Buy(-1, m, "Close long and open long positions")    
                }
             }  
                //If long position negative profit exceeds the margin, then add position

                if (position[0].Profit <position[0].Margin * -1) {
                    longbet1=longbet
                    m=m*longbet
                    exchange.SetDirection("buy")
                    exchange.Buy(-1, position[0].Amount=m)
               }
            }
                  //Short profit greater than expected 
            if (position[0].Type == 1) {
                if (position[0].Profit > profits) {
                    exchange.SetDirection("closesell")
                    exchange.Buy(-1, position[0].Amount)
                    let redom = Math.random()
                   if (redom > 0.5) {  
                     n=ShortAmount
                    exchange.SetDirection("sell")
                    exchange.Sell(-1, n, "Open a short position to offset a short")  
              }
          }
                  //If short position negative profit exceeds the margin, then add position
                if (position[0].Profit <position[0].Margin * -1 ) {
                    shortbet2=shortbet
                    n=n*shortbet
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

https://www.fmz.com/strategy/356471

> Last Modified

2022-06-19 12:12:05
