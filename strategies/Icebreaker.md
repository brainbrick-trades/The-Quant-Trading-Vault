
> Name

Icebreaker

> Author

Zero

> Strategy Description

Modified from Single-Point Sniping High-Frequency Position-Adding Automatic Reverse Position Unwinding Algorithm V1.2, but it does not reverse positions, can operate in a single direction, and includes a stop loss. The effect is very good, those who understand should take it and look at the source code. Not much more to say..

During backtesting, the capital is set to more than 100,000 and the currency is set to more than 30, so as to achieve the ideal effect. The larger the capital, the stronger the strategy's ability to resist fluctuations.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|OpType|0|Opening position direction: long|short|
|OpAmount|0.1|Open position quantity|
|OpMode|0|Position opening method: take order | pending order|
|MaxSpace|0.5|Pending order expiration distance|
|SlidePrice|0.1|Order Slippage Price (Yuan))|
|MaxAmount|0.3|Maximum single order volume for opening a position|
|AddGoal|true|Add position spacing (yuan))|
|AddLine|0.8|Additional position average price target (Yuan))|
|ProfitGoal|0.5|Close target (yuan))|
|Interval|true|Polling interval (seconds)|
|RestoreIt|false|Restore Progress|
|RestoreType|0|Position direction: long|short|
|RestorePrice|false|Average position price|
|RestoreAmount|false|Position Quantity|
|RestoreProfit|false|Last Profit|
|SaveLocal|false|Save local log|
|StopLoss|8|Stop Loss (Yuan)|
|MinStock|0.01|Minimum trading coin quantity|


> Source (javascript)

``` javascript
var TradeType = null;
var OrgAccount = null;
var Counter = {s : 0, f: 0, m: 0};
var LastProfit = 0;
var AllProfit = 0;
var LastTicker = null;
var maxHold = 0;

function _N(v, precision) {
    if (typeof(precision) != 'number') {
        precision = 4;
    }
    var d = parseFloat(v.toFixed(Math.max(10, precision+5)));
    s = d.toString().split(".");
    if (s.length < 2 || s[1].length <= precision) {
        return d;
    }

    var b = Math.pow(10, precision);
    return Math.floor(d*b)/b;
}

function EnsureCall(e, method) {
    var r;
    while (!(r = e[method].apply(this, Array.prototype.slice.call(arguments).slice(2)))) {
        Sleep(Interval);
    }
    return r;
}

function StripOrders(e, orderId) {
    var order = null;
    if (typeof(orderId) == 'undefined') {
        orderId = null;
    }
    while (true) {
        var dropped = 0;
        var orders = EnsureCall(e, 'GetOrders');
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

function updateProfit(e, account, ticker) {
    if (typeof(account) == 'undefined') {
        account = GetAccount(e);
    }
    if (typeof(ticker) == 'undefined') {
        ticker = EnsureCall(e, "GetTicker");
    }
    var profit = _N(LastProfit + (((account.Stocks + account.FrozenStocks) - (OrgAccount.Stocks + OrgAccount.FrozenStocks)) * ticker.Last) + ((account.Balance + account.FrozenBalance) - (OrgAccount.Balance + OrgAccount.FrozenBalance)), 4);
    LogProfit(profit, "Number of coins: ", _N(account.Stocks + account.FrozenStocks, 4), "Number of money:", _N(account.Balance + account.FrozenBalance, 4));
    return profit;
}


var preMsg = "";
function GetAccount(e, waitFrozen) {
    if (typeof(waitFrozen) == 'undefined') {
        waitFrozen = false;
    }
    var account = null;
    var alreadyAlert = false;
    while (true) {
        account = EnsureCall(e, "GetAccount");
        if (!waitFrozen || (account.FrozenStocks < MinStock && account.FrozenBalance < 0.01)) {
            break;
        }
        if (!alreadyAlert) {
            alreadyAlert = true;
            Log("Found frozen funds or coins in the account", account);
        }
        Sleep(Interval);
    }
    // TODO Hack
    msg = "Success: " + Counter.s + " times, Untangle: " + Counter.f + " times, stop loss: " + Counter.m + " times, Maximum position: " + _N(maxHold);
    //msg = Counter.s + " / " + Counter.f + " / " + Counter.m;

    if (LastTicker != null && OrgAccount != null) {
        var profit = (((account.Stocks + account.FrozenStocks) - (OrgAccount.Stocks + OrgAccount.FrozenStocks)) * LastTicker.Last) + ((account.Balance + account.FrozenBalance) - (OrgAccount.Balance + OrgAccount.FrozenBalance));
        msg += "\nProfit and Loss: " + AllProfit + ", Float: " + _N(profit, 4);
        msg += "\nInitial account money: " + OrgAccount.Balance + " Currency: " + OrgAccount.Stocks + ", Current account money: " + _N(account.Balance + account.FrozenBalance) + " Currency: " + _N(account.Stocks + account.FrozenStocks);
    }

    if (msg != preMsg) {
        preMsg = msg;
        LogStatus(msg, "#ff0000");
    }
    return account;
}

// mode = 0 : direct buy, 1 : buy as buy1
function Trade(e, tradeType, tradeAmount, mode, slidePrice, maxAmount, maxSpace, retryDelay) {
    var initAccount = GetAccount(e, true);
    var nowAccount = initAccount;
    var orderId = null;
    var prePrice = 0;
    var dealAmount = 0;
    var diffMoney = 0;
    var isFirst = true;
    var tradeFunc = tradeType == ORDER_TYPE_BUY ? e.Buy : e.Sell;
    var isBuy = tradeType == ORDER_TYPE_BUY;
    while (true) {
        var ticker = EnsureCall(e, 'GetTicker');
        LastTicker = ticker;
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
                nowAccount = GetAccount(e, true);
            }
            var doAmount = 0;
            if (isBuy) {
                diffMoney = _N(initAccount.Balance - nowAccount.Balance, 4);
                dealAmount = _N(nowAccount.Stocks - initAccount.Stocks, 4);
                doAmount = Math.min(maxAmount, tradeAmount - dealAmount, _N((nowAccount.Balance-10) / tradePrice, 4));
            } else {
                diffMoney = _N(nowAccount.Balance - initAccount.Balance, 4);
                dealAmount = _N(initAccount.Stocks - nowAccount.Stocks, 4);
                doAmount = Math.min(maxAmount, tradeAmount - dealAmount, nowAccount.Stocks);
            }
            if (doAmount < MinStock) {
                break;
            }
            prePrice = tradePrice;
            orderId = tradeFunc(tradePrice, doAmount);
        } else {
            if (Math.abs(tradePrice - prePrice) > maxSpace) {
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

    return {price: _N(diffMoney / dealAmount, 4), amount: dealAmount};
}

function loop(isFirst) {
    var minStock = MinStock;
    var initAccount = GetAccount(exchange, true);
    Log(initAccount);
    var holdPrice = 0;
    var holdAmount = 0;
    if (RestoreIt && isFirst) {
        LastProfit = RestoreProfit;
        TradeType = RestoreType == 0 ? ORDER_TYPE_BUY : ORDER_TYPE_SELL;
        holdPrice = RestorePrice;
        holdAmount = RestoreAmount;
        if (holdAmount != 0) {
            initAccount = {
                Stocks: initAccount.Stocks,
                FrozenStocks: initAccount.FrozenStocks,
                Balance: initAccount.Balance,
                FrozenBalance: initAccount.FrozenBalance,
            };
            if (RestoreType == 0) {
                initAccount.Stocks -= holdAmount;
                initAccount.Balance += (holdPrice * holdAmount);
            } else {
                initAccount.Stocks += holdAmount;
                initAccount.Balance -= (holdPrice * holdAmount);
            }
            OrgAccount = initAccount;
            Log("Restore the position status to:", RestoreType == 0 ? "go long" : "go short", "Average Price:", holdPrice, "Quantity:", holdAmount);
            if (RestoreType == 0) {
                holdAmount = Math.min(initAccount.Stocks, holdAmount);
            }
        }
        if (LastProfit != 0) {
            LogProfit(LastProfit, "Restore last profit");
        }
    }
    if (holdAmount == 0) {
        var obj = Trade(exchange, TradeType, OpAmount, OpMode, SlidePrice, MaxAmount, MaxSpace, Interval);
        if (!obj) {
            throw "Unsuccessful start, opening position failed";
        } else {
            Log(TradeType == ORDER_TYPE_BUY ? "Long Position Opened" : "Short Position Opened", "Average Price:", obj.price, "Quantity:", obj.amount);
        }
        Log(GetAccount(exchange, true));
        holdPrice = obj.price;
        holdAmount = obj.amount;
    }
    var openFunc = TradeType == ORDER_TYPE_BUY ? exchange.Buy : exchange.Sell;
    var coverFunc = TradeType == ORDER_TYPE_BUY ? exchange.Sell : exchange.Buy;
    var isFinished = false;
    while (!isFinished) {
        var account = GetAccount(exchange, true);
        var openAmount = 0;
        var openPrice = 0;
        var coverPrice = 0;
        var canOpen = true;

        if (TradeType == ORDER_TYPE_BUY) {
            var upLine = AddLine;
            openPrice = _N(holdPrice - AddGoal, 4);
            openAmount = _N((holdAmount * (holdPrice - openPrice - upLine)) / upLine, 4);
            coverPrice = _N(holdPrice + ProfitGoal, 4);
            if (_N(account.Balance / openPrice, 4) < openAmount) {
                Log("No money to add long position, Need to Add Position: ", openAmount, "Individual/Unit");
                canOpen = false;
            }
        } else {
            var upLine = -AddLine;
            openPrice = _N(holdPrice + AddGoal, 4);
            coverPrice = _N(holdPrice - ProfitGoal, 4);
            openAmount = _N((holdAmount * (holdPrice - openPrice - upLine) / upLine), 4);
            if (account.Stocks < openAmount) {
                Log("No coins to add short position, Required coins:", openAmount);
                canOpen = false;
            }
        }
        if (holdAmount < minStock) {
            Log("Remaining coin amount is too small, Abandon Operation", holdAmount);
            return 0;
        }
        openAmount = Math.max(minStock, openAmount);

        var order_count = 0;
        var openId = null;
        var coverId = null;
        if (!canOpen) {
            openId = -1;
            Log("Enter wait for unlocking mode");
        }

        for (var i = 0; i < 10; i++) {
            if (!openId) {
                openId = openFunc(openPrice, openAmount);
            }
            if (!coverId) {
                coverId = coverFunc(coverPrice, holdAmount);
            }
            if (openId && coverId) {
                break;
            }
            Sleep(Interval);
        }
        if (!openId || !coverId) {
            StripOrders(exchange);
            throw "Order failed";
        }
        if (openId > 0) {
            order_count++;
        }
        if (coverId > 0) {
            order_count++;
        }

        var preAccount = account;
        var loss = null;
        while (true) {
            Sleep(Interval);
            var ticker = EnsureCall(exchange, "GetTicker");
            LastTicker = ticker;
            var floatProfit = Math.abs(ticker.Last - coverPrice) * holdAmount;
            var balance = false;
            if (loss === null) {
                loss = floatProfit;
            } else if (floatProfit - loss > StopLoss) {
                Log("Current floating profit and loss:", floatProfit, "Start stop-loss");
                StripOrders(exchange);
                balance = true;
            }
            var orders = EnsureCall(exchange, "GetOrders");
            var nowAccount = GetAccount(exchange);
            var diff = nowAccount.Stocks + nowAccount.FrozenStocks - preAccount.Stocks;
            if (balance) {
                diff = nowAccount.Stocks + nowAccount.FrozenStocks - OrgAccount.Stocks;
                if (Math.abs(diff) > minStock) {
                    var obj = Trade(exchange, diff > 0 ? ORDER_TYPE_SELL : ORDER_TYPE_BUY, Math.abs(diff), 0, SlidePrice, MaxAmount, MaxSpace, Interval);
                    if (!obj) {
                        throw "Stop Loss Failed";
                    } else {
                        Log(TradeType == ORDER_TYPE_BUY ? "Close short position completed" : "Close long position completed", "Average Price:", obj.price, "Quantity:", obj.amount);
                    }
                }
                nowAccount = GetAccount(exchange);
                AllProfit = updateProfit(exchange, GetAccount(exchange), ticker);
                initAccount = nowAccount;
                isFinished = true;
                Counter.m++;
                break;
            }

            if (orders.length != order_count || Math.abs(diff) >= minStock) {
                StripOrders(exchange);
                nowAccount = GetAccount(exchange, true);
                //Log(nowAccount);
                var diffAmount = nowAccount.Stocks - initAccount.Stocks;
                var diffMoney = nowAccount.Balance - initAccount.Balance;
                if (Math.abs(diffAmount) < minStock) {
                    AllProfit = updateProfit(exchange, nowAccount, ticker);
                    Log("Closing Completed, reached target profit point, Single Profit", _N(holdAmount * ProfitGoal, 4));
                    initAccount = nowAccount;
                    isFinished = true;
                    if (!canOpen) {
                        Counter.f++;
                    }
                    break;
                }
                var newHoldPrice = 0;
                var newHoldAmount = 0;
                if (TradeType == ORDER_TYPE_BUY) {
                    newHoldAmount = _N(diffAmount, 4);
                    newHoldPrice = _N((-diffMoney) / diffAmount, 4);
                } else {
                    newHoldAmount = _N(-diffAmount, 4);
                    newHoldPrice = _N(diffMoney / (-diffAmount), 4);
                }
                // if open again, we need adjust hold positions's price
                var isAdd = false;
                if (newHoldAmount > holdAmount) {
                    holdPrice = newHoldPrice;
                    isAdd = true;
                }
                holdAmount = newHoldAmount;
                maxHold = Math.max(holdAmount, maxHold);
                if (!isAdd) {
                    // reset initAccount
                    initAccount = {
                        Stocks : nowAccount.Stocks,
                        Balance : nowAccount.Balance,
                        FrozenBalance : nowAccount.FrozenBalance,
                        FrozenStocks : nowAccount.FrozenStocks,
                    };
                    if (TradeType == ORDER_TYPE_BUY) {
                        initAccount.Stocks -= holdAmount;
                        initAccount.Balance += holdAmount * holdPrice;
                    } else {
                        initAccount.Stocks += holdAmount;
                        initAccount.Balance -= holdAmount * holdPrice;
                    }
                    initAccount.Stocks = _N(initAccount.Stocks, 4);
                    initAccount.Balance = _N(initAccount.Balance, 4);
                    Log("Adjust account before holding positions: ", initAccount);
                }
                Log((TradeType == ORDER_TYPE_BUY ? "Long position" : "Short position"), (isAdd ? "After adding position" : "After closing a position"), "Adjust position again, Average Price: ", holdPrice, "Quantity", holdAmount);
                Log("Buy one:", ticker.Buy, "Sell one:", ticker.Sell, "Last transaction price:", ticker.Last);
                Log(nowAccount);
                break;
            }
        }
    }
    return 0;
}

function onexit() {
    StripOrders(exchange);
    Log("Exit");
}

function main() {
    if (AddLine > AddGoal || AddLine <= 0) {
        throw "Error in average price target when adding positions";
    }
    if (exchange.GetName().indexOf("Future") != -1) {
        throw "Only supports spot, futures are prone to liquidation, not supported for now";
    }
    if (exchange.GetRate() != 1) {
        Log("Currency conversion disabled");
        exchange.SetRate(1);
    }
    TradeType = OpType == 0 ? ORDER_TYPE_BUY : ORDER_TYPE_SELL;
    EnableLogLocal(SaveLocal);
    Interval *= 1000;
    SetErrorFilter("502:|503:|unexpected|network|timeout|WSARecv|Connect|GetAddr|no such|reset|http|received|EOF");
    StripOrders(exchange);
    OrgAccount = GetAccount(exchange);
    var isFirst = true;
    LogStatus("Startup Successful", TradeType);
    while (true) {
        var ret = loop(isFirst);
        isFirst = false;
        Counter.s++;
        Sleep(Interval);
    }
}
```

> Detail

https://www.fmz.com/strategy/9929

> Last Modified

2018-06-05 16:35:53
