
> Name

TradingView-Strategy-Signal-Order-Robot-Binance-Version

> Author

高频量化



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|IsMarketOrder|false|Whether to use market order|
|QuotePrecision|3|Order price accuracy|
|BasePrecision|3|Order quantity accuracy|
|Ct||Futures contract code|




|Button|Default|Description|
|----|----|----|
|buy|0.01|Test Buy|
|sell|0.01|Test Sell|
|long|0.01|Test to go long|
|short|0.01|Test short selling|
|cover_long|0.01|Test Long Close|
|cover_short|0.01|Test flat|


> Source (javascript)

``` javascript
/*
- Interaction command string format
  action:amount
  action: buy , sell , long , short , cover_long , cover_short, spk , bpk
- Exchange type
  eTypeVariable Values: 0 spot , 1 futures

- TVDocumentation Link
  https://www.tradingview.com/pine-script-docs/en/v4/Quickstart_guide.html
  https://cn.tradingview.com/chart/8xfTuX7F/

- TV webhook Send Request
  https://www.fmz.com/api/v1?access_key=xxx&secret_key=yyyy&method=CommandRobot&args=[186515,"action:amount"]

- Reference Library
  Reference cryptocurrency trading library
*/

// Parameters
//var IsMarketOrder = true 
var QuotePrecision = 3
var BasePrecision = 3

// Futures Parameters
var Ct = "swap"
//exchange.SetContractType("swap")        // Set to perpetual contract
//exchange.SetCurrency("BTC_USDT")

// Global Variables
var BUY = "buy"
var SELL = "sell"
var LONG = "long"
var SHORT = "short"
var COVER_LONG = "cover_long"
var COVER_SHORT = "cover_short"
var SPK = "spk"
var BPK = "bpk"


//------------------- Add
const accountInformation = { //Account information
    type: 'table',
    title: 'Account information',
    cols: ['['Initial Balance', 'Wallet Balance', 'Margin Balance', 'Available Margin', 'Used Margin', 'Total Profit', 'Profit Rate'], //List Header
    rows: null //List array   
};

const binanceFundingRate = { //Array of open positions
    type: 'table',
    title: 'Binance USDT-margined position order',
    cols: ['Trading pair', 'Trading direction', 'Opening volume', 'Opening price', 'Position value', 'Leverage', 'Occupied margin', 'Position profit'], //List header
    rows: null //List array
};


initialPrincipalUsdt = null //Initial principal/usdt
revenueUsdt = 0 //Curve


//--------------------------------------
//Account information
//--------------------------------------
function accountInformationfunction() {
    exchange.SetContractType("swap"); // Set to perpetual contract swap / quarter/
    var Currency = exchange.GetCurrency()
    exchange.SetCurrency(Currency) //Switching products accessesUAccount information in base currency
    var account = _C(exchange.GetAccount)

    _CDelay(2000 * 60)
    if (!account) {
        Log("No assets obtained")
        return
    }
    
    if (initialPrincipalUsdt==null ) {
        initialPrincipalUsdt = account.Info.totalWalletBalance //When loading, net value record is the starting balance
        _G("initialPrincipalUsdt", initialPrincipalUsdt) //Retrieve saved data
        if (initialPrincipalUsdt == 0) {
            Log("USDTNo assets in contract")
            return
        }
    }
    /*API 
    "totalInitialMargin": "0.00000000",  // Total required initial margin in USD
    "totalMaintMargin": "0.00000000",  // Total maintenance margin denominated in USD
    "totalWalletBalance": "126.72469206",   // Total account balance denominated in USD
    "totalUnrealizedProfit": "0.00000000",  // Total unrealized P&L of positions in USD
    "totalMarginBalance": "126.72469206",  // Total margin balance in USD
    "totalPositionInitialMargin": "0.00000000",  // Initial margin required for positions denominated in USD (based on the latest mark price))
    "totalOpenOrderInitialMargin": "0.00000000",  // Initial Margin Required for Current USD-Denominated Pending Orders (Based on Latest Mark Price))
    "totalCrossWalletBalance": "126.72469206",  // Whole account balance in USD
    "totalCrossUnPnl": "0.00000000",    // Unrealized gain/loss total of full-position holdings denominated in USD
    "availableBalance": "126.72469206",       // Available balance in USD
    "maxWithdrawAmount": "126.72469206"     // Maximum transferable balance denominated in USD
    */

    InitialBalance = Number(initialPrincipalUsdt)
    WalletBalance = account.Info.totalWalletBalance
    marginBalance = account.Info.totalCrossWalletBalance
    FreeMargin = account.Info.availableBalance
    UsedMargin = account.Info.totalMaintMargin
   
    TotalRevenue = Number(WalletBalance) - Number(InitialBalance)
    Yield1 = TotalRevenue / InitialBalance
    yield1 = Number(Yield1)
    Yield = (yield1 * 100).toFixed(2) + "%"
    //Encapsulated in an array
    revenueUsdt = Number(TotalRevenue)

    accountInformation.rows = [] //Clear
    //'Initial Balance',  'Wallet Balance ',  'Margin balance', 'Available Margin', 'Used margin', 'Total income', 'Yield'
    accountInformation.rows[0] = [InitialBalance, WalletBalance, marginBalance, FreeMargin, UsedMargin, TotalRevenue, Yield]

}

//--------------------------------------
//Array of open positions
//--------------------------------------
function binanceFundingRatefunction() { //Array of open positions
    binanceFundingRate.rows = []
    exchange.SetContractType("swap"); // Set as a perpetual contract, pay attention to coin-based andUSDTPerpetual exists in all base currencies
    var y = 0 //It can be judged even without the product

    for (var i = 0; i < exchanges.length; i++) {
        exchange.SetCurrency(exchanges[i].GetCurrency()) //Switch product
        //-------------------------------------------------------
        var position = _C(exchange.GetPosition) //Get account position information
       // Log("position", position)
        _CDelay(1000 * 2 * 60)
        //Perpetual and non-uniform coin-margined cross-futures contracts are placed in one array. Perpetual contracts are different.
        if (position) {
            for (var iii = 0; iii < position.length; iii++) {
                if (exchange.GetContractType() == position[iii].ContractType) { //Why judge? Because all the positions in the spread contract are grouped together
                    binanceFundingRate.rows[y] = [position[iii].Info.symbol, position[iii].Type == 0 ? "BUY" : "SELL", position[iii].Amount,
                        position[iii].Price, position[iii].Amount * position[iii].Price,
                        position[iii].MarginLevel, position[iii].Margin, position[iii].Profit
                    ]
                    y++
                }
            }
        }

    }

}


//--------------------------------------
//Main Function
//--------------------------------------

function main() {
    // Clear the logs, delete if not needed
    //LogReset(1)

    // Set Precision
    exchange.SetPrecision(QuotePrecision, BasePrecision)

    // Identify futures or spot
    var eType = 0
    var eName = exchange.GetName() //Exchange name, such as:Futures_Binance
    var patt = /Futures_/
    if (patt.test(eName)) { //Determine whether it hasFutures_     For futures trading, set the contract to perpetual  Ct = "swap"
        Log("The added exchange is a futures exchange:", eName, "#FF0000")
        eType = 1
        if (Ct == "") {
            throw "Ct Set contract to empty"
        } else {
            Log(exchange.SetContractType(Ct), "Set Contract:", Ct, "#FF0000")
        }
    } else {
        Log("The added exchange is a spot exchange:", eName, "#32CD32")
    }


    //Test position function
    var position3 = exchange.GetPosition()
    if (position3.length == 0) {
        Log("Robot's first startup,Conducting a thorough check of the exchange", "#33CD33")
        Log(exchange.GetLabel(), "Account information initialization completed: the exchange has no open positions, everything is normal", "#0000FF")
        Log("Robot is ready! !Wait for signal! !", "#0000FF")
    }
    if (position3.length > 0) {
        Log("Robot's first startup,Conducting a thorough check of the exchange", "#33CD33")
        Log(exchange.GetLabel(), "Account information initialization completed:Exchange exception check, there are open positions, Please confirm! ! !,", "Types of held positions", position3.length, "(species)", "Position Quantity:", position3[0].Amount, "(Zhang/Currency)", "Position Direction:", position3[0].Type, "(0represents long order/1represents short order)", "#0000FF")
        Log("Robot is ready! ! Waiting for signal! ! !", "#0000FF")
    }

    var lastMsg = ""
    var position = _C(exchange.GetPosition)
    var acc = _C(exchange.GetAccount)
    //LogProfit(acc.Balance)
    //LogProfit(acc.Balance, '&')
    //LogProfit(acc.Stocks)
    //var acc = exchange.GetAccount
    Log(acc);

    var count = 0 //Record loop count
    if(initialPrincipalUsdt==null){
       initialPrincipalUsdt = _G("initialPrincipalUsdt") //Retrieve saved data
    }


    while (true) {
        var cmd = GetCommand()

        if (!cmd) {
            //Log("Not receivedcmdCommand:", cmd, "#FF0000")
            //continue
        }

        if (cmd) {
            // Detect interactive commands
            Log("Received fromTradingViewAlert signal", cmd, "#32CD32")
            Log("Begin executing this signal loop!", "#32CD32")

            lastMsg = "Command:" + cmd + "Time:" + _D()
            var arr = cmd.split(":")
            if (arr.length != 2) {
                Log("cmdIncorrect Information:", cmd, "(Please confirm whether the open or close position command is correct)", "#FF0000")
                continue
            }

            var action = arr[0]
            var amount = parseFloat(arr[1])
            //var amount = 0.01 //The number of contracts after the equal sign
            //Log(action, amount)
            //Log("Shared in Telegram group asFMZThe first version of the robot code is for learning only. If you need to perfectly connect with the signal broadcast in the Telegram groupTradingViewStrategy or want more qualityTVFor strategies, please contact the group owner18664029094", "#0000FF")
            //Log("WeChat tian-qi-666 or Telegram group //t.me/tq16889 OrBilbilSearch in the video: earnings14500%Detailed usage of the strategy or500UHow the account uses compounding to place fully automated trades", "#FF0000")
            //Log("TradingViewHow to connect the strategy to the inventor(FMZ)Quantitative trading robots? How the inventor determinesTVSignal for Binance orOKEXWaiting for the exchange to perform fully automated opening and closing of trades? ", "#0000FF")
            //Spot processing logic
            if (eType == 0) {
                if (action == BUY) {
                    var buyInfo = IsMarketOrder ? exchange.Buy(-1, amount) : $.Buy(amount)
                    Log("buyInfo:", buyInfo)
                } else if (action == SELL) {
                    var sellInfo = IsMarketOrder ? exchange.Sell(-1, amount) : $.Sell(amount)
                    Log("sellInfo:", sellInfo)
                } else {
                    Log("Not supported by spot exchange!", "#FF0000")
                }
                //Futures processing logic
            } else if (eType == 1) {
                var tradeInfo = null
                var ticker = _C(exchange.GetTicker)

                if (action == LONG) {
                    Log("open long:", amount, "#32CD32")
                    //If what is sent islong:0.01Command, then close short position while executing long order
                    //exchange.SetDirection("closesell")
                    //var tradeInfo1 = IsMarketOrder ? exchange.Buy(-1, amount) : exchange.Buy(ticker.Sell, amount)
                    //exchange.SetDirection("buy")
                    //var tradeInfo2 = IsMarketOrder ? exchange.Buy(-1, amount) : exchange.Buy(ticker.Sell, amount)
                    //tradeInfo = [tradeInfo1, tradeInfo2]                    
                    exchange.SetDirection("buy")
                    tradeInfo = IsMarketOrder ? exchange.Buy(-1, amount) : exchange.Buy(ticker.Sell, amount)
                    Log("This signal has been processed!!! Waiting to receive a new signal!!!", "#0000FF")

                } else if (action == SHORT) {
                    Log("open short:", amount, "#32CD32")
                    //If what is sent isshort:0.01Command, then close long position while executing short order
                    //exchange.SetDirection("closebuy")
                    //var tradeInfo1 = IsMarketOrder ? exchange.Sell(-1, amount) : exchange.Sell(ticker.Buy, amount)
                    //exchange.SetDirection("sell")
                    //var tradeInfo2 = IsMarketOrder ? exchange.Sell(-1, amount) : exchange.Sell(ticker.Buy, amount)
                    //tradeInfo = [tradeInfo1, tradeInfo2]                    
                    exchange.SetDirection("sell")
                    tradeInfo = IsMarketOrder ? exchange.Sell(-1, amount) : exchange.Sell(ticker.Buy, amount)
                    Log("This signal has been processed!!! Waiting to receive a new signal!!!", "#0000FF")

                } else if (action == COVER_LONG) {
                    Log("Close long position:", amount, "#32CD32")

                    //Added judgment on whether there is a position
                    // Retrieve results from the data sequentially
                    var account = _C(exchange.GetAccount)
                    if (!ticker || !account) {
                        Log(exchange.GetLabel(), ":Exception when fetching trading data, skip order for now.", "@")
                        continue
                    }
                    // Get position situation
                    var position = exchange.GetPosition()
                    // if (position_size != 0)
                    // Log(exchanges[i].GetLabel(), "Position quantity of:", position_size)
                    if (position.length == 0) {
                        Log(exchange.GetLabel(), ":No positions, do not close positions.")
                        Log("This signal has been processed!!! Waiting to receive a new signal!!!", "#0000FF")
                        continue

                    }

                    //If what is sent iscover_long:2Instruction: close long positions and close short positions at the same time
                    //exchange.SetDirection("closebuy")
                    //var tradeInfo1 = IsMarketOrder ? exchange.Sell(-1, amount) : exchange.Sell(ticker.Buy, amount)
                    //exchange.SetDirection("closesell")
                    //var tradeInfo2 = IsMarketOrder ? exchange.Buy(-1, amount) : exchange.Buy(ticker.Sell, amount)
                    //tradeInfo = [tradeInfo1, tradeInfo2]                    
                    exchange.SetDirection("closebuy")
                    tradeInfo = IsMarketOrder ? exchange.Sell(-1, amount) : exchange.Sell(ticker.Buy, amount)
                    Log("This signal has been processed!!! Waiting to receive a new signal!!!", "#0000FF")

                } else if (action == COVER_SHORT) {
                    Log("Close short position:", amount, "#32CD32")

                    //Added judgment on whether there is a position
                    // Retrieve results from the data sequentially
                    var account1 = _C(exchange.GetAccount)
                    if (!ticker || !account1) {
                        Log(exchange.GetLabel(), ":Exception when fetching trading data, skip order for now.", "@")
                        continue
                    }
                    // Get position situation
                    var position1 = exchange.GetPosition()
                    // if (position_size != 0)
                    // Log(exchanges[i].GetLabel(), "Position quantity of:", position_size)
                    if (position1.length == 0) {
                        Log(exchange.GetLabel(), ":No positions, do not close positions.")
                        Log("This signal has been processed!!! Waiting to receive a new signal!!!", "#0000FF")
                        continue
                    }

                    //If what is sent iscover_short:0.01Instruction: close long positions and close short positions at the same time
                    //exchange.SetDirection("closebuy")
                    //var tradeInfo1 = IsMarketOrder ? exchange.Sell(-1, amount) : exchange.Sell(ticker.Buy, amount)
                    //exchange.SetDirection("closesell")
                    //var tradeInfo2 = IsMarketOrder ? exchange.Buy(-1, amount) : exchange.Buy(ticker.Sell, amount)
                    //tradeInfo = [tradeInfo1, tradeInfo2]                    
                    exchange.SetDirection("closesell")
                    tradeInfo = IsMarketOrder ? exchange.Buy(-1, amount) : exchange.Buy(ticker.Sell, amount)
                    Log("This signal has been processed!!! Waiting to receive a new signal!!!", "#0000FF")

                } else if (action == SPK) { // Sell to close a long position, sell to open a short position
                    exchange.SetDirection("closebuy")
                    var tradeInfo1 = IsMarketOrder ? exchange.Sell(-1, amount) : exchange.Sell(ticker.Buy, amount)
                    exchange.SetDirection("sell")
                    var tradeInfo2 = IsMarketOrder ? exchange.Sell(-1, amount) : exchange.Sell(ticker.Buy, amount)
                    tradeInfo = [tradeInfo1, tradeInfo2]

                } else if (action == BPK) { // Buy to close a short position, buy to open a long position
                    exchange.SetDirection("closesell")
                    var tradeInfo1 = IsMarketOrder ? exchange.Buy(-1, amount) : exchange.Buy(ticker.Sell, amount)
                    exchange.SetDirection("buy")
                    var tradeInfo2 = IsMarketOrder ? exchange.Buy(-1, amount) : exchange.Buy(ticker.Sell, amount)
                    tradeInfo = [tradeInfo1, tradeInfo2]

                } else {
                    Log("Futures exchange does not support!", "#FF0000")
                }
                if (tradeInfo) {
                    Log("tradeInfo:", tradeInfo)
                }
            } else {
                throw "eType error, eType:" + eType
            }
            acc = _C(exchange.GetAccount)
        }

        /*   //Originally have
        var tbl = {
            type: "table",
            title: "Status Information",
            cols: ["Data"],
            rows: []
        }
        tbl.rows.push([JSON.stringify(acc)])
        LogStatus(_D(), eName, "Last command received:", lastMsg, "\n", "`" + JSON.stringify(tbl) + "`")
       */

        if (count % 100 == 0) {
            //Show positions and pending orders information
            // binanceOrderRate()
            // FirmOfferIncome()
            accountInformationfunction() //Account information
            binanceFundingRatefunction() //Array of open positions

            //Records only once every hour    
            if (count % 600 == 0) {
                LogProfit(revenueUsdt, '&') //Capital Curve
            }
        }


        LogStatus("Last command received:", lastMsg, "\n",
            '\n`' + JSON.stringify("Last update time:" + _D()) + '`\n' +
            '\n`' + JSON.stringify([accountInformation]) + '`\n' +
            '\n`' + JSON.stringify([binanceFundingRate]) + '`\n'
        ); //Column box display


        count++
        _G("initialPrincipalUsdt", initialPrincipalUsdt) //Retrieve saved data
        Sleep(1000)
    }
}
```

> Detail

https://www.fmz.com/strategy/379174

> Last Modified

2022-08-23 10:25:06
