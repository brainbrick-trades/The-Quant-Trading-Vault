
> Name

Grid-Deformation-Strategy-Unilateral-Grid-OK-Futures

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
|ContractTypeIdx|0|contract types: this week | next week | quarter|
|OpType|0|Grid direction: Buy first, then sell | Sell first, then buy|
|FirstPriceAuto|false|First price automatically|
|FirstPrice|100|First price|
|AllNum|10|Total quantity|
|PriceGrid|true|Price interval|
|PriceDiff|2|Price difference (yuan)|
|AmountType|0|Order size: Same buy and sell volume | Custom quantity|
|AmountOnce|true|Single transaction quantity|
|BAmountOnce|true|Buy order size|
|SAmountOnce|true|Sell order size|
|MarginLevelIdx|0|Leverage Size: 10|20|
|EnableProtectDiff|false|Enable spread protection|
|ProtectDiff|20|Entry-point spread protection|
|CancelAllWS|true|Cancel orders when stopping|
|CheckInterval|2000|Polling Interval|
|Interval|1300|Failed retry interval|
|RestoreProfit|false|Restore last profit|
|LastProfit|false|Last Profit|
|ProfitAsOrg|false|Last profit included in average price|
|EnableStopLoss|false|Enable stop loss|
|StopLoss|0.1|Maximum floating loss|
|StopLossMode|0|Action after stop loss: recover and exit | recover and redeploy|
|AutoMove|false|Automatic movement|
|MaxDistance|20|Maximum distance (yuan).)|
|MaxIdle|7200|Maximum idle (seconds).)|




|Button|Default|Description|
|----|----|----|
|Close network|__button__|stop and balance back to initial state|


> Source (javascript)

``` javascript
var isFuture = false;

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


function balanceAccount(orgAccount, initAccount) {
    if (isFuture) {
        while (true) {
            cancelPending();
            var positions = _C(exchange.GetPosition);
            if (positions.length === 0 ) {
                var accountNow = _C(exchange.GetAccount);
                LogProfit(_N(accountNow.Stocks - orgAccount.Stocks), "Available Margin:", accountNow.Stocks);
                return;
            }
            for (var i = 0; i < positions.length; i++) {
                if (positions[i].Type == PD_LONG) {
                    exchange.SetDirection("closebuy");
                    exchange.Sell(positions[i].Amount);
                } else {
                    exchange.SetDirection("closesell");
                    exchange.Buy(positions[i].Amount);
                }
            }
            Sleep(Interval);
        }
    }
    var account = _C(exchange.GetAccount);
    while (true) {
        var diff = _N(account.Stocks - initAccount.Stocks);
        if (Math.abs(diff) < exchange.GetMinStock()) {
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
        Log("Start balancing", (diff > 0 ? "sell" : "buy"), Math.abs(diff), "Currency");
        if (diff > 0) {
            exchange.Sell(price - 0.2, diff);
        } else {
            exchange.Buy(price + 0.2, -diff);
        }
        Sleep(1000);
        cancelPending();
        account = _C(exchange.GetAccount);
    }
    Log("Balance completed", account);
}

var STATE_WAIT_OPEN  = 0;
var STATE_WAIT_COVER = 1;
var STATE_WAIT_CLOSE = 2;
var ProfitCount = 0;
var BuyFirst = (OpType == 0);
var IsSupportGetOrder = true;
var LastBusy = 0;
var LastFloatProfit = 0;

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
    var amountB = amount;
    var amountS = amount;
    if (typeof(AmountType) !== 'undefined' && AmountType == 1) {
        amountB = BAmountOnce;
        amountS = SAmountOnce;
    }
    if (FirstPriceAuto) {
        FirstPrice = BuyFirst ? _N(ticker.Buy - PriceGrid) : _N(ticker.Sell + PriceGrid);
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
    var marginLevel = [10,20][MarginLevelIdx];
    exchange.SetMarginLevel(marginLevel);
    for (var idx = 0; idx < AllNum; idx++) {
        var price = _N(BuyFirst ? FirstPrice - (idx * PriceGrid) : FirstPrice + (idx * PriceGrid));
        if (isFuture) {
            needStocks += ((100 * amountB) / price) / marginLevel;
            if (_N(needStocks) <= _N(account.Stocks)) {
                actualNeedStocks = needStocks;
                canNum++;
            } else {
                notEnough = true;
            }
        } else {
            needStocks += amountS;
            needMoney += price * amountB;
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
        }
        fishTable[idx] = STATE_WAIT_OPEN;
        uuidTable[idx] = -1;
    }
    if (EnableProtectDiff) {
        if (BuyFirst && (FirstPrice - ticker.Sell) > ProtectDiff) {
            throw "First buy price compared to market sell1high price" + _N(FirstPrice - ticker.Sell) + ' element';
        } else if (!BuyFirst && (ticker.Buy - FirstPrice) > ProtectDiff) {
            throw "First sell price compared to market buy1high price " + _N(ticker.Buy - FirstPrice) + ' element';
        }
    }
    if (BuyFirst && !isFuture) {
        if (account.Balance < _N(needMoney)) {
            if (fishCount == 1) {
                throw "Insufficient funds, Need"+ _N(needMoney) + "element";
            } else {
                Log("Insufficient funds, Need", _N(needMoney), "element, Program only does", canNum, "Number of grids #ff0000");
            }
        } else {
            Log('Expected funds to be used: ', _N(needMoney), "element");
        }
    } else {
        if (account.Stocks < _N(needStocks)) {
            if (fishCount == 1) {
                throw "Insufficient coins, Need "+ _N(needStocks) + " Currency";
            } else {
                Log("Insufficient funds, Need", _N(needStocks), "Currency, Program only does", canNum, "Number of grids #ff0000");
            }
        } else {
            Log('Estimated amount of coins to be used: ', _N(needStocks), "Individual/Unit");
        }
    }

    var OpenFunc = BuyFirst ? exchange.Buy : exchange.Sell;
    var CoverFunc = BuyFirst ? exchange.Sell : exchange.Buy;
    var ts = new Date();
    var preMsg = "";
    var profitMax = 0;
    while (true) {
        var now = new Date();
        if (now.getTime() - ts.getTime() > 5000) {
            if (typeof(GetCommand) == 'function' && GetCommand() == "close the net") {
                Log("Start executing commands to close network operations");
                balanceAccount(orgAccount, InitAccount);
                return false;
            }
            ts = now;
            var msg = "";
            var positions, isHold;
            var ticker = _C(exchange.GetTicker);
            var nowAccount = _C(exchange.GetAccount);
            if (isFuture) {
                positions = _C(exchange.GetPosition);
                isHold = positions.length > 0;
                if (isHold) {
                    msg += "Open Position: " + positions[0].Amount + " Average position price: " + _N(positions[0].Price) + " Floating profit and loss: " + _N(positions[0].Profit);
                    if (EnableStopLoss && -positions[0].Profit >= StopLoss) {
                        Log("Current floating profit and loss", positions[0].Profit, "Start stop-loss");
                        balanceAccount(orgAccount, InitAccount);
                        if (StopLossMode === 0) {
                            throw "Stop loss exit";
                        } else {
                            return true;
                        }
                    }
                } else {
                    msg += "Short position";
                }
                msg += " Available Margin: " + nowAccount.Stocks;
                
            } else {
                isHold = Math.abs(amount_diff) >= exchange.GetMinStock();
                
                var amount_diff = (nowAccount.Stocks + nowAccount.FrozenStocks) - (InitAccount.Stocks + InitAccount.FrozenStocks);
                var money_diff = (nowAccount.Balance + nowAccount.FrozenBalance) - (InitAccount.Balance + InitAccount.FrozenBalance);
                var floatProfit = _N(money_diff + (amount_diff * ticker.Last));
                var floatProfitAll = _N((nowAccount.Balance + nowAccount.FrozenBalance - orgAccount.Balance - orgAccount.FrozenBalance) + ((nowAccount.Stocks + nowAccount.FrozenStocks - orgAccount.Stocks - orgAccount.FrozenStocks) * ticker.Last));
                LastFloatProfit = floatProfitAll;
                profitMax = Math.max(floatProfit, profitMax);
                if (EnableStopLoss) {
                    if ((profitMax - floatProfit) >= StopLoss) {
                        Log("Current floating profit and loss", floatProfit, "Highest profit point: ", profitMax, "Start stop-loss");
                        balanceAccount(orgAccount, InitAccount);
                        if (StopLossMode === 0) {
                            throw "Stop loss exit";
                        } else {
                            return true;
                        }
                    }
                }
                if (isHold) {
                    if (RestoreProfit && ProfitAsOrg) {
                        if (BuyFirst) {
                            money_diff += LastProfit;
                        } else {
                            money_diff -= LastProfit;
                        }
                    }
                    var hold_amount = amount_diff;
                    var hold_price = (-money_diff) / amount_diff;
                    if (!BuyFirst) {
                        hold_amount = -amount_diff;
                        hold_price = (money_diff) / -amount_diff;
                    }
                    msg = (BuyFirst ? "go long: " : "go short: ") +  _N(hold_amount, 4) + " Currency, Average Price: " + _N(hold_price);
                } else {
                    msg += "Short position";
                }
                msg += " Current grid floating profit and loss: " + floatProfit + " Total floating profit and loss: " + floatProfitAll + " No. " + fishCount + " Next net cast, latest coin price: " + _N(ticker.Last);
            }
            if (isHold) {
                setBusy();
            }

            var distance = 0;
            if (AutoMove) {
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
                    Log("Prices exceed the grid range by too much, Start moving the mesh, Current distance: ", _N(distance), "Current Price:", ticker.Last);
                    refish = true;
                }
                if (refish) {
                    balanceAccount(orgAccount, InitAccount);
                    return true;
                }
            }

            if (AutoMove && distance > 0) {
                msg += " (From the grid" + (BuyFirst ? "upward" : "downward") + "deviation: " + _N(distance) + " element)";
            }
            if (msg != preMsg) {
                LogStatus(msg);
                preMsg = msg;
            }

        }
        var orders = _C(exchange.GetOrders);
        for (var idx = 0; idx < canNum; idx++) {
            var openPrice = _N(BuyFirst ? FirstPrice - (idx * PriceGrid) : FirstPrice + (idx * PriceGrid));
            var coverPrice = _N(BuyFirst ? openPrice + PriceDiff : openPrice - PriceDiff);
            var state = fishTable[idx];
            var fishId = uuidTable[idx];
            if (hasOrder(orders, fishId)) {
                continue;
            }

            if (fishId != -1 && IsSupportGetOrder) {
                var order = exchange.GetOrder(fishId);
                if (!order) {
                    Log("Failed to get order information, ID: ", fishId);
                    continue;
                }
                if (order.Status == ORDER_STATE_PENDING) {
                    Log("Order status is not completed, ID: ", fishId);
                    continue;
                }
            }

            if (state == STATE_WAIT_COVER) {
                if (isFuture) {
                    exchange.SetDirection(BuyFirst ? "closebuy" : "closesell");
                }
                var coverId = CoverFunc(coverPrice, BuyFirst ? amountS : amountB, BuyFirst ? 'Buy order completed:' : 'Sell order completed:', openPrice);
                if (coverId) {
                    fishTable[idx] = STATE_WAIT_CLOSE;
                    uuidTable[idx] = coverId;
                }
            } else if (state == STATE_WAIT_OPEN || state == STATE_WAIT_CLOSE) {
                if (isFuture) {
                    exchange.SetDirection(BuyFirst ? "buy" : "sell");
                }
                var openId = OpenFunc(openPrice, BuyFirst ? amountB : amountS);
                if (openId) {
                    fishTable[idx] = STATE_WAIT_COVER;
                    uuidTable[idx] = openId;
                    if (state == STATE_WAIT_CLOSE) {
                        ProfitCount++;
                        if (AmountType === 0) {
                            Log((BuyFirst ? 'Sell order completed: ' : 'Buy order completed: ') + coverPrice);
                        } else {
                            Log((BuyFirst ? 'Sell order completed: ' : 'Buy order completed: ') + coverPrice);
                        }
                        if (!isFuture) {
                            var account = _C(exchange.GetAccount);
                            var ticker = _C(exchange.GetTicker);
                            var initNet = _N(((InitAccount.Stocks + InitAccount.FrozenStocks) * ticker.Buy) + InitAccount.Balance + InitAccount.FrozenBalance, 8);
                            var nowNet = _N(((account.Stocks + account.FrozenStocks) * ticker.Buy) + account.Balance + account.FrozenBalance, 8);
                            var actualProfit = _N(((nowNet - initNet)) * 100 / initNet, 8);
                            LogProfit(LastFloatProfit, "Total floating profit and loss ratio:", _N(LastFloatProfit * 100 / actualNeedMondy, 4), '%');
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
    if (typeof(AmountType) === 'undefined') {
        AmountType = 0;
    }
    IsSupportGetOrder = exchange.GetName().indexOf('itstamp') == -1;
    if (!IsSupportGetOrder) {
        Log(exchange.GetName(), "Not SupportedGetOrder, May affect strategy stability.");
    }
    
    isFuture = exchange.GetName().indexOf("Future") != -1;
    if (AmountType === 0) {
        BAmountOnce = AmountOnce;
        SAmountOnce = AmountOnce;
    }
    if (exchange.GetName() == "Futures_OKCoin" && (AmountOnce.toString().indexOf(".") != -1 || BAmountOnce.toString().indexOf(".") != -1 || SAmountOnce.toString().indexOf(".") != -1)) {
        throw "OKCoinThe number of futures orders placed must be integers";
    }

    SetErrorFilter("502:|503:|unexpected|network|timeout|WSARecv|Connect|GetAddr|no such|reset|http|received|refused|EOF|When");

    exchange.SetRate(1);
    Log('Exchange rate conversion has been disabled, Current currency is', exchange.GetBaseCurrency());

    if (!RestoreProfit) {
        LastProfit = 0;
    }
    exchange.SetContractType(["this_week", "next_week", "quarter"][ContractTypeIdx]);
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

https://www.fmz.com/strategy/8474

> Last Modified

2020-04-06 18:47:43
