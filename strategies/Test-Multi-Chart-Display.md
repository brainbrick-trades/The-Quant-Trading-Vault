
> Name

Test-Multi-Chart-Display

> Author

Zero

> Strategy Description

The platform supports displaying multiple charts for the strategy at the same time. This is a simple example
For specific usage, refer to the Chart section in the API documentation https://www.fmz.com/api#chart



> Source (javascript)

``` javascript
/*backtest
start: 2019-01-22 00:00:00
end: 2019-01-23 00:00:00
period: 30m
exchanges: [{"eid":"OKCoin_EN","currency":"BTC_USD"}]
*/

function main() {
    var cfgA = {
        extension: {
            layout: 'single', // Do not participate in grouping; display separately, default is grouped 'group'
            height: 300, // Specify height
        },
        title: {
            text: 'Handicap chart'
        },
        xAxis: {
            type: 'datetime'
        },
        series: [{
            name: 'Buy one',
            data: [],
        }, {
            name: 'Sell one',
            data: [],
        }]
    }
    var cfgB = {
        title: {
            text: 'Price Difference Chart'
        },
        xAxis: {
            type: 'datetime'
        },
        series: [{
            name: 'Spread',
            type: 'column',
            data: [],
        }]
    }

    var cfgC = {
        __isStock: false,
        title: {
            text: 'Pie chart'
        },
        series: [{
            type: 'pie',
            name: 'one',
            data: [
                ["A", 25],
                ["B", 25],
                ["C", 25],
                ["D", 25],
            ]  // After specifying the initial data, there is no need to update it with the add function. You can update the sequence by directly changing the chart configuration..
        }]
    };
    var cfgD = {
        extension: {
            layout: 'single',
            col: 8, // Specify the cell value occupied by the width, total value is12
            height: '300px',
        },
        title: {
            text: 'Handicap chart'
        },
        xAxis: {
            type: 'datetime'
        },
        series: [{
            name: 'Buy one',
            data: [],
        }, {
            name: 'Sell one',
            data: [],
        }]
    }
    var cfgE = {
        __isStock: false,
        extension: {
            layout: 'single',
            col: 4,
            height: '300px',
        },
        title: {
            text: 'Pie chart2'
        },
        series: [{
            type: 'pie',
            name: 'one',
            data: [
                ["A", 25],
                ["B", 25],
                ["C", 25],
                ["D", 25],
            ]
        }]
    };

    var chart = Chart([cfgA, cfgB, cfgC, cfgD, cfgE]);
    chart.reset()
        // Add a data point for the pie chart,addCan only update passaddData points added by method, Built-in data points cannot be updated later
    chart.add(3, {
        name: "ZZ",
        y: Math.random() * 100
    });
    while (true) {
        Sleep(1000)
        var ticker = exchange.GetTicker()
        if (!ticker) {
            continue;
        }
        var diff = ticker.Sell - ticker.Buy
        cfgA.subtitle = {
            text: 'Buy one ' + ticker.Buy + ', Sell one ' + ticker.Sell,
        };
        cfgB.subtitle = {
            text: 'Price difference ' + diff,
        };

        chart.add([0, [new Date().getTime(), ticker.Buy]]);
        chart.add([1, [new Date().getTime(), ticker.Sell]]);
        // Equivalent to updating the first data series of the second chart
        chart.add([2, [new Date().getTime(), diff]]);
        chart.add(4, [new Date().getTime(), ticker.Buy]);
        chart.add(5, [new Date().getTime(), ticker.Buy]);
        cfgC.series[0].data[0][1] = Math.random() * 100;
        cfgE.series[0].data[0][1] = Math.random() * 100;
        // updateActually equivalent to resetting the chart configuration
        chart.update([cfgA, cfgB, cfgC, cfgD, cfgE]);
    }
}
```

> Detail

https://www.fmz.com/strategy/38203

> Last Modified

2020-04-08 14:53:51
