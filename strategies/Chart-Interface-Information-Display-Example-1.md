
> Name

Chart-Interface-Information-Display-Example-1

> Author

太极

> Strategy Description

11111111



> Source (javascript)

``` javascript
//==========================================
//API: Chart Simple example of function usage (plotting feature))
var chart = { // this chart At/InJS In the language, it is an object, in useChart Before the function, we need to declare an object variable to configure the chartchart.
  __isStock: true,                                    // Mark whether it is a general chart. If interested, you can change it to false and run it.
  tooltip: {xDateFormat: '%Y-%m-%d %H:%M:%S, %A'},    // Zoom tool
  title : { text : 'Spread analysis chart
  rangeSelector: {                                    // Selection range
      buttons:  [{type: 'hour',count: 1, text: '1h'}, {type: 'hour',count: 3, text: '3h'}, {type: 'hour', count: 8, text: '8h'}, {type: 'all',text: 'All'}],
      selected: 0,
      inputEnabled: false
  },
  xAxis: { type: 'datetime'},                         // Horizontal axis of the coordinate system, i.e., x-axis. The currently set type is: Time
  yAxis : {                                           // coordinate axis vertical axis i.e., y-axis, default value adjusts with data size.
      title:{text: 'Price difference'}, // title
      opposite:false,                                // Whether to enable the right vertical axis
  },
  series : [                                          // Data series, this attribute saves each data series (line, candlestick chart, label, etc...)
      {name:"Exchange 0",id:"0,Buy",color:'#FF3030',data:[]}, //The index is 0, and the data array stores the data of the index series
      {name:"Exchange 1",id:"1,Buy",dashStyle:'shortdash',data:[]}, //The index is 1, dashStyle is set: 'shortdash', that is: set the dotted line.
      {name:"exchange2",id:"2,Buy",color:'#912CEE',data:[]},
      //RGBColor comparison table  http://www.114la.com/other/rgb.htm
  ]
};
//==========================================
//Get current time
function getNowFormatDate() {
    var date = new Date();
    var seperator1 = "-";
    var seperator2 = ":";
    var month = date.getMonth() + 1;
    var strDate = date.getDate();
    if (month >= 1 && month <= 9) {
        month = "0" + month;
    }
    if (strDate >= 0 && strDate <= 9) {
        strDate = "0" + strDate;
    }
    var currentdate = date.getFullYear()+seperator1+month+seperator1+strDate+" "+date.getHours()+seperator2+date.getMinutes()+seperator2+date.getSeconds();
    return currentdate;
}


function main() {
//==========================================
    //Drawing   https://www.botvs.com/bbs-topic/581
    var ObjChart = Chart(chart);  // Call Chart Function to initialize the chart.
    ObjChart.reset();           // Clear
    while(true){
        var nowTime = new Date().getTime();   //Get timestamp,
        var Buy_0 = _C(exchanges[0].GetTicker).Buy;  //Get platform0Market Data Buy Price 1
        var Buy_1 = _C(exchanges[1].GetTicker).Buy; //Get platform1Market Data Buy Price 1
        var Buy_2 = _C(exchanges[2].GetTicker).Buy; //Get platform2Market Data Buy Price 1
        ObjChart.add([0, [nowTime,Buy_0]]); // Use timestamp asXValue, buy-one price asYValue passed in index0 data series.
        ObjChart.add([1, [nowTime,Buy_1]]); // Same as above.
        ObjChart.add([2, [nowTime,Buy_2]]); // Same as above.
        ObjChart.update(chart);                  // Update the chart to display.
        Sleep(2000);
    }
//==========================================

}

```

> Detail

https://www.fmz.com/strategy/36026

> Last Modified

2017-02-18 15:29:31
