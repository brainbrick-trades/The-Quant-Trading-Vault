
> Name

Single-Spot-Currency-Balanced-Strategy

> Author

小草

> Strategy Description

The most classic single-currency balancing strategy is to sell when the price rises and buy when the price falls, and always maintain a certain proportion of positions. A relatively moderate strategy that requires long-term operation.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Ratio|0.5|Holding ratio|
|Grid_Ratio|0.005|Adjust the proportion|
|Advance|false|Show more parameters|
|Intervel|1000|Dormant Timems|
|Log_profit|600000|Print profit timems|


> Source (javascript)

``` javascript
/*backtest
start: 2019-07-24 00:00:00
end: 2020-07-23 23:59:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Binance","currency":"BTC_USDT","stocks":1.2,"fee":[0.1,0.1]}]
*/

var order = {buy_price:0,buy_amount:0,buy_id:0,sell_price:0,sell_amount:0,sell_id:0}
var account = null
var last = 0
var symbol = ''

var log_profit_time = 0
var update_status_time = 0
var update_alpha_time = Date.now()
var total_trade_volume = 0

if(exchange.GetName().slice(0,7) == 'Futures'){
    throw 'This strategy only supports spot'
}
if(Ratio < 0.0005){
    throw 'Grid density should not be less than one ten-thousandth5'
}
if(_G('symbol')){
    symbol = _G('symbol')
}else{
    symbol = exchange.GetCurrency()
    _G('symbol', symbol)
}
if(exchange.GetCurrency() != symbol){
    throw 'Cannot change the currency, need to create a new bot'
}

function GetPrecision(){
    if(IsVirtual()){
        return {price:6, amount:6}
    }
    var precision = {price:0, amount:0}
    var depth = exchange.GetDepth()
    if(!depth){
        throw 'Cannot connect to exchange market, need overseas custodian'
    }
    for(var i=0;i<depth.Asks.length;i++){
        var amountPrecision = depth.Asks[i].Amount.toString().indexOf('.') > -1 ? depth.Asks[i].Amount.toString().split('.')[1].length : 0
        precision.amount = Math.max(precision.amount,amountPrecision)
        var pricePrecision = depth.Asks[i].Price.toString().indexOf('.') > -1 ? depth.Asks[i].Price.toString().split('.')[1].length : 0
        precision.price = Math.max(precision.price,pricePrecision)
    }
    return precision
}
function updateAccount() {
    var acc = exchange.GetAccount()
    if(acc){
        if(account && _N(acc.Stocks + acc.FrozenStocks,6) != _N(account.Stocks + account.FrozenStocks,6)){
            if(acc.Stocks + acc.FrozenStocks > account.Stocks + account.FrozenStocks){
                Log('Buy Order Filled:',_N(acc.Stocks + acc.FrozenStocks-account.Stocks - account.FrozenStocks,6),  '  Quantity changes:', _N(account.Stocks + account.FrozenStocks,6), ' -> ', _N(acc.Stocks + acc.FrozenStocks,6))
            }
            if(acc.Stocks + acc.FrozenStocks < account.Stocks + account.FrozenStocks){
                Log('Sell Order Filled:',_N(account.Stocks + account.FrozenStocks - acc.Stocks - acc.FrozenStocks,6),'  Quantity changes:', _N(account.Stocks + account.FrozenStocks,6), ' -> ', _N(acc.Stocks + acc.FrozenStocks,6))
            }
            total_trade_volume += _N(Math.abs(acc.Stocks + acc.FrozenStocks - (account.Stocks + account.FrozenStocks)),6)
        }
        
        account = acc
    }else{
        Log('Error obtaining account information')
    }
}

function updateTicker(){
    var ticker = exchange.GetTicker()
    if(ticker){
        last = ticker.Last
    }else{
        Log('Error fetching market data')
    }
}

function cancelAll(){
    Log('Cancel all orders')
    var orders = exchange.GetOrders()
    if(!orders){
        Log('Failed to get order')
    }
    for(var j=0; j<orders.length; j++){
        exchange.CancelOrder(orders[j].Id)
        Sleep(10)
    }
}

cancelAll()
last = exchange.GetTicker().Last
updateAccount()

var precision = GetPrecision()


var init_value = 0
var init_account = {balance:0, amount:0}

if(_G('init_value')){
    init_value  = _G('init_value')
    init_account = _G('init_account')
}else{
    init_value = _N(account.Balance+account.FrozenBalance+(account.Stocks+account.FrozenStocks)*last, 6)
    init_account = {balance:account.Balance+account.FrozenBalance, amount:account.Stocks+account.FrozenStocks}
    Log('First time starting strategy, Initial Total Value Is: ', init_value)
    _G('init_value', init_value)
    _G('init_account', init_account)
}


function trade(direction, price, value, msg){
    if(price <= 0){return}
    var amount = _N(value/price, precision.amount)
    var new_order = false 
    if(!order[direction+'_id']){
        new_order = true
    }
    if(order[direction+'_price'] > 0 && Math.abs(price-order[direction+'_price'])/order[direction+'_price'] > Grid_Ratio/10.0){
        new_order = true
    }
    if((direction == 'buy' && account.FrozenBalance == 0 && account.Balance > 1.5*value) || (direction == 'sell' && account.FrozenStocks == 0 && account.Stocks > 1.5*amount)){
        new_order = true
    }
    order[direction+'_price'] = price
    if(new_order){
        if(order[direction+'_id']){
            exchange.CancelOrder(order[direction+'_id'])
            order[direction+'_price'] = 0
            order[direction+'_id'] = 0
        }
        var id =null
        if(direction == 'buy'){
            if(account.Balance < 1.5*value){
                Log('Insufficient funds, Cannot place buy order')
            }else{
                id = exchange.Buy(price, amount, msg)
            }
        }
        if(direction == 'sell'){
            if(account.Stocks < 1.5*amount){
                Log('Insufficient coins remaining, Cannot place sell order')
            }else{
                id = exchange.Sell(price, amount, msg)
            }
        }
        order[direction+'_id'] = id
        order[direction+'_price'] = price
    }
}

function updateStatus(){
    if(Date.now()-update_status_time < 4000){
        return
    }
    update_status_time = Date.now()
    var now_value = (account.Stocks+account.FrozenStocks)*last + account.Balance+account.FrozenBalance
    var profit = _N( now_value - init_account.amount*last - init_account.balance, 6)
    var table = {
                 type: 'table', title: 'Account Information', 
                 cols: ['Initial coin', 'Initial capital', 'Current coin', 'Current capital', 'Current ratio', 'Current price', 'Initial market value', 'Current market value', 'Total transactions', 'Profit'],
                 rows: [[_N(init_account.amount,6), _N(init_account.balance,6), _N(account.Stocks+account.FrozenStocks,6),
                     _N(account.Balance+account.FrozenBalance,6), _N((account.Stocks+account.FrozenStocks)*last/now_value,6), _N(last,6), 
                     _N(init_value,6), _N(now_value,6),_N(total_trade_volume,4), _N(profit,6)]]
                 }
    var logString = _D()+'  Last update time of strategy code6Moon10day 14:00\n'
    LogStatus(logString + '`' + JSON.stringify(table) + '`'+'\n')
    
    var log_profit_intervel = IsVirtual() ? 24*60*60*1000 : Log_profit
    if(Date.now()-log_profit_time > log_profit_intervel){
        LogProfit(_N((account.Stocks+account.FrozenStocks)*last + account.Balance+account.FrozenBalance - init_account.amount*last - init_account.balance, 6))
        log_profit_time = Date.now()
    }
}

function onTick(){
    if(last == 0){return}
    var m = account.Stocks+account.FrozenStocks
    var b = account.Balance+account.FrozenBalance
    var r = m*last/(m*last+b)
    if(Math.abs(r-Ratio)>0.3*Ratio){
        throw 'In order to avoid impacting the market, you need to manually trade to a position close to the position ratio, and then trade by strategy'
    }
    var buy_r = Ratio-Grid_Ratio
    var sell_r = Ratio+Grid_Ratio
    var buy_price = _N(b*buy_r/(m-m*buy_r), precision.price)
    var sell_price = _N(b*sell_r/(m-m*sell_r), precision.price)
    
    var buy_value =  (m*buy_price + b)*Grid_Ratio
    var sell_value = (m*sell_price + b)*Grid_Ratio
    trade('buy', buy_price,  buy_value,    'Buy Balance')
    trade('sell', sell_price, sell_value , 'Sell Balance')
}

function onexit(){
    cancelAll()
}

function main() {
    while(true){
        updateTicker()
        updateAccount()
        onTick()
        updateStatus()
        if(!IsVirtual()){
            Sleep(Intervel)
        }
    }
}
```

> Detail

https://www.fmz.com/strategy/214943

> Last Modified

2020-07-25 20:57:12
