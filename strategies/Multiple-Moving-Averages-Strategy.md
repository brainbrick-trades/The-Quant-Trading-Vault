
> Name

Multiple-Moving-Averages-Strategy

> Author

发明者量化-小小梦



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|ma60|60|60daily moving average|
|ma10|10|10daily moving average|
|ma5|5|5daily moving average|


> Source (javascript)

``` javascript
// The following is the test code 
/*- Status needs to be declared in the main policy when using the template
var TASK_IDLE = 0;
var TASK_OPEN_LONG = 1;
var TASK_OPEN_SHORT = 2;
var TASK_ADD = 3;
var TASK_ST = 4;
var TASK_COVER = 5;
*/

// Global Variables
var currency0 = exchanges[0].GetCurrency();
var ChartObj = null;
var TASK_IDLE = 0;
var TASK_OPEN_LONG = 1;
var TASK_OPEN_SHORT = 2;
var TASK_ADD = 3;
var TASK_ST = 4;
var TASK_COVER = 5;
var IDLE = 11;
var LONG = 22;
var SHORT = 33;
var perRecordsTime = 0;

function onTick1() {
    // ObtainKLine Data
    var nowTime = new Date().getTime();
    var records = _C(exchanges[0].GetRecords);
    if(records.length < Math.abs(ma60, ma10, ma5)){
        return $.TaskCmd(TASK_IDLE);
    }
    
    var ma60_line = TA.MA(records, ma60);
    var ma10_line = TA.MA(records, ma10);
    var ma5_line = TA.MA(records, ma5);
    
    // $.AddData = function(index, dataKey, dataValue)
    
    // draw chart
    $.PlotRecords(records, currency0);
    $.PlotLine('ma' + ma60, ma60_line[ma60_line.length - 1], records[records.length - 1].Time);
    $.PlotLine('ma' + ma10, ma10_line[ma10_line.length - 1], records[records.length - 1].Time);
    $.PlotLine('ma' + ma5, ma5_line[ma5_line.length - 1], records[records.length - 1].Time);
    
    if(records[records.length - 1].Time !== perRecordsTime){
        isTradeonThieBar = false;
        perRecordsTime = records[records.length - 1].Time;
    }
    
    if($.GetTaskState(exchanges[0].GetName(), exchanges[0].GetLabel()) == IDLE && records[records.length - 2].Close > ma60_line[ma60_line.length - 2] && ma10_line[ma10_line.length - 2] > ma60_line[ma60_line.length - 2] && ma5_line[ma5_line.length - 2] > ma60_line[ma60_line.length - 2] && 
        ma10_line[ma10_line.length - 3] > ma5_line[ma5_line.length - 3] && ma10_line[ma10_line.length - 2] < ma5_line[ma5_line.length - 2]){
        // Tag
        return $.TaskCmd(TASK_OPEN_LONG, 0.5);
    }else if($.GetTaskState(exchanges[0].GetName(), exchanges[0].GetLabel()) == IDLE && records[records.length - 2].Close < ma60_line[ma60_line.length - 2] && ma10_line[ma10_line.length - 2] < ma60_line[ma60_line.length - 2] && ma5_line[ma5_line.length - 2] < ma60_line[ma60_line.length - 2] && 
        ma10_line[ma10_line.length - 3] < ma5_line[ma5_line.length - 3] && ma10_line[ma10_line.length - 2] > ma5_line[ma5_line.length - 2]){
        // Tag
        isTradeonThieBar = true;
        return $.TaskCmd(TASK_OPEN_SHORT, 0.5);
    }
    
    if (($.GetTaskState(exchanges[0].GetName(), exchanges[0].GetLabel()) == LONG && records[records.length - 2].Close < ma5_line[ma5_line.length - 2]) || ($.GetTaskState(exchanges[0].GetName(), exchanges[0].GetLabel()) == SHORT && records[records.length - 2].Close > ma5_line[ma5_line.length - 2])) {
        // Tag
        isTradeonThieBar = true;
        return $.TaskCmd(TASK_COVER);
    } 

    return $.TaskCmd(TASK_IDLE);
}

function main() {
    LogReset(1);
    ChartObj = Chart(null);
    ChartObj.reset();
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
    var records = null;
    while(!records || records.length < 60){
        records = _C(exchange.GetRecords);
        LogStatus("records.length:", records.length);
        Sleep(1000);
    }

    $.PlotRecords(records, currency0);
    $.PlotLine('ma' + ma60, 0, records[records.length - 1].Time);
    $.PlotLine('ma' + ma10, 0, records[records.length - 1].Time);
    var chart = $.PlotLine('ma' + ma5, 0, records[records.length - 1].Time);
    
    chart.update(ChartObj);
    chart.reset();
    
    $.Relation_Exchange_onTick(exchanges[0], onTick1);
    $.Trend();  // No need to pass parameters.
}
```

> Detail

https://www.fmz.com/strategy/47144

> Last Modified

2017-07-20 11:07:24
