
> Name

Convert_Record_Cycle

> Author

jxc6698

> Strategy Description

# Get the candle chart line data of the specified period

If there are any bugs or questions, please leave a message

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|UI_NewCycleForMS|1000*60*60*2|Synthetic cycle in milliseconds|


> Source (javascript)

``` javascript
/**
*   author: jcx
*   date:   3/10/2017
*/
/**
*   Modified the "Convert Any K-Line Period" template from Xiaoxiaomeng, now supports setting any period size and inputticker
*   The time setting must be an integer multiple of the currently provided records[] period to be meaningful (there is no check in the program)
*   
*
*  Considering that the last data returned in getrecords() may change．
*   1. You can loop in the main function from 0 to < length-1  
*   2. Or the current processing method, in the AddKLine method, use timeAfOrEq() to allow the value of the last period to be updated
*       (Implicitly requires adding kline records in chronological order)
*
*/



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

/**
*   NeWCycleForMS: New Period
*   n            : The size of the candle records array returned each time
*/
var DefaultN = 10
function AssembleRecords(NewCycleForMS, n) {
    var self = {}
    self.NewCycleForMS = NewCycleForMS;
    self.curBars = []       // Used to store the most recent n candle objects
    n = parseInt(n)         // Stores the number of candles returned each time
    if (n*1 === n)
        self.n = n
    else
        self.n = DefaultN
    // Temporary Variable
    self.tmp = {lasttime: 0}

    self.timeAf = function (time1, time2) {
        return time1 < time2
    }
    self.timeAfOrEq = function (time1, time2) {
        return time1 <= time2
    }
    self.inSameKLine = function (time1, time2) {
        if (parseInt(time1/self.NewCycleForMS) === 
            parseInt(time2/self.NewCycleForMS)) {
            return true
        }
        return false;
    }
    self.getKlineStartTime = function (time) {
        return time - time%self.NewCycleForMS
    }
    self.newBarObj = function (time, v) {
        var value = 0;
        value = v
        return {                         // Define One KBar Structure
            Time: time,
            Open: value,
            High: value,
            Low: value,
            Close: value,
            Volume: 0
        }
    }
    self.updateNewBar = function(time, defaultvalue) {
        var barobj;
        if (self.curBars.length == 0) {
            barobj = self.newBarObj(self.getKlineStartTime(time), 
                defaultvalue)
            self.curBars.push(barobj)
        } else if(!self.inSameKLine(self.curBars[self.curBars.length-1].Time,
            time) ) {
            barobj = self.newBarObj(self.getKlineStartTime(time),
                defaultvalue)
            self.curBars.push(barobj)
        }
            
        if (self.curBars.length > n+2) {
            self.curBars.shift()
        }
        return self.curBars[self.curBars.length-1];
    }
    self.AddTicker = function (ticker) {
        var barobj;
//      ticker should passed as time order
        barobj = self.updateNewBar(ticker.Time, ticker.Last);

        if (!self.timeAfOrEq(self.barobj[self.barobj.length-1].Time, 
            cker.Time)) {
            return;
        }        
        if (barobj.High < ticker.High)
            barobj.High = ticker.High
        if (barobj.Low > ticker.Low)
            barobj.Low = ticker.Low
        barobj.Close = ticker.Last
//        barobj.Volume += ticker.Volume
    }
    self.AddKLine = function (klinerecord) {
        var barobj;        

        // must use <=, when stepping into new record, last record may change
        if (!self.timeAfOrEq(self.tmp.lasttime, 
            klinerecord.Time)) {
            return
        }
        barobj = self.updateNewBar(klinerecord.Time, klinerecord.Open)
        self.tmp.lasttime = klinerecord.Time

        if (barobj.High < klinerecord.High) {
            barobj.High = klinerecord.High
        }
        if (barobj.Low > klinerecord.Low)
            barobj.Low = klinerecord.Low
        barobj.Close = klinerecord.Close
        barobj.Volume += klinerecord.Volumn
    }
    self.GetKline = function () {
        var len = self.curBars.length;
        return self.curBars.slice(len-self.n);
    }

    return self;
}

//  Test Code
function main() {
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
    
    // The first parameter is baseKLine, the second parameter is the period in milliseconds to convert, 1000 * 60 * 20 That is, convert to 20Minute
    obj = AssembleRecords(Num_UI_NewCycleForMS, 5);      



    while(true){
        records = _C(exchange.GetRecords);
        
        for (var i=0;i<records.length;i++) {
            obj.AddKLine(records[i])
        }

        newrecords = obj.GetKline()
        $.PlotRecords(newrecords, 'BTC');

        // throw "stop"; // ceshi
        Sleep(1000);
    }
}
```

> Detail

https://www.fmz.com/strategy/37678

> Last Modified

2017-03-13 16:41:10
