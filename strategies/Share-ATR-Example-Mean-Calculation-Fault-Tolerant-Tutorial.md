
> Name

Share-ATR-Example-Mean-Calculation-Fault-Tolerant-Tutorial

> Author

作手君TradeMan

> Strategy Description

In order to give back to the FMZ platform and community, share strategies & codes & ideas & templates

Introduction:
Detailed mean calculation steps, using ATR as an example.
includes details such as metric calls, insufficient fault tolerance for data points, and fault tolerance for unexpected data errors
The key to the strategy is grasping the details.

Welcome to cooperate and communicate, learn and progress together~
v:haiyanyydss



> Source (javascript)

``` javascript
var arecords = _C(exchange.GetRecords, 300);
var time = arecords[arecords.length - 1].Time
var nowtime = time;
var atremaarr = [];
var Onoff = 0;

function main() {
    while (true) {
        //Start here Put this section in a loop   
        var Num = 50; //Can change, average of several candles
        var records = _C(exchange.GetRecords, 300);
        var atr = TA.EMA(records, 9)
        nowtime = records[records.length - 1].Time
        if (nowtime > time || Onoff == 0) {
            atr = atr.slice(atr.length - (20 + Num));
            for (var i = 0; i < (atr.length - Num); i++) { //(atr.length-Num) Length minus the period, for example500Before root50The root is an inaccurate average, here we just take450
                var atremTEMP = 0; //The calculation for the sum, initially set to0
                for (var j = 0; j < Num; j++) { //Sum
                    atrTEMP = atr[i + j] > 0 ? atr[i + j] : 0; //Remove unexpected data, take values greater than O, less than O, or other casesO
                    atremTEMP += atrTEMP;
                }
                atremaarr.push(atremTEMP / Num); //Take averagePTo array
            }
            time = nowtime;
            Onoff += 1;
            Log("Calculate the:", Onoff, "times.");
        }
        //Settle here and put this segment into the loop
        Sleep(3000)
        Log("The last one:", _N(atremaarr[atremaarr.length - 1], 2)) //Get Value
        //Log("Second-to-last candle:", _N(atremaarr[atremaarr.length-2],2))
    }
}

```

> Detail

https://www.fmz.com/strategy/396764

> Last Modified

2023-02-09 09:48:42
