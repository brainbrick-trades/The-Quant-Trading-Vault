
> Name

Example-of-Fund-Transfer-Between-Huobi-Futures-Currency-Accounts

> Author

发明者量化-小小梦





> Source (javascript)

``` javascript
function main() {
    // API Interface description:
    // https://api.huobi.pro
    // POST /v1/futures/transfer
    // params    currency e.g. btc
    //           amount
    //           type futures-to-pro
    
    Log(exchange.GetAccount())
    var ret = exchange.IO("api", "POST", "/v1/futures/transfer", "currency=ltc&amount=0.1&type=pro-to-futures")   // TestingLTC , Spot to futures
    Log("ret", ret)
    
    /* ret
    ret {"status":"ok","data":25669845}
    */
}
```

> Detail

https://www.fmz.com/strategy/148532

> Last Modified

2019-05-20 18:19:53
