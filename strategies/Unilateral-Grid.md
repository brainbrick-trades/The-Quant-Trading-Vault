
> Name

Unilateral-Grid

> Author

6821281

> Strategy Description

When testing, fill in the starting price to test whether it is normal.
If starting price is not filled in, buy at current price + price range
WeChat173970984

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|buyjingdu|2|Order price accuracy|
|buymount|3|Order quantity precision|
|buypersent|true|Order Percentage|
|buylimit|0.01|Minimum transaction volume|
|reffertime|3000|Refresh interval|
|moneybt|100|Price spacing of the grid|
|startpricex|false|Starting Price|
|liruncha|0.1|Profit Spread|


> Source (javascript)

``` javascript
//Get account balance
var  startPrice= 0;
function getBalancex(){
    var balance = exchange.GetAccount();
    Log("Balance:", balance.Balance,"Coin balance:", balance.Stocks);
     return balance;
}    


//Get current coin price
function getPrice(typex){
    var NowPrice =exchange.GetTicker();
    if(typex=='buy'){
        
     Log("Current buy price:"+(NowPrice.Buy))
     return NowPrice.Buy;
    }
    if(typex=='sell'){
     Log("Current sell price:"+(NowPrice.Sell))
     return NowPrice.Sell;
    }
}

//Cancel all buy orders and place them again
function cancelOrders(){
    //Get all unfilled orders
    var orders = _C(exchange.GetOrders);
    for(var z in orders){
       //# Log("Current order type:",orders[z].Type,"OrderId:",orders[z].Id);
        if(orders[z].Type==0){
            exchange.CancelOrder(orders[z].Id)
            Log("Cancel previous pending order successfully,id:",orders[z].Id);
        }
    }
    /*
    for(var i=0;i<orders.length;i++){
        //Only cancel buy orders, do not cancel sell orders
        if(orders.Type==0){
            exchange.CancelOrder(orders.Id)
            Log("Cancel previous pending order successfully")
        }
    }*/
}



var saveBuyId= 0;
var doNowPrice = 0;
//Order operation Buy operation
function doTradingBuy(){
    cancelOrders()
    var price = getPrice("buy");
    if(startpricex>0){
        price=startpricex-moneybt;
    }else{
        price=price-moneybt;  //The actual price is the current price minus the price within the range
    }
    startPrice=price;
    var balancex = getBalancex();
    balanceAmount = balancex.Balance;
    
    //Quantity to be purchased
    doAmount = (balanceAmount*(buypersent/100))/price
    
    
    
    var id = 0; 
    if(doAmount>buylimit){
        saveBuyId=id= exchange.Buy(price, doAmount);
        Log("Order Successfulid:", id,"  Price:", price,"  Quantity:", doAmount);
    }else{
        Log("The available quantity is lower than the minimum transaction volume:", buylimit,"  Quantity:", doAmount);
    }
}


//Based on Last TimeIDto check the order status and then sell
function doSellTrading2(){
    //Get order status
    Log("Previous OrderID:", saveBuyId);
    if(saveBuyId!=0){
        var order = exchange.GetOrder(saveBuyId);
        if(order){
            if(order.Status==ORDER_STATE_CLOSED){
                leftStocks=leftStocks-orderList[i].Amount
                var sellPrice = order.Price+liruncha;
                var sellAmount =  order.Amount;
                var id=exchange.Sell(sellPrice, sellAmount);
                Log("Sale Successfulid:", id,"  Price:", sellPrice,"  Quantity:", sellAmount);
            }
        }
    }

}









//Periodically scan for fulfilled buy orders and sell the corresponding quantity
function doSellTrading(){
    //If the balance is greater than zero  
    balan = getBalancex()
    leftStocks=balan.Stocks;
    if(balan.Stocks>0){
        var orderList = exchange.GetTrades()
        //Before Theoretical Testing20Just Need This Data
        if(orderList){
            for(i=0;i<=100;i++){
                //Log("View order information:",orderList);
                if(orderList[i].Type==0 && leftStocks>orderList[i].Amount){
                    leftStocks=leftStocks-orderList[i].Amount
                    var sellPrice = orderList[i].Price+liruncha;
                    var sellAmount =  orderList[i].Amount;
                    var id=exchange.Sell(sellPrice, sellAmount);
                    Log("Sale Successfulid:", id,"  Price:", sellPrice,"  Quantity:", sellAmount);
                }
            }
        }
    }
}


function onTick(){
    //Write the strategy logic here, which will be called continuouslyexchange
    doSellTrading2()
    doTradingBuy()
}
/*
function main(){
    var id = exchange.Sell(99999, 1);
    var order = exchange.GetOrder(id);//ParametersidThis is the order number; you need to enter the number of the order you want to query
    Log("Id", order.Id, "Price:", order.Price, "Amount:", order.Amount, "DealAmount:",
        order.DealAmount, "Status:", order.Status, "Type:", order.Type);
}
*/
function main(){
    exchange.SetPrecision(buyjingdu, buymount);
    while(true){
        onTick();
        Sleep(reffertime);
    }
}
```

> Detail

https://www.fmz.com/strategy/88472

> Last Modified

2018-04-26 23:14:14
