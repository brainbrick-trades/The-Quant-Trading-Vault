
> Name

Thermostat-Oscillation-Is-Corrected-to-Highest-Price-Lowest-Price-Add-Increase-or-Decrease-Position-Option-Add-Additional-Number-of-Sheets-Function-Correct-Cmi

> Author

醉里挑灯看剑

> Strategy Description

According to backtesting results, with the same parameters, the reduction mode seems to be more effective than the addition mode...
Embarrassed..
![](![IMG](https://www.fmz.com/upload/asset/1c1f3f16b6a9fd54bfb4.jpeg))
This version is a perfect version with a higher degree of freedom. You can use it as you like.
WeChat: fzqtdkj, an old antique code from many years ago. After studying it for so many years, my hair has turned gray, and I haven't even figured it out yet. The difficulty of trading is as difficult as going to heaven. Damn it, I'm so close to cultivating immortality...

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|ContractTypeIdx|0|Contract Type: this_week|next_week|quarter|
|MarginLevelIdx|0|leverage: 10|20|
|LoopInterval|2|Delay|
|AmountOP|true|Quantity|
|Cmi_kLine_Cycle|PERIOD_D1|CMICalculation cycle|
|Shock_kLine_Cycle|PERIOD_H1|Shock_K line cycle|
|Trend_kLine_Cycle|PERIOD_D1|Trend_K line cycle|
|Shock_Reduce_N|true|Oscillation_Increase/Decrease Position N Value|
|Shock_Stop_N|2|Shock_stop loss N value|
|Shock_MaxAddCountLimit|4|Oscillation_maximum increase/decrease in position times|
|Shock_Departure|true|Shock_Departure N value|
|Shock_ATR_Cycle|7|Oscillation_ATR Period|
|Shock_UseLeverval|true|Oscillation_leverage usage ratio|
|Shock_WarehouseMode|false|Oscillation_Enable incremental mode|
|Shock_ExtraAmount_State|false|Oscillation_Additional quantity enable status|
|Trend_MaxAddCountLimit|4|Maximum increase and decrease of trend positions|
|Trend_Reduce_N|true|Trend_Increase/Decrease Position N Value|
|Trend_ATR_Cycle|14|Trend_ATR Period|
|Trend_Stop_N|2|Trend_Stop Loss N Value|
|Trend_UseLeverval|true|Trend_leverage usage ratio|
|Trend_WarehouseMode|false|Trend_Enable incremental mode|
|Trend_ExtraAmount_State|false|Trend_Additional quantity enable status|


> Source (javascript)

``` javascript
/*backtest
start: 2021-01-01 00:00:00
end: 2021-02-13 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_OKCoin","currency":"ETH_USD"}]
args: [["ContractTypeIdx",2],["Shock_Reduce_N",2],["Shock_Departure",2],["Shock_ATR_Cycle",14],["Trend_Reduce_N",2],["Trend_UseLeverval",3]]
*/

var  InitAccount =0;
var  LastAccount =0;
var  LastBarTime =0;

var STATE_IDLE  = 0;
var STATE_LONG  = 1;
var STATE_SHORT = 2;

var curModeState =0;

var  curMarketTrendType ="without";   //Current Market Trend Type
var  Shock_ATR =0;
var  Trend_ATR =0;

var  CmiVal  =0;  //cmivalue

//Shock trading information
var  ShockTreadInfo =
{
    Direction:STATE_IDLE,  //Trade Direction
    Amount:1,              //Current position quantity
    AdmissionBasePrice:0,   //Base price
    LadderIndex:-1,          //Current execution trade index
    LastDirection:STATE_IDLE,
    ExtraAmount:0           //Additional order quantity count (if exit is successful, increase by 1; if stop loss occurs, reset)0)
}

//Trend trading information
var  TrendTreadInfo =
{
    Direction:STATE_IDLE, //Trade Direction
    Amount:1,             //Current position quantity
    AdmissionBasePrice:0,  //Base price    
    LadderIndex:-1,        //Current execution trade index   
    LastDirection:STATE_IDLE,
    ExtraAmount:0           //Additional order quantity count (if exit is successful, increase by 1; if stop loss occurs, reset)0)    
}

//According to contract type,Get the face value of the contract
function GetContractFcaeValue() { //Only Bitcoin is100US Dollar,The rest are all10US Dollar
    if (exchange.GetCurrency() == "BTC_USD") {
        return 100;
    } else {
        return 10;
    }
    return 100;
}

//PD_LONG Long Position   PD_SHORT Short Position
function GetPosition(posType) {
    var positions = exchange.GetPosition();
    for (var i = 0; i < positions.length; i++) {
        if (positions[i].Type === posType) {
            return [positions[i].Price, positions[i].Amount];
        }
    }
    return [0, 0];
}

var N_CMI =30;   //Evaluate cmitimeframe
//ObtainCMIvalue
function GetCmiVal(records)
{
    var Cmi =0;
      if(records.length >N_CMI)
      {
        var  HighPrice =TA.Highest(records, N_CMI, 'High');
        var  LowPrice  =TA.Lowest(records, N_CMI, 'Low');
         
        Cmi =Math.abs((records[records.length -1].Close - records[records.length -N_CMI-1].Close)/(HighPrice -LowPrice))*100;
      //   Log("Cmi:",Cmi,"Highest Price:",HighPrice,"Lowest Price:",LowPrice,"Highest Price-Lowest Price Spread:",HighPrice -LowPrice,"absAbsolute price difference:",Math.abs((records[records.length -1].Close - records[records.length -29].Close)));
       }   
    
    return Cmi;
}

function GetKLineCycle(Cycle)
{
    if(Cycle =="PERIOD_H1")       {    return PERIOD_H1;      }
    else if(Cycle =="PERIOD_D1")  {    return PERIOD_D1;      }
    else if(Cycle =="PERIOD_M30") {    return PERIOD_M30;     }    
    else if(Cycle =="PERIOD_M15") {    return PERIOD_M15;     }        
    else if(Cycle =="PERIOD_M5")  {    return PERIOD_M5;      }         
    else                          {    return PERIOD_M1;      }                
}

//Quantity Conversion
function CoinToSheetsAmount(ticker,CoinAmount,ContractPrice)
{
   var value =ticker.Last *CoinAmount / ContractPrice;
    if(value <1) {
      value =1;
    }
    return _N(value, 0);
}



//Parameters for calculating order quantity:Use leverage ratio (do not use fill in1),Account,ATR_N,Proportion of funds used (fill in if using half)0.5Use all, fill in1),Risk ratio (maximum loss value,Loss %1Just fill in1,Loss2%Just fill in2)
function CalculationAmount(UseLevel,ticker, account, ATR_N,Stop_N, AssestRetion,RiskRatio) {
    var ContractFcaceValue = GetContractFcaeValue(); //Calculate contract value
    var TotalAssest = account.Stocks * ticker.Last * AssestRetion * UseLevel; //Calculate the total funds(usd)
    //Calculate the position opened based on the current funds
    var PositionCoinAmount = (TotalAssest * (RiskRatio / 100)) / (ATR_N[ATR_N.length - 1]*Stop_N); //Position funds
    var Amount = CoinToSheetsAmount(ticker, PositionCoinAmount, ContractFcaceValue) / 4; //Convert coin quantity to lots
    //  Log("Total funds:",TotalAssest,"Calculate the number of coins:",PositionCoinAmount,"Calculate the number of coins to bet:",Amount, "ATRvalue:",ATR_N[ATR_N.length-1]," Contract face value:",ContractFcaceValue,"Market price:",ticker.Last,"Current funds:",account.Stocks)
    if (Amount < 1) {  //The minimum number of pictures is1Zhang
        Amount = 1;
    }
 
    return parseInt(Amount);
}



//Calculate the quantity for opening or closing positions. Parameters: trend type, order type (open position)orClose position), whether incremental is enabled
function  CalcAmount(MarketTrendType,OperationType,WarehouseMode)
{
    var relustAmount =0; //Quantity
    var TempAmount   =0;
    if(MarketTrendType =="ranging market")
    {
        if(ShockTreadInfo.ExtraAmount >=2)
        {
           ShockTreadInfo.ExtraAmount =2;
        }
        
        if(Shock_ExtraAmount_State ==true) //Increase value when enabled
        {
           TempAmount =ShockTreadInfo.Amount +ShockTreadInfo.ExtraAmount; //Increase additional quantity
        }
        else  {
           TempAmount =ShockTreadInfo.Amount; //If not enabled, directly assign the base value
        }
        
        
       if(WarehouseMode ==true) //Add position mode
       {
          if(OperationType =="Admission")               {
             relustAmount =TempAmount;
          }
          else if(OperationType =="Increase or decrease positions")          {
             relustAmount =TempAmount;
          }
          else if(OperationType =="Close all positions")       {
             relustAmount =ShockTreadInfo.LadderIndex *TempAmount;
          }
       }
       else  //Reduce position mode
       {
          if(OperationType =="Admission")               {
             relustAmount =TempAmount*Shock_MaxAddCountLimit;
          }
          else if(OperationType =="Increase or decrease positions")          {
             relustAmount =TempAmount;             
          }
          else if(OperationType =="Close all positions")       {
             relustAmount =(Shock_MaxAddCountLimit -(ShockTreadInfo.LadderIndex-1)) *TempAmount; //(Maximum Position Opening Amount - (Opening Ladder Index - 1) * Quantity == Current Held Position.
          }
       }      
    }
    else if(MarketTrendType =="trend")
    {
        if(TrendTreadInfo.ExtraAmount >=2)
        {
           TrendTreadInfo.ExtraAmount =2;
        }        
        
        if(Trend_ExtraAmount_State ==true) {//Increase value when enabled
           TempAmount =TrendTreadInfo.Amount +TrendTreadInfo.ExtraAmount; //Increase additional quantity
        }
        else  {
           TempAmount =TrendTreadInfo.Amount; //If not enabled, directly assign the base value
        }
        
        
       if(WarehouseMode ==true) //Add position mode
       {
          if(OperationType =="Admission")               {
             relustAmount =TempAmount;
          }
          else if(OperationType =="Increase or decrease positions")          {
             relustAmount =TempAmount;
          }
          else if(OperationType =="Close all positions")       {
             relustAmount =TrendTreadInfo.LadderIndex *TempAmount;
          }
       }
       else  //Reduce position mode
       {
          if(OperationType =="Admission")               {
             relustAmount =TempAmount*Trend_MaxAddCountLimit;
          }
          else if(OperationType =="Increase or decrease positions")         {
             relustAmount =TempAmount;             
          }
          else if(OperationType =="Close all positions")       {
             relustAmount =(Trend_MaxAddCountLimit -(TrendTreadInfo.LadderIndex-1)) *TempAmount; //(Maximum Position Opening Amount - (Opening Ladder Index - 1) * Quantity == Current Held Position.
          }
       }        
    }
  return relustAmount;
}


//Admission 
function Sys_In(MarketTrendType,ticker,records)
{
   if(MarketTrendType =="ranging market")
   {
      var HighPrice = TA.Highest(records, 14, 'High');
      var LowPrice  = TA.Lowest(records, 14, 'Low');

      if (HighPrice == 0 || LowPrice == 0) {
          return;
      }
    
      if(ShockTreadInfo.LastDirection !=STATE_LONG &&  ticker.Last < LowPrice)
     {//Long entry
         Log("Shock entry, currently holding a long position:",GetPosition(PD_LONG)[1],"Hold short position:",GetPosition(PD_SHORT)[1]);    
         
         exchange.SetDirection("buy"); //Set order type to long 
         exchange.Buy(ticker.Sell, CalcAmount("ranging market","Admission",Shock_WarehouseMode)); //with1000Price of, contract quantity is2Place Order 
         ShockTreadInfo.AdmissionBasePrice =ticker.Last;
         ShockTreadInfo.Direction   =STATE_LONG;
         ShockTreadInfo.LadderIndex =1;
         ShockTreadInfo.LastDirection =STATE_LONG;
         
        return true;
     }
     else if(ShockTreadInfo.LastDirection !=STATE_SHORT && ticker.Last > HighPrice)
     {//Short entry
         Log("Shock entry, currently holding a long position:",GetPosition(PD_LONG)[1],"Hold short position:",GetPosition(PD_SHORT)[1]);    
         
         exchange.SetDirection("sell");       //Set order type to short 
         exchange.Sell(ticker.Buy, CalcAmount("ranging market","Admission",Shock_WarehouseMode));      //with1000Price of, contract quantity is2Place Order   
         ShockTreadInfo.AdmissionBasePrice =ticker.Last;
         ShockTreadInfo.Direction   =STATE_SHORT;
         ShockTreadInfo.LadderIndex =1;
         ShockTreadInfo.LastDirection =STATE_SHORT;         
        return true;
     }      
   }
   else if(MarketTrendType =="trend")
   {

 //     var boll = TA.BOLL(records, 20, 2);
 //    var bollLength =boll[0].length;
 //    var upLine   = boll[0];
 //    var midLine  = boll[1];
 //    var downLine = boll[2];
      
    var HighPrice = TA.Highest(records, 25, 'High');
    var LowPrice = TA.Lowest(records, 25, 'Low');
       
       
   //   Log("Upper rail price:",upLine[bollLength -1],"Medium rail price:",midLine[bollLength -1],"Lower track price:",downLine[bollLength -1]);
       
      if(ticker.Buy >HighPrice)
      {// Long entry
     //    Log("Trend entry, currently holding a long position:",GetPosition(PD_LONG)[1],"Hold short position:",GetPosition(PD_SHORT)[1],"Upper rail price:",upLine[bollLength -1],"Medium rail price:",midLine[bollLength -1],"Lower track price:",downLine[bollLength -1],"Market price:",ticker.Last);    
                    
         exchange.SetDirection("buy"); //Set order type to long
         exchange.Buy(ticker.Sell, CalcAmount("trend","Admission",Trend_WarehouseMode)); //with1000Price of, contract quantity is2Place Order
         TrendTreadInfo.AdmissionBasePrice =ticker.Last;
         TrendTreadInfo.Direction   =STATE_LONG;
         TrendTreadInfo.LadderIndex =1;
      }
      else if(ticker.Sell < LowPrice)
      {// Short entry
    //     Log("Trend entry, currently holding a long position:",GetPosition(PD_LONG)[1],"Hold short position:",GetPosition(PD_SHORT)[1],"Upper rail price:",upLine[bollLength -1],"Medium rail price:",midLine[bollLength -1],"Lower track price:",downLine[bollLength -1],"Market price:",ticker.Last);    
                
         exchange.SetDirection("sell");       //Set order type to short 
         exchange.Sell(ticker.Buy, CalcAmount("trend","Admission",Trend_WarehouseMode));      //with1000Price of, contract quantity is2Place Order   
         TrendTreadInfo.AdmissionBasePrice =ticker.Last;
         TrendTreadInfo.Direction   =STATE_SHORT;
         TrendTreadInfo.LadderIndex =1;
      }
       
   }
   
       
}

//reduce position
function Sys_SubPosition(MarketTrendType,ticker,current_price,ATR_N)
{
    if(MarketTrendType =="ranging market")
    {
     if(ShockTreadInfo.LadderIndex >4 || ShockTreadInfo.LadderIndex ==-1)
     {
          ShockTreadInfo.AdmissionBasePrice =0;
          ShockTreadInfo.LadderIndex        =-1; 
          ShockTreadInfo.Direction          =STATE_IDLE;
          return false;
     }
    
   if(ShockTreadInfo.Direction ==STATE_LONG)
   { //Close long positions: Base price + 1/2 * ATR_N * step (used for statistics of opening positions).)

      if (current_price > (ShockTreadInfo.AdmissionBasePrice +Shock_Reduce_N*ATR_N[ATR_N.length -1] *ShockTreadInfo.LadderIndex))
      {  
          if(GetPosition(PD_LONG)[1] >= ShockTreadInfo.Amount)
          {
            exchange.SetDirection("closebuy");   //Close Long Position 
            var relust =exchange.Sell(ticker.Buy, CalcAmount("ranging market","Increase or decrease positions",Shock_WarehouseMode)); //with1000Price of, contract quantity is2Place Order 
            if(relust !=null )
            {
              ShockTreadInfo.LadderIndex++;  //Open position successfully, increase the ladder quantity        
              return true;
            }
          }
      }
   }
   else if(ShockTreadInfo.Direction ==STATE_SHORT)
   { //Reduce short position
    
      if (current_price < (ShockTreadInfo.AdmissionBasePrice -Shock_Reduce_N*ATR_N[ATR_N.length -1] *ShockTreadInfo.LadderIndex))
      {
          if(GetPosition(PD_SHORT)[1] >=ShockTreadInfo.Amount)
          {
           exchange.SetDirection("closesell"); 
           var relust =exchange.Buy(ticker.Sell, CalcAmount("ranging market","Increase or decrease positions",Shock_WarehouseMode));   //Buy to close short position    

           if(relust !=null )
           {
             ShockTreadInfo.LadderIndex++;  //Open position successfully, increase the ladder quantity    
             return true;               
           }
         }
      }
   }
    return false;        
        
    }
    else if(MarketTrendType =="trend")
    {
       if(TrendTreadInfo.LadderIndex >4 || TrendTreadInfo.LadderIndex ==-1)
       {
          TrendTreadInfo.AdmissionBasePrice =0;
          TrendTreadInfo.LadderIndex        =-1; 
          TrendTreadInfo.Direction          =STATE_IDLE;
          return false;
       }
    
      if(TrendTreadInfo.Direction ==STATE_LONG)
      { //Close long positions: Base price + 1/2 * ATR_N * step (used for statistics of opening positions).)

        if (current_price > (TrendTreadInfo.AdmissionBasePrice +Trend_Reduce_N*ATR_N[ATR_N.length -1] *TrendTreadInfo.LadderIndex))
        {  
            if(GetPosition(PD_LONG)[1] >= TrendTreadInfo.Amount)
            {
              exchange.SetDirection("closebuy");   //Close Long Position 
              var relust =exchange.Sell(ticker.Buy, CalcAmount("trend","Increase or decrease positions",Trend_WarehouseMode)); //with1000Price of, contract quantity is2Place Order 
              if(relust !=null )
              {
                TrendTreadInfo.LadderIndex++;  //Open position successfully, increase the ladder quantity        
                return true;
              }
            }
        }
      }
      else if(TrendTreadInfo.Direction ==STATE_SHORT)
      { //Reduce short position
    
         if (current_price < (TrendTreadInfo.AdmissionBasePrice -Trend_Reduce_N*ATR_N[ATR_N.length -1] *TrendTreadInfo.LadderIndex))
         {
            if(GetPosition(PD_SHORT)[1] >=TrendTreadInfo.Amount)
            {
              exchange.SetDirection("closesell"); 
              var relust =exchange.Buy(ticker.Sell, CalcAmount("trend","Increase or decrease positions",Trend_WarehouseMode));   //Buy to close short position    

              if(relust !=null )
              {
                TrendTreadInfo.LadderIndex++;  //Open position successfully, increase the ladder quantity    
                return true;               
              }
            }
          }
        }
        return false;
     }
}

//Add to position
function Sys_AddPosition(MarketTrendType,ticker,ATR_N)
{
   if(MarketTrendType =="ranging market")
   {
       if(ShockTreadInfo.LadderIndex >=Shock_MaxAddCountLimit)
       {
          return false;
       }
    
       if(ShockTreadInfo.Direction ==STATE_LONG)
       { //Add long positions: Base price + 1/2 * ATR_N * step (used for statistics of opening positions).)
          if (ticker.Sell > (ShockTreadInfo.AdmissionBasePrice +Shock_Reduce_N*ATR_N[ATR_N.length -1] *ShockTreadInfo.LadderIndex))
          {  
            exchange.SetDirection("buy"); //Set order type to long 
            exchange.Buy(ticker.Sell, CalcAmount("ranging market","Increase or decrease positions",Shock_WarehouseMode)); //with1000Price of, contract quantity is2Place Order           
            ShockTreadInfo.LadderIndex++;  //Open position successfully, increase the ladder quantity
            
            return true;
          }
       }
       else if(ShockTreadInfo.Direction ==STATE_SHORT)
       { //Increase short position
          if (ticker.Buy < (ShockTreadInfo.AdmissionBasePrice -Shock_Reduce_N*ATR_N[ATR_N.length -1] *ShockTreadInfo.LadderIndex))
          {
             exchange.SetDirection("sell");       //Set order type to short 
             exchange.Sell(ticker.Buy, CalcAmount("ranging market","Increase or decrease positions",Shock_WarehouseMode)); //with1000Price of, contract quantity is2Place Order    
             ShockTreadInfo.LadderIndex++;  //Open position successfully, increase the ladder quantity     
             return true;
          }
        }        
     }
     else if(MarketTrendType =="trend")
     {
         if(TrendTreadInfo.LadderIndex >=Trend_MaxAddCountLimit)
         {
            return false;
         }
    
       if(TrendTreadInfo.Direction ==STATE_LONG)
       { //Add long positions: Base price + 1/2 * ATR_N * step (used for statistics of opening positions).)
         if (ticker.Sell > (TrendTreadInfo.AdmissionBasePrice +Trend_Reduce_N*ATR_N[ATR_N.length -1] *TrendTreadInfo.LadderIndex))
         {  
           exchange.SetDirection("buy"); //Set order type to long 
           exchange.Buy(ticker.Sell,  CalcAmount("trend","Increase or decrease positions",Trend_WarehouseMode)); //with1000Price of, contract quantity is2Place Order           
           TrendTreadInfo.LadderIndex++;  //Open position successfully, increase the ladder quantity
           return true;
          }
        }
       else if(TrendTreadInfo.Direction ==STATE_SHORT)
       { //Increase short position
         if (ticker.Buy < (TrendTreadInfo.AdmissionBasePrice -Trend_Reduce_N*ATR_N[ATR_N.length -1] *TrendTreadInfo.LadderIndex))
         {
            exchange.SetDirection("sell");       //Set order type to short 
            exchange.Sell(ticker.Buy,  CalcAmount("trend","Increase or decrease positions",Trend_WarehouseMode)); //with1000Price of, contract quantity is2Place Order    
            TrendTreadInfo.LadderIndex++;  //Open position successfully, increase the ladder quantity     
            return true;
         }
       }
     }
    return false;
}



//Stop loss withatrValue as the stop-loss target..
function Stop_Loss(MarketTrendType,ticker,current_price,ATR_N)
{
   if(MarketTrendType =="ranging market")
   {
      if(ShockTreadInfo.Direction ==STATE_LONG)
      {
        //Calculate the last transaction price  LadderIndex[Index]-1 The reason is that after the position is established, the assigned value is1,Must reduce1Only then can the last open price be calculated.
        var LastPrice =ShockTreadInfo.AdmissionBasePrice + Shock_Reduce_N *ATR_N[ATR_N.length -1] *(ShockTreadInfo.LadderIndex-1);
   //      Log("Stop-loss trigger","current_price:",current_price,"ATR_N*2:",ATR_N[ATR_N.length -1]*2," Last transaction price:",LastPrice,"ATR_Nvalue:",ATR_N[ATR_N.length -1],"Ladder times:",LadderIndex[Index],"Basic price:",AdmissionBasePrice[Index]);
       
        //Still follows the Turtle rules, the maximum stop loss is price volatility2N
        if(LastPrice -current_price >ATR_N[ATR_N.length -1]*Shock_Stop_N)
        { //If it falls, it will be flat.
          var OldPostionAmount = GetPosition(PD_LONG)[1];
          for(var nCount =0;nCount <10;nCount++)
          {
             var PostionAmount = GetPosition(PD_LONG)[1];
             var CloseAmount =CalcAmount("ranging market","Close all positions",Shock_WarehouseMode); //(Maximum Position Opening Amount - (Opening Ladder Index - 1) * Quantity == Current Held Position.
             if(OldPostionAmount -CloseAmount >=PostionAmount || PostionAmount ==0 )     {
                break;
             }
            else if(CloseAmount >PostionAmount)
            {
               CloseAmount =PostionAmount;
            }              
              
             exchange.SetDirection("closebuy"); 
             exchange.Sell(ticker.Buy, CloseAmount);  //Sell to close long position     
             Sleep(1000);
             Log("Oscillation long position stop-loss, currently holding a long position:",GetPosition(PD_LONG)[1],"Hold short position:",GetPosition(PD_SHORT)[1],"Close Quantity:",CloseAmount);                
          }
          ShockTreadInfo.AdmissionBasePrice =0;
          ShockTreadInfo.LadderIndex        =-1;
          ShockTreadInfo.Direction          =STATE_IDLE;
          ShockTreadInfo.ExtraAmount        =0; // Additional Quantity
          return true;
        }
                 
      }
      else if(ShockTreadInfo.Direction ==STATE_SHORT)
      {
        //Calculate the last transaction price
        var LastPrice =ShockTreadInfo.AdmissionBasePrice - Shock_Reduce_N *ATR_N[ATR_N.length -1] *(ShockTreadInfo.LadderIndex-1);
        //Still follows the Turtle rules, the maximum stop loss is price volatility2N
        if(current_price -LastPrice >ATR_N[ATR_N.length -1]*Shock_Stop_N)
        {//If it rises, it will go short.
             var OldPostionAmount =GetPosition(PD_SHORT)[1];                
             for(var nCount =0;nCount <10;nCount++)
             {
                var PostionAmount =GetPosition(PD_SHORT)[1];
                var CloseAmount =CalcAmount("ranging market","Close all positions",Shock_WarehouseMode); //(Maximum Position Opening Amount - (Opening Ladder Index - 1) * Quantity == Current Held Position.
                if(OldPostionAmount -CloseAmount >=PostionAmount || PostionAmount ==0 )     {
                   break;
               }
               else if(CloseAmount >PostionAmount)
               {
                 CloseAmount =PostionAmount;
               }
                 
               exchange.SetDirection("closesell"); 
               exchange.Buy(ticker.Sell, CloseAmount);   //Buy to close short position     
               Sleep(1000);
             Log("Oscillation short position stop-loss, currently holding a long position:",GetPosition(PD_LONG)[1],"Hold short position:",GetPosition(PD_SHORT)[1],"Close Quantity:",CloseAmount);                   
             }
            ShockTreadInfo.AdmissionBasePrice =0;
            ShockTreadInfo.LadderIndex        =-1;
            ShockTreadInfo.Direction          =STATE_IDLE;
            ShockTreadInfo.ExtraAmount        =0; // Additional Quantity            
            return true;
       }
     }
   }
   else if(MarketTrendType =="trend")
   {
      if(TrendTreadInfo.Direction ==STATE_LONG)
      {
        //Calculate the last transaction price  LadderIndex[Index]-1 The reason is that after the position is established, the assigned value is1,Must reduce1Only then can the last open price be calculated.
        var LastPrice =TrendTreadInfo.AdmissionBasePrice + Trend_Reduce_N *ATR_N[ATR_N.length -1] *(TrendTreadInfo.LadderIndex-1);
   //      Log("Stop-loss trigger","current_price:",current_price,"ATR_N*2:",ATR_N[ATR_N.length -1]*2," Last transaction price:",LastPrice,"ATR_Nvalue:",ATR_N[ATR_N.length -1],"Ladder times:",LadderIndex[Index],"Basic price:",AdmissionBasePrice[Index]);
       
        //Still follows the Turtle rules, the maximum stop loss is price volatility2N
        if(LastPrice -current_price >ATR_N[ATR_N.length -1]*Trend_Stop_N)
        { //If it falls, it will be flat.
          var OldPostionAmount = GetPosition(PD_LONG)[1];
          for(var nCount =0;nCount <10;nCount++)
          {
             var PostionAmount = GetPosition(PD_LONG)[1];
             var CloseAmount =CalcAmount("trend","Close all positions",Trend_WarehouseMode);//(Maximum Position Opening Amount - (Opening Ladder Index - 1) * Quantity == Current Held Position.
             if(OldPostionAmount -CloseAmount >=PostionAmount || PostionAmount ==0 )     {
                break;
             }
            else if(CloseAmount >PostionAmount)
            {
               CloseAmount =PostionAmount;
            }
              
             exchange.SetDirection("closebuy"); 
             exchange.Sell(ticker.Buy, CloseAmount);  //Sell to close long position     
             Sleep(1000);
             Log(" Trend long position stop-loss, currently holding a long position:",GetPosition(PD_LONG)[1],"Hold short position:",GetPosition(PD_SHORT)[1],"Close Quantity:",CloseAmount);                
          }
          TrendTreadInfo.AdmissionBasePrice =0;
          TrendTreadInfo.LadderIndex        =-1;
          TrendTreadInfo.Direction          =STATE_IDLE;
          TrendTreadInfo.ExtraAmount        =0; // Additional Quantity            
          return true;
        }            
      }
      else if(TrendTreadInfo.Direction ==STATE_SHORT)
      {
        //Calculate the last transaction price
        var LastPrice =TrendTreadInfo.AdmissionBasePrice - Trend_Reduce_N *ATR_N[ATR_N.length -1] *(TrendTreadInfo.LadderIndex-1);
        //Still follows the Turtle rules, the maximum stop loss is price volatility2N
        if(current_price -LastPrice >ATR_N[ATR_N.length -1]*Trend_Stop_N)
        {//If it rises, it will go short.
             var OldPostionAmount =GetPosition(PD_SHORT)[1];                
             for(var nCount =0;nCount <10;nCount++)
             {
                var PostionAmount =GetPosition(PD_SHORT)[1];
                var CloseAmount =CalcAmount("trend","Close all positions",Trend_WarehouseMode);//(Maximum Position Opening Amount - (Opening Ladder Index - 1) * Quantity == Current Held Position.
                if(OldPostionAmount -CloseAmount >=PostionAmount || PostionAmount ==0 )     {
                   break;
               }
               else if(CloseAmount >PostionAmount)
               {
                 CloseAmount =PostionAmount;
               }
                 
               exchange.SetDirection("closesell"); 
               exchange.Buy(ticker.Sell, CloseAmount);   //Buy to close short position     
               Sleep(1000);
             Log("Trend short position stop-loss, currently holding a long position:",GetPosition(PD_LONG)[1],"Hold short position:",GetPosition(PD_SHORT)[1],"Close Quantity:",CloseAmount);                   
             }
            TrendTreadInfo.AdmissionBasePrice =0;
            TrendTreadInfo.LadderIndex        =-1;
            TrendTreadInfo.Direction          =STATE_IDLE;
            TrendTreadInfo.ExtraAmount        =0;  // Additional Quantity
            return true;
       }
     }      
   }
    
    return false;
}

//  Leave 
function Sys_OutClosePosition(MarketTrendType,ticker,records,positions,ATR_N)
{
   if(MarketTrendType =="ranging market")
   {
       
      if(ShockTreadInfo.Direction ==STATE_LONG)
      {
         var HighPrice = TA.Highest(records, 14, 'High');
          
          //Calculate the next increase price. If the current price is greater than the current price, leave the market directly..
         var NextAddPrice =ShockTreadInfo.AdmissionBasePrice +Shock_Reduce_N*ATR_N[ATR_N.length -1] *ShockTreadInfo.LadderIndex;
          
         if(ticker.Last > HighPrice || (ticker.Last > NextAddPrice && ShockTreadInfo.LadderIndex >=Shock_MaxAddCountLimit))
         {//Long Exit
         
             var CloseAmount =CalcAmount("ranging market","Close all positions",Shock_WarehouseMode); //(Maximum Position Opening Amount - (Opening Ladder Index - 1) * Quantity == Current Held Position.  
             if(CloseAmount !=0)
             {
               exchange.SetDirection("closebuy");
               exchange.Sell(ticker.Buy, CloseAmount);  //Sell to close long position
             }
              ShockTreadInfo.AdmissionBasePrice =0;
              ShockTreadInfo.Direction          =STATE_IDLE;
              ShockTreadInfo.LadderIndex        =-1;
              ShockTreadInfo.ExtraAmount        ++;  // Additional Quantity    
              Log("Oscillation long position exit, currently holding a long position:",GetPosition(PD_LONG)[1],"Hold short position:",GetPosition(PD_SHORT)[1],"Close Quantity:",CloseAmount);        
            return true;
          }          
      }
      else if(ShockTreadInfo.Direction ==STATE_SHORT)
      {//Short Exit
        var LowPrice = TA.Lowest(records, 14, 'Low');
          
        var NextSbuPrice =ShockTreadInfo.AdmissionBasePrice - Shock_Reduce_N *ATR_N[ATR_N.length -1] *(ShockTreadInfo.LadderIndex);
          
         if(ticker.Last < LowPrice || (ticker.Last < NextSbuPrice && ShockTreadInfo.LadderIndex >=Shock_MaxAddCountLimit))
         {            
             var CloseAmount =CalcAmount("ranging market","Close all positions",Shock_WarehouseMode); //(Maximum Position Opening Amount - (Opening Ladder Index - 1) * Quantity == Current Held Position.
             if(CloseAmount !=0)
             {
               exchange.SetDirection("closesell"); 
               exchange.Buy(ticker.Sell, CloseAmount);   //Buy to close short position
             }
              ShockTreadInfo.AdmissionBasePrice =0;
              ShockTreadInfo.Direction          =STATE_IDLE;
              ShockTreadInfo.LadderIndex        =-1;
              ShockTreadInfo.ExtraAmount        ++;  // Additional Quantity                 
              Log("Oscillation short position exit, currently holding a long position:",GetPosition(PD_LONG)[1],"Hold short position:",GetPosition(PD_SHORT)[1],"Close Quantity:",CloseAmount);              
            return true;
          }                   
      }
       
       
   }
   else if(MarketTrendType =="trend")
   {
//      var boll = TA.BOLL(records, 14, 2);  //Here the value was originally20,Corrected to14Seems to work better?
//      var bollLength =boll[0].length;
//      var upLine   = boll[0];
//      var midLine  = boll[1];
//      var downLine = boll[2];
      
    var HighPrice = TA.Highest(records, 14, 'High');
    var LowPrice = TA.Lowest(records, 14, 'Low');      
       
       
   //   Log("Upper rail price:",upLine[bollLength -1],"Medium rail price:",midLine[bollLength -1],"Lower track price:",downLine[bollLength -1]);
       
      if( TrendTreadInfo.Direction ==STATE_LONG )
      {// Long Exit
          if(ticker.Buy <LowPrice)
          {
              var CloseAmount =CalcAmount("trend","Close all positions",Trend_WarehouseMode);//(Maximum Position Opening Amount - (Opening Ladder Index - 1) * Quantity == Current Held Position.          
              exchange.SetDirection("closebuy");
              exchange.Sell(ticker.Buy, CloseAmount);  //Sell to close long position
             
              TrendTreadInfo.AdmissionBasePrice =0;
              TrendTreadInfo.Direction          =STATE_IDLE;
              TrendTreadInfo.LadderIndex        =-1;
              TrendTreadInfo.ExtraAmount        ++;  // Additional Quantity
              Log("Trend long position exit, currently holding a long position:",GetPosition(PD_LONG)[1],"Hold short position:",GetPosition(PD_SHORT)[1],"Close Quantity:",CloseAmount);        
              return true;
          }
      }
      else if(TrendTreadInfo.Direction ==STATE_SHORT )
      {// Short Exit
          if(ticker.Sell >HighPrice)
          {
              var CloseAmount =CalcAmount("trend","Close all positions",Trend_WarehouseMode); //(Maximum Position Opening Amount - (Opening Ladder Index - 1) * Quantity == Current Held Position.          
              exchange.SetDirection("closesell"); 
              exchange.Buy(ticker.Sell, CloseAmount);   //Buy to close short position
             
              TrendTreadInfo.AdmissionBasePrice =0;
              TrendTreadInfo.Direction          =STATE_IDLE;
              TrendTreadInfo.LadderIndex        =-1;
              TrendTreadInfo.ExtraAmount        ++;  // Additional Quantity
              Log("Trend short position exit, currently holding a long position:",GetPosition(PD_LONG)[1],"Hold short position:",GetPosition(PD_SHORT)[1],"Close Quantity:",CloseAmount);              
              return true;
           }      
      }
              
   }

}
 

//Pullback Exit
function CallbackDeparture(MarketTrendType,ticker,current_price,ATR_N)
{
    if(MarketTrendType =="ranging market")
    {
 
      if(ShockTreadInfo.Direction ==STATE_LONG && ShockTreadInfo.LadderIndex >2)
      {
        //Calculate the last transaction price  ShockTreadInfo.LadderIndex-1 The reason is that after the position is established, the assigned value is1,Must reduce1Only then can the last open price be calculated.
        var LastPrice =ShockTreadInfo.AdmissionBasePrice + 0.5 *ATR_N[ATR_N.length -1] *(ShockTreadInfo.LadderIndex-1);
        var BackedPrice =ShockTreadInfo.AdmissionBasePrice + 0.5 *ATR_N[ATR_N.length -1] *(ShockTreadInfo.LadderIndex-2);    //Previous price, if it falls back to the previous price, the loss will be stopped directly    
   //      Log("Stop-loss trigger","current_price:",current_price,"ATR_N*2:",ATR_N[ATR_N.length -1]*2," Last transaction price:",LastPrice,"ATR_Nvalue:",ATR_N[ATR_N.length -1],"Ladder times:",ShockTreadInfo.LadderIndex,"Basic price:",ShockTreadInfo.AdmissionBasePrice);
        
        // If the current price is less than the opening level-2If the price is , it indicates a pullback, exit directly, stop-loss..
        if(current_price <BackedPrice)
        { //If it falls, it will be flat.
          var OldPostionAmount = GetPosition(PD_LONG)[1];            
          for(var nCount =0;nCount <10;nCount++)
          {
             var PostionAmount = GetPosition(PD_LONG)[1];
             var CloseAmount =CalcAmount("ranging market","Close all positions",Shock_WarehouseMode); //(Maximum Position Opening Amount - (Opening Ladder Index - 1) * Quantity == Current Held Position.
             if(OldPostionAmount -CloseAmount >=PostionAmount || PostionAmount ==0 )     {
                break;
             }
            else if(CloseAmount >PostionAmount)
            {
               CloseAmount =PostionAmount;
            }              
              
             exchange.SetDirection("closebuy"); 
             exchange.Sell(ticker.Buy, CloseAmount);  //Sell to close long position     
             Sleep(1000);
          }
          ShockTreadInfo.AdmissionBasePrice =0;
          ShockTreadInfo.LadderIndex =-1;
          ShockTreadInfo.Direction =STATE_IDLE;     
         return true;
        }
      }
      else if(ShockTreadInfo.Direction ==STATE_SHORT && ShockTreadInfo.LadderIndex >2)
      {
        //Calculate the last transaction price
        var LastPrice =ShockTreadInfo.AdmissionBasePrice - 0.5 *ATR_N[ATR_N.length -1] *(ShockTreadInfo.LadderIndex-1);
        var BackedPrice  =ShockTreadInfo.AdmissionBasePrice - 0.5 *ATR_N[ATR_N.length -1] *(ShockTreadInfo.LadderIndex-2);
        //Current price > pullback price, indicates a pullback, stop loss and exit
        if(current_price  >BackedPrice)
        {//If it rises, it will go short.
             var OldPostionAmount =GetPosition(PD_SHORT)[1];                
             for(var nCount =0;nCount <10;nCount++)
             {
                var PostionAmount =GetPosition(PD_SHORT)[1];
                var CloseAmount =CalcAmount("ranging market","Close all positions",Shock_WarehouseMode); //(Maximum Position Opening Amount - (Opening Ladder Index - 1) * Quantity == Current Held Position.
                if(OldPostionAmount -CloseAmount >=PostionAmount || PostionAmount ==0 )     {
                   break;
               }
               else if(CloseAmount >PostionAmount)
               {
                 CloseAmount =PostionAmount;
               }                 
                 
               exchange.SetDirection("closesell"); 
               exchange.Buy(ticker.Sell, CloseAmount);   //Buy to close short position     
               Sleep(1000);
             }
            ShockTreadInfo.AdmissionBasePrice =0;
            ShockTreadInfo.LadderIndex =-1; 
            ShockTreadInfo.Direction   =STATE_IDLE;
            return true;       
         }
       }
    }
    else if(MarketTrendType =="trend")
    {
 
      if(TrendTreadInfo.Direction ==STATE_LONG && TrendTreadInfo.LadderIndex >2)
      {
        //Calculate the last transaction price  TrendTreadInfo.LadderIndex-1 The reason is that after the position is established, the assigned value is1,Must reduce1Only then can the last open price be calculated.
        var LastPrice =TrendTreadInfo.AdmissionBasePrice + 0.5 *ATR_N[ATR_N.length -1] *(TrendTreadInfo.LadderIndex-1);
        var BackedPrice =TrendTreadInfo.AdmissionBasePrice + 0.5 *ATR_N[ATR_N.length -1] *(TrendTreadInfo.LadderIndex-2);    //Previous price, if it falls back to the previous price, the loss will be stopped directly    
   //      Log("Stop-loss trigger","current_price:",current_price,"ATR_N*2:",ATR_N[ATR_N.length -1]*2," Last transaction price:",LastPrice,"ATR_Nvalue:",ATR_N[ATR_N.length -1],"Ladder times:",TrendTreadInfo.LadderIndex,"Basic price:",TrendTreadInfo.AdmissionBasePrice);
        
        // If the current price is less than the opening level-2If the price is , it indicates a pullback, exit directly, stop-loss..
        if(current_price <BackedPrice)
        { //If it falls, it will be flat.
          var OldPostionAmount = GetPosition(PD_LONG)[1];            
          for(var nCount =0;nCount <10;nCount++)
          {
             var PostionAmount = GetPosition(PD_LONG)[1];
             var CloseAmount =CalcAmount("trend","Close all positions",Trend_WarehouseMode); //(Maximum Position Opening Amount - (Opening Ladder Index - 1) * Quantity == Current Held Position.
             if(OldPostionAmount -CloseAmount >=PostionAmount || PostionAmount ==0 )     {
                break;
             }
            else if(CloseAmount >PostionAmount)
            {
               CloseAmount =PostionAmount;
            }              
              
             exchange.SetDirection("closebuy"); 
             exchange.Sell(ticker.Buy, CloseAmount);  //Sell to close long position     
             Sleep(1000);
          }
          TrendTreadInfo.AdmissionBasePrice =0;
          TrendTreadInfo.LadderIndex =-1;
          TrendTreadInfo.Direction =STATE_IDLE;     
         return true;
        }
    }
    else if(TrendTreadInfo.Direction ==STATE_SHORT && TrendTreadInfo.LadderIndex >2)
    {
        //Calculate the last transaction price
        var LastPrice =TrendTreadInfo.AdmissionBasePrice - 0.5 *ATR_N[ATR_N.length -1] *(TrendTreadInfo.LadderIndex-1);
        var BackedPrice  =TrendTreadInfo.AdmissionBasePrice - 0.5 *ATR_N[ATR_N.length -1] *(TrendTreadInfo.LadderIndex-2);
        //Current price > pullback price, indicates a pullback, stop loss and exit
        if(current_price  >BackedPrice)
        {//If it rises, it will go short.
             var OldPostionAmount =GetPosition(PD_SHORT)[1];                
             for(var nCount =0;nCount <10;nCount++)
             {
                var PostionAmount =GetPosition(PD_SHORT)[1];
                var CloseAmount =CalcAmount("trend","Close all positions",Trend_WarehouseMode); //(Maximum Position Opening Amount - (Opening Ladder Index - 1) * Quantity == Current Held Position.
                if(OldPostionAmount -CloseAmount >=PostionAmount || PostionAmount ==0 )     {
                   break;
               }
               else if(CloseAmount >PostionAmount)
               {
                 CloseAmount =PostionAmount;
               }                 
                 
               exchange.SetDirection("closesell"); 
               exchange.Buy(ticker.Sell, CloseAmount);   //Buy to close short position     
               Sleep(1000);
             }
            TrendTreadInfo.AdmissionBasePrice =0;
            TrendTreadInfo.LadderIndex  =-1;
            TrendTreadInfo.Direction    =STATE_IDLE;
            return true;       
        }
      }          
    }
return false;
}




//Processing Procedure
function MarketTrendProc(MarketTrendType,records,IsOpeningAllowed)
{
    var positions  = _C(exchange.GetPosition); //Get Position Information 
    var ticker     = _C(exchange.GetTicker);   //Market price
    var account    = _C(exchange.GetAccount);  //Get account information    
    
    var curTotalAccount =account.Stocks +account.FrozenStocks
    
    if (account.Stocks < 0.01) //Insufficient margin
    {
        return;
    }
    
    
   if(MarketTrendType =="ranging market")
   {

       if(ShockTreadInfo.LadderIndex ==-1 && IsOpeningAllowed ==true) 
       {//Position establishment detection
         Shock_ATR  = TA.ATR(records,Shock_ATR_Cycle);    
         ShockTreadInfo.Amount =CalculationAmount(Shock_UseLeverval,ticker, account, Shock_ATR,Shock_Stop_N, 1,1);         
         if(Sys_In("ranging market",ticker,records)==true)
         {
            Log("Enter the market - Index:","ranging market","current_price",ticker.Last,"Compare prices:",ShockTreadInfo.AdmissionBasePrice -Shock_Reduce_N*Shock_ATR[Shock_ATR.length -1] *ShockTreadInfo.LadderIndex,"Most Recent CandleATR:",Shock_ATR[Shock_ATR.length -1]);               
         }
       }
        else
        { //reduce position
            if(Shock_WarehouseMode ==true)
            {
               if(Sys_AddPosition("ranging market",ticker,Shock_ATR) ==true)
               {
                  Log("Add to position - Index:","ranging market","current_price",ticker.Last,"Long position comparison price:",ShockTreadInfo.AdmissionBasePrice +Shock_Reduce_N*Shock_ATR[Shock_ATR.length -1] *ShockTreadInfo.LadderIndex,"Short position comparison price:",ShockTreadInfo.AdmissionBasePrice -Shock_Reduce_N*Shock_ATR[Shock_ATR.length -1] *ShockTreadInfo.LadderIndex,"Most Recent CandleATR:",Shock_ATR[Shock_ATR.length -1]);                         
               }
            }
            else
            {
               if(Sys_SubPosition("ranging market",ticker,ticker.Last,Shock_ATR) ==true)
               {
                  Log("reduce position - Index:","ranging market","current_price",ticker.Last,"Long position comparison price:",ShockTreadInfo.AdmissionBasePrice +Shock_Reduce_N*Shock_ATR[Shock_ATR.length -1] *ShockTreadInfo.LadderIndex,"Short position comparison price:",ShockTreadInfo.AdmissionBasePrice -Shock_Reduce_N*Shock_ATR[Shock_ATR.length -1] *ShockTreadInfo.LadderIndex,"Most Recent CandleATR:",Shock_ATR[Shock_ATR.length -1]);                         
               }
            }
        }
    
    
        if(ShockTreadInfo.LadderIndex !=-1)
        {
        //stop loss
          if(Stop_Loss("ranging market",ticker,ticker.Last,Shock_ATR) ==true)
          {
            Log("Index:","ranging market","Stop Loss Successful!!","ATRvalue:",Shock_ATR[Shock_ATR.length -1] ,"ticker.Last:",ticker.Last,"Account Profit:",curTotalAccount -InitAccount.Stocks);
          }
          else if(Sys_OutClosePosition("ranging market",ticker,records,positions,Shock_ATR) ==true)
          {
            Log("Index:","ranging market","Exit Successful!!","ATRvalue:",Shock_ATR[Shock_ATR.length -1] ,"ticker.Last",ticker.Last,"Account Profit:",curTotalAccount -InitAccount.Stocks);
          }
         else if(CallbackDeparture("ranging market",ticker,ticker.Last,Shock_ATR) ==true)
         {
           Log("Index:","Oscillation Retracement Stop loss successful!!","ATRvalue:",Shock_ATR[Shock_ATR.length -1],"ticker.Last:",ticker.Last,"Account Profit:",curTotalAccount -InitAccount.Stocks);            
         }                 
        }
     }
    else if(MarketTrendType =="trend")
    {
       if(TrendTreadInfo.LadderIndex ==-1 && IsOpeningAllowed ==true) 
       {//Position establishment detection
         Trend_ATR  = TA.ATR(records,Trend_ATR_Cycle);  
         TrendTreadInfo.Amount =CalculationAmount(Trend_UseLeverval,ticker, account, Trend_ATR,Trend_Stop_N,1,1);           
         if(Sys_In("trend",ticker,records)==true)
         {
            Log("Enter the market - Index:","trend","current_price",ticker.Last,"Compare prices:",TrendTreadInfo.AdmissionBasePrice -Trend_Reduce_N*Trend_ATR[Trend_ATR.length -1] *TrendTreadInfo.LadderIndex,"Most Recent CandleATR:",Trend_ATR[Trend_ATR.length -1]);               
         }
       }
        else
        { //Reduce or increase position
            if(Trend_WarehouseMode ==true)
            {
               if(Sys_AddPosition("trend",ticker,Trend_ATR) ==true)
               {
                   Log("Add to position - Index:","trend","current_price",ticker.Last,"Long position comparison price:",TrendTreadInfo.AdmissionBasePrice +Trend_Reduce_N*Trend_ATR[Trend_ATR.length -1] *TrendTreadInfo.LadderIndex,"Short position comparison price:",TrendTreadInfo.AdmissionBasePrice -Trend_Reduce_N*Trend_ATR[Trend_ATR.length -1] *TrendTreadInfo.LadderIndex,"Most Recent CandleATR:",Trend_ATR[Trend_ATR.length -1]);                      
               }
            }
            else 
            {
               if(Sys_SubPosition("trend",ticker,ticker.Last,Trend_ATR) ==true)
               {
                   Log("reduce position - Index:","trend","current_price",ticker.Last,"Long position comparison price:",TrendTreadInfo.AdmissionBasePrice +Trend_Reduce_N*Trend_ATR[Trend_ATR.length -1] *TrendTreadInfo.LadderIndex,"Short position comparison price:",TrendTreadInfo.AdmissionBasePrice -Trend_Reduce_N*Trend_ATR[Trend_ATR.length -1] *TrendTreadInfo.LadderIndex,"Most Recent CandleATR:",Trend_ATR[Trend_ATR.length -1]);                      
               }
            }
        }
    
        if(TrendTreadInfo.LadderIndex !=-1)
        {  //stop loss
          if(Stop_Loss("trend",ticker,ticker.Last,Trend_ATR) ==true)
          {
            Log("Index:","trend","Stop Loss Successful!!","ATRvalue:",Trend_ATR[Trend_ATR.length -1] ,"ticker.Last:",ticker.Last,"Account Profit:",curTotalAccount -InitAccount.Stocks);
          }
          else if(Sys_OutClosePosition("trend",ticker,records,positions,Trend_ATR) ==true)
          {
            Log("Index:","trend","Exit Successful!!","ATRvalue:",Trend_ATR[Trend_ATR.length -1] ,"ticker.Last",ticker.Last,"Account Profit:",curTotalAccount -InitAccount.Stocks);
          }
          else if(CallbackDeparture("trend",ticker,ticker.Last,Trend_ATR) ==true)
          {
           Log("Index:","Trend Retracement Stop loss successful!!","ATRvalue:",Trend_ATR[Trend_ATR.length -1],"ticker.Last:",ticker.Last,"Account Profit:",curTotalAccount -InitAccount.Stocks);            
          }                          
        }           
     
    }
}


function onTick(exchange) {
    var recordsCMI        = _C(exchange.GetRecords,GetKLineCycle(Cmi_kLine_Cycle));     //CmiCalculation
    var Shock_records     = _C(exchange.GetRecords,GetKLineCycle(Shock_kLine_Cycle));   //ranging marketkLine
    var Trend_records     = _C(exchange.GetRecords,GetKLineCycle(Trend_kLine_Cycle));   //trendkLine
    
    var Bar = Shock_records[Shock_records.length - 1];
    if (LastBarTime !== Bar.Time) {
       
      CmiVal = GetCmiVal(recordsCMI);  
        
      if(CmiVal <20)           {          Log("Life Goes On!!");             }
      else if(CmiVal >=20)     {          Log("Recklessness Never Stops!!");             }
        
      LastBarTime = Bar.Time;        
    }
    


        if(CmiVal <20)
        {
            MarketTrendProc("ranging market",Shock_records,true);
            MarketTrendProc("Trend",Trend_records,false); // Opening positions not allowed            
        }
        else if(CmiVal >=20)
        {
            MarketTrendProc("trend",Trend_records,true);
            MarketTrendProc("Volatility", Shock_records, false); No open positions allowed        
        }    
    
    
    
}


function main() {
    
    Log(exchange.GetAccount());
    Log(exchange.GetCurrency(), "Contract face value:", GetContractFcaeValue(), "Test conversion to integer:", _N(3.143454515, 0));

    if (exchange.GetName() !== 'Futures_OKCoin') {
      //  throw "Only support OKEX features";
    }
    exchange.SetRate(1);
    exchange.SetContractType(["this_week", "next_week", "quarter"][ContractTypeIdx]);
    exchange.SetMarginLevel([10, 20][MarginLevelIdx]);
    InitAccount = LastAccount = exchange.GetAccount();    
    
    Log(exchange.GetAccount());
    
    while (true) {
        onTick(exchange);
        Sleep(LoopInterval * 1000);
    }
    
}
```

> Detail

https://www.fmz.com/strategy/255502

> Last Modified

2022-03-13 05:18:54
