
> Name

Classic-Moving-Average-Strategy-V10-Simplified-Notes-by-Area-Leader

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
|FastPeriod|5|Market Entry Express Cycle|
|SlowPeriod|15|Slow market entry cycle|
|EnterPeriod|2|Market Entry Observation Period|
|ExitFastPeriod|7|Exit express cycle|
|ExitSlowPeriod|15|Exit slow cycle|
|ExitPeriod|true|Market Exit Observation Period|
|PositionRatio|0.8|Position ratio|
|StopLossRatio|0.05|Stop loss ratio|
|Interval|10|Polling interval (seconds))|


> Source (javascript)

``` javascript
/*backtest
start: 2019-01-01 00:00:00
end: 2019-10-10 00:00:00
period: 1d
exchanges: [{"eid":"OKEX","currency":"ETH_USDT","stocks":0}]
args: [["OpMode",1,10989],["MaxAmount",1,10989],["TradeFee",0.001,10989]]
*/
//After registering on Bihuhttps://m.bihu.com/signup?i=1ewtKO&s=4&c=4
//Search IoT blockchain to contact the author or group leader
function main() {
    var STATE_IDLE  = -1;
    var state = STATE_IDLE; //indicates status
    var entryPrice = 0;
    var initAccount = _C(exchange.GetAccount);
    Log(initAccount);
    while (true) {
        if (state === STATE_IDLE) {  //The initial state is the default position; default is empty position, only buy
            var n = $.Cross(FastPeriod, SlowPeriod);//Template function returnEMAFast line and slow line crossover results
            if (Math.abs(n) >= EnterPeriod) { //EnterPeriodMarket entry observation zone, wait for a certain pull-up before entering
                var account = _C(exchange.GetAccount);
                var ticker = _C(exchange.GetTicker);
                var obj;
                //Account cash multiplied by the ratio, divided by the current price, before decimals3bit
                if(n > 0){
                   obj = $.Buy(_N(account.Balance * PositionRatio / ticker.Sell, 3));
                   if (obj) { //If the purchase is successful, mark the opening position
                      opAmount = obj.amount;
                      entryPrice = obj.price;
                      state = PD_LONG;
                      account = _C(exchange.GetAccount);
                      Log("Open Position:Purchase quantity", opAmount);
                      Log("Current Holdings", account.Stocks, "Cross period", n);
                   }
                }
            }
        } else { //stateSet to non-idle state; handle close position detection
            var n = $.Cross(ExitFastPeriod, ExitSlowPeriod);
            //This condition is a bit long, let's look firstMath.abs(n) >= ExitPeriod,nAbsolute value greater than or equal to observation period; this is the trigger condition1,And
            //(n > 0)At least one of the two is true
            //Need to exit market and close position
            var needCover = Math.abs(n) >= ExitPeriod && (n<0);
            if (needCover) { //Close the position after exiting the market
                var nowAccount = _C(exchange.GetAccount);
                var obj = $.Sell(_N(nowAccount.Stocks, 3));
                if(obj){
                    state=STATE_IDLE;
                    Log("Close position: sell quantity",nowAccount.Stocks);
                    nowAccount = _C(exchange.GetAccount);
                    Log("Current Funds",nowAccount.Balance, "Cross period", n,"Profit",nowAccount.Balance - initAccount.Balance);
                }
                //Print earnings
                //LogProfit(nowAccount.Balance - initAccount.Balance, 'Money:', nowAccount.Balance, 'Currency:', nowAccount.Stocks, 'Close position details:', obj, "Cross period", n);
            }
        }
        Sleep(Interval*1000);
    }
}
```

> Detail

https://www.fmz.com/strategy/169569

> Last Modified

2019-10-18 17:57:59
