
> Name

Test-Using-KDJ-and-VOL-Volume-to-Filter-for-Coins-with-Potential-to-Rise

> Author

xxs1xxs1



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|MarginLevel|20|MarginLevel|
|amountScale|3|quantity precision|
|priceScale|5|Price Precision|
|bet|10|Order Margin|




|Button|Default|Description|
|----|----|----|
|Cleared data |__button__| Cleared data|
|Clear persistent data|__button__|Clear persistent data|


> Source (javascript)

``` javascript
/*backtest
start: 2021-05-1 00:00:00
end: 2021-05-28 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
args: [["OpType",1]]
*/

//Function Tests
exchange.SetContractType("swap") //Contract settings
// exchange.SetCurrency("TRX_USDT");
//    exchange.SetMarginLevel(20) //Contract leverage setting 

//exchange.IO("trade_margin")
//exchange.IO("currency", "STPT_USDT")
var account = _C(exchange.GetAccount) //Account information
var log_profit = 0
var log_profit_intervel = 1000 * 60 * 5
var symbol_list = [] //"1.5timesvol,kdjandmalong"                //indexLocation details 0=>trading pair  1=>Price Precision 2=>quantity precision 3=>Notes 4=>OrderID 5=>Maximum loss for the current cryptocurrency 6=>.....            Suffers from array strictness. Except for the fixed data in the front being useful, unforeseen events later will not affect it????
var symbol_list1 = [] //"3timesvol,Current increase4%orvol5times"
var symbol_list2 = [] //"Three consecutive rises"
var order_list = []
var num = 0 //Record additional purchase quantity
var loss = 0.6
var loss_m = 0

if (_G("symbol")) {
    symbol_list = _G("symbol")
    order_list = _G("orderlist")
    Log("Last data", symbol_list)
    Log("Last completed data", order_list)
}

// Cancel Order Function
function CancelPendingOrders() {
    Sleep(1000); // Sleep for 1 second
    var ret = false;
    while (true) {
        var orders = null;
        // Continuously fetch the array of unexecuted orders; if an exception is returned, continue fetching
        while (!(orders = exchange.GetOrders())) {
            Sleep(1000); // Sleep for 1 second
        }
        if (orders.length == 0) { // If the order array is empty
            return ret; // Return to order cancellation status
        }
        for (var j = 0; j < orders.length; j++) { // Iterate through the array of unfilled orders
            exchange.CancelOrder(orders[j].Id, orders[j]); // Cancel unfilled orders one by one
            ret = true;
            if (j < (orders.length - 1)) {
                Sleep(1000); // Sleep for 1 second
            }
        }
    }
}

function symbols() {


    log_profit_intervel = 1000 * 60 * 5


    if (Date.now() - log_profit > log_profit_intervel && !IsVirtual()) { //All trading pairs 
        log_profit = Date.now()
        var symbol = JSON.parse(HttpQuery("https://www.binance.com/fapi/v1/exchangeInfo"))
        let symbol_all = []
        symbol.symbols.forEach(function(v, k, arr) {
            if (v.quoteAsset == "USDT" && v.contractType == "PERPETUAL") {
                let str = v.symbol.split("USDT", 1)
                str = str + "_USDT"
                symbol_all.push([str, v.pricePrecision, v.quantityPrecision])
            }
        })

        // exchange.SetCurrency("TRX_USDT");                        //Trading pair settings
        //exchange.SetPrecision(priceScale, amountScale)            //Precision setting


        for (let i = 0; i < symbol_all.length; i++) {

            if (symbol_list.length > 0) {

                let flag = false
                symbol_list.forEach(function(v, k, arr) {
                    //   Log(v[0],symbol_all[i][0])
                    if (v[0] == symbol_all[i][0]) {
                        flag = true;
                    }
                })
                if (flag) {
                    continue;
                }
            }



            exchange.SetCurrency(symbol_all[i][0])
            //  exchange.SetCurrency("DOGE_USDT")
            exchange.SetPrecision(symbol_all[i][1], symbol_all[i][2])


            let records = exchange.GetRecords(60 * 60 * 1)
            let kdj = TA.KDJ(records, 9, 3, 3)
            let ma7 = TA.EMA(records, 7)
            let ma25 = TA.EMA(records, 25)

            //      let records1 = exchange.GetRecords(60 * 15)
            //      let kdj1 = TA.KDJ(records1, 9, 3, 3)

            let len = records.length - 1
            let rs = records[len]
            let rs1 = records[len - 1] //Previous data 
            //      if ((rs.Close > rs.Open && rs.Volume > rs1.Volume * 1.5 && rs.Close / rs.Open > 1.04) || (rs.Close > rs.Open && rs.Volume > rs1.Volume * 2)) 
            //     if (rs.Close > rs.Open && _Cross(kdj[0], kdj[1]) > 0 && _Cross(kdj[0], kdj[1]) < 3 && rs.Close / rs.Low < 1.03 && _Cross(kdj1[0], kdj1[1]) > 0 && _Cross(kdj1[0], kdj1[1]) < 3) 

            if (rs.Close > rs.Open && rs.Volume > rs1.Volume * 1.5 && _Cross(kdj[0], kdj[1]) > 0 && _Cross(ma7, ma25) > 0) {

                symbol_list.push([symbol_all[i][0], symbol_all[i][1], symbol_all[i][2], "More requirements",0,0]) //Add data saving

            }
            if ((rs.Close > rs.Open && rs.Volume > rs.Volume * 1.5 && rs.Close / rs.Open > 1.02) || (rs.Close > rs.Open && rs.Volume > rs1.Volume * 2)) {
                symbol_list1.push([symbol_all[i][0], symbol_all[i][1], symbol_all[i][2]]) //Add data saving
            }
            if (records[len - 2].Close > records[len - 2].Open && records[len - 1].Close > records[len - 1].Open && records[len].Close > records[len].Open) {
                symbol_list.push([symbol_all[i][0], symbol_all[i][1], symbol_all[i][2], "Three consecutive rises",0,0]) //Add data saving
            }

            Sleep(100)
        }
        Log("General requirements", symbol_list)
        Log("May rise sharply", symbol_list1)
        //      Log("Three consecutive rises", symbol_list2)

    }
}







function main() {


    var increase = [] //Add position setting
    if (IsVirtual()) { //Needed for simulation accounts, ignored automatically in live accounts
        symbol_list.push([exchange.GetCurrency(), priceScale, amountScale])
    }

    while (1) {
        symbols()
        //       Log("Start", symbol_list)


        if (symbol_list.length > 0 && 1 == 1) {

            for (let i = 0; i < symbol_list.length; i++) {
                //Consider buying directly

                if (symbol_list[i][0] == "ADA_USDT" || symbol_list[i][0] == "BTCDOM_USDT") { //Set trading pairs you do not want
                    continue;
                }
                if (!IsVirtual()) {
                    exchange.SetCurrency(symbol_list[i][0]); //Trading pair settings
                }
                
                exchange.SetPrecision(symbol_list[i][1], symbol_list[i][2]) //Precision setting

                exchange.SetMarginLevel(MarginLevel) //Contract multiple

                let records = exchange.GetRecords(60 * 60 * 1)
                let kdj = TA.KDJ(records, 9, 3, 3)
                let account = exchange.GetAccount()
                let position = _C(exchange.GetPosition) //Position information
                let Amount = position[0] ? position[0].Amount : 0
                let ticker = _C(exchange.GetTicker); // Obtain Tick Data

            let ma7 = TA.EMA(records, 7)
            let ma25 = TA.EMA(records, 25)

                let money = bet * MarginLevel //Buy quantity is 2UCommodity                


                if (_N(money / ticker.Sell, symbol_list[i][2]) == 0) {
                    continue;
                }

                let orderid //Get the order immediately after placing a tradeID
                let pos //Temporarily get position information
                //   Log(symbol_list[i])
                if (typeof(symbol_list[i][4]) != "undefined" && symbol_list[i][4] > 0 ) {
                    let exid = exchange.GetOrder(symbol_list[i][4])
                    if (exid && exid.Status) {

                        Log(symbol_list[i],"-----Profit------")
                        
                        
                        let id = symbol_list.splice(i, 1) //Clear data to prevent second purchase
                        Log(id[0])
                        id[0].push("Profit, technical is limited")
                        order_list.push(id[0])
                    CancelPendingOrders() //Clear invalid orders
                        
                        if (IsVirtual()) { //Needed for simulation accounts, ignored automatically in live accounts
                            symbol_list.push([exchange.GetCurrency(), priceScale, amountScale])
                        }

                    }
                    

                }


                if (!position[0] && _Cross(kdj[0], kdj[1]) > 0 && _Cross(ma7,ma25)>0) { //New position _Cross(kdj[0], kdj[1]) < 4 &&
                    CancelPendingOrders() //Clear invalid orders
                    
                    exchange.SetDirection("buy")
                    exchange.Buy(-1, money / ticker.Sell, symbol_list[i], "Opening price:", ticker.Last, "#ccff00")

                    Sleep(100)
                    CancelPendingOrders() //Clear invalid orders
                    pos = exchange.GetPosition()
                    if(pos[0]){
                    exchange.SetDirection("closebuy")
                    orderid = exchange.Sell(_N(pos[0].Price * 1.01,symbol_list[i][1]), pos[0].Amount, "Pre-set order111111111111111111", "Position Quantity:", pos[0].Amount, "| Floating loss:", pos[0].Profit, "| Margin:", pos[0].Margin, "| Existing funds:", account.Balance, "| Average position price:", pos[0].Price, "-------|", loss_m, symbol_list[i], "#0000ff")


            if(orderid){symbol_list[i][4] = orderid}
                    }



                } else if (position[0] && position[0].Profit > position[0].Margin * 0.2) { //Profit20%Just liquidate, actually means1%The increase, here is20times

                    num = 0
                    loss = 0.6
                    exchange.SetDirection("closebuy")
                    exchange.Sell(-1, position[0].Amount, "Profit", position[0].Profit, symbol_list[i], ticker.Last)

                    CancelPendingOrders() //Clear invalid orders

                    if (!IsVirtual()) { //Real offer required

                        let id = symbol_list.splice(i, 1) //Clear data to prevent second purchase
                        Log(id[0])
                        id[0].push("Profit", position[0].Profit)
                        order_list.push(id[0])
                    }



                } else if (position[0] && position[0].Margin / bet < 2.5 && position[0].Profit * -1 > position[0].Margin * 0.2) { //fall1%Replenish once

                    let nn = 0.2 //Index
                    if (position[0].Profit * -1 / position[0].Margin > 0.4) {
                        nn = position[0].Profit * -1 / position[0].Margin
                        Log(nn, "---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

                    }
                    if (_N(position[0].Amount * nn, symbol_list[i][2]) == 0) {
                        continue;
                    }


                    exchange.SetDirection("buy")
                    exchange.Buy(-1, position[0].Amount * nn, "Cover position", ticker.Last, symbol_list[i], "Position Quantity:", position[0].Amount, "| Floating loss:", position[0].Profit, "| Margin:", position[0].Margin, "| Existing funds:", account.Balance, "| Average position price:", position[0].Price, "-------|", loss_m, symbol_list[i], "#0000ff")



                    Sleep(100)

                    CancelPendingOrders() //Clear invalid orders
                    pos = exchange.GetPosition()
                    exchange.SetDirection("closebuy")
                    orderid = exchange.Sell(_N(pos[0].Price * 1.01,symbol_list[i][1]), pos[0].Amount, "Pre-set order", "Position Quantity:", pos[0].Amount, "| Floating loss:", pos[0].Profit, "| Margin:", pos[0].Margin, "| Existing funds:", account.Balance, "| Average position price:", pos[0].Price, "-------|", loss_m, symbol_list[i], "#0000ff")


            if(orderid){symbol_list[i][4] = orderid}




                } else if (position[0] && position[0].Margin / bet >= 2.5 && position[0].Profit * -1 > position[0].Margin * 2) { //Replenish once after principal is lost

                    exchange.SetDirection("buy")
                    exchange.Buy(-1, position[0].Amount * 2, "Cover position", ticker.Last, symbol_list[i], "Position Quantity:", position[0].Amount, "| Floating loss:", position[0].Profit, "| Margin:", position[0].Margin, "| Existing funds:", account.Balance, "| Average position price:", position[0].Price, "-------|", loss_m, symbol_list[i], "#0000ff")

                    Sleep(100)


                    CancelPendingOrders() //Clear invalid orders
                    pos = exchange.GetPosition()
                    exchange.SetDirection("closebuy")
                    orderid = exchange.Sell(_N(pos[0].Price * 1.01,symbol_list[i][1]), pos[0].Amount, "Pre-set order", "Position Quantity:", pos[0].Amount, "| Floating loss:", pos[0].Profit, "| Margin:", pos[0].Margin, "| Existing funds:", account.Balance, "| Average position price:", pos[0].Price, "-------|", loss_m, symbol_list[i], "#0000ff")

  
            if(orderid){symbol_list[i][4] = orderid}


                }

                Sleep(300)
                if (pos && pos[0] && 1==0) {
                    //      Log(pos[0])   

                    exchange.SetDirection("buy")
                    exchange.Buy(_N(pos[0].Price * 0.9,symbol_list[i][1]), pos[0].Amount * 2, "10%Pre-order", "Current Price", ticker.Last, "Position Quantity:", pos[0].Amount, "| Floating loss:", pos[0].Profit, "| Margin:", pos[0].Margin, "| Existing funds:", account.Balance, "| Average position price:", pos[0].Price, "-------|", loss_m, symbol_list[i], "#ff0000")

                }


                if (position[0]) loss_m = position[0].Profit < loss_m ? position[0].Profit : loss_m
                    symbol_list[i][5] = loss_m
                Sleep(300)

            }
        }
        // Log("Data already cleared",order_list)
        //     Log("End", symbol_list)
        _G("orderlist", order_list)
        _G("symbol", symbol_list)
        Sleep(1000 * 1)



        //      Log("Worked hard through one round")

        let cmd = GetCommand()
        if (cmd) {
            Log(cmd)
            let arr = cmd.split(":")
            if (arr[0] == "Need to short") {
                dan = 100
            } else if (arr[0] == "Checksymbol_list") {
                Log("No data means no conditions are met", symbol_list)
            } else if (arr[0] == "Data already cleared") {

                Log("Data already cleared", order_list)

            } else if (arr[0] == "Clear persistent data") {

                Log("Data already cleared")
                _G("symbol", null)
                _G("orderlist", null)
                _G(null)

            }



        }
    }






}
```

> Detail

https://www.fmz.com/strategy/313036

> Last Modified

2021-09-09 21:39:15
