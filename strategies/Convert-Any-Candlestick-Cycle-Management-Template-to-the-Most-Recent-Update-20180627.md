
> Name

Convert-Any-Candlestick-Cycle-Management-Template-to-the-Most-Recent-Update-20180627

> Author

中本姜

> Strategy Description

Updated on20171114
    a. Solve the problem that Open cannot be found, which is caused by out-of-bounds access to the record array. The out-of-bounds access is caused by problems with the previous candlestick.
Updated on20171113
    a. Filter out candlestick combinations with incorrect start times
    b. Filter out candlestick combinations with incorrect time intervals
Updated on20170622
     a. RecordsManager Add Name parameter to facilitate distinguishing different candlesticks
     b. Fix When the number of fixed candlesticks does not reach a new candlestick cycle, time calculation is incorrect

Updated on20170531
    a. fix VolumeCalculation error

1. Modified from Xiaoxiaomeng's 'Convert Any K-Line Period' template

Principle:
  - Obtain a fixed candlestick period, then synthesize a new candlestick period that is an integer multiple of any fixed candlestick

Function:
  - Convert base candlestick to any candlestick period
  - Second level is not supported for the time being.

Limit:
   - The new candlestick period must be an integer multiple of the fixed candlestick period.
   - The fixed candlestick period is 1min, 3min, 5min, 15min, 30min. The new candlestick period must also be minutes and<60
   - Fixed candlestick period is 1 hour, the new candlestick period must also be in hours<24
   - The fixed candlestick cycle is 1 day, and the new candlestick cycle must also be a day
   - The fixed number of candlestick periods obtained each time is required>=2
Test version, if there are BUGs or issues, feedback is welcome.

Output function:
    $.RecordsManager(NewCycleMS, Name) Generate a new cycle manager
        NewCycleMS Milliseconds for the new candlestick period. Default(1000*60*60*2) 2hour.
        Name: Specify a name for this candlestick management
        Return candlestick manager
    $.AssembleRecords(records, BaseCycleMS) 
        records: Obtained raw datarecords
        BaseCycleMS Fixed candlestick period in milliseconds, calculations are by default done using fixed records
        Return to the new candlestick cyclerecords 
    $.GetRecordsTable(n) Get newKis the latestNEntries, Default output all entries, Output astableType,Convenient forLogStatusoutput
    $.Get***** Get some basic information

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|UI_NewCycleForMS|1000*60*60*2|Synthetic cycle in milliseconds|


> Source (javascript)

``` javascript
/*backtest
  period: 60
 */
/*
20180627
    Modified the problem that Tian cannot be integratedbug
20180118
    Shield some log output
Updated on20171114
    a. Solve the problem that Open cannot be found, which is caused by out-of-bounds access to the record array. The out-of-bounds access is caused by problems with the previous candlestick.
Updated on20171113
    a. Filter out candlestick combinations with incorrect start times
    b. Filter out candlestick combinations with incorrect time intervals
Updated on20170622
     a. RecordsManager Add Name parameter to facilitate distinguishing different candlesticks
     b. Fix When the number of fixed candlesticks does not reach a new candlestick cycle, time calculation is incorrect

Updated on20170531
    a. fix VolumeCalculation error

1. Modified from Xiaoxiaomeng's 'Convert Any K-Line Period' template

Principle:
  - Obtain a fixed candlestick period, then synthesize a new candlestick period that is an integer multiple of any fixed candlestick

Function:
  - Convert base candlestick to any candlestick period
  - Second level is not supported for the time being.

Limit:
   - The new candlestick period must be an integer multiple of the fixed candlestick period.
   - The fixed candlestick period is 1min, 3min, 5min, 15min, 30min. The new candlestick period must also be minutes and<60
   - Fixed candlestick period is 1 hour, the new candlestick period must also be in hours<24
   - The fixed candlestick cycle is 1 day, and the new candlestick cycle must also be a day
   - The fixed number of candlestick periods obtained each time is required>=2
Test version, if there are BUGs or issues, feedback is welcome.

Output function:
    $.RecordsManager(NewCycleMS, Name) Generate a new cycle manager
        NewCycleMS Milliseconds for the new candlestick period. Default(1000*60*60*2) 2hour.
        Name: Specify a name for this candlestick management
        Return candlestick manager
    $.AssembleRecords(records, BaseCycleMS) 
        records: Obtained raw datarecords
        BaseCycleMS Fixed candlestick period in milliseconds, calculations are by default done using fixed records
        Return to the new candlestick cyclerecords 
    $.GetRecordsTable(n) Get newKis the latestNEntries, Default output all entries, Output astableType,Convenient forLogStatusoutput
    $.Get***** Get some basic information
*/
function EasyReadTime(millseconds) {
    if (typeof millseconds == 'undefined' ||
        !millseconds) {
        millseconds = new Date().getTime();
    }
    var newDate = new Date();
    newDate.setTime(millseconds);
    return newDate.toLocaleString();
}

var cloneObj = function(obj) {                             // Deep copy object function
    var str, newobj = obj.constructor === Array ? [] : {};
    if (typeof obj !== 'object') {
        return;
    } else if (JSON) {
        str = JSON.stringify(obj);                         //Serialized object
            newobj = JSON.parse(str);                      //Restore
    } else {
        for (var i in obj) {
            newobj[i] = typeof obj[i] === 'object' ?
                cloneObj(obj[i]) : obj[i];
        }
    }
    return newobj;
};

var DAY = 0;
var HOURS = 1;
var MINUTES = 2;

function GetDHM(objTime, BaseCycle, NewCycleForMS){
    var ret = [];
    if(BaseCycle % (1000 * 60 * 60 * 24) === 0){
        ret[0] = objTime.getDate();
        ret[1] = DAY;
    }else if(BaseCycle % (1000 * 60 * 60) === 0){
        ret[0] = objTime.getHours();
        ret[1] = HOURS;
    }else if(BaseCycle % (1000 * 60) === 0){
        ret[0] = objTime.getMinutes();
        ret[1] = MINUTES;
    }
    if(NewCycleForMS % (1000 * 60 * 60 * 24) === 0){
        ret[2] = DAY;
    }else if(NewCycleForMS % (1000 * 60 * 60) === 0){
        ret[2] = HOURS;
    }else if(NewCycleForMS % (1000 * 60) === 0){
        ret[2] = MINUTES;
    }
    return ret;
}

function SearchFirstTime(ret, BaseCycle, NewCycleForMS){
    if(ret[1] === DAY && ret[2] === DAY){ 
        var array_day = [];
        for(var i = 1 ; i < 29; i += (NewCycleForMS / BaseCycle)){
            array_day.push(i);
        }
        for(var j = 0 ; j < array_day.length; j++ ){
            if(ret[0] === array_day[j]){
                return true;
            }
        }
    }else if(ret[1] === HOURS && ret[2] === HOURS){
        var array_hours = [];
        for(var i = 0 ; i < 24; i += (NewCycleForMS / BaseCycle)){
            array_hours.push(i);
        }
        for(var j = 0 ; j < array_hours.length ; j++){
            if(ret[0] === array_hours[j]){
                return true;
            }
        }
    }else if(ret[1] === MINUTES && ret[2] === MINUTES){
        var array_minutes = [];
        for(var i = 0; i < 60; i += (NewCycleForMS / BaseCycle)){
            array_minutes.push(i);
        }
        for(var j = 0; j < array_minutes.length; j++){
            if(ret[0] === array_minutes[j]){
                return true;
            }
        }
    }else{
        throw "The target period does not match the base period! The target period in milliseconds:" + NewCycleForMS + " Base cycle in milliseconds: " + BaseCycle;
    }
}

function Calc_High(AssRecords, n, BaseCycle, NewCycleForMS){
    var max = AssRecords[n].High;
    for(var i = 1 ; i < NewCycleForMS / BaseCycle; i++){
        max = Math.max(AssRecords[n + i].High, max);
    }
    return max;
}

function Calc_Low(AssRecords, n, BaseCycle, NewCycleForMS){
    var min = AssRecords[n].Low;
    for(var i = 1 ; i < NewCycleForMS / BaseCycle; i++){
        min = Math.min(AssRecords[n + i].Low, min);
    }
    return min;
}

function _RecordsManager(NewCycleForMS, Name) {
    if (typeof NewCycleForMS == 'string') {
        this._NewCycleForMS = 1;
        var arrayNum = NewCycleForMS.split("*");
        for(var indexNum = 0 ; indexNum < arrayNum.length ; indexNum++){
            this._NewCycleForMS = this._NewCycleForMS * Number(arrayNum[indexNum]);
        }
    } else {
        this._NewCycleForMS = NewCycleForMS;
    }
    this._Name = "";
    if (Name) {
        this._Name = Name;
    }
    this._Records = new Array();

    this.GetNewCycleForMS = function() {
        return this._NewCycleForMS;
    };
    
    this.GetRecords = function() {
        return this._Records;
    }

    this.AssembleRecords = function(records, BaseCycle) {
        var NewCycleForMS = this._NewCycleForMS;
        var AssRecords = records.slice(0); // Deep copy
        var AfterAssRecords = [];
        
        if (!records || records.length == 0) {
            Log("record is empty@!");
            return records;
        }
        if(records.length < 2){
            throw (!records) ? "Passed inrecordsParameter is incorrect" + records : "BasicKLine length less than2";
        }
        if (typeof BaseCycle === 'undefined') {
            BaseCycle = records[records.length - 1].Time - records[records.length - 2].Time;
        }
        if(NewCycleForMS % BaseCycle !== 0){
            //Log(EasyReadTime(records[records.length - 1].Time), EasyReadTime(records[records.length - 2].Time));
            //Log("Target cycle'", NewCycleForMS, "'Not the base cycle '", BaseCycle, "' is an integral multiple of <<#8#>> and cannot be synthesized.!");
            return null;
        }
        if(NewCycleForMS / BaseCycle > records.length){
            Log("records: ", records, "NewCycleForMS: ", NewCycleForMS, ", BaseCycle: ", BaseCycle);
            throw "Insufficient basic candlestick quantity, please check if the basic candlestick period is too small!";
        }
    
        // Determine timestamp, Find the baseKline relative to targetKLine start time.
        var objTime = new Date();
        var isFirstFind = true;
        var FirstStamp = null;
        for (var i = 0; i < AssRecords.length; i++) {
            objTime.setTime(AssRecords[i].Time);
            var ret = GetDHM(objTime, BaseCycle, NewCycleForMS); 
            
            if (isFirstFind === true && SearchFirstTime(ret, BaseCycle, NewCycleForMS) === true) {
                FirstStamp = AssRecords[i].Time;
                for (j = 0; j < i; j++) {
                    AssRecords.shift();        // Take the targetKExclude data that does not meet the synthesis before the line period.
                }
                isFirstFind = false;
                break;                         // Exit after exclusion
            }else if(isFirstFind === false){
                if((AssRecords[i].Time - FirstStamp) % NewCycleForMS === 0){
                    for (j = 0; j < i; j++) {
                        AssRecords.shift();    // Take the targetKExclude data that does not meet the synthesis before the line period.
                    }
                    break;
                }
            }
        }
        var BarObj = {                         // Define One KBar Structure
            Time: 0,
            Open: 0,
            High: 0,
            Low: 0,
            Close: 0,
            Volume: 0,
        };
        var n = 0;
        for (n = 0; n < AssRecords.length - (NewCycleForMS / BaseCycle);) {     // Synthesis
            /*
            {
            Time    :A timestamp, accurate to milliseconds, in the same format as the result obtained by Javascript's new Date().getTime()
            Open    :Opening price
            High    :Highest Price
            Low :Lowest Price
            Close   :Closing price
            Volume  :Trading volume
            }
            */
            //Time judgment
            var is_bad = false;
            var start_time = AssRecords[n].Time;
            var stop_time = AssRecords[n + (NewCycleForMS / BaseCycle) - 1].Time + BaseCycle;
            if (ret[2] != DAY && start_time % NewCycleForMS != 0) {
                //Log("The filter start time is incorrectkLine combination", EasyReadTime(start_time));
                is_bad = true;
            }
            if (stop_time - start_time != NewCycleForMS) {
                //Log("The filtering time interval is incorrectkLine combination", EasyReadTime(start_time), EasyReadTime(stop_time));
                is_bad=true;
            }
            if (is_bad) {
                n++;
                continue;
            }
            BarObj.Time = AssRecords[n].Time;
            BarObj.Open = AssRecords[n].Open;
            BarObj.High = Calc_High(AssRecords, n, BaseCycle, NewCycleForMS); 
            BarObj.Low =  Calc_Low(AssRecords, n, BaseCycle, NewCycleForMS); 
            BarObj.Close = AssRecords[n + (NewCycleForMS / BaseCycle) - 1].Close;
            BarObj.Volume = 0;
            for (var j = n; j < n + (NewCycleForMS / BaseCycle); j++) {
                BarObj.Volume += AssRecords[j].Volume;
            }
            AfterAssRecords.push(cloneObj(BarObj));
            n += (NewCycleForMS / BaseCycle)
        }
        
        if (n == 0) {
            BarObj.Time = AssRecords[0].Time;
        } else {
            BarObj.Time = AssRecords[n - (NewCycleForMS / BaseCycle)].Time + NewCycleForMS;  // The last time cannot be changed,
        }
        BarObj.Open = AssRecords[n].Open;
        BarObj.Close = AssRecords[AssRecords.length - 1].Close;
        BarObj.Volume = AssRecords[n].Volume;
        //BarObj.Volume = 0;
        var max = AssRecords[n].High;
        var min = AssRecords[n].Low;
        for(var index_n = n + 1 ;index_n < AssRecords.length; index_n++){
            max = Math.max(max, AssRecords[index_n].High);
            min = Math.min(min, AssRecords[index_n].Low);
            BarObj.Volume += AssRecords[index_n].Volume;
        }
        BarObj.High = max;
        BarObj.Low = min;
        AfterAssRecords.push(cloneObj(BarObj));
    
        this._Records = AfterAssRecords;
        return AfterAssRecords;
    };

    this.GetKlineName = function () {
        return " " + this._NewCycleForMS / 60 / 1000 + " MinuteKLine";
    };

    /* ObtainrecordsData Table*/
    this.GetRecordsTable = function (n) {
        if (typeof n !== 'undefined' && n >=0 ) {
            var records = this._Records.slice(-n);
        } else {
            var records = this._Records.slice(0);
        }
        
        var record_array = new Array();
        for (var i = records.length - 1; i >= 0; i--) {
            var newDate = new Date();
            newDate.setTime(records[i].Time);
            var time_str = newDate.toLocaleString();
            record_array.push([time_str, records[i].Open, records[i].Close,
                               records[i].High, records[i].Low, records[i].Volume]);
        }
        var title = this._Name + " " + this.GetKlineName() + "(" + records.length + "Root)";
        var table = {type: 'table', title: title,
                     cols: ['Time', 'Open','Close', 'High', 'Low', 'Volume'],
                     rows: record_array};
        return table;
    }
}

$.RecordsManager = function (NewCycleForMS, Name) {

    if (typeof NewCycleForMS === 'undefined') {
        NewCycleForMS = UI_NewCycleForMS;
    }
    var RecordsManager = new _RecordsManager(NewCycleForMS, Name);
    return RecordsManager;
}
    
function main() {
    var records = exchange.GetRecords();
    while (!records || records.length < 24) {
        records = exchange.GetRecords();
        Sleep(1000);
    }
    
    while (true) {
        records = _C(exchange.GetRecords);
        record_manager0 = $.RecordsManager(UI_NewCycleForMS, "Hello World");
        new_records0 = record_manager0.AssembleRecords(records);
        var table0 = record_manager0.GetRecordsTable();
        
        var BaseCycle = records[records.length - 1].Time - records[records.length - 2].Time;
        record_manager1 = $.RecordsManager(BaseCycle);
        new_records1 = record_manager1.AssembleRecords(records);
        var table1 = record_manager1.GetRecordsTable();
        LogStatus('`' + JSON.stringify([table0, table1, ""]) +'`');
        records = record_manager1.GetRecords();
        //Log(records[records.length-1]);
        Sleep(60000);
    }
}

```

> Detail

https://www.fmz.com/strategy/41163

> Last Modified

2018-06-28 10:07:56
