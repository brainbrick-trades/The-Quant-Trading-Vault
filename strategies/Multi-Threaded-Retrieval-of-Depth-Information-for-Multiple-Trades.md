
> Name

Multi-Threaded-Retrieval-of-Depth-Information-for-Multiple-Trades

> Author

Zero

> Strategy Description

Multi-threaded retrieval of depth information for multiple trades



> Source (javascript)

``` javascript
function main() {
    var depths = [];
    while (true) {
        for (var i = 0; i < exchanges.length; i++) {
            if (depths[i] == null) {
                // Create Asynchronous Operation
                depths[i] = exchanges[i].Go("GetDepth");
            }
        }
        var failed = 0;
        for (var i = 0; i < exchanges.length; i++) {
            if (typeof(depths[i].wait) != "undefined") {
                // Waiting for results
                var ret = depths[i].wait();
                if (ret) {
                    depths[i] = ret;
                    Log(exchanges[i].GetName(), depths[i]);
                } else {
                    // Try again
                    depths[i] = null;
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

https://www.fmz.com/strategy/3651

> Last Modified

2015-01-02 17:18:36
