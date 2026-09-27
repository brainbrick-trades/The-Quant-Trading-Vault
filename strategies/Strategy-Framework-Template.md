
> Name

Strategy-Framework-Template

> Author

发明者量化-小小梦

> Strategy Description

New strategy framework
Spot trading, open long, open short, stop loss, add position, close position.
// - Status
/*
var TASK_IDLE = 0;
var TASK_OPEN_LONG = 1;
var TASK_OPEN_SHORT = 2;
var TASK_ADD = 3;
var TASK_ST = 4;
var TASK_COVER = 5;
*/

Instructions for use:
https://www.fmz.com/bbs-topic/634

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|OpMode|0|Order type: market order | pending order|
|MaxSpace|0.5|Pending order expiration distance|
|SlidePrice|0.1|Order Slippage Price (Yuan))|
|MaxAmount|0.8|Maximum single order volume for opening a position|
|RetryDelay|500|Retry on failure (milliseconds))|
|Interval|500|Polling Interval|
|_minStock|0.01|Minimum trading coin quantity|


> Source (javascript)

``` javascript
// Template global variables
// - Status
var TASK_IDLE = 0;
var TASK_OPEN_LONG = 1;
var TASK_OPEN_SHORT = 2;
var TASK_ADD = 3;
var TASK_ST = 4;
var TASK_COVER = 5;
// - Variables
var Tasks = [];
var IDLE = 11;
var LONG = 22;
var SHORT = 33;
var cmdList = [TASK_IDLE, TASK_OPEN_LONG, TASK_OPEN_SHORT, TASK_ADD, TASK_ST, TASK_COVER];
// Calculate profit and loss
var SumProfit = 0;

// Spot trading function
function CancelPendingOrders(e, orderType) {
    while (true) {
        var orders = e.GetOrders();
        if (!orders) {
            Sleep(RetryDelay);
            continue;
        }
        var processed = 0;
        for (var j = 0; j < orders.length; j++) {
            if (typeof(orderType) === 'number' && orders[j].Type !== orderType) {
                continue;
            }
            e.CancelOrder(orders[j].Id, orders[j]);
            processed++;
            if (j < (orders.length - 1)) {
                Sleep(RetryDelay);
            }
        }
        if (processed === 0) {
            break;
        }
    }
}

function GetAccount(e, waitFrozen) {
    if (typeof(waitFrozen) == 'undefined') {
        waitFrozen = false;
    }
    var account = null;
    var alreadyAlert = false;
    while (true) {
        account = _C(e.GetAccount);
        if (!waitFrozen || (account.FrozenStocks < _minStock && account.FrozenBalance < 0.01)) {
            break;
        }
        if (!alreadyAlert) {
            alreadyAlert = true;
            Log("Found frozen funds or coins in the account", account);
        }
        Sleep(RetryDelay);
    }
    return account;
}

function StripOrders(e, orderId) {
    var order = null;
    if (typeof(orderId) == 'undefined') {
        orderId = null;
    }
    while (true) {
        var dropped = 0;
        var orders = _C(e.GetOrders);
        for (var i = 0; i < orders.length; i++) {
            if (orders[i].Id == orderId) {
                order = orders[i];
            } else {
                var extra = "";
                if (orders[i].DealAmount > 0) {
                    extra = "Transaction: " + orders[i].DealAmount;
                } else {
                    extra = "unfilled";
                }
                e.CancelOrder(orders[i].Id, orders[i].Type == ORDER_TYPE_BUY ? "Buy Order" : "Sell Order", extra);
                dropped++;
            }
        }
        if (dropped === 0) {
            break;
        }
        Sleep(RetryDelay);
    }
    return order;
}

function Trade(e, tradeType, tradeAmount, mode, slidePrice, maxAmount, maxSpace, retryDelay) {
    var initAccount = GetAccount(e, true);
    var nowAccount = initAccount;
    var orderId = null;
    var prePrice = 0;
    var dealAmount = 0;
    var diffMoney = 0;
    var isFirst = true;
    var tradeFunc = tradeType == ORDER_TYPE_BUY ? e.Buy : e.Sell;
    var isBuy = tradeType == ORDER_TYPE_BUY;
    while (true) {
        var ticker = _C(e.GetTicker);
        var tradePrice = 0;
        if (isBuy) {
            tradePrice = _N((mode === 0 ? ticker.Sell : ticker.Buy) + slidePrice, 4);
        } else {
            tradePrice = _N((mode === 0 ? ticker.Buy : ticker.Sell) - slidePrice, 4);
        }
        if (!orderId) {
            if (isFirst) {
                isFirst = false;
            } else {
                nowAccount = GetAccount(e, true);
            }
            var doAmount = 0;
            if (isBuy) {
                diffMoney = _N(initAccount.Balance - nowAccount.Balance, 4);
                dealAmount = _N(nowAccount.Stocks - initAccount.Stocks, 4);
                doAmount = Math.min(maxAmount, tradeAmount - dealAmount, _N((nowAccount.Balance - 10) / tradePrice, 4));
            } else {
                diffMoney = _N(nowAccount.Balance - initAccount.Balance, 4);
                dealAmount = _N(initAccount.Stocks - nowAccount.Stocks, 4);
                doAmount = Math.min(maxAmount, tradeAmount - dealAmount, nowAccount.Stocks);
            }
            if (doAmount < _minStock) {
                break;
            }
            prePrice = tradePrice;
            orderId = tradeFunc(tradePrice, doAmount, ticker);
            if (!orderId) {
                CancelPendingOrders(e, tradeType);
            }
        } else {
            if (mode === 0 || (Math.abs(tradePrice - prePrice) > maxSpace)) {
                orderId = null;
            }
            var order = StripOrders(e, orderId);
            if (!order) {
                orderId = null;
            }
        }
        Sleep(retryDelay);
    }

    if (dealAmount <= 0) {
        return null;
    }

    return {
        price: _N(diffMoney / dealAmount, 4),
        amount: dealAmount
    };
}

var BuySpot = function(e, amount) {
    if (typeof(e) === 'number') {
        amount = e;
        e = exchange;
    }
    return Trade(e, ORDER_TYPE_BUY, amount, OpMode, SlidePrice, MaxAmount, MaxSpace, RetryDelay);
};

var SellSpot = function(e, amount) {
    if (typeof(e) === 'number') {
        amount = e;
        e = exchange;
    }
    return Trade(e, ORDER_TYPE_SELL, amount, OpMode, SlidePrice, MaxAmount, MaxSpace, RetryDelay);
};

// Function inside the template
// - Initialization function tasksInit
function TasksInit(tasks){
    _.each(tasks, function(task){ // OpenLongAmount OpenShortAmount AddAmount StopLossAmount STATE minStock initAccount Currency Name Label nowAccount lastAccount lastTASKSTATE Profit floatProfit lastPrice preProfit NowPositionInfo
        task.OpenLongAmount = 0;
        task.OpenShortAmount = 0;
        task.AddAmount = 0;
        task.StopLossAmount = 0;
        task.STATE = IDLE;
        task.minStock = _minStock; // _C(task.Exchange.GetMinStock);     Modify, the GetMinStock function has been deprecated
        task.initAccount = _C(task.Exchange.GetAccount);
        task.Currency = _C(task.Exchange.GetCurrency);
        task.Name = _C(task.Exchange.GetName);
        task.Label = _C(task.Exchange.GetLabel);
        task.nowAccount = task.initAccount;
        task.lastAccount = task.initAccount;
        task.lastTASKSTATE = TASK_IDLE;
        task.Profit = 0;
        task.floatProfit = 0;
        task.lastPrice = 0;
        task.preProfit = 0;
        task.CMD = TASK_IDLE;
        task.CMD_AMOUNT = 0;
        task.NowPositionInfo = {
            avgPrice: 0,        // Average position price
            amount: 0 ,         // Position
            floatProfit: 0      // Floating profit and loss
        };
        Log(task.Name, task.Label, "Initial account information:", task.initAccount);
    });
}

function TranslateSTATE_TASKSTATE(STATE){
    switch(STATE){
        case 0: //TASK_IDLE
            return "No task";
        case 1: //TASK_OPEN_LONG
            return "Create long position task";
        case 2: //TASK_OPEN_SHORT
            return "Create short position task";
        case 3: //TASK_ADD
            return "Add position task";
        case 4: //TASK_ST
            return "Stop-loss task";
        case 5: //TASK_COVER
            return "Close position task";
        case 11: //IDLE
            return "Position not opened";
        case 22: //LONG
            return "Hold long position";
        case 33: //SHORT
            return "Hold short position";
    }
}

// - Open long position
function OpenLong(task){
    var BuyInfo = BuySpot(task.Exchange, task.OpenLongAmount);
    if(!BuyInfo){
        //Log("function BuySpot return :", BuyInfo);
    }else{
        task.NowPositionInfo.amount = BuyInfo.amount;
        task.NowPositionInfo.avgPrice = BuyInfo.price;
        task.STATE = LONG;
        task.nowAccount = _C(task.Exchange.GetAccount); // update nowAccount
    }
    return BuyInfo;
}

// - Open short position
function OpenShort(task){
    var SellInfo = SellSpot(task.Exchange, task.OpenShortAmount);
    if(!SellInfo){
        //Log("function SellSpot return :", SellInfo);
    }else{
        task.NowPositionInfo.amount = SellInfo.amount;
        task.NowPositionInfo.avgPrice = SellInfo.price;
        task.STATE = SHORT;
        task.nowAccount = _C(task.Exchange.GetAccount); // update nowAccount
    }
    return SellInfo;
}
// - add to position
function AddPosition(task){
    var tradeInfo = null;
    if(task.STATE === LONG){
        tradeInfo = BuySpot(task.Exchange, task.AddAmount);
    }else if(task.STATE === SHORT){
        tradeInfo = SellSpot(task.Exchange, task.AddAmount);
    }
    if(!tradeInfo){
        //Log("function return :", tradeInfo);
    }else{
        task.NowPositionInfo.avgPrice = (tradeInfo.price * tradeInfo.amount + task.NowPositionInfo.avgPrice * task.NowPositionInfo.amount) / (tradeInfo.amount + task.NowPositionInfo.amount);
        task.NowPositionInfo.amount += tradeInfo.amount;
        task.nowAccount = _C(task.Exchange.GetAccount); // update nowAccount
    }
    return tradeInfo;
}
// - stop loss
function StopLoss(task){
    var tradeInfo = null;
    task.StopLossAmount = Math.min(task.StopLossAmount, task.NowPositionInfo.amount);
    if(task.STATE === LONG){
        tradeInfo = SellSpot(task.Exchange, task.StopLossAmount);
    }else if(task.STATE === SHORT){
        tradeInfo = BuySpot(task.Exchange, task.StopLossAmount);
    }
    if(!tradeInfo){
        //Log("function return :", tradeInfo);
    }else if(Math.abs(task.NowPositionInfo.amount - tradeInfo.amount) > task.minStock){
        task.NowPositionInfo.amount -= tradeInfo.amount;
        Log("Not fully closed, remaining:", Math.abs(task.NowPositionInfo.amount - tradeInfo.amount), " tradeInfo:", tradeInfo, "NowPositionInfo:", task.NowPositionInfo);
        task.nowAccount = _C(task.Exchange.GetAccount); // update nowAccount
    }else{
        task.NowPositionInfo.amount = 0;
        task.NowPositionInfo.avgPrice = 0;
        task.STATE = IDLE;
        CalProfit(task); // equal Cover
    }
    return tradeInfo;
}
// - Close Position
function Cover(task){
    var tradeInfo = null;
    if(task.STATE === LONG){
        tradeInfo = SellSpot(task.Exchange, task.NowPositionInfo.amount);
    }else if(task.STATE === SHORT){
        tradeInfo = BuySpot(task.Exchange, task.NowPositionInfo.amount);
    }
    if(!tradeInfo){
        //Log("function return :", tradeInfo);
    }else if(Math.abs(task.NowPositionInfo.amount - tradeInfo.amount) > task.minStock){
        task.NowPositionInfo.amount -= tradeInfo.amount;
        Log("Not fully closed, remaining:", Math.abs(task.NowPositionInfo.amount - tradeInfo.amount), " tradeInfo:", tradeInfo, "NowPositionInfo:", task.NowPositionInfo);
    }else{
        task.NowPositionInfo.amount = 0;
        task.NowPositionInfo.avgPrice = 0;
        task.STATE = IDLE;
        CalProfit(task);
    }
    return tradeInfo;
}

function CalProfit(task){
    //task.lastAccount = task.nowAccount;
    task.nowAccount = _C(task.Exchange.GetAccount);
    task.lastAccount = task.nowAccount;
    var Bdiff = task.nowAccount.Balance - task.initAccount.Balance;
    task.preProfit = task.Profit;
    task.Profit = Bdiff;

    SumProfit = 0;
    _.each(Tasks, function(task){
        SumProfit += task.Profit;
    });
    LogProfit(SumProfit, task.Name + "-" + task.Currency + "-" + task.Label + "- this time:" + (task.Profit - task.preProfit), "Money:" + _N(task.nowAccount.Balance, 2), "Currency:" + _N(task.nowAccount.Stocks, 2), "Frozen funds:" + _N(task.nowAccount.FrozenBalance, 2), "Frozen coins:" + _N(task.nowAccount.FrozenStocks, 2)); 
}

function CalFloatProfit(task){
    var diffPrice = 0;
    if(task.STATE === LONG){
        diffPrice = (task.lastPrice - task.NowPositionInfo.avgPrice);
        task.NowPositionInfo.floatProfit = _N(diffPrice * task.NowPositionInfo.amount);
    }else if(task.STATE === SHORT){
        diffPrice = (task.NowPositionInfo.avgPrice - task.lastPrice);
        task.NowPositionInfo.floatProfit = _N(diffPrice * task.NowPositionInfo.amount);
    }
}

function isInCMD_List(cmd){
    for(var i = 0; i < cmdList.length ; i++){
        if(cmd === cmdList[i]){
            return true;
        }
    }
    return false;
}

function CMD(index, CMD_STR, amount){
    if(index < Tasks.length || typeof(amount) === 'undefined' || isInCMD_List(CMD_STR) === false){
        Tasks[index].CMD = CMD_STR;
        Tasks[index].CMD_AMOUNT = amount;
    }else{
        Log("Error:", "index:" + index, "CMD_STR:" + CMD_STR, "amount:" + amount);
    }
}

$.TaskCmd = function(cmd, amount, lastPrice){
    if(cmd === TASK_IDLE && typeof(amount) === 'undefined'){
        amount = 0;
    }else if((cmd === TASK_ST || cmd === TASK_COVER) && typeof(amount) === 'undefined'){
        amount = 0;
    }else if(typeof(amount) === 'undefined'){
        throw "No order quantity to be operated has been passed!";
    }
    if(typeof(lastPrice) === 'undefined'){
        return {cmd: cmd, amount: amount, lastPrice: -1};
    }else{
        return {cmd: cmd, amount: amount, lastPrice: lastPrice};
    }
}

$.GetTaskState = function(Name, Label){
    var ret = null;
    _.each(Tasks, function(task){
       if(task.Name == Name && task.Label == Label){
           ret = task.STATE;
       } 
    });
    return ret;
}

// Template export function
var usedTime = 0;
$.Trend = function() {
    TasksInit(Tasks);
    while(true){
        var beginTime = new Date().getTime();
        _.each(Tasks, function(task){
            task.OpenLongAmount = 0;
            task.OpenShortAmount = 0;
            task.AddAmount = 0;
            task.StopLossAmount = 0;
        });
        _.each(Tasks, function(task){
            var obj = task.onTick();
            //Log("obj:", obj);
            var ret = obj.cmd;
            var amount = obj.amount;
            var tradeRet = null;
            if(obj.lastPrice !== -1){
                task.lastPrice = obj.lastPrice;
            }else{
                task.lastPrice = (_C(task.Exchange.GetTicker)).Last;
            }
            if(task.CMD !== TASK_IDLE){
                ret = task.CMD;
                amount = task.CMD_AMOUNT;
            }
            switch (ret) {
                // switch status..
                case TASK_OPEN_LONG:    // Open long position
                    if(task.STATE === IDLE){
                        task.lastTASKSTATE = TASK_OPEN_LONG;
                        task.OpenLongAmount = amount;
                        tradeRet = OpenLong(task);
                        Log("Long position opened, this trade information:", tradeRet, "#FF0000");
                    }else{
                        //Log("TASK_OPEN_LONG Current status is:", task.STATE, "!= ", IDLE);
                    }
                    break;
                case TASK_OPEN_SHORT:   // Open short position
                    if(task.STATE === IDLE){
                        task.lastTASKSTATE = TASK_OPEN_SHORT;
                        task.OpenShortAmount = amount;
                        tradeRet = OpenShort(task);
                        Log("Short position opened, this trade information:", tradeRet, "#FF0000");
                    }else{
                        //Log("TASK_OPEN_SHORT Current status is:", task.STATE, "!= ", IDLE);   
                    }
                    break;
                case TASK_ADD:          // add to position
                    if(task.STATE === LONG || task.STATE === SHORT){
                        task.lastTASKSTATE = TASK_ADD;
                        task.AddAmount = amount;
                        tradeRet = AddPosition(task);
                        Log("Position added, this trade information:", tradeRet, "#FF0000");
                    }else{
                        //Log("TASK_ADD Current status is:", task.STATE, "!=", LONG, "or", SHORT);
                    }
                    break;
                case TASK_ST:           // stop loss
                    if(task.STATE === LONG || task.STATE === SHORT){
                        task.lastTASKSTATE = TASK_ST;
                        task.StopLossAmount = amount;
                        tradeRet = StopLoss(task);
                        Log("Stop loss completed, this trade information:", tradeRet, "#FF0000");
                    }else{
                        //Log("TASK_ST Current status is:", task.STATE, "!=", LONG, "or", SHORT);
                    }
                    break;
                case TASK_COVER:        // Close Position
                    if(task.STATE === LONG || task.STATE === SHORT){
                        task.lastTASKSTATE = TASK_COVER;
                        tradeRet = Cover(task);
                        Log("Position closed, this trade information:", tradeRet, "#FF0000");
                    }else{
                        //Log("TASK_COVER Current status is:", task.STATE, "!= ", LONG, "or", SHORT);
                    }
                    break;
            }
            // Calculate floating profit
            CalFloatProfit(task);

            // ResetCMD
            if(task.CMD !== TASK_IDLE){
                task.CMD = TASK_IDLE;
                task.CMD_AMOUNT = 0;
            }
        });

        // Interaction module
        var cmd = GetCommand(); // CallAPI  Get messages from interface interaction controls. 
        if (cmd) { // Check if there is a message
            var js = cmd.split(':', 2)[1]; // Split the returned message string, limit the return2Items, take the index1Assign the element of to the namejs Variable of 
            Log("Execute code:", js); // Output executed code
            try { // Exception detection
                eval(js); // Execute eval function; this function executes the passed parameter (code)).
            } catch (e) { // Throw exception
                Log("Interactive code error: Exception", e); // Output error message
            }
        }

        // Display in status bar
        var endTime = new Date().getTime();
        usedTime = endTime - beginTime;
        $.ToTable();
        Sleep(Interval);
    }
}

$.Relation_Exchange_onTick = function(Exchange, onTick){
    var task = {
        onTick : onTick, 
        Exchange : Exchange
    };
    Tasks.push(task);
};

$.ToTable = function(){
    var tables = [];
    _.each(Tasks, function(task){
        var table = {type: "table", title: task.Exchange.GetName() + task.Exchange.GetLabel(), cols: ["desc", "value"], rows: []};
        table.rows.push(["Initial account information:", task.initAccount]);
        table.rows.push(["Current account information:", task.nowAccount]);
        table.rows.push(["Account information after the last closing:", task.lastAccount]);
        table.rows.push(["Position information:", task.NowPositionInfo]);
        table.rows.push(["Status:", TranslateSTATE_TASKSTATE(task.STATE)]);
        table.rows.push(["Recent tasks:", TranslateSTATE_TASKSTATE(task.lastTASKSTATE)]);
        table.rows.push(["Floating profit and loss:", task.floatProfit = task.NowPositionInfo.floatProfit]);
        table.rows.push(["total profit and loss:", task.Profit]);
        // Handle custom
        for(var key in task){
            if(key === 'OpenLongAmount' || key === 'OpenShortAmount' || key === 'AddAmount' || key === 'StopLossAmount' || key === 'STATE' || key === 'minStock' || key === 'initAccount' || key === 'Currency' ||
                key === 'Name' || key === 'Label' || key === 'nowAccount' || key === 'lastAccount' || key === 'lastTASKSTATE' || key === 'Profit' || key === 'floatProfit' || key === 'lastPrice' || key === 'preProfit' || key === 'NowPositionInfo' ||
                    key === 'onTick' || key === 'Exchange' || key === 'CMD' || key === 'CMD_AMOUNT'){
                continue;
            }else{
                table.rows.push([key, task[key]]);
            }
        }

        tables.push(table);
    });
    var CMD_STR = "TASK_OPEN_LONG : Open long position, TASK_OPEN_SHORT : Open short position, TASK_ADD : add to position, TASK_ST : stop loss, TASK_COVER : Close position, command function:CMD(index, CMD_STR, amount)";
    LogStatus(" time: " + _D() + " time-consuming:" + usedTime + "Total income:" + SumProfit + "Command:" + '\n' + CMD_STR + '\n`' + JSON.stringify(tables) + '`');
};

$.AddData = function(index, dataKey, dataValue){
    Tasks[index][dataKey] = dataValue;
};

// The following is the test code 
/*- Status needs to be declared in the main policy when using the template
var TASK_IDLE = 0;
var TASK_OPEN_LONG = 1;
var TASK_OPEN_SHORT = 2;
var TASK_ADD = 3;
var TASK_ST = 4;
var TASK_COVER = 5;
*/

function onTick1() {
    // EMA 
    var records = _C(exchanges[0].GetRecords);
    if(records.length < 11){
        return $.TaskCmd(TASK_IDLE);
    }
    var ema_fast = TA.MA(records, 7);
    var ema_slow = TA.MA(records, 20);
    // $.AddData = function(index, dataKey, dataValue)
    
    var data = "fast[-2]:" + ema_fast[ema_fast.length - 2] + " slow[-2]" + ema_slow[ema_slow.length - 2] + " fast[-1]:" + ema_fast[ema_fast.length - 1] + " slow[-1]:" + ema_slow[ema_slow.length - 1];
    $.AddData(0, "MA", data);
    
    if (ema_fast[ema_fast.length - 1] < ema_slow[ema_slow.length - 1] && ema_fast[ema_fast.length - 2] > ema_slow[ema_slow.length - 2]) {
        return $.TaskCmd(TASK_COVER);
    }else if(ema_fast[ema_fast.length - 1] > ema_slow[ema_slow.length - 1] && ema_fast[ema_fast.length - 2] < ema_slow[ema_slow.length - 2]){
        return $.TaskCmd(TASK_OPEN_LONG, 0.5);
    }

    return $.TaskCmd(TASK_IDLE);
}

function onTick2() {
    // MACD
    var records = _C(exchanges[1].GetRecords);
    if(records.length < 15){
        $.TaskCmd(TASK_IDLE);
    }
    var macd = TA.MACD(records);
    var dif = macd[0];
    var dea = macd[1];
    
    var data = "dif[-2]:" + dif[dif.length - 2] + " dea[-2]" + dea[dea.length - 2] + " dif[-1]:" + dif[dif.length - 1] + " dea[-1]:" + dea[dea.length - 1];
    $.AddData(1, "MACD", data);
    
    if (dif[dif.length - 1] > dea[dea.length - 1] && dif[dif.length - 2] < dea[dea.length - 2]) {
        //return $.TaskCmd(TASK_OPEN_SHORT, 0.8);
        return $.TaskCmd(TASK_COVER);
    }else if(dif[dif.length - 1] < dea[dea.length - 1] && dif[dif.length - 2] > dea[dea.length - 2]){
        //return $.TaskCmd(TASK_COVER);
        return $.TaskCmd(TASK_OPEN_LONG, 0.8);
    }

    return $.TaskCmd(TASK_IDLE);
}

function main() {
    if(exchanges.length != 2){
        throw "The test strategy logic function has two onTick1 and onTick2, and two exchange objects need to be added to run it.!"
    }
    $.Relation_Exchange_onTick(exchanges[0], onTick1);
    $.Relation_Exchange_onTick(exchanges[1], onTick2);
    $.Trend();  // No need to pass parameters.
}
```

> Detail

https://www.fmz.com/strategy/30861

> Last Modified

2018-05-30 18:28:23
