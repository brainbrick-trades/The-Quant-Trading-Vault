
> Name

Futures-Backhand-Doubling-Algorithm

> Author

Zero

> Strategy Description

796Futures backhand doubling algorithm, open short or long first, you can also specify to continue in the last direction if it fails. If it fails, add the position by the specified multiple. The strategy is risky and is for learning only..

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Symbol|this_week|Contract name|
|MarginLevel|10|Leverage Size|
|OpType|0|Opening position direction: long|short|
|OpAmount|true|Open position quantity|
|OpMode|0|Position opening method: take order | pending order|
|MaxSpace|0.5|Pending order expiration distance|
|SlidePrice|0.1|Order Slippage Price (Yuan))|
|StopProfit|0.2|Take profit (percentage))|
|StopLoss|0.1|Stop loss (percentage))|
|ReverseRate|2|Reverse position add-on multiple|
|MaxLoss|10|Maximum number of reversals|
|ReverseMode|0|Reverse mode: reverse position|follow position|
|MinStock|0.01|Minimum transaction volume|
|SaveLocal|false|Save local log|
|Interval|true|Polling interval (seconds)|


> Source (javascript)

``` javascript

var FirstTradeType = [ORDER_TYPE_BUY, ORDER_TYPE_SELL][OpType];
var OrgAccount = null;
var Counter = {s : 0, f: 0};
var LastProfit = 0;
var AllProfit = 0;
var _Failed = 0;

function StripOrders(e, orderId) {
    var order = null;
    if (typeof(orderId) == 'undefined') {
        orderId = null;
    }
    while (true) {
        var dropped = 0;
        var orders = _C(e.GetOrders);
        for (var i = 0; i < orders.length; i++) {
            if (orders[i].Id == orderId) {
                order = orders[i];
            } else {
                var extra = "";
                if (orders[i].DealAmount > 0) {
                    extra = "Transaction: " + orders[i].DealAmount;
                } else {
                    extra = "unfilled";
                }
                e.SetDirection(orders[i].Type == ORDER_TYPE_BUY ? "buy" : "sell");
                e.CancelOrder(orders[i].Id, orders[i].Type == ORDER_TYPE_BUY ? "Buy Order" : "Sell Order", extra);
                dropped++;
            }
        }
        if (dropped == 0) {
            break;
        }
        Sleep(300);
    }
    return order;
}


var preMsg = "";
function GetAccount(e, waitFrozen) {
    if (typeof(waitFrozen) == 'undefined') {
        waitFrozen = false;
    }
    var account = null;
    var alreadyAlert = false;
    while (true) {
        account = _C(e.GetAccount);
        if (!waitFrozen || account.FrozenStocks < MinStock) {
            break;
        }
        if (!alreadyAlert) {
            alreadyAlert = true;
            Log("Found frozen funds or coins in the account", account);
        }
        Sleep(Interval);
    }
    msg = "Success: " + Counter.s + " times, Failed: " + Counter.f + " times, Current account currency: " + account.Stocks;
    if (account.FrozenStocks > 0) {
        msg += " Frozen Coins: " + account.FrozenStocks;
    }

    if (msg != preMsg) {
        preMsg = msg;
        LogStatus(msg, "#ff0000");
    }
    return account;
}

function GetPosition(e, orderType) {
    var positions = _C(e.GetPosition);
    if (typeof(orderType) == 'undefined') {
        return positions;
    }
    for (var i = 0; i < positions.length; i++) {
        if (positions[i].Type == orderType) {
            return positions[i];
        }
    }
    return null;
}

function GetTicker(e) {
    while (true) {
        var ticker = _C(e.GetTicker);
        if (ticker.Buy > 0 && ticker.Sell > 0 && ticker.Sell > ticker.Buy) {
            return ticker;
        }
        Sleep(100);
    }
}
// mode = 0 : direct buy, 1 : buy as buy1
function Trade(e, tradeType, tradeAmount, mode, slidePrice, maxSpace, retryDelay) {
    var initPosition = GetPosition(e, tradeType);
    var nowPosition = initPosition;
    var orderId = null;
    var prePrice = 0;
    var dealAmount = 0;
    var diffMoney = 0;
    var isFirst = true;
    var tradeFunc = tradeType == ORDER_TYPE_BUY ? e.Buy : e.Sell;
    var isBuy = tradeType == ORDER_TYPE_BUY;
    while (true) {
        var account = _C(e.GetAccount);
        var ticker = GetTicker(e);
        var tradePrice = 0;
        if (isBuy) {
            tradePrice = _N((mode == 0 ? ticker.Sell : ticker.Buy) + slidePrice, 4);
        } else {
            tradePrice = _N((mode == 0 ? ticker.Buy : ticker.Sell) - slidePrice, 4);
        }
        if (orderId == null) {
            if (isFirst) {
                isFirst = false;
            } else {
                nowPosition = GetPosition(e, tradeType);
            }
            dealAmount = _N((nowPosition ? nowPosition.Amount : 0) - (initPosition ? initPosition.Amount : 0), 6);
            var doAmount = Math.min(tradeAmount - dealAmount, account.Stocks * MarginLevel, 4);
            if (doAmount < MinStock) {
                break;
            }
            prePrice = tradePrice;
            e.SetDirection(tradeType == ORDER_TYPE_BUY ? "buy" : "sell");
            orderId = tradeFunc(tradePrice, doAmount);
        } else {
            if (mode == 0 || Math.abs(tradePrice - prePrice) > maxSpace) {
                orderId = null;
            }
            var order = StripOrders(exchange, orderId);
            if (order == null) {
                orderId = null;
            }
        }
        Sleep(retryDelay);
    }

    if (dealAmount <= 0) {
        return null;
    }

    return nowPosition;
}

function coverFutures(e, orderType) {
    var coverAmount = 0;
    while (true) {
        var positions = _C(e.GetPosition);
        var ticker = GetTicker(e);
        var found = 0;
        for (var i = 0; i < positions.length; i++) {
            if (positions[i].Type == orderType) {
                if (coverAmount == 0) {
                    coverAmount = positions[i].Amount;
                }
                if (positions[i].Type == ORDER_TYPE_BUY) {
                    e.SetDirection("closebuy");
                    e.Sell(ticker.Buy, positions[i].Amount);
                } else {
                    e.SetDirection("closesell");
                    e.Buy(ticker.Sell, positions[i].Amount);
                }
                found++;
            }
        }
        if (found == 0) {
            break;
        }
        Sleep(2000);
        StripOrders(e);
    }
    return coverAmount;
}


function loop(pos) {
    var tradeType = null;
    if (typeof(pos) == 'undefined' || !pos) {
        tradeType = FirstTradeType;
        pos = Trade(exchange, tradeType, OpAmount, OpMode, SlidePrice, MaxSpace, Interval);
        if (!pos) {
            throw "Unsuccessful start, opening position failed";
        } else {
            Log(tradeType == ORDER_TYPE_BUY ? "Long Position Opened" : "Short Position Opened", "Average Price:", pos.Price, "Quantity:", pos.Amount);
        }
    } else {
        tradeType = pos.Type;
    }
    var holdPrice = pos.Price;
    var holdAmount = pos.Amount;

    var openFunc = tradeType == ORDER_TYPE_BUY ? exchange.Buy : exchange.Sell;
    var coverFunc = tradeType == ORDER_TYPE_BUY ? exchange.Sell : exchange.Buy;

    var reversePrice = 0;
    var coverPrice = 0;
    var canOpen = true;

    if (tradeType == ORDER_TYPE_BUY) {
        reversePrice = _N(holdPrice * (1 - StopLoss), 4);
        coverPrice = _N(holdPrice * (1 + StopProfit), 4);
    } else {
        reversePrice = _N(holdPrice * (1 + StopLoss), 4);
        coverPrice = _N(holdPrice * (1 - StopProfit), 4);
    }

    var coverId = null;
    var msg = "Position price: " + holdPrice + " Stop loss price: " + reversePrice;

    for (var i = 0; i < 10; i++) {
        if (coverId) {
            break;
        }
        if (tradeType == ORDER_TYPE_BUY) {
            exchange.SetDirection("closebuy");
            coverId = exchange.Sell(coverPrice, holdAmount, msg);
        } else {
            exchange.SetDirection("closesell");
            coverId = exchange.Buy(coverPrice, holdAmount, msg);
        }

        Sleep(Interval);
    }

    if (!coverId) {
        StripOrders(exchange);
        throw "Order failed";
    }


    while (true) {
        Sleep(Interval);
        var ticker = GetTicker(exchange);
        if ((tradeType == ORDER_TYPE_BUY && ticker.Last < reversePrice) || (tradeType == ORDER_TYPE_SELL && ticker.Last > reversePrice)) {
            StripOrders(exchange);
            var coverAmount = coverFutures(exchange, tradeType);
            if (_Failed >= MaxLoss) {
                Counter.f++;
                Log("Exceeded maximum failure attempts", MaxLoss);
                break;
            }
            var reverseAmount = _N(coverAmount * ReverseRate, 4);

            var account = GetAccount(exchange, true);
            if (_N(account.Stocks * MarginLevel, 4) < reverseAmount) {
                Log("No reverse position open on the coin, Need to open a position: ", reverseAmount, "Individual/Unit, Only", account.Stocks, "Currency");
                Counter.f++;
                break;
            }
            var reverseType = tradeType;
            if (ReverseMode == 0) {
                reverseType = tradeType == ORDER_TYPE_BUY ? ORDER_TYPE_SELL : ORDER_TYPE_BUY;
            }
            var pos = Trade(exchange, reverseType, reverseAmount, OpMode, SlidePrice, MaxSpace, Interval);
            if (pos) {
                Log(reverseType == ORDER_TYPE_BUY ? "Long position" : "Short position", "Double position opening completed");
            }
            return pos;
        } else {
            var orders = _C(exchange.GetOrders);
            if (orders.length == 0) {
                Counter.s++;
                var account = GetAccount(exchange, true);
                LogProfit(account.Stocks, account);
                break;
            }
        }
    }
    return null;
}

function onexit() {
    StripOrders(exchange);
    Log("Exit");
}

function main() {
    if (exchange.GetName().indexOf("Futures") == -1) {
        throw "Only supports futures, spot not supported yet";
    }
    EnableLogLocal(SaveLocal);
    if (exchange.GetRate() != 1) {
        Log("Currency conversion disabled");
        exchange.SetRate(1);
    }

    StopProfit /= 100;
    StopLoss /= 100;

    var eName = exchange.GetName();
    if (eName == "Futures_CTP") {
        throw "Currently only supports cryptocurrency futures"
    }
    exchange.SetContractType(Symbol);
    exchange.SetMarginLevel(MarginLevel);
    Interval *= 1000;
    SetErrorFilter("502:|503:|unexpected|network|timeout|WSARecv|Connect|GetAddr|no such|reset|http|received|EOF");
    StripOrders(exchange);
    OrgAccount = GetAccount(exchange, true);
    LogStatus("Startup Successful");
    var pos = null;
    var positions = GetPosition(exchange);
    if (positions.length == 1) {
        pos = positions[0];
        Log("Found a position, Progress has been automatically restored");
    } else if (positions.length > 1) {
        throw "Detected more than one position";
    }
    while (true) {
        pos = loop(pos);
        if (!pos) {
            _Failed = 0;
        } else {
            _Failed++;
        }
        Sleep(Interval);
    }
}

```

> Detail

https://www.fmz.com/strategy/3648

> Last Modified

2019-06-11 09:15:37
