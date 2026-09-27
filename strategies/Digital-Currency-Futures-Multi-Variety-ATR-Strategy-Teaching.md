
> Name

Digital-Currency-Futures-Multi-Variety-ATR-Strategy-Teaching

> Author

发明者量化-小小梦

> Strategy Description

Related articles:https://www.fmz.com/digest-topic/8726

The strategy is transplanted from a simple Mai language strategy:
```
TR:=MAX(MAX((H-L),ABS(REF(C,1)-H)),ABS(REF(C,1)-L));
ATR:=EMA(TR,LENGTH2);

MIDLINE^^EMA((H + L + C)/3,LENGTH1);
UPBAND^^MIDLINE + N*ATR;
DOWNBAND^^MIDLINE - N*ATR;


BKVOL=0 AND C>=UPBAND AND REF(C,1)<REF(UPBAND,1),BPK;
SKVOL=0 AND C<=DOWNBAND AND REF(C,1)>REF(DOWNBAND,1),SPK;

BKVOL>0 AND C<=MIDLINE,SP(BKVOL);
SKVOL>0 AND C>=MIDLINE,BP(SKVOL);
// stop loss
// stop loss
C>=SKPRICE*(1+SLOSS*0.01),BP;
C<=BKPRICE*(1-SLOSS*0.01),SP;
AUTOFILTER;
```

For multi-currency design, parameters are designed as a JSON string:
```
var params = '[{
        "symbol" : "swap",
        "period" : 86400,
        "stopLoss" : 0.07,
        "atrPeriod" : 10,
        "emaPeriod" : 10,
        "trackRatio" : 1,
        "openRatio" : 0.1
    }, {
        "symbol" : "swap",
        "period" : 86400,
        "stopLoss" : 0.07,
        "atrPeriod" : 10,
        "emaPeriod" : 10,
        "trackRatio" : 1,
        "openRatio" : 0.1
    }]'
```

The strategy uses a template library: Cryptocurrency Futures Trading Library (Test Version))

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|params||Parameters|
|onlyOne|true|Run Single Product Only|
|symbol|swap|Futures contract code|
|period|86400|KLine Period Seconds|
|stopLoss|0.07|stop loss|
|atrPeriod|10|ATRtimeframe|
|emaPeriod|10|EMAtimeframe|
|trackRatio|true|Orbit coefficient|
|openRatio|0.1|Opening Coefficient|


> Source (javascript)

``` javascript
/*backtest
start: 2021-09-01 00:00:00
end: 2022-01-06 00:00:00
period: 1d
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"ETH_USDT","balance":1000000},{"eid":"Futures_Binance","currency":"LTC_USDT"}]
args: [["params","[{         \"symbol\" : \"swap\",         \"period\" : 86400,         \"stopLoss\" : 0.07,         \"atrPeriod\" : 10,         \"emaPeriod\" : 20,         \"trackRatio\" : 2,         \"openRatio\" : 0.1     }, {         \"symbol\" : \"swap\",         \"period\" : 86400,         \"stopLoss\" : 0.07,         \"atrPeriod\" : 10,         \"emaPeriod\" : 20,         \"trackRatio\" : 2,         \"openRatio\" : 0.1     }]"]]
*/

var arrParam = onlyOne ? [{"symbol": symbol, "period": period, "stopLoss": stopLoss, "atrPeriod": atrPeriod, "emaPeriod": emaPeriod, "trackRatio": trackRatio, "openRatio": openRatio}] : JSON.parse(params)

function createChartConfig(symbol, atrPeriod, emaPeriod, index) {
    var chart = {                                        
        __isStock: true,    
        extension: {
                layout: 'single', 
                height: 600, 
        },
        title : { text : symbol},                       
        xAxis: { type: 'datetime'},           
        series : [                                          
            {                                      
                type: 'candlestick',    // KLine Data Series                         
                name: symbol,   
                id: symbol + "-" + index,
                data: []                                           
            }, {                                      
                type: 'line',           // EMA
                name: symbol + ',EMA:' + emaPeriod,          
                data: [],               
            }, {
                type: 'line',           // upBand
                name: symbol + ',upBand' + atrPeriod,
                data: []
            }, {
                type: 'line',           // downBand
                name: symbol + ',downBand' + atrPeriod,
                data: []
            }, {
                type: 'flags',
                onSeries: symbol + "-" + index,
                data: [],
            }
        ]
    }
    return chart
}

function process(e, kIndex, c) {
    var r = e.GetRecords(e.param.period)
    if (!r || r.length < e.param.atrPeriod + 2 || r.length < e.param.emaPeriod + 2) {
        return 
    }

    var atr = TA.ATR(r, e.param.atrPeriod)
    var arrAvgPrice = []
    _.each(r, function(bar) {
        arrAvgPrice.push((bar.High + bar.Low + bar.Close) / 3)
    })
    var midLine = TA.EMA(arrAvgPrice, e.param.emaPeriod)
    var upBand = []
    var downBand = [] 
    _.each(midLine, function(mid, index) {
        if (index < e.param.emaPeriod - 1 || index < e.param.atrPeriod - 1) {
            upBand.push(NaN)
            downBand.push(NaN)
            return 
        }
        upBand.push(mid + e.param.trackRatio * atr[index])
        downBand.push(mid - e.param.trackRatio * atr[index])
    })

    // Drawing
    for (var i = 0 ; i < r.length ; i++) {
        if (r[i].Time == e.state.lastBarTime) {
            // Update
            c.add(kIndex, [r[i].Time, r[i].Open, r[i].High, r[i].Low, r[i].Close], -1)
            c.add(kIndex + 1, [r[i].Time, midLine[i]], -1)
            c.add(kIndex + 2, [r[i].Time, upBand[i]], -1)
            c.add(kIndex + 3, [r[i].Time, downBand[i]], -1)
        } else if (r[i].Time > e.state.lastBarTime) {
            // Add
            e.state.lastBarTime = r[i].Time
            c.add(kIndex, [r[i].Time, r[i].Open, r[i].High, r[i].Low, r[i].Close])  
            c.add(kIndex + 1, [r[i].Time, midLine[i]])
            c.add(kIndex + 2, [r[i].Time, upBand[i]])
            c.add(kIndex + 3, [r[i].Time, downBand[i]])
        }
    }

    // Check Positions
    var pos = e.GetPosition()
    if (!pos) {
        return 
    }
    var holdAmount = 0
    var holdPrice = 0
    if (pos.length > 1) {
        throw "Detect both long and short positions simultaneously!"
    } else if (pos.length != 0) {
        holdAmount = pos[0].Type == PD_LONG ? pos[0].Amount : -pos[0].Amount
        holdPrice = pos[0].Price
    }

    if (e.state.preBar == -1) {
        e.state.preBar = r[r.length - 1].Time
    }
    // Check Signals
    if (e.state.preBar != r[r.length - 1].Time) {   // Closing Price Model
        if (holdAmount <= 0 && r[r.length - 3].Close < upBand[upBand.length - 3] && r[r.length - 2].Close > upBand[upBand.length - 2]) {   // Closing price crosses above the upper band
            if (holdAmount < 0) {   // Hold short position, close
                Log(e.GetCurrency(), "Close Short Position", "#FF0000")
                $.CoverShort(e, e.param.symbol, Math.abs(holdAmount))
                c.add(kIndex + 4, {x: r[r.length - 2].Time, color: 'red', shape: 'flag', title: 'Flat', text: "Close Short Position"})
            }
            // open long
            Log(e.GetCurrency(), "Open long position", "#FF0000")
            $.OpenLong(e, e.param.symbol, 10)
            c.add(kIndex + 4, {x: r[r.length - 2].Time, color: 'red', shape: 'flag', title: 'Many', text: "Open long position"})
        } else if (holdAmount >= 0 && r[r.length - 3].Close > downBand[downBand.length - 3] && r[r.length - 2].Close < downBand[downBand.length - 2]) {  // Closing price crosses below the lower band
            if (holdAmount > 0) {   // Hold long position, close position
                Log(e.GetCurrency(), "Close Long Position", "#FF0000")
                $.CoverLong(e, e.param.symbol, Math.abs(holdAmount))
                c.add(kIndex + 4, {x: r[r.length - 2].Time, color: 'green', shape: 'flag', title: 'Flat', text: "Close Long Position"})
            }
            // open short
            Log(e.GetCurrency(), "Open short position", "#FF0000")
            $.OpenShort(e, e.param.symbol, 10)
            c.add(kIndex + 4, {x: r[r.length - 2].Time, color: 'green', shape: 'flag', title: 'Empty', text: "Open short position"})
        } else {
            // Close Position
            if (holdAmount > 0 && (r[r.length - 2].Close <= holdPrice * (1 - e.param.stopLoss) || r[r.length - 2].Close <= midLine[midLine.length - 2])) {   // Hold a long position, if the closing price is less than or equal to the midline, stop loss at the opening price
                Log(e.GetCurrency(), "Trigger mid-line or stop loss, close long position", "#FF0000")
                $.CoverLong(e, e.param.symbol, Math.abs(holdAmount))
                c.add(kIndex + 4, {x: r[r.length - 2].Time, color: 'green', shape: 'flag', title: 'Flat', text: "Close Long Position"})
            } else if (holdAmount < 0 && (r[r.length - 2].Close >= holdPrice * (1 + e.param.stopLoss) || r[r.length - 2].Close >= midLine[midLine.length - 2])) {  // Hold a short position, if the closing price is greater than or equal to the midline, stop loss at the opening price
                Log(e.GetCurrency(), "Trigger mid-line or stop loss, close short position", "#FF0000")
                $.CoverShort(e, e.param.symbol, Math.abs(holdAmount))
                c.add(kIndex + 4, {x: r[r.length - 2].Time, color: 'red', shape: 'flag', title: 'Flat', text: "Close Short Position"})
            }
        }
        e.state.preBar = r[r.length - 1].Time
    }
}

function main() {
    var arrChartConfig = []
    if (arrParam.length != exchanges.length) {
        throw "Parameters do not match the exchange object!"
    }
    var arrState = _G("arrState")
    _.each(exchanges, function(e, index) {
        if (e.GetName() != "Futures_Binance") {
            throw "This exchange is not supported!"
        }
        e.param = arrParam[index]
        e.state = {lastBarTime: 0, symbol: e.param.symbol, currency: e.GetCurrency()}
        if (arrState) {
            if (arrState[index].symbol == e.param.symbol && arrState[index].currency == e.GetCurrency()) {
                Log("Restore:", e.state)
                e.state = arrState[index]
            } else {
                throw "The restored data does not match the current settings!"
            }
        }
        e.state.preBar = -1   // Initial Settings-1
        e.SetContractType(e.param.symbol)
        Log(e.GetName(), e.GetLabel(), "Set Contract:", e.param.symbol)
        arrChartConfig.push(createChartConfig(e.GetCurrency(), e.param.atrPeriod, e.param.emaPeriod, index))
    })
    var chart = Chart(arrChartConfig)
    chart.reset()

    while (true) {
        _.each(exchanges, function(e, index) {
            process(e, index + index * 4, chart)
            Sleep(500)
        })      
    }
}

function onexit() {
    // Record e.state
    var arrState = []
    _.each(exchanges, function(e) {
        arrState.push(e.state)
    })
    Log("Record:", arrState)
    _G("arrState", arrState)
}

```

> Detail

https://www.fmz.com/strategy/339344

> Last Modified

2022-01-22 13:35:11
