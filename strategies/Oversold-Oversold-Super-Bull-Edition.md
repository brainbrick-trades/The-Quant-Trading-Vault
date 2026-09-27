
> Name

Oversold-Oversold-Super-Bull-Edition

> Author

ChaoZhang

> Strategy Description

## 4.13 Updated content

Stop_lossSetting it to 0.8 means that when the funds reach less than 80% of the initial funds, stop loss, clear all positions, and stop the strategy. As the strategy runs, Stop_loss can be set to greater than 1 (restart to take effect). For example, if you earn 1,500 from 1,000, and Stop_loss is set to 1.3, then the stop loss will be retraced to 1,300 yuan. If you don't want to stop the loss, you can set this parameter very small. The risk is that if everyone uses this kind of stop loss, it will cause a stampede and increase losses. The initial funds are in the init_balance field of the status bar. Please note that operations such as withdrawals will be affected. Don't accidentally stop the loss. If you are still afraid of black swan events, such as a certain currency returning to 0, etc., you can withdraw it manually.

Max_diffand Min_diff limit the degree of deviation, which needs to be determined by yourself based on your own trade_value, total funds and risk tolerance.

To give a simple example, if a total of 20 coins are traded, the value of one of the coins gradually rises to a deviation of 0.4 and is no longer traded, while the prices of other coins remain unchanged, resulting in a loss of 7 times the trade_value. If it continues to fall to a deviation of -0.3, it will lose 6 times of trade_value.

```
var Stop_loss = 0.8 
var Max_diff = 0.4 //When deviationdiffGreater than0.4Do not continue adding short positions at, Set by oneself
var Min_diff = -0.3 //whendiffLess Than-0.3Do not continue adding long positions at, Set by oneself
```

## 4.10 Updated content

**Copy the policy code to the local policy, overwrite and save directly. Restart the bot to take effect, and the original position will be retained**

Binance Futures short-selling, long-selling, and falling strategies are important to optimize the notebook code address.:https://www.fmz.com/bbs-topic/5364 

Original strategy altcoin index = mean(sum((altcoin price/bitcoin price)/(altcoin initial price/bitcoin initial price))). The biggest problem is that the comparison between the latest price and the initial price when the strategy is started will deviate more and more as time goes by. A coin may hold many positions, which is very risky. In the end, it will hold many positions, increasing risks and drawdowns.

The latest altcoin index = mean(sum((altcoin price/bitcoin price)/EMA(altcoin price/bitcoin price))), which is compared with the price of the moving average, can track the latest price changes, is more flexible, and backtesting has found that it reduces strategic positions and also reduces retracement. More stable. The most important thing is that if a few abnormal trading pairs were added to the original strategy, the risk would be extremely high and the position would probably be liquidated, but now it is almost unaffected.

For seamless upgrades, two parameters are written in the first two lines of the strategy code and can be modified as needed.

Alpha = 0.04 The larger the Alpha parameter of the index moving tie is set, the more sensitive the benchmark price tracking will be. The fewer transactions will be made, the lower the final position will be. This reduces the leverage, but will reduce the income, reduce the maximum drawdown, and can increase the trading volume. You need to weigh it based on the backtest results.
Update_base_price_time_interval = 30*60 How often to update the benchmark price, in seconds, related to the Alpha parameter. The smaller the Alpha setting, the smaller the interval can also be set.

If you read the article and want to trade all currencies, here is the list``ETH,BCH,XRP,EOS,LTC,TRX,ETC,LINK,XLM,ADA,XMR,DASH,ZEC,XTZ,BNB,ATOM,ONT,IOTA,BAT,VET,NEO,QTUM,IOST``

## **Important content!!**

- Be sure to read this study https://www.fmz.com/digest-topic/5294 first. Understand a series of issues such as strategy principles, risks, how to screen trading pairs, how to set parameters, the ratio of opening positions to total funds, etc.
- The previous research report needs to be downloaded and uploaded to your own research environment. Run the actual modifications. If you have already seen this report, it was recently updated with data for the latest week.
- **The strategy cannot be backtested directly and needs to be backtested in the research environment**.
- Strategy code and default parameters are for research purposes only. Caution is required for live trading; set parameters based on your own research, **at your own risk**.**.
- **The strategy cannot be profitable every day. You can check backtest history; sideways movement and drawdowns over 1-2 weeks are normal and need to be handled correctly**
- The code is public and can be modified by yourself. If you have any questions, please leave comments and feedback. It is best to join the inventor's Binance exchange group (how to join is in the research report) to get update notifications.
- **The strategy only supports Binance futures and needs to be run in full position mode. Do not set two-way positions! ! , just use the default trading pair and candlestick cycle when creating the robot. The strategy does not use candlestick.**
- **The strategy conflicts with other strategies and manual operations, so you need to pay attention**
- Overseas hosts are required for real-time operation. During the test phase, you can rent Alibaba Cloud Hong Kong servers with one click on the platform. It is cheaper to rent the entire server by yourself on a monthly basis (the lowest configuration is sufficient, please refer to the deployment tutorial:https://www.fmz.com/bbs-topic/2848)
- Binance's futures and spot need to be added separately. Binance futures are``Futures_Binance``
- Restarting this strategy does not affect it, but creating a new robot will re-record historical data.
- The strategy may be updated based on user feedback. Just ctrl+A to copy the code and save it (generally the parameters will not be updated). Restart the robot to use the latest code.
- The strategy does not trade at the beginning. The first startup requires recording data, and trading will only occur after market changes.

## Join the WeChat group to participate in Binance Thousand Group Battle for updates

Add the WeChat ID below, reply "Binance" to be automatically added to the group:

https://www.fmz.com![IMG](https://www.fmz.com/upload/asset/1fbed0c3795dbecac04.jpg)

## Strategy Principle

We will short the currency whose price is higher than the altcoin-Bitcoin price index and long the currency whose price is lower than the index. The greater the deviation, the larger the position. (This strategy does not use BTC to hedge unequal positions. BTC can also be added to the trading pair). Performance in the past two months (about 3 times leverage, data updated to4.8):
 ![IMG](https://www.fmz.com/upload/asset/1b2a6f297fcf590ad02.png) 

## Strategy Logic

1.Update market prices and account positions. The initial price will be recorded in the first run (newly added currencies are calculated based on the time of addition))
2.Update the index, the index is Altcoin-Bitcoin price index = mean(sum((Altcoin price/Bitcoin price)/(Altcoin initial price/Bitcoin initial price)))
3.Determine long or short positions based on deviation index, determine position size based on deviation magnitude
4.Place an order. The order quantity is determined by Bingshan Commission, and the transaction is completed according to the counterparty price (buy at the same price as the sell). **Cancel the order immediately after placing it (so you will see many orders with failed cancellation 400: {"code":-2011,"msg":"Unknown order sent."}, normal phenomenon)**
5.Loop again

The leverage in the status bar represents the margin used percentage, which needs to be maintained at a low level to accommodate new positions

## Strategy Arguments

 ![IMG](https://www.fmz.com/upload/asset/272b24a9c0018c96fb6.png) 

- Trade_symbols:Trading coins should be selected based on your own research platform, can also be added.BTC
- Trade_value:Every 1% deviation of the altcoin price (priced in BTC) from the holding value of the index needs to be determined based on the total funds invested and risk preference. It is recommended to set it to 3-10% of the total funds. The size of the leverage can be seen through backtesting in the research environment. Trade_value can be less than Adjust_value, such as half of Adjust_value, which is equivalent to a holding value that deviates from the index by 2%.
- Adjust_value:	Contract value (priced in USDT) adjusts the deviation value. When the index deviates from \* Trade_value - current position > Adjust_value, that is, the difference between the target position and the current position exceeds this value, a transaction will start. If it is too large, the adjustment will be slow. If it is too small, transactions will be frequent. It cannot be lower than 10, otherwise the minimum transaction will not be reached. It is recommended to set it to more than 40% of Trade_value.
- Ice_value:The iceberg commission value cannot be less than 10. When placing a single order, choose the smaller one between Adjust_value and Ice_value. If you have more funds, you can set it to a relatively large value so that the adjustment can be made faster. It is recommended not to be less than 20% of Adjust_value, so that the transaction can be completed in 5 times of Iceberg. Of course, when the Trade_value is not large, Ice_value can be set to a relatively large value, and it can be adjusted in one or two times.
- Interval:Loop Sleep Time: It can be set shorter, e.g., 1s, but cannot exceed Binance frequency limits.
- Reset:Reset historical data, which will reset the initial price referenced by the strategy to the current price, usually not set.


## Strategy Risks

noticed that if a certain currency goes out of independent market, for example, it rises several times relative to the index, a large number of short positions will be accumulated on the currency, and the same sharp decline will also cause the strategy to go long in large quantities. You can limit the opening amount or stop loss and no longer trade.



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Trade_symbols|IOST,TRX,XLM,QTUM,DASH,ADA,BNB,XMR,ZEC,ATOM,IOTA,NEO,ONT,XRP,BAT,VET,EOS,ETC,LTC|Transaction currency|
|Trade_value|20|Holding value for every 1% deviation from the index|
|Adjust_value|20|Contract value adjustment deviation|
|Ice_value|20|Size of iceberg order|
|Log_profit_interval|600|LogTotal equity intervals|
|Interval|true|Dormant Times|
|Reset|false|Reset historical data|


> Source (javascript)

``` javascript

/*
 * @Description: Semicolon version. First, this is a knockoff version. The added functions are below; no logical content has been changed
 * @Version: 0.1.3
 * @Author: RedSword
 * @Email: redsword@gamil.com
 * @Date: 2020-04-10 11:48:38
 * @LastEditors: Home RedSword
 * @LastEditTime: 2020-04-18 19:49:28
 *
 * Before running, be sure to carefully read Caoshen's article, the address is https://www.fmz.com/strategy/195226
 * 
 * Add function
 * 
 * 2020-04-18
 * 1.Added Caoshen's balanced hedging feature
 * 2.Modified the default Alpha value and base price update time, Alpha was changed to 0.001, and the base price update time was changed to 1 minute
 * 3.Added forced liquidation distance and percentage
 * 4.Modified deviation from average and estimated win rate for each coin are placed in the coin index information
 * 5.Disabled Log profit function to save some space
 * 
 * 2020-04-16
 * 1.Fixed "When the moon moves, I move" issueBUG
 * 2.Fixed error when adding a new coinBUG
 * 
 * 2020-04-15
 * 1.Add account asset information
 * 2.Add currency index information
 * 3.Add the winning rate of each currency
 * 4.Add single-currency surrender function
 * 5.Thanks to fmzero for the open-source code
 * 
 * 2020-04-13
 * 1.Add trading-related statistics, thanks to Douzi for the open-source code
 * 2.Anything labeled as estimated is inaccurate and can only be used as a rough reference.
 * 3.Added Caoshen's latest stop-loss logic
 * 4.Remove the original Max_amount stop-loss method
 * 5.Added toggle to display absolute returns
 * 6.Show the prompts from the original strategy, added stop-loss prompts in profit statistics
 * 
 * 2020-04-12
 * 1.Added maximum position opening limit, 0 means no limit
 * 2.Display the absolute value of position value, do not show negative sign
 * 3.Display the current currency leverage multiple and position liquidation price
 * 4.Added position opening mode for currency, full position or isolated margin
 * 5.Fix reset not workingBUG
 * 6.Correct inaccurate running timeBUG
 * 7.Modify margin display to be consistent with the official version
 * 8.Margin does not display as a percentage, change to ratio, consistent with official
 * 
 * 2020-04-10
 * 1.Added a semicolon for obsessive-compulsive disorder
 * 2.Added profit statistics
 * 3.Added open position direction, and color-coded position direction and position profit/loss
 */

var Alpha = 0.001; //Exponential moving averageAlphaParameter, the larger the setting, the more sensitive the benchmark price tracking will be, and the final position will be lower, which reduces the leverage, but will reduce the income. You need to weigh it based on the backtest results.
var Update_base_price_time_interval = 60; //How often to update the benchmark price, in seconds, related to the Alpha parameter. The smaller the Alpha setting, the smaller the interval can also be set.



//Stop_lossSet as0.8Indicates when funds fall below the initial capital80%Trigger stop loss, clear all positions, and stop the strategy.
//As the strategy runs,Stop_lossCan set greater than1(Effective after restart), for example from1000Earn1500,Stop_lossSet as1.3,Then draw down to1300Yuan stop loss. If you don't want to stop the loss, you can set this parameter very small.
//The risk is that if everyone uses this stop loss, it will cause a stampede and increase losses.
//Initial funds in the status barinit_balancefield, please note that operations such as withdrawals will be affected. Don't accidentally stop the loss.
//If still afraid of black swan events, for example if a coin returns0Waiting, can manually withdraw.

var Stop_loss = 0.8;
var Max_diff = 0.4; //When deviationdiffGreater than0.4Do not continue adding short positions at, Set by oneself
var Min_diff = -0.3; //whendiffLess Than-0.3Do not continue adding long positions at, Set by oneself

var Version = '0.1.3';
var Show = false; //Default isfalseThe accumulated profit shows the account balance,Change totrueDisplay cumulative profit as earnings,If the account balance was displayed before,You useLogProfitReset()Clear the chart
var Funding = 0; //Account initial balance,is0When,Automatically obtain,Not0is customized
var Success = '#5cb85c'; //Success color
var Danger = '#ff0000'; //Dangerous colors
var Warning = '#f0ad4e'; //Warning color
var RunTime; //Running time
var SelfFee = '0.04'; //https://www.binance.com/cn/fee/futureFee
var TotalLong;
var TotalShort;
var UpProfit = 0;
var accountAssets = []; //Save assets
var WinRateData = {}; //Save the win rate and number of positions opened for all currencies

if (IsVirtual()) {
    throw 'Cannot backtest, reference for backtest https://www.fmz.com/digest-topic/5294 ';
}
if (exchange.GetName() != 'Futures_Binance') {
    throw 'Only supports Binance futures exchange, which is different from spot exchange and needs to be added separately with the nameFutures_Binance';
}
var trade_symbols = Trade_symbols.split(',');
var symbols = trade_symbols;
var index = 1; //Index
if (trade_symbols.indexOf('BTC') < 0) {
    symbols = trade_symbols.concat(['BTC']);
}
var update_profit_time = 0;
var update_base_price_time = Date.now();
var assets = {};
var init_prices = {};
var trade_info = {};

function init() {
    InitRateData();
    var exchange_info = HttpQuery('https://fapi.binance.com/fapi/v1/exchangeInfo');
    if (!exchange_info) {
        throw 'Unable to connect to Binance network, requires overseas hosting';
    }
    exchange_info = JSON.parse(exchange_info);
    for (var i = 0; i < exchange_info.symbols.length; i++) {
        if (symbols.indexOf(exchange_info.symbols[i].baseAsset) > -1) {
            assets[exchange_info.symbols[i].baseAsset] = {
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
            trade_info[exchange_info.symbols[i].baseAsset] = {
                minQty: parseFloat(exchange_info.symbols[i].filters[1].minQty),
                priceSize: parseInt((Math.log10(1.1 / parseFloat(exchange_info.symbols[i].filters[0].tickSize)))),
                amountSize: parseInt((Math.log10(1.1 / parseFloat(exchange_info.symbols[i].filters[1].stepSize))))
            };
        }
    }
}
assets.USDT = {
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

function updateAccount() { //Update account and positions
    var account = exchange.GetAccount();
    var pos = exchange.GetPosition();
    if (account == null || pos == null) {
        Log('update account time out');
        return;
    }
    accountAssets = account.Info.assets;
    assets.USDT.update_time = Date.now();
    for (var i = 0; i < trade_symbols.length; i++) {
        assets[trade_symbols[i]].margin = 0;
        assets[trade_symbols[i]].unrealised_profit = 0;
        assets[trade_symbols[i]].hold_price = 0;
        assets[trade_symbols[i]].amount = 0;
    }
    for (var j = 0; j < account.Info.positions.length; j++) {
        if (account.Info.positions[j].positionSide == 'BOTH') {
            var pair = account.Info.positions[j].symbol;
            var coin = pair.slice(0, pair.length - 4);
            if (trade_symbols.indexOf(coin) < 0) {
                continue;
            }
            assets[coin].margin = parseFloat(account.Info.positions[j].initialMargin) + parseFloat(account.Info.positions[j].maintMargin);
            assets[coin].unrealised_profit = parseFloat(account.Info.positions[j].unrealizedProfit);
            assets[coin].positionInitialMargin = parseFloat(account.Info.positions[j].positionInitialMargin);
            assets[coin].leverage = account.Info.positions[j].leverage;
        }
    }
    assets.USDT.margin = _N(parseFloat(account.Info.totalInitialMargin) + parseFloat(account.Info.totalMaintMargin), 2);
    assets.USDT.margin_balance = _N(parseFloat(account.Info.totalMarginBalance), 2);
    assets.USDT.total_balance = _N(parseFloat(account.Info.totalWalletBalance), 2);
    if (assets.USDT.init_balance == 0) {
        if (_G('init_balance')) {
            assets.USDT.init_balance = _N(_G('init_balance'), 2);
        } else {
            assets.USDT.init_balance = assets.USDT.total_balance;
            _G('init_balance', assets.USDT.init_balance);
        }
    }
    assets.USDT.profit = _N(assets.USDT.margin_balance - assets.USDT.init_balance, 2);
    assets.USDT.stop_balance = _N(Stop_loss * assets.USDT.init_balance, 2);
    assets.USDT.total_balance = _N(parseFloat(account.Info.totalWalletBalance), 2);
    assets.USDT.unrealised_profit = _N(parseFloat(account.Info.totalUnrealizedProfit), 2);
    assets.USDT.leverage = _N(assets.USDT.margin / assets.USDT.total_balance, 2);
    assets.USDT.margin_ratio = (account.Info.totalMaintMargin / account.Info.totalMarginBalance * 100);
    pos = JSON.parse(exchange.GetRawJSON());
    if (pos.length > 0) {
        for (var k = 0; k < pos.length; k++) {
            var pair = pos[k].symbol;
            var coin = pair.slice(0, pair.length - 4);
            if (trade_symbols.indexOf(coin) < 0) {
                continue;
            }
            if (pos[k].positionSide != 'BOTH') {
                continue;
            }
            assets[coin].hold_price = parseFloat(pos[k].entryPrice);
            assets[coin].amount = parseFloat(pos[k].positionAmt);
            assets[coin].unrealised_profit = parseFloat(pos[k].unRealizedProfit);
            assets[coin].liquidationPrice = parseFloat(pos[k].liquidationPrice);
            assets[coin].marginType = pos[k].marginType;
        }
    }
}

function updateIndex() { //Update index
    if (!_G('init_prices') || Reset) {
        Reset = false;
        for (var i = 0; i < trade_symbols.length; i++) {
            init_prices[trade_symbols[i]] = (assets[trade_symbols[i]].ask_price + assets[trade_symbols[i]].bid_price) / (assets.BTC.ask_price + assets.BTC.bid_price);
        }
        Log('Save the price at startup');
        _G('init_prices', init_prices);
        _G("StartTime", null); //Reset start time
        _G("initialAccount_" + exchange.GetLabel(), null); //Reset starting funds
        _G("tradeNumber", null); //Reset number of trades
        _G("tradeVolume", null); //Reset trading volume
        _G("buyNumber", null); //Reset number of long positions
        _G("sellNumber", null); //Reset number of short positions
        _G("totalProfit", null); //Reset print count
        _G("profitNumber", null); //Reset number of profitable trades
    } else {
        init_prices = _G('init_prices');
        if (Date.now() - update_base_price_time > Update_base_price_time_interval * 1000) {
            update_base_price_time = Date.now();
            for (var i = 0; i < trade_symbols.length; i++) { //Update initial price
                init_prices[trade_symbols[i]] = init_prices[trade_symbols[i]] * (1 - Alpha) + Alpha * (assets[trade_symbols[i]].ask_price + assets[trade_symbols[i]].bid_price) / (assets.BTC.ask_price + assets.BTC.bid_price);
            }
            _G('init_prices', init_prices);
        }
        var temp = 0;
        for (var i = 0; i < trade_symbols.length; i++) {
            assets[trade_symbols[i]].btc_price = (assets[trade_symbols[i]].ask_price + assets[trade_symbols[i]].bid_price) / (assets.BTC.ask_price + assets.BTC.bid_price);
            if (!(trade_symbols[i] in init_prices)) {
                Log('Add new currency', trade_symbols[i]);
                init_prices[trade_symbols[i]] = assets[trade_symbols[i]].btc_price;
                _G('init_prices', init_prices);
            }
            assets[trade_symbols[i]].btc_change = _N(assets[trade_symbols[i]].btc_price / init_prices[trade_symbols[i]], 4);
            temp += assets[trade_symbols[i]].btc_change;
        }
        index = _N(temp / trade_symbols.length, 4);
    }

}

function updateTick() { //Update Quotes
    var ticker = HttpQuery('https://fapi.binance.com/fapi/v1/ticker/bookTicker');
    try {
        ticker = JSON.parse(ticker);
    } catch (e) {
        Log('get ticker time out');
        return;
    }
    assets.USDT.short_value = 0;
    assets.USDT.long_value = 0;
    for (var i = 0; i < ticker.length; i++) {
        var pair = ticker[i].symbol;
        var coin = pair.slice(0, pair.length - 4);
        if (symbols.indexOf(coin) < 0) {
            continue;
        }
        assets[coin].ask_price = parseFloat(ticker[i].askPrice);
        assets[coin].bid_price = parseFloat(ticker[i].bidPrice);
        assets[coin].ask_value = _N(assets[coin].amount * assets[coin].ask_price, 2);
        assets[coin].bid_value = _N(assets[coin].amount * assets[coin].bid_price, 2);
        if (trade_symbols.indexOf(coin) < 0) {
            continue;
        }
        if (assets[coin].amount < 0) {
            assets.USDT.short_value += Math.abs((assets[coin].ask_value + assets[coin].bid_value) / 2);
        } else {
            assets.USDT.long_value += Math.abs((assets[coin].ask_value + assets[coin].bid_value) / 2);
        }
        assets.USDT.short_value = _N(assets.USDT.short_value, 0);
        assets.USDT.long_value = _N(assets.USDT.long_value, 0);
    }
    updateIndex();
    for (var i = 0; i < trade_symbols.length; i++) {
        assets[trade_symbols[i]].btc_diff = _N(assets[trade_symbols[i]].btc_change - index, 4);
    }
}



function trade(symbol, dirction, value) { //Transaction
    if (Date.now() - assets.USDT.update_time > 10 * 1000) {
        Log('Update account delay, do not trade');
        return;
    }
    var price = dirction == 'sell' ? assets[symbol].bid_price : assets[symbol].ask_price;
    var amount = _N(Math.min(value, Ice_value) / price, trade_info[symbol].amountSize);
    if (amount < trade_info[symbol].minQty) {
        Log(symbol, 'Contract value deviation or iceberg order size is set too small to meet the minimum transaction., At least needed: ', _N(trade_info[symbol].minQty * price, 0) + 1);
        return;
    }
    exchange.IO("currency", symbol + '_' + 'USDT');
    exchange.SetContractType('swap');
    exchange.SetDirection(dirction);
    var f = dirction == 'buy' ? 'Buy' : 'Sell';
    var id = exchange[f](price, amount, symbol);
    if (id) {
        exchange.CancelOrder(id); //Order will be canceled immediately
    }
    tradingCounter("tradeVolume", price * amount); //Save transaction volume
    tradingCounter("tradeNumber", 1); //Save number of trades
    WinRateData[symbol].tradeNumber += 1;
    if (dirction == 'buy') {
        tradingCounter("buyNumber", 1);
        WinRateData[symbol].buyNumber += 1;
    } else {
        tradingCounter("sellNumber", 1);
        WinRateData[symbol].sellNumber += 1;
    }
    _G("WinRateData", WinRateData); //Save trading data for each currency
    return id;
}

function InitRateData() {
    if (Reset) {
        _G("WinRateData", null);
    }
    if (_G("WinRateData")) {
        WinRateData = _G("WinRateData");
    }
    for (var i = 0; i < symbols.length; i++) {
        if (typeof WinRateData[symbols[i]] == 'undefined') {
            WinRateData[symbols[i]] = {
                totalProfit: 0, //Count of statistics
                profitNumber: 0, //Number of Wins
                tradeNumber: 0, //Number of Trades
                buyNumber: 0, //Number of long trades
                sellNumber: 0 //Number of short trades
            };
        }
    }
    _G("WinRateData", WinRateData);
}

function RunCommand() {
    var str_cmd = GetCommand();
    if (str_cmd) {
        var arrCmd = str_cmd.split(':');
        var symbol = arrCmd[1];
        var amount = parseFloat(arrCmd[2]);
        if (amount == 0) {
            Log('Dear,Do you still remember Qiao Biluo by Daming Lake??' + Danger);
            return;
        }
        var f = amount < 0 ? 'Buy' : 'Sell';
        var dirction = amount < 0 ? 'buy' : 'sell';
        exchange.IO("currency", symbol + '_' + 'USDT');
        exchange.SetContractType('swap');
        exchange.SetDirection(dirction);
        exchange[f](-1, Math.abs(amount), symbol);
    }
}

function FirstAccount() {
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
        cols: ["Running days", "Initial funds", "Existing funds", "Margin balance", "Used margin", "Margin ratio", "Stop loss", "Total income", "Estimated annualized", "Estimated monthly", "Average daily"],
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
    if (Funding == 0) {
        Funding = parseFloat(FirstAccount().Info.totalWalletBalance);
    }
    var profitColors = Danger;
    var totalProfit = assets.USDT.total_balance - Funding; //Total profit
    if (totalProfit > 0) {
        profitColors = Success;
    }
    var dayProfit = totalProfit / runday; //Daily profit
    var dayRate = dayProfit / Funding * 100;
    accountTable.rows.push([
        runday,
        '$' + _N(Funding, 2),
        '$' + assets.USDT.total_balance,
        '$' + assets.USDT.margin_balance,
        '$' + assets.USDT.margin,
        _N(assets.USDT.margin_ratio, 2) + '%',
        _N(assets.USDT.stop_balance, 2) + Danger,
        _N(totalProfit / Funding * 100, 2) + "% = $" + _N(totalProfit, 2) + (profitColors),
        _N(dayRate * 365, 2) + "% = $" + _N(dayProfit * 365, 2) + (profitColors),
        _N(dayRate * 30, 2) + "% = $" + _N(dayProfit * 30, 2) + (profitColors),
        _N(dayRate, 2) + "% = $" + _N(dayProfit, 2) + (profitColors)
    ]);
    var vloume = _G("tradeVolume") ? _G("tradeVolume") : 0;
    feeTable.rows.push([
        index, //Index
        _G("tradeNumber") ? _G("tradeNumber") : 0, //Number of Trades
        _G("buyNumber") ? _G("buyNumber") : 0, //Number of long trades
        _G("sellNumber") ? _G("sellNumber") : 0, //Number of short trades
        _N(_G("profitNumber") / _G("totalProfit") * 100, 2) + '%', //Win rate
        '$' + _N(vloume, 2) + ' ≈ ฿' + _N(vloume / ((assets.BTC.bid_price + assets.BTC.ask_price) / 2), 6), //Transaction amount
        '$' + _N(vloume * (SelfFee / 100), 4), //trading fee
        '$' + _N(assets.USDT.unrealised_profit, 2) + (assets.USDT.unrealised_profit >= 0 ? Success : Danger),
        '$' + _N(TotalLong + Math.abs(TotalShort), 2), //Total value of positions
        '$' + _N(TotalLong, 2) + Success, //Total value of long trades
        '$' + _N(Math.abs(TotalShort), 2) + Danger, //Total value of short trades
    ]);
    var assetTable = {
        type: 'table',
        title: 'Account asset information',
        cols: ['Number', 'Asset name', 'Initial margin', 'Maintenance margin', 'Margin balance', 'Maximum withdrawal amount', 'Starting margin for pending orders', 'Starting margin for positions', 'Unrealized profit and loss for positions', 'Account balance'],
        rows: []
    };
    for (var i = 0; i < accountAssets.length; i++) {
        var acc = accountAssets[i];
        assetTable.rows.push([
            i + 1,
            acc.asset, acc.initialMargin, acc.maintMargin, acc.marginBalance,
            acc.maxWithdrawAmount, acc.openOrderInitialMargin, acc.positionInitialMargin,
            acc.unrealizedProfit, acc.walletBalance
        ]);
    }
    var indexTable = {
        type: 'table',
        title: 'Coin index information',
        cols: ['Number', 'Currency information', 'Current price', 'BTC pricing', 'BTC pricing change (%)', 'Deviation from average', 'Number of transactions', 'Number of shorts', 'Number of longs', 'Estimated winning rate'],
        rows: []
    };
    for (var i = 0; i < symbols.length; i++) {
        var price = _N((assets[symbols[i]].ask_price + assets[symbols[i]].bid_price) / 2, trade_info[symbols[i]].priceSize);
        if (symbols.indexOf(symbols[i]) < 0) {
            indexTable.rows.push([i + 1, symbols[i], price, assets[symbols[i]].btc_price, _N((1 - assets[symbols[i]].btc_change) * 100), assets[symbols[i]].btc_diff], 0, 0, 0, '0%');
        } else {
            var rateData = _G("WinRateData");
            var winRate = _N(rateData[symbols[i]].profitNumber / rateData[symbols[i]].totalProfit * 100, 2);
            indexTable.rows.push([
                (i + 1),
                symbols[i] + Warning,
                price,
                _N(assets[symbols[i]].btc_price, 6),
                _N((1 - assets[symbols[i]].btc_change) * 100),
                assets[symbols[i]].btc_diff + (assets[symbols[i]].btc_diff >= 0 ? Success : Danger),
                rateData[symbols[i]].tradeNumber,
                rateData[symbols[i]].sellNumber,
                rateData[symbols[i]].buyNumber,
                (rateData[symbols[i]].profitNumber > 0 && rateData[symbols[i]].totalProfit > 0 ? winRate : '0') + '%' + (winRate >= 50 ? Success : Danger), //Win rate
            ]);
        }
    }
    var retData = {};
    retData.upTable = RunTime.str + '\n' + "Last Update: " + _D() + '\n' + 'Version:' + Version + '\n' + '`' + JSON.stringify([accountTable, assetTable]) + '`\n' + '`' + JSON.stringify(feeTable) + '`\n';
    retData.indexTable = indexTable;
    return retData;
}

function WinRate() {
    for (var i = 0; i < symbols.length; i++) {
        var unrealised = assets[symbols[i]].unrealised_profit;
        WinRateData[symbols[i]].totalProfit += 1;
        if (unrealised != 0) {
            if (unrealised > 0) {
                WinRateData[symbols[i]].profitNumber += 1;
            }
        }
    }
    _G("WinRateData", WinRateData);
}


function tradingCounter(key, newValue) {
    var value = _G(key);
    if (!value) {
        _G(key, newValue);
    } else {
        _G(key, value + newValue);
    }
}

function updateStatus() { //Status bar information
    var table = {
        type: 'table',
        title: 'Trading pair information',
        cols: ['Number', '[Mode][Multiple]', 'Currency Information', 'Opening Direction', 'Opening Quantity', 'Position Price', 'Current Price', 'Liquidation Price', 'Liquidation Difference', 'Position Value', 'Margin', 'Unrealized Profit and Loss', 'Surrender'],
        rows: []
    };
    TotalLong = 0;
    TotalShort = 0;
    for (var i = 0; i < symbols.length; i++) {
        var direction = 'Short position';
        var margin = direction;
        if (assets[symbols[i]].amount != 0) {
            direction = assets[symbols[i]].amount > 0 ? 'go long' + Success : 'go short' + Danger;
            margin = (assets[symbols[i]].marginType == 'cross' ? 'Cross margin : Isolated margin');
        }

        var price = _N((assets[symbols[i]].ask_price + assets[symbols[i]].bid_price) / 2, trade_info[symbols[i]].priceSize);
        var value = _N((assets[symbols[i]].ask_value + assets[symbols[i]].bid_value) / 2, 2);
        if (value != 0) {
            if (value > 0) {
                TotalLong += value;
            } else {
                TotalShort += value;
            }
        }
        // var rateData = _G("WinRateData");
        var infoList = [
            i + 1,
            "[" + margin + "] [" + assets[symbols[i]].leverage + 'x] ',
            symbols[i],
            direction,
            Math.abs(assets[symbols[i]].amount),
            assets[symbols[i]].hold_price,
            price,
            assets[symbols[i]].liquidationPrice, //Forced liquidation price
            assets[symbols[i]].liquidationPrice == 0 ? '0' : '$' + _N(assets[symbols[i]].liquidationPrice - price, 5) + ' ≈ ' + _N(assets[symbols[i]].liquidationPrice / price * 100, 2) + '%' + Warning, //Forced liquidation price
            Math.abs(value),
            _N(assets[symbols[i]].positionInitialMargin, 2),
            // assets[symbols[i]].btc_diff,
            _N(assets[symbols[i]].unrealised_profit, 3) + (assets[symbols[i]].unrealised_profit >= 0 ? Success : Danger),
            // (rateData[symbols[i]].profitNumber > 0 && rateData[symbols[i]].totalProfit > 0 ? _N(rateData[symbols[i]].profitNumber / rateData[symbols[i]].totalProfit * 100, 2) : '0') + '%', //Win rate
            {
                'type': 'button',
                'cmd': 'There was supposed to be no retreat???:' + symbols[i] + ':' + assets[symbols[i]].amount + ':',
                'name': symbols[i] + ' Surrender'
            }
        ];
        table.rows.push(infoList);
    }
    delete assets.USDT.update_time; //Timestamp is useless, discard it
    var logString = JSON.stringify(assets.USDT) + '\n';
    var StatusData = AppendedStatus();
    LogStatus(StatusData.upTable + '`' + JSON.stringify([table, StatusData.indexTable]) + '`\n' + logString);

    if (Date.now() - update_profit_time > Log_profit_interval * 1000) {
        var balance = assets.USDT.margin_balance;
        if (Show) {
            balance = assets.USDT.margin_balance - Funding;
        }
        LogProfit(_N(balance, 3), '&');
        update_profit_time = Date.now();
        if (UpProfit != 0 && (_N(balance, 0) != UpProfit)) { //Do not calculate the first time,Do not calculate win rate for decimal parts
            tradingCounter("totalProfit", 1); //Count the number of prints, winning rate = number of profits/number of prints*100
            if (_N(balance, 0) > UpProfit) {
                tradingCounter("profitNumber", 1); //Number of Wins
            }
            WinRate();
        }
        UpProfit = _N(balance, 0);
    }

}

function stopLoss() { //Stop-loss function
    while (true) {
        if (assets.USDT.margin_balance < Stop_loss * assets.USDT.init_balance && assets.USDT.init_balance > 0) {
            Log('Trigger stop-loss, current funds:', assets.USDT.margin_balance, 'Initial capital:', assets.USDT.init_balance);
            Ice_value = 200; //Stop loss faster, can be modified
            updateAccount();
            updateTick();
            var trading = false; //Is it trading
            for (var i = 0; i < trade_symbols.length; i++) {
                var symbol = trade_symbols[i];
                if (assets[symbol].ask_price == 0) {
                    continue;
                }
                if (assets[symbol].bid_value >= trade_info[symbol].minQty * assets[symbol].bid_price) {
                    trade(symbol, 'sell', assets[symbol].bid_value);
                    trading = true;
                }
                if (assets[symbol].ask_value <= -trade_info[symbol].minQty * assets[symbol].ask_price) {
                    trade(symbol, 'buy', -assets[symbol].ask_value);
                    trading = true;
                }
            }
            Sleep(1000);
            if (!trading) {
                throw 'Stop loss ends. If you need to re-run the strategy, you need to lower the stop loss.';
            }
        } else { //No need for stop-loss
            return;
        }
    }
}

function onTick() { //Strategy logic section
    for (var i = 0; i < trade_symbols.length; i++) {
        var symbol = trade_symbols[i];
        if (assets[symbol].ask_price == 0) {
            continue;
        }
        var aim_value = -Trade_value * _N(assets[symbol].btc_diff / 0.01, 3);
        if (aim_value - assets[symbol].ask_value >= Adjust_value && assets[symbol].btc_diff > Min_diff && assets.USDT.long_value - assets.USDT.short_value <= 1.1 * Trade_value) {
            trade(symbol, 'buy', aim_value - assets[symbol].ask_value);
        }
        if (aim_value - assets[symbol].bid_value <= -Adjust_value && assets[symbol].btc_diff < Max_diff && assets.USDT.short_value - assets.USDT.long_value <= 1.1 * Trade_value) {
            trade(symbol, 'sell', -(aim_value - assets[symbol].bid_value));
        }
    }
}

function main() {
    SetErrorFilter("502:|503:|tcp|character|unexpected|network|timeout|WSARecv|Connect|GetAddr|no such|reset|http|received|EOF|reused|Unknown");
    while (true) {
        RunTime = RuningTime();
        RunCommand(); //Capture interactive commands
        updateAccount(); //Update account and positions
        updateTick(); //Market quotation
        stopLoss(); //stop loss
        onTick(); //Strategy logic section
        updateStatus(); //Output status bar information
        Sleep(Interval * 1000);
    }
}
```

> Detail

https://www.fmz.com/strategy/196784

> Last Modified

2020-05-06 10:45:30
