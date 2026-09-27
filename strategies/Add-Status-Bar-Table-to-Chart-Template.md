
> Name

Add-Status-Bar-Table-to-Chart-Template

> Author

发明者量化-小小梦

> Strategy Description

Chart template

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|indicatorsName|Indicator Axis 1 | Indicator Axis|
|indicators_1|Indicator 1 | Indicator1|
|indicators_2|Indicator 2 | Indicator2|
|indicators_3|Indicator 3 | Indicator3|
|Interval|500|Interval (milliseconds)|
|isOpenRightY|true|Enable Right Y-Axis|
|lineType|line|Indicator line type|


> Source (javascript)

``` javascript
/*
This is a chart template; for detailed usage, see the post in the forum.
*/
//----------------------------------Chart module----------------------------------------------------------------
var ChartObj = {//Drawing
    tooltip: {xDateFormat: '%Y-%m-%d %H:%M:%S, %A'},
    chart: { zoomType:'x',panning:true },//Chart type  
    title: { text: title}, //Title
    rangeSelector: {
            buttons:  [{type: 'hour',count: 1, text: '1h'}, {type: 'hour',count: 3, text: '3h'}, {type: 'hour', count: 8, text: '8h'}, {type: 'all',text: 'All'}],
            selected: 0,
            inputEnabled: false
        },
    subtitle: {text: subtitle},//Subtitle
    xAxis:{type: 'datetime'},
    yAxis: [{
            title: {text: 'KLine'},//Title
            style: {color: '#4572A7'},//Style 
            opposite: false  //Generate right Y-axis
        },
       {
            title:{text: indicatorsName},
            opposite: isOpenRightY  //Generate right Y-axis  ceshi
       }
    ],
    series: [//Series
        {type:'candlestick',yAxis:0,name:'K',id:'KLine',data:[]},
        {type:'flags',onSeries:'KLine',data:[]},
        {name:indicators_1,type:lineType,yAxis:isOpenRightY?1:0,data:[]},
        {name:indicators_2,type:lineType,yAxis:isOpenRightY?1:0,data:[]},
        {name:indicators_3,type:lineType,yAxis:isOpenRightY?1:0,data:[]},
        //{name:indicators_1,type:'spline',yAxis:1,data:[]},
        //{name:indicators_2,type:'spline',yAxis:1,data:[]}
        ]                  
};
var chart = Chart(ChartObj);
var isFirst = true;
var preRecordTime = 0;
var lastRecordsTime = 0;
var title = exchange.GetName();
var subtitle = indicators_1+","+indicators_2+"Indicator trend";
function Draw(records){
    var strState = "";
    var fcolor = "";
    var msg = "";
    while(!records || records.length < 5){
        records = exchange.GetRecords();
        //LogStatus("ObtainKIn line...records.length:",records === null ? "records is null" : records.length);
        Sleep(Interval);
    }
    if(isFirst === true){
        chart.reset();
        isFirst = false;
        preRecordTime = records[records.length - 1].Time;
    }
    if(preRecordTime === records[records.length - 1].Time){
        chart.add([0,[records[records.length - 1].Time,records[records.length - 1].Open,records[records.length - 1].High,records[records.length - 1].Low,records[records.length - 1].Close ],-1]);
    }else{
        //Update the previous column
        chart.add([0,[records[records.length - 2].Time,records[records.length - 2].Open,records[records.length - 2].High,records[records.length - 2].Low,records[records.length - 2].Close ],-1]);

        chart.add([0,[records[records.length - 1].Time,records[records.length - 1].Open,records[records.length - 1].High,records[records.length - 1].Low,records[records.length - 1].Close ]]);
       
        preRecordTime = records[records.length - 1].Time;
    }
    //chart.update(ChartObj); //Test cancel
    //chart.reset(500); //Test cancel
}
function SignOP(time,price,amount,state,message){
    var msg = "";
    var fcolor = ""; // ceshi
    var strState = "";//ceshi
    msg = "Average price: "+price+" coins:"+amount;
    switch(state){
        case 3:strState = "Custom information";fcolor = "black";msg = message;break;
        case 1:strState = "Open long position";fcolor = "red";break;
        case 2:strState = "Open short position";fcolor = "green";break;
        case 0:strState = "Close Position";fcolor = "blue";break;
    }
    chart.add(1, {x:time, color: fcolor , shape: 'flag', title: strState, text: msg});
}
//----------------------------------Chart moduleover------------------------------------------------------------
//----------------------------------Status bar table module-----------------------------------------------------------
var TV = null; //Table object, control table content.
var objTable = null;//Object used to display tables.
function CreateObjectString(cols,rows){
    var i = cols;// column column
    var j = rows;// row    OK
    var firstCols = 'a';
    var charValue = 0;
    var firstName = ""; //The letter part of the object's string member
    var lastName = "";  //The numeric part of the object's string member
    var strMember = ""; //Object string members
    var objStr = "";//Returned string
    if(i > 26){
        throw "ERROR column must less 26";
    }
    var strHead = '{';
    var strEnd = '}';
    for(var n = 0 ; n < j; n++){
        //Processing Line
        for(var m = 0 ; m < i; m++){
            //Process column Process abc , Number=n
            charValue = firstCols.charCodeAt();//Get character encoding
            firstName = String.fromCharCode(charValue + m);
            lastName = n;
            if(n === j - 1 && m === i - 1 ){
                strMember = '"' + firstName + lastName + '"' + ':' + '""';
            }else{
                strMember = '"' + firstName + lastName + '"' + ':' + '""' + ',';
            }
            objStr += strMember;
        }
    }
    objStr = strHead + objStr + strEnd;
    return objStr;
}

var g_cols = 0;
var g_rows = 0;
$.TableInit = function(cols,rows){
    g_cols = cols;
    g_rows = rows;
    var str = CreateObjectString(cols,rows);//Generate TVObject string
    TV = JSON.parse(str); // Parse string generation TVObject
    var tableString = CreateTableString(cols,rows);//Generate table object string
    objTable = JSON.parse(tableString);//Parse table object string
    LogStatus("Current Time:" + (new Date()) + "\n" + "`" + JSON.stringify(objTable) + "`");//Displays the table object to the status bar for the first time
    //ConnectDate(cols,rows);//Initial link data 
    return TV;//Return TVObject
};
function ConnectDate(cols,rows){//Associated function
    //Processcols 
    var i = 0;//Control objTable.cols
    for(var unit1 in TV){
        if(i < cols){
            objTable.cols[i] = TV[unit1];
        }else{
            break;
        }
        i++;
    }
    //Processrows
    var m = 0;//mControl which row
    var n = 0;//nControl which item
    var o = 1;//Skipcols section count
    for(var unit2 in TV){
        if( o <= cols){
            o++;
            continue;
        }
        if(n >= cols){
            n = 0;
            m++;
        }
        objTable.rows[m][n] = TV[unit2];
        n++;
    }
}
function CreateTableString(cols,rows){
    var strHead = '{';
    var strEnd = '}';
    var srtTable_type = ' "type": "table",';
    var strTable_title = ' "title": "Running information",';
    var strTable_cols_begin = ' "cols" : [';
    var strTable_cols_end = '],';
    var strTable_rows_begin = ' "rows" : [';
    var strTable_rows_end = ']';
    var strCols = "";
 
    var length = 0;
    for(var y in TV){// Obtain TVNumber of Members of Object
        length++;
    }
    
    var i = 1;
    for(var x in TV){// Initialize strCols 
        if(i >= cols){
            strCols += '"' + "TV." + x + '"' ;
            break;
        }else{
            strCols += '"' + "TV." + x + '"' + ',';
        }
        i++;
    }

    i = 1;//Control loop, reset the counter after one line of cols
    var n = 1; //Used to count the last time, no addition, all good
    var m = 1; //Used for skippingcols section count
    var strRowsUnit = "";
    var strRows = "";
    length = length - cols;
    for(var z in TV){
        if(m <= cols){//Skip the table cols part
            m++;
            continue;
        }

        if(i >= cols){
            strRowsUnit += '"' + "TV." + z + '"' ;
            i = 1;//Reseti
            if(n < length){
                strRowsUnit = '[' + strRowsUnit + ']' + ',';
            }else if(n === length){
                strRowsUnit = '[' + strRowsUnit + ']';
            }
            strRows += strRowsUnit;
            strRowsUnit = "";//Reset
        }else{
            strRowsUnit += '"' + "TV." + z + '"' + ',';
            i++;
        }
        n++;
    }
    var tableString = strHead + srtTable_type + strTable_title + strTable_cols_begin + strCols + strTable_cols_end + strTable_rows_begin + strRows + strTable_rows_end + strEnd;
    return tableString;
}
$.UpDateLogStatus = function(msg) { //Update status bar 
    //Column useABCmeans, use0123Display
    ConnectDate(g_cols,g_rows);//Linked data
    LogStatus("Current Time:" + (new Date()) + "msg:" + msg +  "\n" + "`" + JSON.stringify(objTable) + "`");//Update status bar
};
//----------------------------------Status bar table moduleover-------------------------------------------------------
//----------------------------------Export Function----------------------------------------------------------------
$.SignOP = function(time,price,amount,state,message){//This function is used when the strategy is running.KMark on the line chart"Open long position","Open short position","Close Position" Position of.
    //Parameterstime: The time this function is used in the strategy, generally used(new Date()).getTime() ,  price:This parameter displays the price (long/short/flat) on the label), amount:This parameter is to display the quantity on the label(Transaction) ,state: This parameter is used to control the type of tag,state = 1open long ,2open short ,0 Close Position
    if(arguments.length < 4){
        Log("SignOP Function must be passed in4Parameters : time,price,amount,state");
        return;
    }
    if(typeof(message) === "undefined"){
        message = "";
    }
    SignOP(time,price,amount,state,message);
};
$.Draw = function(records){
    Draw(records);
};
$.AddZhiBiao = function(zhibiao_Array,records,index){//This function adds an indicator line on the chart,zhibiao_Array:This parameter is indicator data (array)),records:Original data generating indicatorKLine Data,index:Indicator Line Number, Starting from1Start incrementing
    if(records[records.length - 1].Time === lastRecordsTime){
        chart.add([index+1,[records[records.length - 1].Time,zhibiao_Array[zhibiao_Array.length - 1]],-1]);
    }else{
        chart.add([index+1,[records[records.length - 2].Time,zhibiao_Array[zhibiao_Array.length - 2]],-1]);
        chart.add([index+1,[records[records.length - 1].Time,zhibiao_Array[zhibiao_Array.length - 1]]]);
        //lastRecordsTime = records[records.length - 1].Time; //Test Cancel
    }
    //chart.update(ChartObj); //Test cancel
};
$.UpDateChart = function(records){//Update the chart. Each time you add indicator lines, you need to update them after adding tags for them to be valid. records: KLine raw data
    if(records[records.length - 1].Time !== lastRecordsTime){
        lastRecordsTime = records[records.length - 1].Time;
    }
    chart.update(ChartObj);
    chart.reset(500);//Default reserved500Individual/UnitKLine
};
//----------------------------------Export Functionover-----------------------------------------------------------
//Test
function main(){
    ///*Test chart functionality
    var i = 0;
    var records = exchange.GetRecords();
    while(!records || records.length < 5){
        records = exchange.GetRecords();
        Sleep(500);
    }
    var zhibiao = [1,2,3,5,6,4,1,21,5];//ceshi
    var zhibiao2 = [11,22,44,57,8,77,5];
    
    //$.SignOP((new Date()).getTime(),null,null,3,"Customize information markers on charts");// Test mark custom information onto the chart
    while(i < 500){
        Draw(records);
        if(i===20){
            //Sleep(60*60*1000);
            SignOP((new Date()).getTime(),2900,1,1);
            $.SignOP((new Date()).getTime(),null,null,3,"Customize information markers on charts");// Test mark custom information onto the chart
        }
        //zhibiao.shift();
        //zhibiao.push(zhibiao[zhibiao.length - 1] + 1);//ceshi
        //Log("ceshi"); //ceshi
        $.AddZhiBiao(zhibiao,records,1);
        //$.AddZhiBiao(zhibiao2,records,2);
        //Log("ceshi"); //ceshi

        //Draw(records);
        //Log("ceshi1"); //ceshi
        Sleep(200);
        records = exchange.GetRecords();
        $.UpDateChart(records);//Update chart
        i++;
    }
    //*/
    /*Test status bar table functionality*/
    var cols = 6;//Column: set a variable representing the column
    var rows = 4;//Row: set a variable representing the row
    $.TableInit(cols,rows); //During initialization, the status bar will display the coordinates of each cell
    ///*
    for(var x in TV){
        TV[x] = "lalala";// Write all cells as lalala
    }
    //Update table display  lalala, Table header data cannot be duplicated, otherwise it will not display.
    /*
    TV.a0 = "a0";
    TV.b0 = "b0";
    TV.c0 = "c0";
    TV.d0 = "d0";
    TV.e0 = "e0";
    TV.f0 = "f0";//First, write the header data differently
    */
    $.UpDateLogStatus(cols,rows);//Update Status Bar Table

    ///*
    //How to write data into the table??
    var num = 100;
    var text = "Text: test table text";
    var obj = {name:"Object",age:"19",sex:"girl"};
    var array = ["Array",22,33,54];
    TV.a1 = num;
    TV.c2 = text;
    TV.b3 = obj;
    TV.b0 = array;

    $.UpDateLogStatus(cols,rows);//Update the status bar table again
    //*/
}
/*Modify
1,Added option to enable right-hand axis
2,Add parameter  lineType :  spline  /   line
*/
```

> Detail

https://www.fmz.com/strategy/20967

> Last Modified

2018-06-05 11:52:32
