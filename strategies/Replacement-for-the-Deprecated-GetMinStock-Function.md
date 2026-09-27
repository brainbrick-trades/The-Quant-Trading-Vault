
> Name

Replacement-for-the-Deprecated-GetMinStock-Function

> Author

hugo_zhou





> Source (javascript)

``` javascript
/****************
  Get minimum trading volume for different currency pairs on Huobi Pro
  Other platforms need to add different error parsing codes themselves.
****************/

function main() {
    SetErrorFilter("limit order amount error");
    //Add the currency pairs you want to know
    var huobipro = ["BTC_USDT","XRP_USDT","EOS_BTC","OMG_ETH"];
    
    for(var i = 0;i<huobipro.length;i++){
        exchange.IO("currency", huobipro[i]);
        var ticker = exchange.GetTicker();
        exchange.Buy(ticker.Sell, 0.00000001);   // amountYou can only write as small as possible, and get the correct one returned by the server.min 
        var error = GetLastError();
        // Huobi error code analysis, different trading platforms should be different     limit order amount error, min: `0.00000001`    
        if(error.indexOf("limit order amount error, min") >= 0){
            var min = parseFloat(error.split(": `")[1]);
            _G(exchange.GetName()+exchange.GetCurrency(),min);
        }
    }
    
    //Print out from the database
    for(var j = 0;j<huobipro.length;j++){
        Log(exchange.GetName()+huobipro[j],":",_G(exchange.GetName()+huobipro[j]));
    }
}
```

> Detail

https://www.fmz.com/strategy/69436

> Last Modified

2018-01-17 17:42:25
