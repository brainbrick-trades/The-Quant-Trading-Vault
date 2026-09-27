
> Name

Bull-and-Bear-Small-Shop-Strategy-V10-OKEx-Contract

> Author

区班量化

> Strategy Description

As discussed in the previous article, the canteen strategy can achieve an annualized return of 130% under certain circumstances. However, this is under specific circumstances, that is, the monthly moving average of the commodity is rising in the long term, and after a long period of time. If the market is in a downtrend within the short 3 months after entering the market, you may suffer a major blow.
The most important reason is that this strategy does not introduce a short-selling mechanism. Just like in the A-share market, you can only go long. When the market falls, you can only take short positions or be beaten passively. Fortunately, digital currencies provide a short-selling mechanism. Through contract transactions, we can avoid the risk of falling.
The strategy adopted by the district leader today is the bull and bear canteen strategy. The main idea is that when the bull market comes, go long and raise expectations of fair prices; when the bear market comes, go short and lower expectations of fair prices. When the monkey market comes, sell high and buy low. The judgment of Bull, Bear and Monkey refers to the previous article, which determines the current market status based on the relationship between short-term high and low points and long-term high and low points.
This strategy is applied to ETH. There are two pitfalls that need to be pointed out here: 1. This strategy is based on ETH. ETH in OKex futures is 10 dollars each; friends who need BTC, please modify the divisor yourself; 2. After the contract is placed, if it is the same multiple orders, they will be merged into one Position, so the length of the Position is at most 2. This is also what caused the district leader to repeatedly debug at that time. Fortunately, it was finally solved.
After registering on Bihuhttps://m.bihu.com/signup?i=1ewtKO&s=4&c=4
Search IoT blockchain to contact the author or group leader

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Interval|10|Polling interval (seconds))|
|mnum|20|30Minute line period|
|initRatio|0.5|Initial position ratio|
|dnum|5|Daily cycle|


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
//Search IoT blockchain to contact the author or group leader
var status = 10; //10Indicates monkey market initialization,11Indicates monkey market continues;20indicates bull market initialization,21Indicates bull market continues;30indicates bear market initialization,31Indicates bear market continues
var dhigh;
var dlow;
var mlow;
var mhigh;
    
var operPrice;
function monkeyOper(){
   var i;
   var position;
   var account = _C(exchange.GetAccount);
   var ticker = _C(exchange.GetTicker);
   var nowPrice=ticker.Sell;
   var pAmount;
    
  /* if(status==10){ //enter monkey market initialization,Set fair price
       operPrice=mlow+mhigh;
   }else{ 
       if(nowPrice<operPrice*0.97){ //worth buying
            //Buy to close all short positions
            position = _C(exchange.GetPosition);
            for (i = 0; i < position.length; i++) {
               if(position[i].Type==PD_SHORT){ //Buy short order
                 exchange.SetDirection("closesell"); 
                 exchange.Buy(nowPrice,position[i].Amount);
               }else{
                 pAmount=position[i].Amount;
               }
           }
          
           if(pAmount*10<account.Stocks*nowPrice){ //Hold at most half position
              exchange.Buy(nowPrice,Math.floor(nowPrice*account.Stocks*0.1/10)); //Try to go long
              Log("Monkey market buy",account.Stocks*0.1);
              operPrice=nowPrice;
           } 
       }else if(nowPrice>operPrice*1.03){ //Worth selling
            //Sell to close all long positions
            position = _C(exchange.GetPosition);
            for (i = 0; i < position.length; i++) {
               if(position[i].Type==PD_LONG){ //Sell long order
                 exchange.SetDirection("closebuy"); 
                 exchange.Sell(nowPrice,position[i].Amount);
               }else{
                 pAmount=position[i].Amount;
               }
           }
          
           if(pAmount*10<account.Stocks*nowPrice){ //Hold at most half position
              exchange.Sell(nowPrice,Math.floor(nowPrice*account.Stocks*0.1/10)); //Try to go long
              Log("Monkey market sell",account.Stocks*0.1);
              operPrice=nowPrice;
           } 
       }    
   }*/
}

function bullOper(){
   //Remove all pending short positions
   var orders = _C(exchange.GetOrders);
   var account = _C(exchange.GetAccount);
  
   for (var i = 0; i < orders.length; i++) {
       var order=orders[i];
       if(order.type==1){  //Short position
           exchange.CancelOrder(order.Id);
           Log("Clear long orders");
       }
   }
   
   var ticker = _C(exchange.GetTicker);
   var nowPrice=ticker.Sell;
   //Buy to close all short positions
   var position = _C(exchange.GetPosition);
   var pAmount=0;
   for (i = 0; i < position.length; i++) {
       if(position[i].Type==PD_SHORT){ //Buy to close a short position, note that the transaction direction is opposite
           exchange.SetDirection("closesell"); 
           exchange.Buy(nowPrice,position[i].Amount);
       }else{
           pAmount=position[i].Amount;
       }
   }
   
   if(status==20){  //Current price go long
       exchange.SetDirection("buy"); 
       if(pAmount*10<account.Stocks*nowPrice){ //Hold at most half position
          exchange.Buy(nowPrice,Math.floor(nowPrice*account.Stocks*0.2/10)); //Try to go long
          Log("Initial purchase",account.Stocks*0.1);
       } 
       operPrice=nowPrice;
   }else if(nowPrice<operPrice*0.97){  //Maximum of two orders allowed, strongly go long
       exchange.SetDirection("buy");
       if(pAmount*10<account.Stocks*nowPrice){ //Hold at most half position
          exchange.Buy(nowPrice,Math.floor(nowPrice*account.Stocks*0.3/10));
          Log("Increase buying",account.Stocks*0.3);
       }
       operPrice=nowPrice;
   }
}

function bearOper(){
   //Remove all pending long positions
   var orders = _C(exchange.GetOrders);
   var account = _C(exchange.GetAccount);
  
   for (var i = 0; i < orders.length; i++) {
       var order=orders[i];
       if(order.type==0){  //Long position
           exchange.CancelOrder(order.Id);
           Log("Clear multiple orders");
       }
   }
   
   var ticker = _C(exchange.GetTicker);
   var nowPrice=ticker.Sell;
   //Buy to close all long positions
   var position = _C(exchange.GetPosition);
   var pAmount=0;
   for (i = 0; i < position.length; i++) {
       if(position[i].Type==PD_LONG){ //Sell long order
           exchange.SetDirection("closebuy"); 
           exchange.Sell(nowPrice,position[i].Amount);
       }else{
           pAmount=position[i].Amount;
       }
   }
   
   if(status==30){  //Short at current price
       exchange.SetDirection("sell"); 
       if(pAmount*10<account.Stocks*nowPrice){ //Hold at most half position
          exchange.Sell(nowPrice,Math.floor(nowPrice*account.Stocks*0.2/10)); //Try short selling
          Log("Initial Sell",account.Stocks*0.1);
       } 
       operPrice=nowPrice;
   }else if(nowPrice>operPrice*1.03){  //Maximum of two orders allowed, strongly go long
       exchange.SetDirection("sell");
       if(pAmount*10<account.Stocks*nowPrice){ //Hold at most half position
          exchange.Sell(nowPrice,Math.floor(nowPrice*account.Stocks*0.3/10));
          Log("Increase selling",account.Stocks*0.3);
       }
       operPrice=nowPrice;
   }
}

function oper(){
    var ticker = _C(exchange.GetTicker);
    var nowPrice=ticker.Sell;
    
    var drecords = exchange.GetRecords(PERIOD_D1);
    var mrecords = exchange.GetRecords(PERIOD_M30);
    //Daily line5High and low points within days(Does not include currentBar)
    dhigh=TA.Highest(drecords, dnum, 'High');
    dlow=TA.Lowest(drecords, dnum, 'Low');
       
    //30Minute chart10Highs and lows within the cycle(Does not include currentBar)
    mhigh=TA.Highest(mrecords, mnum, 'High');
    mlow=TA.Lowest(mrecords, mnum, 'Low');
    
    if(mhigh>dhigh&&mlow<dlow){ //If both minute high and low points break daily high and low points, pay attention to the center of gravity to determine what market it is
        if((mhigh+mlow)<(dhigh+dlow)*0.97){
            if(status==30){
              status=31;
            }else{
              status=30; 
            }
            bearOper();
        }else if((mhigh+mlow)>(dhigh+dlow)*1.03){
            if(status==20){
              status=21;
            }else{
              status=20; 
            }
            bullOper();
        }else{
            if(status==10){
              status=11;
            }else{
              status=10;
            }
            monkeyOper();
        }
    }else if(mhigh>dhigh){ //Minute low breaks daily high, bull begins
        if(status==20){
           status=21;
        }else{
           status=20; 
        }
        bullOper();
    }else if(mlow<dlow){  //Minute low breaks daily low, bear begins
        if(status==30){
           status=31;
        }else{
           status=30;
        }
        bearOper();
    }else{  //no direction, monkey market
        if(status==10){
           status=11;
        }else{
           status=10;
        }
        monkeyOper();
    }
}

function main() {
    var initAccount = _C(exchange.GetAccount);
    Log(initAccount);
    exchange.SetContractType("quarter")    // Example set asOKEXFutures current week contract
    exchange.SetMarginLevel(5);              // Set leverage to5times
    while (true) {
        oper();
        Sleep(Interval*1000);
    }
}
```

> Detail

https://www.fmz.com/strategy/171038

> Last Modified

2019-10-24 13:44:56
