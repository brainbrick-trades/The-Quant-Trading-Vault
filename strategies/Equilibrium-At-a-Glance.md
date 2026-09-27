
> Name

Equilibrium-At-a-Glance

> Author

icesun963

> Strategy Description

Ichimoku Balance Basic Version

Use hourly chart as the basis, test for one to two months.
Use cloud thickness, baseline, and conversion line as signals to buy and sell.
Stop loss not judged.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|keh|12|HullMA|
|TenkanSenPeriods|9|TenkanSenConversion value interval|
|KijunSenPeriods|24|Kijun SenBaseline interval|
|SenkouSpanBPeriods|51|Senkou Span B Lookahead limit 2 intervals|
|displacement|24|DisplacementDelay line interval|
|CX|100|Cloud Thickness|


> Source (javascript)

``` javascript
var diffarray = [];
var diff1array = [];
var TenkanSenArray = [];
var KijunSenArray = [];
var SenkouSpanBArray = [];
var SenkouSpanAArray = [];
var lastOrderId = null;
var absAB = [];
var closeArray = [];



var cross = function(values1, values2) {

    var r1 = values1[values1.length - 1];
    var r2 = values1[values1.length - 2];
    var r21 = values2[values2.length - 1];
    var r22 = values2[values2.length - 2];
    //Log(r1 + " " + r2 + " " + r21 + " " + r22);
    if (r21 > r1 && r2 > r22) {
        return true;
    }
    if (r21 < r1 && r2 < r22) {
        return true;
    }
    return false;
}

function min(a, b) {
    if (a < b)
        return a;
    else
        return b;
}

function max(a, b) {
    if (a > b)
        return a;
    else
        return b;
}

function avg(a, b) {
    return (a + b) / 2;
}

function donchian(records, len) {

    var hig = TA.Highest(records, len, 'High');
    var low = TA.Lowest(records, len, 'Low');
    //Log("hig:" + hig + " low:" + low);

    return avg(hig, low);
    //avg(lowest(len), highest(len))

}

function cloudStats() {

    var a = absAB[absAB.length - 1];

    var logx = a + " ";
    for (var i = 1; i < 10; i++) {
        var b = absAB[absAB.length - i];
        var x = Math.abs(b - a);
        var q = x / a;

        if (x < 0.1) {

        } else {
            if (a > b) {
                return 1;
            } else {
                return -1;
            }
        }
        logx += b + " "

    }
    //Log(logx);
    return 0;
}


function onTick(exchange) {
    var records = exchange.GetRecords();
    var ticker = exchange.GetTicker();

    //Log("onTick");
    var close = records[records.length - 1].Close;
    closeArray.push(close);

    var wma = talib.WMA(records, Math.round(keh / 2));
    //Log(wma);
    var n2ma = 2 * wma[records.length - 1];
    //Log(n2ma);
    var wma2 = talib.WMA(records, keh);

    var nma = wma2[records.length - 1];
    var diff = n2ma - nma;
    var sqn = Math.round(Math.sqrt(keh));

    var n2ma1 = 2 * wma[records.length - 2];
    var nma1 = wma2[records.length - 2];
    var diff1 = n2ma1 - nma1;
    //var sqn1 = Math.round(Math.sqrt(keh));
    diffarray.push(diff);
    diff1array.push(diff1);
    //Log(diff + " " + diff1);
    var dwma = talib.WMA(diffarray, sqn);
    var d1wma = talib.WMA(diff1array, sqn);

    var n1 = dwma[dwma.length - 1];
    var n2 = d1wma[d1wma.length - 1];
    var b = n1 > n2 ? "lime" : "red";
    var c = n1 > n2 ? "green" : "red"
    var d = n1 > n2 ? "red" : "green";
    //Log(b + " " + c + " " + d);
    //Log(n1 + " " + n2);
    
   var ttime = records[records.length - 1].Time;
    //Conversion value=(Including today9Highest price of the day+9Lowest price of the day)/2
    var TenkanSen = donchian(records, TenkanSenPeriods);
    TenkanSenArray.push(TenkanSen);

    // Benchmark value=(Including today26Highest price of the day+26Daily Low Price)/2
    var KijunSen = donchian(records, KijunSenPeriods);
    KijunSenArray.push(KijunSen);

    // Leading Upper Limit1 (Span A) (Transformed value+Benchmark value)/2
    var SenkouSpanA = avg(TenkanSen, KijunSen);
    SenkouSpanAArray.push(SenkouSpanA);

    //Leading Upper Limit2 (Span B) (52Highest value of the day+52Lowest value of the day)/2
    var SenkouSpanB = donchian(records, SenkouSpanBPeriods);
    SenkouSpanBArray.push(SenkouSpanB);

    var absx = Math.abs(SenkouSpanA - SenkouSpanB);
    //Cloud composed ofSpan AandSpan BCompose

    absAB.push(absx);

    var SenkouSpanH = max(SenkouSpanAArray[records.length - displacement], SenkouSpanBArray[records.length - displacement]);
    var SenkouSpanL = min(SenkouSpanAArray[records.length - displacement], SenkouSpanBArray[records.length - displacement]);
    //Lagging line (Chinkou Span ) ( Green line) The closing price of the day is used as26Delayed line from days ago
 
    if(typeof(records[records.length - displacement])!="undefined"){
      var ChikouSpan = records[records.length - displacement].Close;
      $.PlotLine("ChikouSpan(Lagging line)", ChikouSpan, ttime, "green");
    }
 
   

 
    //$.PlotLine("n2", n2, ttime,"yellow");
    //$.PlotLine("n1", n1, ttime,"yellow");
    $.PlotLine("k", close, ttime, "black");
    //if (records.length > displacement + 1)
    //    $.PlotLine("k2", records[records.length - displacement].Close, ttime);
    $.PlotLine("TenkanSen(Conversion value)", TenkanSen, ttime, "red");
    $.PlotLine("KijunSen(Base line)", KijunSen, ttime, "blue");



    $.PlotLine("SenkouSpanA(Cloud layerA)", SenkouSpanA, ttime, "gray");
    $.PlotLine("SenkouSpanB(Cloud layerB)", SenkouSpanB, ttime, "gray");

    //$.PlotLine("Cloud(Cloud Thickness)",absx + 3500, ttime,"lime");
    //if (n1 > n2 && close > n2 && close > ChikouSpan) {
    //    Log("N1:" + n1 + " n2:" + n2 + " close:" + close);
    //    Log(" ChikouSpan:" + ChikouSpan + " TenkanSen:" + TenkanSen + " KijunSen:" + KijunSen);
    //    Log("SenkouSpanH :" + SenkouSpanH + " SenkouSpanL:" + SenkouSpanL);
    //}
    var longCondition = (TenkanSen >= KijunSen || close > KijunSen);
    var price = ticker.Last;
    //Log("cloudStats");
    //Log(cloudStats());

    if (cross(TenkanSenArray, closeArray) && cross(KijunSenArray, closeArray)) {
        $.PlotFlag(ttime, "Q", "Q", "circlepin", "green");

        if (absx < CX) {
            if (close < TenkanSen) {
                exchange.Buy(price, 1, "go long");
            } else {
                exchange.Sell(price, 1, "go short");
            }
        } else {
            if (close > TenkanSen) {
                exchange.Buy(price, 1, "go long2");
            } else {
                exchange.Sell(price, 1, "go short2");
            }
        }

    }



}

function main() {
    Log(exchange.GetAccount());
    while (true) {
        onTick(exchange);
        Sleep(60 * 60 * 1000);
    }
}
```

> Detail

https://www.fmz.com/strategy/55839

> Last Modified

2017-09-27 13:52:15
