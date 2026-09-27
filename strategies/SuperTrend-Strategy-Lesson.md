
> Name

SuperTrend-Strategy-Lesson

> Author

发明者量化-小小梦

> Strategy Description

Related articles:https://www.fmz.com/bbs-topic/5438

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Amount|true|Single opening position volume|
|TradeInterval|2000|Trading API access polling interval|
|PriceTick|0.5|Tick price of the contract|
|Symbol|quarter|Contract Code|
|pd|45|SuperTrend Parameterspd|
|factor|3|SuperTrend Parametersfactor|


> Source (javascript)

``` javascript
/*backtest
start: 2019-08-01 00:00:00
end: 2020-03-11 00:00:00
period: 15m
basePeriod: 5m
exchanges: [{"eid":"Futures_OKCoin","currency":"BTC_USD"}]
*/

// Global Variables
var OpenAmount = 0                                                  // Quantity held after opening a position
var KeepAmount = 0                                                  // Reserve position
var IDLE = 0
var LONG = 1
var SHORT = 2
var COVERLONG = 3
var COVERSHORT = 4
var COVERLONG_PART = 5
var COVERSHORT_PART = 6
var OPENLONG = 7
var OPENSHORT = 8

var State = IDLE

// Transaction logic part
function GetPosition(posType) {
    var positions = _C(exchange.GetPosition)
    /*
    if(positions.length > 1){
        throw "positions error:" + JSON.stringify(positions)
    }
    */
    var count = 0
    for(var j = 0; j < positions.length; j++){
        if(positions[j].ContractType == Symbol){
            count++
        }
    }

    if(count > 1){
        throw "positions error:" + JSON.stringify(positions)
    }

    for (var i = 0; i < positions.length; i++) {
        if (positions[i].ContractType == Symbol && positions[i].Type === posType) {
            return [positions[i].Price, positions[i].Amount];
        }
    }
    
    Sleep(TradeInterval);
    return [0, 0]
}

function CancelPendingOrders() {
    while (true) {
        var orders = _C(exchange.GetOrders)
        for (var i = 0; i < orders.length; i++) {
            exchange.CancelOrder(orders[i].Id);
            Sleep(TradeInterval);
        }
        if (orders.length === 0) {
            break;
        }
    }
}

function Trade(Type, Price, Amount, CurrPos, OnePriceTick){    // Process transactions
    if(Type == OPENLONG || Type == OPENSHORT){              // Processing position opening
        exchange.SetDirection(Type == OPENLONG ? "buy" : "sell")
        var pfnOpen = Type == OPENLONG ? exchange.Buy : exchange.Sell
        var idOpen = pfnOpen(Price, Amount, CurrPos, OnePriceTick, Type)
        Sleep(TradeInterval)
        if(idOpen) {
            exchange.CancelOrder(idOpen)
        } else {
            CancelPendingOrders()
        }
    } else if(Type == COVERLONG || Type == COVERSHORT){     // Process closing position
        exchange.SetDirection(Type == COVERLONG ? "closebuy" : "closesell")
        var pfnCover = Type == COVERLONG ? exchange.Sell : exchange.Buy
        var idCover = pfnCover(Price, Amount, CurrPos, OnePriceTick, Type)
        Sleep(TradeInterval)
        if(idCover){
            exchange.CancelOrder(idCover)
        } else {
            CancelPendingOrders()
        }
    } else {
        throw "Type error:" + Type
    }
}

function SuperTrend(r, period, multiplier) {
    // atr
    var atr = talib.ATR(r, period)

    // baseUp , baseDown
    var baseUp = []
    var baseDown = []
    for (var i = 0; i < r.length; i++) {
        if (isNaN(atr[i])) {
            baseUp.push(NaN)
            baseDown.push(NaN)
            continue
        }
        baseUp.push((r[i].High + r[i].Low) / 2 + multiplier * atr[i])
        baseDown.push((r[i].High + r[i].Low) / 2 - multiplier * atr[i])
    }

    // fiUp , fiDown
    var fiUp = []
    var fiDown = []
    var prevFiUp = 0
    var prevFiDown = 0
    for (var i = 0; i < r.length; i++) {
        if (isNaN(baseUp[i])) {
            fiUp.push(NaN)
        } else {
            fiUp.push(baseUp[i] < prevFiUp || r[i - 1].Close > prevFiUp ? baseUp[i] : prevFiUp)
            prevFiUp = fiUp[i]
        }

        if (isNaN(baseDown[i])) {
            fiDown.push(NaN)
        } else {
            fiDown.push(baseDown[i] > prevFiDown || r[i - 1].Close < prevFiDown ? baseDown[i] : prevFiDown)
            prevFiDown = fiDown[i]
        }
    }

    var st = []
    var prevSt = NaN
    for (var i = 0; i < r.length; i++) {
        if (i < period) {
            st.push(NaN)
            continue
        }

        var nowSt = 0
        if (((isNaN(prevSt) && isNaN(fiUp[i - 1])) || prevSt == fiUp[i - 1]) && r[i].Close <= fiUp[i]) {
            nowSt = fiUp[i]
        } else if (((isNaN(prevSt) && isNaN(fiUp[i - 1])) || prevSt == fiUp[i - 1]) && r[i].Close > fiUp[i]) {
            nowSt = fiDown[i]
        } else if (((isNaN(prevSt) && isNaN(fiDown[i - 1])) || prevSt == fiDown[i - 1]) && r[i].Close >= fiDown[i]) {
            nowSt = fiDown[i]
        } else if (((isNaN(prevSt) && isNaN(fiDown[i - 1])) || prevSt == fiDown[i - 1]) && r[i].Close < fiDown[i]) {
            nowSt = fiUp[i]
        }

        st.push(nowSt)
        prevSt = st[i]
    }

    var up = []
    var down = []
    for (var i = 0; i < r.length; i++) {
        if (isNaN(st[i])) {
            up.push(st[i])
            down.push(st[i])
        }

        if (r[i].Close < st[i]) {
            down.push(st[i])
            up.push(NaN)
        } else {
            down.push(NaN)
            up.push(st[i])
        }
    }

    return [up, down]
}

var preTime = 0
function main() {
    exchange.SetContractType(Symbol)
    
    while (1) {
        var r = _C(exchange.GetRecords)
        var currBar = r[r.length - 1]
        if (r.length < pd) {
            Sleep(5000)
            continue    
        }
        
        var st = SuperTrend(r, pd, factor)
             
        $.PlotRecords(r, "K")
        $.PlotLine("L", st[0][st[0].length - 2], r[r.length - 2].Time)
        $.PlotLine("S", st[1][st[1].length - 2], r[r.length - 2].Time)
        
        if(!isNaN(st[0][st[0].length - 2]) && isNaN(st[0][st[0].length - 3])){  
            if (State == SHORT) {
                State = COVERSHORT
            } else if(State == IDLE) {
                State = OPENLONG
            }
        }

        if(!isNaN(st[1][st[1].length - 2]) && isNaN(st[1][st[1].length - 3])){  
            if (State == LONG) {
                State = COVERLONG 
            } else if (State == IDLE) {
                State = OPENSHORT
            }
        }

        // Execution signal
        var pos = null
        var price = null
        if(State == OPENLONG){                          // Open long position
            pos = GetPosition(PD_LONG)                  // Check positions
                                                        // Determine whether the status is satisfied, and if so, modify the status
            if(pos[1] >= Amount){                       // Hold positions greater than or equal to the parameter-set opening volume
                Sleep(1000)
                $.PlotFlag(currBar.Time, "Open long position", 'OL') // Tag
                
                OpenAmount = pos[1]                     // Record of opening positions
                State = LONG                            // Mark as long position status
                continue
            }
            price = currBar.Close - (currBar.Close % PriceTick) + PriceTick * 2     // Calculate price
            Trade(OPENLONG, price, Amount - pos[1], pos, PriceTick)                 // Order Function (Type, Price, Amount, CurrPos, PriceTick)
        }

        if(State == OPENSHORT){                         // Open short position
            pos = GetPosition(PD_SHORT)                 // Check positions
            if(pos[1] >= Amount){
                Sleep(1000)
                $.PlotFlag(currBar.Time, "Open short position", 'OS')
                
                OpenAmount = pos[1]
                State = SHORT
                continue
            }
            price = currBar.Close - (currBar.Close % PriceTick) - PriceTick * 2
            Trade(OPENSHORT, price, Amount - pos[1], pos, PriceTick)
        }

        if(State == COVERLONG){                                         // Handle closing long positions
            pos = GetPosition(PD_LONG)                                  // Get Position Information
            if(pos[1] == 0){                                            // Determine whether the position is 0
                $.PlotFlag(currBar.Time, "Close Long Position", '----CL')             // Tag
                State = IDLE
                continue
            }
            price = currBar.Close - (currBar.Close % PriceTick) - PriceTick * 2
            Trade(COVERLONG, price, pos[1], pos, PriceTick)
        }
    
        if(State == COVERSHORT){                                        // Handle opening long positions
            pos = GetPosition(PD_SHORT)
            if(pos[1] == 0){
                $.PlotFlag(currBar.Time, "Close Short Position", '----CS')
                State = IDLE
                continue
            }
            price = currBar.Close - (currBar.Close % PriceTick) + PriceTick * 2
            Trade(COVERSHORT, price, pos[1], pos, PriceTick)
        }

        if(State == COVERLONG_PART) {                                   // Partially close long positions
            pos = GetPosition(PD_LONG)                                  // Get a position
            if(pos[1] <= KeepAmount){                                   // Hold positions less than or equal to the maintenance volume, this closing is completed
                $.PlotFlag(currBar.Time, "Close Long Position,Keep:" + KeepAmount, '----CL')     // Tag
                State = pos[1] == 0 ? IDLE : LONG                                  // Update Status
                continue
            }
            price = currBar.Close - (currBar.Close % PriceTick) - PriceTick * 2
            Trade(COVERLONG, price, pos[1] - KeepAmount, pos, PriceTick)
        }

        if(State == COVERSHORT_PART){
            pos = GetPosition(PD_SHORT)
            if(pos[1] <= KeepAmount){
                $.PlotFlag(currBar.Time, "Close Short Position,Keep:" + KeepAmount, '----CS')
                State = pos[1] == 0 ? IDLE : SHORT
                continue
            }
            price = currBar.Close - (currBar.Close % PriceTick) + PriceTick * 2
            Trade(COVERSHORT, price, pos[1] - KeepAmount, pos, PriceTick)
        }

        LogStatus(_D())
        Sleep(1000)
    }
}
```

> Detail

https://www.fmz.com/strategy/201837

> Last Modified

2020-04-24 14:34:33
