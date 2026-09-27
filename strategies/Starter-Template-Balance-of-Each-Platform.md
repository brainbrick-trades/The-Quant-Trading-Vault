
> Name

Starter-Template-Balance-of-Each-Platform

> Author

Zero

> Strategy Description

Check balances and coin quantities on each platform

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|DisableRate|false|Disable exchange rate conversion|


> Source (javascript)

``` javascript
function main() {
    for (var i = 0; i < exchanges.length; i++) {
        if (DisableRate) {
            exchanges[i].SetRate(1);
        }

        if (exchanges[i].GetName().indexOf('CTP') != -1) {
            while (!exchanges[i].IO("status")) {
                LogStatus("Waiting" + exchanges[i].GetLabel() + "Connect to the exchange server, Market data server: " + (exchanges[i].IO("status", 0) ? 'Normal' : 'Disconnect') + ', Trading server: ' + (exchanges[i].IO("status", 1) ? 'Normal' : 'Disconnect'));
                Sleep(1000);
            }
            LogStatus("Connection successful");
        }

        while (true) {
            var account = exchanges[i].GetAccount();
            if (account) {
                Log(exchanges[i].GetName(), exchanges[i].GetLabel(), exchanges[i].GetCurrency(), exchanges[i].GetAccount());
                break;
            }
            Sleep(3000);
        }
    }
}
```

> Detail

https://www.fmz.com/strategy/48

> Last Modified

2016-07-25 16:10:13
