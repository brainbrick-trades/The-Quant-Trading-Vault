
> Name

Statistics-of-the-Maximum-Price-Difference-Between-Platforms-by-JackConan

> Author

yzl_126@126.com

> Strategy Description

Statistics of the largest price difference between various platforms; 
If you want to print the market conditions of each exchange at that time, you can remove the comment // in front of //printCurPrice();;



> Source (javascript)

``` javascript
var maxSpace = 0;

function adjustFloat(v) {
    return Math.floor(v*1000)/1000;
}

function printCurPrice() {
    for (var i = 0; i < exchanges.length; i++) {
        Log(exchanges[i].GetName(),'=',exchanges[i].GetTicker());
    }
}

function onTick() {
    // TODO something.
    var smallPrice = 99999;
    var bigPrice = 0;
    var curPrice = 0;
    var curSpace = 0;
    
    for (var i = 0; i < exchanges.length; i++) {
        curPrice = exchanges[i].GetTicker().Buy;
        if (curPrice < smallPrice){
            smallPrice = curPrice;
        }
        if (curPrice > bigPrice){
            bigPrice = curPrice;
        }
        curSpace = bigPrice - smallPrice;
    }
    
    if (curSpace > maxSpace){
        maxSpace = curSpace;
        Log('Spread:', adjustFloat(maxSpace),'High price:', bigPrice,'Low price:', smallPrice, 'Occurrence Time →_→');
        //Print the current market quotes of each exchange;
        printCurPrice();
    }
}

function main() {
    if (exchanges.length < 2) {
        Log("The number of exchanges must be at least two to complete the statistics");
        return;
    }
    while(true) {
        onTick();
        Sleep(60000);
    }
}
```

> Detail

https://www.fmz.com/strategy/86

> Last Modified

2014-06-22 21:15:34
