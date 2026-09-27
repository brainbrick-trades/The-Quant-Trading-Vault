
> Name

Large-Medium-and-Small-Three-Cycle-Leap-Strategy-V20-Spot-Test

> Author

区班量化

> Strategy Description

Large, medium and small three-cycle transition strategy. In general, the large cycle indicates the market direction, the medium cycle is the current operating cycle, and the small cycle indicates the trend stopping signal. When you enter the market, as long as you refer to the status of the three cycles of large, medium and small, you can, like Zhuge Liang, adopt ever-changing strategies to deal with the complex market. If your operating cycle frequency is several times a day, you can choose the daily line for the large cycle, 4 hours for the medium cycle, and 30 minutes for the small cycle; if your operating cycle frequency is dozens of times a day, you can choose 4 hours for the large cycle, 30 minutes for the medium cycle, and 5 minutes for the small cycle; the previous cycle is always 6 to 8 times different from the next cycle.
Then we list the relationship between the candlestick and the Bollinger Band in each cycle. There are 8 states in total. In three cycles, there are 8*8*8=512 states. These 512 states are enough to cope with all possible market conditions. Programmers with strong technical ability can pre-design the best order points and stop-loss points for each state. In order for everyone to have a basis for discussion, the district class leader has also made the strategy public on the inventor platform. Everyone is welcome to improve on this basis.
Then let's backtest it. We can see an annualized return of 29, with a drawdown being a bit high, reaching 36%. We download the logs and analyze the drawdown, which is the advantage of the Inventor platform.
 ![IMG](https://www.fmz.com/upload/asset/13120536c7fe04832dbcb.png) 
  ![IMG](https://www.fmz.com/upload/asset/131192810d7ecb2b1d1ef.png)  
  ![IMG](https://www.fmz.com/upload/asset/130ed64aa7da2ceabc187.png) 
After analysis, there are mainly the following reasons::
1,Although the structure of large, medium and small cycles is better, the strategy of how small cycles affect medium cycles is difficult to conceive. It can be simplified first and added later.;
2,When the market goes short, you should resolutely abandon your position
3,5The directional role of the daily moving average is very important, but it is not reflected in the strategy.
4,Rapid decline outside the Bollinger Bands should be sold
5,When the reason for the rise is broken, you should take profits and stop losses in time
 ![IMG](https://www.fmz.com/upload/asset/1310b2148822a81917ce8.png)  ![IMG](https://www.fmz.com/upload/asset/13173d3b37858cf619f9e.png) 
After targeted improvements and dozens of iterations, we finally achieved an annualized rate of 210, a drawdown of 16.4, and the number of transactions also dropped.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Interval|10|Polling interval (seconds))|


> Source (javascript)

``` javascript
/*backtest
start: 2019-01-01 00:00:00
end: 2019-10-10 00:00:00
period: 1d
exchanges: [{"eid":"OKEX","currency":"ETH_USDT","stocks":0}]
args: [["OpMode",1,10989],["MaxAmount",1,10989],["TradeFee",0.001,10989]]
*/
//After registering on Bihuhttps://m.bihu.com/signup?i=1ewtKO&s=4&c=4
//Search for IoT blockchain and you can contact the author area leader. You can also write me an email.tomjava@163.com
var midStatus = 0; //Medium Cycle State
var bigStatus = 0; //Large Cycle State
var beforeBigStatus = 0; //Previous big cycle status
var operPrice;
var markTime=0;

function mySell(rate){
   var account = _C(exchange.GetAccount);
   var ticker = _C(exchange.GetTicker);
   var nowPrice=ticker.Sell;
     
   //Start selling below
   var allAmount=account.Balance+account.Stocks*ticker.Sell; //Calculate total amount
   var cashRatio=account.Balance*100/allAmount;
   
   if(cashRatio<90){  //You can sell only if the cash ratio is less than 10
      if(rate==1){ //Sold 1 copy
          if(cashRatio<80){
              $.Sell(allAmount*0.1/nowPrice);
              Log("Cash Ratio",cashRatio+10);
          }else{
              $.Sell(allAmount*0.05/nowPrice);
              Log("Cash Ratio",cashRatio+5);
          }
      }else{
          if(cashRatio<75){
              $.Sell(allAmount*0.2/nowPrice);
              Log("Cash Ratio",cashRatio+20);
          }else{
              $.Sell(allAmount*0.1/nowPrice);
              Log("Cash Ratio",cashRatio+10);
          }
      }
   }
}

function myBuy(rate){
   var account = _C(exchange.GetAccount);
   var ticker = _C(exchange.GetTicker);
   var nowPrice=ticker.Sell;
     
   //Start buying below
   var allAmount=account.Balance+account.Stocks*ticker.Sell; //Calculate total amount
   var cashRatio=account.Balance*100/allAmount;
   //Log("Required purchasing ratio",rate);
   if(cashRatio>10){  //You can buy only if the cash ratio is greater than 10
      if(rate==1){ //Buy 1 copy
          if(cashRatio>20){
              $.Buy(allAmount*0.1/nowPrice);
              Log("Cash Ratio",cashRatio-10);
          }else{
              $.Buy(allAmount*0.05/nowPrice);
              Log("Cash Ratio",cashRatio-5);
          }
      }else{
          if(cashRatio>25){
              $.Buy(allAmount*0.2/nowPrice);
              Log("Cash Ratio",cashRatio-20);
          }else{
              $.Buy(allAmount*0.1/nowPrice);
              Log("Cash Ratio",cashRatio-10);
          }
      }
   }
}

function oper(){
    var ticker = _C(exchange.GetTicker);
    var nowPrice=ticker.Sell;
   
    var h1records = exchange.GetRecords(PERIOD_H1);
    var h1boll;var h1upLine;var h1midLine;var h1downLine;
    var h1bw;
    if(h1records && h1records.length > 20) {
        h1boll = TA.BOLL(h1records, 20, 2);
        h1upLine = h1boll[0][h1records.length-1];
        h1midLine = h1boll[1][h1records.length-1];
        h1downLine = h1boll[2][h1records.length-1];
    }
    
    var drecords = exchange.GetRecords(PERIOD_D1);
    var dboll;var dupLine;var dmidLine;var ddownLine;
    var dbw;var beforePrice;
    if(drecords && drecords.length > 20) {
        dboll = TA.BOLL(drecords, 20, 2);
        dupLine = dboll[0][drecords.length-1];
        dmidLine = dboll[1][drecords.length-1];
        ddownLine = dboll[2][drecords.length-1];
        dbw=dupLine-dmidLine;
        beforePrice=(drecords[drecords.length-2].Open+drecords[drecords.length-2].Close)/2;
    }
    
    if(ticker.Time-markTime<15*60*1000){ //Only allowed to judge status if a 15-minute interval is met
        return;
    }else{
        markTime=ticker.Time;
    }
    
    if(h1records && h1records.length > 20 && drecords && drecords.length > 20) {
        if(nowPrice>dupLine+dbw*0.1){
            bigStatus=0;
        }else if(nowPrice>dupLine-dbw*0.1){
            bigStatus=1;
        }else if(nowPrice>dmidLine+dbw*0.1){
            bigStatus=2;
        }else if(nowPrice>dmidLine){
            bigStatus=3;
        }else if(nowPrice>dmidLine-dbw*0.1){
            bigStatus=4;
        }else if(nowPrice>ddownLine+dbw*0.1){
            bigStatus=5;
        }else if(nowPrice>ddownLine-dbw*0.1){
            bigStatus=6;
        }else{
            bigStatus=7;
        }
        
        if(beforePrice>dupLine+dbw*0.1){
            beforeBigStatus=0;
        }else if(beforePrice>dupLine-dbw*0.1){
            beforeBigStatus=1;
        }else if(beforePrice>dmidLine+dbw*0.1){
            beforeBigStatus=2;
        }else if(beforePrice>dmidLine){
            beforeBigStatus=3;
        }else if(beforePrice>dmidLine-dbw*0.1){
            beforeBigStatus=4;
        }else if(beforePrice>ddownLine+dbw*0.1){
            beforeBigStatus=5;
        }else if(beforePrice>ddownLine-dbw*0.1){
            beforeBigStatus=6;
        }else{
            beforeBigStatus=7;
        }
        
        if(nowPrice>h1upLine+h1bw*0.1){
            midStatus=0;
        }else if(nowPrice>h1upLine-h1bw*0.1){
            midStatus=1;
        }else if(nowPrice>h1midLine+h1bw*0.1){
            midStatus=2;
        }else if(nowPrice>h1midLine){
            midStatus=3;
        }else if(nowPrice>h1midLine-h1bw*0.1){
            midStatus=4;
        }else if(nowPrice>h1downLine+h1bw*0.1){
            midStatus=5;
        }else if(nowPrice>h1downLine-h1bw*0.1){
            midStatus=6;
        }else{
            midStatus=7;
        }
        
        if(bigStatus-beforeBigStatus>0){ //Currently a large cycle downward jump
            if(midStatus==6||midStatus==7){
                //Log("Sell2A big portion",bigStatus,"Previous large",beforeBigStatus,"middle",midStatus);
                //Buy2portion
                mySell(2);
            }else if(midStatus==3||midStatus==4){
                //Log("Sell1A big portion",bigStatus,"Previous large",beforeBigStatus,"middle",midStatus);
                //Buy1portion
                mySell(1);
            }else{
                //Log("Current large",bigStatus,"Previous large",beforeBigStatus,"middle",midStatus);
            }
        }else if(bigStatus-beforeBigStatus<0){  //Currently a large cycle upward jump
            if(midStatus==6||midStatus==7){
                //Log("Buy2A big portion",bigStatus,"Previous large",beforeBigStatus,"middle",midStatus);
                //Buy2portion
                myBuy(2);
            }else if(midStatus==3||midStatus==4){
                //Log("Buy1A big portion",bigStatus,"Previous large",beforeBigStatus,"middle",midStatus);
                //Buy1portion
                myBuy(1);
            }else{
                //Log("Current large",bigStatus,"Previous large",beforeBigStatus,"middle",midStatus);
            }
        }else{
            //Log("Current large",bigStatus,"Previous large",beforeBigStatus,"middle",midStatus," dup",dupLine," Length",dboll[0].length);
        }
    }
}

function main() {
    var initAccount = _C(exchange.GetAccount);
    Log(initAccount);
    exchange.SetCurrency("LTC_USDT")
    Log("BTC_USDTName of the priced currency:", exchange.GetQuoteCurrency())
  
    while (true) {
        oper();
        Sleep(Interval*1000);
    }
}
```

> Detail

https://www.fmz.com/strategy/177631

> Last Modified

2024-01-28 18:15:48
