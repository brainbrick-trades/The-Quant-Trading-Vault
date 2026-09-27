
> Name

SummerPlot10

> Author

夏天不打你





> Source (javascript)

``` javascript


//#region Version update
/*
------------  [1.0 Version]   ---------------------
----------- 2023.3.14 --------------
1,First edition.
----------- 2023.3.16 --------------
1,Adjust the time range selector.
*/
//#endregion

var _Cfgs = [];
var _Chart = null;

function init() {
    _Chart = Chart([]);
    _Chart.reset();
    Log("SummerPlot init finished.");
}

function setChart(title, line, col, is_single, series_type, is_stock) {
    let char = _Cfgs.find(item => item?.title?.text === title);
    if (char) {
        char.extension.col = col;
        char.extension.layout = is_single ? 'single' : 'group';
        return char;
    } else {
        _Cfgs.push({
            __isStock: is_stock,
            tooltip: {
                xDateFormat: '%Y-%m-%d %H:%M:%S, %A'                // Prompt to add date format
            },
            legend: {
                enabled: true,                                      // Curve user selectable
            },
            extension: {
                layout: is_single ? 'single' : 'group',
                col: col,
            },
            title: {
                text: title
            },
            xAxis: {
                type: 'datetime'
            },
            series: [{
                name: line,
                data: [],
                type: series_type,
            }],
            //#region Set time range as optional
            rangeSelector: {
                buttons: [{
                    type: 'day',
                    count: 1,
                    text: '1d'
                }, {
                    type: 'day',
                    count: 7,
                    text: '7d'
                }, {
                    type: 'month',
                    count: 1,
                    text: '1M'
                }, {
                    type: 'month',
                    count: 3,
                    text: '3M'
                }, {
                    type: 'month',
                    count: 6,
                    text: '6M'
                }, {
                    type: 'year',
                    count: 1,
                    text: '1Y'
                }, {
                    type: 'all',
                    text: 'All'
                }],
                selected: 2,
                inputEnabled: true
            },
            //#endregion
        });
    }
    return _Cfgs[_Cfgs.length - 1];
}

function getSeriesIndex(title, line, series_type) {
    let index = -1, cfg_index = -1, last_series_index = -1;
    for (let i = 0; i < _Cfgs.length; i++) {
        for (let j = 0; j < _Cfgs[i].series.length; j++) {
            index++;
            if (_Cfgs[i].title.text === title) {
                cfg_index = i;                              // Record the index corresponding to the chart
                last_series_index = index;                  // Record the last subscript of the corresponding chart
                if (_Cfgs[i].series[j].name === line && _Cfgs[i].series[j].type === series_type) {
                    // Find the corresponding curve and return the subscript directly
                    return index;
                }
            }
        }
    }
    // If there is no corresponding curve
    _Cfgs[cfg_index].series.push({
        name: line,
        data: [],
        type: series_type,
    });
    return (last_series_index + 1);
}

$.PlotLineSummer = function(title, line, dot, date, col, is_single) {
    setChart(title, line, col, is_single, 'line', true);
    let index = getSeriesIndex(title, line, 'line');
    _Chart.add(index, [date, dot]);
    _Chart.update(_Cfgs);
}

$.PlotBarSummer = function(title, line, dot, date, col, is_single) {
    setChart(title, line, col, is_single, 'column', true);
    let index = getSeriesIndex(title, line, 'column');
    _Chart.add(index, [date, dot]);
    _Chart.update(_Cfgs);
}

$.PlotPieSummer = function(title, line, data, col, is_single) {
    let chart = setChart(title, line, col, is_single, 'pie', false);
    chart.series[0].data = data;
    _Chart.update(_Cfgs);
}

function main() {
    let count = 0;
    while (true) {
        Sleep(1000)
        let ticker = exchange.GetTicker()
        if (!ticker) {
            continue;
        }
        let diff = ticker.Sell - ticker.Buy;
        let time = new Date().getTime()
        $.PlotLineSummer('Handicap chart', 'Buy one', ticker.Buy, time, 12, true);
        $.PlotLineSummer('Handicap chart', 'Sell one', ticker.Sell, time, 12, true);
        $.PlotBarSummer('Price Difference Chart', 'Spread1', diff, time, 12, true);
        $.PlotBarSummer('Price Difference Chart', 'Spread2', diff * 2, time, 12, true);
        $.PlotLineSummer('Handicap chart2', 'Buy one', ticker.Buy, time, 8, true);
        $.PlotLineSummer('Handicap chart2', 'Sell one', ticker.Sell, time, 8, true);
        $.PlotLineSummer('Handicap chart3', 'Buy one', ticker.Buy, time, 4, true);
        $.PlotLineSummer('Handicap chart3', 'Sell one', ticker.Sell, time, 4, true);
        let data = [["A", 25 + (++count)],
                    ["B", 25 - count],
                    ["C", 25],
                    ["D", 25]];
        $.PlotPieSummer('Pie chart1', 'Pie chart1', data, 6, true);
        $.PlotPieSummer('Pie chart2', 'Pie chart2', data, 6, true);
    }
}
```

> Detail

https://www.fmz.com/strategy/404014

> Last Modified

2023-08-09 13:04:14
