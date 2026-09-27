
> Name

Transfer-USDT-from-the-Contract-Account-to-the-Spot-Funding-Account-Supported-Simultaneously-on-OKEx-and-Binance

> Author

夏天不打你





> Source (javascript)

``` javascript
function main() {
    transferToMain(100);
}

// fromUTransfer the specified amount from the contract wallet to the spot walletUSDT
function transferToMain(amount){
    var ret = null;
    if (isOKexExchange()) {
        let param = "ccy=USDT" + "&from=18" + "&amt=" + amount.toString() + "&to=6";
        ret = exchange.IO("api", "POST", "/api/v5/asset/transfer", param);
    } else if (isBinanceExchange()) {
        let time = UnixNano() / 1000000;
        let param = "type=UMFUTURE_MAIN" + "&asset=USDT" + "&amount=" + amount.toString() + "&timestamp=" + time.toString();
        exchange.SetBase('https://api.binance.com');
        ret = exchange.IO("api", "POST", "/sapi/v1/asset/transfer", param);
        exchange.SetBase('https://fapi.binance.com');
    } else {
        Log("Fund transfer failed, unsupported exchange!");
    }
    if (ret) {
        Log("has been transferred from the contract to the spot account: ", amount, " USDT");
        return true;
    } else {
        Log("Fund transfer failed!");
        return false;
    }
}

// Determine whether it is a Binance exchange
function isBinanceExchange() {
    if (exchange.GetName() == "Futures_Binance") {
        return true;
    }
    return false;
}

// Determine WhetherOKEXexchange
function isOKexExchange() {
    if (exchange.GetName() == "Futures_OKCoin") {
        return true;
    }
    return false;
}
```

> Detail

https://www.fmz.com/strategy/338145

> Last Modified

2021-12-30 16:11:11
