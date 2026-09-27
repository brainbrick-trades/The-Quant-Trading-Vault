
> Name

Binance-Account-Cross-Transfer-Small-Tool

> Author

wenzhang.





> Source (javascript)

``` javascript
function userUniversalTransfer(type, amount) {
    let ret = null;
    const param =
      "type=" +
      type +
      "&asset=USDT" +
      "&amount=" +
      amount.toString() +
      "&timestamp=" +
      new Date().getTime().toString();

    exchange.SetBase("https://api.binance.com");
    ret = exchange.IO("api", "POST", "/sapi/v1/asset/transfer", param);
    exchange.SetBase("https://fapi.binance.com");

    if (ret) {
      switch (type) {
        case "MAIN_UMFUTURE":
          Log(`Already ${amount.toFixed(3)} USDT Transferred from spot walletUBase contract wallet`);
          break;

        case "UMFUTURE_MAIN":
          Log(`Already ${amount.toFixed(3)} USDT fromUTransfer contract wallet to spot wallet`);
          break;
      }
    } else {
      Log("Fund transfer failed!");
    }
  }
```

> Detail

https://www.fmz.com/strategy/446356

> Last Modified

2024-03-28 00:17:46
