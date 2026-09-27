
> Name

Binance-Futures-Butterfly-Arbitrage-Thousand-Group-War-Strategy-3

> Author

小草

> Strategy Description

Binance butterfly arbitrage strategy cannot be backtested. For specific principles, refer to the article in the documentation:https://www.fmz.com/digest-topic/6102

**You need to read this strategy manual, and you cannot run it without thinking. The strategy code is for reference only and can be modified as needed. Feedback is welcome.**

### Strategy Principle

Binance currency-based contracts such as BTC, ETH, etc. have three contracts at the same time, namely perpetual BTCUSD_PERP, current quarter BTCUSD_200925, and second quarterBTCUSD_201225.

Perpetual contracts can be treated like spot contracts. Generally, when hedging with two contracts, there are three spreads: nearby-perpetual, next quarter-perpetual, and next quarter-nearby. Butterfly arbitrage requires trading three contracts, and the spread is (next quarter - nearby) - (nearby - perpetual), that is, spread = next quarter + perpetual - 2 * nearby. To go long on the spread, one needs to go long one next quarter and one perpetual contract, and short two nearby contracts.

### Strategy Arguments

- Trading currencies: perpetual, current quarter, and next quarter varieties must all exist simultaneously.
- Number of orders placed: Number of orders placed in each grid.
- Grid opening price difference: for each price deviation, go long or short one share.
- Spread smoothing parameter Alpha: used to calculate the mean of the spread, can use the default value or backtest your own.
- Iceberg order number: If the number of open positions is too large, in order to reduce the single-leg phenomenon, you can set the minimum number of orders each time. The disadvantage is that it is not timely to grab the price difference. No iceberg commission is required. This parameter setting is the same as the number of orders placed.

If the moving average of the price difference is 100, the current price difference is 200, the number of orders placed is 2, and the grid opening price difference is 30, then the positions at this time are: 6 short positions in the second quarter, 6 permanent short positions, and 12 long positions in the current quarter. If you are not sure, you can look at the code specifically.

### Notes

- Delivery contracts require one-way positions, that is, holding long and short positions at the same time.
- Margin is in cross mode.
- This strategy is not a mindless running strategy; test cautiously under an understanding of the principles.
- The backtesting in research articles does not reflect real trading conditions, parameter optimization is unnecessary.
- If the robot has not been running for a long time, a new robot needs to be created to prevent large price differences.
- The grid opening spread parameter must cover the handling fee. For example, the taker handling fee is 20,000 and the Bitcoin price is 10,000. It must be at least greater than 8\*10000\*0.0002=16. Plus a certain margin, it can be set to25-30.
- As delivery approaches, the time difference between the second quarter and the current quarter, and the current quarter and the perpetuity becomes larger and larger. Finally, the current quarter is close to the perpetuity. Butterfly arbitrage is actually an arbitrage between the second quarter and perpetuity and cannot be run. It needs to be stopped 2 weeks before delivery or to observe whether it continues to run. In the same way, new contracts should also be observed.
- When placing an order using IOC, the tradable part will be immediately executed at the entrusted price (or better), and the part that cannot be fully executed immediately will be cancelled. So there is no need to cancel the order.
- With slight modification, this strategy can also be adapted for arbitrage between the current and perpetual contracts or the next-quarter and perpetual contracts.
- The strategy will not open or close positions frequently, and it is possible not to open an order in a day.
- The robot starts calculating the average spread only after it begins operation, it will not trace historical data.
- The strategy is likely to be single-legged due to the inability to close the transaction. It can be optimized by itself.
- The slip price is added to the order, which has little effect on the number of small open positions. For large open positions, you need to optimize it yourself, such as the iceberg order.











> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Symbol|BTC|Transaction currency|
|Trade_value|true|Order Quantity|
|Grid|false|Grid order price difference|
|Alpha|1e-06|Price difference smoothing parameterAlpha|
|Ice_value|5|Iceberg order quantity|


> Source (javascript)

``` javascript
if(IsVirtual()){
    throw 'Cannot backtest; refer to research articles for backtesting https://www.fmz.com/digest-topic/6102'
}
if(exchange.GetName() != 'Futures_Binance'){
    throw 'Only supports Binance futures exchange, which is different from spot exchange and needs to be added separately with the nameFutures_Binance'
}
if(Grid == 0){
    throw 'Need to set grid price difference, cover 8 portions of transaction fees, can be set at the current price.*fee*15'
}

exchange.SetBase("https://dapi.binance.com") //Switch to delivery contract

var exchange_info = HttpQuery('https://dapi.binance.com/dapi/v1/exchangeInfo')
if(!exchange_info){
    throw 'Cannot connect to the Binance network, requires a non-public overseas custodian.'
}
exchange_info = JSON.parse(exchange_info)
trade_info = {} //Contract basic information
trade_contract = {NEXT_QUARTER:'',CURRENT_QUARTER:'',PERPETUAL:''} //The contract code that needs to be traded
for (var i=0; i<exchange_info.symbols.length; i++){
   trade_info[exchange_info.symbols[i].symbol] =  exchange_info.symbols[i]
   if(exchange_info.symbols[i].baseAsset == Symbol && exchange_info.symbols[i].contractType in trade_contract && exchange_info.symbols[i].contractStatus == 'TRADING'){
       trade_contract[exchange_info.symbols[i].contractType] = exchange_info.symbols[i].symbol
   }
}
if(!(trade_contract.NEXT_QUARTER && trade_contract.CURRENT_QUARTER && trade_contract.PERPETUAL)){
    throw 'Unable to find the three contracts for the butterfly hedge'
}
var pricePrecision = trade_info[trade_contract.PERPETUAL].pricePrecision //Price Precision

var ticker = {}
var account = {}
var position = {}

var diff_mean = null //Average price difference
if(_G('diff_mean') && _G('symbol') == Symbol){ //Prevent currency switching and price difference errors
    diff_mean = _G('diff_mean')
}else{
    _G('symbol',Symbol)
}

var diff_buy = 0 //Spread of long positions
var diff_sell = 0 //Short spread
Trade_value = _N(Trade_value, 0)
 
var init_asset = 0 //Initial capital
if(_G('init_asset')){
    init_asset = _G('init_asset')
}else{
    updateAccount()
    init_asset = parseFloat(account[Symbol].marginBalance)
    _G('init_asset', init_asset)
}
var update_status_time = 0
var update_account_time = Date.now()

function onexit(){
    _G('diff_mean', diff_mean)
}

function updateTicker(){
    var bookTicker =  HttpQuery('https://dapi.binance.com/dapi/v1/ticker/bookTicker')
    try {
        bookTicker = JSON.parse(bookTicker)
        for(var i=0;i<bookTicker.length;i++){
            ticker[bookTicker[i].symbol] = bookTicker[i]
        }
    } catch (e) {
        Log('Unable to get market data')
    }
}

function updateAccount(){
    var acc = exchange.IO("api", "GET", "/dapi/v1/account", "timestamp="+Date.now())
    if(!acc){
        Log('Unable to get account')
        return
    }
    for(var i=0;i<acc.assets.length;i++){
        account[acc.assets[i].asset] = acc.assets[i]
    }
}

function updatePosition(){
    var pos = exchange.IO("api", "GET", "/dapi/v1/positionRisk", "timestamp="+Date.now())
    if(!pos){
        Log('Unable to get position')
        return
    }
    for(var i=0;i<pos.length;i++){
        position[pos[i].symbol] = pos[i]
    }
}

function updateStatus(){
    if(Date.now() - update_status_time < 4000){
        return
    }
    update_status_time = Date.now()
    if(Date.now() - update_account_time >  5*60*1000){
        update_account_time = Date.now()
        updateAccount()
        LogProfit(_N(parseFloat(account[Symbol].marginBalance) - init_asset, 5))
    }
    
    $.PlotLine('buy', _N(diff_buy, pricePrecision))
    $.PlotLine('sell', _N(diff_sell, pricePrecision))
    $.PlotLine('mean', _N(diff_mean, pricePrecision+3))
    
    var table1 = {type: 'table', title: 'Account Information', 
             cols: ['Account balance', 'Unrealized profit and loss', 'Margin balance', 'Available balance', 'Maintenance margin', 'Initial margin', 'BNB', 'Initial balance', 'Profit', 'Average spread', 'Long spread', 'Short spread', 'Order volume''],
             rows: [[_N(parseFloat(account[Symbol].walletBalance),5), _N(parseFloat(account[Symbol].unrealizedProfit),5), _N(parseFloat(account[Symbol].marginBalance),5), 
                     _N(parseFloat(account[Symbol].availableBalance),5),  _N(parseFloat(account[Symbol].maintMargin),5), _N(parseFloat(account[Symbol].initialMargin),5), 
                     _N(parseFloat(account.BNB.walletBalance),5), _N(init_asset,5),
                      _N(parseFloat(account[Symbol].marginBalance) - init_asset,5), _N(diff_mean, pricePrecision+1),
                     _N(diff_buy, pricePrecision),_N(diff_sell, pricePrecision), Trade_value
                    ]]}
    var table2 = {type: 'table', title: 'Hedging information', 
             cols: ['Contract', 'Number of positions', 'Bid', 'Ask', 'Position value', 'Leverage', 'Average opening price', 'Unrealized profit and loss''],
             rows: []}
    for(var contract in trade_contract){
        var symbol = trade_contract[contract]
        table2.rows.push([symbol, position[symbol].positionAmt, ticker[symbol].bidPrice, ticker[symbol].askPrice, 
                          parseInt(position[symbol].positionAmt)*parseInt(trade_info[symbol].contractSize), position[symbol].leverage,
                         position[symbol].entryPrice, position[symbol].unRealizedProfit])
    }
    var logString = _D()+'  Last update time of strategy code9Moon29day\n'
    LogStatus(logString + '`' + JSON.stringify(table1) + '`'+'\n'+'`' + JSON.stringify(table2) + '`')
}

function trade(symbol, side, price, amount){
    //IOCPlace order; unfilled portions will be automatically canceled
    exchange.Log(side == 'BUY' ? LOG_TYPE_BUY : LOG_TYPE_SELL, price, amount, ' buy: ' + _N(diff_buy, pricePrecision) + ' sell: '+ _N(diff_sell, pricePrecision) + ' mean: '+_N(diff_mean, pricePrecision+3))
    exchange.IO("api", "POST","/dapi/v1/order","symbol="+symbol+"&side="+side+"&type=LIMIT&timeInForce=IOC&quantity="+amount+"&price="+price+"&timestamp="+Date.now())
}


function onTicker(){
    
    //Since it is a taker order, the price difference between long and short needs to be calculated separately.
    diff_sell = parseFloat(ticker[trade_contract.NEXT_QUARTER].bidPrice) + parseFloat(ticker[trade_contract.PERPETUAL].bidPrice) -
                2*parseFloat(ticker[trade_contract.CURRENT_QUARTER].askPrice)
    diff_buy = parseFloat(ticker[trade_contract.NEXT_QUARTER].askPrice) + parseFloat(ticker[trade_contract.PERPETUAL].askPrice)  -
                2*parseFloat(ticker[trade_contract.CURRENT_QUARTER].bidPrice)

    
    if(!diff_mean){diff_mean = (diff_buy+diff_sell)/2}
    diff_mean = diff_mean*(1-Alpha) + Alpha*(diff_buy+diff_sell)/2 //Update of average price difference
    
    
    var aim_buy_amount = -Trade_value*(diff_buy - diff_mean)/Grid
    var aim_sell_amount = -Trade_value*(diff_sell - diff_mean)/Grid 
    
    if(aim_buy_amount - parseFloat(position[trade_contract.PERPETUAL].positionAmt) > Trade_value){ //Go long the price difference, the price has a slippage
        trade(trade_contract.PERPETUAL, 'BUY', _N(parseFloat(ticker[trade_contract.PERPETUAL].askPrice)*1.01, pricePrecision), _N(Math.min(aim_buy_amount-parseFloat(position[trade_contract.PERPETUAL].positionAmt),Ice_value),0))
    }
    if(aim_buy_amount - parseFloat(position[trade_contract.NEXT_QUARTER].positionAmt) > Trade_value){
        trade(trade_contract.NEXT_QUARTER, 'BUY', _N(parseFloat(ticker[trade_contract.NEXT_QUARTER].askPrice)*1.01,pricePrecision), _N(Math.min(aim_buy_amount-parseFloat(position[trade_contract.NEXT_QUARTER].positionAmt),Ice_value),0))
    }
    if(-2*aim_buy_amount - parseFloat(position[trade_contract.CURRENT_QUARTER].positionAmt) < -2*Trade_value){
        trade(trade_contract.CURRENT_QUARTER, 'SELL', _N(parseFloat(ticker[trade_contract.CURRENT_QUARTER].bidPrice)*0.99,pricePrecision), _N(2*Math.min(aim_buy_amount+parseFloat(position[trade_contract.CURRENT_QUARTER].positionAmt),Ice_value),0))
    }
    
    if(aim_sell_amount - parseFloat(position[trade_contract.PERPETUAL].positionAmt) < -Trade_value){ //Short the difference
        trade(trade_contract.PERPETUAL, 'SELL', _N(parseFloat(ticker[trade_contract.PERPETUAL].bidPrice)*0.99,pricePrecision), _N(Math.min(parseFloat(position[trade_contract.PERPETUAL].positionAmt)-aim_sell_amount,Ice_value),0))
    }
    if(aim_sell_amount - parseFloat(position[trade_contract.NEXT_QUARTER].positionAmt) < -Trade_value){
        trade(trade_contract.NEXT_QUARTER, 'SELL', _N(parseFloat(ticker[trade_contract.NEXT_QUARTER].bidPrice)*0.99,pricePrecision), _N(Math.min(parseFloat(position[trade_contract.NEXT_QUARTER].positionAmt)-aim_sell_amount,Ice_value),0))
    }
    if(-2*aim_sell_amount - parseFloat(position[trade_contract.CURRENT_QUARTER].positionAmt) > 2*Trade_value){
        trade(trade_contract.CURRENT_QUARTER, 'BUY', _N(parseFloat(ticker[trade_contract.CURRENT_QUARTER].askPrice)*1.01,pricePrecision), _N(-2*Math.min(aim_sell_amount-parseFloat(position[trade_contract.CURRENT_QUARTER].positionAmt),Ice_value),0))
    }
}

function main() {
    updateAccount()
    updatePosition()
    while(true){
        updateTicker()
        updatePosition()
        onTicker()
        updateStatus()
        Sleep(1*1000)
    }
}
```

> Detail

https://www.fmz.com/strategy/226882

> Last Modified

2021-09-07 14:40:17
