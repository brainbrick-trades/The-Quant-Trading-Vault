
> Name

Beginners-Guide-to-CoinEx-Trading-LTC-USDT

> Author

yuehen7

> Strategy Description

Newbie starting out, after researching for a few days, wrote a simple one......


QQ:185772115
We can communicate~

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|MinSpace|0.06|Minimum profit spread|
|MaxSpace|0.03|Pending order expiration distance|
|SlidePrice|0.01|Order sliding price|
|RetryDelay|500|Retry on failure|
|MinStock|0.001|Minimum transaction volume|
|OrderAmount|0.02|Fixed order quantity|
|Precision|2|Decimal precision|


> Source (javascript)

``` javascript
function GetAccount(e, waitFrozen) {
    if (typeof(waitFrozen) == 'undefined') {
        waitFrozen = false;
    }
    var account = null;
    var alreadyAlert = false;
    while (true) {
        account = _C(e.GetAccount);
        if (!waitFrozen || (account.FrozenStocks < MinStock && account.FrozenBalance < 0.01)) {
            break;
        }
        if (!alreadyAlert) {
            alreadyAlert = true;
            Log("Found frozen funds or coins in the account", account);
        }
        Sleep(RetryDelay);
    }
    return account;
}

function CancelPendingOrders(e, orderType) {
    while (true) {
        var orders = e.GetOrders();
        if (!orders) {
            Sleep(RetryDelay);
            continue;
        }
        var processed = 0;
        for (var j = 0; j < orders.length; j++) {
            if (typeof(orderType) == 'number' && orders[j].Type != orderType) {
                continue;
            }
            e.CancelOrder(orders[j].Id, orders[j]);
            processed++;
            if (j < (orders.length - 1)) {
                Sleep(RetryDelay);
            }
        }
        if (processed == 0) {
            break;
        }
    }
}

function StripOrders(e, tradeType, orderId) {
    var dealAmount = 0; //Return trading quantity,-1Represents all trades,0indicates no transaction, other values indicate partial transaction
    if (typeof(orderId) == 'undefined') {
        orderId = null;
    }
    var isBuy = tradeType == ORDER_TYPE_BUY;
    while (true) {
        logAccount();
        var order = null;
        var orders = _C(e.GetOrders); //Retrieve unfinished orders
        for (var i = 0; i < orders.length; i++) {
            if (orders[i].Id == orderId) {
                order = orders[i];
            }
        }
        if (orders.length == 0 || order == null) {
            dealAmount = -1;
            break;
        } else {
            var ticker = _C(e.GetTicker);
            var tradePrice = 0;
            if (isBuy) {
                tradePrice = _N(ticker.Buy + SlidePrice, Precision);
            } else {
                tradePrice = _N(ticker.Sell - SlidePrice, Precision);
            }
            var price = order.Price;
            if (Math.abs(tradePrice - price) > MaxSpace) { //Exceeds maximum pending order range
                var extra = "";
                if (order.DealAmount > 0) {
                    dealAmount = order.DealAmount;
                    extra = "Orderid:" + order.Id + ",Transaction: " + order.DealAmount;
                } else {
                    dealAmount = 0;
                    extra = "Orderid:" + order.Id + ",unfilled";
                }
                var flag = e.CancelOrder(order.Id, order.Type == ORDER_TYPE_BUY ? "buy-" : "sell-", extra, ' #C9C9C9');
                Log('Cancel order:', flag, ' #ff0000');
                if (flag) {
                    break;
                }
            }
        }
        Sleep(RetryDelay);
    }
    return dealAmount;
}

function Trade(e, tradeType, ordPrice, tradeAmount) {
    var ret = null;
    var nowAccount = GetAccount(e, true);
    var tradeFunc = tradeType == ORDER_TYPE_BUY ? e.Buy : e.Sell;
    var isBuy = tradeType == ORDER_TYPE_BUY;

    var doAmount = 0;
    if (isBuy) {
        doAmount = Math.min(tradeAmount, _N(nowAccount.Balance / ordPrice, 6));
    } else {
        doAmount = Math.min(tradeAmount, nowAccount.Stocks);
    }
    if (doAmount == MinStock) {} else if (doAmount < tradeAmount) {
        Log('Fixed Order Quantity:', tradeAmount, ',Currently Tradable:', doAmount, ' #9400D3');
        ret = {
            price: ordPrice,
            amount: -1
        };
        return ret;
    }
    logAccount();
    var orderId = tradeFunc(ordPrice, tradeAmount);
    if (!orderId) {
        CancelPendingOrders(e, tradeType);
        ret = {
            price: ordPrice,
            amount: 0
        };
    } else {
        var amount = StripOrders(e, tradeType, orderId); //-1Transaction,0Cancel All, Greater Than0Represents partially filled quantity
        if (amount < 0) {
            ret = {
                price: ordPrice,
                amount: tradeAmount
            };
        } else {
            ret = {
                price: ordPrice,
                amount: amount
            };
        }
    }
    logAccount();
    return ret;
}

var ini_blance = 0;
var ini_stocks = 0;
var ini_cet = 0;
var count = 0;
var usdt_Profit = 0.0;
var BuyInfo; //Buy order information
var SellCet = 0;

function OrderPrice(e) {
    var ticker = _C(e.GetTicker);
    var c = _N(ticker.Sell - ticker.Buy, 6);
    var buyPrice = 0;
    var sellPrice = 0;
    if (c > MinSpace) {
        buyPrice = _N(((ticker.Buy + ticker.Sell) / 2) - SlidePrice * 2, Precision);
        sellPrice = _N(((ticker.Buy + ticker.Sell) / 2) + SlidePrice * 2, Precision);
    } else if (c >= (2 * SlidePrice)) {
        buyPrice = _N(ticker.Buy + SlidePrice, Precision);
        sellPrice = _N(ticker.Sell - SlidePrice, Precision);
    } else {
        buyPrice = _N(ticker.Last, Precision);
        sellPrice = _N(ticker.Last, Precision);
    }

    if (BuyInfo != null && BuyInfo.amount > 0) {
        var space = Math.abs(BuyInfo.price - sellPrice)
        if (space > MaxSpace && space <= (MaxSpace * 1.5)) { //Sell price less than buy price-Pending order distance
            sellPrice = _N(BuyInfo.price - MaxSpace, Precision);
        } else if(space > (MaxSpace * 1.5)) {
            sellPrice = _N(BuyInfo.price - MaxSpace * 1.5, Precision);
        }
    }
    count = count + 1;
    Log('Counter:', count, 'Planned buy price:', buyPrice, ',Planned sell price:', sellPrice, ' #f47920');
    logAccount();
    return {
        buy: buyPrice,
        sell: sellPrice
    };
}

logAccount = function() {
    var ex1 = exchanges[0]; //Main Trading Account
    var ex2 = exchanges[1]; //Profit account

    var ticker = _C(ex1.GetTicker);
    var nowBlance = _C(ex1.GetAccount);
    var account2 = _C(ex2.GetAccount);
    var cet = account2.Stocks;

    var table = {
        type: 'table',
        title: 'Position information',
        cols: ['Current price', 'Initial CET', 'Initial USDT', 'Initial LTC', 'Current USDT', 'Current LTC', 'Freeze USDT', 'Freeze LTC', 'Current CET', 'USDT profit', 'Current CET profit', 'SellCET'],
        rows: [
            [ticker.Last, ini_cet, ini_blance, ini_stocks, nowBlance.Balance, nowBlance.Stocks, nowBlance.FrozenBalance, nowBlance.FrozenStocks, cet, _N(usdt_Profit, 6), _N(cet - ini_cet, 8), SellCet]
        ]
    };
    LogStatus('`' + JSON.stringify(table) + '`\n\nNewbie trying out, just for fun......');
}

function onTick(e) {
    var prices = OrderPrice(e);
    var buyPrice = prices.buy;
    var sellPrice = prices.sell;
    var sellInfo;

    if (BuyInfo == null) { //No buy order, place buy order first
        var buyInfo = Trade(e, ORDER_TYPE_BUY, buyPrice, OrderAmount);
        if (buyInfo != null && buyInfo.amount > 0) {
            BuyInfo = buyInfo;
        } else if (buyInfo.amount < 0) {
            Log('Insufficient balance to buy, automatically sell to balance...... #d71345');
            Trade(e, ORDER_TYPE_SELL, -1, MinStock);
        }
    }
    if (BuyInfo != null) {
        sellInfo = Trade(e, ORDER_TYPE_SELL, sellPrice, BuyInfo.amount);
    } else {
        sellInfo = Trade(e, ORDER_TYPE_SELL, sellPrice, OrderAmount);
    }

    if (BuyInfo != null && sellInfo != null && sellInfo.amount > 0) {
        var profit = _N(sellInfo.amount * (sellInfo.price - BuyInfo.price), 6);
        Log('Buy price is:', BuyInfo.price, 'Sell price is:', sellInfo.price, 'Profit:', profit, ' #d71345');
        usdt_Profit += profit;
        LogProfit(usdt_Profit);
        BuyInfo = null;
    } else if (BuyInfo != null && sellInfo.amount < 0) { //Only need to balance quantities when there are buy orders and insufficient sell quantities
        Log('Insufficient quantity to sell, automatically buy to balance...... #d71345');
        Trade(e, ORDER_TYPE_BUY, -1, MinStock);
    }
    logAccount();
}

function autoSellCet(e) {
    var account = _C(e.GetAccount);
    var cet = account.Stocks;
    var profit = _N(cet - ini_cet);
    if (profit > 1 && (profit % 3) == 0) {
        var orderId = e.Sell(-1, 1);
        if (!orderId) {
            CancelPendingOrders(e, ORDER_TYPE_SELL);
        }
        SellCet += 1;
        Log('Automatic sellCET:', 1, ' #FF00FF');
    }
}

function main() {
    LogReset();
    LogProfitReset();

    if (exchanges.length == 2) {
        var ex1 = exchanges[0]; //Main Trading Account
        var ex2 = exchanges[1]; //Profit account

        var iniAccount = _C(ex1.GetAccount);
        ini_blance = iniAccount.Balance;
        ini_stocks = iniAccount.Stocks;

        var account2 = _C(ex2.GetAccount);
        ini_cet = account2.Stocks;
        Log('Primary Trading Account:', ex1.GetCurrency(), ',Settlement unit:', ex1.GetQuoteCurrency(), ' #ff0000');
        Log('Sub-trading Account:', ex2.GetCurrency(), ',Settlement unit:', ex2.GetQuoteCurrency(), ' #ff0000');
        Log('Account initial balance:', ini_blance, ',Initial currency quantity:', ini_stocks, ',initialCETQuantity:', ini_cet, ' #ff0000');

        count = 0;
        while (true) {
            onTick(ex1, ex2);
            autoSellCet(ex2);
            Sleep(1000);
        }
    }
}
```

> Detail

https://www.fmz.com/strategy/103464

> Last Modified

2018-07-07 15:13:14
