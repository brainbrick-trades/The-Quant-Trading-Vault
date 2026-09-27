
> Name

Function-Automatic-Fault-Tolerance-Template

> Author

Zero

> Strategy Description

After checking the box to call this template, it will automatically retry fault tolerance for the specified API function, supporting multiple exchanges

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|RetryInterval|500|Fault-tolerant retry interval (milliseconds)|
|Debug|true|Display retry records|
|EnableErrorFilter|false|Filter out common network error messages|
|ApiList|GetAccount,GetDepth,GetTicker,GetRecords,GetTrades,GetOrders,SetContractType|Fault-tolerant API list|


> Source (javascript)

``` javascript
// Called during template initialization
function init() {
    // Filter common errors
    if (EnableErrorFilter) {
        SetErrorFilter("502:|503:|tcp|character|connection|unexpected|network|timeout|WSARecv|Connect|GetAddr|no such|reset|http|received|EOF|reused");
    }
    // Redefine functions that require fault tolerance
    var names = ApiList.split(',');
    _.each(exchanges, function(e) {
        _.each(names, function(name) {
            if (typeof(e[name]) !== 'function') {
                throw "Try fault tolerance " + name + " Failed, Please confirm existence of thisAPIAnd enter correctly.";
            }
            var old = e[name];
            e[name] = function() {
                var r;
                while (!(r = old.apply(this, Array.prototype.slice.call(arguments)))) {
                    if (Debug) {
                        Log(e.GetLabel(), name, "Call failed", RetryInterval, "Retry after milliseconds...");
                    }
                    Sleep(RetryInterval);
                }
                return r;
            };
        });
    });
    Log("Fault-tolerance mechanism enabled", names);
}

// Test
function main() {
    // At This MomentGetTickerNo need to retry
    Log(exchange.GetTicker());
}
```

> Detail

https://www.fmz.com/strategy/11609

> Last Modified

2016-04-03 17:17:41
