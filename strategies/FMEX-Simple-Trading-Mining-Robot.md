
> Name

FMEX-Simple-Trading-Mining-Robot

> Author

小草

> Strategy Description

Refer to the specific article: https://www.fmz.com/digest-topic/5834

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|MaxAmount|1000|Maximum Order Quantity|
|ProfitTime|60|Print profit time interval|
|Fee|0.05|Taker Fee%|
|PeriodTradeBack|0.0001|BTC quantity unlocked per minute for trading|
|CoverCost|0.25|Default closing loss on trade|
|Intervel|2|Dormant Time|
|Url|https://api.testnet.fmex.com|APIBase address|


> Source (javascript)

``` javascript
exchange.SetBase(Url)
if(exchange.GetName()!= 'Futures_FMex'){
    throw 'This strategy only supports FMEX perpetual'
}

var account = null
var records = null 
var pos = {direction:'empty',price:0,amount:0,unrealised_profit:0}


var total_efficiency = 0 //Total Efficiency
var my_efficiency = 0

var ordersInfo = {buyId:0, buyPrice:0, sellId:0, sellPrice:0}
var coverInfo = {buyId:0, buyPrice:0, sellId:0, sellPrice:0}
var depthInfo = {asks:[], bids:[]}
var lastProfitTime = 0 //Control printing profit time
var lastRestTime = Date.now()   //Timed reset strategy
var lastLogStatusTime = 0
var lastPeriod = 0
var today = _D().slice(8,11)

updateAccount()

var total_back = 0
if(_G('total_back')){
    total_back = _G('total_back')
}else{
    _G('total_back',total_back)
}
var init_value = 0
if(_G('init_value')){
    init_value  = _G('init_value')
}else{
    init_value = _N(account.Info.data.BTC[0]+account.Info.data.BTC[1]+account.Info.data.BTC[2], 6)
    Log('First time starting strategy, Initial Total Value Is: ', init_value)
    _G('init_value', init_value)
}

function updateRecords(){
    var data = exchange.GetRecords(60)
    if(data){
        records = data
    }else{
        Log('Error fetching market data')
    }
}

function updateAccount(){
    var data = exchange.GetAccount()
    if(data){
        account = data
    }else{
        Log('Error fetching account data')
    }
}

function updatePosition(){
    var data = exchange.GetPosition()
    if(data){
        if(data.length > 0){
            if(data[0].Info.direction !=  pos.direction || data[0].Info.quantity != pos.amount){
                Log('Position Change:', pos.direction + ' ' +  pos.amount + ' -> ' + data[0].Info.direction + ' ' + data[0].Info.quantity)
            }
            pos = {direction:data[0].Info.direction, price:data[0].Info.entry_price, amount:data[0].Info.quantity, unrealised_profit:data[0].Info.unrealized_pnl}
        }else{
            if(pos.amount){
                Log('Position Change:', pos.direction + ' ' +  pos.amount + ' -> ' + 'empty')
            }
            pos = {direction:'empty',price:0,amount:0,unrealised_profit:0}
        }
    }else{
        Log('Error fetching positions')
    }
}

function calcEfficiency(){
    total_efficiency = 0
    for(var i=0;i<records.length;i++){
        total_efficiency += 1000000*(Amount/(records[i].Volume+Amount))*0.3*0.5/2880
    }
    if(_D().slice(17) > 57){
        my_efficiency = 1000000*(Amount/(records[records.length-1].Volume+Amount))*0.3*0.5/2880
    }
}


function logStatus(){
    if(Date.now()-lastLogStatusTime < 4000){
        return
    }
    lastLogStatusTime = Date.now()
    var leverage = pos.amount/(account.Info.data.BTC[0]*(depth.Asks[0].Price+depth.Bids[0].Price)/2)
    var table1 = {type: 'table', title: 'Account Information', 
             cols: ['Available Margin', 'Frozen Margin', 'Position Margin', 'Position Direction', 'Number of Positions', 'Position Price', 'Unrealized Profit and Loss', 'Used Leverage', 'Initial Capital', 'Profit', 'Bid Price', 'Selling Price', 'Average Efficiency', 'My Efficiency'],
             rows: [[_N(account.Info.data.BTC[0], 6),_N(account.Info.data.BTC[1], 6),_N(account.Info.data.BTC[2], 6),
                     pos.direction,pos.amount,_N(pos.price,2),_N(pos.unrealised_profit,5),_N(leverage,2),
                     _N(init_value,6),_N(account.Info.data.BTC[0]-init_value, 6), ordersInfo.buyPrice, ordersInfo.sellPrice,
                     _N(total_efficiency/records.length,2),_N(my_efficiency,2)
                    ]]
                 }
    var table2 = {type: 'table', title: 'Order Information', cols: ['Position', 'Buy Price', 'Buy Volume', 'Efficiency', 'Sell Price', 'Sell Volume', 'Efficiency'], rows: []}
    for(var i=0;i<15;i++){
        //Log(i+1,depthInfo.bids[i][1],depthInfo.bids[i][2],depthInfo.bids[i][3],depthInfo.asks[i][1],depthInfo.asks[i][2],depthInfo.asks[i][3])
        table2.rows.push([i+1,depthInfo.bids[i][1],depthInfo.bids[i][2],depthInfo.bids[i][3],depthInfo.asks[i][1],depthInfo.asks[i][2],depthInfo.asks[i][3]])
    }
    if(_D().slice(8,11) != today){
        today = _D().slice(8,11)
        Log('The total amount unlocked yesterday was one millionth',total_back,'.Recalculate today')
        total_back = 0
        
    }
    var logString = 'Current mining cycle:'+_D().slice(11,14) + nowPeriod*5 + ' - ' + _D().slice(11,14) + (nowPeriod*5+5) + ' '+'Sorted mining has obtained one millionth of the total amount unlocked on the day'+ _N(total_back,4) +'\n'
    LogStatus(logString + '`' + JSON.stringify(table1) + '`'+'\n'+'`' + JSON.stringify(table2) + '`')
    if(Date.now()-lastProfitTime > ProfitTime*1000){
        updateAccount()
        lastProfitTime = Date.now()
        LogProfit(_N(account.Info.data.BTC[0]+account.Info.data.BTC[1]+account.Info.data.BTC[2],6))
    }
}

function cancelAll(){ //Reset the strategy to prevent some orders from getting stuck, which may affect other running strategies
    var orders = exchange.GetOrders()
    if(orders){
        for(var i=0;i<orders.length;i++){
            exchange.CancelOrder(orders[i].Id)
        }
        ordersInfo = {buyId:0, buyPrice:0, sellId:0, sellPrice:0}
    }
}


function coverPosition(){
    if(pos.amount>0){
        if(pos.direction == 'long'){ //To close a long position, if you use the order to take the order, you will lose the handling fee. You can change it to the order to place the order, which will increase the risk of holding the position.
            var sellPrice = _N(pos.price,0)+_N(CoverProfit,0)
            if(sellPrice != coverInfo.sellPrice){
                if(coverInfo.sellId){
                    exchange.CancelOrder(coverInfo.sellId)
                    coverInfo.sellId = 0
                }
                exchange.SetDirection('sell')
                var sellId = exchange.Sell(sellPrice, pos.amount, 'Close Long Position')
                coverInfo.sellPrice = sellPrice
                if(sellId){
                     coverInfo.sellId = sellId
                }else{
                     coverInfo.sellId = 0
                }
            }        
        }else{
            var buyPrice = _N(pos.price,0)-_N(CoverProfit,0)
            if(buyPrice != coverInfo.buyPrice){
                if(coverInfo.buyId){
                    exchange.CancelOrder(coverInfo.buyId)
                    coverInfo.buyId = 0
                }
                exchange.SetDirection('buy')
                var buyId = exchange.Buy(buyPrice, pos.amount, 'Close Short Position')
                coverInfo.buyPrice = buyPrice
                if(buyId){
                     coverInfo.buyId = buyId
                }else{
                    coverInfo.buyId = 0
                }
            }
        }
    }
}

function onTick(){
        var price = calcDepth(depth)
        var sellPrice = price[0]
        var buyPrice = price[2]
        if(buyPrice != ordersInfo.buyPrice){
            if(ordersInfo.buyId){
                exchange.CancelOrder(ordersInfo.buyId)
                ordersInfo.buyId = 0
            }
            exchange.SetDirection('buy')
            var buyId = exchange.Buy(buyPrice, Amount, _N(price[1],3))
            ordersInfo.buyPrice = buyPrice
            if(buyId){
                ordersInfo.buyId = buyId
            }else{
                ordersInfo.buyId = 0
            }
            
        }
        if(sellPrice != ordersInfo.sellPrice){
            if(ordersInfo.sellId){
                exchange.CancelOrder(ordersInfo.sellId)
                ordersInfo.sellId = 0
            }
            exchange.SetDirection('sell')
            var sellId = exchange.Sell(sellPrice, Amount, _N(price[3],3))
            ordersInfo.sellPrice = sellPrice
            if(sellId){
                ordersInfo.sellId = sellId
            }else{
                ordersInfo.sellId = 0
            }
        }

        if(Date.now()-lastRestTime > 10*60*1000){
            lastRestTime = Date.now()
            cancelAll()
        }
}


function onexit(){  //Cancel orders after exit
    cancelAll()
    _G('total_back',total_back)
}


exchange.SetContractType('swap')
exchange.SetMarginLevel(0)



function main() {
    cancelAll()
    while(true){
        updatePosition()
        updateRecords()
        onTick()
        logStatus()
        Sleep(Intervel*1000)
    }
}
```

> Detail

https://www.fmz.com/strategy/171560

> Last Modified

2020-09-25 15:34:15
