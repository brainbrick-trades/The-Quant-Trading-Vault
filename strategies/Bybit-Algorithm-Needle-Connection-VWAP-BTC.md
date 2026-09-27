
> Name

Bybit-Algorithm-Needle-Connection-VWAP-BTC

> Author

扁豆子

> Strategy Description

Start sharing the original Bybit penetration strategy here~
What is the main reason?///
 ![IMG](https://www.fmz.com/upload/asset/95a9985fc126e73d27e9.png) 
 
 This is very annoying, isn't it?...
 You said you were doing good open source and got angry without even knowing about it...
 Hope the little brother doesn't do this anymore~
 Open source directly here,
 It itself is not really an impressive strategy...
 
 Everyone is free to play.~
 Stop spending money to buy my crappy source code~
 Let's use it directly!! Let's go!!
 
 By the way, a quick advertisement~
 For more money-losing strategies, please follow the public account "Bean's Quantitative Journal""
 WX: wangxiaoba
 
 (●'◡'●)

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|start_balance|false|Initial amount|
|long_qty|true|Single long positionUSD|
|short_qty|true|Single short positionUSD|
|maxPosition|500000|Maximum Order Quantity|
|take_profit|45|Initial take profit(USD)|
|trailing_profit|true|Trailing take profitUSD|
|stop_loss|9|Stop Loss Percentage|
|long_vwap_offset|2.5|VWAPUpper Limit Percentage|
|short_vwap_offset|2.5|VWAPLower Limit Percentage|
|GG|3|leverage multiplier (2x-7x is suitable, the higher the leverage, the greater the risk))|
|stop_step|3600|Stop time after stop loss(s)|


> Source (javascript)

``` javascript
// JudgmentuidPermissions (UID list + getAccount uid Verification)
function user_auth() {
    user_list = [775536, 783571, 789086, 819490, 1265698, 1294567, 1299150]
    user_id = account.Info.result[0].user_id
    //Log(user_id)
    if (user_list.indexOf(user_id) == -1) {
        throw new Error('User authentication error, please contact WeChat: wangxiaoba')
    }
}

// Calculate acquisitionVWAPAnd Upper & Lower Boundaries Bybit
function VWAP() {
    // DefinitionKLine, CalculationVWAP
    if (records.length > 1440) {
        records.splice(0, 1);
    }
    var n = records.length - 1
    //Log(n)
    var total_sum = 0.0
    var volume_sum = 0
    vwap_arr = []
    vwap_up_arr = []
    vwap_dw_arr = []
    for (var i = 0; i < n + 1; i++) {
        var high_price = records[i].High
        //Log("log high_price " + high_price)
        var low_price = records[i].Low
        var close_price = records[i].Close
        //Log("log low_price " + low_price)
        var price = (high_price + low_price + close_price) / 3
        //Log("price", price)
        var volume = records[i].Volume
        //Log("log volume " + volume)
        total_sum += price * volume
        //Log("log total_sum " + total_sum)
        volume_sum += volume
        //Log("log volume_sum " + volume_sum)
        var re = total_sum / volume_sum
        var re_up = re * (1 + long_vwap_offset / 100)
        var re_dw = re * (1 - short_vwap_offset / 100)
        vwap_arr.push(re)
        vwap_up_arr.push(re_up)
        vwap_dw_arr.push(re_dw)
        //return total_sum / volume_sum
    }
    if (vwap_arr.length > 2000) {
        vwap_arr.splice(0, 1);
    }
    if (vwap_up_arr.length > 2000) {
        vwap_up_arr.splice(0, 1);
    }
    if (vwap_dw_arr.length > 2000) {
        vwap_dw_arr.splice(0, 1);
    }
    vwap = vwap_arr[vwap_arr.length - 1]
    vwap_up = vwap_up_arr[vwap_arr.length - 1]
    vwap_dw = vwap_dw_arr[vwap_arr.length - 1]
    //Log("log vwap " + vwap, "log vwap_up " + vwap_up, "log vwap_dw " + vwap_dw)
}

// Draw lines
function PlotMA_Kline(records, isFirst) {
    $.PlotRecords(records, "K")
    if (isFirst) {
        for (var i = records.length - 1; i >= 0; i--) {
            if (vwap_arr[i] !== null) {
                $.PlotLine("vwap", vwap_arr[i], records[i].Time)
                $.PlotLine("vwap_up", vwap_up_arr[i], records[i].Time)
                $.PlotLine("vwap_dw", vwap_dw_arr[i], records[i].Time)
            }
        }
        PreBarTime = records[records.length - 1].Time
    } else {
        if (PreBarTime !== records[records.length - 1].Time) {
            $.PlotLine("vwap", vwap_arr[vwap_arr.length - 2], records[records.length - 2].Time)
            $.PlotLine("vwap_up", vwap_up_arr[vwap_up_arr.length - 2], records[records.length - 2].Time)
            $.PlotLine("vwap_dw", vwap_dw_arr[vwap_dw_arr.length - 2], records[records.length - 2].Time)
            PreBarTime = records[records.length - 1].Time
        }
        $.PlotLine("vwap", vwap_arr[vwap_arr.length - 1], records[records.length - 1].Time)
        $.PlotLine("vwap_up", vwap_up_arr[vwap_up_arr.length - 1], records[records.length - 1].Time)
        $.PlotLine("vwap_dw", vwap_dw_arr[vwap_dw_arr.length - 1], records[records.length - 1].Time)
    }
}

// Encapsulate order, Many, Empty Bybit
// DefinitionBuy
function buy(Price, Amount, dec) {
    exchange.SetDirection("buy");
    var orderId = null;
    orderId = exchange.Buy(Price, Amount, dec, '@');
    while (!orderId && typeof(orderId) != "undefined" && orderId != 0) {
        Log(orderId);
        Sleep(100);
        orderId = exchange.Buy(Price, Amount, dec, '@');

    }
    return orderId;
}

// DefinitionSell
function sell(Price, Amount, dec) {
    exchange.SetDirection("sell");
    var orderId = null;
    orderId = exchange.Sell(Price, Amount, dec, '@');
    while (!orderId && typeof(orderId) != "undefined" && orderId != 0) {
        Log(orderId);
        Sleep(100);
        orderId = exchange.Sell(Price, Amount, dec, '@');

    }
    return orderId;
}

// Account Information
function AccountInfo() {
    // Asset Information Table
    var AccountTab = {
        type: "table",
        title: "Asset information",
        cols: ["Position", "Position direction", "Average position price", "Current price", "Liquidation point", "Leverage multiple", "Position profit and loss", "Starting asset value", "Total assets", "Net assets", "Total profit and loss""],
        rows: [],
    }
    AccountTab.rows.push([account.Info.result[0].size, CW, account.Info.result[0].entry_price, ticker.Last, account.Info.result[0].liq_price, account.Info.result[0].leverage, account.Info.result[0].unrealised_pnl, start_balance, account.Info.result[0].wallet_balance, jzc, pt])
    LogStatus(_D() + '   STATUS: ' + CW + '\n' +
        'Total orderable quantity(*leverage): ' + yue + '\n' +
        'index: ' + index + '\n' +
        'VWAP: ' + vwap + '\n' +
        'VWAP_UP: ' + vwap_up + '\n' +
        'VWAP_DW: ' + vwap_dw + '\n' +
        'N: ' + records.length + '\n' +
        'WX: wangxiaoba' + '\n' +
        '`' + JSON.stringify([AccountTab]) + '`' + '\n');
}

// Status judgment
function Status() {
    if (account.Info.result[0].side === "Buy") {
        status = PD_LONG;
        CW = "LONG";
    } else if (account.Info.result[0].side === "Sell") {
        status = PD_SHORT;
        CW = "SHORT";
    } else {
        status = idle;
        CW = "IDLE";
    }
}

// Trailing Take Profit Initial%, TrackingU
function TP() {
    var TP_first_long = account.Info.result[0].entry_price + take_profit
    var TP_trailing_long = TP_HH - trailing_profit
    var TP_first_short = account.Info.result[0].entry_price - take_profit
    var TP_trailing_short = TP_LL + trailing_profit
    // When holding a long position, Current price greater than opening+Initial Take Profit Price -> Trigger trailing take profit 
    if ((status === PD_LONG) && (ticker.Last > TP_first_long)) {
        // Log('When holding a long position, Current price greater than opening+Initial Take Profit Price -> Trigger trailing take profit', TP_HH)
        TP_status = true
        // Trigger trailing take profit, Uninitialized maximum opening price -> After opening a position, update the maximum price to the current price
        if (TP_status === true && TP_HH == 0) {
            Log('Trigger trailing take profit, Uninitialized maximum opening price -> After opening a position, update the maximum price to the current price', TP_HH)
            TP_HH = ticker.Last
        }
        // Trigger trailing take profit, Maximum price after existing positions opened, The current price is greater than the maximum price after opening the position -> After opening a position, update the maximum price to the current price
        else if (TP_status === true && TP_HH != 0 && ticker.Last > TP_HH) {
            Log('Trigger trailing take profit, Maximum price after existing positions opened, The current price is greater than the maximum price after opening the position -> After opening a position, update the maximum price to the current price', TP_HH)
            TP_HH = ticker.Last
        }
        // Trigger trailing take profit, Maximum price after existing positions opened, Current price is less than (Maximum price reduction after opening a position - RetracementUSD) -> Close short position with take profit
        else if (TP_status === true && TP_HH != 0 && ticker.Last < TP_trailing_long) {
            Log('Trigger trailing take profit, Maximum price after existing positions opened, Current price is less than (Maximum price reduction after opening a position - RetracementUSD) -> Close short position with take profit', TP_HH)
            sell(-1, account.Info.result[0].size, "At/In" + ticker.Last + "Take Profit Close Long Position!! Opening price: " + account.Info.result[0].entry_price + "Quantity: " + account.Info.result[0].size)
            status = idle
            $.PlotFlag(new Date().getTime(), 'Close_Long', 'PT_L')
            TP_status = false
            TP_HH = 0
            LogProfit(pt, pt * ticker.Last)
        }
    }
    // When holding a short position, Current price less than opening-Initial Take Profit Price -> Trigger trailing take profit
    else if ((status === PD_SHORT) && (ticker.Last < TP_first_short)) {
        // Log('When holding a short position, Current price less than opening-Initial Take Profit Price -> Trigger trailing take profit', TP_LL)
        TP_status = true
        // Trigger trailing take profit, Uninitialized maximum opening price -> After opening a position, update the minimum price to the current price
        if (TP_status === true && TP_LL == 0) {
            Log('Trigger trailing take profit, Uninitialized maximum opening price -> After opening a position, update the minimum price to the current price', TP_LL)
            TP_LL = ticker.Last
        }
        // Trigger trailing take profit, Minimum price after existing positions opened, The current price is less than the minimum price after opening the position -> After opening a position, update the minimum price to the current price
        else if (TP_status === true && TP_LL != 0 && ticker.Last < TP_LL) {
            Log('Trigger trailing take profit, Minimum price after existing positions opened, The current price is less than the minimum price after opening the position -> After opening a position, update the minimum price to the current price', TP_LL)
            TP_LL = ticker.Last
        }
        // Trigger trailing take profit, Minimum price after existing positions opened, Current price is greater than (After opening a position, the minimum price is reduced + RetracementUSD) -> Close long position with take profit
        else if (TP_status === true && TP_LL != 0 && ticker.Last > TP_trailing_short) {
            Log('Trigger trailing take profit, Minimum price after existing positions opened, Current price is greater than (After opening a position, the minimum price is reduced + RetracementUSD) -> Close long position with take profit', TP_LL)
            buy(-1, account.Info.result[0].size, "At/In" + ticker.Last + "Take Profit Close Short Position!! Opening price: " + account.Info.result[0].entry_price + "Quantity: " + account.Info.result[0].size)
            status = idle
            $.PlotFlag(new Date().getTime(), 'Close_Short', 'PT_S')
            TP_status = false
            TP_LL = 0
            LogProfit(pt, pt * ticker.Last)
        }
    }
}

// stop loss %
function Stoploss() {
    // When holding a long position, Current price less than opening-Stop loss price, Short to close long
    if ((status === PD_LONG) && (ticker.Last < account.Info.result[0].entry_price - (ticker.Last * stop_loss / 100))) {
        Log('When holding a long position, Current price less than opening-Stop loss price, Short to close long')
        sell(-1, account.Info.result[0].size, "At/In" + ticker.Last + "Stop Loss Close Long Position!! Opening price: " + account.Info.result[0].entry_price + " Quantity: " + account.Info.result[0].size)
        status = idle
        isstoploss = true
        $.PlotFlag(new Date().getTime(), 'Close_Long', 'ST_L')
        LogProfit(pt, pt * ticker.Last)
    }
    // When holding a short position, Current price greater than opening+Stop loss price, Long to close short
    else if ((status === PD_SHORT) && (ticker.Last > account.Info.result[0].entry_price + (ticker.Last * stop_loss / 100))) {
        Log('When holding a short position, Current price greater than opening+Stop loss price, Long to close short')
        buy(-1, account.Info.result[0].size, "At/In" + ticker.Last + "Stop Loss Close Short Position!! Opening price: " + account.Info.result[0].entry_price + " Quantity: " + account.Info.result[0].size)
        status = idle
        isstoploss = true
        $.PlotFlag(new Date().getTime(), 'Close_Short', 'ST_S')
        LogProfit(pt, pt * ticker.Last)
    }
}

function AtrIndex() {
    if (records && records.length > 14) {
        var atr = TA.ATR(records, 14)
    }
    if (atr && atr.length > 20) {
        var eamatr = TA.EMA(atr, 20)
        // Log(eamatr[eamatr.length - 1])
    }
    if (eamatr){
        var temp = 0
        for(var i=0; i<eamatr.length; i++){
            temp += atr[atr.length - 1]/eamatr[eamatr.length - 1]
        }
    }
    index = _N((temp/eamatr.length), 4)
}


// Calculate income
function PT_log() {
    time = new Date().getTime();
    if (time >= (timep + 7200000)) {
        LogProfit(pt, pt * ticker.Last);
        timep = time;
    }
}


function main() {
    // Initialize parameters 
    PreBarTime = 0
    isFirst = true
    exchange.SetMarginLevel(GG)
    exchange.SetContractType('swap');
    _CDelay(100);
    idle = -1;
    status = idle;
    CW = 0;
    timep = 0;
    TP_status = false // Whether to trigger trailing take profit 
    TP_HH = 0
    TP_LL = 0
    isstoploss = false
    index = 0
    // WS Configuration
    var param = {
        "op": "subscribe",
        "args": "liquidation"
    }
    var client = Dial("wss://www.bitmex.com/realtime|reconnect=true&payload=" + JSON.stringify(param), 3800)
    client.write('{"op": "subscribe", "args": "liquidation"}')
    while (1) {
        // Define basic information
        account = _C(exchange.GetAccount)
        records_5m = _C(exchange.GetRecords, PERIOD_M5)
        records = _C(exchange.GetRecords, PERIOD_M1)
        ticker = _C(exchange.GetTicker)
        yue = account.Info.result[0].wallet_balance * ticker.Last * GG; // Total openable position (Wallet coins x Latest price x Leverage))
        jzc = account.Info.result[0].wallet_balance + account.Info.result[0].unrealised_pnl; // Net asset amount (total assets - unrealized P&L))
        pt = jzc - start_balance; // Profit (Net Assets - Initial Coin Amount)
        //Log('Initialize')
        // Status judgment
        Status()
        //Log('Status judgment')
        // Permission verification
        // user_auth()
        //Log('Permission verification')
        // Packaging indicators, Parallel drawingKLine
        AtrIndex()
        VWAP()
        //Log('Indicator packaging')
        if (records) {
            PlotMA_Kline(records_5m, isFirst)
            //Log('Draw lines')
            isFirst = false
        }
        // ReadWSMessage
        bitmexData = client.read(-1)
        obj = null
        //Log('ReadWSMessage')
        if (bitmexData) {
            obj = JSON.parse(bitmexData)
            //Log('bitmex liquidation Data ', obj)
        }
        //Log('ReadWSMessage completed')
        // Order logic!
        // Determine trading pair, and liquidation value (BTC>100000, ETH>7500 , EOS?? , XRP??) {"table":"liquidation","action":"insert","data":[{"orderID":"77e987c5-03c2-814e-0fb3-5632f9438f31","symbol":"XBTUSD","side":"Buy","price":9938,"leavesQty":32618}]}
        // trading pair
        if (obj) {
            if (obj.table == "liquidation" && obj.action == "insert" && obj.data[0].symbol == "XBTUSD") {
                // Log('Determine trading pair')
                // Direction and size
                // When liquidation direction isBuy, Liquidation amount greater than10W, Latest price greater thanvwapUpper bound time, is less than the maximum opening amount!! go short
                if (obj.data[0].side == "Buy" && obj.data[0].leavesQty > 250000 && ticker.Last > vwap_up && account.Info.result[0].size < maxPosition) {
                    Log('Determine size direction, Empty')
                    sell(-1, short_qty, "At/In" + ticker.Last + "- go short " + short_qty + "|")
                    $.PlotFlag(new Date().getTime(), 'Sell', 'SK')
                }
                // When liquidation direction isSell, Liquidation amount greater than10W, Latest price less thanvwapNether time, is less than the maximum opening amount!! go long
                else if (obj.data[0].side == "Sell" && obj.data[0].leavesQty > 250000 && ticker.Last < vwap_dw && account.Info.result[0].size < maxPosition) {
                    Log('Determine size direction, Many')
                    buy(-1, long_qty, "At/In" + ticker.Last + "- go long " + long_qty + "|")
                    $.PlotFlag(new Date().getTime(), 'Buy', 'BK')
                }
            }
        }
        // stop loss 
        Stoploss()
        if (isstoploss === true) {
            Log("Trigger stop loss, Pause after stop loss!! " + stop_step + "s!!!")
            AccountInfo()
            Sleep(stop_step * 1000)
            isstoploss = false
        }
        //Log('stop loss')
        // Trailing take profit
        TP()
        //Log('Trailing take profit')
        // Account information update
        AccountInfo()
        // Interval time
        //Log('Interval time')
        Sleep(600);
    }
}
```

> Detail

https://www.fmz.com/strategy/182656

> Last Modified

2021-01-29 10:44:37
