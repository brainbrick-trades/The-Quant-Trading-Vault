
> Name

OKEx-Futures-Test-for-Novices

> Author

区班量化

> Strategy Description

OKexFutures are more troublesome to use, so I wrote such a framework to make it easier for new users to understand and use. Note that ETH is priced at $10 each.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Interval|10|Polling interval (seconds))|
|mnum|20|30Minute line period|
|initRatio|0.5|Initial position ratio|


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
var isInit = 1; //Indicates initial state
function oper(){
    var allAmount;
    var cashRatio;
    var lastPrice;
    var wantRatio;
    var wantOper=0;//Expected operation,0no operation,1buy,-1sell
    var mhigh;
    var mlow;
   
        
        var mrecords = exchange.GetRecords(PERIOD_M30);
        //High and low points within a certain period
        mhigh=TA.Highest(mrecords, mnum, 'High');
        mlow=TA.Lowest(mrecords, mnum, 'Low');
        
        var midLine = (mhigh+mlow)/2;
        
        var ticker = _C(exchange.GetTicker);
        var nowPrice=ticker.Sell;
        var account = _C(exchange.GetAccount);
        var objid;
        var order;
        
        if (isInit == 1) {  //The initialization state is the default warehouse; 
            /*exchange.SetDirection("sell");    
            objid = exchange.Sell(nowPrice,Math.floor(nowPrice*account.Stocks*0.2/10)); //Okexmust be rounded
            order = exchange.GetOrder(objid);            // ParametersidThis is the order number; you need to enter the number of the order you want to query
            
            if (objid) { //If purchase is successful
                      isInit=2; //Initialization successful
                      account = _C(exchange.GetAccount);
                      Log(account);
                      Log("Fair price",midLine,"High point",mhigh,"Low point",mlow);
                      Log("Information of the order just placed,ID:", order.Id, "Price:", order.Price, "Amount:", order.Amount,
        "DealAmount:", order.DealAmount, "type:", order.Type);
            }*/
            
            exchange.SetDirection("buy");    
            objid = exchange.Buy(nowPrice,Math.floor(nowPrice*account.Stocks*0.2/10)); //Okexmust be rounded
            order = exchange.GetOrder(objid);            // ParametersidThis is the order number; you need to enter the number of the order you want to query
           
            if (objid) { //If purchase is successful
                      isInit=2; //Initialization successful
                      account = _C(exchange.GetAccount);
                      Log(account);
                      Log("Fair price",midLine,"High point",mhigh,"Low point",mlow);
                      Log("Information of the order just placed,ID:", order.Id, "Price:", order.Price, "Amount:", order.Amount,
        "account.Stocks:", account.Stocks, "type:", order.Type);
            }
            
            exchange.SetDirection("buy");    
            objid = exchange.Buy(nowPrice,Math.floor(nowPrice*account.Stocks*0.2/10)); //Okexmust be rounded
            order = exchange.GetOrder(objid);            // ParametersidThis is the order number; you need to enter the number of the order you want to query
           
            if (objid) { //If purchase is successful
                      isInit=2; //Initialization successful
                      account = _C(exchange.GetAccount);
                      Log(account);
                      Log("Fair price",midLine,"High point",mhigh,"Low point",mlow);
                      Log("Information of the order just placed,ID:", order.Id, "Price:", order.Price, "Amount:", order.Amount,
        "DealAmount:", order.DealAmount, "type:", order.Type);
            }
        }else if(isInit==2){ //Routine operation check
            //Print unfilled positions
            var orders = _C(exchange.GetOrders);
           
            for (var i = 0; i < orders.length; i++) {
                Log("Place Order",orders[i]);
            }
           
            var positions = exchange.GetPosition();
            Log("positions",positions.length);
            for (i = 0; i < positions.length; i++) { //Placing two long orders will be merged into one order
                 if (positions[i].Type == PD_LONG) {
                    //exchange.SetDirection("closebuy");
                    //exchange.Sell(nowPrice,positions[i].Amount);
                } else {
                   // exchange.SetDirection("closesell");
                   // exchange.Buy(nowPrice,positions[i].Amount);
                }
                Log("Open Position",positions[i]);
            }
            //If there are no pending or held orders
            if(orders.length<2){//&&positions.length==0){
                isInit=3;
                account = _C(exchange.GetAccount);
                Log("executed");
                Log(account);
            }
        }else{
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

https://www.fmz.com/strategy/170842

> Last Modified

2020-02-20 19:45:23
