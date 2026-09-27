
> Name

Ladder-Order-Trigger-Price-Can-Be-Set

> Author

Zero

> Strategy Description

Ladder orders can be bought or sold. The program places a specified number of buy orders or sell orders according to the order interval. If it is a buy order, the first order will be the highest priced order, and the prices of subsequent orders will decrease in sequence. The first sell order will be the cheapest sell order, and the prices of subsequent orders will increase in sequence.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|OpType|0|Place a buy order: Buy|Sell|
|StartPrice|20|Initial order price|
|PriceDiff|0.2|Order Interval|
|OrderNum|10|Number of Orders|
|Amount|0.8|Number of coins per order|
|EnableTrigger|false|Use trigger conditions|
|TriggerPrice|18|Trigger price|


> Source (javascript)

``` javascript
function adjustFloat(v) {
    return Math.floor(parseFloat(v.toFixed(10))*1000)/1000;
}

function GetAccount(e) {
    var account;
    while (!(account = exchange.GetAccount())) {
        Sleep(Interval);
    }
    return account;
}

function GetTicker() {
    var ticker;
    while (!(ticker = exchange.GetTicker())) {
        Sleep(1000);
    }
    return ticker;
}

function main() {
    var ticker = GetTicker();
    var InitPrice = ticker.Last;
    if (EnableTrigger) {
        Log('Current Price: ', InitPrice, InitPrice > TriggerPrice ? 'Price drops below' : 'Price rises above', TriggerPrice, 'triggers ladder order placement');
        while (true) {
            if (InitPrice > TriggerPrice && ticker.Last < TriggerPrice) {
                Log('Current Price', ticker.Last, 'Price drops below ', TriggerPrice, 'element, Start ordering');
                break;
            } else if (InitPrice < TriggerPrice && ticker.Last > TriggerPrice) {
                Log('Current Price', ticker.Last, 'Price rises above ', TriggerPrice, 'element, Start ordering');
                break;
            }
            ticker = GetTicker();
            Sleep(1000);
        }
    }
    var account = GetAccount();
    var needMoney = 0;
    var needStocks = 0;
    for (var i = 0; i < OrderNum; i++) {
        needMoney += (StartPrice - (i * PriceDiff)) * Amount;
        needStocks += Amount;
    }

    if (OpType == 0) {
        if (needMoney > account.Balance) {
            throw "Not enough money to place an order";
        }
        for (var i = 0; i < OrderNum; i++) {
            exchange.Buy(adjustFloat(StartPrice - (i * PriceDiff)), Amount);
        }
    } else {
        if (needStocks > account.Stocks) {
            throw "Not enough coins to place an order";
        }
        for (var i = 0; i < OrderNum; i++) {
            exchange.Sell(adjustFloat(StartPrice + (i * PriceDiff)), Amount);
        }        
    }
    Log("All orders completed");
}
```

> Detail

https://www.fmz.com/strategy/639

> Last Modified

2015-04-22 16:18:14
