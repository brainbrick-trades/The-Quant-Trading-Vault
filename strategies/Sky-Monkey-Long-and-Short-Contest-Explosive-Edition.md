
> Name

Sky-Monkey-Long-and-Short-Contest-Explosive-Edition

> Author

Zero

> Strategy Description

- Use long and short forces as the opening position condition
- Fixed take profit and stop loss points
- The name is randomly generated, for learning purposes, use cautiously in real trading

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|DepthLevel|5|Market depth statistics|
|EnterPeriod|2|Observation period|
|CalcInterval|10|Observation polling interval (seconds)|
|DiffRatio|2.1|Currency multiple|
|PositionRatio|0.8|Position ratio|
|StopProfit|0.02|Take profit (percentage)|
|StopLoss|0.01|Stop loss (percentage))|
|Interval|true|Price polling interval (seconds)|


> Source (javascript)

``` javascript
function calcDepth(orders) {
    var base = parseInt(orders[0].Price);
    var allAmount = 0;
    var n = 0;
    for (var i = 0; i < orders.length && n < DepthLevel; i++) {
        var p = parseInt(orders[i].Price);
        if (p != base) {
            n++;
            base = p;
        }
        allAmount += orders[i].Amount;
    }
    return allAmount;
}

function main() {
    var STATE_IDLE  = -1;
    var state = STATE_IDLE;
    var initAccount = $.GetAccount();
    Log(initAccount);
    var pos = null;
    while (true) {
        Sleep(Interval*1000);
        if (state === STATE_IDLE) {
            var n = 0;
            while (Math.abs(n) < EnterPeriod) {
                var depth = exchange.GetDepth();
                if (!depth || depth.Asks.length < DepthLevel || depth.Bids.length < DepthLevel) {
                    Sleep(Interval * 1000);
                    continue;
                }

                var asksAmount = calcDepth(depth.Asks);
                var bidsAmount = calcDepth(depth.Bids);
                var ratio = Math.max(asksAmount/bidsAmount, bidsAmount/asksAmount);
                if (ratio > DiffRatio) {
                    if (asksAmount > bidsAmount) {
                        n = n < 0 ? 0 : n+1;
                    } else {
                        n = n > 0 ? 0 : n-1;
                    }
                } else {
                    n = 0;
                }
                LogStatus("Buy Volume:", _N(asksAmount), "Sell Volume:", _N(bidsAmount), "Proportion: ", _N(ratio * 100, 4) + '%', "Duration period:", n);
                Sleep(CalcInterval * 1000);
            }
            var opAmount = parseFloat((initAccount.Stocks * PositionRatio).toFixed(3));
            pos = n > 0 ? $.Buy(opAmount) : $.Sell(opAmount);
            if (pos) {
                opAmount = pos.amount;
                pos.stopLossPrice = n > 0 ? (pos.price * (1-StopLoss)) : (pos.price * (1 + StopLoss));
                pos.stopProfitPrice = n > 0 ? (pos.price * (1+StopProfit)) : (pos.price * (1 - StopProfit));
                state = n > 0 ? PD_LONG : PD_SHORT;
                Log("Open position details", pos);
            }
        } else {
            var ticker = exchange.GetTicker();
            if (!ticker) {
                continue;
            }
            var dynamicProfit = (state === PD_LONG ? (ticker.Last - pos.price) : (pos.price - pos.price)) * pos.amount;
            LogStatus("Position type", (state === PD_LONG ? "Long position" : "Short position"), "Average position price:", pos.price, "Quantity:", pos.amount, "Floating profit and loss:", _N(dynamicProfit), "Stop loss price:", pos.stopLossPrice, "Take-profit price:", pos.stopProfitPrice);
            if ((state === PD_LONG && ((ticker.Last > pos.stopProfitPrice) || (ticker.Last < pos.stopLossPrice))) ||
                (state === PD_SHORT && ((ticker.Last < pos.stopProfitPrice) || (ticker.Last > pos.stopLossPrice))) ){
                Log("stop loss, Average position price:", pos.price, "Quantity:", pos.amount, "Floating profit and loss:", _N(dynamicProfit), "Last transaction price:", ticker.Last);
                var nowAccount = $.GetAccount();
                var obj = state === PD_LONG ? $.Sell(nowAccount.Stocks - initAccount.Stocks) : $.Buy(initAccount.Stocks - nowAccount.Stocks);
                state = STATE_IDLE;
                nowAccount = $.GetAccount();
                LogProfit(nowAccount.Balance - initAccount.Balance, 'Money:', nowAccount.Balance, 'Coins:', nowAccount.Stocks, 'Close details:', obj, "Cross cycle", n);
            }
        }
    }
}
```

> Detail

https://www.fmz.com/strategy/13597

> Last Modified

2016-04-18 16:39:43
