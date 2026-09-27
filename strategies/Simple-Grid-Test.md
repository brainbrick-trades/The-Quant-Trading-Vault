
> Name

Simple-Grid-Test

> Author

cnxzcxy





> Source (javascript)

``` javascript
/*backtest
start: 2018-08-01 00:00:00
end: 2018-09-01 15:00:00
period: 15m
exchanges: [{"eid":"Huobi","currency":"LTC_BTC","stocks":0}]
*/

var runBuyOrder = [];
var runSellOrder = [];
var basePrice = 0;
var percent = 0.05;

function onTick(){
    var date = _D();
    var depth = exchange.GetDepth();
    account = exchange.GetAccount();
    
    //Initialize account
    if((account.Balance > 0) && (basePrice == 0)){
        buyMoney = account.Balance * 0.09;
        basePrice = depth.Asks[0].Price;

        buyPrice = basePrice * (1-percent * 0);
        runBuyOrder.push(exchange.Buy(buyPrice, buyMoney / buyPrice));
        
        buyPrice = basePrice * (1-percent * 1);
        runBuyOrder.push(exchange.Buy(buyPrice, buyMoney / buyPrice));
        
        buyPrice = basePrice * (1-percent * 2);
        runBuyOrder.push(exchange.Buy(buyPrice, buyMoney / buyPrice));
        
        buyPrice = basePrice * (1-percent * 3);
        runBuyOrder.push(exchange.Buy(buyPrice, buyMoney / buyPrice));
        
        buyPrice = basePrice * (1-percent * 4);
        runBuyOrder.push(exchange.Buy(buyPrice, buyMoney / buyPrice));

        buyPrice = basePrice * (1-percent * 5);
        runBuyOrder.push(exchange.Buy(buyPrice, buyMoney / buyPrice));
        
        buyPrice = basePrice * (1-percent * 6);
        runBuyOrder.push(exchange.Buy(buyPrice, buyMoney / buyPrice));
        
        buyPrice = basePrice * (1-percent * 7);
        runBuyOrder.push(exchange.Buy(buyPrice, buyMoney / buyPrice));
        
        buyPrice = basePrice * (1-percent * 8);
        runBuyOrder.push(exchange.Buy(buyPrice, buyMoney / buyPrice));
        
        buyPrice = basePrice * (1-percent * 9);
        runBuyOrder.push(exchange.Buy(buyPrice, buyMoney / buyPrice));
        
        buyPrice = basePrice * (1-percent * 10);
        runBuyOrder.push(exchange.Buy(buyPrice, buyMoney / buyPrice));
        
        Log(date);
        Log('exchange:', exchange.GetName(), ' Account:', exchange.GetAccount());
        Log('Sell Order:', runSellOrder, ' Buy Order:', runBuyOrder);
        
    }
    
    //Check order polling
    allOrders = runBuyOrder.concat(runSellOrder);
    allOrders.forEach(function(orderId){
        order = exchange.GetOrder(orderId);
        //Check sell order
        if(runSellOrder.indexOf(order.Id) > -1){
            if((order.Status == ORDER_STATE_CLOSED) && (order.Type == ORDER_TYPE_SELL)){
                Log(date);
                Log('Sell order successful price:', order.Price, ' Quantity:', order.DealAmount);
                Log('exchange:', exchange.GetName(), ' Account:', exchange.GetAccount());
                //Remove from local database and place a new buy order
                index = runSellOrder.indexOf(order.Id);
                runSellOrder.splice(index, 1);
                buyPrice = order.Price * (1 - percent);
                runBuyOrder.push(exchange.Buy(buyPrice, order.DealAmount * order.Price / buyPrice));                
            }
            
        }
        //Check the purchase order
        if(runBuyOrder.indexOf(order.Id) > -1){
            if((order.Status == ORDER_STATE_CLOSED) && (order.Type == ORDER_TYPE_BUY)){
                Log(date);
                Log('Buy order successful price:', order.Price, ' Quantity:', order.DealAmount);
                Log('exchange:', exchange.GetName(), ' Account:', exchange.GetAccount());
                //Remove from local database and place a new sell order
                index = runBuyOrder.indexOf(order.Id);
                runBuyOrder.splice(index, 1);
                sellPrice = order.Price * (1 + percent);
                runSellOrder.push(exchange.Sell(sellPrice, order.DealAmount));                
            }
            
        }
    });
    
}

function main(){
    while(true){
        onTick();
    }

}

```

> Detail

https://www.fmz.com/strategy/116289

> Last Modified

2018-09-14 16:05:05
