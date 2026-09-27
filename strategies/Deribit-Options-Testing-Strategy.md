
> Name

Deribit-Options-Testing-Strategy

> Author

发明者量化-小小梦

> Strategy Description

## DeribitOption test strategy

Test code for testing option opening, closing, order placement and cancellation, market data retrieval, etc.
UsingDeribitTest environment, can be used for actual live trading, can be deleted```exchange.IO("base", "https://test.deribit.com")```Line of Code.

![IMG](https://www.fmz.com/upload/asset/1705e6bb63a19de89463.png) 



> Source (javascript)

``` javascript
function CancelAll() {
    while (1) {
        var orders = exchange.GetOrders()
        for (var i = 0; i < orders.length; i++) {
            exchange.CancelOrder(orders[i].Id, orders[i])
            Sleep(500)
        }
        if (orders && orders.length == 0) {
            break
        }
        Sleep(500)
    }
    Log(exchange.GetOrders())
}

function main() {
    contract = "BTC-27DEC19-7250-P"
    exchange.IO("base", "https://test.deribit.com")    // Test, usingderibitSimulated test environment, if trading live, please delete this sentence
    exchange.SetContractType(contract)     // Set option contract
    
    // Cancel all current pending orders
    CancelAll()
    
    // Get current account information
    LogStatus(exchange.GetAccount())
    Sleep(500)
    
    // Get current market information
    Log(exchange.GetTicker())
    Sleep(500)

    // Get current depth information
    Log(exchange.GetDepth())
    Sleep(500)
    
    // Get the latest transaction records in the current market
    Log(exchange.GetTrades())
    Sleep(500)
    
    // Get CurrentKLine Data
    Log(exchange.GetRecords())
    Sleep(500)
    
    // Test Order
    exchange.SetDirection("buy")
    var id = exchange.Buy(0.002, 0.1)   // The first parameter refers to the royalty, and the second parameter refers to the quantity of the underlying object.
    Log("id:", id)
    Sleep(500)
    
    // Get order information
    Log(exchange.GetOrder(id))
    Sleep(500)
    
    // Get all current pending orders
    Log(exchange.GetOrders())
    Sleep(500)
    
    // Get current option positions
    Log(exchange.GetPosition())
    Sleep(500)
    
    // Cancel pending order
    exchange.CancelOrder(id)
    Sleep(500)
    
    // Retrieve current pending orders again to check if they are canceled
    Log(exchange.GetOrders())
    Sleep(500)
    
    // Taker transaction
    exchange.SetDirection("sell")
    var ticker = exchange.GetTicker()
    var id2 = exchange.Sell(ticker.Buy, 0.1)
    Sleep(500)
    
    // Get a position
    Log(exchange.GetPosition())
    Sleep(500)
    
    // Close Position
    exchange.SetDirection("closesell")
    var pos = exchange.GetPosition(contract)
    Log("pos", pos)
    var id3 = exchange.Buy(ticker.Sell, pos[0].Amount)
    Log(exchange.GetPosition())
    Sleep(500)
}
```

> Detail

https://www.fmz.com/strategy/179475

> Last Modified

2019-12-25 15:17:30
