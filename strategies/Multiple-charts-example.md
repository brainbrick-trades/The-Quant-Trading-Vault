
> Name

Multiple-charts-example

> Author

小草

> Strategy Description

An example of displaying multiple charts, where multiple charts can share one row, and the width of the chart can be set.
Supports basic charts of HighCharts and HighStocks, such as line charts, histograms, column charts, pie charts, candlestick charts, etc. Please check the highchart official website for details. You can use this example with slight changes.



> Source (javascript)

``` javascript
var tradeHistory = {buyData:{amount:0, money:0}, sellData:{amount:0, money:0}, a:0, b:0, c:0, d:0, total:0}
var updateB = 0
var lastNet = 0
var updateD = 0
if(_G('tradeHistory')){
    tradeHistory = _G('tradeHistory')
}
function getDepth(){
    var asks = []
    var bids = []
    var temp = 0
    var depth = JSON.parse(HttpQuery('https://api.binance.com/api/v1/depth?symbol=BTCUSDT'))
    if(!depth){
        return false
    }
    depth.bids.reverse()
    for(i=0;i<depth.bids.length;i++){
        temp += parseFloat(depth.bids[i][1])
    }
    for(i=0;i<depth.bids.length;i++){
        temp -= parseFloat(depth.bids[i][1])
        bids.push([parseFloat(depth.bids[i][0]), temp])
    }
    temp = 0
    for(i=0;i<depth.asks.length;i++){
        temp += parseFloat(depth.asks[i][1])
        asks.push([parseFloat(depth.asks[i][0]), temp])
    }
    return {asks:asks,bids:bids}
    
}
var chartA = {
    __isStock: false,
    extension: {
        layout: 'single',
        col: 6, // Specify the cell value occupied by the width, total value is12
        height: 500,
    },
    title: {
        text: 'Trading volume distribution chart'
    },
    xAxis: [{
        title: { text: 'Data' },
        alignTicks: false
    }, {
        title: { text: 'Histogram' },
        alignTicks: false,
        opposite: true
    }],

    yAxis: [{
        title: { text: 'Data' }
    }, {
        title: { text: 'Histogram' },
        opposite: true
    }],

    series: [{
        name: 'Histogram',
        type: 'histogram',
        xAxis: 1,
        yAxis: 1,
        baseSeries: 's1',
        zIndex: -1
    },{
        name: 'Data',
        type: 'scatter',
        data: [],
        id: 's1',
        marker: {
            radius: 1.5
        }
    }]
};
var chartB = {
    extension: {
        layout: 'single', // Do not participate in grouping; display separately, default is grouped 'group'
        col: 6,
        height: 300, // Specify height
    },
    credits: {
        enabled: false
    },
    title: {
        text: 'Net buying funds'
    },
    xAxis: {
        type: 'datetime'
    },
    series: [{
        name: 'net purchase',
        type: 'column',
        data: []
    }],
}
var chartC = {
    extension: {
        layout: 'single', // Do not participate in grouping; display separately, default is grouped 'group'
        col: 6,
        height: 300,      // Specify the height // The unit value of the specified width, the total value is12
    },
    title: {
        text: 'transaction price'
    },
    xAxis: {
        type: 'datetime'
    },
    series: [{
        name: 'last',
        data: [],
    }]
}
var chartD = {
    __isStock: false,
    extension: {
        layout: 'single', // Do not participate in grouping; display separately, default is grouped 'group'
        col: 6,
        height: 500,      // Specify the height // The unit value of the specified width, the total value is12
    },
    chart: {
        type: 'area',
        zoomType: 'xy'
    },
    title: {
        text: 'BTC-USDTDepth'
    },
    xAxis: {
        minPadding: 0,
        maxPadding: 0,
        plotLines: [{
            color: '#888',
            value: 0.1523,
            width: 1,
            label: {
                text: 'Actual price',
                rotation: 90
            }
        }],
        title: {
            text: 'Price'
        }
    },
    yAxis: [{
        min:0,
        lineWidth: 1,
        gridLineWidth: 1,
        title: null,
        tickWidth: 1,
        tickLength: 5,
        tickPosition: 'inside',
        labels: {
            align: 'left',
            x: 8
        }
    }, {
        opposite: true,
        linkedTo: 0,
        lineWidth: 1,
        gridLineWidth: 0,
        title: null,
        tickWidth: 1,
        tickLength: 5,
        tickPosition: 'inside',
        labels: {
            align: 'right',
            x: -8
        }
    }],
    plotOptions: {
        area: {
            fillOpacity: 0.2,
            lineWidth: 1,
            step: 'center'
        }
    },
    tooltip: {
        headerFormat: '<span style="font-size=10px;">Price: {point.key}</span><br/>',
        valueDecimals: 2
    },
    series: [{
        name: 'Bids',
        data: [],
        color: '#03a7a8'
    }, {
        name: 'Asks',
        data: [],
        color: '#fc5857'
    }]
};
var chartE = {
    __isStock: false,
    extension: {
        layout: 'single', // Do not participate in grouping; display separately, default is grouped 'group'
        col: 6,
        height: 500,      // Specify the height // The unit value of the specified width, the total value is12
    },
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: 0,
        plotShadow: false
    },
    title: {
        text: 'Transaction quantity<br>distribution<br>',
        align: 'center',
        verticalAlign: 'middle',
        y: 40
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
        pie: {
            dataLabels: {
                enabled: true,
                distance: -50,
                style: {
                    fontWeight: 'bold',
                    color: 'white'
                }
            },
            startAngle: -90,
            endAngle: 90,
            center: ['50%', '75%'],
            size: '110%'
        }
    },
    series: [{
        type: 'pie',
        name: 'Proportion',
        innerSize: '50%',
        data: []
    }]
}
var chartF = {
    extension: {
        layout: 'single', // Do not participate in grouping; display separately, default is grouped 'group'
        col: 6,
        height: 300,      // Specify the height // The unit value of the specified width, the total value is12
    },
    title: {
        text: 'Total Net Buys'
    },
    xAxis: {
        type: 'datetime'
    },
    series: [{
        name: 'last',
        data: [],
    }]
}
var chart = Chart([chartB,chartC,chartD,chartA,chartF,chartE]);
//chart.reset()
function main() {
    var client = Dial("wss://stream.binance.com:9443/ws/" + 'btcusdt' + "@trade", 60)
    var updateTime = new Date().getTime()
    while(true){
        var trade = JSON.parse(client.read())
        if(trade.m){
            tradeHistory.sellData.amount += parseFloat(trade.q)
            tradeHistory.sellData.money += parseFloat(trade.q) * parseFloat(trade.p)
        }else{
            tradeHistory.buyData.amount += parseFloat(trade.q)
            tradeHistory.buyData.money += parseFloat(trade.q) * parseFloat(trade.p)
        }
        var buyNet = _N(tradeHistory.buyData.money - tradeHistory.sellData.money, 3)
        var tradeAmount = _N(parseFloat(trade.q),2)>1 ? 1 : _N(parseFloat(trade.q),2)
        if(parseFloat(trade.q)<0.01){
            tradeHistory.a += 1
        }else if(parseFloat(trade.q)<0.1){
            tradeHistory.b += 1
        }else if(parseFloat(trade.q)<1){
            tradeHistory.c += 1
        }else{
            tradeHistory.d += 1
        }
        tradeHistory.total +=1
        chartE.series[0].data = [
            ['Less Than0.01', _N(tradeHistory.a/tradeHistory.total,4)],
            ['Less Than0.1', _N(tradeHistory.b/tradeHistory.total,4)],
            ['Less Than1', _N(tradeHistory.c/tradeHistory.total,4)],
            ['Greater than1', _N(tradeHistory.d/tradeHistory.total,4)],
        ]
        if(tradeAmount>0.01){
            while(chartA.series[1].data.length>2000){
                chartA.series[1].data.shift()
            }
            chartA.series[1].data.push(tradeAmount)
        }
        if(Date.now() - updateB > 60*1000){
            chart.add(0,[Date.now(), _N(buyNet-lastNet,2)])
            lastNet = buyNet
            updateB = Date.now()
            chart.add(1, [Date.now(), _N(parseFloat(trade.p),2)])
            chart.add(6, [Date.now(), _N(buyNet,2)])
        }else{
            chart.add(0, [Date.now(), _N(buyNet-lastNet,2)], -1)
            chart.add(1, [Date.now(), _N(parseFloat(trade.p),2)], -1)
            chart.add(6, [Date.now(), _N(buyNet,2)],-1)
        }
        if(Date.now() - updateD > 6*1000){
            var depth = getDepth()
            if(!depth){
                continue
            }
            chartD.series[0].data = depth.bids
            chartD.series[1].data = depth.asks
            updateD = Date.now()
        }
        chart.update([chartB,chartC,chartD,chartA,chartF,chartE])
    }
        
}
```

> Detail

https://www.fmz.com/strategy/136056

> Last Modified

2019-07-03 16:13:56
