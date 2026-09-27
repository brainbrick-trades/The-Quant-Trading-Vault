
> Name

Boll-Fool-Version

> Author

sabar





> Source (javascript)

``` javascript
 function main (){
    $.CTA("BTC_USDT", function(st){
        var r = st.records; //ObtainKLine array
        if (r.Length <20) return; // FilterKLine length
        var close = r[r.length - 2].close; //Get the upper rootKLine closing price
        var mp = st. positLon.amount; //Get Position Information

        var boll = TA.BOLL(r, 20, 2); // Calculate Bollinger Bands indicator
        var upLine = boll[0];
        //Get Upper Band Array
        var midLine = boll[1]; //Get Middle Band Array
        var downLine = boll[2];//Get Lower Band Array
        var upPrice = upLine [upLine.length -2];
        //Get the upper rootKLine's Upper Band Array
        var midPrice = midLine[midLine.length -2]; 
        //Get the upper rootKLine's Middle Band Array
        var downPrice = downLine[ downLine.length -2];
        //Get the upper rootKLine's Lower Band Array
        if(mp == 1 && (close < midPrice)) return -1; //If holding a long position and the closing price is below the middle band, close long
        if (mp == -1 && (close > midPrice)) return 1; //If holding a short position and the closing price is above the middle line, close the short.
        if (mp == 0 && close > midPrice) return 1; //If there is no position and the closing price is above the upper band, go long
        if (mp == 0 && close < midPrice) return -1; //If there is no position, and the closing price is below the lower band, open a short position
    });
 }     
```

> Detail

https://www.fmz.com/strategy/318249

> Last Modified

2021-09-23 09:43:52
