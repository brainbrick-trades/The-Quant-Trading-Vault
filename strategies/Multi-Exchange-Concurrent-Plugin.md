
> Name

Multi-Exchange-Concurrent-Plugin

> Author

@cqz



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|AsyncTimeout|2000|Asynchronous operation timeout|


> Source (javascript)

``` javascript
/*
-- After the strategy references this template, use it directly $.Test() Call this method
-- main The function will not be triggered in the strategy, only serves as an entry point for template debugging
*/

//AsyncTimeout

function asyncExchangeCmd(param) {
    let beginTime = new Date().getTime();
    let elapses = [];
    let results = [];
    while (true) {
        for (let i = 0; i < exchanges.length; i++) {
            if (results[i] == null && (elapses[i] == null || elapses[i] <= AsyncTimeout)) {
                // Create Asynchronous Operation
                results[i] = exchanges[i].Go.apply(this, param)
            }
        }
        let failed = 0;
        for (let i = 0; i < exchanges.length; i++) {
            if (results[i] == null) {
                continue;
            }
            if (typeof (results[i].wait) != "undefined") {
                // Waiting for results
                let result = results[i].wait(2);
                if (typeof (result) != "undefined") {
                    if (result) {
                        results[i] = result;
                    } else {
                        // Try again
                        results[i] = null;
                        failed++;
                    }
                } else {
                    failed++;
                }
                elapses[i] = new Date().getTime() - beginTime;
            }
        }
        if (failed === 0) {
            break;
        }
    }
    let failed = 0;
    for (let i = 0; i < exchanges.length; i++) {
        if (results[i] == null) {
            failed++;
        }
    }
    let finishTime = new Date().getTime();
    return {
        "failed": failed,
        "totalElapse": finishTime - beginTime,
        "elapses": elapses,
        "results": results
    };
}

$.GetTickerInfo = function () {
    return asyncExchangeCmd(["GetTicker"]);
};


$.GetDepthInfo = function () {
    return asyncExchangeCmd(["GetDepth"]);
};

function main() {
    var depthInfo = $.GetDepthInfo();
    Log(JSON.stringify(depthInfo));
}
```

> Detail

https://www.fmz.com/strategy/365412

> Last Modified

2022-05-24 17:55:21
