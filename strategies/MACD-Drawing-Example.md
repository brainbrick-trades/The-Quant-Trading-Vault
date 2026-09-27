
> Name

MACD-Drawing-Example

> Author

发明者量化-小小梦





> Source (javascript)

``` javascript
/*backtest
start: 2019-05-13 00:00:00
end: 2019-06-12 00:00:00
period: 1d
exchanges: [{"eid":"Futures_OKCoin","currency":"BTC_USD"}]
*/

var preTime = 0;
var ChartObj = null;
function main(){
    LogReset(1);
    ChartObj = Chart(null);
    ChartObj.reset();
    var records = null;
    var MACD = null;
    exchange.SetContractType("quarter");
    // Log(exchange.GetUSDCNY());
    // exchange.SetRate(exchange.GetUSDCNY());
    exchange.SetRate(1);
    ChartObj = $.GetCfg();
    
    // Handle indicator axis------------------------
    ChartObj.yAxis = [{
            title: {text: 'KLine'},//Title
            style: {color: '#4572A7'},//Style 
            opposite: false  //Generate right Y-axis
        },
        {
            title:{text: "Indicator axis"},
            opposite: true,  //Generate right Y-axis  ceshi
        }
    ];
    // Initialize indicator lines
    while(!records || records.length < 30){
        records = _C(exchange.GetRecords);
        LogStatus("records.length:", records.length);
        Sleep(1000);
    }
    
    $.PlotRecords(records, 'OKfutures');
    $.PlotLine('dif', 0, records[records.length - 1].Time);
    $.PlotLine('dea', 0, records[records.length - 1].Time);
    var chart = $.PlotLine('macd', 0, records[records.length - 1].Time);
    // Modify indicator line axisYaxis
    for(var key in ChartObj.series){
        if(ChartObj.series[key].name == 'dif' || ChartObj.series[key].name == 'dea' || ChartObj.series[key].name == 'macd'){
            ChartObj.series[key].yAxis = 1;
        }
    }
    chart.update(ChartObj);
    chart.reset();
    
    while(true){
        records = _C(exchange.GetRecords);
        if(records.length > 50){
            $.PlotRecords(records, 'OKfutures');
            MACD = TA.MACD(records);
            var dif = MACD[0];
            var dea = MACD[1];
            var macd = MACD[2];
            if(preTime !== records[records.length - 1].Time){
                $.PlotLine('dif', dif[dif.length - 2], records[records.length - 2].Time);
                $.PlotLine('dea', dea[dea.length - 2], records[records.length - 2].Time);
                $.PlotLine('macd', macd[macd.length - 2], records[records.length - 2].Time);
                
                $.PlotLine('dif', dif[dif.length - 1], records[records.length - 1].Time);
                $.PlotLine('dea', dea[dea.length - 1], records[records.length - 1].Time);
                $.PlotLine('macd', macd[macd.length - 1], records[records.length - 1].Time);
                
                preTime = records[records.length - 1].Time;
            }else{
                $.PlotLine('dif', dif[dif.length - 1], records[records.length - 1].Time);
                $.PlotLine('dea', dea[dea.length - 1], records[records.length - 1].Time);
                $.PlotLine('macd', macd[macd.length - 1], records[records.length - 1].Time);
            }
        }
        LogStatus("records.length:", records.length, records[records.length - 1]);
        // Log(records[records.length - 1]);
        Sleep(1000);
    }
}
```

> Detail

https://www.fmz.com/strategy/151972

> Last Modified

2020-02-27 14:09:37
