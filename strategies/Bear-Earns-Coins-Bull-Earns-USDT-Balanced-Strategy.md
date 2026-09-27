
> Name

Bear-Earns-Coins-Bull-Earns-USDT-Balanced-Strategy

> Author

VIC

> Strategy Description

* Contract version of Buffett's concept money balance strategy, by default directly going long half position in contracts.
* Binance BUSD has no order placement fees, allowing for extremely narrow balancing distance and capturing maximum profit and fee rebates.
* The principle and code are very simple. We borrowed the writing methods of the big guys and calculated the order point and lot number in advance to place the order. Theoretically, the larger the principal, the closer the rate of return is to the limit.
* Not recommended to run below 1000U, the minimum order value limit causes too much difference in pending orders.
* Profit is based on rising or volatile coin prices.
* Can be copied directly for backtesting
* Large capital capacity; disadvantage is that it requires a fluctuating or slow bull market, prolonged bear markets will accumulate many long positions but will not cause liquidation..
* Finally, to say, having tried Martingale negative expectation and high-frequency arbitrage with high competition, perhaps returning to value investing is the ultimate path to victory..
* Welcome to click the avatar and add me on WeChat to discuss this strategy

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|pricePrecision|2|Price Precision|
|amountPrecision|3|Order accuracy|
|linjie|30|Critical value|
|leverage|10|Leverage initialization|


> Source (javascript)

``` javascript


/*backtest
start: 2019-12-01 00:00:00
end: 2024-02-07 23:59:00
period: 30m
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"ETH_USDT","balance":100000}]
args: [["pricePrecision",2],["amountPrecision",3],["linjie",30]]
*/

function cancelAll() {
    while (1) {
        var orders = _C(exchange.GetOrders)
        if (orders.length == 0) {
            break
        }
        for (var i = 0; i < orders.length; i++) {
            exchange.CancelOrder(orders[i].Id, orders[i].Id)
            Sleep(100)
        }
        Sleep(100)
    }
}
function onexit() {
    //
    cancelAll()
}

function main() {
    exchange.SetContractType("swap")
    exchange.SetPrecision(pricePrecision, amountPrecision) //Accuracy
    exchange.SetMarginLevel(leverage) //leverage
    //LogProfitReset()
    LogReset(1)
    var buyOrderId
    var sellOrderId
    while (1) {
        var pos = _C(exchange.GetPosition)
        if (pos.length > 0) {
            var Mar = pos[0].Margin //Margin
        } else {
            var Mar = 0
        }

        var MarginLevel = leverage //leverage
        var account = _C(exchange.GetAccount)
        var Bala = account.Balance //Available balance
        var Bal = Bala - Mar * (MarginLevel - 1) //Balance after removing positions
        var ticker = _C(exchange.GetTicker)
        var price = ticker.Last //Latest price
        var Qian = Mar + Bala
        LogStatus("Token price: ", price," benefits:",Qian)
        var orders = _C(exchange.GetOrders)
        if (orders.length == 0) { //No order
            if (Mar * MarginLevel - Bal > 2 * linjie) { //Position value more than balance //Critical value
                exchange.SetDirection("closebuy")
                var Amount = 0.5 * (Mar * MarginLevel - Bal) / price
                exchange.Sell(-1, Amount)
            } else if (Bal - Mar * MarginLevel > 2 * linjie) { //Balance more than position value //Critical value
                var Amount = 0.5 * (Bal - Mar * MarginLevel) / price
                exchange.SetDirection("buy")
                exchange.Buy(-1, Amount)
            } else {//Place orders in both directions when status is balanced
                var Bprice = price * (Bal - linjie) / (Mar * leverage)
                var BAmount = 0.5 * linjie / Bprice
                exchange.SetDirection("buy")
                buyOrderId = exchange.Buy(Bprice, BAmount)
                var Sprice = price * (Bal - (-linjie)) / (Mar * leverage)
                var SAmount = 0.5 * linjie / Sprice
                exchange.SetDirection("closebuy")
                sellOrderId = exchange.Sell(Sprice, SAmount)
            }


        } else { //has orders
            var isFindBuyId = false
            var isFindSellId = false
            //Log("Initial state")
            for (var i = 0; i < orders.length; i++) {

                if (buyOrderId == orders[i].Id) {
                    isFindBuyId = true
                    //Log("has buy orders")
                }
                if (sellOrderId == orders[i].Id) {
                    isFindSellId = true
                    //Log("has sell orders")
                }
            }
            if (!isFindBuyId || !isFindSellId) { //One side has been executed,Cancel orders and enter a new cycle
                cancelAll()
                var Qian = Mar + Bala
                LogProfit(Qian)
                //LogStatus("Coin price:", price)
            }

        }
        Sleep(5000)
    }
}
```

> Detail

https://www.fmz.com/strategy/339698

> Last Modified

2024-03-06 11:15:26
