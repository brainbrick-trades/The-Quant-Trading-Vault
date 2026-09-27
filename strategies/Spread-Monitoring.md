
> Name

Spread-Monitoring

> Author

Zero

> Strategy Description

Only supports two exchanges, customizable price difference types, and 2.77 custodian custom charting features

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|AType|0|Main platform price type: Last traded price | Best bid price | Best ask price|
|BType|0|Sub-platform price type: Last transaction price|Buy price|Sell price|
|Interval|2000|Error retry interval (milliseconds)|
|TickInterval|2000|Detection frequency (milliseconds)|
|EnableCR|false|Custom exchange rate|
|USDCNY|false|USDCNY|
|NormalDiff|0.1|Ordinary spread|
|HighDiff|0.3|Higher spread|




|Button|Default|Description|
|----|----|----|
|Reset data|__button__|@|


> Source (javascript)

``` javascript

var __lastDiff = 0;
var __AType = ["Last", "Buy", "Sell"][AType];
var __BType = ["Last", "Buy", "Sell"][BType];

var cfg = {
			tooltip: {xDateFormat: '%Y-%m-%d %H:%M:%S, %A'},
			title : { text : 'Spread analysis chart'},
			rangeSelector: {
                buttons:  [{type: 'hour',count: 1, text: '1h'}, {type: 'hour',count: 3, text: '3h'}, {type: 'hour', count: 8, text: '8h'}, {type: 'all',text: 'All'}],
                selected: 0,
                inputEnabled: false
            },
			xAxis: { type: 'datetime'},
			yAxis : {
				plotLines : [{
					value : 0.0,
					color : 'black',
					dashStyle : 'shortdash',
					width : 3,
				}, {
					value : NormalDiff,
					color : 'green',
					dashStyle : 'shortdash',
					width : 1,
				}, {
					value : HighDiff,
					color : 'red',
					dashStyle : 'shortdash',
					width : 1,
				},{
					value : -NormalDiff,
					color : 'green',
					dashStyle : 'shortdash',
					width : 1,
				}, {
					value : -HighDiff,
					color : 'red',
					dashStyle : 'shortdash',
					width : 1,
				}]
			},
			series : [{
				name : 'Price difference',
				data : [],
				tooltip: {
					valueDecimals: 2
				}
			}]
		};
function _N(v, precision) {
    if (typeof(precision) != 'number') {
        precision = 4;
    }
    var d = parseFloat(v.toFixed(Math.max(10, precision+5)));
    s = d.toString().split(".");
    if (s.length < 2 || s[1].length <= precision) {
        return d;
    }

    var b = Math.pow(10, precision);
    return Math.floor(d*b)/b;
}

function GetTicker(e) {
    if (typeof(e) == 'undefined') {
        e = exchange;
    }
    var ticker;
    while (!(ticker = e.GetTicker())) {
        Sleep(Interval);
    }
    return ticker;
}

function onTick() {
    var tickerA = GetTicker(exchanges[0]);
    var tickerB = GetTicker(exchanges[1]);
    var diff = _N(tickerA[__AType] - tickerB[__BType]);
    LogStatus(exchanges[0].GetName(), _N(tickerA[__AType]), exchanges[1].GetName(), _N(tickerB[__BType]), "Spread:", diff);
    if (__lastDiff != 0) {
        if (Math.abs(Math.abs(diff) - Math.abs(__lastDiff)) > 200) {
            return;
        }
    }
    if (diff != __lastDiff) {
        // addAdd data toseries, Parameter format is[seriesSerial number, Data];
        cfg.yAxis.plotLines[0].value=diff;
        cfg.subtitle={text:'Current spread:' + diff};
        __chart.update(cfg);
        __chart.add([0, [new Date().getTime(), diff]]);
        __lastDiff = diff;
    }
 }

function main() {
    if (parseFloat(Version()) < 2.77) {
        throw "Only supports version 2.77 or above";
    }
    if (exchanges.length != 2) {
        throw "Only supports hedging between two exchanges";
    }
    // Pass toChartFunction must be a struct independent of the context(ConformHighStocksRules, Detailed parametersHighStocksUsage Method)
    __chart = Chart(cfg);
	// reset Clear all previous chart information
	// __chart.reset();
    if (EnableCR) {
        for (var i = 0; i < exchanges.length; i++) {
            var rate = exchanges[i].GetRate();
            if (exchanges[i].GetBaseCurrency() != 'CNY') {
                exchanges[i].SetRate(USDCNY);
                Log("Modify", exchanges[i].GetName(), "Exchange rate", rate, "is", USDCNY);
            }
            var eName = exchanges[i].GetName();
            if (eName == "Futures_BitVC") {
                exchanges[i].SetContractType("week");
            }
        }
    }
    Log(exchanges[0].GetName()+"."+__AType, "-", exchanges[1].GetName()+"."+__BType, 'The spread is displayed on the chart as profit');
    TickInterval = Math.max(TickInterval, 50);
    Interval = Math.max(Interval, 50);
    while (true) {
        onTick();
        Sleep(TickInterval);
        if (GetCommand() === 'Reset data') {
            LogReset();
            LogProfitReset();
            __chart.reset();
            Log("Data reset successful");
        }
    }
}
```

> Detail

https://www.fmz.com/strategy/1340

> Last Modified

2017-09-13 22:28:04
