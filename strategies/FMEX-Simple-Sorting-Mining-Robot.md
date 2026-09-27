
> Name

FMEX-Simple-Sorting-Mining-Robot

> Author

小草

> Strategy Description

Refer to the specific article: https://www.fmz.com/digest-topic/5843

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Intervel|2|Dormant Time|
|Amount|10|Order Quantity|
|CoverProfit|-10|Closing Profit|
|ProfitTime|60|Print profit time interval|
|Url|https://api.fmextest.net|APIBase address|


> Source (javascript)

``` javascript
exchange.SetBase(Url)
if(exchange.GetName()!= 'Futures_FMex'){
    throw 'This strategy only supports FMEX perpetual'
}

var account = null
var depth = null 
var pos = {direction:'empty',price:0,amount:0,unrealised_profit:0}

//Official mining coefficients can be set as needed, such as increasing the farther from the order book, the lower the transaction risk
var factors = [1/4, 1/40, 1/40,1/40,1/40,1/50,1/50,1/50,1/50,1/50,1/100,1/100,1/100,1/100,1/100]
var total_efficiency = 0 //Total Efficiency
var avg_efficiency = 0
var avg_num = 0

var ordersInfo = {buy:[],sell:[]}//id:0, price:0, amount:0}
var coverInfo = {buyId:0, buyPrice:0, sellId:0, sellPrice:0}
var depthInfo = []
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

function updateDepth(){
    var data = exchange.GetDepth()
    if(data){
        depth = data
    }else{
        Log('Error fetching depth')
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

function calcDepth(){ 
    depthInfo = [] // price amount efficent  ratio  
    var ask_price = depth.Asks[0].Price
    var bid_price = depth.Bids[0].Price
    total_efficiency = 0
    for(var i=0;i<15;i++){
        var factor = factors[i]
        total_efficiency += 1000000*(Amount*2/(depth.Asks[i].Amount+depth.Bids[i].Amount))*factor*0.5/288
        while(ask_price <= depth.Asks[i].Price){ //Considering unoccupied depth positions
            var my_ask_amount = _.findWhere(ordersInfo.sell, {price:ask_price}) ? _.findWhere(ordersInfo.sell, {price:ask_price}).amount : 0 //Eliminate interference from your own orders
            var ask_amount = ask_price == depth.Asks[i].Price ? Math.max(depth.Asks[i].Amount-my_ask_amount,0) : 0
            depthInfo.push({side:'sell', pos:i+1, price:ask_price, amount:ask_amount, factor:factor, my_amount:0, e:0, r:0})
            ask_price += 0.5
        }
        
    }
    for(var i=0;i<15;i++){
        var factor = factors[i]
        total_efficiency += 1000000*(Amount*2/(depth.Asks[i].Amount+depth.Bids[i].Amount))*factor*0.5/288
        while(bid_price >= depth.Bids[i].Price){
            var my_bid_amount = _.findWhere(ordersInfo.buy, {price:bid_price}) ? _.findWhere(ordersInfo.buy, {price:bid_price}).amount : 0 
            var bid_amount = bid_price == depth.Bids[i].Price ? Math.max(depth.Bids[i].Amount-my_bid_amount,0) : 0
            depthInfo.push({side:'buy', pos:i+1, price:bid_price, amount:bid_amount, factor:factor, my_amount:0, e:0, r:0})
            bid_price -= 0.5
        }
    }
}

function calcAmount(){
    var total_amount = Amount
    var per_amount = _N(Amount/100,0)
    var max_id = 0
    while(total_amount >= per_amount){
        var max_e = 0
        for(var i=0;i<30;i++){
            if(depthInfo[i].amount == 0){
                depthInfo[i].my_amount = per_amount
            }else{
                depthInfo[i].e = depthInfo[i].factor*depthInfo[i].amount/Math.pow(depthInfo[i].my_amount+per_amount+depthInfo[i].amount,2)
                max_id = depthInfo[i].e > max_e ? i : max_id 
                max_e = depthInfo[i].e > max_e ? depthInfo[i].e : max_e
            }
        }
        depthInfo[max_id].my_amount += per_amount     
        total_amount -= per_amount
    }
}

function makeOrders(){
    var e = 0
    var new_orders = {buy:[],sell:[]}
    for(var i=0;i<30;i++){
        if(depthInfo[i].my_amount > 0){
            var find = _.findWhere(ordersInfo[depthInfo[i].side], {price:depthInfo[i].price})
            //Log(find)
            var now_amount = find ? find.amount : 0
            var now_id =  find ? find.id : 0
            if(Math.abs(now_amount  - depthInfo[i].my_amount) > 2.1*Amount/100 || depthInfo[i].amount == 0){ //Need to place the order again
                if(now_id){
                    exchange.CancelOrder(now_id,find)
                    find.id = 0
                }
                if(depthInfo[i].my_amount > 0){
                    exchange.SetDirection(depthInfo[i].side)
                    
                    var id = exchange[depthInfo[i].side == 'buy'  ? 'Buy' :  'Sell'](depthInfo[i].price,depthInfo[i].my_amount)
                    if(id){ 
                        new_orders[depthInfo[i].side].push({price:depthInfo[i].price,amount:depthInfo[i].my_amount,id:id})
                    }
                }
           }else{
               now_id =  find ? find.id : 0
               if(now_id){
                   new_orders[depthInfo[i].side].push(find)
               }
           }
           depthInfo[i].r = 1000000*(depthInfo[i].my_amount/(depthInfo[i].my_amount+depthInfo[i].amount))*depthInfo[i].factor*0.5/288
           e += depthInfo[i].r
        }
    }
    for(var i=0;i<ordersInfo.buy.length;i++){
        if(ordersInfo.buy[i].price < depth.Bids[15].Price && ordersInfo.buy[i].id ){
            exchange.CancelOrder(ordersInfo.buy[i].id,'Retract buy orders outside the scope')
        }
    }
    for(var i=0;i<ordersInfo.sell.length;i++){
        if(ordersInfo.sell[i].price > depth.Asks[15].Price && ordersInfo.sell[i].id){
            exchange.CancelOrder(ordersInfo.sell[i].id,'Sell orders outside the revocation range')
        }
    }
    ordersInfo = new_orders
    var total = avg_efficiency*avg_num + e
    avg_num += 1
    avg_efficiency = total/avg_num
}

function logStatus(){
    if(Date.now()-lastLogStatusTime < 4000){
        return
    }
    lastLogStatusTime = Date.now()
    var leverage = pos.amount/(account.Info.data.BTC[0]*(depth.Asks[0].Price+depth.Bids[0].Price)/2)
    var table1 = {type: 'table', title: 'Account Information', 
             cols: ['Available Margin', 'Frozen Margin', 'Position Margin', 'Position Direction', 'Number of Positions', 'Position Price', 'Unrealized Profit and Loss', 'Used Leverage', 'Initial Fund', 'Profit', 'Close Bid Price', 'Sell Price', 'Average Efficiency', 'My Efficiency'],
             rows: [[_N(account.Info.data.BTC[0], 6),_N(account.Info.data.BTC[1], 6),_N(account.Info.data.BTC[2], 6),
                     pos.direction,pos.amount,_N(pos.price,2),_N(pos.unrealised_profit,5),_N(leverage,2),
                     _N(init_value,6),_N(account.Info.data.BTC[0]-init_value, 6), coverInfo.buyPrice, coverInfo.sellPrice,
                     _N(total_efficiency/30,2),_N(avg_efficiency,2)
                    ]]
                 }
    var table2 = {type: 'table', title: 'Order Information', cols: ['Position', 'Buy Price', 'Buy Volume','Mine', 'Efficiency', 'Sell Price', 'Sell Volume', 'Mine', 'Efficiency'], rows: []}
    
    for(var i=0;i<15;i++){                          
        table2.rows.push([i+1,depthInfo[i+15].price,depthInfo[i+15].amount,depthInfo[i+15].my_amount,_N(depthInfo[i+15].r,3),
                          depthInfo[i].price,depthInfo[i].amount,depthInfo[i].my_amount,_N(depthInfo[i].r,3)])
    }
    if(_D().slice(8,11) != today){
        today = _D().slice(8,11)
        Log('The total amount unlocked yesterday was one millionth',total_back,'.Recalculate today')
        total_back = 0
    }
    var nowPeriod = _N(_D().slice(14,16)/5,0)
    if(lastPeriod != nowPeriod){
        lastPeriod = nowPeriod 
        total_back += avg_efficiency
        avg_efficiency = 0
        avg_num = 0
        
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
        ordersInfo = {buy:[],sell:[]}
        coverInfo = {buyId:0, buyPrice:0, sellId:0, sellPrice:0} 
    }
}


function coverPosition(){
    if(pos.amount>0){
        if(pos.direction == 'long'){ //Close Long Position
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
    calcDepth()
    calcAmount()
    makeOrders()
    if(Date.now()-lastRestTime > 3*60*1000){
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
        updateDepth()
        onTick()
        coverPosition()
        logStatus()
        Sleep(Intervel*1000)
    }
}
```

> Detail

https://www.fmz.com/strategy/171042

> Last Modified

2020-09-25 15:34:00
