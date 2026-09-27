
> Name

Binance-Perpetual-Dual-Account-Single-Coin-Hedging-YNRUN

> Author

高吸低抛



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Reset|false|Reset historical data|
|MarginLevel|50|Leverage of the trading pair|
|CloseAllOnExit|false|Cancel all positions after the bot stops|


> Source (javascript)

``` javascript
var Stop_loss = 0.8;
//var MarginLevel =100;
var NO_TRADE = false
var Interval =1

var Log_profit_interval = 60;
var update_profit_time = 0;
var update_base_price_time = Date.now();
var assets = {};
//var init_prices = {};
var trade_info = {};

var Version = '0.1.3';
var Success = '#5cb85c'; //Success color
var Danger = '#ff0000'; //Dangerous colors
var Warning = '#f0ad4e'; //Warning color

var accountAssets_0 = []; //Save assets
var accountAssets_1 = []; //Save assets
var Funding_0 = 0;
var Funding_1 = 0;

var Trade_ex = 0;

var exLabel_0 = exchanges[0].GetLabel()
var exLabel_1 = exchanges[1].GetLabel()

var baseApiURL = ""
//baseApiURL = "https://testnet.binancefuture.com"
baseApiURL = "https://fapi.binance.com"

function init() {
    if (Reset) {
        LogReset()
        LogProfitReset()

        _G('init_balance', null)
        _G("WinRateData", null)
        _G('init_prices', null);
        _G("StartTime", null); //Reset start time
        _G("initialAccount_" + exchange.GetLabel(), null); //Reset starting funds
        _G("tradeNumber", null); //Reset number of trades
        _G("tradeVolume", null); //Reset trading volume
        _G("buyNumber", null); //Reset number of long positions
        _G("sellNumber", null); //Reset number of short positions
        _G("totalProfit", null); //Reset print count
        _G("profitNumber", null); //Reset number of profitable trades
        _G("initialAccount_" + exLabel_0 , null);
        _G("initialAccount_" + exLabel_1 , null);
    }

    //Settings BTC_USDT
    exchanges[0].IO("currency", 'BTC_USDT')
    exchanges[1].IO("currency", 'BTC_USDT')


    exchanges[0].SetMarginLevel(MarginLevel)
    exchanges[1].SetMarginLevel(MarginLevel)

    exchanges[0].SetContractType('swap')
    exchanges[1].SetContractType('swap')

    //Set to one-way
    changeToDualSidePosition(false,exchanges[0])
    changeToDualSidePosition(false,exchanges[1])

    //Set to isolated margin mode
    changeMarginTypeToCROSSED(false,"BTCUSDT",exchanges[0])
    changeMarginTypeToCROSSED(false,"BTCUSDT",exchanges[1])


    assets[exLabel_0]={}
    assets[exLabel_0].USDT = {
        unrealised_profit: 0,
        margin: 0,
        margin_balance: 0,
        total_balance: 0,
        leverage: 0,
        update_time: 0,
        margin_ratio: 0,
        init_balance: 0,
        stop_balance: 0,
        short_value: 0,
        long_value: 0,
        profit: 0
    };
    assets[exLabel_0]["BTC"] = {
        amount: 0,
        hold_price: 0,
        value: 0,
        bid_price: 0,
        ask_price: 0,
        btc_price: 0,
        btc_change: 1,
        btc_diff: 0,
        realised_profit: 0,
        margin: 0,
        unrealised_profit: 0,
        leverage: 20,
        positionInitialMargin: 0,
        liquidationPrice: 0
    };

    updateAccount(exchanges[0])


    assets[exLabel_1]={}
    assets[exLabel_1].USDT = {
        unrealised_profit: 0,
        margin: 0,
        margin_balance: 0,
        total_balance: 0,
        leverage: 0,
        update_time: 0,
        margin_ratio: 0,
        init_balance: 0,
        stop_balance: 0,
        short_value: 0,
        long_value: 0,
        profit: 0
    };
    assets[exLabel_1]["BTC"] = {
        amount: 0,
        hold_price: 0,
        value: 0,
        bid_price: 0,
        ask_price: 0,
        btc_price: 0,
        btc_change: 1,
        btc_diff: 0,
        realised_profit: 0,
        margin: 0,
        unrealised_profit: 0,
        leverage: 20,
        positionInitialMargin: 0,
        liquidationPrice: 0
    };
    updateAccount(exchanges[1])

    getExchangeInfo()


   // Log(assets)

}
function getExchangeInfo(){
    var exchange_info = HttpQuery(baseApiURL + '/fapi/v1/exchangeInfo');
    if (!exchange_info) {
        throw 'Unable to connect to Binance network, requires overseas hosting';
    }
    exchange_info = JSON.parse(exchange_info);
    for (var i = 0; i < exchange_info.symbols.length; i++) {
        if (exchange_info.symbols[i].baseAsset =="BTC") {
            trade_info["BTC"] = {
                minQty: parseFloat(exchange_info.symbols[i].filters[1].minQty),
                priceSize: parseInt((Math.log10(1.1 / parseFloat(exchange_info.symbols[i].filters[0].tickSize)))),
                amountSize: parseInt((Math.log10(1.1 / parseFloat(exchange_info.symbols[i].filters[1].stepSize))))
            };
        }
    }
}
function onexit() {
                updateAccount(exchanges[0])
                updateAccount(exchanges[1]); //Update account and positions
                updateTick(); //Market quotation
                //stopLoss(); //stop loss
                //onTick(); //Strategy logic section
                updateStatus(); //Output status bar information
    //cancelCloseAll()
    if(CloseAllOnExit){
      cancelAll("BTC",exchanges[0])
      cancelAll("BTC",exchanges[1])
      closeAll("BTC",exchanges[0])
      closeAll("BTC",exchanges[1])
    }

    Log('exit')
}
function isEmpty(v) { //same with _.isEmpty()
    let type = typeof v;
    if (type === 'undefined') {
        return true;
    }
    if (type === 'boolean') {
        return !v;
    }
    if (v === null) {
        return true;
    }
    if (v === undefined) {
        return true;
    }
    if (v instanceof Array) {
        if (v.length < 1) {
            return true;
        }
    } else if (type === 'string') {
        if (v.length < 1) {
            return true;
        }
        if (v === '0') {
            return true;
        }
    } else if (type === 'object') {
        if (Object.keys(v).length < 1) {
            return true;
        }
    } else if (type === 'number') {
        if (v === 0) {
            return true;
        }
    }
    return false;
}
function changeToDualSidePosition(param = "true",ex = exchange) {
    try {
        if(param == false||param == true) params = "dualSidePosition="+param
        var msg = ex.IO('api', 'GET', '/fapi/v1/positionSide/dual');
        if (!msg) return msg
        if (msg.dualSidePosition != param){

          msg = ex.IO('api', 'POST', '/fapi/v1/positionSide/dual', params);

          if (!msg) return msg
          if (msg.code == -4059) return msg
          if (msg.code != 200) {
              Sleep(10)
              msg = changeToDualSidePosition(param,ex)
          }
        }
        return msg
    } catch (err) {
        Log('changeToDualSidePosition error:' + err);
    }

}
function changeMarginTypeToCROSSED(cross = false,param = "BTCUSDT",ex = exchange) {
    try {
        if(cross == true){
          params = "marginType=CROSSED&symbol=" + param
        }else if(cross == false){
          params = "marginType=ISOLATED&symbol=" + param
        }

        var msg = ex.IO('api', 'POST', '/fapi/v1/marginType', params);
        if (!msg) return msg
        if (msg.code == -4046) return msg
        if (msg.code != 200) {
            Sleep(10)
            msg = changeMarginTypeToCROSSED(cross,param,ex)
        }
        return msg
    } catch (err) {
        Log('changeMarginTypeToCROSSED error:' + err);
    }

}
function getPostion(symbol = "BTC",exchange = exchanges[0]) { //Update account and positions
  try {
    var exLabel=exchange.GetLabel()
    var params =""
    if(!isEmpty(symbol))
        params = "symbol="+symbol+"USDT"
    else
        params = "symbol=BTCUSDT"
    var pos = exchange.IO('api', 'GET', '/fapi/v2/positionRisk',params);
    if (isEmpty(pos)) return;



    //var asset = assets[exLabel]
/*
    var account = exchange.GetAccount();
    var pos = exchange.GetPosition();
    if (account == null || pos == null) {
        Log(115,exchange.GetLabel(),' update account time out');
        return;
    }
    if(exLabel==exLabel_0)
       accountAssets_0 = account.Info.assets;
    else
       accountAssets_1 = account.Info.assets;

    assets[exLabel].USDT.update_time = Date.now();
    //for (var i = 0; i < trade_symbols.length; i++) {
        assets[exLabel]["BTC"].margin = 0;
        assets[exLabel]["BTC"].unrealised_profit = 0;
        assets[exLabel]["BTC"].hold_price = 0;
        assets[exLabel]["BTC"].amount = 0;
    //}
    for (var j = 0; j < account.Info.positions.length; j++) {
        if (account.Info.positions[j].positionSide == 'BOTH') {
            var pair = account.Info.positions[j].symbol;
            var coin = pair.slice(0, pair.length - 4);
            if ("BTC" != coin) {
                continue;
            }
            assets[exLabel][coin].margin = parseFloat(account.Info.positions[j].initialMargin) + parseFloat(account.Info.positions[j].maintMargin);
            assets[exLabel][coin].unrealised_profit = parseFloat(account.Info.positions[j].unrealizedProfit);
            assets[exLabel][coin].positionInitialMargin = parseFloat(account.Info.positions[j].positionInitialMargin);//Initial margin of the position
            assets[exLabel][coin].leverage = account.Info.positions[j].leverage;
        }
    }
    assets[exLabel].USDT.margin = _N(parseFloat(account.Info.totalInitialMargin) + parseFloat(account.Info.totalMaintMargin), 2); //Total initial margin (ignore if using isolated margin) + total maintenance margin
    assets[exLabel].USDT.margin_balance = _N(parseFloat(account.Info.totalMarginBalance), 2); //Total margin balance (excluding occupied margin) = Total wallet account balance + Unrealized P&L
    assets[exLabel].USDT.total_balance = _N(parseFloat(account.Info.totalWalletBalance), 2);//Total account balance (excluding unrealized profits and losses))
    //assets[exLabel].USDT.total_balance = _N(parseFloat(account.Info.totalWalletBalance), 2);//Total account balance

    assets[exLabel].USDT.unrealised_profit = _N(parseFloat(account.Info.totalUnrealizedProfit), 2); //Total unrealized P&L of positions
    assets[exLabel].USDT.margin_ratio = (account.Info.totalMaintMargin / account.Info.totalMarginBalance * 100);// Total maintenance margin / total margin balance

    if(exLabel==exLabel_0)
        assets[exLabel].USDT.init_balance = parseFloat(FirstAccount(exchanges[0]).Info.totalWalletBalance);
    else
        assets[exLabel].USDT.init_balance = parseFloat(FirstAccount(exchanges[1]).Info.totalWalletBalance);
    assets[exLabel].USDT.profit = _N(assets[exLabel].USDT.margin_balance - assets[exLabel].USDT.init_balance, 2);//Total margin balance - initial account total balance
    assets[exLabel].USDT.stop_balance = _N(Stop_loss * assets[exLabel].USDT.init_balance, 2);
    assets[exLabel].USDT.leverage = _N(assets[exLabel].USDT.margin / assets[exLabel].USDT.total_balance, 2);//  (Total initial margin (ignore isolated margin + total maintenance margin) / total account balance

    pos = JSON.parse(exchange.GetRawJSON());
*/
    if (pos.length > 0) {
        for (var k = 0; k < pos.length; k++) {
            var pair = pos[k].symbol;
            var coin = pair.slice(0, pair.length - 4);
            if (symbol != coin) {
                continue;
            }
            if (pos[k].positionSide != 'BOTH') {
                continue;
            }
            assets[exLabel][coin].hold_price = parseFloat(pos[k].entryPrice);
            assets[exLabel][coin].amount = parseFloat(pos[k].positionAmt);
            assets[exLabel][coin].unrealised_profit = parseFloat(pos[k].unRealizedProfit);
            assets[exLabel][coin].liquidationPrice = parseFloat(pos[k].liquidationPrice);
            //zyn add
            assets[exLabel][coin].markPrice = parseFloat(pos[k].markPrice);
            assets[exLabel][coin].leverage = parseFloat(pos[k].leverage);
            assets[exLabel][coin].positionSide = pos[k].positionSide;
            //zyn add end
            assets[exLabel][coin].marginType = pos[k].marginType;
        }
    }

    //return assets[exLabel];
  } catch (err) {
     Log('getPostion error:' + err);
  }
}
function updateAccount(exchange = exchanges[0]) { //Update account and positions
  try {
    var exLabel=exchange.GetLabel()
    //var asset = assets[exLabel]
    var account = exchange.GetAccount();
    var pos = exchange.GetPosition();

    //zyn add
    //if(isEmpty(pos)) getPostion()
    //zyn add end


    if (account == null || pos == null) {
        Log(115,exchange.GetLabel(),' update account time out');
        return;
    }
    if(exLabel==exLabel_0)
       accountAssets_0 = account.Info.assets;
    else
       accountAssets_1 = account.Info.assets;

    assets[exLabel].USDT.update_time = Date.now();
    /*
    for (var i = 0; i < trade_symbols.length; i++) {
        assets[exLabel]["BTC"].margin = 0;
        assets[exLabel]["BTC"].unrealised_profit = 0;
        assets[exLabel]["BTC"].hold_price = 0;
        assets[exLabel]["BTC"].amount = 0;
    }
    */
    for (var j = 0; j < account.Info.positions.length; j++) {
        if (account.Info.positions[j].positionSide == 'BOTH') {
            var pair = account.Info.positions[j].symbol;
            var coin = pair.slice(0, pair.length - 4);
            if ("BTC" != coin) {
                continue;
            }
            assets[exLabel][coin].margin = parseFloat(account.Info.positions[j].initialMargin) + parseFloat(account.Info.positions[j].maintMargin);
            assets[exLabel][coin].unrealised_profit = parseFloat(account.Info.positions[j].unrealizedProfit);
            assets[exLabel][coin].positionInitialMargin = parseFloat(account.Info.positions[j].positionInitialMargin);//Initial margin of the position
            assets[exLabel][coin].leverage = account.Info.positions[j].leverage;
            //zyn add
            assets[exLabel][coin].hold_price = account.Info.positions[j].entryPrice;
            assets[exLabel][coin].positionSide = account.Info.positions[j].positionSide;
            //zyn add end
        }
    }
    assets[exLabel].USDT.margin = _N(parseFloat(account.Info.totalInitialMargin) + parseFloat(account.Info.totalMaintMargin), 2); //Total initial margin (ignore if using isolated margin) + total maintenance margin
    assets[exLabel].USDT.margin_balance = _N(parseFloat(account.Info.totalMarginBalance), 2); //Total margin balance (excluding occupied margin) = Total wallet account balance + Unrealized P&L
    assets[exLabel].USDT.total_balance = _N(parseFloat(account.Info.totalWalletBalance), 2);//Total account balance (excluding unrealized profits and losses))
    //assets[exLabel].USDT.total_balance = _N(parseFloat(account.Info.totalWalletBalance), 2);//Total account balance

    assets[exLabel].USDT.unrealised_profit = _N(parseFloat(account.Info.totalUnrealizedProfit), 2); //Total unrealized P&L of positions
    assets[exLabel].USDT.margin_ratio = (account.Info.totalMaintMargin / account.Info.totalMarginBalance * 100);// Total maintenance margin / total margin balance
/*
    if (assets[exLabel].USDT.init_balance == 0) {
        if (_G('init_balance')) {
            assets[exLabel].USDT.init_balance = _N(_G('init_balance'), 2);
        } else {
            assets[exLabel].USDT.init_balance = assets[exLabel].USDT.total_balance; // Total account balance
            _G('init_balance', assets[exLabel].USDT.init_balance);
        }
    }
*/
    if(exLabel==exLabel_0)
        assets[exLabel].USDT.init_balance = parseFloat(FirstAccount(exchanges[0]).Info.totalWalletBalance);
    else
        assets[exLabel].USDT.init_balance = parseFloat(FirstAccount(exchanges[1]).Info.totalWalletBalance);
    assets[exLabel].USDT.profit = _N(assets[exLabel].USDT.margin_balance - assets[exLabel].USDT.init_balance, 2);//Total margin balance - initial account total balance
    assets[exLabel].USDT.stop_balance = _N(Stop_loss * assets[exLabel].USDT.init_balance, 2);
    assets[exLabel].USDT.leverage = _N(assets[exLabel].USDT.margin / assets[exLabel].USDT.total_balance, 2);//  (Total initial margin (ignore isolated margin + total maintenance margin) / total account balance

    pos = JSON.parse(exchange.GetRawJSON());


    if (pos.length > 0) {
        for (var k = 0; k < pos.length; k++) {
            var pair = pos[k].symbol;
            var coin = pair.slice(0, pair.length - 4);
            if ("BTC" != coin) {
                continue;
            }
            if (pos[k].positionSide != 'BOTH') {
                continue;
            }
            assets[exLabel][coin].hold_price = parseFloat(pos[k].entryPrice);
            assets[exLabel][coin].amount = parseFloat(pos[k].positionAmt);
            assets[exLabel][coin].unrealised_profit = parseFloat(pos[k].unRealizedProfit);
            assets[exLabel][coin].liquidationPrice = parseFloat(pos[k].liquidationPrice);
            //zyn add
            assets[exLabel][coin].markPrice = parseFloat(pos[k].markPrice);
            assets[exLabel][coin].leverage = parseFloat(pos[k].leverage);
            assets[exLabel][coin].positionSide = pos[k].positionSide;
            //zyn add end
            assets[exLabel][coin].marginType = pos[k].marginType;
        }
    }
    //return assets[exLabel];
  } catch (err) {
     Log('updateAccount error:' + err);
  }
}
function updateTick() { //Update Quotes


    var ticker = HttpQuery(baseApiURL + '/fapi/v1/ticker/bookTicker');
    try {
        ticker = JSON.parse(ticker);
    } catch (e) {
        Log('get ticker time out');
        return;
    }
    //assets.USDT.short_value = 0;
    //assets.USDT.long_value = 0;
    for (var i = 0; i < ticker.length; i++) {
        var pair = ticker[i].symbol;
        var coin = pair.slice(0, pair.length - 4);
        if (coin !="BTC") {
            continue;
        }
        trade_info[coin].ask_price = parseFloat(ticker[i].askPrice);
        trade_info[coin].bid_price = parseFloat(ticker[i].bidPrice);

        assets[exLabel_0][coin].ask_price = parseFloat(ticker[i].askPrice);
        assets[exLabel_0][coin].bid_price = parseFloat(ticker[i].bidPrice);
        assets[exLabel_0][coin].ask_value = _N(assets[exLabel_0][coin].amount * assets[exLabel_0][coin].ask_price, 2);
        assets[exLabel_0][coin].bid_value = _N(assets[exLabel_0][coin].amount * assets[exLabel_0][coin].bid_price, 2);

        assets[exLabel_1][coin].ask_price = parseFloat(ticker[i].askPrice);
        assets[exLabel_1][coin].bid_price = parseFloat(ticker[i].bidPrice);
        assets[exLabel_1][coin].ask_value = _N(assets[exLabel_1][coin].amount * assets[exLabel_1][coin].ask_price, 2);
        assets[exLabel_1][coin].bid_value = _N(assets[exLabel_1][coin].amount * assets[exLabel_1][coin].bid_price, 2);

        //trade_info[coin].ask_value = _N(assets[coin].amount * trade_info[coin].ask_price, 2);
        //trade_info[coin].bid_value = _N(assets[coin].amount * trade_info[coin].bid_price, 2);
        //if (trade_symbols.indexOf(coin) < 0) {
        //    continue;
        //}
        //if (assets[coin].amount < 0) {
        //    assets.USDT.short_value += Math.abs((assets[coin].ask_value + assets[coin].bid_value) / 2);
        //} else {
        //    assets.USDT.long_value += Math.abs((assets[coin].ask_value + assets[coin].bid_value) / 2);
        //}
        //assets.USDT.short_value = _N(assets.USDT.short_value, 0);
        //assets.USDT.long_value = _N(assets.USDT.long_value, 0);
    }
    //updateIndex();
    //for (var i = 0; i < trade_symbols.length; i++) {
    //    assets[trade_symbols[i]].btc_diff = _N(assets[trade_symbols[i]].btc_change - index, 4);
        //zyn add
        //btcDiffIndex.push(assets[trade_symbols[i]].btc_diff)
        //zyn add end
    //}
    //zyn add
    //btcDiffIndex.sort((a,b)=>b-a)
    //Log(295," btcDiffIndex=",btcDiffIndex)
    //zyn add end
}
function cancelAll(symbol,exchange = exchanges[0]) {
  try {
          //updateAccount();
          //updateTick();
              var orders = _C(exchange.GetOrders);
              for (var i = 0; i < orders.length; i++) {
                if(orders[i].Info.symbol!=symbol+"USDT") continue;
                exchange.CancelOrder(orders[i].Id)

                Log(502,exchange.GetLabel()," Cancel all",symbol,"Order orderId: ", orders[i].Id);

              }

  } catch (err) {
     Log('closeAll error:' + err);
  }
}
function cancelAllOrders(symbol,exchange = exchanges[0]) {
  try {
          //updateAccount();
          //updateTick();
          return exchange.IO('api', 'DELETE', '/fapi/v1/allOpenOrders', 'symbol=' + symbol)

  } catch (err) {
     Log('cancelAllOrders error:' + err);
  }
}

function closeAll(symbol,exchange = exchanges[0]) {
  try {
          updateAccount(exchange);
          updateTick();
          //var f = assets[symbol].amount < 0 ? 'Buy' : 'Sell';
        if(assets[exchange.GetLabel()][symbol].amount!=0){
          var dirction = assets[exchange.GetLabel()][symbol].amount < 0 ? 'buy' : 'sell';
          var f = dirction == 'buy' ? 'Buy' : 'Sell';
          exchange.IO("currency", symbol + '_' + 'USDT');
          exchange.SetContractType('swap');
          exchange.SetDirection(dirction);
          exchange.SetMarginLevel(MarginLevel)
          var id=exchange[f](-1, Math.abs(assets[exchange.GetLabel()][symbol].amount), symbol);
          if (id) {
              exchange.CancelOrder(id); //Order will be canceled immediately

              Log(502,exchange.GetLabel()," ",symbol," Position has been closed at market price(orderId:",id,")")
          }
        }

        if((assets[exchange.GetLabel()][symbol].amount!=0 && id) ||
            assets[exchange.GetLabel()][symbol].amount==0){
              var orders = _C(exchange.GetOrders);
              for (var i = 0; i < orders.length; i++) {
                if(orders[i].Info.symbol!=symbol+"USDT") continue;
                exchange.CancelOrder(orders[i].Id)

                Log(502,exchange.GetLabel()," Cancel all",symbol,"Stop Loss and Take Profit Order orderId: ", orders[i].Id);

              }
        }
  } catch (err) {
     Log('closeAll error:' + err);
  }
}
function makeOrder(Order = [],exchange = exchanges=[0]) { //Input list or array
    try {
        exchange.SetContractType('swap')
        /*
        var Order = {"symbol":"BTCUSDT", "side":"BUY" , "positionSide":"LONG" , "type":"MARKET", "quantity":0.001}
        */
        var marketOrder = false

        if (Array.isArray(Order)) {
            Order = Order[0]
        }
        if (Object.keys(Order).length < 4) return Log("makeOrderThe function places an order. The minimum number of parameters in the order is4,Cannot be ", Object.keys(Order).length)

        if (Order.type == "MARKET") marketOrder = true

        //Log("Order=",Order)

        var theOrder = {}
        theOrder = exchange.IO('api', 'POST', '/fapi/v1/order', "", JSON.stringify(Order)); //Return list  Object, not array

        Log(400,"makeOrder Order=",Order," => orderId:",theOrder.orderId)

        if (Object.keys(theOrder).length == 0) return {}
        /*
                    var params = []
                    if(!Array.isArray(Order)) {
                       params.push(Order)
                       Order = params
                       params = []
                    }
                    if(Order.length!=1) return Log("makeOrderMaximum order quantity for function1,Cannot be ",Order.length)

                    for(var key in Order[0]) {
                         if(key=="type"&&Order[0][key]=="MARKET"){
                            //symbol = Order[0].symbol
                            marketOrder =true
                         }
                         params.push(key+"="+Order[0][key]);
                    }
                    params = params.join("&")
                    //Log(params)
                    var theOrder = exchange.IO('api', 'POST', '/fapi/v1/order',params); //Return list  Object, not array
        */
        if (marketOrder) {
            Log(389," theOrder=",theOrder)
            theOrder = waitOrder(theOrder)
        }
        return theOrder //Return list Object, not array
    } catch (err) {
        Log('makeOrder error:' + err);
    }

}
function waitOrder(theOrder = "",exchange =  exchanges[0]) { //Input List or ID   //does not have to be passed in symbol trading pair  //Only wait for status change, do not place a new order
    try {
        if (!theOrder) return Log("waitOrderFunction parameter attributes must includeId,Cannot be ", theOrder)
        if (Array.isArray(theOrder)) theOrder = theOrder[0]
        if (typeof theOrder == "string" || typeof theOrder == "number") {
            theOrder = exchange.GetOrder(theOrder) //Return List
            theOrder = theOrder.Info
        }
        var j = 11
        while (--j) {
            if (theOrder.status != "NEW") break;

            //Log((11-j)," Wait 100ms for OrderID:",theOrder.orderId ," status=",theOrders[i].status)

            Sleep(100)

            //theOrder = GetOrder(theOrder.orderId)
            //theOrder = theOrder.Info

            theOrder = getAllOrders("symbol=" + theOrder.symbol + "&limit=1&orderId=" + theOrder.orderId) //Return array
            theOrder = theOrder[0]

            Log(420, " ", (11 - j), " waitOrder= OrderId:", theOrder.orderId, " (", theOrder.status, ")", " (", theOrder.timeInForce, ")")

            //Log("theOrder=",theOrder," !theOrder=",!theOrder)

            if (!theOrder) break;
            //return theOrder
        }
        return theOrder //output List
    } catch (err) {
        Log(429,'waitOrder error:' + err);
    }
}
function FirstAccount(exchange = exchanges[0]) {
    var key = "initialAccount_" + exchange.GetLabel();
    var initialAccount = _G(key);
    if (initialAccount == null) {
        initialAccount = exchange.GetAccount();
        _G(key, initialAccount);
    }
    return initialAccount;
}
function StartTime() {
    var StartTime = _G("StartTime");
    if (StartTime == null) {
        StartTime = _D();
        _G("StartTime", StartTime);
    }
    return StartTime;
}

function RuningTime() {
    var ret = {};
    var dateBegin = new Date(StartTime());
    var dateEnd = new Date(_D());
    var dateDiff = dateEnd.getTime() - dateBegin.getTime();
    var dayDiff = Math.floor(dateDiff / (24 * 3600 * 1000));
    var leave1 = dateDiff % (24 * 3600 * 1000);
    var hours = Math.floor(leave1 / (3600 * 1000));
    var leave2 = leave1 % (3600 * 1000);
    var minutes = Math.floor(leave2 / (60 * 1000));
    ret.dayDiff = dayDiff;
    ret.hours = hours;
    ret.minutes = minutes;
    ret.str = "Running time: " + dayDiff + " Sky/Heaven " + hours + " Hour " + minutes + " Minute";
    return ret;
}
function AppendedStatus() {
    var accountTable = {
        type: "table",
        title: "Profit statistics",
        cols: ["Exchange", "Initial Funds", "Existing Funds", "Margin Balance", "Used Margin", "Margin Ratio", "Stop Loss", "Total Profit", "Estimated Annualized", "Estimated Monthly", "Average Daily"],
        rows: []
    };
    var feeTable = {
        type: 'table',
        title: 'Trading statistics',
        cols: ["Strategy index", 'Number of transactions', 'Number of longs', 'Number of shorts', 'Estimated winning rate', 'Estimated transaction volume', 'Estimated handling fee', "Unrealized profit", 'Total position value', 'Total long value', 'Total short value''],
        rows: []
    };
    var runday = RunTime.dayDiff;
    if (runday == 0) {
        runday = 1;
    }
    if (Funding_0 == 0) {
        Funding_0 = parseFloat(FirstAccount(exchanges[0]).Info.totalWalletBalance); // Initial total account balance
    }
    if (Funding_1 == 0) {
        Funding_1 = parseFloat(FirstAccount(exchanges[1]).Info.totalWalletBalance); // Initial total account balance
    }
    var profitColors_0 = Danger;
    var profitColors_1 = Danger;
    var totalProfit_0 = assets[exLabel_0].USDT.total_balance - Funding_0; //Total profit
    var totalProfit_1 = assets[exLabel_1].USDT.total_balance - Funding_1; //Total profit
    if (totalProfit_0 > 0) {
        profitColors_0 = Success;
    }
    if (totalProfit_1 > 0) {
        profitColors_1 = Success;
    }
    var dayProfit_0 = totalProfit_0 / runday; //Daily profit
    var dayProfit_1 = totalProfit_1 / runday; //Daily profit
    var dayRate_0 = dayProfit_0 / Funding_0 * 100;
    var dayRate_1 = dayProfit_1 / Funding_0 * 100;
    accountTable.rows.push([
        exLabel_0,
        '$' + _N(Funding_0, 2), // Initial total account balance
        '$' + assets[exLabel_0].USDT.total_balance, // Total account balance
        '$' + assets[exLabel_0].USDT.margin_balance,//Total margin balance
        '$' + assets[exLabel_0].USDT.margin,//Total initial margin (ignore if using isolated margin) + total maintenance margin
        _N(assets[exLabel_0].USDT.margin_ratio, 2) + '%',// Total maintenance margin / total margin balance
        _N(assets[exLabel_0].USDT.stop_balance, 2) + Danger,
        _N(totalProfit_0 / Funding_0 * 100, 2) + "% = $" + _N(totalProfit_0, 2) + (profitColors_0),
        _N(dayRate_0 * 365, 2) + "% = $" + _N(dayProfit_0 * 365, 2) + (profitColors_0),
        _N(dayRate_0 * 30, 2) + "% = $" + _N(dayProfit_0 * 30, 2) + (profitColors_0),
        _N(dayRate_0, 2) + "% = $" + _N(dayProfit_0, 2) + (profitColors_0)
    ]);
    accountTable.rows.push([
        exLabel_1,
        '$' + _N(Funding_1, 2), // Initial total account balance
        '$' + assets[exLabel_1].USDT.total_balance, // Total account balance
        '$' + assets[exLabel_1].USDT.margin_balance,//Total margin balance
        '$' + assets[exLabel_1].USDT.margin,//Total initial margin (ignore if using isolated margin) + total maintenance margin
        _N(assets[exLabel_1].USDT.margin_ratio, 2) + '%',// Total maintenance margin / total margin balance
        _N(assets[exLabel_1].USDT.stop_balance, 2) + Danger,
        _N(totalProfit_1 / Funding_1 * 100, 2) + "% = $" + _N(totalProfit_1, 2) + (profitColors_1),
        _N(dayRate_1 * 365, 2) + "% = $" + _N(dayProfit_1 * 365, 2) + (profitColors_1),
        _N(dayRate_1 * 30, 2) + "% = $" + _N(dayProfit_1 * 30, 2) + (profitColors_1),
        _N(dayRate_1, 2) + "% = $" + _N(dayProfit_1, 2) + (profitColors_1)
    ]);
/*
    var vloume = _G("tradeVolume") ? _G("tradeVolume") : 0;
    feeTable.rows.push([
        exLabel_0, //Index
        _G("tradeNumber") ? _G("tradeNumber") : 0, //Number of Trades
        _G("buyNumber") ? _G("buyNumber") : 0, //Number of long trades
        _G("sellNumber") ? _G("sellNumber") : 0, //Number of short trades
        _N(_G("profitNumber") / _G("totalProfit") * 100, 2) + '%', //Win rate
        '$' + _N(vloume, 2) + ' ≈ ฿' + _N(vloume / ((assets.BTC.bid_price + assets.BTC.ask_price) / 2), 6), //Transaction amount
        '$' + _N(vloume * (SelfFee / 100), 4), //trading fee
        '$' + _N(assets.USDT.unrealised_profit, 2) + (assets.USDT.unrealised_profit >= 0 ? Success : Danger),//Total unrealized P&L of positions account.Info.totalUnrealizedProfit
        '$' + _N(TotalLong + Math.abs(TotalShort), 2), //Total value of positions
        '$' + _N(TotalLong, 2) + Success, //Total value of long trades
        '$' + _N(Math.abs(TotalShort), 2) + Danger, //Total value of short trades
    ]);
*/
    var assetTable = {
        type: 'table',
        title: 'Account asset information',
        cols: ['Exchange', 'Asset Name', 'Initial Margin', 'Maintenance Margin', 'Margin Balance', 'Maximum Withdrawal Amount', 'Starting Margin for Pending Orders', 'Starting Margin for Positions', 'Unrealized Profit and Loss for Positions', 'Account Balance'],
        rows: []
    };
    for (var i = 0; i < accountAssets_0.length; i++) {
        var acc = accountAssets_0[i];
        assetTable.rows.push([
            exLabel_0,
            acc.asset,
            acc.initialMargin,// Initial Margin
            acc.maintMargin,// Maintenance margin
            acc.marginBalance,//Margin balance
            acc.maxWithdrawAmount,//Maximum withdrawable amount
            acc.openOrderInitialMargin,//Order initial margin
            acc.positionInitialMargin,//Initial margin of the position
            acc.unrealizedProfit,//Unrealized P&L of positions
            acc.walletBalance //Account balance
        ]);
    }
    for (var i = 0; i < accountAssets_1.length; i++) {
        var acc = accountAssets_1[i];
        assetTable.rows.push([
            exLabel_1,
            acc.asset,
            acc.initialMargin,// Initial Margin
            acc.maintMargin,// Maintenance margin
            acc.marginBalance,//Margin balance
            acc.maxWithdrawAmount,//Maximum withdrawable amount
            acc.openOrderInitialMargin,//Order initial margin
            acc.positionInitialMargin,//Initial margin of the position
            acc.unrealizedProfit,//Unrealized P&L of positions
            acc.walletBalance //Account balance
        ]);
    }
/*
    var indexTable = {
        type: 'table',
        title: 'Coin index information',
        cols: ['Number', 'Minimum amount', 'Currency', 'Current price', 'BTC pricing', 'Initial BTC pricing', 'BTC pricing change (%)', 'Coin group', 'Group number', 'Deviation from average (%)', 'Max(%)', 'Number of transactions', 'Number of shorts', 'Number of longs', 'Estimated winning rate'],
        rows: []
    };
    for (var i = 0; i < symbols.length; i++) {
        var price = _N((assets[symbols[i]].ask_price + assets[symbols[i]].bid_price) / 2, trade_info[symbols[i]].priceSize);
        if (symbols.indexOf(symbols[i]) < 0) {
            indexTable.rows.push([i + 1, symbols[i], price, assets[symbols[i]].btc_price,0, _N((assets[symbols[i]].btc_change-1) * 100), _N(100 * assets[symbols[i]].btc_diff,2), 0, 0, 0, '0%']);
        } else {
            var rateData = _G("WinRateData");
            //zyn add
            init_prices = _G('init_prices');

            var symbolText=""
            var symbolNum=0
            if(symbols[i] in highIndex){
              // if(i==highIndex[symbols[i]]){
                 //symbolText= "[High]"+"-"+highIndex[symbols[i]]+Danger
                 symbolText= "[High]"+Danger
                 symbolNum=highIndex[symbols[i]]
              // }
            }else if(symbols[i] in midIndex){
              // if(i==midIndex[symbols[i]]){
                 //symbolText= "[Mid]"+"-"+midIndex[symbols[i]]+Success
                 symbolText= "[Mid]"+Success
                 symbolNum=midIndex[symbols[i]]
              // }
            }else if(symbols[i] in lowIndex){
              // if(i==lowIndex[symbols[i]]){
                 //symbolText= "[Low]"+"-"+lowIndex[symbols[i]]+Danger
                 symbolText= "[Low]"+Danger
                 symbolNum=lowIndex[symbols[i]]
              // }
            }else if(symbols[i] in nullIndex){
                 symbolText= "[NULL]"
                 symbolNum=nullIndex[symbols[i]]
            }else{
                 symbolText= "[Other]"
            }

            //zyn add end
            var winRate = _N(rateData[symbols[i]].profitNumber / rateData[symbols[i]].totalProfit * 100, 2);
            indexTable.rows.push([
                (i + 1), //'Number'
                _N(trade_info[symbols[i]].minQty * price,2),//Minimum trading amount
                symbols[i] + Warning, //Coin information
                price, //Current price
                _N(assets[symbols[i]].btc_price, 6), //BTCPricing
                //zyn add
                _N(init_prices[symbols[i]],6), //Initial BTC valuation
                _N((assets[symbols[i]].btc_change-1) * 100),//BTCPrice change(%)
                //zyn add end
                //_N((1 - assets[symbols[i]].btc_change) * 100),//BTCPrice change(%)
                symbolText,
                symbolNum,
                _N(100 * assets[symbols[i]].btc_diff,2) + (assets[symbols[i]].btc_diff >= 0 ? Success : Danger),//Deviation from average(%)
                100*maxDiff[symbols[i]]+"/"+100*minDiff[symbols[i]],
                rateData[symbols[i]].tradeNumber,//Number of Trades
                rateData[symbols[i]].sellNumber,//Number of short trades
                rateData[symbols[i]].buyNumber,//Number of long trades
                (rateData[symbols[i]].profitNumber > 0 && rateData[symbols[i]].totalProfit > 0 ? winRate : '0') + '%' + (winRate >= 50 ? Success : Danger), //Win rate
            ]);
        }
    }
*/
    var retData = {};
    //retData.upTable = RunTime.str + '\n' + "Last Update: " + _D() + '\n' + 'Version:' + Version + '\n' + '`' + JSON.stringify([accountTable, assetTable]) + '`\n' + '`' + JSON.stringify(feeTable) + '`\n';
    retData.upTable = RunTime.str + '\n' + "Last Update: " + _D() + '\n' + 'Version:' + Version + '\n' + '`' + JSON.stringify([accountTable, assetTable]) + '`\n' ;
    //retData.indexTable = indexTable;
    return retData;
}

function updateStatus() { //Status bar information
    //updateFundingRate()

    var table = {
        type: 'table',
        title: 'Trading pair information',
        //cols: ['Number', '[Mode][Multiples]','Rate%', 'Currency','Currency group','Group number','Deviation from average(%)','Max(%)', 'Direction', 'Quantity', 'Position price', 'Current price', 'Liquidation price', 'Additional required for forced liquidation', 'Position Value', 'Margin', 'Unrealized profit and loss', 'Surrender'],
        cols: ['Exchange', '[Mode][Multiple]', 'Currency', 'Direction', 'Quantity', 'Position price', 'Current price', 'Liquidation price', 'Liquidation still required', 'Position value', 'Margin', 'Unrealized profit and loss', 'Surrender''],
        rows: []
    };
    //TotalLong = 0;
    //TotalShort = 0;
    //for (var i = 0; i < symbols.length; i++) {
        var symbol ="BTC"
        var direction = 'Short position';
        var margin = direction;
        if (assets[exLabel_0][symbol].amount != 0) {
            direction = assets[exLabel_0][symbol].amount > 0 ? 'go long' + Success : 'go short' + Danger;
            margin = (assets[exLabel_0][symbol].marginType == 'cross' ? 'Cross margin : Isolated margin');
        }

        var price = _N((assets[exLabel_0][symbol].ask_price + assets[exLabel_0][symbol].bid_price) / 2, trade_info[symbol].priceSize);
        var value = _N((assets[exLabel_0][symbol].ask_value + assets[exLabel_0][symbol].bid_value) / 2, 2);

        /*
        if (value != 0) {
            if (value > 0) {
                TotalLong += value;
            } else {
                TotalShort += value;
            }
        }
        */

        // var rateData = _G("WinRateData");
        //zyn add

        /*
        var symbolText=""
        var symbolNum=0
        if(symbol in highIndex){
          // if(i==highIndex[symbol]){
             //symbolText= "[High]"+"-"+highIndex[symbol]+Danger
             symbolText= "[High]"+Danger
             symbolNum=highIndex[symbol]
          // }
        }else if(symbol in midIndex){
          // if(i==midIndex[symbol]){
             //symbolText= "[Mid]"+"-"+midIndex[symbol]+Success
             symbolText= "[Mid]"+Success
             symbolNum=midIndex[symbol]
          // }
        }else if(symbol in lowIndex){
          // if(i==lowIndex[symbol]){
             //symbolText= "[Low]"+"-"+lowIndex[symbol]+Danger
             symbolText= "[Low]"+Danger
             symbolNum=lowIndex[symbol]
          // }
        }else if(symbol in nullIndex){
             symbolText= "[NULL]"
             symbolNum=nullIndex[symbol]
        }else{
             symbolText= "[Other]"
        }
        */

        //Forced liquidation spread
        liquidationToMarkPrice = 0
        if(assets[exLabel_0][symbol].amount < 0)
           liquidationToMarkPrice = assets[exLabel_0][symbol].liquidationPrice == 0 ? '0' : "↑" + _N(assets[exLabel_0][symbol].liquidationPrice - assets[exLabel_0][symbol].markPrice, trade_info[symbol].priceSize) + '$' + ' ≈ ' + _N((assets[exLabel_0][symbol].liquidationPrice - assets[exLabel_0][symbol].markPrice) / assets[exLabel_0][symbol].markPrice * 100, 2) + '%' + Warning  //Forced liquidation spread

        if(assets[exLabel_0][symbol].amount > 0)
           liquidationToMarkPrice = assets[exLabel_0][symbol].liquidationPrice == 0 ? '0' : "↓" + _N(assets[exLabel_0][symbol].markPrice - assets[exLabel_0][symbol].liquidationPrice, trade_info[symbol].priceSize) + '$' + ' ≈ ' + _N((assets[exLabel_0][symbol].markPrice - assets[exLabel_0][symbol].liquidationPrice) / assets[exLabel_0][symbol].markPrice * 100, 2) + '%' + Warning //Forced liquidation spread


        //zyn add end
        var infoList = [
            exLabel_0,
            "[" + margin + "] [" + assets[exLabel_0][symbol].leverage + 'x] ',
            //_N(100 * assets[exLabel_0][symbol].fundingRate,3), //Rate%
            symbol,
            //symbolText,
            //symbolNum,
            //_N(100 * assets[exLabel_0][symbol].btc_diff,2) + (assets[exLabel_0][symbol].btc_diff >= 0 ? Success : Danger),//Deviation from average(%)
            //100*maxDiff[symbol]+"/"+100*minDiff[symbol],
            direction,
            Math.abs(assets[exLabel_0][symbol].amount),
            assets[exLabel_0][symbol].hold_price,
            price,
            assets[exLabel_0][symbol].liquidationPrice, //Forced liquidation price
            //assets[exLabel_0][symbol].liquidationPrice == 0 ? '0' : '$' + _N(assets[exLabel_0][symbol].liquidationPrice - price, 5) + ' ≈ ' + _N(assets[exLabel_0][symbol].liquidationPrice / price * 100, 2) + '%' + Warning, //Forced liquidation price
            liquidationToMarkPrice,//Forced liquidation spread
            Math.abs(value),
            _N(assets[exLabel_0][symbol].positionInitialMargin, 2),
            // assets[exLabel_0][symbol].btc_diff,
            _N(assets[exLabel_0][symbol].unrealised_profit, 3) + (assets[exLabel_0][symbol].unrealised_profit >= 0 ? Success : Danger),//Unrealized profit and loss
            // (rateData[symbol].profitNumber > 0 && rateData[symbol].totalProfit > 0 ? _N(rateData[symbol].profitNumber / rateData[symbol].totalProfit * 100, 2) : '0') + '%', //Win rate
            {
                'type': 'button',
                'cmd': 'There was supposed to be no retreat???:' + symbol + ':' + assets[exLabel_0][symbol].amount + ':'+ 0 + ':',
                'name': symbol + ' Surrender'
            }
        ];
        table.rows.push(infoList);
        direction = 'Short position';
        margin = direction;
        if (assets[exLabel_1][symbol].amount != 0) {
            direction = assets[exLabel_1][symbol].amount > 0 ? 'go long' + Success : 'go short' + Danger;
            margin = (assets[exLabel_1][symbol].marginType == 'cross' ? 'Cross margin : Isolated margin');
        }

        price = _N((assets[exLabel_1][symbol].ask_price + assets[exLabel_1][symbol].bid_price) / 2, trade_info[symbol].priceSize);
        value = _N((assets[exLabel_1][symbol].ask_value + assets[exLabel_1][symbol].bid_value) / 2, 2);


        //Forced liquidation spread
        liquidationToMarkPrice = 0
        if(assets[exLabel_1][symbol].amount < 0)
           liquidationToMarkPrice = assets[exLabel_1][symbol].liquidationPrice == 0 ? '0' : "↑" + _N(assets[exLabel_1][symbol].liquidationPrice - assets[exLabel_1][symbol].markPrice, trade_info[symbol].priceSize) + '$' + ' ≈ ' + _N((assets[exLabel_1][symbol].liquidationPrice - assets[exLabel_1][symbol].markPrice) / assets[exLabel_1][symbol].markPrice * 100, 2) + '%' + Warning  //Forced liquidation spread

        if(assets[exLabel_1][symbol].amount > 0)
           liquidationToMarkPrice = assets[exLabel_1][symbol].liquidationPrice == 0 ? '0' : "↓" + _N(assets[exLabel_1][symbol].markPrice - assets[exLabel_1][symbol].liquidationPrice, trade_info[symbol].priceSize) + '$' + ' ≈ ' + _N((assets[exLabel_1][symbol].markPrice - assets[exLabel_1][symbol].liquidationPrice) / assets[exLabel_1][symbol].markPrice * 100, 2) + '%' + Warning //Forced liquidation spread

        infoList = [
            exLabel_1,
            "[" + margin + "] [" + assets[exLabel_1][symbol].leverage + 'x] ',
            //_N(100 * assets[exLabel_1][symbol].fundingRate,3), //Rate%
            symbol,
            //symbolText,
            //symbolNum,
            //_N(100 * assets[exLabel_1][symbol].btc_diff,2) + (assets[exLabel_1][symbol].btc_diff >= 0 ? Success : Danger),//Deviation from average(%)
            //100*maxDiff[symbol]+"/"+100*minDiff[symbol],
            direction,
            Math.abs(assets[exLabel_1][symbol].amount),
            assets[exLabel_1][symbol].hold_price,
            price,
            assets[exLabel_1][symbol].liquidationPrice, //Forced liquidation price
            //assets[exLabel_1][symbol].liquidationPrice == 0 ? '0' : '$' + _N(assets[exLabel_1][symbol].liquidationPrice - price, 5) + ' ≈ ' + _N(assets[exLabel_1][symbol].liquidationPrice / price * 100, 2) + '%' + Warning, //Forced liquidation price
            liquidationToMarkPrice,//Forced liquidation spread
            Math.abs(value),
            _N(assets[exLabel_1][symbol].positionInitialMargin, 2),
            // assets[exLabel_1][symbol].btc_diff,
            _N(assets[exLabel_1][symbol].unrealised_profit, 3) + (assets[exLabel_1][symbol].unrealised_profit >= 0 ? Success : Danger),//Unrealized profit and loss
            // (rateData[symbol].profitNumber > 0 && rateData[symbol].totalProfit > 0 ? _N(rateData[symbol].profitNumber / rateData[symbol].totalProfit * 100, 2) : '0') + '%', //Win rate
            {
                'type': 'button',
                'cmd': 'There was supposed to be no retreat???:' + symbol + ':' + assets[exLabel_1][symbol].amount + ':'  + 1 + ':',
                'name': symbol + ' Surrender'
            }
        ];
        table.rows.push(infoList);
    //}
    //delete assets.USDT.update_time; //Timestamp is useless,Don't want it
    var logString = JSON.stringify(assets[exLabel_0].USDT) + '\n';
        logString = logString + JSON.stringify(assets[exLabel_1].USDT) + '\n';
    var StatusData = AppendedStatus();
    //LogStatus(StatusData.upTable + '`' + JSON.stringify([table, StatusData.indexTable]) + '`\n' + logString);
    LogStatus(StatusData.upTable + '`' + JSON.stringify([table]) + '`\n' + logString);

    if (Date.now() - update_profit_time > Log_profit_interval * 1000) {
        var balance = assets[exLabel_0].USDT.margin_balance + assets[exLabel_1].USDT.margin_balance;
/*
        if (Show) {
            balance = assets.USDT.margin_balance - Funding;
        }
*/
        LogProfit(_N(balance, 3), '&');
        update_profit_time = Date.now();
/*
        if (UpProfit != 0 && (_N(balance, 0) != UpProfit)) { //Do not calculate the first time,Do not calculate win rate for decimal parts
            tradingCounter("totalProfit", 1); //Count the number of prints, winning rate = number of profits/number of prints*100
            if (_N(balance, 0) > UpProfit) {
                tradingCounter("profitNumber", 1); //Number of Wins
            }
            WinRate();
        }
        UpProfit = _N(balance, 0);
*/
    }

}
function onTick() { //Strategy logic section
        var symbol = "BTC";
        if (trade_info[symbol].ask_price == 0 || trade_info[symbol].bid_price ==0) {
            return;
        }
        //Check whether the position has already been closed by take-profit or stop-loss orders

        //Complete0Open Position
        //Hedge ended
            if(assets[exLabel_0][symbol].amount == 0 &&
               assets[exLabel_1][symbol].amount == 0 &&
              (
               //assets[exLabel_1].USDT.total_balance <1 ||
               //assets[exLabel_0].USDT.total_balance <1 ||
               assets[exLabel_0].USDT.total_balance * MarginLevel < trade_info[symbol].minQty * trade_info[symbol].bid_price  ||
               assets[exLabel_1].USDT.total_balance * MarginLevel < trade_info[symbol].minQty * trade_info[symbol].bid_price 
               ) 
              ){
              // Log(assets[exLabel_0].USDT.total_balance,"<",trade_info[symbol].minQty * trade_info[symbol].bid_price)
              // Log(assets[exLabel_1].USDT.total_balance,"<",trade_info[symbol].minQty * trade_info[symbol].bid_price)
                onexit();
                throw '1082 After hedging ends, if you need to rerun the strategy, you need to reset the account parameters.';
            }
            if ( Math.abs(assets[exLabel_0][symbol].amount) <= trade_info[symbol].minQty  &&
                 Math.abs(assets[exLabel_1][symbol].amount) <= trade_info[symbol].minQty  &&
                 assets[exLabel_0].USDT.total_balance * MarginLevel  >= trade_info[symbol].minQty * trade_info[symbol].bid_price  &&
                 assets[exLabel_1].USDT.total_balance * MarginLevel  >= trade_info[symbol].minQty * trade_info[symbol].bid_price   ) { //When positions are almost zero and account balances are all non-zero0

                 exchanges[0].IO("currency", symbol + '_' + 'USDT');
                 exchanges[0].SetContractType('swap');
                 exchanges[0].SetMarginLevel(MarginLevel)

                 exchanges[1].IO("currency", symbol + '_' + 'USDT');
                 exchanges[1].SetContractType('swap');
                 exchanges[1].SetMarginLevel(MarginLevel)

                 var amount =0

    if(assets[exLabel_1].USDT.total_balance > assets[exLabel_0].USDT.total_balance ){
        // USDT.total_balance Small full order placement
        Trade_ex = 0

        //Set to cross margin mode
        //changeMarginTypeToCROSSED(true,"BTCUSDT",exchanges[0])
        //changeMarginTypeToCROSSED(false,"BTCUSDT",exchanges[1])

    }else{
        Trade_ex = 1

        //Set to cross margin mode
        //changeMarginTypeToCROSSED(true,"BTCUSDT",exchanges[1])
        //changeMarginTypeToCROSSED(false,"BTCUSDT",exchanges[0])
    }

                 if (NO_TRADE){
                   //Log(exchanges[Trade_ex].GetLabel())
                   //Log(assets[exchanges[Trade_ex].GetLabel()])
                   //Log(assets)
                  // Log(assets[exchanges[Trade_ex].GetLabel()].USDT.total_balance)
                  // Log(trade_info[symbol].ask_price)
                   Log(353,"exchanges[",Trade_ex,"] buy",symbol," amount:",_N(assets[exchanges[Trade_ex].GetLabel()].USDT.total_balance * MarginLevel  /trade_info[symbol].ask_price,trade_info[symbol].amountSize)," total_balance:",assets[exchanges[Trade_ex].GetLabel()].USDT.total_balance," ask_price:",trade_info[symbol].ask_price)
                   Log(354,"exchanges[",1-Trade_ex,"] sell",symbol," amount:",_N(assets[exchanges[Trade_ex].GetLabel()].USDT.total_balance * MarginLevel  /trade_info[symbol].bid_price,trade_info[symbol].amountSize)," total_balance:",assets[exchanges[Trade_ex].GetLabel()].USDT.total_balance," bid_price:",trade_info[symbol].bid_price)
                   }else{


                   //Set to cross margin mode
                   changeMarginTypeToCROSSED(true,"BTCUSDT",exchanges[Trade_ex])
                   changeMarginTypeToCROSSED(false,"BTCUSDT",exchanges[1-Trade_ex])

                   cancelAll(symbol,exchanges[Trade_ex])

                   exchanges[Trade_ex].SetDirection('buy');

                   //var ticker = _C(exchange.GetTicker);
                   //var spread = ticker.Sell - ticker.Buy;
                   //(ticker.Sell + spread)

                   var spread = trade_info[symbol].ask_price - trade_info[symbol].bid_price;
                   amount = _N(assets[exchanges[Trade_ex].GetLabel()].USDT.total_balance * MarginLevel * 0.99  /(trade_info[symbol].ask_price+spread) ,trade_info[symbol].amountSize)

                   //Log(1052,exchanges[Trade_ex].GetLabel()," buy ",symbol," value(",MarginLevel,"x):",_N(assets[exchanges[Trade_ex].GetLabel()].USDT.total_balance * MarginLevel,2)," amount:",amount," balance:",assets[exchanges[Trade_ex].GetLabel()].USDT.total_balance," ask_price:",trade_info[symbol].ask_price," ticker.Sell:",ticker.Sell ,"  spread:",spread)
                   Log(1052,exchanges[Trade_ex].GetLabel()," buy ",symbol," value(",MarginLevel,"x):",_N(assets[exchanges[Trade_ex].GetLabel()].USDT.total_balance * MarginLevel,2)," amount:",amount," balance:",assets[exchanges[Trade_ex].GetLabel()].USDT.total_balance," ask_price:",trade_info[symbol].ask_price)
                   var exOrderid_01=exchanges[Trade_ex].Buy(-1, amount, symbol);

                if(exOrderid_01){ //Buy the same amount of coins; accounts with less money should buy first (not sell), because buying spends more money than selling.

                   cancelAll(symbol,exchanges[1-Trade_ex])
                   exchanges[1-Trade_ex].SetDirection('sell');
                   //amount = _N(assets[exchanges[Trade_ex].GetLabel()].USDT.total_balance * MarginLevel  /trade_info[symbol].bid_price,trade_info[symbol].amountSize)

                   Log(1094,exchanges[1-Trade_ex].GetLabel()," sell ",symbol," value(",MarginLevel,"x):",_N(assets[exchanges[Trade_ex].GetLabel()].USDT.total_balance * MarginLevel,2)," amount:",amount," balance:",assets[exchanges[Trade_ex].GetLabel()].USDT.total_balance," bid_price:",trade_info[symbol].bid_price)

                 for (var i = 0; i < 10; i++) {
                   var exOrderid_02=exchanges[1-Trade_ex].Sell(-1, amount, symbol);
                   if(!isEmpty(exOrderid_02))break;
                   Sleep(100)
                 }

                 if(isEmpty(exOrderid_02))return;

                   //Sleep(1000)
                   var theOrder = waitOrder(exOrderid_01,exchanges[Trade_ex])

                   //var theOrder = exchanges[Trade_ex].GetOrder(exOrderid_01);

                   //if(!isEmpty(theOrder))theOrder=theOrder.Info;

                   //Log(theOrder);
                   Log(946,exchanges[Trade_ex].GetLabel()," buy ",symbol," OrderId:",theOrder.orderId ,"=>(",theOrder.status,")"," origQty:",theOrder.origQty,"=>(executed:",theOrder.executedQty,") avgPrice:",theOrder.avgPrice," USDT.balance: ",assets[exchanges[Trade_ex].GetLabel()].USDT.total_balance)

                   if (theOrder.status != "NEW"){

                     //var theOrder2 = waitOrder(exOrderid_02,exchanges[1-Trade_ex])

                     updateAccount(exchanges[Trade_ex])


                     exchanges[Trade_ex].SetDirection('closebuy');
                     //exchanges[Trade_ex].Sell(_N( parseFloat(theOrder.avgPrice) * 1.0055,trade_info[symbol].priceSize ) , parseFloat(theOrder.executedQty), symbol);  //Take profit order


                     //amount = _N(assets[symbol].liquidationPrice * Stop_loss + assets[symbol].hold_price * (1 - Stop_loss), trade_info[symbol].priceSize)
                     //assets[exchanges[Trade_ex].GetLabel()][symbol].liquidationPrice -10

                     if(isEmpty(assets[exchanges[Trade_ex].GetLabel()][symbol].liquidationPrice)){
                        getPostion(symbol,exchanges[Trade_ex])
                     }

                     if(isEmpty(assets[exchanges[Trade_ex].GetLabel()][symbol].liquidationPrice)){
                        return
                     }

                     amount = assets[exchanges[Trade_ex].GetLabel()][symbol].liquidationPrice +10

/*
                   if (theOrder2.status != "NEW"){

                     updateAccount(exchanges[1-Trade_ex])

                     if(isEmpty(assets[exchanges[1-Trade_ex].GetLabel()][symbol].liquidationPrice)){
                        getPostion(symbol,exchanges[1-Trade_ex])
                     }

                     if(isEmpty(assets[exchanges[1-Trade_ex].GetLabel()][symbol].liquidationPrice)){
                        return
                     }

                     exchanges[Trade_ex].Sell(_N( parseFloat(assets[exchanges[1-Trade_ex].GetLabel()][symbol].liquidationPrice) ,trade_info[symbol].priceSize ) , parseFloat(theOrder.executedQty), symbol);  //Take profit order
                   }else{
                     exchanges[Trade_ex].Sell(_N( parseFloat(theOrder.avgPrice) * 1.0055,trade_info[symbol].priceSize ) , parseFloat(theOrder.executedQty), symbol);  //Take profit order
                   }
*/

                     var Order = [{
                            "symbol": symbol + "USDT",
                            "side": "SELL",
                            "positionSide": "BOTH",
                            "type": "STOP",
                            "stopPrice": _N( amount , trade_info[symbol].priceSize ),
                            "workingType": "MARK_PRICE",
                            "quantity": _N( parseFloat(theOrder.executedQty) , trade_info[symbol].amountSize ),
                            "price": _N( amount -9 , trade_info[symbol].priceSize ),
                            "timeInForce": "GTC",
                            "reduceOnly": true
                        }]

                     //Log(995,Order)
                     theOrder = makeOrder(Order,exchanges[Trade_ex])


                     amount = _N((1-amount / assets[exchanges[Trade_ex].GetLabel()][symbol].hold_price) * 100, 2)

                     Log(533, " Place stop-loss order(Loss rate:", amount, "%) closebuy ", symbol, " (status:", theOrder.status, ") Order Id:", theOrder.orderId, " price:", theOrder.price, "(stopPrice:",_N( assets[exchanges[Trade_ex].GetLabel()][symbol].liquidationPrice +10 , trade_info[symbol].priceSize ),") liquidationPrice:", _N(assets[exchanges[Trade_ex].GetLabel()][symbol].liquidationPrice, trade_info[symbol].priceSize), " amount:", theOrder.origQty, " MarginLevel:", MarginLevel, " timeInForce=", theOrder.timeInForce, " @", _D())

                   }

                   //Sleep(1000)
                   theOrder = waitOrder(exOrderid_02,exchanges[1-Trade_ex])
                   //theOrder = theOrder2

                   //theOrder = exchanges[1-Trade_ex].GetOrder(exOrderid_02);


                   //if(!isEmpty(theOrder))theOrder=theOrder.Info;

                   Log(987,exchanges[1-Trade_ex].GetLabel()," sell ",symbol," OrderId:",theOrder.orderId ,"=>(",theOrder.status,")"," origQty:",theOrder.origQty,"=>(executed:",theOrder.executedQty,") avgPrice:",theOrder.avgPrice," USDT.balance: ",assets[exchanges[1-Trade_ex].GetLabel()].USDT.total_balance)


                   if (theOrder.status != "NEW"){

                     updateAccount(exchanges[1-Trade_ex])

                     //exchanges[1-Trade_ex].SetDirection('closesell');
                     //exchanges[1-Trade_ex].Buy(_N( parseFloat(theOrder.avgPrice) * 0.9944,trade_info[symbol].priceSize ) , parseFloat(theOrder.executedQty), symbol);  //Take profit order


                     if(isEmpty(assets[exchanges[1-Trade_ex].GetLabel()][symbol].liquidationPrice)){
                        getPostion(symbol,exchanges[1-Trade_ex])
                     }

                     if(isEmpty(assets[exchanges[1-Trade_ex].GetLabel()][symbol].liquidationPrice)){
                        return
                     }


                     amount = assets[exchanges[1-Trade_ex].GetLabel()][symbol].liquidationPrice -10


                     exchanges[Trade_ex].SetDirection('closebuy');
                     exchanges[Trade_ex].Sell(_N( parseFloat(assets[exchanges[1-Trade_ex].GetLabel()][symbol].liquidationPrice) ,trade_info[symbol].priceSize ) ,_N( parseFloat(Math.abs(assets[exchanges[Trade_ex].GetLabel()][symbol].amount)), trade_info[symbol].amountSize), symbol);  //Take profit order

                     exchanges[1-Trade_ex].SetDirection('closesell');
                     exchanges[1-Trade_ex].Buy(_N( parseFloat(assets[exchanges[Trade_ex].GetLabel()][symbol].liquidationPrice),trade_info[symbol].priceSize ) , _N( parseFloat(Math.abs(assets[exchanges[1-Trade_ex].GetLabel()][symbol].amount)), trade_info[symbol].amountSize), symbol);  //Take profit order


                     var Order = [{
                            "symbol": symbol + "USDT",
                            "side": "BUY",
                            "positionSide": "BOTH",
                            "type": "STOP",
                            "stopPrice": _N( amount , trade_info[symbol].priceSize ),
                            "workingType": "MARK_PRICE",
                            "quantity": _N(parseFloat(theOrder.executedQty), trade_info[symbol].amountSize),
                            "price": _N( amount +9 , trade_info[symbol].priceSize ),
                            "timeInForce": "GTC",
                            "reduceOnly": true
                        }]
                     theOrder = makeOrder(Order,exchanges[1-Trade_ex])

                     amount = _N((amount / assets[exchanges[1-Trade_ex].GetLabel()][symbol].hold_price -1) * 100, 2)

                     Log(571, " Place stop-loss order(Loss rate:", amount, "%) closesell ", symbol, " (status:", theOrder.status, ") Order Id:", theOrder.orderId, " price:", theOrder.price, "(stopPrice:",_N( assets[exchanges[1-Trade_ex].GetLabel()][symbol].liquidationPrice -10 , trade_info[symbol].priceSize ),") liquidationPrice:", _N(assets[exchanges[1-Trade_ex].GetLabel()][symbol].liquidationPrice, trade_info[symbol].priceSize), " amount:", theOrder.origQty, " MarginLevel:", MarginLevel, " timeInForce=", theOrder.timeInForce, " @", _D())

                   }
                  }//end order_01
                 }//end NO_TRADE

            }
        //Single position
            if ((Math.abs(assets[exLabel_0][symbol].amount) >= trade_info[symbol].minQty  &&
                 Math.abs(assets[exLabel_1][symbol].amount) <= trade_info[symbol].minQty )||
                (Math.abs(assets[exLabel_0][symbol].amount) <= trade_info[symbol].minQty &&
                 Math.abs(assets[exLabel_1][symbol].amount) >= trade_info[symbol].minQty )) { //Any one of0Another otherwise0

                if(assets[exLabel_0][symbol].amount != 0){
                  cancelAll(symbol,exchanges[0])
                  cancelAll(symbol,exchanges[1])
                  closeAll(symbol,exchanges[0])
                  Log(1022,exLabel_0," Already closed(Closed by another exchange)! exLabel_0_Amount:",assets[exLabel_0][symbol].amount,"exLabel_1_Amount:",assets[exLabel_1][symbol].amount)
                }
                if(assets[exLabel_1][symbol].amount != 0){
                  cancelAll(symbol,exchanges[0])
                  cancelAll(symbol,exchanges[1])
                  closeAll(symbol,exchanges[1])
                  Log(1026,exLabel_1," Already closed(Closed by another exchange)! exLabel_0_Amount:",assets[exLabel_0][symbol].amount,"exLabel_1_Amount:",assets[exLabel_1][symbol].amount)
                }
                onexit();
                throw '1317 Hedge finished, please check the positions, whether the orders have been cleared, and restart';

            }
        //take profit//stop loss
            if ( Math.abs(assets[exLabel_0][symbol].amount) >= trade_info[symbol].minQty  &&
                 Math.abs(assets[exLabel_1][symbol].amount) >= trade_info[symbol].minQty ){ //No position is allowed0

                if(assets[exchanges[Trade_ex].GetLabel()][symbol].markPrice <= assets[exchanges[Trade_ex].GetLabel()][symbol].liquidationPrice +10 ||
                   assets[exchanges[1-Trade_ex].GetLabel()][symbol].markPrice >= assets[exchanges[1-Trade_ex].GetLabel()][symbol].liquidationPrice -10 ){ //stop loss

                   if(assets[exchanges[Trade_ex].GetLabel()][symbol].markPrice <= assets[exchanges[Trade_ex].GetLabel()][symbol].liquidationPrice +10)
                      Log(1224,exchanges[Trade_ex].GetLabel(),"stop loss,And close positions on another exchange markPrice",assets[exchanges[Trade_ex].GetLabel()][symbol].markPrice,"<=",assets[exchanges[Trade_ex].GetLabel()][symbol].liquidationPrice +10)

                   if(assets[exchanges[1-Trade_ex].GetLabel()][symbol].markPrice >= assets[exchanges[1-Trade_ex].GetLabel()][symbol].liquidationPrice -10)
                      Log(1225,exchanges[1-Trade_ex].GetLabel(),"stop loss,And close positions on another exchange markPrice",assets[exchanges[1-Trade_ex].GetLabel()][symbol].markPrice,">=",assets[exchanges[1-Trade_ex].GetLabel()][symbol].liquidationPrice -10)

                   cancelAll(symbol,exchanges[Trade_ex])
                   cancelAll(symbol,exchanges[1-Trade_ex])

                   closeAll(symbol,exchanges[Trade_ex])
                   closeAll(symbol,exchanges[1-Trade_ex])
                }

            }


}
function RunCommand() {
    var str_cmd = GetCommand();
    if (str_cmd) {
        var arrCmd = str_cmd.split(':');
        var symbol = arrCmd[1];
        var amount = parseFloat(arrCmd[2]);
        var ex = arrCmd[3];
        var exchange=exchanges[ex]
        if (amount == 0) {
            Log('Dear,Do you still remember Qiao Biluo by Daming Lake??' + Danger);
            return;
        }
        var f = amount < 0 ? 'Buy' : 'Sell';
        var dirction = amount < 0 ? 'buy' : 'sell';
        exchange.IO("currency", symbol + '_' + 'USDT');
        exchange.SetContractType('swap');
        exchange.SetDirection(dirction);
        exchange.SetMarginLevel(MarginLevel)
        exchange[f](-1, Math.abs(amount), symbol);
        Log(737,exchange.GetLabel(),dirction,symbol," Surrender amount=",amount)
    }
}

function main() {
    while (true) {
        RunTime = RuningTime();
        RunCommand(); //Capture interactive commands
        updateAccount(exchanges[0])
        updateAccount(exchanges[1]); //Update account and positions
        updateTick(); //Market quotation
        //stopLoss(); //stop loss
        onTick(); //Strategy logic section
        updateStatus(); //Output status bar information
        Sleep(Interval * 1000);
    }

}
```

> Detail

https://www.fmz.com/strategy/211262

> Last Modified

2020-09-08 19:25:12
