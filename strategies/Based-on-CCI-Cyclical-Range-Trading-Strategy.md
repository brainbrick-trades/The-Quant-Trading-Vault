
> Name

Based-on-CCI-Cyclical-Range-Trading-Strategy

> Author

深蓝



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Diff|40|Period range|
|Length|100|Period Length|
|AvgLength|10|CCIMean|
|Name|rb1810|Contract Code|


> Source (javascript)

``` javascript
/*backtest
start: 2015-01-01 09:00:00
end: 2018-04-22 15:00:00
period: 1h
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES","minfee":0,"fee":[0,0]}]
*/


//Syntax fixed format, callmainMain Function
function main() {
    //Call from the commodities futures trading libraryCTAFramework
    $.CTA(Name, function(st) {
        //ObtainKLine array
        var j = st.records;
        //Maximum reference for indicator calculationKNumber of lines
        if (j.length < Length) {
            return;
        }
        //Get the upper rootKThe closing price of the line
        var c1 = j[j.length - 2].Close;
        //Get previous barKThe closing price of the line
        var c2 = j[j.length - 3].Close;
        //ObtainCCIIndicator array
        var cci = talib.CCI(j, Length);
        //Calculate upper barKLine'sCCIAverage
        var sum1 = 0;
        for (var i = cci.length - 1 - 1; i >= cci.length - AvgLength - 1; i--) {
            sum1 += cci[i];
        }
        var ccima1 = sum1 / AvgLength;
        //Calculate previous barKLine'sCCIAverage
        var sum2 = 0;
        for (var k = cci.length - 1 - 2; k >= cci.length - AvgLength - 2; k--) {
            sum2 += cci[k];
        }
        var ccima2 = sum2 / AvgLength;
        //Get the current position quantity, positive number indicates long position, Negative Value Indicates Short Position, 0Then do not hold position
        var mp = st.position.amount;
        //If currently no position, and the previous candleKLine's closing price greater than the upper barKLine'sMAvalue, and rootKLine'sKValue greater than the previous barKLine'sDvalue, open long position
        if (mp === 0 && ccima2 < Diff && ccima1 > Diff) {
            return 1; //If there is currently no position, the specified return value isN,Just OpenNLong position.
        }
        //If currently no position, and the previous candleKLine's closing price less than the upper barKLine'sMAvalue, and rootKLine'sKValue less than the previous barKLine'sDvalue, open short position
        if (mp === 0 && ccima2 > -Diff && ccima1 < -Diff) {
            return -1; //If there is currently no position, the specified return value is-N,Just OpenNShort-handed order.
        }
        //If currently holding a long position, and the previousKLine'sKValue less than the previous barKLine'sDvalue, close long position
        if (mp > 0 && ccima2 > Diff && ccima1 < Diff) {
            return -1; //If there are currently multiple orders, the specified return value is-N,It's flatNLong position.
        }
        //If currently holding a short position, and the previousKLine'sKValue greater than the previous barKLine'sDvalue, close short position
        if (mp < 0 && ccima2 < -Diff && ccima1 > -Diff) {
            return 1; //If there is currently an open order, the specified return value isN,It's flatNShort-handed order.
        }
    });
}
```

> Detail

https://www.fmz.com/strategy/60287

> Last Modified

2018-04-23 17:42:32
