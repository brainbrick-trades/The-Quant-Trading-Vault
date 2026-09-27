
> Name

Share-Bar-by-Bar-Analysis-of-Long-and-Short-Strength-Indicators

> Author

作手君TradeMan

> Strategy Description

In order to give back to the FMZ platform and community, share strategies & codes & ideas & templates

Introduction:
Packaged function indicators, can be called directly
Analyze candlesticks one by one
Measure the strength of bulls and bears in the market by comparing the closing position of the candlestick itself with the relationship between the two most recent candlesticks.

In most cases, when we observe price movements, we only pay attention to the closing price or the shape of the underlying candlestick. How to read the candlestick in a better way and understand the strength of the long and short lines is the direction of more in-depth research. This study proposes a solution that compares the type of the candlestick itself with the position of the underlying candlestick and the upper and lower candlesticks to code the long and short strength. As shown in the figure, this study defines candlesticks as 18 types. There are two main classification methods, one is the closing position (to help determine the view of a single candlestick), and the other is the closing comparison (to help determine the view of the connected candlestick). The closing position can help determine the view of a single candlestick. Based on the position of a candlestick's closing price in the range from its highest price to its lowest price, we define it as a high closing candlestick, a mid closing candlestick and a low closing candlestick. The candlestick closing at each position is divided into a strong candlestick (closing price > opening price) and a weak candlestick (closing price < opening price). Therefore, there are a total of 6 categories of single candlestick, namely: strong candlestick closing at high level; weak candlestick closing at high level; strong candlestick closing at mid-range; weak candlestick closing at mid-range; strong candlestick closing at low level; weak candlestick closing at low level.
 ![IMG](https://www.fmz.com/upload/asset/a7be2f213a94a4dc6b8f.png) 
  ![IMG](https://www.fmz.com/upload/asset/a898d4d1a12440ee8bc4.png) 
   ![IMG](https://www.fmz.com/upload/asset/a87da3bf5541e8c910da.png) 
    ![IMG](https://www.fmz.com/upload/asset/a875e44f3b9fbff5a691.png) 
To sum up, by combining 6 candlestick closing relationships with 3 candlestick closing comparisons, a total of 18 candlestick strength relationships are generated. The strongest candlestick for bulls is coded as 9, the weakest candlestick is coded as -9, and the rest are progressively coded according to the strength relationship. The results are as shown in the figure
 ![IMG](https://www.fmz.com/upload/asset/a86de64549f7f9a0fc87.png) 

Welcome to cooperate and communicate, learn and progress together~
v:haiyanyydss



> Source (javascript)

``` javascript
$.getClosezhubang = function(rds){
    var arrclose = [];
    var arropen = [];
    var arrhigh = [];
    var arrlow = [];
    var arrzhubang = [];
    
    for(var i in rds){
        arrclose[i] = rds[i].Close;
        arropen[i] = rds[i].Open;
        arrhigh[i] = rds[i].High;
        arrlow[i] = rds[i].Low;
    
     if(i>1){
         
         if(arrclose[i] >= arrhigh[i-1]){
             
             if(arrclose[i] >= (arrhigh[i]-(arrhigh[i]-arrlow[i])/3) && arrclose[i] >= arropen[i]){
                 arrzhubang[i] = arrclose[i]*1.09;
             }else if(arrclose[i] >= (arrhigh[i]-(arrhigh[i]-arrlow[i])/3) && arrclose[i] < arropen[i]){
                 arrzhubang[i] = arrclose[i]*1.08;
             }else if(arrclose[i] > (arrlow[i]+(arrhigh[i]-arrlow[i])/3) && arrclose[i] < (arrhigh[i]-(arrhigh[i]-arrlow[i])/3) && arrclose[i] >= arropen[i]){
                 arrzhubang[i] = arrclose[i]*1.07;
             }else if(arrclose[i] > (arrlow[i]+(arrhigh[i]-arrlow[i])/3) && arrclose[i] < (arrhigh[i]-(arrhigh[i]-arrlow[i])/3) && arrclose[i] < arropen[i]){
                 arrzhubang[i] = arrclose[i]*1.06;
             }else if(arrclose[i] <= (arrlow[i]+(arrhigh[i]-arrlow[i])/3) && arrclose[i] >= arropen[i]){
                 arrzhubang[i] = arrclose[i]*1.05;
             }else if(arrclose[i] <= (arrlow[i]+(arrhigh[i]-arrlow[i])/3) && arrclose[i] < arropen[i]){
                 arrzhubang[i] = arrclose[i]*1.04;
             }
             
         }
         else if(arrclose[i] < arrhigh[i-1] && arrclose[i] > arrlow[i-1]){
             
             if(arrclose[i] >= (arrhigh[i]-(arrhigh[i]-arrlow[i])/3) && arrclose[i] >= arropen[i]){
                 arrzhubang[i] = arrclose[i]*1.03;
             }else if(arrclose[i] >= (arrhigh[i]-(arrhigh[i]-arrlow[i])/3) && arrclose[i] < arropen[i]){
                 arrzhubang[i] = arrclose[i]*1.02;
             }else if(arrclose[i] > (arrlow[i]+(arrhigh[i]-arrlow[i])/3) && arrclose[i] < (arrhigh[i]-(arrhigh[i]-arrlow[i])/3) && arrclose[i] >= arropen[i]){
                 arrzhubang[i] = arrclose[i]*1.01;
             }else if(arrclose[i] > (arrlow[i]+(arrhigh[i]-arrlow[i])/3) && arrclose[i] < (arrhigh[i]-(arrhigh[i]-arrlow[i])/3) && arrclose[i] < arropen[i]){
                 arrzhubang[i] = arrclose[i]*0.99;
             }else if(arrclose[i] <= (arrlow[i]+(arrhigh[i]-arrlow[i])/3) && arrclose[i] >= arropen[i]){
                 arrzhubang[i] = arrclose[i]*0.98;
             }else if(arrclose[i] <= (arrlow[i]+(arrhigh[i]-arrlow[i])/3) && arrclose[i] < arropen[i]){
                 arrzhubang[i] = arrclose[i]*0.97;
             }
             
         }
         else if(arrclose[i] <= arrlow[i-1]){
             
             if(arrclose[i] >= (arrhigh[i]-(arrhigh[i]-arrlow[i])/3) && arrclose[i] >= arropen[i]){
                 arrzhubang[i] = arrclose[i]*0.96;
             }else if(arrclose[i] >= (arrhigh[i]-(arrhigh[i]-arrlow[i])/3) && arrclose[i] < arropen[i]){
                 arrzhubang[i] = arrclose[i]*0.95;
             }else if(arrclose[i] > (arrlow[i]+(arrhigh[i]-arrlow[i])/3) && arrclose[i] < (arrhigh[i]-(arrhigh[i]-arrlow[i])/3) && arrclose[i] >= arropen[i]){
                 arrzhubang[i] = arrclose[i]*0.94;
             }else if(arrclose[i] > (arrlow[i]+(arrhigh[i]-arrlow[i])/3) && arrclose[i] < (arrhigh[i]-(arrhigh[i]-arrlow[i])/3) && arrclose[i] < arropen[i]){
                 arrzhubang[i] = arrclose[i]*0.93;
             }else if(arrclose[i] <= (arrlow[i]+(arrhigh[i]-arrlow[i])/3) && arrclose[i] >= arropen[i]){
                 arrzhubang[i] = arrclose[i]*0.92;
             }else if(arrclose[i] <= (arrlow[i]+(arrhigh[i]-arrlow[i])/3) && arrclose[i] < arropen[i]){
                 arrzhubang[i] = arrclose[i]*0.91;
             }
             
         }
     
     }else{
         arrzhubang[i] = arrclose[i];
     }    
    
    }
    return arrzhubang;
}
```

> Detail

https://www.fmz.com/strategy/396760

> Last Modified

2023-02-09 09:48:55
