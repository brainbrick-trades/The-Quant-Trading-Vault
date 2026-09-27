
> Name

Dynamic-Balance-Market-Making-Strategy-Xiao-Gao

> Author

gaotiansong



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|DELAY|5|Balance interval|
|PRICE_INCREMENT|1e-06|Minimum price movement|
|AMOUNT_INCREMENT|0.01|Minimum quantity movement|
|AMOUNT_MINIMUM|0.01|Minimum trading quantity|
|SPREAD|0.3|Order price interval|


> Source (javascript)

``` javascript
var Coin = ''
var Fiat = ''
var RefreshLoop = 0
var Account = ''
var Depth = ''
var Orders = ''
var BuyWeighted = 0
var SellWeighted = 0
var MidPrice = 0
var InitialBalance = exchange.GetAccount().Balance + exchange.GetAccount().Stocks * exchange.GetDepth().Bids[0].Price

function CancelPendingOrders() {
    for (var j = 0; j < Orders.length; j++) {
          exchange.CancelOrder(Orders[j].Id, Orders[j])}
}

function UpdateAll() {
    Account = exchange.GetAccount()
    Depth = exchange.GetDepth()
    Orders = exchange.GetOrders()
    //Log("UpdateAll")
}

function UpdatePrice() {
    //MidPrice = (Depth.Asks[0].Price+Depth.Bids[0].Price)/2
    BuyWeighted = Depth.Asks[0].Price * (1+SPREAD/100)
    SellWeighted = Depth.Bids[0].Price * (1-SPREAD/100)
    //Log("UpdatePrice")
}

function onTick(){
    // Refresh account balance and market data
    //Log("UpdateAll")
    UpdateAll()
    var Buy = Depth.Asks[0].Price
    var Sell = Depth.Bids[0].Price
    
    // Calculate weighted price
    //Log("UpdatePrice")
    UpdatePrice()
    
    // Check existing orders
    if (Orders.length==2){
        return
    }
    if (Orders.length>2){
        CancelPendingOrders()
        UpdateAll()
    }
    // Process single order
    if (Orders.length==1){
        Order = Orders[0]
        Price=Order.Price
        if (Order.Type==0){
            if (Price/(1-SPREAD/100) > Sell){
                return
            }else{
                CancelPendingOrders()
                UpdateAll()
            }
        }else{
            if (Price/(1+SPREAD/100) < Buy){
                return
            }else{
                CancelPendingOrders()
                UpdateAll()
            }
        }
    }
    
    // Calculate the value of current positions
    var ValueByBuy = Account.Stocks * BuyWeighted
    var ValueBySell = Account.Stocks * SellWeighted
    Log(Coin + " Value By Weighted Ask - " + Fiat +" Balance : " + (ValueByBuy-Account.Balance))
    Log(Fiat + " Balance - " + Coin +" Value By Weighted Bid : " +(Account.Balance-ValueBySell))
    //Log(ValueByBuy)
    //Log(ValueBySell)
    
    // The value of the currency held is higher than the pricing currency. Sell the currency held.
    if (ValueByBuy > Account.Balance){
        ToBeSold = (ValueByBuy - Account.Balance)/2/BuyWeighted
        if (ToBeSold > AMOUNT_MINIMUM){
            ToBeSold = _N(Math.ceil(ToBeSold / AMOUNT_INCREMENT) * AMOUNT_INCREMENT)
            Log("To be sold " + Coin + " Quantity:" + ToBeSold)
            exchange.Sell(BuyWeighted,ToBeSold)
        }
    }
    // The value of the pricing currency held is higher than the currency held. Buy the currency
    if (ValueBySell < Account.Balance){
        ToBeBought = (Account.Balance - ValueBySell)/2/SellWeighted
        if (ToBeBought > AMOUNT_MINIMUM){
            ToBeBought = _N(Math.ceil(ToBeBought / AMOUNT_INCREMENT) * AMOUNT_INCREMENT)
            Log("To be purchased " + Coin + " Quantity:" + ToBeBought)
            exchange.Buy(SellWeighted,ToBeBought)
        }
    }
    Log(Fiat + " Quantity:" + Account.Balance)
    Log(Coin + " Quantity:" + Account.Stocks)
    
    RefreshLoop = RefreshLoop+1
    if (RefreshLoop>60) {
        var Profit = _N(Account.Stocks*Sell) + _N(Account.Balance) - _N(InitialBalance)
        LogProfit(Profit)
        RefreshLoop = 0
    }
}
function main(){
    var Pair = exchange.GetCurrency()
    LogReset()
    LogProfitReset()
    LogProfit(0)
    UpdateAll()
    CancelPendingOrders()
    Coin = Pair.split("_")[0]
    Fiat = Pair.split("_")[1]
    while (true){
        try {
            onTick()
        } catch (err) {
            Log(err)
        }
        Sleep(DELAY*1000)
    }
}
```

> Detail

https://www.fmz.com/strategy/114044

> Last Modified

2018-08-29 17:28:23
