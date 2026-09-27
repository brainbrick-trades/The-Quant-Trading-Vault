
> Name

Statistics-Candlestick-Backtesting-to-See-If-There-Is-a-Trend

> Author

小草

> Strategy Description

This strategy mainly aims to examine whether the next rise or fall can be predicted based on the previous rise and fall from the backtest data. The details are as follows: If 4 or 5 of the 5 candlesticks rise, then whether the next one tends to rise more, this strategy will calculate the frequency of the rise. Of course, the parameters of the strategy have also been changed to count other rising or falling situations. Within a few days of backtesting, the strategy works fine, but when the backtesting period is longer, such as from the 13th of this month to now, there will be chaos, and it is unclear why.



> Source (javascript)

``` javascript
function adjustFloat(v) {

    return Math.floor(v*1000)/1000;
}
function main(){
    var arr=[0,0,0,0,0,0];//A total of six roots are examinedKLine, use the results of the first five to predict the sixth, freely selectable
    var appear=0;         //Number of occurrences of the pattern
    var fit=0;            //SixthKThe result of the line meets expectations
    var diff=0;           //After the scheduled pattern appears, the difference between the closing price and the opening price of the sixth candle.
    while(true){
    var records=exchange.GetRecords();
    i=records.length-1;
    if(i>1&&(records[i].Close-records[i].Open>0)){
        arr.push(1);
        arr.shift();      //Take the most recent oneKInsert line at the end of the array, delete element one to keep the length unchanged. Increase insertion1,Otherwise insert0
    }
    if(i>1&&!(records[i].Close-records[i].Open>0)){
        arr.push(0);
        arr.shift();
    }
    if(i>5){
        var count=0;
        for(k=0;k<5;k++){
            if(arr[k]<1){
                count++;   //The number of gains among the top 5 candlesticks
            }
        }
        if(count<2){       //Set the number of bullish candlesticks needed, here require four or five.
            appear++;      //The required pattern appears once
            diff+=(records[i].Close-records[i].Open);//Calculate the price difference sum of the sixth, also the most recent one
            if(arr[5]<1){  //The expected result here is an increase, but it can also be written as something else
                fit++;     //The expected result appears once
                Log("Pattern occurrence count",appear,"Meets the expected number of times",fit,"Proportion",adjustFloat(fit/appear),"Sum of price differences",adjustFloat(diff));
                LogProfit(adjustFloat(fit/appear));   //Output the proportion as the return curve
            }
        }
    }
    Sleep(300000);       //Interval time, should be the same as the selected candlestick period? Here it is 5 minutes
    }
}
```

> Detail

https://www.fmz.com/strategy/1125

> Last Modified

2014-10-28 19:32:09
