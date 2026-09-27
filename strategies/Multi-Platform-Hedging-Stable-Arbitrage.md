
> Name

Multi-Platform-Hedging-Stable-Arbitrage

> Author

John.

> Strategy Description

The program automatically converts the exchange rate and handling fee. When placing an order, refer to the price of buying one and selling one. Note that this is not a move, but a hedging! No need to manually transfer money or coins, one deposits money, one deposits coins, one buys, one sells, advanced hedging mode.
This hedging mode earns only the price difference regardless of whether the coin price goes up or down.
To open a position, you need to put money in one place and coins in the other. For example, the current price of BTC is 6,000, put 3,000 knives in one exchange, and put 0.45 in the other to get coins, or double them all.
MaxDiffrefers to the lowest platform price difference
SlidePriceRefers to the slippage price when placing an order; add this price for buy orders and subtract it for sell orders.
TickIntervalS Detection period
The lower limit value means that the currency will not operate if it falls to this price, and the upper limit value means that the currency will not operate if it is higher than this price, to prevent the platform from maliciously trapping robots..

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Interval|500|Error retry interval (milliseconds)|
|TickInterval|300|Detection frequency (milliseconds)|
|MaxDiff|3|Minimum Spread (Yuan))|
|SlidePrice|0.1|Stop loss sliding price (yuan)|
|SlideRatio|2|Hedging sliding price coefficient|
|StopPriceL|1000|Lower limit value (Yuan))|
|StopPriceH|9000|Upper limit value (Yuan))|
|optFeeTimeout|30|Commission update period (minutes))|
|AmountOnce|0.2|Single Trade Quantity|
|UseMarketOrder|false|Use market orders to stop loss|
|StopWhenLoss|false|Stop when losing|
|MaxLoss|50|Maximum loss limit (yuan)|
|SMSAPI|http://|SMS Notification Interface|


> Source (javascript)

``` javascript
var initState;
var isBalance = true;
var feeCache = new Array();
var feeTimeout = optFeeTimeout * 60000;
var lastProfit = 0;
var lastAvgPrice = 0;
var lastSpread = 0;
var lastOpAmount = 0;

function adjustFloat(v) {
    return Math.floor(v * 1000) / 1000;
}

function isPriceNormal(v) {
    return (v >= StopPriceL) && (v <= StopPriceH);
}

function stripTicker(t) {
    return 'Buy: ' + adjustFloat(t.Buy) + ' Sell: ' + adjustFloat(t.Sell);
}

function updateStatePrice(state) {
    var now = (new Date()).getTime();
    for (var i = 0; i < state.details.length; i++) {
        var ticker = null;
        var key = state.details[i].exchange.GetName() + state.details[i].exchange.GetCurrency();
        var fee = null;
        while (!(ticker = state.details[i].exchange.GetTicker())) {
            Sleep(Interval);
        }

        if (key in feeCache) {
            var v = feeCache[key];
            if ((now - v.time) > feeTimeout) {
                delete feeCache[key];
            } else {
                fee = v.fee;
            }
        }
        if (!fee) {
            while (!(fee = state.details[i].exchange.GetFee())) {
                Sleep(Interval);
            }
            feeCache[key] = {
                fee: fee,
                time: now
            };
        }
        // Buy-=fee Sell+=fee
        state.details[i].ticker = {
            Buy: ticker.Buy * (1 - (fee.Sell / 100)),
            Sell: ticker.Sell * (1 + (fee.Buy / 100))
        };
        state.details[i].realTicker = ticker;
        state.details[i].fee = fee;
    }
}

function getProfit(stateInit, stateNow, coinPrice) {
    var netNow = stateNow.allBalance + (stateNow.allStocks * coinPrice);
    var netInit = stateInit.allBalance + (stateInit.allStocks * coinPrice);
    return adjustFloat(netNow - netInit);
}

function getExchangesState() {
    var allStocks = 0;
    var allBalance = 0;
    var minStock = 0;
    var details = [];
    for (var i = 0; i < exchanges.length; i++) {
        var account = null;
        while (!(account = exchanges[i].GetAccount())) {
            Sleep(Interval);
        }
        allStocks += account.Stocks + account.FrozenStocks;
        allBalance += account.Balance + account.FrozenBalance;
        minStock = Math.max(minStock, exchanges[i].GetMinStock());
        details.push({
            exchange: exchanges[i],
            account: account
        });
    }
    return {
        allStocks: adjustFloat(allStocks),
        allBalance: adjustFloat(allBalance),
        minStock: minStock,
        details: details
    };
}

function cancelAllOrders() {
    for (var i = 0; i < exchanges.length; i++) {
        while (true) {
            var orders = null;
            while (!(orders = exchanges[i].GetOrders())) {
                Sleep(Interval);
            }

            if (orders.length == 0) {
                break;
            }

            for (var j = 0; j < orders.length; j++) {
                exchanges[i].CancelOrder(orders[j].Id, orders[j]);
            }
        }
    }
}

function balanceAccounts() {
    // already balance
    if (isBalance) {
        return;
    }

    cancelAllOrders();

    var state = getExchangesState();
    var diff = state.allStocks - initState.allStocks;
    var adjustDiff = adjustFloat(Math.abs(diff));
    if (adjustDiff < state.minStock) {
        isBalance = true;
    } else {
        Log('Initial Total Coins:', initState.allStocks, 'Current Total Coins: ', state.allStocks, 'Difference:', adjustDiff);
        // other ways, diff is 0.012, bug A only has 0.006 B only has 0.006, all less then minstock
        // we try to statistical orders count to recognition this situation
        updateStatePrice(state);
        var details = state.details;
        var ordersCount = 0;
        if (diff > 0) {
            var attr = 'Sell';
            if (UseMarketOrder) {
                attr = 'Buy';
            }
            // Sell adjustDiff, sort by price high to low
            details.sort(function(a, b) {
                return b.ticker[attr] - a.ticker[attr];
            });
            for (var i = 0; i < details.length && adjustDiff >= state.minStock; i++) {
                if (isPriceNormal(details[i].ticker[attr]) && (details[i].account.Stocks >= state.minStock)) {
                    var orderAmount = adjustFloat(Math.min(AmountOnce, adjustDiff, details[i].account.Stocks));
                    var orderPrice = details[i].realTicker[attr] - SlidePrice;
                    if ((orderPrice * orderAmount) < details[i].exchange.GetMinPrice()) {
                        continue;
                    }
                    ordersCount++;
                    if (details[i].exchange.Sell(orderPrice, orderAmount, stripTicker(details[i].ticker))) {
                        adjustDiff = adjustFloat(adjustDiff - orderAmount);
                    }
                    // only operate one platform
                    break;
                }
            }
        } else {
            var attr = 'Buy';
            if (UseMarketOrder) {
                attr = 'Sell';
            }
            // Buy adjustDiff, sort by sell-price low to high
            details.sort(function(a, b) {
                return a.ticker[attr] - b.ticker[attr];
            });
            for (var i = 0; i < details.length && adjustDiff >= state.minStock; i++) {
                if (isPriceNormal(details[i].ticker[attr])) {
                    var canRealBuy = adjustFloat(details[i].account.Balance / (details[i].ticker[attr] + SlidePrice));
                    var needRealBuy = Math.min(AmountOnce, adjustDiff, canRealBuy);
                    var orderAmount = adjustFloat(needRealBuy * (1 + (details[i].fee.Buy / 100)));
                    var orderPrice = details[i].realTicker[attr] + SlidePrice;
                    if ((orderAmount < details[i].exchange.GetMinStock()) ||
                        ((orderPrice * orderAmount) < details[i].exchange.GetMinPrice())) {
                        continue;
                    }
                    ordersCount++;
                    if (details[i].exchange.Buy(orderPrice, orderAmount, stripTicker(details[i].ticker))) {
                        adjustDiff = adjustFloat(adjustDiff - needRealBuy);
                    }
                    // only operate one platform
                    break;
                }
            }
        }
        isBalance = (ordersCount == 0);
    }

    if (isBalance) {
        var currentProfit = getProfit(initState, state, lastAvgPrice);
        LogProfit(currentProfit, "Spread: ", adjustFloat((currentProfit - lastProfit) / lastOpAmount), "Balance: ", adjustFloat(state.allBalance), "Stocks: ", adjustFloat(state.allStocks));

        if (StopWhenLoss && currentProfit < 0 && Math.abs(currentProfit) > MaxLoss) {
            Log('Trading loss exceeds the maximum limit, Exit after program cancels all orders.');
            cancelAllOrders();
            if (SMSAPI.length > 10 && SMSAPI.indexOf('http') == 0) {
                HttpQuery(SMSAPI);
                Log('SMS Already Notified');
            }
            throw 'stopped';
        }
        lastProfit = currentProfit;
    }
}

function onTick() {
    if (!isBalance) {
        balanceAccounts();
        return;
    }

    var state = getExchangesState();
    // We also need details of price
    updateStatePrice(state);

    var details = state.details;
    var maxPair = null;
    var minPair = null;
    for (var i = 0; i < details.length; i++) {
        var sellOrderPrice = details[i].account.Stocks * (details[i].realTicker.Buy - SlidePrice);
        if (((!maxPair) || (details[i].ticker.Buy > maxPair.ticker.Buy)) && (details[i].account.Stocks >= state.minStock) &&
            (sellOrderPrice > details[i].exchange.GetMinPrice())) {
            details[i].canSell = details[i].account.Stocks;
            maxPair = details[i];
        }

        var canBuy = adjustFloat(details[i].account.Balance / (details[i].realTicker.Sell + SlidePrice));
        var buyOrderPrice = canBuy * (details[i].realTicker.Sell + SlidePrice);
        if (((!minPair) || (details[i].ticker.Sell < minPair.ticker.Sell)) && (canBuy >= state.minStock) &&
            (buyOrderPrice > details[i].exchange.GetMinPrice())) {
            details[i].canBuy = canBuy;
            // how much coins we real got with fee
            details[i].realBuy = adjustFloat(details[i].account.Balance / (details[i].ticker.Sell + SlidePrice));
            minPair = details[i];
        }
    }

    if ((!maxPair) || (!minPair) || ((maxPair.ticker.Buy - minPair.ticker.Sell) < MaxDiff) ||
        !isPriceNormal(maxPair.ticker.Buy) || !isPriceNormal(minPair.ticker.Sell)) {
        return;
    }

    // filter invalid price
    if (minPair.realTicker.Sell <= minPair.realTicker.Buy || maxPair.realTicker.Sell <= maxPair.realTicker.Buy) {
        return;
    }

    // what a fuck...
    if (maxPair.exchange.GetName() == minPair.exchange.GetName()) {
        return;
    }

    lastAvgPrice = adjustFloat((minPair.realTicker.Buy + maxPair.realTicker.Buy) / 2);
    lastSpread = adjustFloat((maxPair.realTicker.Sell - minPair.realTicker.Buy) / 2);

    // compute amount
    var amount = Math.min(AmountOnce, maxPair.canSell, minPair.realBuy);
    lastOpAmount = amount;
    var hedgePrice = adjustFloat((maxPair.realTicker.Buy - minPair.realTicker.Sell) / Math.max(SlideRatio, 2))
    if (minPair.exchange.Buy(minPair.realTicker.Sell + hedgePrice, amount * (1 + (minPair.fee.Buy / 100)), stripTicker(minPair.realTicker))) {
        maxPair.exchange.Sell(maxPair.realTicker.Buy - hedgePrice, amount, stripTicker(maxPair.realTicker));
    }

    isBalance = false;
}

function main() {
    if (exchanges.length < 2) {
        throw "At least two exchanges are required to complete hedging";
    }

    TickInterval = Math.max(TickInterval, 50);
    Interval = Math.max(Interval, 50);

    cancelAllOrders();

    initState = getExchangesState();
    if (initState.allStocks == 0) {
        throw "The total amount of all currencies on all exchanges is zero; you must open a position on any exchange before completing the hedge.";
    }
    if (initState.allBalance == 0) {
        throw "The total CNY amount across all exchanges is zero, unable to proceed with hedging";
    }

    for (var i = 0; i < initState.details.length; i++) {
        var e = initState.details[i];
        Log(e.exchange.GetName(), e.exchange.GetCurrency(), e.account);
    }

    Log("ALL: Balance: ", initState.allBalance, "Stocks: ", initState.allStocks, "Ver:", Version());


    while (true) {
        onTick();
        Sleep(parseInt(TickInterval));
    }
}
```

> Detail

https://www.fmz.com/strategy/194150

> Last Modified

2020-04-15 14:13:49
