
> Name

Multi-Platform-Account-Statistics

> Author

数·狂

> Strategy Description

Multi-Platform Account Statistics

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Interval|20|Detection Interval (Seconds))|
|Type|0|Display type: Total assets|Net assets|Total money|Total coins|
|coverStocks|false|Total coins to close|
|Thr|0.1|Report threshold|


> Source (javascript)

``` javascript
function EnsureCall(e, method) {
    var r;
    while (!(r = e[method].apply(this, Array.prototype.slice.call(arguments).slice(2)))) {
        Sleep(Interval);
    }
    return r;
}

var lastReport = 0;

function onTick() {
    var allBalance = 0;
    var allStocks = 0;
    var asset = 0;
    for (var i = 0; i < exchanges.length; i++) {
        var account = EnsureCall(exchanges[i],"GetAccount");
        var ticker = EnsureCall(exchanges[i],"GetTicker");
        allBalance += account.Balance + account.FrozenBalance;
        allStocks += account.Stocks + account.FrozenStocks;
        asset += (account.Balance + account.FrozenBalance) + (account.Stocks + account.FrozenStocks) * ticker.Last;
    }
    
    if (Type === 0 && Math.abs(asset - lastReport) >= Thr) {
        LogProfit(asset, "Total money:", allBalance, "Total coins:", allStocks, "Total assets:", asset);
        lastReport = asset;
    }
    else if (Type == 1) {
        var netAsset = asset - coverStocks * (asset - allBalance) / allStocks;
        if (Math.abs(netAsset - lastReport) >= Thr) {
            LogProfit(netAsset, "Total money:", allBalance, "Total coins:", allStocks, "Total assets:", asset);
            lastReport = netAsset;
        }
    }
    else if (Type == 2 && Math.abs(allBalance - lastReport) >= Thr){
        LogProfit(allBalance, "Total money:", allBalance, "Total coins:", allStocks, "Total assets:", asset);
        lastReport = allBalance;
    }
    else if (Type == 3 && Math.abs(allStocks - lastReport) >= Thr) {
        LogProfit(allStocks, "Total money:", allBalance, "Total coins:", allStocks, "Total assets:", asset);
        lastReport = allStocks;
    }
    
}

function main() {
    while (1) {
        onTick();
        Sleep(Interval*1000);
    }
}

```

> Detail

https://www.fmz.com/strategy/7827

> Last Modified

2015-12-08 12:17:13
