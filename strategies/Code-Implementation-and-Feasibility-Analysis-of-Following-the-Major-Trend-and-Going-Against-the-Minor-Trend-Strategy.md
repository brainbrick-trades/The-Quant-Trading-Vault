
> Name

Code-Implementation-and-Feasibility-Analysis-of-Following-the-Major-Trend-and-Going-Against-the-Minor-Trend-Strategy

> Author

深蓝



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|maLen|100|maLen|
|kd1|50|kd1|
|kd2|15|kd2|


> Source (javascript)

``` javascript
//Syntax fixed format, callmainMain Function
function main() {
    
    //Call from the commodities futures trading libraryCTAFramework
    $.CTA("RM000", function(st) {
        
        //ObtainKLine array
        var j = st.records;
        
        //Maximum reference for indicator calculationKNumber of lines
        if (j.length < 100) {
            return;
        }
        
        //Get the upper rootKThe closing price of the line
        var c = j[j.length - 2].Close;
        
        //ObtainKDJIndicator array
        var kds = TA.KDJ(j, kd1, kd2, kd2);
        
        //ObtainKDJIndicatorKArray of
        var ks = kds[0];
        
        //ObtainKDJIndicatorDArray of
        var ds = kds[1];
        
        //Get the upper rootKLine'sKvalue
        var k = ks[ks.length - 2].toFixed(2);
        
        //Get the upper rootKLine'sDvalue
        var d = ds[ds.length - 2].toFixed(2);
        
        //Get moving average array
        var mas = TA.MA(j, 100);
        
        //Get the upper rootKLine'sMAvalue
        var ma = mas[mas.length - 2];
        
        //Get the current position quantity, positive number indicates long position, Negative Value Indicates Short Position, 0Then do not hold position
        var mp = st.position.amount;
        
        //If currently holding a long position, and the previousKLine'sKValue less than the previous barKLine'sDvalue, close long position
        if (mp > 0 && k < d) {
            return -1; //If there are currently multiple orders, the specified return value is-N,It's flatNLong position.
        }

        //If currently holding a short position, and the previousKLine'sKValue greater than the previous barKLine'sDvalue, close short position
        if (mp < 0 && k > d) {
            return 1; //If there is currently an open order, the specified return value isN,It's flatNShort-handed order.
        }

        //If currently no position, and the previous candleKLine's closing price greater than the upper barKLine'sMAvalue, and rootKLine'sKValue greater than the previous barKLine'sDvalue, open long position
        if (mp === 0 && c > ma && k > d) {
            return 1; //If there is currently no position, the specified return value isN,Just OpenNLong position.
        }
    
        //If currently no position, and the previous candleKLine's closing price less than the upper barKLine'sMAvalue, and rootKLine'sKValue less than the previous barKLine'sDvalue, open short position
        if (mp === 0 && c < ma && k < d) {
            return -1; //If there is currently no position, the specified return value is-N,Just OpenNShort-handed order.
        }
    });
}
```

> Detail

https://www.fmz.com/strategy/59356

> Last Modified

2018-05-08 17:00:54
