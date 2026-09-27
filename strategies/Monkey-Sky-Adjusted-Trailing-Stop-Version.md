
> Name

Monkey-Sky-Adjusted-Trailing-Stop-Version

> Author

Zero

> Strategy Description

Popularize the concept of trailing stop, for strategy learning use, cautious in actual trading !

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|FastPeriod|5|Market Entry Express Cycle|
|SlowPeriod|15|Slow market entry cycle|
|EnterPeriod|2|Market Entry Observation Period|
|PositionRatio|0.8|Position ratio|
|TrailingStopLoss|0.02|Trailing stop (percentage)|
|StopLoss|0.01|Stop loss (percentage))|
|Interval|10|Polling interval (seconds))|


> Source (javascript)

``` javascript
function main() {
    var STATE_IDLE  = -1;
    var state = STATE_IDLE;
    var initAccount = $.GetAccount();
    Log(initAccount);
    var pos = null;
    var table = {
        type : 'table',
        title : 'Account Information',
        cols : ['Stage', 'Money', 'Currency'],
        rows : [['initial', initAccount.Balance, initAccount.Stocks], ['current', 0, 0]],
    };
    while (true) {
        var status = '';
        var nowAccount = null;
        if (state === STATE_IDLE) {
            var n = $.Cross(FastPeriod, SlowPeriod);
            if (Math.abs(n) >= EnterPeriod) {
                var opAmount = parseFloat((initAccount.Stocks * PositionRatio).toFixed(3));
                pos = n > 0 ? $.Buy(opAmount) : $.Sell(opAmount);
                if (pos) {
                    opAmount = pos.amount;
                    pos.stopLossPrice = n > 0 ? (pos.price * (1-StopLoss)) : (pos.price * (1 + StopLoss));
                    pos.holdProfitPrice = n > 0 ? (pos.price * (1+TrailingStopLoss)) : (pos.price * (1 - TrailingStopLoss));
                    state = n > 0 ? PD_LONG : PD_SHORT;
                    Log("Open position details", pos, "Cross period", n);
                }
            }
        } else {
            var ticker = exchange.GetTicker();
            if (!ticker) {
                Sleep(Interval*1000);
                continue;
            }
            var dynamicProfit = 0;
            var shouldCover = false;
            var enableTS = false;
            if (state === PD_LONG) {
                dynamicProfit = (ticker.Last - pos.price) * pos.amount;
                if (ticker.Last > pos.holdProfitPrice) {
                    pos.stopLossPrice = pos.holdProfitPrice * (1-StopLoss);
                    pos.holdProfitPrice += (pos.price * TrailingStopLoss);
                    enableTS = true;
                }
                shouldCover = ticker.Last < pos.stopLossPrice;
            } else {
                dynamicProfit = (pos.price - ticker.Last) * pos.amount;
                if (ticker.Last < pos.holdProfitPrice) {
                    pos.stopLossPrice = pos.holdProfitPrice * (1+StopLoss);
                    pos.holdProfitPrice -= (pos.price * TrailingStopLoss);
                    enableTS = true;
                }
                shouldCover = ticker.Last > pos.stopLossPrice;
            }
            if (enableTS) {
                Log("Trigger trailing stop, Lock profit percentage:", _N(Math.abs((pos.price-ticker.Last)/pos.price)) + '%', "Current Price:", ticker.Last, "Position Profit and Loss:", dynamicProfit);
            }
            status = ["Position type", (state === PD_LONG ? "Long position" : "Short position"), "Average position price:", pos.price, "Quantity:", pos.amount, "Floating profit and loss:", _N(dynamicProfit), "Stop loss price:", pos.stopLossPrice].join(' ');
            if (status.length > 0) {
                status += '\n';
            }
            if (shouldCover) {
                Log("stop loss, Average position price:", pos.price, "Quantity:", pos.amount, "Floating profit and loss:", _N(dynamicProfit), "Last transaction price:", ticker.Last);
                nowAccount = $.GetAccount();
                var obj = state === PD_LONG ? $.Sell(nowAccount.Stocks - initAccount.Stocks) : $.Buy(initAccount.Stocks - nowAccount.Stocks);
                state = STATE_IDLE;
                nowAccount = $.GetAccount();
                LogProfit(nowAccount.Balance - initAccount.Balance, 'Money:', nowAccount.Balance, 'Coins:', nowAccount.Stocks, 'Close details:', obj, "Cross cycle", n);
            }
        }
        if (!nowAccount) {
            nowAccount = $.GetAccount();
        }
        if (nowAccount.Balance !== table.rows[1][1] || nowAccount.Stocks !== table.rows[1][2]) {
            table.rows[1] = ['Current #ff0000', nowAccount.Balance, nowAccount.Stocks];
        }
        status += '`'+JSON.stringify(table)+'`';
        LogStatus(status);
            
        Sleep(Interval*1000);
    }
}
```

> Detail

https://www.fmz.com/strategy/13594

> Last Modified

2016-04-19 00:56:36
