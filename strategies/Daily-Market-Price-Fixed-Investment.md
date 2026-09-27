
> Name

Daily-Market-Price-Fixed-Investment

> Author

cdxy



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|singleInvestAmount|true|Market Buy|


> Source (javascript)

``` javascript


function main() {
   Log(exchange.GetAccount());

   
   //Date of the most recent investment
   var lastInvestDate = '';

   while (true) {
       //Each polling interval is60second
       Sleep(60 * 1000);

       //If the current date is the same as the last investment date, it means that you have already invested on that day and skip it.
       var now = new Date();
       var date = now.toISOString().slice(0,10);
       if (date == lastInvestDate) {
           continue;
       }

       lastInvestDate = date;
       Log("Date: " + date);

    
       exchange.Buy(-1, singleInvestAmount);
   }
}

```

> Detail

https://www.fmz.com/strategy/151259

> Last Modified

2019-06-07 16:26:19
