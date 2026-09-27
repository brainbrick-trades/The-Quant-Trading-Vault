
> Name

Trend-Following-Shock-Strategy

> Author

Zero

> Strategy Description

Trend-following oscillation strategy, tracking take-profit (take profit if a specified loss occurs after profit).)

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Interval|2000|Error retry interval (milliseconds)|
|SlidePrice|0.3|Sliding price (yuan)|
|StopLoss|0.8|Stop-loss point|
|RatioUp|0.8|Reference points for selling on a rise (shorting))|
|RatioDown|0.8|Reference points for buying on a fall (going long))|
|UpWeightingVal|50|Open long positions on price rises (relative to the highest dip))|
|DownWeightingVal|50|Open short positions on price falls (relative to the highest rise))|
|StopProfitThreshold|0.9|Take profit coefficient(0-1)|
|EMA_Slow|30|EMASlow line cycle|
|EMA_Fast|7|EMAFast line cycle|
|EnableGoingShort|true|Short selling is allowed|
|MinStock|0.001|Minimum transaction volume|
|LoopInterval|60|Polling interval (seconds)|


> Source (javascript)

``` javascript

function CancelPendingOrders() {
    while (true) {
        var orders = null;
        while (!(orders = exchange.GetOrders())) {
            Sleep(Interval);
        }

        if (orders.length == 0) {
            return;
        }

        for (var j = 0; j < orders.length; j++) {
            exchange.CancelOrder(orders[j].Id, orders[j]);
            if (j < (orders.length-1)) {
                Sleep(Interval);
            }
        }
    }
}

var STATE_WAIT_IDLE     = 0;
var STATE_WAIT_BUY      = 1;
var STATE_WAIT_SELL     = 2;
var STATE_BUY           = 3;
var STATE_SELL          = 4;

var State = STATE_WAIT_IDLE;
var InitAccount = null;
var LastBuyPrice = 0;
var LastSellPrice = 0;
var LastHighPrice = 0;
var LastLowPrice = 0;
var LastRecord = null;
var Goingshort = false;

function onTick(exchange) {
    var oldState = State;

    if (State == STATE_WAIT_IDLE) {
        var records = exchange.GetRecords();
        if (!records || records.length < (EMA_Slow + 3)) {
            return;
        }
        // Price not change
        var newLast = records[records.length-1];
        if ((!LastRecord) || (LastRecord.Time == newLast.Time && LastRecord.Close == newLast.Close)) {
            LastRecord = newLast;
            return;
        }
        LastRecord = newLast;

        var emaFast = TA.EMA(records, EMA_Fast);
        var emaSlow = TA.EMA(records, EMA_Slow);
        if (emaFast[emaFast.length-1] > emaSlow[emaSlow.length-1]) {
            Goingshort = false;
            State = STATE_WAIT_BUY;
        } else if (EnableGoingShort && (emaFast[emaFast.length-1] < emaSlow[emaSlow.length-1])) {
            Goingshort = true;
            State = STATE_WAIT_SELL;
        } else {
            return;
        }
    }

    var ticker = _C(exchange.GetTicker);
    // Reset these two parameters
    if (oldState == STATE_WAIT_IDLE && State != STATE_WAIT_IDLE) {
        LastLowPrice = ticker.Last;
        LastHighPrice = ticker.Last;
    }

    // go long
    if (!Goingshort) {
        if (State == STATE_WAIT_BUY) {
            var lastDownRatio = Math.abs((LastHighPrice - LastLowPrice) / LastHighPrice) * 100;
            var currentUpRatio = Math.abs((ticker.Last - LastLowPrice) / ticker.Last) * 100;
            if (lastDownRatio > RatioDown && currentUpRatio > (RatioDown*(UpWeightingVal/100))) {
                State = STATE_BUY;
            } else {
                LastHighPrice = Math.max(LastHighPrice, ticker.Last);
                LastLowPrice = Math.min(LastLowPrice, ticker.Last);
            }
        } else if (State == STATE_WAIT_SELL) {
            var ratioStopLoss = Math.abs((LastHighPrice - ticker.Last) / LastHighPrice) * 100;
            var ratioStopProfit = Math.abs((ticker.Last - LastBuyPrice) / LastBuyPrice) * 100;
            var ratioMaxUp = Math.abs((LastHighPrice - LastBuyPrice) / LastBuyPrice) * 100;
            if (ticker.Last < LastBuyPrice && ratioStopLoss >= StopLoss) {
                State = STATE_SELL;
                Log("Start stop-loss, Current drop points:", _N(ratioStopLoss), "Current Price", ticker.Last, "Compare Price", _N(LastHighPrice));
            } else if (ticker.Last > LastBuyPrice && ticker.Last < LastHighPrice && ratioStopProfit <= (ratioMaxUp*StopProfitThreshold)) {
                State = STATE_SELL;
                Log("Start taking profit, Current rise points:", _N(ratioStopProfit), "Current Price", ticker.Last, "Compare Price", _N(LastBuyPrice));
            }
            LastHighPrice = Math.max(LastHighPrice, ticker.Last);
        }
    } else {
        if (State == STATE_WAIT_SELL) {
            var lastUpRatio = Math.abs((LastHighPrice - LastLowPrice) / LastHighPrice) * 100;
            var currentDownRatio = Math.abs((LastHighPrice - ticker.Last) / LastHighPrice) * 100;
            if (lastUpRatio > RatioUp && currentDownRatio > (RatioUp*(DownWeightingVal/100))) {
                State = STATE_SELL;
            } else {
                LastHighPrice = Math.max(LastHighPrice, ticker.Last);
                LastLowPrice = Math.min(LastLowPrice, ticker.Last);
            }
        } else if (State == STATE_WAIT_BUY) {
            var ratioStopLoss = Math.abs((ticker.Last - LastLowPrice) / LastLowPrice) * 100;
            var ratioStopProfit = Math.abs((LastSellPrice - ticker.Last) / LastSellPrice) * 100;
            var ratioMaxDown = Math.abs((LastSellPrice - LastLowPrice) / LastSellPrice) * 100;
            if (ticker.Last > LastSellPrice && ratioStopLoss >= StopLoss) {
                State = STATE_BUY;
                Log("Start stop-loss, Current rise points:", _N(ratioStopLoss), "Current Price", ticker.Last, "Compare Price", _N(LastSellPrice));
            } else if (ticker.Last < LastSellPrice && ticker.Last > LastLowPrice && ratioStopProfit <= (ratioMaxDown*StopProfitThreshold)) {
                State = STATE_BUY;
                Log("Start Taking Profit, Current drop points:", _N(ratioStopProfit), "Current Price", ticker.Last, "Compare Price", _N(LastLowPrice));
            }
            LastHighPrice = Math.max(LastHighPrice, ticker.Last);
            LastLowPrice = Math.min(LastLowPrice, ticker.Last);
        }

    }

    if (State != STATE_BUY && State != STATE_SELL) {
        return;
    }

    // Buy or Sell, Cancel pending orders first
    CancelPendingOrders();

    var account = _C(exchange.GetAccount);

    // go long
    if (!Goingshort) {
        if (State == STATE_BUY) {
            var price = ticker.Sell + SlidePrice;
            var amount = _N(account.Balance*0.99 / price);
            if (amount >= MinStock) {
                if (exchange.Buy(price, amount, "go long")) {
                    LastBuyPrice = LastHighPrice = price;
                } else {
                    Log("Failed to open a long position", price, amount, account);
                }
            } else {
                State = STATE_WAIT_SELL;
            }
        } else {
            var sellAmount = account.Stocks - InitAccount.Stocks;
            if (sellAmount > MinStock) {
                exchange.Sell(ticker.Buy - SlidePrice, sellAmount);
            } else {
                // No stocks, wait buy and log profit
                LogProfit(account.Balance - InitAccount.Balance, account);
                State = STATE_WAIT_IDLE;
            }
        }
    } else {
        if (State == STATE_BUY) {
            var price = ticker.Sell + SlidePrice;
            var amount = Math.min(_N(account.Balance*0.99 / price), InitAccount.Stocks - account.Stocks);
            if (amount >= MinStock) {
                exchange.Buy(price, amount);
            } else {
                LogProfit(account.Balance - InitAccount.Balance, account);
                State = STATE_WAIT_IDLE;
            }
        } else {
            var price = ticker.Buy - SlidePrice;
            var sellAmount = account.Stocks;
            if (sellAmount > MinStock) {
                exchange.Sell(ticker.Last - SlidePrice, sellAmount, "go short");
                LastSellPrice = LastLowPrice = price;
            } else {
                // No stocks, wait buy and log profit
                State = STATE_WAIT_BUY;
            }
        }
    }
}

function main() {
    InitAccount = _C(exchange.GetAccount);
    Log(exchange.GetName(), exchange.GetCurrency(), InitAccount);
    EnableGoingShort = EnableGoingShort && (InitAccount.Stocks > MinStock);
    LoopInterval = Math.max(LoopInterval, 1);
    while (true) {
        onTick(exchange);
        Sleep(LoopInterval*1000);
    }
}

```

> Detail

https://www.fmz.com/strategy/179

> Last Modified

2018-03-27 16:16:09
