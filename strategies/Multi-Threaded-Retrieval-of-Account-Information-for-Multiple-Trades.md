
> Name

Multi-Threaded-Retrieval-of-Account-Information-for-Multiple-Trades

> Author

Zero

> Strategy Description

Multi-threaded retrieval of account information for multiple trades



> Source (javascript)

``` javascript
function main() {
    var accounts = [];
    while (true) {
        for (var i = 0; i < exchanges.length; i++) {
            if (accounts[i] == null) {
                // Create Asynchronous Operation
                accounts[i] = exchanges[i].Go("GetAccount");
            }
        }
        var failed = 0;
        for (var i = 0; i < exchanges.length; i++) {
            if (typeof(accounts[i].wait) != "undefined") {
                // Waiting for results
                var ret = accounts[i].wait();
                if (ret) {
                    accounts[i] = ret;
                    Log(exchanges[i].GetName(), accounts[i]);
                } else {
                    // Try again
                    accounts[i] = null;
                    failed++;
                }
            }
        }
        if (failed == 0) {
            break;
        } else {
            Sleep(100);
        }
    }
}
```

> Detail

https://www.fmz.com/strategy/3297

> Last Modified

2014-12-11 03:56:53
