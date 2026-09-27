
> Name

Plan-to-Entrust-Buying

> Author

Zero

> Strategy Description

Plan to entrust buying, and carry out the buying operation after the price rises above or falls below the specified price. If you use a market price order, just write the purchase amount. If you use a limit order, you need to specify the price and number of the limit order.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|OpType|0|Order type: market order | limit order|
|TriggerPrice|2600|Trigger price|
|MarketUsedMoney|10000|Market order - purchase amount|
|BuyPrice|2610|Limit order - purchase price|
|BuyAmount|3|Limit order - purchase quantity|
|LoopInterval|200|Detection interval (milliseconds))|
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
    return Math.floor(parseFloat(v.toFixed(Math.min(10, precision+5)))*b)/b;
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

function ensureBuy() {
    var account = GetAccount();
    var initAccount = account;
    var minStock = MinStock;
    var isfirst = true;
    var c = 0;
    while (true) {
        cancelPending();
        if (!isfirst) {
            account = GetAccount();
        }
        isfirst = false;
        var needCost = _N(MarketUsedMoney - (initAccount.Balance - account.Balance));
        var ticker = GetTickerFromDepth();
        var price = _N(ticker.Sell);
        var amount = Math.min(ticker.SellAmount, _N(needCost / price));
        if (_N(needCost / price) < minStock) {
            Log('Planned order completed');
            break;
        }
        exchange.Buy(price, amount);
        Sleep(100);
    }
    var realBuy = _N(account.Stocks - initAccount.Stocks);
    return realBuy > 0 ? _N((initAccount.Balance - account.Balance) / realBuy) : 0;
}

function BuyIt() {
    if (UseMarketOrder) {
        var avgPrice = ensureBuy();
        Log("Market order buy completed, Average Price: ", avgPrice);
    } else {
        var success = false;
        for (var i = 0; i < 20; i++) {
            if (exchange.Buy(BuyPrice, BuyAmount) > 0) {
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
        Log('Price drops below ', TriggerPrice, 'element, Start buying according to plan');
        BuyIt();
        doIt = true;
    } else if (InitPrice < TriggerPrice && ticker.Last > TriggerPrice) {
        Log('Price rises above ', TriggerPrice, 'element, Start buying according to plan');
        BuyIt();
        doIt = true;
    }
    return doIt;
}

function main() {
    var account = GetAccount();
    var ticker = GetTicker();
    Log('Current Account: ', account);
    if (account.Balance < (UseMarketOrder ? MarketUsedMoney : (BuyPrice * BuyAmount))) {
        throw "The account does not have enough money to buy coins";
    }
    
    InitPrice = ticker.Last;
    
    if (UseMarketOrder) {
        msg = 'Use market price to buy ' + MarketUsedMoney + ' Yuan (currency) ' + exchange.GetCurrency();
    } else {
        msg = 'Use Limit Price When ' + BuyPrice + ' buy ' + BuyAmount + 'Individual/Unit ' + exchange.GetCurrency();
    }
    
    Log('Current Price: ', InitPrice, ticker.Last > TriggerPrice ? 'Price drops below' : 'Price rises above', TriggerPrice, msg);
    
    while (!onTick()) {
        Sleep(LoopInterval);
    }
}

```

> Detail

https://www.fmz.com/strategy/638

> Last Modified

2018-06-05 16:31:29
