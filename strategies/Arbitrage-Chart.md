
> Name

Arbitrage-Chart

> Author

ChaoZhang



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|SYMBOL1||trading pair1|
|SYMBOL2||trading pair2|
|BASESYBMOL||Reference Trading Pair|
|PERIOD||timeframe|


> Source (javascript)

``` javascript
// thischartAt/InJavaScriptIn the language it is an object, when usingChartBefore the function, we need to declare an object variable to configure the chartchart
let PERIODARR = [PERIOD_M1, PERIOD_M3, PERIOD_M5, PERIOD_M15, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H4, PERIOD_H6, PERIOD_H12, PERIOD_D1, PERIOD_D3, PERIOD_W1];

/**
 * Calculate the simple moving average (SMA)
 * @param {Array<number>} data - Input data array
 * @param {number} period - Period of moving average
 * @returns {Array<number>} - An array containing SMA values
 */
function calculateSMA(data, period) {
    let sma = [];
    let sum = 0;

    for (let i = 0; i < data.length; i++) {
        sum += data[i];

        if (i >= period - 1) {
            sma.push(sum / period);
            sum -= data[i - period + 1];
        } else {
            sma.push(null); // If there are not enough data points to calculateSMA,Returnnull
        }
    }

    // Fillnullvalue
    let firstNonNull = sma.find(value => value !== null);
    for (let i = 0; i < sma.length; i++) {
        if (sma[i] === null) {
            sma[i] = firstNonNull;
        }
    }

    return sma;
}

/**
 * Calculate Standard Deviation (Standard Deviation)
 * @param {Array<number>} data - Input data array
 * @param {number} period - Period for standard deviation calculation
 * @returns {Array<number>} - An array containing standard deviation values
 */
function calculateStdev(data, period) {
    let stdev = [];

    for (let i = 0; i < data.length; i++) {
        if (i >= period - 1) {
            let subset = data.slice(i - period + 1, i + 1);
            let mean = subset.reduce((a, b) => a + b, 0) / period;
            let variance = subset.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / period;
            stdev.push(Math.sqrt(variance));
        } else {
            stdev.push(null); // If there are not enough data points to calculate standard deviation, returnnull
        }
    }

    // Fillnullvalue
    let firstNonNull = stdev.find(value => value !== null);
    for (let i = 0; i < stdev.length; i++) {
        if (stdev[i] === null) {
            stdev[i] = firstNonNull;
        }
    }

    return stdev;
}

function main() {
    exchange.SetContractType("swap");
    // exchange.SetMaxBarLen(200);
    let chart = {
        // This field marks whether the chart is a general chart; those interested can modify itfalseRun and see
        __isStock: false, // Zoom tool
        tooltip: {
            xDateFormat: "%Y-%m-%d %H:%M:%S, %A",
            shared: true,
            crosshairs: true, // Enable Crosshair
            formatter: function () {
                let s = "<b>" + Highcharts.dateFormat("%Y-%m-%d %H:%M:%S, %A", this.x) + "</b>";

                this.points.forEach(function (point) {
                    s += "<br/>" + point.series.name + ": " + point.y.toFixed(2);
                });

                return s;
            }
        }, // Title
        title: { text: "Spread analysis chart
        rangeSelector: {
            buttons: [
                { type: "hour", count: 1, text: "1h" },
                { type: "hour", count: 3, text: "3h" },
                {
                    type: "hour",
                    count: 8,
                    text: "8h"
                },
                { type: "all", text: "All" }
            ],
            selected: 0,
            inputEnabled: false
        }, // The horizontal axis of the coordinate axis is: x-axis. The current setting type is: time
        xAxis: {
            type: "datetime",
            crosshair: {
                color: "#cccccc", // Crosshair Color
                dashStyle: "shortdash", // Dashed line style
                width: 1, // Line width
                zIndex: 5 // Ensure the line displays above other elements
            }
        }, // The vertical axis of the coordinate axis is: y-axis. The default value is adjusted according to the data size.
        yAxis: {
            // Title
            title: { text: "Spread
            opposite: false
        }, // Data series, this property stores the various data series (lines, candlestick charts, labels, etc.)....)
        series: [
            // indexed as0,dataThe array stores the data of this index series
            //Specify Color Asblue
            { name: "spread", id: "spread", data: [], color: "blue" }, // Index is 1, dashStyle:'shortdash' is set, meaning: set to dashed line.
            { name: "basis", id: "basis", data: [], color: "orange" },
            {
                name: "upper",
                id: "upper",
                data: [],
                color: "red"
            },
            { name: "lower", id: "lower", data: [], color: "green" }
        ]
    };
    let symbol1Trades = exchange.GetRecords(SYMBOL1 , PERIODARR[PERIOD]);
    let symbol2Trades = exchange.GetRecords(SYMBOL2 , PERIODARR[PERIOD]);
    let baseTrades = exchange.GetRecords(BASESYBMOL , PERIODARR[PERIOD]);
    Log(symbol1Trades.length, symbol2Trades.length, baseTrades.length);
    Log(symbol1Trades[0], symbol2Trades[0], baseTrades[0]);
    //Take the smallest length as the number of cycles
    let len = Math.min(symbol1Trades.length, symbol2Trades.length, baseTrades.length);
    let spreadRecords = [];
    //Loop traversal
    for (let i = 0; i < len; i++) {
        //Get the price of each trading pair
        let symbol1Price = symbol1Trades[i].Close;
        let symbol2Price = symbol2Trades[i].Close;
        let basePrice = baseTrades[i].Close;
        //Calculate the price difference
        let diff1 = symbol1Price / basePrice;
        let diff2 = symbol2Price / basePrice;
        let spread = diff1 / diff2;
        spreadRecords.push(spread);
        let basis = calculateSMA(spreadRecords, 20);
        let calculateStdevs = calculateStdev(spreadRecords, 20);
        let dev = 2 * calculateStdevs[i];
        let upper = basis[i] + dev;
        let lower = basis[i] - dev;
        //Add spread data to the chart
        chart.series[0].data.push([symbol1Trades[i].Time, spread]);
        chart.series[1].data.push([symbol1Trades[i].Time, basis[i]]);
        chart.series[2].data.push([symbol1Trades[i].Time, upper]);
        chart.series[3].data.push([symbol1Trades[i].Time, lower]);
    }
    return chart;
}

```

> Detail

https://www.fmz.com/strategy/455637

> Last Modified

2024-07-11 18:33:26
