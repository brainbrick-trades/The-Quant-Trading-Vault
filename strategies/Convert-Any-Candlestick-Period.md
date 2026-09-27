
> Name

Convert-Any-Candlestick-Period

> Author

发明者量化-小小梦

> Strategy Description

Example strategy
- Convert base candlestick to any candlestick period
- Second level is not supported for the time being.
Test version, if there are BUGs or issues, feedback is welcome.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|UI_NewCycleForMS|1000*60*60*2|Synthetic cycle in milliseconds|


> Source (javascript)

``` javascript
// KLine period synthesis expanded based on the baseKLine synthesized into any period.
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
var isFirstFind = true;
var FirstStamp = null;

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

function AssembleRecords(records, NewCycleForMS) {
    var AssRecords = records.slice(0); // Deep copy
    var AfterAssRecords = [];
    
    if(!records || records.length < 2){
        throw (!records) ? "Passed inrecordsParameter is incorrect" + records : "BasicKLine length less than2";
    }
    var BaseCycle = records[records.length - 1].Time - records[records.length - 2].Time;
    if(NewCycleForMS % BaseCycle !== 0){
        throw "Target cycle'" + NewCycleForMS + "'Not the base cycle '" + BaseCycle + "' is an integral multiple of <<#8#>> and cannot be synthesized.!";
    }
    if(NewCycleForMS / BaseCycle > records.length){
        throw "Insufficient basic candlestick quantity, please check if the basic candlestick period is too small!";
    }

    // Determine timestamp, Find the baseKline relative to targetKLine start time.
    var objTime = new Date();
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
    for (n = 0; n < AssRecords.length - (NewCycleForMS / BaseCycle); n += (NewCycleForMS / BaseCycle)) {     // Synthesis
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
        BarObj.Time = AssRecords[n].Time;
        BarObj.Open = AssRecords[n].Open;
        BarObj.High = Calc_High(AssRecords, n, BaseCycle, NewCycleForMS); 
        BarObj.Low =  Calc_Low(AssRecords, n, BaseCycle, NewCycleForMS); 
        BarObj.Close = AssRecords[n + (NewCycleForMS / BaseCycle) - 1].Close;
        BarObj.Volume = AssRecords[n + (NewCycleForMS / BaseCycle) - 1].Volume;
        AfterAssRecords.push(cloneObj(BarObj));
    }
    
    BarObj.Time = AssRecords[n - (NewCycleForMS / BaseCycle)].Time + NewCycleForMS;  // The last time cannot be changed,
    BarObj.Open = AssRecords[n].Open;
    BarObj.Close = AssRecords[AssRecords.length - 1].Close;
    BarObj.Volume = AssRecords[AssRecords.length - 1].Volume;
    var max = AssRecords[n].High;
    var min = AssRecords[n].Low;
    for(var index_n = n + 1 ;index_n < AssRecords.length; index_n++){
        max = Math.max(max, AssRecords[index_n].High);
        min = Math.min(min, AssRecords[index_n].Low);
    }
    BarObj.High = max;
    BarObj.Low = min;
    AfterAssRecords.push(cloneObj(BarObj));

    return AfterAssRecords;
}

function main() {                                                    // Test Code
    var records = exchange.GetRecords();
    while (!records || records.length < 24) {
        records = exchange.GetRecords();
    }
    
    // Processing interface parameters, if you write it into your own strategy, you can refer to the following
    var Num_UI_NewCycleForMS = 1;
    var arrayNum = UI_NewCycleForMS.split("*");
    for(var indexNum = 0 ; indexNum < arrayNum.length ; indexNum++){
        Num_UI_NewCycleForMS = Num_UI_NewCycleForMS * Number(arrayNum[indexNum]);
    }
    Log("Custom period in milliseconds is:", Num_UI_NewCycleForMS);
    

    while(true){
        records = _C(exchange.GetRecords);
        // Log("OriginalKLine data: length", records.length, "Data:", records);
        records = AssembleRecords(records, Num_UI_NewCycleForMS);        // The first parameter is the basic candlestick, and the second parameter is the number of milliseconds of the period to be converted, 1000 * 60 * 20 is converted to 20 minutes
        // Log("After conversionKLine data: length", records.length, "Data:", records);
        $.PlotRecords(records, 'BTC');
        // throw "stop"; // ceshi
        Sleep(1000);
    }
}
```

> Detail

https://www.fmz.com/strategy/35986

> Last Modified

2017-03-05 11:47:06
