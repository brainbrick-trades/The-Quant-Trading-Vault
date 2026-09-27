
> Name

Quantification-of-Indicators

> Author

6821281



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|junxianx|true|Average value|
|junxiant|true|Moving Average Days|
|rise_fall|0|Closing price of the previous hour or previous day at the current time: Please select|Hour|Day|
|rise_warn|true|Increase warning value|
|fall_warn|true|Decline Warning Value|
|macdwarn|8000|macdReminder value|
|macdzhouqi|0|macdPeriod: 1 minute | 5 minutes | 15 minutes | 30 minutes | 1 hour | one day|
|kdj1|9|Period 1 Value|
|kdj2|3|Period 2 Value|
|kdj3|3|Period 3 Value|
|kdjkwarn|true|kReminder value|
|kdjdwarn|true|dReminder value|
|kdjjwarn|true|jReminder value|
|kdjtp|0|Periodic moving average types: 1 minute | 5 minutes | 15 minutes | 30 minutes | 1 hour | 1 day|


> Source (javascript)

``` javascript

//Moving Average Module
function juxian(){
    var records = exchange.GetRecords()
    if (records && records.length > junxiant) {
        var ema = TA.EMA(records, junxiant)          // KLinebar Quantity meets indicator calculation period.

        if(ema[ema.length-2]>junxianx && ema[ema.length-1]>junxianx){
            Log("Moving average exceeds set value!Current Daily Moving Average:",ema[ema.length-1]," Previous Moving Average Value:",ema[ema.length-2],"Set moving average value to:",junxianx);
        }



        if(ema[ema.length-2]<junxianx && ema[ema.length-1]<junxianx){
            Log("Moving average below set value!Current",junxiant,"daily moving average:",ema[ema.length-1]," Set moving average value to:",junxianx);
        }

    }else{
        Log("Insufficient Moving Average",junxiant,"day");
    }
}



//Take profit and stop loss reminder module: you can choose to monitorXThe coin's price change in the current time unit (editable hours or days, etc.) reachesX%,Trigger Take Profit/Stop-loss reminder (or operation))
function Riseandfall(){
    if(!rise_fall){
        rise_fall=1;
    }

   //Get closing price of the previous hour
    if(rise_fall==1){
       ress =  exchange.GetRecords(PERIOD_H1); 
       return  ress[ress.length-2];
      
    }

    //Get the previous day's closing price
    if(rise_fall==2){
       ress=   exchange.GetRecords(PERIOD_D1); 
       return  ress[ress.length-2];
    }
}

//Get current buy order price
function checkPrice(){
    lastPrice = Riseandfall();
   
    lastPrice =lastPrice.Close;
    nowPrice = exchange.GetTicker();
    nowPrice=nowPrice.Buy;
    //Increase
  
    if((nowPrice-lastPrice)>0 && ((nowPrice-lastPrice)/lastPrice)>(rise_warn/100)){
       Log("Current Price:",nowPrice,"Previous Closing Price:",lastPrice,"Price Increase Reaches:"+rise_warn+"%")
    }
    //Decline
    if((lastPrice-nowPrice)>0 && ((lastPrice-nowPrice)/lastPrice)>(fall_warn/100)){
        Log("Current Price:",nowPrice,"Previous Closing Price:",lastPrice,"The decline reached:"+rise_warn+"%")
    }
    //Decline
}

//macdReminder value
function macdwarning(){
     if(!macdzhouqi){
         macdzhouqi=0;
     }
      var macdarr = new Array();
      macdarr[0]=PERIOD_M1;
      macdarr[1]=PERIOD_M5;
      macdarr[2]=PERIOD_M15;
      macdarr[3]=PERIOD_M30;
      macdarr[4]=PERIOD_H1;
      macdarr[5]=PERIOD_D1;
    var records = exchange.GetRecords(macdarr[macdzhouqi]);//Can fill in differentkLine period, for examplePERIOD_M1,PERIOD_M30,PERIOD_H1......
    var macd = TA.MACD(records, 12, 26, 9);
    if( macd[2][macd[2].length-2]>macdwarn && macd[2][macd[2].length-1]>macdwarn){
    
         Log("PreviousMacdValue greater than the set value currentMacdValue greater than set value! Previous value:",
             macd[2][macd[2].length-2],"Current value:",macd[2][macd[2].length-1],"Setting value",macdwarn);
    
    }
    
    
     if( macd[2][macd[2].length-2]<macdwarn && macd[2][macd[2].length-1]<macdwarn){
    
         Log("PreviousMacdValue less than the set value currentMacdValue less than set value! Previous value:",
             macd[2][macd[2].length-2],"Current value:",macd[2][macd[2].length-1],"Setting value",macdwarn);
    
    }
    
}

//rsi
function getrsi(){

  var records = exchange.GetRecords(PERIOD_M30);
    var rsi = TA.RSI(records, 14);
    Log(rsi);
}


function kdjzhishu(){
    if(!kdjtp){
        kdjtp=0;
    }
     var macdarr2 = new Array();
      macdarr2[0]=PERIOD_M1;
      macdarr2[1]=PERIOD_M5;
      macdarr2[2]=PERIOD_M15;
      macdarr2[3]=PERIOD_M30;
      macdarr2[4]=PERIOD_H1;
      macdarr2[5]=PERIOD_D1;
    var records = exchange.GetRecords(macdarr2[kdjtp]);
    var kdj = TA.KDJ(records, kdj1,kdj2, kdj3);
    var k = kdj[0];
    var d= kdj[1];
    var j = kdj[2];
    if(k[k.length-2] > kdjkwarn && k[k.length-1] >kdjkwarn){
    
        Log("PreviousKvalue, currentKValue greater than warning value! Previous:",k[k.length-2],"Current:",k[k.length-1],"Early Warning:",kdjkwarn);
    }
    
    
     if(d[d.length-2] > kdjdwarn && d[d.length-1] >kdjdwarn){
    
        Log("Previousdvalue, currentdValue greater than warning value! Previous:",d[d.length-2],"Current:",d[d.length-1],"Early Warning:",kdjdwarn);
    }
    
    
     if(j[j.length-2] > kdjjwarn && j[j.length-1] >kdjjwarn){
    
        Log("Previousjvalue, currentjValue greater than warning value! Previous:",j[j.length-2],"Current:",j[j.length-1],"Early Warning:",kdjjwarn);
    }
      if(k[k.length-2] <kdjkwarn && k[k.length-1] <kdjkwarn){
    
        Log("PreviousKvalue, currentKValue less than warning value! Previous:",k[k.length-2],"Current:",k[k.length-1],"Early Warning:",kdjkwarn);
    }
    
    
     if(d[d.length-2] < kdjdwarn && d[d.length-1] <kdjdwarn){
    
        Log("Previousdvalue, currentdValue less than warning value! Previous:",d[d.length-2],"Current:",d[d.length-1],"Early Warning:",kdjdwarn);
    }
    
    
     if(j[j.length-2] < kdjjwarn && j[j.length-1] <kdjjwarn){
    
        Log("Previousjvalue, currentjValue less than warning value! Previous:",j[j.length-2],"Current:",j[j.length-1],"Early Warning:",kdjjwarn);
    }

}
//


function main() {
 //kdjzhishu()
   while(1){
       Log("=======================Moving average module start========================");
       juxian();
       Log("=======================Moving average module end========================");
       Log("=======================KDJModule Start========================");
       kdjzhishu();
       Log("=======================KDJModule End========================");


       Log("=======================Price rise and fall module start========================");
       checkPrice();
       Log("=======================Price rise and fall module end========================");


       Log("=======================Take-profit and stop-loss module start========================");
       Riseandfall();
       Log("=======================Take-profit and stop-loss module end========================");

       Log("=======================macdModule Start========================");
       macdwarning();
       Log("=======================macdModule End========================");

       Sleep(90000);
  }
    // getrsi()
   /*
    while(1){
    
     checkPrice()
     Sleep(90000)
    }
   */
 //   ,,var records = Riseandfall();
   // Log(records.length)
   // Log("The first onekThe line data is,Time:", records[0].Time, "Open:", records[0].Open, "High:", records[0].High,
      //  "Low:", records[0].Close, "Volume:", records[0].Volume);
}
```

> Detail

https://www.fmz.com/strategy/91704

> Last Modified

2018-05-13 11:35:48
