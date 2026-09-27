
> Name

Open-a-Reverse-Order-When-Someone-Liquidates-Their-Position

> Author

Exodus[策略代写]

> Strategy Description

Someone asked me to write a strategy, then didn't want it after it was finished and didn't pay
I just wrote it in vain, wishing him a coupon for buying a coffin.
Strategy does not support backtesting.
This strategy only supports currency standard. After selecting the currency, it will detect the liquidation order of the corresponding currency. If there is a short order and it is liquidated, it will open a long position. If there are many orders and it is liquidated, it will be a short position. No closing logic.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|openDistance|false|Pending order distance (percentage, if it is 0, it is a market order)|
|cancelOrderTime|true|Order cancellation time (how long an order remains unfilled before being canceled, unit: minutes))|
|tickPeriod|15|Detection cycle (seconds))|
|margin|20|Leverage multiple|
|buyMinute|-1|(For testing) Buy timing|
|sellMinute|-1|(For testing) Sell timing|
|contractType|swap|Contract Type|
|orderType|0|Order method: Fixed number of sheets|Balance percentage|
|orderVolume|3|Order quantity (corresponding to the method of placing orders by number of contracts or percentage))|
|qtyValueSequence|0.4626,|Contract quantity sequence, how many coins correspond to one contract|
|xbtApi|false|Use Coin-denominatedAPI|


> Source (javascript)

``` javascript
/*backtest
start: 2021-05-07 00:00:00
end: 2021-08-04 00:00:00
period: 15m
basePeriod: 5m
exchanges: [{"eid":"Futures_Binance","currency":"LTC_USDT","balance":200},{"eid":"Futures_Binance","currency":"BTC_USDT","balance":500},{"eid":"Futures_Binance","currency":"ETH_USDT","balance":200},{"eid":"Futures_Binance","currency":"EOS_USDT","balance":500},{"eid":"Futures_Binance","currency":"BCH_USDT","balance":500}]
args: [["stopProfitRate",100],["cancelOrderTime",15]]
*/

class MyExchange{
    constructor(tExchange,tIndex,tQtyValue){
        this.exchange=tExchange;       
        this.getThis=()=>this;
        this.exchange.SetContractType(contractType);
        this.exchange.SetMarginLevel(margin);
        
        this.currency=this.exchange.GetCurrency();
        let precision = $.GetPrecision(this.exchange);
        this.pricePrecision = $.GetPricePrecision(this.currency);
        this.amountPrecision = $.GetAmountPrecision(this.currency);
        
        this.index=tIndex;
        this.qtyValue=tQtyValue;
        
        //Coin-margined account funds
        this.walletBalance=0;
        this.unrealizedProfit=0;
        this.marginBalance=0;
        this.availableBalance=0;
        
        this.exchange.SetMaxBarLen(2000);
        
        //RegisterwssLink
        let eName = this.currency.replace("_", "").toLowerCase();
        let symbol=eName+"t@forceOrder";
        if(xbtApi)
            symbol=eName+"@forceOrder";
        //let symbol=eName+"t@aggTrade";
        let str = "wss://fstream.binance.com/ws/" + symbol + "|reconnect=true";
        this.streamClient=Dial(str);
        Log(this.currency+"wssLink is:"+str);
    }
    
    Open(direction,curPrice,distance){
        let pricePrecision=this.pricePrecision;
        let amountPrecision=this.amountPrecision;
        //Log("Price Precision",pricePrecision,"Quantity Precision",amountPrecision);
        if(this.walletBalance==0)
            return;
        let orderAmount = orderVolume;
        if(orderType==1){//Percentage
            if(xbt)
                orderAmount=Math.floor(Math.floor(this.walletBalance/this.qtyValue)*0.01*orderVolume);//Number of Shares               
        }
        
        if($.GetPosByDirection(PD_LONG,this.exchange)==null && direction==PD_LONG){//Only open one long position at a time
            Log(this.exchange.GetCurrency(),"Place long order");
            this.exchange.SetDirection("buy");
            if(xbt)
                this.exchange.Buy(distance==0?-1:_N(curPrice*(1-0.01*distance),pricePrecision),orderAmount);//Zhang
            else
                this.exchange.Buy(distance==0?-1:_N(curPrice*(1-0.01*distance),pricePrecision),_N((buyVolume/curPrice)*margin,amountPrecision));
           
            
        }
         if($.GetPosByDirection(PD_SHORT,this.exchange)==null && direction==PD_SHORT){
            this.exchange.SetDirection("sell");
            Log(this.exchange.GetCurrency(),"Place short order");
            if(xbt)
                this.exchange.Sell(distance==0?-1:_N(curPrice*(1+0.01*distance),pricePrecision),orderAmount); //Zhang
            else
                this.exchange.Sell(distance==0?-1:_N(curPrice*(1+0.01*distance),pricePrecision),_N((buyVolume/curPrice)*margin,amountPrecision));  
           
        }
    }
    
    UpdateBalance(walletBalance,unrealizedProfit,marginBalance,availableBalance){
        this.walletBalance=walletBalance;
        this.unrealizedProfit=unrealizedProfit;
        this.marginBalance=marginBalance;
        this.availableBalance=availableBalance;//Synchronize funds for opening position method
    }
    run(){
           let buy=false;
           let sell=false;
       
            let socketRs = null;
           
            try {
                socketRs = JSON.parse(this.streamClient.read(-2));//Obtainwebsocket
            } catch (e) {
                socketRs = null;
                //Log('Get price anomaly(Does not affect program operation):',e); 
            }
            //Log(socketRs);
            if (socketRs == null || typeof(socketRs) == "undefined") {
                //Log("Failed to get market information................");        
            } else {
                let o = socketRs.o;
                Log("Received forced liquidation information,socketRs.ois:",o);
                if(o.S=="SELL")
                    buy=true;
                if(o.S=="BUY")
                    sell=true;
            }
        
     
        
        
        //Close missed opened orders
        let orders=_C(this.exchange.GetOrders);
        for(let i=0;i<orders.length;i++){
           
            if(orders[i]!=null && Math.floor(_N((Unix()*1000-orders[i].Info.time)/(PERIOD_M1*1000),1))>=cancelOrderTime){
                Log("Detected opening order process"+cancelOrderTime+"Not executed even after minutes");
                Log("Cancel open orders");                
                this.exchange.CancelOrder(orders[i].Id,orders[i]);
                
            }
             
        }
       
        
        let curMinute=new Date().getMinutes();
        //Test
        if(curMinute==buyMinute)
            buy=true;
        if(curMinute==sellMinute)
            sell=true;
        if(buy){
            Log("Buy Start");
            let shortPos=$.GetPosByDirection(PD_SHORT,this.exchange);
            if(shortPos)
                $.CloseAmount(PD_SHORT,shortPos.Amount,shortPos,this.exchange);//close short
            $.CancelAllOrder(this.exchange);//Clear all orders
            let curPrice=_C(this.exchange.GetTicker).Last;
            this.Open(PD_LONG,curPrice,openDistance);//open long
        } 
        if(sell){
            Log("Sell Start");
            let longPos=$.GetPosByDirection(PD_LONG,this.exchange);
            if(longPos)
                $.CloseAmount(PD_LONG,longPos.Amount,longPos,this.exchange);//close long
            $.CancelAllOrder(this.exchange);//Clear all orders
            let curPrice=_C(this.exchange.GetTicker).Last;
            this.Open(PD_SHORT,curPrice,openDistance);
        }
        
        table.rows.push([this.currency,this.walletBalance,this.unrealizedProfit,this.marginBalance,this.availableBalance]);
       
    }
}
function GetAllBalance(exchange){
   
    let account=_C(exchange.GetAccount);
    let info=account.Info;
    let assets=info.assets;
    /*let totalWalletBalance=info.totalWalletBalance;//Wallet Balance
    let canUseBalance=account.Balance;//Available balance
    let frozenBalance=account.FrozenBalance;
    let frozenStocks=account.FrozenStocks;
    return {totalWalletBalance,canUseBalance,frozenBalance,frozenStocks};*/
    return {account,assets};
}

function FindExchange(currency){
    for(let myE of myExchanges){
        //Log(myE.currency,currency);
        if(myE.currency==currency){
            return myE.getThis();
        }
    }
}


var lastRunSecond = 0;

var myExchanges=new Array();
let qtyValueArray=new Array();
var xbt=true;
function main() {
   
    if(_G("profit")){
        LogProfit(_G("profit"));
    }else{
        _G("profit",0);
        LogProfit(0);
    }
   
    qtyValueArray=qtyValueSequence.split(",");
    for (let i = 0; i < exchanges.length; i++) {

        myExchanges.push(new MyExchange(exchanges[i],i,parseFloat(qtyValueArray[i])));
    }
    
     table = {
            type: "table",
            title: "Account Information",
            cols: [""Currency","Wallet Balance","Unrealized P/L","Margin Balance","Available Balance for Orders""],
            rows: [

            ]
        }
    
    /*if (IsVirtual() == false) {
        var symbols = "";
        for (let i = 0; i < exchanges.length; i++) {
            let e = exchanges[i];
            let eName = e.GetCurrency().replace("_", "").toLowerCase();
            symbols += eName + "@forceOrder" + (i == exchanges.length - 1 ? "" : "/");

        }

        let str = "wss://fstream.binance.com/stream?streams=" + symbols + "|reconnect=true";
        let str1="wss://fstream.binance.com/stream?streams=!forceOrder@arr|reconnect=true"
        Log("websocketRequest link is:" + str1);
        streamClient = Dial(str1);
    }*/
    
    while(true){
        
        let date = new Date();
        let curMinute = date.getMinutes();
        
       
         /*if(useTKTick && Math.abs( curSecond - lastCloseSecond)> basePeriod ){
            //Log("Check Price");
            for(let myE of myExchanges){
                myE.getThis().CloseImmidiate();
                //Log("Real-time Take Profit");
            }
            lastCloseSecond=Unix();
        }*/

        if (Unix() - lastRunSecond > tickPeriod ) {
           table.rows.length=0;
            for (let myE of myExchanges) {
                myE.getThis().run();
            }
            lastRunSecond = Unix();
            
            //Print account information
            let balance=GetAllBalance(exchange);
            let account=balance.account;
            let assets=balance.assets;
            for(let i=0;i<assets.length;i++){
                let asset=assets[i];
                //table.rows.push([asset.asset+"USD",asset.walletBalance,asset.unrealizedProfit,asset.marginBalance,asset.availableBalance]);
                let e=FindExchange(asset.asset+"_USD");
                if(e!=null)
                    e.UpdateBalance(asset.walletBalance,asset.unrealizedProfit,asset.marginBalance,asset.availableBalance);
                //Log(asset.walletBalance,asset.unrealizedProfit,asset.marginBalance,asset.availableBalance);
            }
            
            LogStatus("`" + JSON.stringify(table) + "`")
        }

        let curMillSecond = date.getMilliseconds();
        Sleep(1000 - curMillSecond);
    }
    
}

function onexit(){    
         Log("Cancel all orders");
         for(let e of exchanges){
            let orders= _C(e.GetOrders);
            for (var i = 0 ; i < orders.length ; i++) {           
                e.CancelOrder(orders[i].Id)
            }
         }
    
}
```

> Detail

https://www.fmz.com/strategy/323894

> Last Modified

2021-10-18 23:05:15
