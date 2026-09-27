
> Name

Weekly-Quarter-Price-Difference-Drawing-Plugin

> Author

小草

> Strategy Description

Can plot the price difference chart between quarterly and this week for hedging analysis

The plug-in can be started with one click on the trading terminal, free of charge, and convenient for manual trading. Detailed introduction:https://www.fmz.com/digest-topic/5051



> Source (javascript)

``` javascript

var chart = { 
    __isStock: true,    
    title : { text : 'Spread analysis chart'},                     
    xAxis: { type: 'datetime'},                 
    yAxis : {                                        
        title: {text: 'Spread'},                   
        opposite: false,                             
    },
    series : [                    
        {name : "diff", data : []}, 

    ]
}
function main() {
    exchange.SetContractType('quarter')
    var recordsA = exchange.GetRecords(PERIOD_M5)
    exchange.SetContractType('this_week')
    var recordsB = exchange.GetRecords(PERIOD_M5)
    
    for(var i=0;i<Math.min(recordsA.length,recordsB.length);i++){
        var diff = recordsA[recordsA.length-Math.min(recordsA.length,recordsB.length)+i].Close - recordsB[recordsB.length-Math.min(recordsA.length,recordsB.length)+i].Close
        chart.series[0].data.push([recordsA[recordsA.length-Math.min(recordsA.length,recordsB.length)+i].Time, diff])
    }
    return chart
}
```

> Detail

https://www.fmz.com/strategy/187755

> Last Modified

2020-03-24 10:52:17
