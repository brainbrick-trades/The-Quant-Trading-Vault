
> Name

Test-About-the-Long-Term-Effect-of-Martin

> Author

xxs1xxs1

> Strategy Description

I don't even know if this counts as Martin. I just want to go long. Just find any price level to open a position. Then add to the position.
For example, the initial small additional position is prepared for a 10% drop.
For large positions, you can slowly set 10%, 20%, 50% if you can feel that the possibility of falling is high to some extent. Just enlarge the position to cover the position to form a bargain hunting.
Therefore, pre-supplementing positions is very important...
Make the best use of everyone's wisdom. Hopefully, we can have more suggestions to improve mechanical trading together.
The most important thing is to calculate the tolerable point. Do not trigger liquidation. At present, this should open up to 8x at most

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|MarginLevel|20|MarginLevel|
|amountScale|3|quantity precision|
|priceScale|5|Price Precision|
|bet|100|Order Margin|




|Button|Default|Description|
|----|----|----|
|Cleared data |__button__| Cleared data|
|Clear persistent data|__button__|Clear persistent data|


> Source (javascript)

``` javascript
/*backtest
start: 2021-05-1 00:00:00
end: 2021-08-28 00:00:00
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
var symbol_list = [] //"1.5timesvol,kdjandmalong"
var symbol_list1 = [] //"3timesvol,Current increase4%orvol5times"
var symbol_list2 = [] //"Three consecutive rises"
var order_list = []
var num = 0 //Record additional purchase quantity
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
            exchange.CancelOrder(orders[j].Id); // Cancel unfilled orders one by one
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
            //      let rs1 = records[len]
            //      if ((rs.Close > rs.Open && rs.Volume > rs1.Volume * 1.5 && rs.Close / rs.Open > 1.04) || (rs.Close > rs.Open && rs.Volume > rs1.Volume * 2)) 
            //     if (rs.Close > rs.Open && _Cross(kdj[0], kdj[1]) > 0 && _Cross(kdj[0], kdj[1]) < 3 && rs.Close / rs.Low < 1.03 && _Cross(kdj1[0], kdj1[1]) > 0 && _Cross(kdj1[0], kdj1[1]) < 3) 

            if (rs.Close > rs.Open && rs.Volume > rs1.Volume * 1.5 && _Cross(kdj[0], kdj[1]) > 0 && _Cross(kdj[0], kdj[1]) < 5 && _Cross(ma7, ma25) > 0) {

                symbol_list.push([symbol_all[i][0], symbol_all[i][1], symbol_all[i][2]]) //Add data saving

            }
            if ((rs.Close > rs.Open && rs.Volume > rs1.Volume * 2 && rs.Close / rs.Open > 1.04) || (rs.Close > rs.Open && rs.Volume > rs1.Volume * 4)) {
                symbol_list1.push([symbol_all[i][0], symbol_all[i][1], symbol_all[i][2]]) //Add data saving
            }
            if (records[len - 3].Close > records[len - 3].Open && records[len - 1].Close > records[len - 1].Open && records[len - 2].Close > records[len - 2].Open) {
                symbol_list2.push([symbol_all[i][0], symbol_all[i][1], symbol_all[i][2]]) //Add data saving
            }

            Sleep(100)
        }
        Log("No data", symbol_list)
        Log("No data", symbol_list1)
        Log("Three consecutive rises", symbol_list2)

    }
}







function main() {

    let loss = 2
    let loss_m = 0

    while (1) {
        // symbols()



        exchange.SetPrecision(priceScale, amountScale) //Precision setting

        exchange.SetMarginLevel(MarginLevel) //Contract multiple

        let records = exchange.GetRecords(60 * 60 * 4)
        let kdj = TA.KDJ(records, 9, 3, 3)
        let account = exchange.GetAccount()
        let position = _C(exchange.GetPosition) //Position information
        let Amount = position[0] ? position[0].Amount : 0
        let ticker = _C(exchange.GetTicker); // Obtain Tick Data
        let ma7 = TA.EMA(records, 7)
        let ma25 = TA.EMA(records, 25)
        let money = bet * MarginLevel //Buy quantity is 2UCommodity                

        if (_N(money / ticker.Sell, amountScale) == 0) {
            continue;
        }
        let len = records.length - 1
        if (!position[0] && _Cross(kdj[0], kdj[1]) > 0 && kdj[2][len] > kdj[1][len] + 2) {
            exchange.SetDirection("buy")
            exchange.Buy(-1, money / ticker.Sell, ticker.Last,"Opening price:", ticker.Sell)


        } else if (position[0] && position[0].Profit > position[0].Margin * 0.2) { //Profit20%Then clear positions

            //     Log(loss_m,position[0])
            exchange.SetDirection("closebuy")
            exchange.Sell(-1, position[0].Amount,ticker.Last, "Profit", position[0].Profit, ticker.Last, "#ff0000")
            loss = 0.6
            num = 0 //Clear count
            CancelPendingOrders() //Clear invalid orders

        } else if (position[0] &&  _Cross(kdj[0], kdj[1]) < 0 && position[0].Profit > position[0].Margin * 0.1) { //death cross Close Position

            //     Log(loss_m,position[0])
            exchange.SetDirection("closebuy")
            exchange.Sell(-1, position[0].Amount,ticker.Last, "death cross Close Position", position[0].Profit, ticker.Last, "#00009c")
            loss = 0.6
            num = 0 //Clear count
            CancelPendingOrders() //Clear invalid orders

        }else if (position[0] && position[0].Margin / bet < 2.5 && position[0].Profit * -1 > position[0].Margin * 0.4) { //Replenish once after principal is lost

            let nn = 0.2 //Index
            if (position[0].Profit * -1 / position[0].Margin > 0.4) {
                nn = position[0].Profit * -1 / position[0].Margin
                Log(nn, "---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

            }

            exchange.SetDirection("buy")
            exchange.Buy(-1, position[0].Amount * nn, ticker.Last,"Small replenishment", ticker.Last, "Position Quantity:", position[0].Amount, "| Floating loss:", position[0].Profit, "| Margin:", position[0].Margin, "| Existing funds:", account.Balance, "| Average position price:", position[0].Price, "-------|Maximum single floating loss", loss_m, "#0000ff")

            //      CancelPendingOrders() //Clear invalid orders
        } else if (position[0] && position[0].Margin / bet >= 2.5 && position[0].Margin / bet < 6 && position[0].Profit * -1 > position[0].Margin * 2) { //Replenish once after principal is lost


            exchange.SetDirection("buy")
            exchange.Buy(-1, position[0].Amount * 2, ticker.Last,"Large replenishment", ticker.Last, "Position Quantity:", position[0].Amount, "| Floating loss:", position[0].Profit, "| Margin:", position[0].Margin, "| Existing funds:", account.Balance, "| Average position price:", position[0].Price, "-------|Maximum single floating loss", loss_m, "#ccff00")

            //    CancelPendingOrders() //Clear invalid orders
        }

        Sleep(1000)

        // Log("Data already cleared",order_list)
        //     Log("End", symbol_list)
        _G("orderlist", order_list)
        _G("symbol", symbol_list)
        Sleep(1000 * 2)

        if (position[0]) loss_m = position[0].Profit < loss_m ? position[0].Profit : loss_m

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
                _G(null)

            }



        }
    }
Log( _C(exchange.GetPosition))





}
```

> Detail

https://www.fmz.com/strategy/313486

> Last Modified

2021-09-19 12:42:30
