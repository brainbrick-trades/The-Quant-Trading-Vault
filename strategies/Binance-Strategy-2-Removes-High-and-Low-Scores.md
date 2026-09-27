
> Name

Binance-Strategy-2-Removes-High-and-Low-Scores

> Author

区班量化

> Strategy Description

Thanks to FMZ for publishing the strategy and thanks to the guards for support!
I made two modifications:
1,Because many friends default to 10x and 20x leverage, and this strategy is a full position mode. If the position of one coin is liquidated, the group will be wiped out. Therefore, a Max_amount is added. The purchase amount of a single currency will not exceed this amount to prevent liquidation.
2,If there are coins in the currency pool that are over-priced, over-priced, or unique, it will easily drag everyone down, and the overall strategy will easily fail. Therefore, when I calculate the index, I remove one of the highest scores and one of the lowest scores, and the resulting index is fairer.
   Once the special currency returns to normal, you can still buy it normally.
Note: Due to conditional limitations, this strategy has not been backtested and is for reference only; no responsibility will be assumed for any losses.!

## **Important content!!**

- Be sure to read this study https://www.fmz.com/digest-topic/5294 first. Understand a series of issues such as strategy principles, risks, how to screen trading pairs, how to set parameters, the ratio of opening positions to total funds, etc.
- The previous research report needs to be downloaded and uploaded to your own research environment. Run the actual modifications. If you have already seen this report, it was recently updated with data for the latest week.
- **The strategy cannot be backtested directly and needs to be backtested in the research environment**.
- Strategy code and default parameters are for research only; use in live trading requires caution and is at your own risk.
- The code is public and can be modified by yourself. If you have any questions, you are welcome to comment and give feedback. It is best to join the inventor Binance exchange group (the method of joining is in the research report)
- The strategy needs to run in the cross position mode. The ** strategy supports Binance. When creating the robot, just use the default trading pair and candlestick cycle. The strategy does not use candlestick.**

## Strategy Principle

We will short the currencies whose price is higher than the altcoin-Bitcoin price index, and go long the currencies whose price is lower than the index. The greater the deviation, the larger the position. (This strategy has no hedging, and BTC can also be added to the trading pair). Performance in the past two months (about 3 times leverage, data updated to4.8):
 ![IMG](https://www.fmz.com/upload/asset/2546f22f018c51604db.png) 

## Strategy Logic

1.Update market prices and account positions. The initial price will be recorded in the first run (newly added currencies are calculated based on the time of addition))
2.Update the index, the index is Altcoin-Bitcoin price index = mean(sum((Altcoin price/Bitcoin price)/(Altcoin initial price/Bitcoin initial price)))
3.Determine long or short positions based on deviation index, determine position size based on deviation magnitude
4.Place an order. The order quantity is determined by Bingshan Commission, and the transaction is completed according to the counterparty price (buy at the same price as the sell). **Cancel the order immediately after placing it (so you will see many orders with failed cancellation, which is normal)**
5.Loop again


## Strategy Arguments

 ![IMG](https://www.fmz.com/upload/asset/272b24a9c0018c96fb6.png) 

- Trade_symbols:Trading coins should be selected based on your own research platform, can also be added.BTC
- Trade_value:Shorting altcoins requires assessing their value based on total invested capital, which can be evaluated by backtesting the environment to determine leverage size
- Adjust_value:	Contract value (priced in USDT) adjustment deviation: Large deviations adjust slowly and cannot be less than 20, otherwise, the minimum transaction will not be achieved.
- Ice_value:The iceberg commission value cannot be less than 20. To actually place an order, choose the smaller one of Adjust_value/Ice_value.
- Reset:Reset historical data


## Strategy Risks

noticed that if a certain currency goes out of independent market, for example, it rises several times relative to the index, a large number of short positions will be accumulated on the currency, and the same sharp decline will also cause the strategy to go long in large quantities. You can limit the opening amount or stop loss and no longer trade.



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Trade_symbols|IOST,TRX,XLM,QTUM,DASH,ADA,XMR,ZEC,ATOM,IOTA,NEO,ONT,XRP,VET,EOS,ETC,LTC|Transaction currency|
|Trade_value|50|Holding value for every 1% deviation from the index|
|Adjust_value|20|Contract value adjustment deviation|
|Ice_value|20|Size of iceberg order|
|Log_profit_interval|600|LogTotal equity intervals|
|Interval|5|Dormant Times|
|Reset|false|Reset historical data|
|Max_amount|300|Maximum trading volume, do not buy if exceeded|


> Source (javascript)

``` javascript
//Index of the coin with the largest upward deviation
var highIndex=0;
//Index of the coin with the largest downward deviation
var lowIndex=0;

var trade_symbols = Trade_symbols.split(',')
var symbols = trade_symbols
var index = 1 //Index
if(trade_symbols.indexOf('BTC')<0){
    symbols = trade_symbols.concat(['BTC'])
}
var update_profit_time = 0
var assets = {}
var trade_info = {}
var exchange_info = HttpQuery('https://fapi.binance.com/fapi/v1/exchangeInfo')
if(!exchange_info){
    Log('Unable to connect to the network')
    return
}
exchange_info = JSON.parse(exchange_info)
for (var i=0; i<exchange_info.symbols.length; i++){
    if(symbols.indexOf(exchange_info.symbols[i].baseAsset) > -1){
       assets[exchange_info.symbols[i].baseAsset] = {amount:0, hold_price:0, value:0, bid_price:0, ask_price:0, 
                                                     btc_price:0, btc_change:1,btc_diff:0,
                                                     realised_profit:0, margin:0, unrealised_profit:0}
       trade_info[exchange_info.symbols[i].baseAsset] = {minQty:parseFloat(exchange_info.symbols[i].filters[1].minQty),
                                                         priceSize:parseInt((Math.log10(1.1/parseFloat(exchange_info.symbols[i].filters[0].tickSize)))),
                                                         amountSize:parseInt((Math.log10(1.1/parseFloat(exchange_info.symbols[i].filters[1].stepSize))))
                                                        }
    }
}
assets.USDT = {unrealised_profit:0, margin:0, margin_balance:0, total_balance:0, leverage:0, update_time:0}

function updateAccount(){ //Update account and positions
    var account = exchange.GetAccount()
    var pos = exchange.GetPosition()
    if (account == null || pos == null ){
        Log('update account time out')
        return
    }
    assets.USDT.update_time = Date.now()
    for(var i=0; i<trade_symbols.length; i++){
        assets[trade_symbols[i]].margin = 0
        assets[trade_symbols[i]].unrealised_profit = 0
        assets[trade_symbols[i]].hold_price = 0
        assets[trade_symbols[i]].amount = 0
        assets[trade_symbols[i]].unrealised_profit = 0
    } 
    for(var j=0; j<account.Info.positions.length; j++){
        var pair = account.Info.positions[j].symbol 
        var coin = pair.slice(0,pair.length-4)
        if(symbols.indexOf(coin) < 0){continue}
        assets[coin].margin = parseFloat(account.Info.positions[j].initialMargin) + parseFloat(account.Info.positions[j].maintMargin)
        assets[coin].unrealised_profit = parseFloat(account.Info.positions[j].unrealizedProfit)
    }
    assets.USDT.margin = _N(parseFloat(account.Info.totalInitialMargin) + parseFloat(account.Info.totalMaintMargin),2)
    assets.USDT.margin_balance = _N(parseFloat(account.Info.totalMarginBalance),2)
    assets.USDT.total_balance = _N(parseFloat(account.Info.totalWalletBalance),2)
    assets.USDT.unrealised_profit = _N(parseFloat(account.Info.totalUnrealizedProfit),2)
    assets.USDT.leverage = _N(assets.USDT.margin/assets.USDT.total_balance,2)
    
    if(pos.length > 0){
        pos = JSON.parse(exchange.GetRawJSON())
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

function updateIndex(){ //Update index
    var init_prices = {}
    if(!_G('init_prices') || Reset){
        for(var i=0; i<trade_symbols.length; i++){
            init_prices[trade_symbols[i]] = (assets[trade_symbols[i]].ask_price+assets[trade_symbols[i]].bid_price)/(assets.BTC.ask_price+assets.BTC.bid_price)
        }
        Log('Save the price at startup')
        _G('init_prices',init_prices)
    }else{
        init_prices = _G('init_prices')
        var temp = 0
        
        highIndex=0;
        lowIndex=0;
        var highChange;var lowChange;
        //This calculation identifies the maximum deviation high and low scores
        for(var i=0; i<trade_symbols.length; i++){
            assets[trade_symbols[i]].btc_price =  (assets[trade_symbols[i]].ask_price+assets[trade_symbols[i]].bid_price)/(assets.BTC.ask_price+assets.BTC.bid_price)
            if(!init_prices[trade_symbols[i]]){
                Log('Add new currency',trade_symbols[i])
                init_prices[trade_symbols[i]] = assets[trade_symbols[i]].btc_price 
                _G('init_prices',init_prices)
            }
            assets[trade_symbols[i]].btc_change = _N(assets[trade_symbols[i]].btc_price/init_prices[trade_symbols[i]],4)
            if(i==0){
                highChange=assets[trade_symbols[i]].btc_change;
                lowChange=assets[trade_symbols[i]].btc_change;
            }
            
            if(highChange<assets[trade_symbols[i]].btc_change){
                highChange=assets[trade_symbols[i]].btc_change;
                highIndex=i;
            }
            if(lowChange>assets[trade_symbols[i]].btc_change){
                lowChange=assets[trade_symbols[i]].btc_change;
                lowIndex=i;
            }
        }
        
        for(var i=0; i<trade_symbols.length; i++){
            assets[trade_symbols[i]].btc_price =  (assets[trade_symbols[i]].ask_price+assets[trade_symbols[i]].bid_price)/(assets.BTC.ask_price+assets.BTC.bid_price)
            assets[trade_symbols[i]].btc_change = _N(assets[trade_symbols[i]].btc_price/init_prices[trade_symbols[i]],4)
            if(i!=lowIndex&&i!=highIndex){ //Remove the influence of high and low points
                temp += assets[trade_symbols[i]].btc_change
            }
        }
        //Since the highest and lowest scores are removed, subtract2
        index = _N(temp/(trade_symbols.length-2), 4)
    }
    
}

function updateTick(){ //Update Quotes
    var ticker = HttpQuery('https://fapi.binance.com/fapi/v1/ticker/bookTicker')
    try {
        ticker = JSON.parse(ticker)
    }catch(e){
        Log('get ticker time out')
        return
    }
    for(var i=0; i<ticker.length; i++){
        var pair = ticker[i].symbol 
        var coin = pair.slice(0,pair.length-4)
        if(symbols.indexOf(coin) < 0){continue}
        assets[coin].ask_price = parseFloat(ticker[i].askPrice)
        assets[coin].bid_price = parseFloat(ticker[i].bidPrice)
        assets[coin].ask_value = _N(assets[coin].amount*assets[coin].ask_price, 2)
        assets[coin].bid_value = _N(assets[coin].amount*assets[coin].bid_price, 2)
    }
    updateIndex()
    for(var i=0; i<trade_symbols.length; i++){
        assets[trade_symbols[i]].btc_diff = _N(assets[trade_symbols[i]].btc_change - index, 4)
    }
}

function trade(symbol, dirction, value){ //Transaction
    if(Date.now()-assets.USDT.update_time > 10*1000){
        Log('Update account delay, do not trade')
        return
    }
    var price = dirction == 'sell' ? assets[symbol].bid_price : assets[symbol].ask_price
    var amount = _N(Math.min(value,Ice_value)/price, trade_info[symbol].amountSize)
    if(amount <= trade_info[symbol].minQty){
        Log(symbol, 'Contract value deviation or iceberg order size is set too small to meet the minimum transaction., At least needed: ', _N(trade_info[symbol].minQty*price,0))
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

function updateStatus(){ //Status bar information
        var table = {type: 'table', title: 'Trading pair information update', 
             cols: ['Symbol', 'amount', 'hold_price',  'price', 'diff', 'value', 'margin', 'unrealised_profit'],
             rows: []}
        var infoList;
    for (var i=0; i<symbols.length; i++){
        var price = _N((assets[symbols[i]].ask_price + assets[symbols[i]].bid_price)/2, trade_info[symbols[i]].priceSize)
        var value = _N((assets[symbols[i]].ask_value + assets[symbols[i]].bid_value)/2, 2)
        if(i==lowIndex){
           infoList = [symbols[i]+"Low", assets[symbols[i]].amount, assets[symbols[i]].hold_price, price, assets[symbols[i]].btc_diff, value, _N(assets[symbols[i]].margin,3), _N(assets[symbols[i]].unrealised_profit,3)]    
        }else if(i==highIndex){
           infoList = [symbols[i]+"High", assets[symbols[i]].amount, assets[symbols[i]].hold_price, price, assets[symbols[i]].btc_diff, value, _N(assets[symbols[i]].margin,3), _N(assets[symbols[i]].unrealised_profit,3)]
        }else{
           infoList = [symbols[i], assets[symbols[i]].amount, assets[symbols[i]].hold_price, price, assets[symbols[i]].btc_diff, value, _N(assets[symbols[i]].margin,3), _N(assets[symbols[i]].unrealised_profit,3)]
        }
        table.rows.push(infoList)
    }
    var logString = _D() + '   ' + JSON.stringify(assets.USDT) + ' Index:' + index + '\n'
    LogStatus(logString + '`' + JSON.stringify(table) + '`')
    
    if(Date.now()-update_profit_time > Log_profit_interval*1000){
        LogProfit(_N(assets.USDT.margin_balance,3))
        update_profit_time = Date.now()
    }
    
}

function onTick(){ //Strategy logic section
    for(var i=0; i<trade_symbols.length; i++){
        var symbol = trade_symbols[i]
        if(assets[symbol].ask_price == 0){ continue }
        var aim_value = -Trade_value * _N(assets[symbol].btc_diff/0.01,1)
        
        if(i!=lowIndex&&i!=highIndex){ //Do not trade high-low rated currencies
           if(aim_value - assets[symbol].ask_value > Adjust_value&&assets[symbol].ask_value<Max_amount){
              trade(symbol,'buy', aim_value - assets[symbol].ask_value)
           }
           if(aim_value - assets[symbol].bid_value < -Adjust_value&&assets[symbol].bid_value<Max_amount){
              trade(symbol,'sell', -(aim_value - assets[symbol].bid_value))
           }
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

https://www.fmz.com/strategy/196445

> Last Modified

2020-04-09 21:51:18
