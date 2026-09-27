
> Name

Mesh-Deformation-Strategy-for-Single-Sided-Mesh

> Author

Zero

> Strategy Description

Grid can customize direction
Buy first and sell later:
The grid will place buy orders downwards from the first price. The interval between each buy order is the "price interval" parameter. The number of pending orders is "single quantity". If the "total quantity" of buy orders is placed, after any buy order is completed, the program will add the "spread (yuan)" parameter to the purchase price to place a sell order. After selling, the buy order will be placed again at the original price of this grid.
Sell first then buy:
Operation is exactly the opposite

The biggest risk of the strategy is a one-sided market, where price fluctuations exceed the grid range.

Grid has automatic stop loss and moving function

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|OpType|0|Grid direction: Buy first, then sell | Sell first, then buy|
|FirstPriceAuto|true|First price automatically|
|FirstPrice|100|First price|
|AllNum|10|Total quantity|
|PriceGrid|true|Price interval|
|PriceDiff|2|Price difference (yuan)|
|AmountType|0|Order size: Same buy and sell volume | Custom quantity|
|AmountOnce|0.1|Single transaction quantity|
|BAmountOnce|0.1|Buy order size|
|SAmountOnce|0.1|Sell order size|
|AmountCoefficient|*1|volume difference|
|AmountDot|3|Maximum decimal places for quantity|
|EnableProtectDiff|false|Enable spread protection|
|ProtectDiff|20|Entry-point spread protection|
|CancelAllWS|true|Cancel all orders when stopping|
|CheckInterval|2000|Polling Interval|
|Interval|1300|Failed retry interval|
|RestoreProfit|false|Restore last profit|
|LastProfit|false|Last Profit|
|ProfitAsOrg|false|Last profit included in average price|
|EnableAccountCheck|true|Activate fund inspection|
|EnableStopLoss|false|Enable stop loss|
|StopLoss|100|Maximum floating loss (CNY))|
|StopLossMode|0|Action after stop loss: recover and exit | recover and redeploy|
|EnableStopWin|false|Enable take profit|
|StopWin|120|Maximum floating profit (CNY))|
|StopWinMode|0|Action after taking profit: recover and exit | recover and redeploy|
|AutoMove|false|Automatic movement|
|MaxDistance|20|Maximum distance (yuan).)|
|MaxIdle|7200|Maximum idle (seconds).)|
|EnableDynamic|false|Enable dynamic order placement|
|DynamicMax|30|Order expiration distance (CNY))|
|ResetData|true|Clear all data at startup|
|Precision|5|Price decimal place length|
|XPrecision|5|Decimal length for order quantity|
|MinStock|0.001|Minimum transaction volume|




|Button|Default|Description|
|----|----|----|
|Close network|__button__|stop and balance back to initial state|


> Source (javascript)

``` javascript
function hasOrder(orders, orderId) {
    for (var i = 0; i < orders.length; i++) {
        if (orders[i].Id == orderId) {
            return true;
        }
    }
    return false;
}


function cancelPending() {
    var ret = false;
    while (true) {
        if (ret) {
            Sleep(Interval);
        }
        var orders = _C(exchange.GetOrders);
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

function valuesToString(values, pos) {
    var result = '';
    if (typeof(pos) === 'undefined') {
        pos = 0;
    }
    for (var i = pos; i < values.length; i++) {
        if (i > pos) {
            result += ' ';
        }
        if (values[i] === null) {
            result += 'null';
        } else if (typeof(values[i]) == 'undefined') {
            result += 'undefined';
        } else {
            switch (values[i].constructor.name) {
                case 'Date':
                case 'Number':
                case 'String':
                case 'Function':
                    result += values[i].toString();
                    break;
                default:
                    result += JSON.stringify(values[i]);
                    break;
            }
        }
    }
    return result;
}

function Trader() {
    var vId = 0;
    var orderBooks = [];
    var hisBooks = [];
    var orderBooksLen = 0;
    this.Buy = function(price, amount, extra) {
        if (typeof(extra) === 'undefined') {
            extra = '';
        } else {
            extra = valuesToString(arguments, 2);
        }
        vId++;
        var orderId = "V" + vId;
        orderBooks[orderId] = {
            Type: ORDER_TYPE_BUY,
            Status: ORDER_STATE_PENDING,
            Id: 0,
            Price: price,
            Amount: amount,
            Extra: extra
        };
        orderBooksLen++;
        return orderId;
    };
    this.Sell = function(price, amount, extra) {
        if (typeof(extra) === 'undefined') {
            extra = '';
        } else {
            extra = valuesToString(arguments, 2);
        }
        vId++;
        var orderId = "V" + vId;
        orderBooks[orderId] = {
            Type: ORDER_TYPE_SELL,
            Status: ORDER_STATE_PENDING,
            Id: 0,
            Price: price,
            Amount: amount,
            Extra: extra
        };
        orderBooksLen++;
        return orderId;
    };
    this.GetOrders = function() {
        var orders = _C(exchange.GetOrders);
        for (orderId in orderBooks) {
            var order = orderBooks[orderId];
            if (order.Status !== ORDER_STATE_PENDING) {
                continue;
            }
            var found = false;
            for (var i = 0; i < orders.length; i++) {
                if (orders[i].Id == order.Id) {
                    found = true;
                    break;
                }
            }
            if (!found) {
                orders.push(orderBooks[orderId]);
            }
        }
        return orders;
    }
    this.GetOrder = function(orderId) {
        if (orderId && orderId.toString().indexOf("V") != 0) {
            return exchange.GetOrder(orderId);
        }
        if (typeof(hisBooks[orderId]) !== 'undefined') {
            return hisBooks[orderId];
        }
        if (typeof(orderBooks[orderId]) !== 'undefined') {
            return orderBooks[orderId];
        }
        return null;
    };
    this.Len = function() {
        return orderBooksLen;
    };
    this.RealLen = function() {
        var n = 0;
        for (orderId in orderBooks) {
            if (orderBooks[orderId].Id > 0) {
                n++;
            }
        }
        return n;
    };
    this.Poll = function(ticker, priceDiff) {
        var orders = _C(exchange.GetOrders);
        for (orderId in orderBooks) {
            var order = orderBooks[orderId];
            if (order.Id > 0) {
                var found = false;
                for (var i = 0; i < orders.length; i++) {
                    if (order.Id == orders[i].Id) {
                        found = true;
                    }
                }
                if (!found) {
                    order.Status = ORDER_STATE_CLOSED;
                    hisBooks[orderId] = order;
                    delete(orderBooks[orderId]);
                    orderBooksLen--;
                    continue;
                }
            }
            var diff = _N(order.Type == ORDER_TYPE_BUY ? (ticker.Buy - order.Price) : (order.Price - ticker.Sell));
            var pfn = order.Type == ORDER_TYPE_BUY ? exchange.Buy : exchange.Sell;
            if (order.Id == 0 && diff <= priceDiff) {
                var realId = pfn(order.Price, order.Amount, order.Extra + "(distance: " + diff + (order.Type == ORDER_TYPE_BUY ? (" Buy one: " + ticker.Buy) : (" Sell one: " + ticker.Sell))+")");
                if (realId) {
                    order.Id = realId;
                }
            } else if (order.Id > 0 && diff > (priceDiff + 1)) {
                var ok = true;
                do {
                    ok = true;
                    exchange.CancelOrder(order.Id, "Unnecessary" + (order.Type == ORDER_TYPE_BUY ? "Buy Order" : "Sell Order"), "order price:", order.Price, "Amount:", order.Amount, ", distance:", diff, order.Type == ORDER_TYPE_BUY ? ("Buy one: " + ticker.Buy) : ("Sell one: " + ticker.Sell));
                    Sleep(200);
                    orders = _C(exchange.GetOrders);
                    for (var i = 0; i < orders.length; i++) {
                        if (orders[i].Id == order.Id) {
                            ok = false;
                        }
                    }
                } while (!ok);
                order.Id = 0;
            }
        }
    };
}

function balanceAccount(orgAccount, initAccount) {
    cancelPending();
    var nowAccount = _C(exchange.GetAccount);
    var slidePrice = 0.2;
    var ok = true;
    while (true) {
        var diff = _N(nowAccount.Stocks - initAccount.Stocks);
        if (Math.abs(diff) < MinStock) {
            break;
        }
        var depth = _C(exchange.GetDepth);
        var books = diff > 0 ? depth.Bids : depth.Asks;
        var n = 0;
        var price = 0;
        for (var i = 0; i < books.length; i++) {
            n += books[i].Amount;
            if (n >= Math.abs(diff)) {
                price = books[i].Price;
                break;
            }
        }
        var pfn = diff > 0 ? exchange.Sell : exchange.Buy;
        var amount = Math.abs(diff);
        var price = diff > 0 ? (price - slidePrice) : (price + slidePrice);
        Log("Start balancing", (diff > 0 ? "sell" : "buy"), amount, "Currency");
        if (diff > 0) {
            amount = Math.min(nowAccount.Stocks, amount);
        } else {
            amount = Math.min(nowAccount.Balance / price, amount);
        }
        if (amount < MinStock) {
            Log("Insufficient funds, Unable to balance to the initial state");
            ok = false;
            break;
        }
        pfn(price, amount);
        Sleep(1000);
        cancelPending();
        nowAccount = _C(exchange.GetAccount);
    }
    if (ok) {
        LogProfit(_N(nowAccount.Balance - orgAccount.Balance));
        Log("Balance completed", nowAccount);
    }
}

var STATE_WAIT_OPEN = 0;
var STATE_WAIT_COVER = 1;
var STATE_WAIT_CLOSE = 2;
var ProfitCount = 0;
var BuyFirst = true;
var IsSupportGetOrder = true;
var LastBusy = 0;

function setBusy() {
    LastBusy = new Date();
}

function isTimeout() {
    if (MaxIdle <= 0) {
        return false;
    }
    var now = new Date();
    if (((now.getTime() - LastBusy.getTime()) / 1000) >= MaxIdle) {
        LastBusy = now;
        return true;
    }
    return false;
}

function onexit() {
    if (CancelAllWS) {
        Log("Exiting, Try to cancel all pending orders");
        cancelPending();
    }
    Log("The strategy successfully stopped");
    Log(_C(exchange.GetAccount));
}


function fishing(orgAccount, fishCount) {
    setBusy();
    var account = _C(exchange.GetAccount);
    Log(account);
    var InitAccount = account;
    var ticker = _C(exchange.GetTicker);
    var amount = _N(AmountOnce);
    var amountB = [amount];
    var amountS = [amount];
    if (typeof(AmountType) !== 'undefined' && AmountType == 1) {
        for (var idx = 0; idx < AllNum; idx++) {
            amountB[idx] = BAmountOnce;
            amountS[idx] = SAmountOnce;
        }
    } else {
        for (var idx = 1; idx < AllNum; idx++) {
            switch (AmountCoefficient[0]) {
                case '+':
                    amountB[idx] = amountB[idx - 1] + parseFloat(AmountCoefficient.substring(1));
                    break;
                case '-':
                    amountB[idx] = amountB[idx - 1] - parseFloat(AmountCoefficient.substring(1));
                    break;
                case '*':
                    amountB[idx] = amountB[idx - 1] * parseFloat(AmountCoefficient.substring(1));
                    break;
                case '/':
                    amountB[idx] = amountB[idx - 1] / parseFloat(AmountCoefficient.substring(1));
                    break;
            }
            amountB[idx] = _N(amountB[idx], AmountDot);
            amountS[idx] = amountB[idx];
        }
    }
    if (FirstPriceAuto) {
        FirstPrice = BuyFirst ? _N(ticker.Buy - PriceGrid, Precision) : _N(ticker.Sell + PriceGrid, Precision);
    }
    // Initialize fish table
    var fishTable = {};
    var uuidTable = {};
    var needStocks = 0;
    var needMoney = 0;
    var actualNeedMoney = 0;
    var actualNeedStocks = 0;
    var notEnough = false;
    var canNum = 0;
    for (var idx = 0; idx < AllNum; idx++) {
        var price = _N((BuyFirst ? FirstPrice - (idx * PriceGrid) : FirstPrice + (idx * PriceGrid)), Precision);
        needStocks += amountS[idx];
        needMoney += price * amountB[idx];
        if (BuyFirst) {
            if (_N(needMoney) <= _N(account.Balance)) {
                actualNeedMondy = needMoney;
                actualNeedStocks = needStocks;
                canNum++;
            } else {
                notEnough = true;
            }
        } else {
            if (_N(needStocks) <= _N(account.Stocks)) {
                actualNeedMondy = needMoney;
                actualNeedStocks = needStocks;
                canNum++;
            } else {
                notEnough = true;
            }
        }
        fishTable[idx] = STATE_WAIT_OPEN;
        uuidTable[idx] = -1;
    }
    if (!EnableAccountCheck && (canNum < AllNum)) {
        Log("Warning, Current funds can only be used for", canNum, "Number of grids, Total network requires", (BuyFirst ? needMoney : needStocks), "Please keep funds sufficient");
        canNum = AllNum;
    }
    if (BuyFirst) {
        if (EnableProtectDiff && (FirstPrice - ticker.Sell) > ProtectDiff) {
            throw "First buy price compared to market sell1high price" + _N(FirstPrice - ticker.Sell, Precision) + ' element';
        } else if (EnableAccountCheck && account.Balance < _N(needMoney)) {
            if (fishCount == 1) {
                throw "Insufficient funds, Need" + _N(needMoney) + "element";
            } else {
                Log("Insufficient funds, Need", _N(needMoney), "element, Program only does", canNum, "Number of grids #ff0000");
            }
        } else {
            Log('Expected funds to be used: ', _N(needMoney), "element");
        }
    } else {
        if (EnableProtectDiff && (ticker.Buy - FirstPrice) > ProtectDiff) {
            throw "First sell price compared to market buy1high price " + _N(ticker.Buy - FirstPrice, Precision) + ' element';
        } else if (EnableAccountCheck && account.Stocks < _N(needStocks)) {
            if (fishCount == 1) {
                throw "Insufficient coins, Need " + _N(needStocks) + " Currency";
            } else {
                Log("Insufficient funds, Need", _N(needStocks), "Currency, Program only does", canNum, "Number of grids #ff0000");
            }
        } else {
            Log('Estimated amount of coins to be used: ', _N(needStocks), "Individual/Unit, Approximately", _N(needMoney), "element");
        }
    }

    var trader = new Trader();
    var OpenFunc = BuyFirst ? exchange.Buy : exchange.Sell;
    var CoverFunc = BuyFirst ? exchange.Sell : exchange.Buy;
    if (EnableDynamic) {
        OpenFunc = BuyFirst ? trader.Buy : trader.Sell;
        CoverFunc = BuyFirst ? trader.Sell : trader.Buy;
    }
    var ts = new Date();
    var preMsg = "";
    var profitMax = 0;
    while (true) {
        var now = new Date();
        var table = null;
        if (now.getTime() - ts.getTime() > 5000) {
            if (typeof(GetCommand) == 'function' && GetCommand() == "close the net") {
                Log("Start executing commands to close network operations");
                balanceAccount(orgAccount, InitAccount);
                return false;
            }
            ts = now;
            var nowAccount = _C(exchange.GetAccount);
            var ticker = _C(exchange.GetTicker);
            if (EnableDynamic) {
                trader.Poll(ticker, DynamicMax);
            }
            var amount_diff = (nowAccount.Stocks + nowAccount.FrozenStocks) - (InitAccount.Stocks + InitAccount.FrozenStocks);
            var money_diff = (nowAccount.Balance + nowAccount.FrozenBalance) - (InitAccount.Balance + InitAccount.FrozenBalance);
            var floatProfit = _N(money_diff + (amount_diff * ticker.Last));
            var floatProfitAll = _N((nowAccount.Balance + nowAccount.FrozenBalance - orgAccount.Balance - orgAccount.FrozenBalance) + ((nowAccount.Stocks + nowAccount.FrozenStocks - orgAccount.Stocks - orgAccount.FrozenStocks) * ticker.Last));
            var isHold = Math.abs(amount_diff) >= MinStock;
            if (isHold) {
                setBusy();
            }

            profitMax = Math.max(floatProfit, profitMax);
            if (EnableAccountCheck && EnableStopLoss) {
                if ((profitMax - floatProfit) >= StopLoss) {
                    Log("Current floating profit and loss", floatProfit, "Highest profit point: ", profitMax, "Start stop-loss");
                    balanceAccount(orgAccount, InitAccount);
                    if (StopLossMode == 0) {
                        throw "Stop loss exit";
                    } else {
                        return true;
                    }
                }
            }
            if (EnableAccountCheck && EnableStopWin) {
                if (floatProfit > StopWin) {
                    Log("Current floating profit and loss", floatProfit, "Start Taking Profit");
                    balanceAccount(orgAccount, InitAccount);
                    if (StopWinMode == 0) {
                        throw "Take Profit Exit";
                    } else {
                        return true;
                    }
                }
            }
            var distance = 0;
            if (EnableAccountCheck && AutoMove) {
                if (BuyFirst) {
                    distance = ticker.Last - FirstPrice;
                } else {
                    distance = FirstPrice - ticker.Last;
                }
                var refish = false;
                if (!isHold && isTimeout()) {
                    Log("Empty position for too long, Start moving the mesh");
                    refish = true;
                }
                if (distance > MaxDistance) {
                    Log("Prices exceed the grid range by too much, Start moving the mesh, Current distance: ", _N(distance, Precision), "Current Price:", ticker.Last);
                    refish = true;
                }
                if (refish) {
                    balanceAccount(orgAccount, InitAccount);
                    return true;
                }
            }

            var holdDirection, holdAmount = "--",
                holdPrice = "--";
            if (isHold) {
                if (RestoreProfit && ProfitAsOrg) {
                    if (BuyFirst) {
                        money_diff += LastProfit;
                    } else {
                        money_diff -= LastProfit;
                    }
                }
                holdAmount = amount_diff;
                holdPrice = (-money_diff) / amount_diff;
                if (!BuyFirst) {
                    holdAmount = -amount_diff;
                    holdPrice = (money_diff) / -amount_diff;
                }
                holdAmount = _N(holdAmount, 4);
                holdPrice = _N(holdPrice, Precision);
                holdDirection = BuyFirst ? "Long : Short";
            } else {
                holdDirection = "--";
            }
            table = {
                type: 'table',
                title: 'Running Status',
                cols: ['Use funds', 'Position held', 'Position size', 'Average position price', 'Total floating profit and loss', 'Current grid profit and loss', 'Number of net casts', 'Grid offset', 'Real order', 'Latest currency price''],
                rows: [
                    [_N(actualNeedMondy, 4), holdDirection, holdAmount, holdPrice, _N(floatProfitAll, 4) + ' ( ' + _N(floatProfitAll * 100 / actualNeedMondy, 4) + ' % )', floatProfit, fishCount, (AutoMove && distance > 0) ? ((BuyFirst ? "upward" : "downward") + "deviation: " + _N(distance) + " element") : "--", trader.RealLen(), ticker.Last]
                ]
            };
            
        }
        var orders = _C(trader.GetOrders);
        if (table) {
            if (!EnableDynamic) {
                table.rows[0][8] = orders.length;
            }
            LogStatus('`' + JSON.stringify(table) + '`');
        }
        for (var idx = 0; idx < canNum; idx++) {
            var openPrice = _N((BuyFirst ? FirstPrice - (idx * PriceGrid) : FirstPrice + (idx * PriceGrid)), Precision);
            var coverPrice = _N((BuyFirst ? openPrice + PriceDiff : openPrice - PriceDiff), Precision);
            var state = fishTable[idx];
            var fishId = uuidTable[idx];
            if (hasOrder(orders, fishId)) {
                continue;
            }

            if (fishId != -1 && IsSupportGetOrder) {
                var order = trader.GetOrder(fishId);
                if (!order) {
                    Log("Failed to get order information, ID: ", fishId);
                    continue;
                }
                if (order.Status == ORDER_STATE_PENDING) {
                    //Log("Order status is not completed, ID: ", fishId);
                    continue;
                }
            }

            if (state == STATE_WAIT_COVER) {
                var coverId = CoverFunc(coverPrice, (BuyFirst ? amountS[idx] : amountB[idx]), (BuyFirst ? 'Buy order completed:' : 'Sell order completed:'), openPrice, 'Amount:', (BuyFirst ? amountB[idx] : amountS[idx]));
                if (coverId) {
                    fishTable[idx] = STATE_WAIT_CLOSE;
                    uuidTable[idx] = coverId;
                }
            } else if (state == STATE_WAIT_OPEN || state == STATE_WAIT_CLOSE) {
                var openId = OpenFunc(openPrice, BuyFirst ? amountB[idx] : amountS[idx]);
                if (openId) {
                    fishTable[idx] = STATE_WAIT_COVER;
                    uuidTable[idx] = openId;
                    if (state == STATE_WAIT_CLOSE) {
                        ProfitCount++;
                        var account = _C(exchange.GetAccount);
                        var ticker = _C(exchange.GetTicker);
                        var initNet = _N(((InitAccount.Stocks + InitAccount.FrozenStocks) * ticker.Buy) + InitAccount.Balance + InitAccount.FrozenBalance, 8);
                        var nowNet = _N(((account.Stocks + account.FrozenStocks) * ticker.Buy) + account.Balance + account.FrozenBalance, 8);
                        var actualProfit = _N(((nowNet - initNet)) * 100 / initNet, 8);
                        if (AmountType == 0) {
                            var profit = _N((ProfitCount * amount * PriceDiff) + LastProfit, 8);
                            Log((BuyFirst ? 'Sell order completed:' : 'Buy order completed:'), coverPrice, 'Amount:', (BuyFirst ? amountS[idx] : amountB[idx]), 'Closing Profit', profit);
                        } else {
                            Log((BuyFirst ? 'Sell order completed:' : 'Buy order completed:'), coverPrice, 'Amount:', (BuyFirst ? amountS[idx] : amountB[idx]));
                        }
                    }
                }
            }
        }
        Sleep(CheckInterval);
    }
    return true;
}

function main() {
    if (ResetData) {
        LogProfitReset();
        LogReset();
    }
    exchange.SetPrecision(Precision, XPrecision)
    if (typeof(AmountType) === 'undefined') {
        AmountType = 0;
    }
    if (typeof(AmountDot) === 'undefined') {
        AmountDot = 3;
    }
    if (typeof(EnableDynamic) === 'undefined') {
        EnableDynamic = false;
    }
    if (typeof(AmountCoefficient) === 'undefined') {
        AmountCoefficient = "*1";
    }
    if (typeof(EnableAccountCheck) === 'undefined') {
        EnableAccountCheck = true;
    }
    BuyFirst = (OpType == 0);
    IsSupportGetOrder = exchange.GetName().indexOf('itstamp') == -1;
    if (!IsSupportGetOrder) {
        Log(exchange.GetName(), "Not SupportedGetOrder, May affect strategy stability.");
    }

    SetErrorFilter("502:|503:|S_U_001|unexpected|network|timeout|WSARecv|Connect|GetAddr|no such|reset|http|received|refused|EOF|When");

    exchange.SetRate(1);
    Log('Exchange rate conversion has been disabled, Current currency is', exchange.GetBaseCurrency());

    if (!RestoreProfit) {
        LastProfit = 0;
    }

    var orgAccount = _C(exchange.GetAccount);
    var fishCount = 1;
    while (true) {
        if (!fishing(orgAccount, fishCount)) {
            break;
        }
        fishCount++;
        Log("No.", fishCount, "Recast net next time...");
        FirstPriceAuto = true;
        Sleep(1000);
    }
}
```

> Detail

https://www.fmz.com/strategy/629

> Last Modified

2020-02-04 16:33:00
