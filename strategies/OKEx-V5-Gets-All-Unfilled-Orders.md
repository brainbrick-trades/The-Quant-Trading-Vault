
> Name

OKEx-V5-Gets-All-Unfilled-Orders

> Author

夏天不打你





> Source (javascript)

``` javascript


function getAllPendingOrdersInOkex(num) {
    var pending_orders = [];

    // Limit order
    var param = "instType=SWAP";
    var ret = exchanges[num].IO("api", "GET", "/api/v5/trade/orders-pending", param);
    // take profit and stop loss order
    param = "instType=SWAP" + "&ordType=oco,conditional";
    var ret2 = exchanges[num].IO("api", "GET", "/api/v5/trade/orders-algo-pending", param);

    if (!ret) {
        Log(exchanges[num].GetLabel(), ":Failed to get limit order!", "@");
        return null;
    }
    if (!ret2) {
        Log(exchanges[num].GetLabel(), ":Failed to fetch take-profit/stop-loss order!", "@");
        return null;
    }

    for (let i = 0; i < ret.data.length; i++) {
        let type = "";
        if (ret.data[i].posSide == "long") {
            type = ret.data[i].side == "buy" ? "Limit order to open long: Limit order to close long";
        } else if (ret.data[i].posSide == "short") {
            type = ret.data[i].side == "sell" ? "Limit order to open short: Limit order to close short";
        } else {
            type = "Order Type Error";
        }
        let symbol = ret.data[i].instId.replace("-USDT-SWAP", "") + "_USDT";
        pending_orders.push({
            OrderId: ret.data[i].ordId,
            Symbol: symbol,
            Price: Number(ret.data[i].px),
            Amount: Number(ret.data[i].sz),
            DealAmount: Number(ret.data[i].accFillSz),
            Type: type,
            StopPrice: 0,
            TakeProfitPrice: 0,
            Time: ret.data[i].uTime,
        });
    }
    for (let i = 0; i < ret2.data.length; i++) {
        let type = "";
        let stop_price = 0;
        let take_profit_price = 0;
        if (ret2.data[i].slTriggerPx && ret2.data[i].tpTriggerPx) {
            type = ret2.data[i].posSide == "long" ? "Long position take profit and stop loss : Short position take profit and stop loss";
            stop_price = Number(ret2.data[i].slTriggerPx);
            take_profit_price = Number(ret2.data[i].tpTriggerPx);
        } else if (ret2.data[i].slTriggerPx) {
            type = ret2.data[i].posSide == "long" ? "Long position stop loss: Short position stop loss";
            stop_price = Number(ret2.data[i].slTriggerPx);         
        } else if (ret2.data[i].tpTriggerPx) {
            type = ret2.data[i].posSide == "long" ? "Long position take profit: Short position take profit";
            take_profit_price = Number(ret2.data[i].tpTriggerPx);       
        } else {
            type = "Order Type Error";
        }
        let symbol = ret2.data[i].instId.replace("-USDT-SWAP", "") + "_USDT";
        pending_orders.push({
            OrderId: ret2.data[i].algoId,
            Symbol: symbol,
            Price: 0,
            Amount: Number(ret2.data[i].sz),
            DealAmount: 0,
            Type: type,
            StopPrice: stop_price,
            TakeProfitPrice: take_profit_price,
            Time: ret2.data[i].cTime,
        });
    }

    return pending_orders;
} 

function main() {
    getAllPendingOrdersInOkex(0);
}
```

> Detail

https://www.fmz.com/strategy/340779

> Last Modified

2022-01-14 22:29:20
