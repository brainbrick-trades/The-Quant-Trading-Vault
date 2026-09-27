
> Name

js-R-Breaker

> Author

太极

> Strategy Description

R-Breaker



> Source (javascript)

``` javascript
NPeriod=2 //timeframe
f1=0.47   //Upper and lower top interval coefficients of the middle rail
f2=0.07   //Upper and lower interval coefficients of the middle rail
f3=0.25   //Upper and lower rail coefficients

//==========================================
//API: Chart Simple example of function usage (plotting feature))
var chart = { // this chart At/InJS In the language, it is an object, in useChart Before the function, we need to declare an object variable to configure the chartchart.
  __isStock: true,                                    // Mark whether it is a general chart. If interested, you can change it to false and run it.
  tooltip: {xDateFormat: '%Y-%m-%d %H:%M:%S, %A'},    // Zoom tool
  title : { text : 'Market Analysis Chart'}, // Title
  rangeSelector: {                                    // Selection range
      buttons:  [{type: 'hour',count: 1, text: '1h'}, {type: 'hour',count: 3, text: '3h'}, {type: 'hour', count: 8, text: '8h'}, {type: 'all',text: 'All'}],
      selected: 0,
      inputEnabled: false
  },
  xAxis: { type: 'datetime'},                         // Horizontal axis of the coordinate system, i.e., x-axis. The currently set type is: Time
  yAxis : {                                           // coordinate axis vertical axis i.e., y-axis, default value adjusts with data size.
      title:{text: 'Market Simulation'}, // Title
      opposite:false,                                // Whether to enable the right vertical axis
  },
  series : [                                          // Data series, this attribute saves each data series (line, candlestick chart, label, etc...)
      {name:"0X",id:"0",color:'#FF83FA',data:[]},
      {name:"1X",id:"1",color:'#FF3E96',dashStyle:'shortdash',data:[]},
      {name:"2X",id:"2",color:'#FF0000',data:[]},

      {name:"3X",id:"3",color:'#7D26CD',dashStyle:'shortdash',data:[]}, //

      {name:"4X",id:"4",color:'#2B2B2B',data:[]},
      {name:"5X",id:"5",color:'#707070',dashStyle:'shortdash',data:[]},
      {name:"6X",id:"6",color:'#778899',data:[]},

      {name:"7X",id:"7",color:'#0000CD',data:[]},

      //RGBColor comparison table  http://www.114la.com/other/rgb.htm
  ]
};

/*
//Pivot PointsStrategy
chart["series"][0]["name"]="resistance3:";
chart["series"][1]["name"]="resistance2:";
chart["series"][2]["name"]="resistance1:";

chart["series"][3]["name"]="Pivot Point:";

chart["series"][4]["name"]="support level1:";
chart["series"][5]["name"]="support level2:";
chart["series"][6]["name"]="support level3:";
chart["series"][6]["name"]="Current Price:";
*/
///*
//R-BreakerStrategy
chart["series"][0]["name"]="Bbreak_A1:";
chart["series"][1]["name"]="Ssetup_A2:";
chart["series"][2]["name"]="Senter_A3:";

chart["series"][4]["name"]="Benter_B1:";
chart["series"][5]["name"]="Sbreak_B2:";
chart["series"][6]["name"]="Bsetup_B3:";
chart["series"][7]["name"]="Current Price:";
//*/


var ObjChart = Chart(chart);  // Call Chart Function to initialize the chart.
ObjChart.reset();           // Clear
function onTick(e){
        var records = _C(e.GetRecords);  //Return aKLine History
        var ticker = _C(e.GetTicker);    //Return aTickerStructure
        var account = _C(e.GetAccount);  //Return to main exchange account information

        var High = TA.Highest(records, NPeriod, 'High'); //Highest Price
        var Close = TA.Lowest(records, NPeriod, 'Close');       //Closing price
        var Low = TA.Lowest(records, NPeriod, 'Low');   //Lowest Price

        /*
        //Pivot PointsStrategy
        //Aupper 7235 Amiddle 7259 Alower 7275 Bupper 7195 Bmiddle 7155 Blower 7179
        Pivot = (High+Close+Low)/3 //Pivot Point

        var Senter=High+2*(Pivot-Low)  //resistance3
        var Ssetup=Pivot+(High-Low)  //resistance2
        var Bbreak=2*Pivot-Low  //resistance1

        var Benter=2*Pivot-High  //support level1
        var Sbreak=Pivot-(High-Low)  //support level2
        var Bsetup=Low-2*(High-Pivot)  //support level3
        //Draw lines
        var nowTime = new Date().getTime(); //Get timestamp,
        ObjChart.add([0, [nowTime,_N(Senter,3)]]); //resistance3
        ObjChart.add([1, [nowTime,_N(Ssetup,3)]]); //resistance2
        ObjChart.add([2, [nowTime,_N(Bbreak,3)]]); //resistance1

        ObjChart.add([3, [nowTime,_N(Pivot,3)]]); //Pivot Point

        ObjChart.add([4, [nowTime,_N(Benter,3)]]);  //support level1
        ObjChart.add([5, [nowTime,_N(Sbreak,3)]]);  //support level2
        ObjChart.add([6, [nowTime,_N(Bsetup,3)]]);  //support level3

        ObjChart.add([7, [nowTime,_N(ticker.Last,3)]]); //Last transaction price

        ObjChart.update(chart);  // Update the chart to display.
        */


        ///*
        //R-BreakerStrategy
        //Aupper 7261.46 Amiddle 7246.76 Alower 7228.68 Bupper 7204.48 Bmiddle 7187.96 Blower 7173.26
        var Ssetup = High + f1 * (Close - Low);  //Amiddle
        var Bsetup = Low - f1 * (High - Close);  //Blower

        var Bbreak = Ssetup + f3 * (Ssetup - Bsetup);  //Aupper
        var Senter = ((1 + f2) / 2) * (High + Close) - f2 * Low;  //Alower

        var Benter = ((1 + f2) / 2) * (Low + Close) - f2 * High;  //Bupper
        var Sbreak = Bsetup - f3 * (Ssetup - Bsetup);  //Bmiddle
        //Draw lines
        var nowTime = new Date().getTime(); //Get timestamp,
        ObjChart.add([0, [nowTime,_N(Bbreak,3)]]); //Aupper
        ObjChart.add([1, [nowTime,_N(Ssetup,3)]]); //Amiddle
        ObjChart.add([2, [nowTime,_N(Senter,3)]]); //Alower

        //ObjChart.add([3, [nowTime,_N(Pivot,3)]]); //Pivot Point

        ObjChart.add([4, [nowTime,_N(Benter,3)]]);  //Bupper
        ObjChart.add([5, [nowTime,_N(Sbreak,3)]]);  //Bmiddle
        ObjChart.add([6, [nowTime,_N(Bsetup,3)]]);  //Blower

        ObjChart.add([7, [nowTime,_N(ticker.Last,3)]]); //Last transaction price

        ObjChart.update(chart);  // Update the chart to display.
        //*/

        Log('Aupper',_N(Bbreak,3),'Amiddle',_N(Ssetup,3),'Alower',_N(Senter,3),'Bupper',_N(Benter,3),'Bmiddle',_N(Bsetup,3),'Blower',_N(Sbreak,3));
}



function main() {
    Log("Strategy Start");
    while(true){
        onTick(exchanges[0]);
        Sleep(1000);
    }
}




```

> Detail

https://www.fmz.com/strategy/36195

> Last Modified

2017-02-20 15:33:43
