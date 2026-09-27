
> Name

BitMEX-Advanced-API-Features-Futures-Bulk-Order-and-One-Click-Cancel-JavaScript

> Author

FawkesPan





> Source (javascript)

``` javascript
/*

 BitMEX Advanced API Interface for FMZ.com.

 Copyright 2018 FawkesPan
 Contact : i@fawkex.me / Telegram@FawkesPan

 GNU General Public License v3.0

*/

function main() {
    Log(exchange.GetAccount());
}
var bulk = []
// Add Bulk Buy Orders
function BulkBuy(symbol,qty,price,type,exec) {
    Log("NewBulkOrder Open Long "+ symbol + " " + price + "   " + qty)
    var order = {};
    order.symbol = symbol;
    order.side = "Buy";
    order.orderQty = qty;
    order.price = price;
    order.ordType = type;
    order.execInst = exec;
    bulk[Object.keys(bulk).length] = order;
}
// Add Bulk Sell Orders
function BulkSell(symbol,qty,price,type,exec) {
    Log("NewBulkOrder Open Short "+ symbol + " " + price + "   " + qty)
    var order = {};
    order.symbol = symbol;
    order.side = "Sell";
    order.orderQty = qty;
    order.price = price;
    order.ordType = type;
    order.execInst = exec;
    bulk[Object.keys(bulk).length] = order;
}
//Execute Bulk Orders
function BulkPost() {
    Log("is executingBulkOrders Total " + Object.keys(bulk).length + " Orders");
    var param = "orders=" + JSON.stringify(bulk);
    bulk = [];
    exchange.IO("api", "POST", "/api/v1/order/bulk", param);
}
//Cancel All Orders
function CancelPendingOrders() {
    exchange.IO("api","DELETE","/api/v1/order/all","symbol="+exchange.GetCurrency());
}
```

> Detail

https://www.fmz.com/strategy/105056

> Last Modified

2018-08-30 03:01:43
