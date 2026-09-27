
> Name

Place-a-Fixed-Point-Entry-Order-and-a-Fixed-Point-Exit-Sell-Order

> Author

Zero

> Strategy Description

You can choose what time to enter and what time to leave. The system will force the opening and closing of positions. It will constantly try to open and close positions. The default is to enter and buy at 0 o'clock and exit at 8 o'clock. Set to enter 23 and exit 8, which means entering the market at 23 o'clock in the evening and leaving at 8 o'clock the next day. If it is set to 8.5, it means 8:30. Setting it to 8.6 means 8:36. The decimal point multiplied by 6 is the number of minutes. Stop loss can be disabled. If it is checked, stop loss will be enabled. If the stop loss point is 0.1, it means forced selling if the price falls by 0.1%. If the stop loss price refers to the highest price, it means that if you buy it for 1,000 and it rises to 2,000, you will stop the loss if 2,000 drops by 0.1%. If you do not refer to the highest price, you will stop the loss if it drops by 0.1% from the average buying price..

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|EnterHour|false|Entry time (hours)|
|LeaveHour|8|Exit time (hours))|
|SlidePrice|true|Slide Value|
|UsedFund|1000|Position Amount|
|RetryInterval|5|Retry Interval (Seconds))|
|StopLoss|0.5|Stop-loss point|
|EnableStopLoss|true|Whether to enable stop loss|
|RefHigh|true|Stop loss based on the highest reference price|
|StopProfit|0.5|take profit point|
|EnableStopProfit|false|Whether to enable take profit|


> Source (javascript)

``` javascript

// 0 means wait buy, 1 means wait sell
var state = 0;
var lastBuyAmount = 0;
var lastHighPrice = 0;
var lastBuyPrice = 0;
var initBalance = 0;


function cancelAllOrders() {
    var orders = null;
    while (!(orders = exchange.GetOrders())) {
        Sleep(2000);
    }
    
    if (orders.length > 0) {
        for (var j = 0; j < orders.length; j++) {
            exchange.CancelOrder(orders[j].Id);
            if (j < (orders.length-1)) {
                Sleep(2000);
            }
        }
    }
}

function MustBuy() {
    var buyAmount = 0;
    var initAccount = _C(exchange.GetAccount);
    if (initBalance == 0) {
        initBalance = initAccount.Balance;
        if (initAccount.Balance < UsedFund) {
            throw "Insufficient account balance, less than the set value " + UsedFund;
        }
    }

    
    UsedFund = Math.min(initAccount.Balance, UsedFund);
    
    var spend = 0;
    var buyAmount = 0;
    
    while (spend < UsedFund) {
        var ticker = _C(exchange.GetTicker);
        var amount = _N((UsedFund - spend) / (ticker.Last + SlidePrice));
        if (amount < 0.001) {
            break;
        }
        exchange.Buy(ticker.Last + SlidePrice, amount);
        Sleep(RetryInterval * 1000);
        cancelAllOrders();
        var account = _C(exchange.GetAccount);
        spend = initAccount.Balance - account.Balance;
        buyAmount = account.Stocks - initAccount.Stocks;
    }
    
    if (buyAmount > 0) {
        lastBuyPrice = lastHighPrice = (spend / buyAmount);
        Log("Average buying price", _N(lastHighPrice));
    }
    
    return buyAmount;
}

function MustSell(sellAmount) {
    var remaind = sellAmount;
    var initAccount = _C(exchange.GetAccount);
    while (remaind >= 0.001) {
        var ticker = _C(exchange.GetTicker);
        exchange.Sell(ticker.Last - SlidePrice, remaind);
        Sleep(RetryInterval * 1000);
        cancelAllOrders();
        var newAccount = _C(exchange.GetAccount);
        remaind -= (initAccount.Stocks - newAccount.Stocks);
        initAccount = newAccount;
    }
    LogProfit(initAccount.Balance - initBalance);
}

function onTick() {
    var now = new Date();
    var h = now.getHours() + (now.getMinutes() / 60);
    if (state == 0 && (
        (EnterHour < LeaveHour && h >= EnterHour && h < LeaveHour) || 
        (EnterHour > LeaveHour && (h >= EnterHour || h < LeaveHour))
        )) {
        lastBuyAmount = MustBuy();
        state = 1;
    } else if (state == 1 && (
        (EnterHour < LeaveHour && (h >= LeaveHour || h < EnterHour)) || 
        (EnterHour > LeaveHour && (h >= LeaveHour && h < EnterHour))
        )) {
        if (lastBuyAmount > 0) {
            MustSell(lastBuyAmount);
            lastBuyAmount = 0;
        }
        state = 0;
    } else if ((EnableStopProfit || EnableStopLoss) && lastBuyAmount > 0) {
        var ticker = _C(exchange.GetTicker);
        if (RefHigh) {
            lastHighPrice = Math.max(lastHighPrice, ticker.Last);
        }
        var ratioStopLoss = Math.abs((lastHighPrice - ticker.Last) / lastHighPrice);
        var ratioStopProfit = Math.abs((lastBuyPrice - ticker.Last) / lastBuyPrice);
        var shouldSell = false;
        
        if (EnableStopLoss && ticker.Last < lastHighPrice && (ratioStopLoss >= (StopLoss/100))) {
            // Stop loss
            Log("Start stop-loss, Current price drop points:", _N(ratioStopLoss*100), "Current Price", ticker.Last, "Compare Price", _N(lastHighPrice));
            shouldSell = true;
            
        } else if (EnableStopProfit && ticker.Last > lastBuyPrice && (ratioStopProfit >= (StopProfit/100))) {
            // Stop loss
            Log("Start taking profit, Current price increase points:", _N(ratioStopProfit*100), "Current Price", ticker.Last, "Compare Price", _N(lastBuyPrice));
            shouldSell = true;
        }
        
        if (shouldSell) {
            MustSell(lastBuyAmount);
            lastBuyAmount = 0;
        }
    }
}

function main() {
    if (EnterHour == LeaveHour) {
        throw "Entry time and exit time cannot be the same!";
    }
    Log(_C(exchange.GetAccount));
    while(true) {
        onTick();
        Sleep(60000);
    }
} 


```

> Detail

https://www.fmz.com/strategy/64

> Last Modified

2018-03-27 15:53:49
