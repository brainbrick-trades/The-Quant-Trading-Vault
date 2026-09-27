
> Name

Contract-Hedging-Order-Multi-Threaded-Version

> Author

醉里挑灯看剑

> Strategy Description

Developed a long time ago, JavaScript is developed as soon as you learn it, and you don't like to spray it.,![](![IMG](https://www.fmz.com/upload/asset/1c0a7b8670d7529f0f63.jpeg))
Those who are interested can update it in the secondary development. WeChat:fzqtdkj 

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|ContractTypeIdxString|quarter|quarter|Contract Type|
|MarginLevelIdxString|10|10|leverage|
|VarietiesCount|true|Number of trading varieties|
|LoopInterval|2|Delay|
|VarietiesString|BTC|ETH|Trading varieties|
|ArbitrageSpreadString|15|16|23.5|25.5|25.5#3.5|4|5|Arbitrage spread list|
|ArbitrageAmountString|10|10|10|10|20#10|10|10|10|10|Arbitrage quantity list|
|CloseNarrowSpreadString|5|6|9.7|9.8|10.2#2.1|2.2|2.3|2.4|2|2|2|The price difference in the same direction narrows and the position is closed|
|NormalDiff|0.1|Normal spread (chart))|
|HighDiff|0.3|Higher spread (chart))|
|PriceCancelRatioString|0.02|0.02|Cancel order value (percentage)|
|SlideString|0.8|0.1|Slide Value|
|BuyDepthIndex|true|Buy depth index|
|SellDepthIndex|true|Sell depth index|
|MarketState|true|Whether it is a market order|
|IsDeleteGloablConfig|false|Whether to delete _G configuration|
|IsShowLog|false|Whether to display logs|




|Button|Default|Description|
|----|----|----|
|ModifyArbitrageSpread|15|16|23.5|25.5|25.5#3.5|4|5|Modify arbitrage spread|
|ModifyArbitrageAmount|10|10|10|10|20#10|10|10|10|10|Modify arbitrage quantity|
|ModifyCloseNarrowSpread|5|6|9.7|9.8|10.2#2.1|2.2|2.3|2.4|2|2|2|Modify closing spread|


> Source (javascript)

``` javascript
var ContractTypeIdx =[] //Contract Type
var MarginLevelIdx  =[] //leverage
var VarietiesIndx   =[] //Trading varieties

var PriceCancelRatio =[]; //Order cancellation ratio
var Slide =[];  //Slide Value

var CloseNarrowSpreadList =[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]; //Close position value in the same direction


var  curVarietiesIndex =[0,0,0,0,0,0,0,0,0,0,0,0]; //0 Current execution variety subscript 1Current platform execution flag
var  curPlatformIndex  =[]; //Used to mark which two platforms are currently compared for spread(For example, index0,Index1Exchange Comparison)

var  ArbitrageSpreadList =[[],[],[],[],[],[],[],[],[],[],[],[]];   //Arbitrage spread
var  ArbitrageAmountList =[[],[],[],[],[],[],[],[],[],[],[],[]];   //Transaction quantity

var OrderInfoArry  =[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]];    //My order information (mainly records order type and order number))

var CanCelOrderCheckTimer =[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];        //Order Cancellation Detection Time

var LastBarTime    =[]; 

var DifferentHistory =[0,0,0,0,0] //Spread History


/////kLine market information//
var __lastDiff = 0;
 

var cfg = {
			tooltip: {xDateFormat: '%Y-%m-%d %H:%M:%S, %A'},
			title : { text : 'Spread analysis chart'},
			rangeSelector: {
                buttons:  [{type: 'hour',count: 1, text: '1h'}, {type: 'hour',count: 3, text: '3h'}, {type: 'hour', count: 8, text: '8h'}, {type: 'all',text: 'All'}],
                selected: 0,
                inputEnabled: false
            },
			xAxis: { type: 'datetime'},
			yAxis : {
				plotLines : [{
					value : 0.0,
					color : 'black',
					dashStyle : 'shortdash',
					width : 3,
				}, {
					value : NormalDiff,
					color : 'green',
					dashStyle : 'shortdash',
					width : 1,
				}, {
					value : HighDiff,
					color : 'red',
					dashStyle : 'shortdash',
					width : 1,
				},{
					value : -NormalDiff,
					color : 'green',
					dashStyle : 'shortdash',
					width : 1,
				}, {
					value : -HighDiff,
					color : 'red',
					dashStyle : 'shortdash',
					width : 1,
				}]
			},
			series : [{
				name : 'Price difference',
				data : [],
				tooltip: {
					valueDecimals: 2
				}
			}]
		};
function _N(v, precision) {
    if (typeof(precision) != 'number') {
        precision = 4;
    }
    var d = parseFloat(v.toFixed(Math.max(10, precision+5)));
    s = d.toString().split(".");
    if (s.length < 2 || s[1].length <= precision) {
        return d;
    }

    var b = Math.pow(10, precision);
    return Math.floor(d*b)/b;
}

function GetTicker(e) {
    if (typeof(e) == 'undefined') {
        e = exchange;
    }
    var ticker;
    while (!(ticker = e.GetTicker())) {
        Sleep(Interval);
    }
    return ticker;
}



var curArbitrageInfo =  //Current information
   [ {
        SpreadIndex:0,    //Spread Index
        UsedAmount:0,   //Current spread, used quantity
        LastArbitrageType:0 //The last arbitrage type. If the arbitrage type changes, the arbitrage spread subscript also needs to be changed..
    },
    {
        SpreadIndex:0,    //Spread Index
        UsedAmount:0,   //Current spread, used quantity
        LastArbitrageType:0 //The last arbitrage type. If the arbitrage type changes, the arbitrage spread subscript also needs to be changed..
    },   
    {
        SpreadIndex:0,    //Spread Index
        UsedAmount:0,   //Current spread, used quantity
        LastArbitrageType:0 //The last arbitrage type. If the arbitrage type changes, the arbitrage spread subscript also needs to be changed..
    },
    {
        SpreadIndex:0,    //Spread Index
        UsedAmount:0,   //Current spread, used quantity
        LastArbitrageType:0 //The last arbitrage type. If the arbitrage type changes, the arbitrage spread subscript also needs to be changed..
    },    
   ];

//Quantity Conversion
function CoinToSheetsAmount(curPrice,CoinAmount,ContractPrice)
{
   var value =curPrice *CoinAmount / ContractPrice;
    if(value <1) {
      value =1;
    }
    return _N(value, 0);
}

//Convert number of contracts to quantity
function SheetsToCoinAmount(curPrice,SheetsAmount,ContractPrice)
{
   var value =SheetsAmount * ContractPrice/curPrice;
// Log("SheetsAmount",SheetsAmount,"ContractPrice",ContractPrice,"curPrice",curPrice);
    return _N(value, 3);
}


//PD_LONG Long Position   PD_SHORT Short Position
function GetPosition(Index,posType) {
    var positions = _C(exchanges[Index].GetPosition);
    for (var i = 0; i < positions.length; i++) {
        if (positions[i].Type === posType) {
            return [positions[i].Price, positions[i].Amount];
        }
    }
    return [0, 0];
}

//Get basic exchange information
function getExchangesBaseInfo() {

    var details = [];
    for (var i = 0; i < exchanges.length; i++) {   //Only retrieves the two exchanges currently being compared..
       var account  =null;
       var ticker   =null;
       var LongPosition  =null;
       var ShortPosition =null;
       var depth    =null;
       
       if(exchanges[curPlatformIndex[i]].GetName() == 'Futures_OKCoin' ||
          exchanges[curPlatformIndex[i]].GetName() == 'Futures_HuobiDM')
       {//For contracts, get position information
          LongPosition  = GetPosition(curPlatformIndex[i],PD_LONG);
          ShortPosition = GetPosition(curPlatformIndex[i],PD_SHORT);
       }
        
       var accountTemp =exchanges[curPlatformIndex[i]].Go("GetAccount"); 
       var tickerTemp  =exchanges[curPlatformIndex[i]].Go("GetTicker");
       var depthTemp   =exchanges[curPlatformIndex[i]].Go("GetDepth");
        
       ticker   =tickerTemp.wait();
       depth    =depthTemp.wait();
       account  =accountTemp.wait();
        if(ticker ==null ||depth ==null ||  account ==null)
        { //If data acquisition fails, then directlypass..
           break;
        }
      details.push({account: account, ticker: ticker,depth: depth,LongPosition:LongPosition,ShortPosition:ShortPosition});
        
    }
    return details;
}

//Get price difference parameters:Spot Index,Dataset,Type
function GetPriceDifferent(ExchangeInfo)
{
    var Different =0;
    var Type      =0;
    //Forward calculation to obtain the spread if the contract price >If the spot price is the spot price, the spread will be calculated in a positive way.,Otherwise, calculate in the opposite way..
    
    var curSpread =ArbitrageSpreadList[curVarietiesIndex[0]][curArbitrageInfo[curVarietiesIndex[1]].SpreadIndex];
    var curUsedAmount =curArbitrageInfo[curVarietiesIndex[1]].UsedAmount;
    var curMaxArbitrageAmount =ArbitrageAmountList[curVarietiesIndex[0]][curArbitrageInfo[curVarietiesIndex[1]].SpreadIndex] ;
    
    var BuyAveragePrice  =[0,0,0,0,0,0];  //Average Buy Price
    var SellAveragePrice =[0,0,0,0,0,0];  //Average Sell Price
    
    for(var n =0;n<=BuyDepthIndex;n++)
    {//Buy Price
        BuyAveragePrice[0] +=ExchangeInfo[0].depth.Bids[n].Price;
        BuyAveragePrice[1] +=ExchangeInfo[1].depth.Bids[n].Price;        
    }

     BuyAveragePrice[0] =BuyAveragePrice[0] /(BuyDepthIndex+1); //Average Price
     BuyAveragePrice[1] =BuyAveragePrice[1] /(BuyDepthIndex+1); //Average Price    

    for(var n =0;n<=SellDepthIndex;n++)
    {//Sell Price
        SellAveragePrice[0] +=ExchangeInfo[0].depth.Asks[n].Price;
        SellAveragePrice[1] +=ExchangeInfo[1].depth.Asks[n].Price;        
    }

    SellAveragePrice[0] =SellAveragePrice[0] /(SellDepthIndex+1); //Calculate average price
    SellAveragePrice[1] =SellAveragePrice[1] /(SellDepthIndex+1); //Calculate average price        
   
   if(BuyAveragePrice[0] >SellAveragePrice[1] )
   { //Exchange 0 open short, Exchange 1 opens long
       Different =BuyAveragePrice[0] -SellAveragePrice[1];
       Type =1;
   }
   else if(BuyAveragePrice[1] >SellAveragePrice[0])   
   { //Exchange 1 is open short, Exchange 0 is long
       Different =BuyAveragePrice[1] -SellAveragePrice[0];
       Type =2;
   }
    
    if(ExchangeInfo[0].depth.Bids[0].Price <ExchangeInfo[0].depth.Bids[1].Price ||
       ExchangeInfo[1].depth.Bids[0].Price <ExchangeInfo[1].depth.Bids[1].Price ||
       ExchangeInfo[0].depth.Asks[0].Price >ExchangeInfo[0].depth.Asks[1].Price ||
       ExchangeInfo[1].depth.Asks[0].Price >ExchangeInfo[1].depth.Asks[1].Price)
    {
       Type =0;
       Different =0;
       Log("Platform Glitch,Price sorting is incorrect!!!!");
    }
    
   return  {TYPE:Type,DIFFERENT:Different};  //Return value type(Long futures, short spot ==1 Short futures, long spot==2) ,Price difference
}



//Dynamic quantity calculation,Make the most appropriate quantity based on the number of pending orders.
function  CalcAmount(ExchangeInfo,Type)
{
   var  amount =0;
    var BuyTotalAmount  =[0,0,0,0,0,0,0];
    var SellTotalAmount =[0,0,0,0,0,0,0];
    for(var n =0; n<=BuyDepthIndex;n++)
    {
       BuyTotalAmount[0] +=ExchangeInfo[0].depth.Bids[n].Amount;
       BuyTotalAmount[1] +=ExchangeInfo[1].depth.Bids[n].Amount;        
    }
    
    for (var n =0;n <=SellDepthIndex;n++)
    {
       SellTotalAmount[0] +=ExchangeInfo[0].depth.Asks[n].Amount;
       SellTotalAmount[1] +=ExchangeInfo[1].depth.Asks[n].Amount;        
    }
    
   if(Type  ==1)
   { //Exchange 0 open short, Exchange 1 opens long
        amount =Math.min(BuyTotalAmount[0],SellTotalAmount[1]);
       //Calculate the minimum buying and selling depth values for both platforms(Place Order with Minimum Value,Prevent severe issues due to insufficient depth..)
       //Extract the value with the minimum depth, but the minimum depth value cannot exceed the specified number of orders
        amount =Math.min(amount,ArbitrageAmountList[curVarietiesIndex[0]][curArbitrageInfo[curVarietiesIndex[1]].SpreadIndex]);       
   }
   else if(Type ==2)
   {//Exchange 0 opens long, Exchange 1 opens short
        amount =Math.min(SellTotalAmount[0],BuyTotalAmount[1]);
       //Extract the value with the minimum depth, but the minimum depth value cannot exceed the specified number of orders
        amount =Math.min(amount,ArbitrageAmountList[curVarietiesIndex[0]][curArbitrageInfo[curVarietiesIndex[1]].SpreadIndex]);
   }
   else if(Type ==3)
   {// 0 Close short, 1 close long
       amount =Math.min(SellTotalAmount[0],BuyTotalAmount[1]);
       //Extract the value with the minimum depth, but the minimum depth value cannot exceed the specified number of orders      
       var MinPostion = Math.min(ExchangeInfo[0].ShortPosition[1],ExchangeInfo[1].LongPosition[1]); //Close Position,Take the quantity on the side with the smallest quantity
       amount =Math.min(amount,MinPostion);
   }
   else if(Type ==4)
   {//Close: Exchange 0 closes long, Exchange 1 closes short
       amount =Math.min(BuyTotalAmount[0],SellTotalAmount[1]);       
       var MinPostion = Math.min(ExchangeInfo[0].LongPosition[1],ExchangeInfo[1].ShortPosition[1]); //Close Position,Take the quantity on the side with the smallest quantity      
       amount =Math.min(amount,MinPostion);     
   }
    
    if(Type ==1 || Type ==2)
    {//This judgment is only made for opening position types...
     //Remaining Quantity(Maximum open position quantity)
      var SurplusAmount =ArbitrageAmountList[curVarietiesIndex[0]][curArbitrageInfo[curVarietiesIndex[1]].SpreadIndex] -curArbitrageInfo[curVarietiesIndex[1]].UsedAmount;
      amount =amount >SurplusAmount?SurplusAmount:amount;   
      amount =amount>0?amount:1; //Defaults to the number of sheets (adding three items here, the main purpose is to prevent the calculation of a value of 0..)
    }
    else if(Type ==3 || Type ==4)
    {//After modification, after partial liquidation, the number of positions closed cannot exceed the maximum quantity at the current level
        //Find the index of the last position opened,If the last open position subscript is less than0,Then forcibly set to0
       if(curArbitrageInfo[curVarietiesIndex[1]].UsedAmount ==0)
       {//If there is no excess quantity in the current position, directly use the quantity from the last opening to calculate the closing
         var MinSpreadIndex =curArbitrageInfo[curVarietiesIndex[1]].SpreadIndex -1 <=0?0:curArbitrageInfo[curVarietiesIndex[1]].SpreadIndex -1; //Minimum Spread Index
         amount =Math.min(amount,ArbitrageAmountList[curVarietiesIndex[0]][MinSpreadIndex]);          
       }
       else 
       { //If there are scattered quantities in the current level, simply select the scattered quantities as the main ones
          amount =Math.min(amount,curArbitrageInfo[curVarietiesIndex[1]].UsedAmount);             
       }
    }
    
    return amount; //Return number of lots..
}

//Start Arbitrage Function
function OpenArbitrage(DifferentInfo,ExchangeInfo)
{
   var TreadAmount = CalcAmount(ExchangeInfo,DifferentInfo.TYPE);
    
   var OrderIdA   =null;
   var OrderIdB   =null;
   var OrderAWait =null;
   var OrderBWait =null;
    
   if(DifferentInfo.TYPE ==1)
   { //Exchange 0 open short, Exchange 1 opens long
       while(OrderIdA ==null &&OrderIdB ==null)
       {         
         if(OrderIdA ==null)
         {
           exchanges[curPlatformIndex[0]].SetDirection("sell");       //Set order type to short
           OrderAWait = exchanges[curPlatformIndex[0]].Go("Sell",MarketState ==true?-1:ExchangeInfo[0].depth.Bids[BuyDepthIndex].Price -Slide[curVarietiesIndex[0]],TreadAmount);  //Original Quantity Order  
         }
         if(OrderIdB ==null)
         {
           exchanges[curPlatformIndex[1]].SetDirection("buy");           //Set order type to long 
           OrderBWait = exchanges[curPlatformIndex[1]].Go("Buy",MarketState ==true?-1:ExchangeInfo[1].depth.Asks[SellDepthIndex].Price +Slide[curVarietiesIndex[0]], TreadAmount); //Quantity converted to 
         }
          OrderIdA = OrderAWait.wait();
          OrderIdB = OrderBWait.wait();
           
          if(MarketState !=true &&(OrderIdA ==null || OrderIdB ==null)){ 
              ExchangeInfo = getExchangesBaseInfo();       //Refresh data (reorder))
          }
       }

       OrderInfoArry[curVarietiesIndex[1]].push({OrderId:OrderIdA,Type:2});  //Save order information to container     
       OrderInfoArry[curVarietiesIndex[1]].push({OrderId:OrderIdB,Type:1});  //Save order information to container              

   }   
   else if(DifferentInfo.TYPE ==2)
   { //Exchange 0 opens long, Exchange 1 opens short
       while(OrderIdA ==null &&OrderIdB ==null)
       {
         if(OrderIdA ==null)
         {           
           exchanges[curPlatformIndex[0]].SetDirection("buy");           //Set order type to long 
           OrderAWait =exchanges[curPlatformIndex[0]].Go("Buy",MarketState ==true?-1:ExchangeInfo[0].depth.Asks[SellDepthIndex].Price +Slide[curVarietiesIndex[0]], TreadAmount); //Quantity converted to     
         }
         if(OrderIdB ==null)
         {          
           exchanges[curPlatformIndex[1]].SetDirection("sell");       //Set order type to short
           OrderBWait =exchanges[curPlatformIndex[1]].Go("Sell",MarketState ==true?-1:ExchangeInfo[1].depth.Bids[BuyDepthIndex].Price -Slide[curVarietiesIndex[0]],TreadAmount);  //Original Quantity Order  
         }
          OrderIdA = OrderAWait.wait();
          OrderIdB = OrderBWait.wait();  
           
          if(MarketState !=true &&(OrderIdA ==null || OrderIdB ==null)){ 
              ExchangeInfo = getExchangesBaseInfo();       //Refresh data (reorder))
          }           
       }
       
       OrderInfoArry[curVarietiesIndex[1]].push({OrderId:OrderIdA,Type:1});          
       OrderInfoArry[curVarietiesIndex[1]].push({OrderId:OrderIdB,Type:2});                 
   }
    
    
          curArbitrageInfo[curVarietiesIndex[1]].UsedAmount +=TreadAmount;
          if(curArbitrageInfo[curVarietiesIndex[1]].UsedAmount >=ArbitrageAmountList[curVarietiesIndex[0]][curArbitrageInfo[curVarietiesIndex[1]].SpreadIndex])
          {
             curArbitrageInfo[curVarietiesIndex[1]].UsedAmount =0;
              //Minimum Index Value Is0,Less Than0Then Force Return0
             curArbitrageInfo[curVarietiesIndex[1]].SpreadIndex =curArbitrageInfo[curVarietiesIndex[1]].SpreadIndex++ >ArbitrageSpreadList[curVarietiesIndex[0]].length?curArbitrageInfo[curVarietiesIndex[1]].SpreadIndex:curArbitrageInfo[curVarietiesIndex[1]].SpreadIndex++;
          }
    
      //Modify Current Index Type
       curArbitrageInfo[curVarietiesIndex[1]].LastArbitrageType =DifferentInfo.TYPE;          
      
}


//Close position, end a round of arbitrage
function  CloseArbitrage(DifferentInfo,ExchangeInfo)
{
   var TreadAmount = CalcAmount(ExchangeInfo,DifferentInfo.TYPE);
    
   var OrderIdA   =null;
   var OrderIdB   =null;
   var OrderAWait =null;
   var OrderBWait =null;
    
    if(TreadAmount >0)
    {
      if(DifferentInfo.TYPE ==3)
      { //Close short on Exchange 0, open long on Exchange 1
     //         close short ,    close long
       while(OrderIdA ==null &&OrderIdB ==null) {
           
          if(OrderIdA ==null){ 
             exchanges[curPlatformIndex[0]].SetDirection("closesell"); 
             OrderAWait =exchanges[curPlatformIndex[0]].Go("Buy",MarketState ==true?-1:ExchangeInfo[0].depth.Asks[SellDepthIndex].Price +Slide[curVarietiesIndex[0]],TreadAmount); 
          }
           
           if(OrderIdB ==null){
             exchanges[curPlatformIndex[1]].SetDirection("closebuy");
             OrderBWait =exchanges[curPlatformIndex[1]].Go("Sell",MarketState ==true?-1:ExchangeInfo[1].depth.Bids[BuyDepthIndex].Price -Slide[curVarietiesIndex[0]], TreadAmount);  //Sell to close long position  
           }
           
           OrderIdA = OrderAWait.wait();
           OrderIdB = OrderBWait.wait();
          if(MarketState !=true &&(OrderIdA ==null || OrderIdB ==null)){ 
              ExchangeInfo = getExchangesBaseInfo();       //Refresh data (reorder))
          }                   
       }
         OrderInfoArry[curVarietiesIndex[1]].push({OrderId:OrderIdA,Type:4});       
         OrderInfoArry[curVarietiesIndex[1]].push({OrderId:OrderIdB,Type:3});             
      }
        
     else if(DifferentInfo.TYPE ==4)
     {//Close: Exchange 0 closes long, Exchange 1 closes short
        while(OrderIdA ==null &&OrderIdB ==null) {     
          if(OrderIdA ==null)  {  
             exchanges[curPlatformIndex[0]].SetDirection("closebuy");
            OrderAWait =exchanges[curPlatformIndex[0]].Go("Sell",MarketState ==true?-1:ExchangeInfo[0].depth.Bids[BuyDepthIndex].Price -Slide[curVarietiesIndex[0]], TreadAmount);  //Sell to close long position    
          }
          if(OrderIdB ==null)  {
             exchanges[curPlatformIndex[1]].SetDirection("closesell"); 
             OrderBWait =exchanges[curPlatformIndex[1]].Go("Buy",MarketState ==true?-1:ExchangeInfo[1].depth.Asks[SellDepthIndex].Price +Slide[curVarietiesIndex[0]],TreadAmount);
          }
            OrderIdA = OrderAWait.wait();
            OrderIdB = OrderBWait.wait();        
          if(MarketState !=true &&(OrderIdA ==null || OrderIdB ==null)){ 
              ExchangeInfo = getExchangesBaseInfo();       //Refresh data (reorder))
           }
        }
         OrderInfoArry[curVarietiesIndex[1]].push({OrderId:OrderIdA,Type:3});           
         OrderInfoArry[curVarietiesIndex[1]].push({OrderId:OrderIdB,Type:4});             
      }  
    }
    else 
    {
       Log("Failed to close position,One party can close the position with a quantity less than0Zhang!!!,Type:",DifferentInfo.TYPE);
	   return;
    }
   
   curArbitrageInfo[curVarietiesIndex[1]].UsedAmount -=TreadAmount;
   if(curArbitrageInfo[curVarietiesIndex[1]].UsedAmount <=0)
   {
       curArbitrageInfo[curVarietiesIndex[1]].UsedAmount =0;
       //Minimum Index Value Is0,Less Than0Then Force Return0
       curArbitrageInfo[curVarietiesIndex[1]].SpreadIndex =curArbitrageInfo[curVarietiesIndex[1]].SpreadIndex--<=0?0:curArbitrageInfo[curVarietiesIndex[1]].SpreadIndex--;   
   }       
}


//Contract Price Cancellation Detection
function FuturePriceCancelCheck(Index,ExchangeInfo,CancelValue)
{
    if(IsVirtual() ==true)
    {//If it is a simulation, there is no need to cancel the order function.....
      return ;
    }
    
    var orders = exchanges[Index].GetOrders();   
    var Type    =0;
    var OrderId =0;
    
    if(orders ==null ||orders.length <=0)   {//Return directly if there are no unfilled orders....
      return; 
    }
    
    //Main purpose is for correction types (open long, open short, close long, close short))
    for(var l =0;l <OrderInfoArry[curVarietiesIndex[1]].length;l++)    {
       for(var n =0;n <orders.length;n++)   {
           if(orders[n].Id ==OrderInfoArry[curVarietiesIndex[1]][l].OrderId)  {
               orders[n].Type =OrderInfoArry[curVarietiesIndex[1]][l].Type;
               break;
           }
        }
    }
    
    for(var n =0;n <orders.length;n++)
    {
        if(Math.abs(orders[n].Price - ExchangeInfo[Index].ticker.Last) >CancelValue)
        {//If the specified value is exceeded, the order will be canceled and placed again...

            if(exchanges[Index].CancelOrder(orders[n].Id) ==true)
            {
               Sleep(2000);  //Delay 2 seconds, mainly to prevent the server from being unable to respond in time after canceling the order..
               var curOrderInfo  =_C(exchanges[Index].GetOrder,orders[n].Id);
               if(curOrderInfo.Status !=ORDER_STATE_CANCELED || curOrderInfo.Status ==ORDER_STATE_CLOSED)
               {
                   Log("Cancel and Replace Order,Cancel Order Failed,The current order status is not canceled.,Return...Current Status:",curOrderInfo.Status,"Currentid",orders[n].Id);
                   return false;
               }
               Log("Cancel order type,",orders[n].Type,"Quantity:",orders[n].Amount -orders[n].DealAmount,"Exchange index:",Index,"Orderid:",orders[n].Id);
              if(orders[n].Type ==1)
              {
                  exchanges[Index].SetDirection("buy");       //open long
                  OrderId =_C(exchanges[Index].Buy,MarketState ==true?-1:ExchangeInfo[Index].depth.Asks[SellDepthIndex].Price +Slide[curVarietiesIndex[0]],orders[n].Amount -orders[n].DealAmount);       //Original Quantity Order
                  Type =1;
                  break;
              }
              else if(orders[n].Type ==2)
              {
                   exchanges[Index].SetDirection("sell");       //open short
                   OrderId =_C(exchanges[Index].Sell,MarketState ==true?-1:ExchangeInfo[Index].depth.Bids[BuyDepthIndex].Price -Slide[curVarietiesIndex[0]],orders[n].Amount -orders[n].DealAmount);       //Original Quantity Order    
                   Type =2;
                   break;
              }            
              else if(orders[n].Type ==3)
              {
                  exchanges[Index].SetDirection("closebuy");
                  OrderId =_C(exchanges[Index].Sell,MarketState ==true?-1:ExchangeInfo[Index].depth.Bids[BuyDepthIndex].Price -Slide[curVarietiesIndex[0]], orders[n].Amount -orders[n].DealAmount);  //Sell to close long position    
                  Type =3;
                  break;
              }
              else if(orders[n].Type ==4)
              {
                  exchanges[Index].SetDirection("closesell"); 
                  OrderId =_C(exchanges[Index].Buy,MarketState ==true?-1:ExchangeInfo[Index].depth.Asks[SellDepthIndex].Price +Slide[curVarietiesIndex[0]],orders[n].Amount -orders[n].DealAmount);       
                  Type =4;
                  break;
              }
            }
        }
    }
    
    if(Type !=0) //If the value is not empty, push the new order information in..
    {
       OrderInfoArry[curVarietiesIndex[1]].push({OrderId:OrderId,Type:Type});    //After canceling the order, the new pending order will still be pushed in and saved...      
    }

    return false;   
}

//Save the values of some core variables locally
function SaveVarValue()
{
    _G("curArbitrageInfo"+curVarietiesIndex[1].toString()+"LastArbitrageType", curArbitrageInfo[curVarietiesIndex[1]].LastArbitrageType);
    _G("curArbitrageInfo"+curVarietiesIndex[1].toString()+"SpreadIndex", curArbitrageInfo[curVarietiesIndex[1]].SpreadIndex);
    _G("curArbitrageInfo"+curVarietiesIndex[1].toString()+"UsedAmount", curArbitrageInfo[curVarietiesIndex[1]].UsedAmount);    
 
}
//Read Local Content
function ReadVarValue(n)
{
      curArbitrageInfo[n].LastArbitrageType  =_G("curArbitrageInfo"+n.toString()+"LastArbitrageType");
      curArbitrageInfo[n].SpreadIndex =_G("curArbitrageInfo"+n.toString()+"SpreadIndex");
      curArbitrageInfo[n].UsedAmount  =_G("curArbitrageInfo"+n.toString()+"UsedAmount");       
    if(curArbitrageInfo[n].LastArbitrageType ==null || curArbitrageInfo[n].SpreadIndex ==null || curArbitrageInfo[n].UsedAmount ==null)
    {//If the configuration content has no data, directly classify it0
       curArbitrageInfo[n].LastArbitrageType =0;
       curArbitrageInfo[n].SpreadIndex =0;
       curArbitrageInfo[n].UsedAmount  =0;
    }
    Log("Read local configuration value:",curArbitrageInfo[n].LastArbitrageType,curArbitrageInfo[n].SpreadIndex,curArbitrageInfo[n].UsedAmount);
}

function onTick(exchanges) {
    var records      =_C(exchanges[0].GetRecords,PERIOD_M1);   //Default1Hour
    var ExchangeInfo = getExchangesBaseInfo();                 //Fetch Data
    
    if(ExchangeInfo.length <2 || records ==null || ExchangeInfo[0].account.Stocks ==0 || ExchangeInfo[1].account.Stocks ==0)  { 
       return;//If one of the two exchanges has no margin or the data only has one currency pair, then directlypass
    }    
    
   var DifferentInfo =GetPriceDifferent(ExchangeInfo);
    
   DifferentHistory[curVarietiesIndex[0]] =DifferentInfo.DIFFERENT;  //Record price difference records of different varieties for log refresh...   
    
   if(ExchangeInfo[0].ShortPosition[1] !=ExchangeInfo[1].LongPosition[1]||
      ExchangeInfo[1].ShortPosition[1] !=ExchangeInfo[0].LongPosition[1])
   {    //If the number of positions is not equal, no position opening or closing operations will be performed to prevent the Huobi contract from being blown away, resulting in unilateral positions. In this way, only one price level can be unilateral at most, and the risk is controllable...
        DifferentInfo.TYPE =-1; //Without any type, directly blocked...
   }
    

    var Bar = records[records.length - 1];    
    if (LastBarTime[curVarietiesIndex[0]] !== Bar.Time) { 
        
      if(IsShowLog ==true)
      {//Whether to display logs
          Log("Spread Information:",DifferentInfo,"  Position information",ExchangeInfo[0].ShortPosition[1],ExchangeInfo[0].LongPosition[1],
          ExchangeInfo[1].ShortPosition[1],ExchangeInfo[1].LongPosition[1],"Current spread subscript: ",curArbitrageInfo[curVarietiesIndex[1]].SpreadIndex,"Current used quantity:",curArbitrageInfo[curVarietiesIndex[1]].UsedAmount,
         "Platform 0 price:",ExchangeInfo[0].ticker.Last,"Platform 1 price:",ExchangeInfo[1].ticker.Last);
      }
        
        if(ExchangeInfo[0].ShortPosition[1] !=ExchangeInfo[1].LongPosition[1]||
           ExchangeInfo[1].ShortPosition[1] !=ExchangeInfo[0].LongPosition[1])
        { //If the number of positions is not equal, no opening or closing operations are performed to prevent Huobi contracts from acting up, resulting in only one-sided positions..
           DifferentInfo.TYPE =-1; //Without any type, directly blocked...
        }
        
    //Chart..    
    var diff = ExchangeInfo[0].ticker.Last - ExchangeInfo[1].ticker.Last;
    var strLogStatus ="";
    for(var LogN =0;LogN <VarietiesCount;LogN++)
    {
        var TempLogStatus ="Symbol : " +VarietiesIndx[LogN]+"Spread:"+ DifferentHistory[LogN].toString()+"\r\n";
        strLogStatus+=TempLogStatus;
    }
     strLogStatus+="\r\nSpeaking of liquidation, I think of hedging,Risk-free hedge,Bosses in need can contact,Literature and style flourish,Understand naturally if know!!\r\n Lease1888element/One Month,3888element/Season WeChat:fzq250 ";

     LogStatus(strLogStatus);
        
    if (__lastDiff != 0) {
        if (Math.abs(Math.abs(diff) - Math.abs(__lastDiff)) > 200) {
            return;
        }
    }
      
        if(curVarietiesIndex[0] ==0)
        {
          cfg.yAxis.plotLines[0].value=diff;
     //     cfg.subtitle={text:'Current spread:' + diff};
          __chart.update([cfg,cfg]);
          __chart.add([0, [new Date().getTime(), diff]]);           
        }
        else if(curVarietiesIndex[0] ==1)
        {
          cfg.yAxis.plotLines[1].value=diff;
  //        cfg.subtitle={text:'Current spread:' + diff};
        __chart.update([cfg,cfg]);
        __chart.add([1, [new Date().getTime(), diff]]);
        }
        
      SaveVarValue();  //Save Value to Local Periodically

      LastBarTime[curVarietiesIndex[0]] = Bar.Time; 
    }
    
    
    if((curArbitrageInfo[curVarietiesIndex[1]].SpreadIndex <=0 &&curArbitrageInfo[curVarietiesIndex[1]].UsedAmount <=0)||
      (ExchangeInfo[0].ShortPosition[1]==0&&ExchangeInfo[0].LongPosition[1]==0&&
       ExchangeInfo[1].ShortPosition[1]==0&&ExchangeInfo[1].LongPosition[1]==0))   
    {//If the current price difference subscript and the current used quantity == 0, then reinitialize..
        var PlatformAOrder =exchanges[curPlatformIndex[0]].GetOrders();
        var PlatformBOrder =exchanges[curPlatformIndex[1]].GetOrders();
        if(PlatformAOrder !=null&&PlatformBOrder !=null &&PlatformAOrder.length <=0 &&PlatformBOrder.length <=0 )
        {//If there are no unfulfilled orders on both platforms and no open orders, the order array can be cleared... Otherwise, it will be very troublesome if there are unfulfilled orders once cleared...
          curArbitrageInfo[curVarietiesIndex[1]].LastArbitrageType =0;
          curArbitrageInfo[curVarietiesIndex[1]].SpreadIndex =0;
          curArbitrageInfo[curVarietiesIndex[1]].UsedAmount  =0;
          OrderInfoArry[curVarietiesIndex[1]] =[];  //Clear Order Array
        }
    }
    
    
    //Forward calculation to obtain the spread if the contract price >If the spot price is the spot price, the spread will be calculated in a positive way.,Otherwise, calculate in the opposite way..
    
    var curOpenSpread =ArbitrageSpreadList[curVarietiesIndex[0]][curArbitrageInfo[curVarietiesIndex[1]].SpreadIndex];
    var curUsedAmount =curArbitrageInfo[curVarietiesIndex[1]].UsedAmount;
    var curMaxArbitrageAmount =ArbitrageAmountList[curVarietiesIndex[0]][curArbitrageInfo[curVarietiesIndex[1]].SpreadIndex] ;
    
    var LastArbitrageType =curArbitrageInfo[curVarietiesIndex[1]].LastArbitrageType;
    
    //Current closing price difference    
     var  curCloseSpread  =CloseNarrowSpreadList[curVarietiesIndex[0]][curArbitrageInfo[curVarietiesIndex[1]].SpreadIndex]; 

     if(curArbitrageInfo[curVarietiesIndex[1]].UsedAmount ==0)
     {//If there is no excess quantity in the current position, directly use the quantity from the last opening to calculate the closing
         var MinSpreadIndex  =curArbitrageInfo[curVarietiesIndex[1]].SpreadIndex -1 <=0?0:curArbitrageInfo[curVarietiesIndex[1]].SpreadIndex -1; //Minimum Spread Index
         curCloseSpread  =CloseNarrowSpreadList[curVarietiesIndex[0]][MinSpreadIndex];
     } 
    
    
    if(curArbitrageInfo[curVarietiesIndex[1]].SpreadIndex <ArbitrageSpreadList[curVarietiesIndex[0]].length)
    {
       if(DifferentInfo.TYPE ==1 &&DifferentInfo.DIFFERENT >curOpenSpread &&curMaxArbitrageAmount >curUsedAmount)
       { //Exchange 0 open short, Exchange 1 opens long
        DifferentInfo.TYPE =1;        
         OpenArbitrage(DifferentInfo,ExchangeInfo);
       }
       else if(DifferentInfo.TYPE ==2 &&DifferentInfo.DIFFERENT >curOpenSpread &&curMaxArbitrageAmount >curUsedAmount)
       {//Exchange 0 opens long, Exchange 1 opens short  
         DifferentInfo.TYPE =2;        
         OpenArbitrage(DifferentInfo,ExchangeInfo);      
       }
    }
    //Close Position Check_Strip Out..
    if(LastArbitrageType ==1 &&DifferentInfo.TYPE ==1 &&DifferentInfo.DIFFERENT <=curCloseSpread)
    {//Close position Close 0 short position Close 1 long position
        DifferentInfo.TYPE =3;
        CloseArbitrage(DifferentInfo,ExchangeInfo);
    }
    else if(LastArbitrageType ==2 &&DifferentInfo.TYPE ==2 &&DifferentInfo.DIFFERENT <=curCloseSpread)
    {//Close position, close 0 long position, close 1 short position
        DifferentInfo.TYPE =4;
        CloseArbitrage(DifferentInfo,ExchangeInfo);       
    }
    
    
    //Here is the closing logic when the exchange price difference reverses.(A >B Now isB<A Then the previously opened position should be closed.)
    //Do not check index here,Only judge whether the spread has reversed,Reverse Then Close..
    if(DifferentInfo.TYPE ==1 && DifferentInfo.DIFFERENT >0 &&
       ExchangeInfo[0].LongPosition[1]!=0 &&ExchangeInfo[1].ShortPosition[1]!=0)
    {//If the type == 1 and there is a position opened in the opposite direction, it will be closed. Exchange 0 opens a long position and Exchange 1 opens a short position.  
        DifferentInfo.TYPE =4;
        CloseArbitrage(DifferentInfo,ExchangeInfo);    
        Log("Spread Reversal Occurs,Close Position...",DifferentInfo.TYPE);        
    }
    else if(DifferentInfo.TYPE ==2 && DifferentInfo.DIFFERENT >0 &&
            ExchangeInfo[0].ShortPosition[1]!=0 &&ExchangeInfo[1].LongPosition[1]!=0)
    {//If type ==2 is open in the opposite direction, then close the exchange. 0 open short, exchange 1 opens long
        DifferentInfo.TYPE =3;
        CloseArbitrage(DifferentInfo,ExchangeInfo);
        Log("Spread Reversal Occurs,Close Position...",DifferentInfo.TYPE);
    }
    
    
    if(CanCelOrderCheckTimer[curVarietiesIndex[1]]++ >3)
    { //Detect order cancellation every 5 seconds
       FuturePriceCancelCheck(curPlatformIndex[0],ExchangeInfo,PriceCancelRatio[curVarietiesIndex[0]]/100*ExchangeInfo[0].ticker.Last);
       FuturePriceCancelCheck(curPlatformIndex[1],ExchangeInfo,PriceCancelRatio[curVarietiesIndex[0]]/100*ExchangeInfo[1].ticker.Last);
       CanCelOrderCheckTimer[curVarietiesIndex[1]] =0;   //Reset to 0, recount
    }
    
    
     set_command();   //Set Interaction Information
}

function main() {
    Log("exchange0:",exchanges[0].GetName(),"Symbol:",exchanges[0].GetCurrency(),exchanges[0].GetAccount());
    Log("exchange1:",exchanges[1].GetName(),"Symbol:",exchanges[1].GetCurrency(),exchanges[1].GetAccount());    
    
    __chart = Chart(cfg);
    
    var strContractTypeIdxArray  =ContractTypeIdxString.split("|");    
    var strMarginLevelIdxArray   =MarginLevelIdxString.split("|");
    var strVarietiesArray        =VarietiesString.split("|");
    var strPriceCancelRatioArray =PriceCancelRatioString.split("|");    
    var strSlideArray            =SlideString.split("|");        
//    var strCloseNarrowSpreadArray =CloseNarrowSpreadString.split("|");
    
    var strArbitrageSpreadArrayA      =ArbitrageSpreadString.split("#");       
    var strArbitrageAmountA           =ArbitrageAmountString.split("#");   //#Separator symbol for splitting
 
    for(var n =0;n<strArbitrageSpreadArrayA.length;n++)   {  //Split Arbitrage Spread
        var strArbitrageSpreadArrayB      =strArbitrageSpreadArrayA[n].split("|");       
        for(var l=0;l <strArbitrageSpreadArrayB.length;l++)    {
           ArbitrageSpreadList[n][l] =parseFloat(strArbitrageSpreadArrayB[l]);        
        }
    }
    
      for(var n =0;n<strArbitrageAmountA.length;n++)   {   //Split Trading Quantity
         var strArbitrageAmountB      =strArbitrageAmountA[n].split("|");     //|Specific data for splitting         
        for(var l=0;l <strArbitrageAmountB.length;l++)    {
           ArbitrageAmountList[n][l] =parseFloat(strArbitrageAmountB[l]);        
        }
    }  

   var strCloseNarrowSpreadArray       =CloseNarrowSpreadString.split("#");    
    
   for(var n =0;n<strCloseNarrowSpreadArray.length;n++)   {   //Split Closing Spread
         var strCloseNarrowSpreadB   =strCloseNarrowSpreadArray[n].split("|");     //|Specific data for splitting         
        for(var l=0;l <strCloseNarrowSpreadB.length;l++)    {
           CloseNarrowSpreadList[n][l] =parseFloat(strCloseNarrowSpreadB[l]);
            Log("Close Spread:", CloseNarrowSpreadList[n][l] );
        }
    }  
    
    
    for(var n =0;n<2;n++)  //Maximum quantity is the number of trading varieties
    {
       ContractTypeIdx[n]       =strContractTypeIdxArray[n];
       MarginLevelIdx[n]        =parseInt(strMarginLevelIdxArray[n]);
       VarietiesIndx[n]         =strVarietiesArray[n];
       PriceCancelRatio[n]      =parseFloat(strPriceCancelRatioArray[n]);         
       Slide[n]                 =parseFloat(strSlideArray[n]);
 
    }
    
    for(var n =0;n<exchanges.length;n++)
    {
       exchanges[n].SetPrecision(3, 1);
       exchanges[n].SetRate(1);
       exchanges[n].SetContractType(ContractTypeIdx[n]);
       exchanges[n].SetMarginLevel(MarginLevelIdx[n]);   
        Log("exchange:",n,"Current Contract Type:",ContractTypeIdx[n],"leverage:",MarginLevelIdx[n]);
    }

    
    for(var a =0;a <exchanges.length;a++)   {
        for(var b =a+1;b <exchanges.length;b++)   {
         for(var n =0; n <VarietiesCount;n++)  {    
           ReadVarValue(a+b+n);  //Read Local Configuration Information                
        }
     }
   }
    
    if(IsDeleteGloablConfig ==true)
    { //Delete the configuration information retained by _G
       _G(null); // Delete All Global Variables
    }
       
    while(true)
    {
        for(var a =0;a <exchanges.length;a++)   {
            for(var b =a+1;b <exchanges.length;b++)   {
              curPlatformIndex[0] =a; //exchange0
              curPlatformIndex[1] =b; //exchange1                 
                
              for(var n =0; n <VarietiesCount;n++)  {
                curVarietiesIndex[0]  =n;   //Current execution order is used to change the product type
                curVarietiesIndex[1]  =a+b+n;   //The current exchange and trading pair are marked 0, 1, 2, 3, 4, 5, and so on..
                if(IsVirtual() ==false)
                {//Switch symbol in live trading
                  exchanges[curPlatformIndex[0]].IO("currency", VarietiesIndx[n]+"_USD");  //Contract Symbol Change
                  exchanges[curPlatformIndex[1]].IO("currency", VarietiesIndx[n]+"_USD");  //Spot Symbol Change            
                }     

                onTick(exchanges);
                Sleep(1000); //Delay 1 Second
             }              
           }            
        }   
      Sleep(LoopInterval * 1000);     
    }   
    
}



//Obtain dynamic parameters (strategy interaction content))
 function set_command() {

     var get_command = GetCommand();//  GetCommandThe method is to get parameters, the obtained parameters are in string format, format is "Parameter Name:Parameter Value" SeeBotVS APIDocumentation
     if (get_command != null) {
         if (get_command.indexOf("ModifyArbitrageSpread:") == 0) {  //If the incoming parameter is namedA3(with"A3:"Leading, indicatingA3Parameters)

            var  AAA = (get_command.replace("ModifyArbitrageSpread:", "")); //Assign to the value in the strategyAAA(Replace the leading string with empty, and the remaining is our parameter value)
            var strArbitrageSpreadArrayA  =AAA.split("#");      
             for(var n =0;n<strArbitrageSpreadArrayA.length;n++)   {  //Split Arbitrage Spread
               var strArbitrageSpreadArrayB      =strArbitrageSpreadArrayA[n].split("|");       
                 for(var l=0;l <strArbitrageSpreadArrayB.length;l++)    {
                  ArbitrageSpreadList[n][l] =parseFloat(strArbitrageSpreadArrayB[l]);     
                  Log("New Value:",ArbitrageSpreadList[n][l]);
               }
             }
         }
         
          if (get_command.indexOf("ModifyArbitrageAmount:") == 0) {  //If the incoming parameter is namedB3(with"B3:"Leading, indicatingB3Parameters)

            var BBB = (get_command.replace("ModifyArbitrageAmount:", "")); //Assign to the value in the strategyBBB(Replace the leading string with empty, and the remaining is our parameter value)
             var strArbitrageAmountA  =BBB.split("#");   //#Separator symbol for splitting
             for(var n =0;n<strArbitrageAmountA.length;n++)   {   //Split Trading Quantity
                 var strArbitrageAmountB      =strArbitrageAmountA[n].split("|");     //|Specific data for splitting         
                 for(var l=0;l <strArbitrageAmountB.length;l++)    {
                    ArbitrageAmountList[n][l] =parseFloat(strArbitrageAmountB[l]);     
                     Log("New Value:",ArbitrageAmountList[n][l]);
                 }
              }                
         }

          if (get_command.indexOf("ModifyCloseNarrowSpread:") == 0) {  //If the incoming parameter is namedB3(with"B3:"Leading, indicatingB3Parameters)

            var CCC = (get_command.replace("ModifyCloseNarrowSpread:", "")); //Assign to the value in the strategyBBB(Replace the leading string with empty, and the remaining is our parameter value)
            var strCloseNarrowSpreadArray  =CCC.split("#");    
    
            for(var n =0;n<strCloseNarrowSpreadArray.length;n++)   {   //Split Closing Spread
               var strCloseNarrowSpreadB   =strCloseNarrowSpreadArray[n].split("|");     //|Specific data for splitting         
               for(var l=0;l <strCloseNarrowSpreadB.length;l++)    {
                 CloseNarrowSpreadList[n][l] =parseFloat(strCloseNarrowSpreadB[l]);
                Log("New Value:", CloseNarrowSpreadList[n][l] );
               }
            }  
         }         
         
     }
 }


```

> Detail

https://www.fmz.com/strategy/134174

> Last Modified

2022-03-13 05:04:50
