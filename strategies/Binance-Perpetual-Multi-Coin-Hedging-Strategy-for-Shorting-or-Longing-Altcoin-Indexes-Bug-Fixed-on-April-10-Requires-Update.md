
> Name

Binance-Perpetual-Multi-Coin-Hedging-Strategy-for-Shorting-or-Longing-Altcoin-Indexes-Bug-Fixed-on-April-10-Requires-Update

> Author

小草

> Strategy Description

## **Important content!!**

- Be sure to read this study https://www.fmz.com/digest-topic/5294 first. Understand a series of issues such as strategy principles, risks, how to screen trading pairs, how to set parameters, the ratio of opening positions to total funds, etc.
- The previous research report needs to be downloaded and uploaded to your own research environment. Run the actual modifications. If you have already seen this report, it was recently updated with data for the latest week.
- **The strategy cannot be backtested directly and needs to be backtested in the research environment**.
- Strategy code and default parameters are for research purposes only. Caution is required for live trading; set parameters based on your own research, **at your own risk**.**.
- **It is impossible for the strategy to make profits every day. You can look at the backtest history. Sideways and retracements of 1-2 weeks are normal, and the backtest may be large, and it needs to be treated correctly.**
- The code is public and can be modified by yourself. If you have any questions, please leave comments and feedback. It is best to join the inventor's Binance exchange group (how to join is in the research report) to get update notifications.
- **The strategy needs to run in full position mode. Do not set two-way positions. The strategy only supports Binance futures. When creating the robot, just use the default trading pair and candlestick cycle. The strategy does not use candlestick.**
- **The strategy conflicts with other strategies and manual operations, so you need to pay attention**
- Overseas hosts are required for real-time operation. During the test phase, you can rent Alibaba Cloud Hong Kong servers with one click on the platform. It is cheaper to rent the entire server by yourself on a monthly basis (the lowest configuration is sufficient, please refer to the deployment tutorial: https://www.fmz.com/bbs-topic/2848 )
- Binance's futures and spot need to be added separately. Binance futures are``Futures_Binance``

## Strategy Principle

The strategy will diversify into equal short positions on a selected basket of altcoins, while equal positions are long on Bitcoin to hedge, reducing risk and volatility. As prices fluctuate, positions are constantly adjusted to keep the value of short positions constant and long positions equal. **Essentially shorting the Altcoin-Bitcoin Price Index**. The performance of the past two months (about 3 times leverage, data updated to 4.8), in the past week, altcoins have risen relative to Bitcoin, so there has been a loss. If you are bullish on altcoins, you can set short Bitcoin and long altcoins in the parameters.:

**The default strategy is to go long on Bitcoin and short altcoins, but you can do the opposite (if you think altcoins are at the bottom), and the decision is yours**

 ![IMG](https://www.fmz.com/upload/asset/24281c6de45544ca2b7.png) 



## Strategy Logic

1.Update market quotes and account positions
2.Update the short positions' value of various altcoins to determine whether adjustments are needed.
3.Update the total short positions, determine the long positions, and determine whether the long positions need to be adjusted.
4.Place an order. The order quantity is determined by Bingshan Commission, and the transaction is completed according to the counterparty price (buy at the same price as the sell). **Cancel the order immediately after placing it (so you will see many orders with failed cancellation 400: {"code":-2011,"msg":"Unknown order sent."}, normal phenomenon)**
5.Loop again

**Will judgeShort_symbols,Long_symbolsThat trading pair is long,The opening value for each extra coinTrade_value,The minimum contract value of each currency is the average of the value that needs to be hedged.**

If you are only short BTC and long TRX, DASH, ONT, QTUM, and Trade_value is 50, then TRX, DASH, ONT, and QTUM are all long positions 50, and BTC is short.50\*4.

If you are only long BTC and short TRX, DASH, ONT, QTUM, and Trade_value is 50, then TRX, DASH, ONT, and QTUM all have short positions of 50, and BTC holds long positions.50\*4.

The level in the status bar represents the proportion of the margin used and should not be too high.

## Strategy Arguments

 ![IMG](https://www.fmz.com/upload/asset/2c9e5e0e4c30f9eaada.png)  

- Short_symbols:Shorted currencies, separated by ","
- Long_symbols:If you want to go long on the currency, you can also leave it short without hedging. You can go bare-short directly.
- Trade_value:Short holding value of a single currency. You also need to do long hedging, the total value = 2\*Trade_value\*number of short currencies. Generally, 3-5 times leverage is used, that is, total value = 3*account balance. You need to decide based on the total amount of funds you invest. You can check the size of the leverage through backtesting in the research environment.
- Adjust_value:	The contract value (priced in USDT) adjusts the deviation value. If it is too large, the adjustment will be slow, and if it is too small, the handling fee will be too high. It is decided based on Trade_value. It cannot be lower than 20, otherwise the minimum transaction will not be reached.
- Ice_value:The iceberg commission value cannot be less than 20. When placing an order, choose the smaller one between Adjust_value and Ice_value.


## Strategy Risks

When the price of the shorted currency rises and the contract value increases, the position is reduced. On the contrary, the profit is increased. This keeps the total contract value constant. It is very likely that altcoins will emerge from an independent market. From the current one-year cycle, altcoins may be at the bottom and may rise a lot from the bottom. It depends on how to use it. If you are optimistic about the altcoin and think it has reached the bottom, you can operate in the direction and go long on the index. Or if you are optimistic about certain currencies (not necessarily Bitcoin), you can hedge against them.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Short_symbols|TRX,DASH,ONT,QTUM,BAT,IOST,ADA,ZEC,XMR,NEO,VET,XRP,IOTA,XLM|Short trading pair|
|Long_symbols|BTC|Long trading pair|
|Trade_value|50|Value of a single short contract|
|Adjust_value|20|Contract value adjustment deviation|
|Ice_value|50|Size of iceberg order|
|Log_profit_interval|20|LogTotal equity intervals|
|Interval|5|Dormant Times|


> Source (javascript)

``` javascript
if(IsVirtual()){
    throw 'Cannot backtest, reference for backtest https://www.fmz.com/digest-topic/5294 '
}
if(exchange.GetName() != 'Futures_Binance'){
    throw 'Only supports Binance futures exchange, which is different from spot exchange and needs to be added separately with the nameFutures_Binance'
}

var short_symbols = Short_symbols.split(',')
var long_symbols = Long_symbols.split(',')

if(short_symbols.length == 1 && short_symbols[0] == ''){
    short_symbols = []
}
if(long_symbols.length == 1 && long_symbols[0] == ''){
    long_symbols = []
}
var symbols = []
for(var i=0; i<short_symbols.length; i++){
    if(short_symbols[i]){
        symbols.push(short_symbols[i])
    }
}
for(var i=0; i<long_symbols.length; i++){
    if(long_symbols[i]){
        symbols.push(long_symbols[i])
    }
}
var update_profit_time = 0
var assets = {}
var trade_info = {}
var exchange_info = HttpQuery('https://fapi.binance.com/fapi/v1/exchangeInfo')
if(!exchange_info){
    throw 'Unable to connect to Binance network, requires overseas hosting'
}
exchange_info = JSON.parse(exchange_info)
for (var i=0; i<exchange_info.symbols.length; i++){
    if(symbols.indexOf(exchange_info.symbols[i].baseAsset) > -1){
       assets[exchange_info.symbols[i].baseAsset] = {amount:0, hold_price:0, value:0, bid_price:0, ask_price:0, realised_profit:0, margin:0, unrealised_profit:0}
       trade_info[exchange_info.symbols[i].baseAsset] = {minQty:parseFloat(exchange_info.symbols[i].filters[1].minQty),
                                                         priceSize:parseInt((Math.log10(1.1/parseFloat(exchange_info.symbols[i].filters[0].tickSize)))),
                                                         amountSize:parseInt((Math.log10(1.1/parseFloat(exchange_info.symbols[i].filters[1].stepSize))))
                                                        }
    }
}
assets.USDT = {unrealised_profit:0, margin:0, margin_balance:0, total_balance:0, leverage:0}


function updateAccount(){
    var account = exchange.GetAccount()
    var pos = exchange.GetPosition()
    if (account == null || pos == null ){
        Log('update account time out')
        return
    }
    assets.USDT.update_time = Date.now()
    for(var i=0; i<symbols.length; i++){
        assets[symbols[i]].margin = 0
        assets[symbols[i]].unrealised_profit = 0
        assets[symbols[i]].hold_price = 0
        assets[symbols[i]].amount = 0
        assets[symbols[i]].unrealised_profit = 0
    }
    for(var j=0; j<account.Info.positions.length; j++){
        if(account.Info.positions[j].positionSide == 'BOTH'){
            var pair = account.Info.positions[j].symbol 
            var coin = pair.slice(0,pair.length-4)
            if(symbols.indexOf(coin) < 0){continue}
            assets[coin].margin = parseFloat(account.Info.positions[j].initialMargin) + parseFloat(account.Info.positions[j].maintMargin)
            assets[coin].unrealised_profit = parseFloat(account.Info.positions[j].unrealizedProfit)
        }
    }
    assets.USDT.margin = _N(parseFloat(account.Info.totalInitialMargin) + parseFloat(account.Info.totalMaintMargin),2)
    assets.USDT.margin_balance = _N(parseFloat(account.Info.totalMarginBalance),2)
    assets.USDT.total_balance = _N(parseFloat(account.Info.totalWalletBalance),2)
    assets.USDT.unrealised_profit = _N(parseFloat(account.Info.totalUnrealizedProfit),2)
    assets.USDT.leverage = _N(assets.USDT.margin/assets.USDT.total_balance,2)
    pos = JSON.parse(exchange.GetRawJSON())
    if(pos.length > 0){
        for(var k=0; k<pos.length; k++){
            var pair = pos[k].symbol
            var coin = pair.slice(0,pair.length-4)
            if(symbols.indexOf(coin) < 0){continue}
            assets[coin].hold_price = parseFloat(pos[k].entryPrice)
            assets[coin].amount = parseFloat(pos[k].positionAmt)
            assets[coin].unrealised_profit = parseFloat(pos[k].unRealizedProfit)
        }
    }
}

function updateTick(){
    var ticker = HttpQuery('https://fapi.binance.com/fapi/v1/ticker/bookTicker')
    if(ticker == null){
        Log('get ticker time out')
        return
    }
    ticker = JSON.parse(ticker)
    for(var i=0; i<ticker.length; i++){
        var pair = ticker[i].symbol 
        var coin = pair.slice(0,pair.length-4)
        if(symbols.indexOf(coin) < 0){continue}
        assets[coin].ask_price = parseFloat(ticker[i].askPrice)
        assets[coin].bid_price = parseFloat(ticker[i].bidPrice)
        assets[coin].ask_value = _N(assets[coin].amount*assets[coin].ask_price, 2)
        assets[coin].bid_value = _N(assets[coin].amount*assets[coin].bid_price, 2)
    }
}

function trade(symbol, dirction, value){
    if(Date.now()-assets.USDT.update_time > 10*1000){
        Log('Update account delay, do not trade')
        return
    }
    var price = dirction == 'sell' ? assets[symbol].bid_price : assets[symbol].ask_price
    var amount = _N(Math.min(value,Ice_value)/price, trade_info[symbol].amountSize)
    if(amount < trade_info[symbol].minQty){
        Log(symbol, 'The contract adjustment deviates from the value or the iceberg order setting is too small and the minimum transaction cannot be reached., At least needed: ', _N(trade_info[symbol].minQty*price,0))
        return
    }
    exchange.IO("currency", symbol+'_'+'USDT')
    exchange.SetContractType('swap')
    exchange.SetDirection(dirction)
    var f = dirction == 'buy' ? 'Buy' : 'Sell'
    var id = exchange[f](price, amount, symbol)
    if(id){
        exchange.CancelOrder(id) //Order will be canceled immediately
    }
}



function updateStatus(){
        var table = {type: 'table', title: 'Trading pair information', 
             cols: ['Currency', 'Quantity', 'Position Price', 'Current Price', 'Position Value', 'Margin', 'Unrealized Profit and Loss''],
             rows: []}
    for (var i=0; i<symbols.length; i++){
        var price = _N((assets[symbols[i]].ask_price + assets[symbols[i]].bid_price)/2, trade_info[symbols[i]].priceSize)
        var value = _N((assets[symbols[i]].ask_value + assets[symbols[i]].bid_value)/2, 2)
        var infoList = [symbols[i], assets[symbols[i]].amount, assets[symbols[i]].hold_price, price, value,_N(assets[symbols[i]].margin,3), _N(assets[symbols[i]].unrealised_profit,3)]
        table.rows.push(infoList)
    }
    var logString = _D() + '  ' + JSON.stringify(assets.USDT) + '\n'
    LogStatus(logString + '`' + JSON.stringify(table) + '`')
    
    if(Date.now()-update_profit_time > Log_profit_interval*1000){
        LogProfit(_N(assets.USDT.margin_balance,3))
        update_profit_time = Date.now()
    }
    
}

function onTick(){
    var short_value = Trade_value
    if(short_symbols.length<long_symbols.length){
        short_value = _N(long_symbols.length*Trade_value/short_symbols.length,0)
    }
    var long_value = Trade_value
    if(short_symbols.length>long_symbols.length){
        long_value = _N(short_symbols.length*Trade_value/long_symbols.length,0)
    }
    var symbol = ''
    for(var i=0; i<short_symbols.length; i++){
        symbol = short_symbols[i]
        if(assets[symbol].ask_price == 0){ continue }
        if(assets[symbol].bid_value + short_value > Adjust_value){
            trade(symbol, 'sell', assets[symbol].bid_value + short_value)
        }
        if(assets[symbol].ask_value + short_value < -Adjust_value){
            trade(symbol, 'buy', -(assets[symbol].ask_value + short_value))
        }
    }
    for(var i=0; i<long_symbols.length; i++){
        symbol = long_symbols[i]
        if(assets[symbol].ask_price == 0){ continue }
        if(assets[symbol].bid_value - long_value > Adjust_value){
            trade(symbol, 'sell', assets[symbol].bid_value-long_value)
        }
        if(assets[symbol].ask_value - long_value < -Adjust_value){
            trade(symbol, 'buy', long_value-assets[symbol].ask_value)
        }
    }   
}

function main() {
    while(true){
        updateAccount()
        updateTick()
        onTick()
        updateStatus()
        Sleep(Interval*1000)
    }
}
```

> Detail

https://www.fmz.com/strategy/194825

> Last Modified

2020-08-04 14:22:07
