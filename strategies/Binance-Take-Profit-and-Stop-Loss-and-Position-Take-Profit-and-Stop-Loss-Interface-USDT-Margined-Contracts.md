
> Name

Binance-Take-Profit-and-Stop-Loss-and-Position-Take-Profit-and-Stop-Loss-Interface-USDT-Margined-Contracts

> Author

夏天不打你





> Source (javascript)

``` javascript
// Place long orders and stop loss
function longStopLoss(num, symbol, price, size) {
    var time = UnixNano() / 1000000;
    var param = null;
    // var param = "symbol=" + symbol + "&quantity=" + size.toString() + "&stopPrice=" + price.toString() + "&side=SELL" + "&type=STOP_MARKET" + "&timestamp=" + time.toString();                           // Unidirectional position
    if (size != 0) {
        param = "symbol=" + symbol + "&quantity=" + size.toString() + "&stopPrice=" + price.toString() + "&side=SELL" + "&type=STOP_MARKET" + "&positionSide=LONG" + "&timestamp=" + time.toString();       // Bidirectional position
    } else {
        param = "symbol=" + symbol + "&closePosition=true" + "&stopPrice=" + price.toString() + "&side=SELL" + "&type=STOP_MARKET" + "&positionSide=LONG" + "&timestamp=" + time.toString();                // Position take profit and stop loss
    }
    var ret = exchanges[num].IO("api", "POST", "/fapi/v1/order", param);
    Log(exchanges[num].GetLabel(), ": Place long orders and stop loss:", ret);
    return true;
}

// Place long order to take profit
function longTakeProfit(num, symbol, price, size) {
    var time = UnixNano() / 1000000;
    var param = null;
    if (size != 0) {
        param = "symbol=" + symbol + "&quantity=" + size.toString() + "&stopPrice=" + price.toString() + "&side=SELL" + "&type=TAKE_PROFIT_MARKET" + "&positionSide=LONG" + "&timestamp=" + time.toString();       // Bidirectional position
    } else {
        param = "symbol=" + symbol + "&closePosition=true" + "&stopPrice=" + price.toString() + "&side=SELL" + "&type=TAKE_PROFIT_MARKET" + "&positionSide=LONG" + "&timestamp=" + time.toString();                // Position take profit and stop loss
    }
    var ret = exchanges[num].IO("api", "POST", "/fapi/v1/order", param);
    Log(exchanges[num].GetLabel(), ": Place long order to take profit:", ret);
    return true;
}

// Place short order and stop loss
function shortStopLoss(num, symbol, price, size) {
    var time = UnixNano() / 1000000;
    var param = null;
    // var param = "symbol=" + symbol + "&quantity=" + size.toString() + "&stopPrice=" + price.toString() + "&side=BUY" + "&type=STOP_MARKET" + "&timestamp=" + time.toString();                          // Unidirectional position   
    if (size != 0) {     
        param = "symbol=" + symbol + "&quantity=" + size.toString() + "&stopPrice=" + price.toString() + "&side=BUY" + "&type=STOP_MARKET" + "&positionSide=SHORT" + "&timestamp=" + time.toString();     // Bidirectional position
    } else {
        param = "symbol=" + symbol + "&closePosition=true" + "&stopPrice=" + price.toString() + "&side=BUY" + "&type=STOP_MARKET" + "&positionSide=SHORT" + "&timestamp=" + time.toString();              // Position take profit and stop loss
    }
    var ret = exchanges[num].IO("api", "POST", "/fapi/v1/order", param);
    Log(exchanges[num].GetLabel(), ": Place short order and stop loss:", ret);
    return true;
}

// Place short order to take profit
function shortTakeProfit(num, symbol, price, size) {
    var time = UnixNano() / 1000000;
    var param = null;
    if (size != 0) {     
        param = "symbol=" + symbol + "&quantity=" + size.toString() + "&stopPrice=" + price.toString() + "&side=BUY" + "&type=TAKE_PROFIT_MARKET" + "&positionSide=SHORT" + "&timestamp=" + time.toString();     // Bidirectional position
    } else {
        param = "symbol=" + symbol + "&closePosition=true" + "&stopPrice=" + price.toString() + "&side=BUY" + "&type=TAKE_PROFIT_MARKET" + "&positionSide=SHORT" + "&timestamp=" + time.toString();              // Position take profit and stop loss
    }
    var ret = exchanges[num].IO("api", "POST", "/fapi/v1/order", param);
    Log(exchanges[num].GetLabel(), ": Place short order to take profit:", ret);
    return true;
}
```

> Detail

https://www.fmz.com/strategy/319427

> Last Modified

2022-06-13 11:56:29
