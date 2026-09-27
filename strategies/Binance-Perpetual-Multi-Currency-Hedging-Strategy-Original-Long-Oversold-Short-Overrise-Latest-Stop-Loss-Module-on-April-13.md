
> Name

Binance-Perpetual-Multi-Currency-Hedging-Strategy-Original-Long-Oversold-Short-Overrise-Latest-Stop-Loss-Module-on-April-13

> Author

小草

> Strategy Description

The paid upgraded version of this strategy is now available, add WeChat wangweibing_ustb for details

## **Important content!!**

- Be sure to read this study https://www.fmz.com/digest-topic/5294 first. Understand a series of issues such as strategy principles, risks, how to screen trading pairs, how to set parameters, the ratio of opening positions to total funds, etc.
- The previous research report needs to be downloaded and uploaded to your own research environment. Run the actual modifications. If you have already seen this report, it was recently updated with data for the latest week.
- If the robot has been stopped for a long time before restarting, be sure to reset data or create a new robot
- **The strategy cannot be backtested directly and needs to be backtested in the research environment**.
- Strategy code and default parameters are for research purposes only. Caution is required for live trading; set parameters based on your own research, **at your own risk**.**.
- **The strategy cannot be profitable every day. You can check backtest history; sideways movement and drawdowns over 1-2 weeks are normal and need to be handled correctly**
- The code is public and can be modified by yourself. If you have any questions, please leave comments and feedback. It is best to join the inventor's Binance exchange group (how to join is in the research report) to get update notifications.
- **The strategy only supports Binance futures and needs to be run in full position mode. Do not set two-way positions! ! , just use the default trading pair and candlestick cycle when creating the robot. The strategy does not use candlestick.**
- **The strategy conflicts with other strategies and manual operations, so you need to pay attention**
- Overseas hosts are required for real-time operation. During the test phase, you can rent Alibaba Cloud Hong Kong servers with one click on the platform. It is cheaper to rent the entire server by yourself on a monthly basis (the lowest configuration is sufficient, please refer to the deployment tutorial:https://www.fmz.com/bbs-topic/2848)
- Binance's futures and spot need to be added separately. Binance futures are``Futures_Binance``
- Restarting this strategy does not affect it, but creating a new robot will re-record historical data.
- The strategy may be updated based on user feedback. Just ctrl+A to copy the code and save it (generally the parameters will not be updated). Restart the robot to use the latest code.
- The strategy does not trade at the beginning. The first startup requires recording data, and trading will only occur after market changes.
## 4.16Daily update content

Changed stop lossbug

Default parameters modified:

```
var Alpha = 0.001 //Exponential moving averageAlphaParameter, the larger the setting, the more sensitive the benchmark price tracking will be, and the final position will be lower, which reduces the leverage, but will reduce the income. You need to weigh it based on the backtest results.
var Update_base_price_time_interval = 60 //How often to update the benchmark price, in seconds, related to the Alpha parameter. The smaller the Alpha setting, the smaller the interval can also be set.
```

## 4.13 Updated content

Stop_lossSetting it to 0.8 means that when the funds reach less than 80% of the initial funds, stop loss, clear all positions, and stop the strategy. As the strategy runs, Stop_loss can be set to greater than 1 (restart to take effect). For example, if you earn 1,500 from 1,000, and Stop_loss is set to 1.3, then the stop loss will be retraced to 1,300 yuan. If you don't want to stop the loss, you can set this parameter very small. The risk is that if everyone uses this kind of stop loss, it will cause a stampede and increase losses. The initial funds are in the init_balance field of the status bar. Please note that operations such as withdrawals will be affected. Don't accidentally stop the loss. If you are still afraid of black swan events, such as a certain currency returning to 0, etc., you can withdraw it manually.

Max_diffand Min_diff limit the degree of deviation, which needs to be determined by yourself based on your own trade_value, total funds and risk tolerance.

To give a simple example, if a total of 20 coins are traded, the value of one of the coins gradually rises to a deviation of 0.4 and is no longer traded, while the prices of other coins remain unchanged, resulting in a loss of 7 times the trade_value. If it continues to fall to a deviation of -0.3, it will lose 6 times of trade_value.

```
var Stop_loss = 0.8 
var Max_diff = 0.4 //When deviationdiffGreater than0.4Do not continue adding short positions at, Set by oneself
var Min_diff = -0.3 //whendiffLess Than-0.3Do not continue adding long positions at, Set by oneself
```

## 4.10 Updated content

**Copy the policy code to the local policy, overwrite and save directly. Restart the bot to take effect, and the original position will be retained**

Binance Futures short-selling, long-selling, and falling strategies are important to optimize the notebook code address.:https://www.fmz.com/bbs-topic/5364 

Original strategy altcoin index = mean(sum((altcoin price/bitcoin price)/(altcoin initial price/bitcoin initial price))). The biggest problem is that the comparison between the latest price and the initial price when the strategy is started will deviate more and more as time goes by. A coin may hold many positions, which is very risky. In the end, it will hold many positions, increasing risks and drawdowns.

The latest altcoin index = mean(sum((altcoin price/bitcoin price)/EMA(altcoin price/bitcoin price))), which is compared with the price of the moving average, can track the latest price changes, is more flexible, and backtesting has found that it reduces strategic positions and also reduces retracement. More stable. The most important thing is that if a few abnormal trading pairs were added to the original strategy, the risk would be extremely high and the position would probably be liquidated, but now it is almost unaffected.

For seamless upgrades, two parameters are written in the first two lines of the strategy code and can be modified as needed.

Alpha = 0.04 The larger the Alpha parameter of the index moving tie is set, the more sensitive the benchmark price tracking will be. The fewer transactions will be made, the lower the final position will be. This reduces the leverage, but will reduce the income, reduce the maximum drawdown, and can increase the trading volume. You need to weigh it based on the backtest results.
Update_base_price_time_interval = 30*60 How often to update the benchmark price, in seconds, related to the Alpha parameter. The smaller the Alpha setting, the smaller the interval can also be set.

If you read the article and want to trade all currencies, here is the list``ETH,BCH,XRP,EOS,LTC,TRX,ETC,LINK,XLM,ADA,XMR,DASH,ZEC,XTZ,BNB,ATOM,ONT,IOTA,BAT,VET,NEO,QTUM,IOST``


## Join the WeChat group to participate in Binance Thousand Group Battle for updates

Add the WeChat ID below, reply "Binance" to be automatically added to the group:

https://www.fmz.com![IMG](https://www.fmz.com/upload/asset/1fbed0c3795dbecac04.jpg)

## Strategy Principle

We will short the currency whose price is higher than the altcoin-Bitcoin price index and long the currency whose price is lower than the index. The greater the deviation, the larger the position. (This strategy does not use BTC to hedge unequal positions. BTC can also be added to the trading pair). Performance in the past two months (about 3 times leverage, data updated to4.8):
 ![IMG](https://www.fmz.com/upload/asset/1b2a6f297fcf590ad02.png) 

## Strategy Logic

1.Update market prices and account positions. The initial price will be recorded in the first run (newly added currencies are calculated based on the time of addition))
2.Update the index, the index is Altcoin-Bitcoin price index = mean(sum((Altcoin price/Bitcoin price)/(Altcoin initial price/Bitcoin initial price)))
3.Determine long or short positions based on deviation index, determine position size based on deviation magnitude
4.Place an order. The order quantity is determined by Bingshan Commission, and the transaction is completed according to the counterparty price (buy at the same price as the sell). **Cancel the order immediately after placing it (so you will see many orders with failed cancellation 400: {"code":-2011,"msg":"Unknown order sent."}, normal phenomenon)**
5.Loop again

The leverage in the status bar represents the margin used percentage, which needs to be maintained at a low level to accommodate new positions

## Strategy Arguments

 ![IMG](https://www.fmz.com/upload/asset/272b24a9c0018c96fb6.png) 

- Trade_symbols:Trading coins should be selected based on your own research platform, can also be added.BTC
- Trade_value:Every 1% deviation of the altcoin price (priced in BTC) from the holding value of the index needs to be determined based on the total funds invested and risk preference. It is recommended to set it to 3-10% of the total funds. The size of the leverage can be seen through backtesting in the research environment. Trade_value can be less than Adjust_value, such as half of Adjust_value, which is equivalent to a holding value that deviates from the index by 2%.
- Adjust_value:	Contract value (priced in USDT) adjusts the deviation value. When the index deviates from \* Trade_value - current position > Adjust_value, that is, the difference between the target position and the current position exceeds this value, a transaction will start. If it is too large, the adjustment will be slow. If it is too small, transactions will be frequent. It cannot be lower than 10, otherwise the minimum transaction will not be reached. It is recommended to set it to more than 40% of Trade_value.
- Ice_value:The iceberg commission value cannot be less than 10. When placing a single order, choose the smaller one between Adjust_value and Ice_value. If you have more funds, you can set it to a relatively large value so that the adjustment can be made faster. It is recommended not to be less than 20% of Adjust_value, so that the transaction can be completed in 5 times of Iceberg. Of course, when the Trade_value is not large, Ice_value can be set to a relatively large value, and it can be adjusted in one or two times.
- Interval:Loop Sleep Time: It can be set shorter, e.g., 1s, but cannot exceed Binance frequency limits.
- Reset:Reset historical data, which will reset the initial price referenced by the strategy to the current price, usually not set.


## Strategy Risks

noticed that if a certain currency goes out of independent market, for example, it rises several times relative to the index, a large number of short positions will be accumulated on the currency, and the same sharp decline will also cause the strategy to go long in large quantities. You can limit the opening amount or stop loss and no longer trade.



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Trade_symbols|QTUM,DASH,ADA,BNB,XMR,ZEC,ATOM,IOTA,NEO,ONT,XRP,BAT,VET,EOS,ETC,LTC|Transaction currency|
|Trade_value|20|Holding value for every 1% deviation from the index|
|Adjust_value|20|Contract value adjustment deviation|
|Ice_value|20|Size of iceberg order|
|Log_profit_interval|600|LogTotal equity intervals|
|Interval|true|Dormant Times|
|Reset|false|Reset historical data|


> Source (javascript)

``` javascript


var Alpha = 0.001 //Exponential moving averageAlphaParameter, the larger the setting, the more sensitive the benchmark price tracking will be, and the final position will be lower, which reduces the leverage, but will reduce the income. You need to weigh it based on the backtest results.
var Update_base_price_time_interval = 60 //How often to update the benchmark price, in seconds, related to the Alpha parameter. The smaller the Alpha setting, the smaller the interval can also be set.

//Stop_lossSet as0.8Indicates when funds fall below the initial capital80%Trigger stop loss, clear all positions, and stop the strategy.
//As the strategy runs,Stop_lossCan set greater than1(Effective after restart), for example from1000Earn1500,Stop_lossSet as1.3,Then draw down to1300Yuan stop loss. If you don't want to stop the loss, you can set this parameter very small.
//The risk is that if everyone uses this stop loss, it will cause a stampede and increase losses.
//Initial funds in the status barinit_balancefield, please note that operations such as withdrawals will be affected. Don't accidentally stop the loss.
//If still afraid of black swan events, for example if a coin returns0Waiting, can manually withdraw.

var Stop_loss = 0.8 
var Max_diff = 0.4 //When deviationdiffGreater than0.4Do not continue adding short positions at, Set by oneself
var Min_diff = -0.3 //whendiffLess Than-0.3Do not continue adding long positions at, Set by oneself

if(IsVirtual()){
    throw 'Cannot backtest, reference for backtest https://www.fmz.com/digest-topic/5294 '
}
if(exchange.GetName() != 'Futures_Binance'){
    throw 'Only supports Binance futures exchange, which is different from spot exchange and needs to be added separately with the nameFutures_Binance'
}
var trade_symbols = Trade_symbols.split(',')
var symbols = trade_symbols
var index = 1 //Index
if(trade_symbols.indexOf('BTC')<0){
    symbols = trade_symbols.concat(['BTC'])
}
var update_profit_time = 0
var update_base_price_time= Date.now()
var assets = {}
var init_prices = {}


var trade_info = {}
var exchange_info = HttpQuery('https://fapi.binance.com/fapi/v1/exchangeInfo')
if(!exchange_info){
    throw 'Unable to connect to Binance network, requires overseas hosting'
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
assets.USDT = {unrealised_profit:0, margin:0, margin_balance:0, total_balance:0, leverage:0, update_time:0, init_balance:0, stop_balance:0, short_value:0, long_value:0, profit:0}

function updateAccount(){ //Update account and positions
    exchange.SetContractType('swap')
    var account = exchange.GetAccount()
    var pos = exchange.GetPosition()
    if (!account || !pos){
        Log('update account time out')
        return
    }
    assets.USDT.update_time = Date.now()
    for(var i=0; i<trade_symbols.length; i++){
        assets[trade_symbols[i]].margin = 0
        assets[trade_symbols[i]].unrealised_profit = 0
        assets[trade_symbols[i]].hold_price = 0
        assets[trade_symbols[i]].amount = 0
    } 
    for(var j=0; j<account.Info.positions.length; j++){
        if(account.Info.positions[j].positionSide == 'BOTH'){
            var pair = account.Info.positions[j].symbol 
            var coin = pair.slice(0,pair.length-4)
            if(trade_symbols.indexOf(coin) < 0){continue}
            assets[coin].margin = parseFloat(account.Info.positions[j].initialMargin) + parseFloat(account.Info.positions[j].maintMargin)
            assets[coin].unrealised_profit = parseFloat(account.Info.positions[j].unrealizedProfit)
        }
    }
    assets.USDT.margin = _N(parseFloat(account.Info.totalInitialMargin) + parseFloat(account.Info.totalMaintMargin),2)
    assets.USDT.margin_balance = _N(parseFloat(account.Info.totalMarginBalance),2)
    assets.USDT.total_balance = _N(parseFloat(account.Info.totalWalletBalance),2)
    if(assets.USDT.init_balance == 0){
        if(_G('init_balance')){
            assets.USDT.init_balance = _N(_G('init_balance'),2)
        }else{
            assets.USDT.init_balance = assets.USDT.total_balance 
            _G('init_balance',assets.USDT.init_balance)
        }
    }
    assets.USDT.profit = _N(assets.USDT.margin_balance - assets.USDT.init_balance, 2)
    assets.USDT.stop_balance = _N(Stop_loss*assets.USDT.init_balance, 2)
    assets.USDT.total_balance = _N(parseFloat(account.Info.totalWalletBalance),2)
    assets.USDT.unrealised_profit = _N(parseFloat(account.Info.totalUnrealizedProfit),2)
    assets.USDT.leverage = _N(assets.USDT.margin/assets.USDT.total_balance,2)
    pos = JSON.parse(exchange.GetRawJSON())
    if(pos.length > 0){
        for(var k=0; k<pos.length; k++){
            var pair = pos[k].symbol
            var coin = pair.slice(0,pair.length-4)
            if(trade_symbols.indexOf(coin) < 0){continue}
            if(pos[k].positionSide != 'BOTH'){continue}
            assets[coin].hold_price = parseFloat(pos[k].entryPrice)
            assets[coin].amount = parseFloat(pos[k].positionAmt)
            assets[coin].unrealised_profit = parseFloat(pos[k].unRealizedProfit)
        }
    }
}

function updateIndex(){ //Update index
    
    if(!_G('init_prices') || Reset){
        Reset = false
        for(var i=0; i<trade_symbols.length; i++){
            init_prices[trade_symbols[i]] = (assets[trade_symbols[i]].ask_price+assets[trade_symbols[i]].bid_price)/(assets.BTC.ask_price+assets.BTC.bid_price)
        }
        Log('Save the price at startup')
        _G('init_prices',init_prices)
    }else{
        init_prices = _G('init_prices')
        if(Date.now() - update_base_price_time > Update_base_price_time_interval*1000){
            update_base_price_time = Date.now()
            for(var i=0; i<trade_symbols.length; i++){ //Update initial price
                init_prices[trade_symbols[i]] = init_prices[trade_symbols[i]]*(1-Alpha)+Alpha*(assets[trade_symbols[i]].ask_price+assets[trade_symbols[i]].bid_price)/(assets.BTC.ask_price+assets.BTC.bid_price)
            }
            _G('init_prices',init_prices)
        }
        var temp = 0
        for(var i=0; i<trade_symbols.length; i++){
            assets[trade_symbols[i]].btc_price =  (assets[trade_symbols[i]].ask_price+assets[trade_symbols[i]].bid_price)/(assets.BTC.ask_price+assets.BTC.bid_price)
            if(!(trade_symbols[i] in init_prices)){
                Log('Add new currency',trade_symbols[i])
                init_prices[trade_symbols[i]] = assets[trade_symbols[i]].btc_price / index
                _G('init_prices',init_prices)
            }
            assets[trade_symbols[i]].btc_change = _N(assets[trade_symbols[i]].btc_price/init_prices[trade_symbols[i]],4)
            temp += assets[trade_symbols[i]].btc_change
        }
        index = _N(temp/trade_symbols.length, 4)
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
    assets.USDT.short_value = 0
    assets.USDT.long_value = 0
    for(var i=0; i<ticker.length; i++){
        var pair = ticker[i].symbol 
        var coin = pair.slice(0,pair.length-4)
        if(symbols.indexOf(coin) < 0){continue}
        assets[coin].ask_price = parseFloat(ticker[i].askPrice)
        assets[coin].bid_price = parseFloat(ticker[i].bidPrice)
        assets[coin].ask_value = _N(assets[coin].amount*assets[coin].ask_price, 2)
        assets[coin].bid_value = _N(assets[coin].amount*assets[coin].bid_price, 2)
        if(trade_symbols.indexOf(coin) < 0){continue}
        if(assets[coin].amount<0){
            assets.USDT.short_value += Math.abs((assets[coin].ask_value+assets[coin].bid_value)/2)
        }else{
            assets.USDT.long_value += Math.abs((assets[coin].ask_value+assets[coin].bid_value)/2)
        }
        assets.USDT.short_value = _N(assets.USDT.short_value,0)
        assets.USDT.long_value = _N(assets.USDT.long_value,0)
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
    if(amount < trade_info[symbol].minQty){
        Log(symbol, 'Contract value deviation or iceberg order size is set too small to meet the minimum transaction., At least needed: ', _N(trade_info[symbol].minQty*price,0)+1)
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
    return id
}



function updateStatus(){ //Status bar information
        var table = {type: 'table', title: 'Trading pair information', 
             cols: ['Currency', 'Quantity', 'Position Price', 'Current Price', 'Deviation from Average', 'Position Value', 'Margin', 'Unrealized Profit and Loss''],
             rows: []}
    for (var i=0; i<symbols.length; i++){
        var price = _N((assets[symbols[i]].ask_price + assets[symbols[i]].bid_price)/2, trade_info[symbols[i]].priceSize)
        var value = _N((assets[symbols[i]].ask_value + assets[symbols[i]].bid_value)/2, 2)
        var infoList = [symbols[i], assets[symbols[i]].amount, assets[symbols[i]].hold_price, price, assets[symbols[i]].btc_diff, value, _N(assets[symbols[i]].margin,3), _N(assets[symbols[i]].unrealised_profit,3)]
        table.rows.push(infoList)
    }
    var logString = _D() + '   ' + JSON.stringify(assets.USDT) + ' Index:' + index + '\n'
    LogStatus(logString + '`' + JSON.stringify(table) + '`')
    
    if(Date.now()-update_profit_time > Log_profit_interval*1000){
        LogProfit(_N(assets.USDT.margin_balance,3))
        update_profit_time = Date.now()
    }
    
}

function stopLoss(){ //Stop-loss function
    while(true){
        if(assets.USDT.margin_balance < Stop_loss*assets.USDT.init_balance && assets.USDT.init_balance > 0){
            Log('Trigger stop-loss, current funds:', assets.USDT.margin_balance, 'Initial capital:', assets.USDT.init_balance)
            Ice_value = 200 //Stop loss faster, can be modified
            updateAccount()
            updateTick()
            var trading = false //Is it trading
            for(var i=0; i<trade_symbols.length; i++){
                var symbol = trade_symbols[i]
                if(assets[symbol].ask_price == 0){ continue }
                if(assets[symbol].bid_value >= trade_info[symbol].minQty*assets[symbol].bid_price){
                    trade(symbol, 'sell', assets[symbol].bid_value)
                    trading = true
                }
                if(assets[symbol].ask_value <= -trade_info[symbol].minQty*assets[symbol].ask_price){
                    trade(symbol, 'buy', -assets[symbol].ask_value)
                    trading = true
                }
            }
            Sleep(1000)
            if(!trading){
                throw 'Stop loss ends. If you need to re-run the strategy, you need to lower the stop loss.'
            }
        }else{ //No need for stop-loss
            return
        }
    }    
}

function onTick(){ //Strategy logic section
    for(var i=0; i<trade_symbols.length; i++){
        var symbol = trade_symbols[i]
        if(assets[symbol].ask_price == 0){ continue }
        var aim_value = -Trade_value * _N(assets[symbol].btc_diff/0.01,3)
        if(aim_value - assets[symbol].ask_value >= Adjust_value && assets[symbol].btc_diff > Min_diff && assets.USDT.long_value-assets.USDT.short_value <= 1.1*Trade_value){
            trade(symbol,'buy', aim_value - assets[symbol].ask_value)
        }
        if(aim_value - assets[symbol].bid_value <= -Adjust_value && assets[symbol].btc_diff < Max_diff && assets.USDT.short_value-assets.USDT.long_value <= 1.1*Trade_value){
            trade(symbol,'sell', -(aim_value - assets[symbol].bid_value))
        }
    }
}

function main() {
    while(true){
        updateAccount()
        updateTick()
        stopLoss() //stop loss
        onTick()
        updateStatus()
        Sleep(Interval*1000)
    }
}
```

> Detail

https://www.fmz.com/strategy/195226

> Last Modified

2020-08-20 16:03:49
