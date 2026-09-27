
> Name

30-Lines-of-Strategies-for-Gamblers

> Author

发明者量化-小小梦



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|_StopWin|500|take profit|
|_StopLoss|500|stop loss|
|_FirstAmount|0.01|Single order quantity|
|_MaxGear|8|Double the number of bets|


> Source (javascript)

``` javascript
var hold = {price : 0, amount : 0}
var _Gear = 0
function main(){
    var initAccount = _C(exchange.GetAccount)
    Log(initAccount, "#FF0000")
    while(1){
        var ticker = _C(exchange.GetTicker)
        if(hold.amount == 0){
            var firstInfo = $.Buy(_FirstAmount)
            hold.amount = firstInfo.amount
            hold.price = firstInfo.price
        } else {
            if(ticker.Sell > hold.price + _StopWin){
                var coverStopWinInfo = $.Sell(hold.amount)
                hold.price = 0
                hold.amount = 0
                _Gear = 0
            } else if(ticker.Sell < hold.price - _StopLoss && _Gear < _MaxGear){
                $.Sell(hold.amount)
                var amount = hold.amount * 2
                var addInfo = $.Buy(amount)
                hold.price = addInfo.price
                hold.amount = addInfo.amount
                _Gear++
            }
        }
        LogStatus(_D(), "Number of doubling bets: ", _Gear, "\n", "Current position:", hold)
        Sleep(500)
    }
}
```

> Detail

https://www.fmz.com/strategy/113796

> Last Modified

2018-08-31 10:43:45
