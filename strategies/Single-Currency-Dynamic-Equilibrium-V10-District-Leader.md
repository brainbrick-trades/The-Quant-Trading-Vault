
> Name

Single-Currency-Dynamic-Equilibrium-V10-District-Leader

> Author

区班量化

> Strategy Description

"Talk is cheap. Show me the code"

For teaching purposes, use with caution in real trading.


Note: ` Strategy uses a trading template library`

`I hope that novices can get started with this strategy, learn to write strategies step by step, and experience the impact of simulation and real environments on the trading system.`

https://dn-filebox.qbox.me/fb4d0c7d773ca83e9d0230927705d419dc0bbeaa.png

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Interval|60|Polling interval (seconds))|
|changeRatio|0.1|Switch warning ratio|


> Source (javascript)

``` javascript
/*backtest
start: 2019-01-01 00:00:00
end: 2019-10-10 00:00:00
period: 1d
exchanges: [{"eid":"OKEX","currency":"BTC_USDT","stocks":0}]
*/
//Very simple single currency dynamic equilibrium strategy, below50%Buy with a certain proportion, sell when higher
//After registering on Bihuhttps://m.bihu.com/signup?i=1ewtKO&s=4&c=4
//Search IoT blockchain to contact the author or group leader
function main() {
    var STATE_IDLE  = -1;
    var state = STATE_IDLE; //Indicates Empty Position
    var entryPrice = 0;
    var initAccount = _C(exchange.GetAccount);
    var obj;
    var allAmount;
    var cashRatio;
    Log(initAccount);
    while (true) {
        var account = _C(exchange.GetAccount);
        var ticker = _C(exchange.GetTicker);
        if (state === STATE_IDLE) {  //The initial state is the default position; default is empty position, only buy
            obj = $.Buy(_N(account.Balance * 0.5 / ticker.Sell, 3));
            if (obj) { //If the purchase is successful, mark the opening position
                opAmount = obj.amount;
                entryPrice = obj.price;
                state = PD_LONG;
                account = _C(exchange.GetAccount);
                Log("Open a buying position",obj.amount,"Price",obj.price,"Current Holdings", account.Stocks);
            }
        } else { //stateis non-idle; Handles dynamic balance detection
            allAmount=account.Balance+account.Stocks*ticker.Sell; //Calculate total amount
            cashRatio=parseFloat((account.Balance/allAmount).toFixed(3));
            //Log("Cash",account.Balance,"Total assets",allAmount,"Proportion",cashRatio);
            if (cashRatio>0.5+changeRatio) { //I have too much cash and need to buy currency.
                obj = $.Buy(_N(allAmount*(cashRatio-0.5)/ticker.Sell/2.0, 3)); //Sell half of the excess, for balance
                if(obj){
                    Log("Open a buying position",obj.amount,"Price",obj.price);
                    Log("Current Funds",allAmount, "Profit",allAmount - initAccount.Balance);
                }
            }else if(cashRatio<0.5-changeRatio){  //Cash is low, need to toss coins
                obj = $.Sell(_N(allAmount*(0.5-cashRatio)/ticker.Sell/2.0, 3)); //Buy the extra part
                if(obj){
                    Log("Close Position Sell",obj.amount,"Price",obj.price);
                    Log("Current Funds",allAmount, "Profit",allAmount - initAccount.Balance);
                }
            }
        }
        Sleep(Interval*1000);
    }
}
```

> Detail

https://www.fmz.com/strategy/169701

> Last Modified

2019-10-12 16:48:48
