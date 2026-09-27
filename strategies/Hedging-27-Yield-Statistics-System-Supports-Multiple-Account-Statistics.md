
> Name

Hedging-27-Yield-Statistics-System-Supports-Multiple-Account-Statistics

> Author

Zero

> Strategy Description

Hedging 2.7 yield statistics system supports multiple groups of account statistics. Add exchanges with an even length to start statistics. Every two are added as a group.
The coin price will use the first exchange's best bid as a reference

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Interval|60|Statistics interval (seconds)|
|InitMode|0|Mode of counting initial funds: automatic statistics | manual input|
|InitBalance|false|Initial total money|
|InitStocks|false|Initial total coins|


> Source (javascript)

``` javascript
//

function main() {
    if (exchanges.length == 0 || exchanges.length % 2 !== 0) {
        throw "Exchange parameters must be integers of 2";
    }
    var cfg = {
        __isStock: true,
        tooltip: {
            xDateFormat: '%Y-%m-%d %H:%M:%S, %A'
        },
        title: {
            text: 'Multi-platform return statistics'
        },
        subtitle: {
            text: 'Counting...'
        },
        xAxis: {
            type: 'datetime'
        },
        legend: {
            enabled: true,
        },
        rangeSelector: {
            buttons: [{
                type: 'hour',
                count: 1,
                text: '1h'
            }, {
                type: 'hour',
                count: 3,
                text: '3h'
            }, {
                type: 'hour',
                count: 8,
                text: '8h'
            }, {
                type: 'all',
                text: 'All'
            }],
            selected: 0,
            inputEnabled: false
        },
        series: []
    };
    var i = 0;
    for (i = 0; i < exchanges.length; i += 2) {
        cfg.series.push({
            name: exchanges[i].GetLabel() + '/' + exchanges[i + 1].GetLabel(),
            data: [],
            tooltip: {
                valueDecimals: 4
            }
        });
    }
    var chart = Chart(cfg);
    var counter = 0;
    var getAccounts = function() {
        var accounts = [];
        for (var i = 0; i < exchanges.length; i++) {
            accounts.push(_C(exchanges[i].GetAccount));
        }
        return accounts;
    };
    var initAccounts = getAccounts();
    if (InitMode == 1) {
        Log("Initial total funds manually specified as, Money: ", InitBalance, "Currency:", InitStocks);
    } else {
        InitBalance = 0;
        InitStocks = 0;
        for (var i = 0; i < initAccounts.length; i++) {
            InitBalance += initAccounts[i].Balance + initAccounts[i].FrozenBalance;
            InitStocks += initAccounts[i].Stocks + initAccounts[i].FrozenStocks;
        }
        Log("Initial total funds automatically specified as, Money: ", InitBalance, "Currency:", InitStocks);
    }
    while (true) {
        if (counter > 0) {
            Sleep(Interval * 1000);
        }
        counter++;
        var tbl = {
            type: 'table',
            title: 'Account Information',
            cols: ['Exchange', 'Current group income', 'Initial money', 'Initial coin', 'Current money', 'Current currency'],
            rows: []
        };
        var ticker = _C(exchange.GetTicker);
        var accounts = getAccounts();
        var ts = new Date().getTime();
        var allBalance = 0;
        var allStocks = 0;
        for (i = 0; i < accounts.length; i += 2) {
            var profit = (accounts[i].Balance + accounts[i].FrozenBalance + accounts[i + 1].Balance + accounts[i + 1].FrozenBalance) - (initAccounts[i].Balance + initAccounts[i].FrozenBalance + initAccounts[i + 1].Balance + initAccounts[i + 1].FrozenBalance) + (((accounts[i].Stocks + accounts[i].FrozenStocks + accounts[i + 1].Stocks + accounts[i + 1].FrozenStocks) - (initAccounts[i].Stocks + initAccounts[i].FrozenStocks + initAccounts[i + 1].Stocks + initAccounts[i + 1].FrozenStocks)) * ticker.Buy);
            chart.add(i / 2, [ts, _N(profit)]);
            for (var j = i; j < (i+2); j++) {
                tbl.rows.push([exchanges[j].GetLabel(), j % 2 == 0 ? _N(profit, 4) : '--', initAccounts[j].Balance + (initAccounts[j].FrozenBalance > 0 ? ' ( freeze: ' + initAccounts[j].FrozenBalance + ' )' : ''), initAccounts[j].Stocks+ (initAccounts[j].FrozenStocks > 0 ? ' ( freeze: ' + initAccounts[j].FrozenStocks + ' )' : ''), accounts[j].Balance+ (accounts[j].FrozenBalance > 0 ? ' ( freeze: ' + accounts[j].FrozenBalance + ' )' : ''), accounts[j].Stocks+ (accounts[j].FrozenStocks > 0 ? ' ( freeze: ' + accounts[j].FrozenStocks + ' )' : '')]);
                allBalance += accounts[j].Balance + accounts[j].FrozenBalance;
                allStocks += accounts[j].Stocks + accounts[j].FrozenStocks;
            }
        }
        cfg.subtitle.text = "Initial total money: " + _N(InitBalance) + ", Initial total coins: " + _N(InitStocks) + ", Current total money: " + _N(allBalance) + ", Current total coins: " + _N(allStocks) + ", Buy one price: " + ticker.Last + ", Total profit: " + _N((allBalance-InitBalance) + ((allStocks-InitStocks) * ticker.Buy)) + " element";
        chart.update(cfg);
        LogStatus('`' + JSON.stringify(tbl) + '`');
    }
}
```

> Detail

https://www.fmz.com/strategy/18678

> Last Modified

2016-08-13 18:32:22
