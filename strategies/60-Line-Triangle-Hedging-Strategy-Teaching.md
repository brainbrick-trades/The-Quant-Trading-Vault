
> Name

60-Line-Triangle-Hedging-Strategy-Teaching

> Author

发明者量化-小小梦

> Strategy Description

## Triangle hedging teaching strategy

#### Principle
  - For Example 
     A exchange : ETH_BTC 
     B exchange : ETH_USDT
     C Exchange (actually it is another trading pair of Exchange B, logically it isC.) : BTC_USDT

  - B ,C The exchange trading pair is composed of ETH_BTC and A exchange hedging. In this way BC is actually an exchange account.
 
#### Optimize space

  - Coin Balance.
  - Calculate the hedging spread based on the handling rate and the dynamic spread.
  - Moving bricks hard.
  - Order book depth scanning to calculate the best hedge amount.
    .....


#### BUGFeedback
 - If there are errors, feel free to leave a message.



> Source (javascript)

``` javascript
// The trading pair is ETH_BTC , ETH_USDT , BTC_USDT As an Example
// There is still a lot of room for optimization in teaching strategies, such as: currency balance module, controlling hedging differences based on handling rates, hard copying, etc.
function main () {                                                                                      
    if (exchanges[0].GetQuoteCurrency() != exchanges[2].GetCurrency().split("_")[0] || 
        exchanges[0].GetCurrency().split("_")[0] != exchanges[1].GetCurrency().split("_")[0]) {
        throw "Exchange trading pair configuration error."
    }
    var marketSlideRate = 1 // 1.02
    var hedgeDiff = 0.0007
    var hedgeAmount = 0.1
    var isFirst = true
    var concurrenter = function (funcName, isWait, tasks, amounts) {
        for (var i = 0 ; i < exchanges.length; i++) {
            if (isFirst) {
                exchanges[i].acc = _C(exchanges[i].GetAccount)
                exchanges[i].initAcc = exchanges[i].acc
            }
            if (isWait) {
                var a = funcName == "GetTicker" ? exchanges[i].ticker = exchanges[i].tiR.wait() : exchanges[i].id = exchanges[i].trR.wait()
                if (funcName == "trade") {
                    exchanges[i].acc = _C(exchanges[i].GetAccount)
                }
            } else {
                var b = funcName == "GetTicker" ? exchanges[i].tiR = exchanges[i].Go(funcName) : exchanges[i].trR = exchanges[i].Go(tasks[i], -1, amounts[i], exchanges[i].GetCurrency())
            }
        }
        if (funcName == "trade" && isWait) {
            Log("BTC:", exchange.BTC = exchanges[0].acc.Balance + exchanges[2].acc.Stocks, "ETH:", exchange.ETH = exchanges[0].acc.Stocks + exchanges[1].acc.Stocks, "USDT:", 
                exchange.USDT = exchanges[1].acc.Balance + exchanges[2].acc.Balance, "#FF0000")
            LogProfit(exchange.USDT - (exchanges[1].initAcc.Balance + exchanges[2].initAcc.Balance) - 
                (exchanges[0].initAcc.Balance + exchanges[2].initAcc.Stocks - exchange.BTC) * exchanges[2].ticker.Last -
                (exchanges[0].initAcc.Stocks + exchanges[1].initAcc.Stocks - exchange.ETH) * exchanges[1].ticker.Last)
        }
        isFirst = false
    }

    while (1) {
        concurrenter("GetTicker", false)
        concurrenter("GetTicker", true)
        var tickerA = exchanges[0].ticker
        var tickerB = exchanges[1].ticker
        var tickerC = exchanges[2].ticker

        var tickerBC = {
            Buy : tickerB.Buy / tickerC.Sell,
            Sell : tickerB.Sell / tickerC.Buy,
        }

        if (tickerA.Buy - tickerBC.Sell > hedgeDiff && exchanges[0].acc.Stocks > 0.2 && exchanges[1].acc.Balance > 500 && exchanges[2].acc.Stocks > 0.03) {                          // Sell A , Buy BC (Buy B Sell C)
            concurrenter("trade", false, ["Sell", "Buy", "Sell"], [hedgeAmount, marketSlideRate * tickerB.Sell * hedgeAmount, tickerB.Sell * hedgeAmount / tickerC.Buy])
            concurrenter("trade", true)
        }
        if (tickerBC.Buy - tickerA.Sell > hedgeDiff && exchanges[0].acc.Balance > 0.03 && exchanges[1].acc.Stocks > 0.2 && exchanges[2].acc.Balance > 500) {                          // Buy A , Sell BC (...)
            concurrenter("trade", false, ["Buy", "Sell", "Buy"], [marketSlideRate * hedgeAmount * tickerA.Sell, hedgeAmount, marketSlideRate * hedgeAmount * tickerA.Sell * tickerC.Sell])
            concurrenter("trade", true)
        }
        Sleep(500)
    }
}


```

> Detail

https://www.fmz.com/strategy/144257

> Last Modified

2019-04-16 16:38:17
