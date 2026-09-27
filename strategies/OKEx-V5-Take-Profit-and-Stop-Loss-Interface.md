
> Name

OKEx-V5-Take-Profit-and-Stop-Loss-Interface

> Author

夏天不打你





> Source (javascript)

``` javascript


// Place long orders and stop loss
function longStopLossInOkex(num, symbol, price, size) {
    let real_symbol = symbol.replace("_USDT", "") + "-USDT-SWAP";
    var param = "instId=" + real_symbol + "&tdMode=cross" + "&side=sell" + "&posSide=long" + "&ordType=conditional" + "&sz=" + size.toString() + "&slTriggerPx=" + price.toString() + "&slOrdPx=-1";
    var ret = exchanges[num].IO("api", "POST", "/api/v5/trade/order-algo", param);
    Log(exchanges[num].GetLabel(), ": Place long orders and stop loss:", ret);
    return true;
}

// Place long order to take profit
function longTakeProfitInOkex(num, symbol, price, size) {
    let real_symbol = symbol.replace("_USDT", "") + "-USDT-SWAP";
    var param = "instId=" + real_symbol + "&tdMode=cross" + "&side=sell" + "&posSide=long" + "&ordType=conditional" + "&sz=" + size.toString() + "&tpTriggerPx=" + price.toString() + "&tpOrdPx=-1";
    var ret = exchanges[num].IO("api", "POST", "/api/v5/trade/order-algo", param);
    Log(exchanges[num].GetLabel(), ": Place long order to take profit:", ret);
    return true;
}

// Place short order and stop loss
function shortStopLossInOkex(num, symbol, price, size) {
    let real_symbol = symbol.replace("_USDT", "") + "-USDT-SWAP";
    var param = "instId=" + real_symbol + "&tdMode=cross" + "&side=buy" + "&posSide=short" + "&ordType=conditional" + "&sz=" + size.toString() + "&slTriggerPx=" + price.toString() + "&slOrdPx=-1";
    var ret = exchanges[num].IO("api", "POST", "/api/v5/trade/order-algo", param);
    Log(exchanges[num].GetLabel(), ": Place short order and stop loss:", ret);
    return true;
}

// Place short order to take profit
function shortTakeProfitInOkex(num, symbol, price, size) {
    let real_symbol = symbol.replace("_USDT", "") + "-USDT-SWAP";
    var param = "instId=" + real_symbol + "&tdMode=cross" + "&side=buy" + "&posSide=short" + "&ordType=conditional" + "&sz=" + size.toString() + "&tpTriggerPx=" + price.toString() + "&tpOrdPx=-1";
    var ret = exchanges[num].IO("api", "POST", "/api/v5/trade/order-algo", param);
    Log(exchanges[num].GetLabel(), ": Place short order to take profit:", ret);
    return true;
}

// Take profit and stop loss for long orders
function longTpAndSlInOkex(num, symbol, tp_price, sl_price, size) {
    let real_symbol = symbol.replace("_USDT", "") + "-USDT-SWAP";
    var param = "instId=" + real_symbol + "&tdMode=cross" + "&side=sell" + "&posSide=long" + "&ordType=oco" + "&sz=" + size.toString() + "&tpTriggerPx=" + tp_price.toString() + "&tpOrdPx=-1"
                    + "&slTriggerPx=" + sl_price.toString() + "&slOrdPx=-1";
    var ret = exchanges[num].IO("api", "POST", "/api/v5/trade/order-algo", param);
    Log(exchanges[num].GetLabel(), ": Take profit and stop loss for long orders:", ret);
    return true;
}

// Take profit and stop loss for short orders
function shortTpAndSlInOkex(num, symbol, tp_price, sl_price, size) {
    let real_symbol = symbol.replace("_USDT", "") + "-USDT-SWAP";
    var param = "instId=" + real_symbol + "&tdMode=cross" + "&side=buy" + "&posSide=short" + "&ordType=oco" + "&sz=" + size.toString() + "&tpTriggerPx=" + tp_price.toString() + "&tpOrdPx=-1"
                    + "&slTriggerPx=" + sl_price.toString() + "&slOrdPx=-1";
    var ret = exchanges[num].IO("api", "POST", "/api/v5/trade/order-algo", param);
    Log(exchanges[num].GetLabel(), ": Take profit and stop loss for short orders:", ret);
    return true;
}

function main() {
    shortTakeProfitInOkex(0, "ETH_USDT", 2800, 1);
    shortTpAndSlInOkex(0, "ETH_USDT", 2800, 3000, 1);
}
```

> Detail

https://www.fmz.com/strategy/340820

> Last Modified

2022-04-07 19:38:37
