
> Name

Plan-to-Entrust-Selling

> Author

Zero

> Strategy Description

Plan to entrust selling, and sell after the price rises above or falls below the specified price. If you use a market order, you only need to fill in the selling quantity. If you use a limit order, you need to specify the selling price.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|OpType|0|Order type: market order | limit order|
|TriggerPrice|2600|Trigger price|
|SellPrice|2610|Limit order - selling price|
|SellAmount|3|Sell Quantity|
|LoopInterval|true|Detection interval (seconds))|
|MinStock|0.01|Minimum trading coin quantity|


> Source (javascript)

``` javascript

var InitPrice = 0;
var Interval = 300;
var UseMarketOrder = (OpType == 0);

function _N(v, precision) {
    if (typeof(precision) != 'number') {
        precision = 4;
    }
    var s = v.toString().split(".");
    if (s.length < 2 || s[1].length <= precision) {
        return v;
    }
    var b = Math.pow(10, precision);
    return Math.floor(parseFloat(v.toFixed(Math.min(20, precision+10)))*b)/b;
}

function GetTicker() {
    var ticker;
    while (!(ticker = exchange.GetTicker())) {
        Sleep(Interval);
    }
    return ticker;
}


function GetDepth(e) {
    if (typeof(e) == 'undefined') {
        e = exchange;
    }
    var depth;
    while (true) {
        depth = e.GetDepth();
        if (depth && depth.Asks.length > 0 && depth.Bids.length > 0 && depth.Asks[0].Price > depth.Bids[0].Price) {
            break;
        }
        Sleep(Interval);
    }
    return depth;
}

function GetTickerFromDepth(e) {
    var depth = GetDepth(e);
    return {Buy : depth.Bids[0].Price, Sell : depth.Asks[0].Price, BuyAmount: depth.Bids[0].Amount, SellAmount: depth.Asks[0].Amount, depth: depth};
}

function GetOrders() {
    var orders;
    while (!(orders = exchange.GetOrders())) {
        Sleep(Interval);
    }
    return orders;
}

function GetAccount() {
    var account;
    while (!(account = exchange.GetAccount())) {
        Sleep(Interval);
    }
    return account;
}


function cancelPending() {
    var ret = false;
    while (true) {
        var orders = GetOrders();
        if (orders.length == 0) {
            break;
        }
        for (var j = 0; j < orders.length; j++) {
            exchange.CancelOrder(orders[j].Id, orders[j]);
            ret = true;
        }
    }
    return ret;
}

function ensureSell() {
    var account = GetAccount();
    var initAccount = account;
    var minStock = MinStock;
    var isfirst = true;
    while (true) {
        cancelPending();
        if (!isfirst) {
            account = GetAccount();
        }
        isfirst = false;
        var needSell = _N(SellAmount - (initAccount.Stocks - account.Stocks));
        var ticker = GetTickerFromDepth();
        var price = _N(ticker.Buy);
        var amount = Math.min(ticker.BuyAmount, needSell);
        if (needSell < minStock) {
            Log('Planned order completed');
            break;
        }
        exchange.Sell(price, amount);
        Sleep(100);
    }
    return _N((account.Balance - initAccount.Balance) / SellAmount);
}

function SellIt() {
    if (UseMarketOrder) {
        var avgPrice = ensureSell();
        Log("Market order sell completed, Average Price: ", avgPrice);
    } else {
        var success = false;
        for (var i = 0; i < 20; i++) {
            if (exchange.Sell(SellPrice, SellAmount) > 0) {
                success = true;
                break;
            }
            Sleep(Interval);
        }
        Log(success ? "Limit order placed successfully" : "Limit order placement failed");
    }
}

function onTick() {
    var doIt = false;
    var ticker = GetTicker();
    if (InitPrice > TriggerPrice && ticker.Last < TriggerPrice) {
        Log('Price drops below ', TriggerPrice, 'element, Start selling according to plan');
        SellIt();
        doIt = true;
    } else if (InitPrice < TriggerPrice && ticker.Last > TriggerPrice) {
        Log('Price rises above ', TriggerPrice, 'element, Start selling according to plan');
        SellIt();
        doIt = true;
    }
    return doIt;
}

function main() {
    var account = GetAccount();
    var ticker = GetTicker();
    Log('Current Account: ', account);
    if (account.Stocks < SellAmount) {
        throw "The account does not have enough coins to sell";
    }
    
    InitPrice = ticker.Last;
    
    if (UseMarketOrder) {
        msg = 'Use market price to sell ' + SellAmount + ' Individual/Unit ' + exchange.GetCurrency();
    } else {
        msg = 'Use Limit Price When ' + SellPrice + ' sell ' + SellAmount + 'Individual/Unit ' + exchange.GetCurrency();
    }
    
    Log('Current Price: ', InitPrice, ticker.Last > TriggerPrice ? 'Price drops below' : 'Price rises above', TriggerPrice, msg);
    
    while (!onTick()) {
        Sleep(LoopInterval * 1000);
    }
}

```

> Detail

https://www.fmz.com/strategy/747

> Last Modified

2018-06-05 16:29:07
