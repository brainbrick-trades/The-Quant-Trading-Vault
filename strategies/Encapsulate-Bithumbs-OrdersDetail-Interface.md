
> Name

Encapsulate-Bithumbs-OrdersDetail-Interface

> Author

发明者量化-小小梦

> Strategy Description

Due to the needs of some users, when using Bithumb, they want to check the order information of a certain ID.,
Encapsulated this interface of the exchange :  https://api.bithumb.com/info/order_detail
Only orders that are fully executed can be queried; orders with other statuses cannot be queried.

The interface information is as follows:
```
    /*
        https://api.bithumb.com/info/order_detail
        order_id   :
        type       : bid : Buy ask : sell
        currency   : Currency code ,Default : BTC
    */
```


```
function main() {
    var id = exchange.Sell(-1, 0.01)        // Sell order executed, because $.GetOrder Can only query fully executed orders.
                                            // If the lower limit order does not execute, check thisID ,will report an error Futures_OP 4: status: 5600, message: 거래 체결내역이 존재하지 않습니다. (Does not exist in trading, , meaning that the order could not be found
    Sleep(5000)
    var order = $.GetOrder(exchange, id)    // Pass into exchange Bithumb The exchange object of , pass inID ,Cannot query, return null 
    Log(order)
}
```



> Source (javascript)

``` javascript
function GetOrder(e, id, type){
    /*
        https://api.bithumb.com/info/order_detail
        order_id   :
        type       : bid : Buy ask : sell
        currency   : Currency code ,Default : BTC
    */
    var symbol = e.GetCurrency()
    var arr = symbol.split("_")
    var currency = arr[0]
    
    var ret = e.IO("api", "POST", "/info/order_detail", "order_id=" + id + "&type=" + type + "&currency=" + currency)
    
    // ret 
    /*
    {
        "status":"0000",
        "data":[
            {
                "order_currency":"BTC",
                "payment_currency":"KRW",
                "units_traded":"0.01",
                "price":"4322000",
                "cont_no":"32314118",
                "transaction_date":"1546054726834326",
                "type":"Buy",
                "fee":"64.83",
                "total":"43220"
            }
        ]
    }
    */
    
    /* order Structure
    {
        Id          :Unique identifier for the trade order
        Price       :Order price
        Amount      :Order quantity
        DealAmount  :Transaction quantity
        AvgPrice    :Average transaction price, # Note that some exchanges do not provide this data, and the settings that do not provide it are 0 . 
        Status      :Order status, referring to the order status in constants
        Type        :Order type, referring to the order type in constants
    }
    */
    
    var order = null
    var typeValue = null
    if(type == "Buy"){
        typeValue = ORDER_TYPE_BUY
    } else {
        typeValue = ORDER_TYPE_SELL
    }
    if(ret){
        order = {
            Info      : ret,                 // Original message
            Id        : id,                  // Unique identifier for the trade order
            Price     : ret.data[0].price,   // Order price
            Amount    : ret.data[0].units_traded,  // Order quantity
            DealAmount: ret.data[0].units_traded,  // Transaction quantity
            AvgPrice  : ret.data[0].price,         // Average transaction price, # Note that some exchanges do not provide this data, and the settings that do not provide it are 0 . 
            Status    : ORDER_STATE_CLOSED,        // Order status, referring to the order status in constants
            Type      : typeValue,                 // Type 
        }
    }
    
    return order
}

$.GetOrder = function(e, id, type){
    if(e.GetName() != "Bithumb"){
        Log("the parameter e is not bithumb!")
        return null
    }
    
    if(typeof(id) == "undefined"){
        Log("id Parameter error!")
        return null
    }
    
    if(type == "Buy"){
        GetOrder(e, id, type)
    } else if (type == "Sell") {
        GetOrder(e, id, type)
    } else {
        var buyOrder = GetOrder(e, id, "Buy")
        if(buyOrder){
            return buyOrder
        }
        var sellOrder = GetOrder(e, id, "Sell")
        if(sellOrder){
            return sellOrder
        } else {
            return null
        }
    }
}

function main() {
    var id = exchange.Sell(-1, 0.01)        // Sell order executed, because $.GetOrder Can only query fully executed orders.
                                            // If the lower limit order does not execute, check thisID ,will report an error Futures_OP 4: status: 5600, message: 거래 체결내역이 존재하지 않습니다. (Does not exist in trading, , meaning that the order could not be found
    Sleep(5000)
    var order = $.GetOrder(exchange, id)    // Pass into exchange Bithumb The exchange object of , pass inID ,Cannot query, return null 
    Log(order)
}
```

> Detail

https://www.fmz.com/strategy/132241

> Last Modified

2018-12-29 12:06:11
