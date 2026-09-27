
> Name

OKCoin-Futures-Conditional-Trigger-Order-with-Stop-Loss

> Author

Zero

> Strategy Description

OKCoinPlace orders when futures conditions are triggered, and enable automatic conditional stop-loss after execution.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|CType|0|Currency type: RMB|USD|
|ContractType|0|Contract types: This Week | Next Week | This Month | Quarter|
|OpType|0|Operation type: Open long|Open short|
|MLevel|0|Leverage size: 10x | 20x|
|TriggerType|0|Triggering method: rising or falling | falling|
|TriggerPrice|2000|Trigger price for opening positions (CNY))|
|OrderPrice|2005|Opening order price (CNY)|
|OrderAmount|true|Opening order amount|
|StopLossTrigger|1800|Stop loss trigger price (CNY)|
|StopOrderPrice|1790|Stop loss order price (CNY)|
|LoopInterval|300|Polling interval (milliseconds)|


> Source (javascript)

``` javascript
var _ContractType = ["this_week", "next_week", "month", "quarter"][ContractType];
var _TradeType = ["buy", "sell"][OpType];
var _MarginLevel = [10, 20][MLevel];
var Interval = 300;

function GetTicker() {
    var ticker;
    while (!(ticker = exchange.GetTicker())) {
        Sleep(Interval);
    }
    return ticker;
}

function GetOrders() {
    var orders;
    while (!(orders = exchange.GetOrders())) {
        Sleep(Interval);
    }
    return orders;
}

function GetAccount(maxRetry) {
    var account;
    var counter = 0;
    while (!(account = exchange.GetAccount())) {
        Sleep(Interval);
        counter++;
        if (typeof(maxRetry) == 'number' && counter > maxRetry) {
            break;
        }
    }
    return account;
}

function now() {
    var t = new Date();
    var year = t.getFullYear();
    var month = t.getMonth() + 1;
    var day = t.getDate();
    var hour = t.getHours();
    var minute = t.getMinutes();
    var second = t.getSeconds();

    if (month < 10) {
        month = '0' + month;
    }
    if (day < 10) {
        day = '0' + day;
    }
    if (hour < 10) {
        hour = '0' + hour;
    }
    if (minute < 10) {
        minute = '0' + minute;
    }
    if (second < 10) {
        second = '0' + second;
    }

    return year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second;
}

function main() {
    if (exchange.GetName() != 'Futures_OKCoin') {
        throw "This strategy is a dedicated strategy for OKCoin futures";
    }
    if (CType == 1) {
        exchange.SetRate(1);
    }
    Log(CType == 0 ? "Currency isRMB" : "Currency is USD...");
    
    var account = GetAccount(10);
    if (!account) {
        throw "Account information acquisition failed. Please check if the API configuration is correct; only isolated margin mode is supported";
    }

    SetErrorFilter("502:|503:|network|timeout|WSARecv|Connect|GetAddr|no such|reset");
    Log(account);
    Log('Current robotID: ', _G(), 'Start Running...');
    
    exchange.SetContractType(_ContractType);
    exchange.SetMarginLevel(_MarginLevel);

    LoopInterval = Math.max(LoopInterval, 100);

    var ticker = GetTicker();
    var preLast = 0;
    Log('Current Price:', ticker.Last, 'Waiting for price', TriggerType == 0 ? 'Rise exceed' : 'Break below', TriggerPrice, 'element...');
    while (true) {
        if (TriggerType == 1 && ticker.Last < TriggerPrice) {
            Log('Price drops below ', TriggerPrice, 'element, Start placing orders as planned');
            break;
        } else if (TriggerType == 0 && ticker.Last > TriggerPrice) {
            Log('Price rises above ', TriggerPrice, 'element, Start placing orders as planned');
            break;
        }
        ticker = GetTicker();
        if (ticker.Last != preLast) {
            preLast = ticker.Last;
            LogStatus("Latest transaction price: ", ticker.Last, now());
        }
        Sleep(LoopInterval);
    }
    Log("Last transaction price: ", ticker.Last);
    exchange.SetDirection(_TradeType);
    var pfn = _TradeType == "buy" ? exchange.Buy : exchange.Sell;
    var orderId = pfn(OrderPrice, OrderAmount);
    if (!orderId) {
        Log("First order failed, Retry last time!");
        orderId = pfn(OrderPrice, OrderAmount);
    }

    if (!orderId) {
        throw "Order failed";
    }
    Log("Start waiting for order completion, Order number:", orderId);
    while (true) {
        var order = exchange.GetOrder(orderId);
        if (order && order.Status == ORDER_STATE_CLOSED) {
            break;
        }
        Sleep(LoopInterval);
    }
    Log("Order completed, Start waiting for stop-loss...");

    var ticker = GetTicker();
    Log('Current Price:', ticker.Last, 'Stop-loss condition:', _TradeType == "buy" ? 'Break below' : 'Rise exceed', StopLossTrigger, 'element');
    while (true) {
        if (_TradeType == "buy" && ticker.Last <= StopLossTrigger) {
            Log('Price drops below ', StopLossTrigger, 'element, Start stop-loss.');
            break;
        } else if (_TradeType == "sell" && ticker.Last >= StopLossTrigger) {
            Log('Price rises above ', StopLossTrigger, 'element, Start stop-loss.');
            break;
        }
        ticker = GetTicker();
        if (ticker.Last != preLast) {
            preLast = ticker.Last;
            LogStatus("Latest transaction price: ", ticker.Last, now());
        }
        Sleep(LoopInterval);
    }
    for (var i = 0; i < 2; i++) {
        if (_TradeType == "buy") {
            exchange.SetDirection("closebuy");
            orderId = exchange.Sell(StopOrderPrice, OrderAmount);
        } else {
            exchange.SetDirection("closesell");
            orderId = exchange.Buy(StopOrderPrice, OrderAmount);
        }
        if (orderId) {
            break;
        }
    }
    Log("Complete all operations, Strategy exit.");
}
```

> Detail

https://www.fmz.com/strategy/2169

> Last Modified

2014-12-10 15:33:25
