
> Name

Binance-One-Time-Retrieval-of-All-Open-Orders-List-for-USDT-Margined-Contracts

> Author

夏天不打你





> Source (javascript)

``` javascript
// Get all pending orders
function getAllPendingOrders(num) {
    var ret = exchanges[num].IO("api", "GET", "/fapi/v1/openOrders");
    var pending_orders = [];

    if (!ret || ret.length <= 0) {
        return null;
    }

    for (var i = 0; i < ret.length; i++) {
        var type = "";
        if (ret[i].stopPrice == "0") {
            if (ret[i].positionSide == "LONG") {
                type = ret[i].side == "BUY" ? "Limit order to open long: Limit order to close long";
            } else if (ret[i].positionSide == "SHORT") {
                type = ret[i].side == "SELL" ? "Limit order to open short: Limit order to close short";
            } else {
                type = "Order Type Error";
            }
        } else {
            if (ret[i].origType == "TAKE_PROFIT_MARKET") {
                if (ret[i].closePosition) {
                    type = ret[i].positionSide == "LONG" ? "Take profit for long positions : Take profit for short positions";
                } else {
                    type = ret[i].positionSide == "LONG" ? "Long position take profit: Short position take profit";
                }
            } else if (ret[i].origType == "STOP_MARKET") {
                if (ret[i].closePosition) {
                    type = ret[i].positionSide == "LONG" ? "Stop loss for long positions : Stop loss for short positions";
                } else {
                    type = ret[i].positionSide == "LONG" ? "Long position stop loss: Short position stop loss";
                }
            } else {
                type = "Order Type Error";
            }
        }
        pending_orders.push({
            OrderId: ret[i].orderId,
            Symbol: ret[i].symbol.substring(0, ret[i].symbol.lastIndexOf("USDT")) + "_USDT",
            Price: Number(ret[i].price),
            Amount: Number(ret[i].origQty),
            DealAmount: Number(ret[i].executedQty),
            Type: type,
            StopPrice: Number(ret[i].stopPrice),
            Time: ret[i].time,
        });
    }

    return pending_orders;
}
```

> Detail

https://www.fmz.com/strategy/319429

> Last Modified

2021-09-27 10:27:08
