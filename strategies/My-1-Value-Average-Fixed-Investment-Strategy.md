
> Name

My-1-Value-Average-Fixed-Investment-Strategy

> Author

Lizza

> Strategy Description

Live trading:https://www.fmz.com/m/robot/26018
This strategy is suitable for fans who are optimistic about Bitcoin in the long term. Using the value average strategy for fixed investment can effectively resist market fluctuations. (For information about value average fixed investment, please contact me.)

The basic idea is to first think about how much money you want to invest every month (strategy variable: MoneyEveryMonth), and then decide how often to trade. The trading interval is not recommended to be less than 5 minutes (strategy parameters:InvestInternal).

The following uses an example to explain the strategy idea and timing of trades:
Suppose you want to buy 72,000 yuan worth of Bitcoin every month (for easy calculation) and trade once every hour. That means you plan to trade 24*30=720 times a month. The planned investment value each time is 72,000/720=100 yuan (variableA).

Hour B, the price at that time was C, the capital D has been invested, the number of coins purchased E, the current currency value F, the capital invested this time G, the number of coins purchased this timeH
1      400     0            0           C*E=0         A*B-F=100         G/C=0.25                   
2      200     100          0.25        200*0.25=50   100*2-50=150      0.75
3     1000     250          1           1000          100*3-1000=-700   -0.7
4     500      -550         0.3         150           100*4-150=250      0.5

The final result was to invest 300 yuan and buy 0.8 Bitcoin (worth 400 yuan), with an average price of 375 yuan.

Note: The program will check the difference between the funds and Bitcoins in the account and when it is started each time to calculate the amount that needs to be purchased each time. Therefore, do not share an account with other robots, and do not perform manual buying and selling operations. If there is recharge and reflection in the exchange, it should be filled in in the interactive part of the program, otherwise the program calculation will be wrong.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|ErrorInterval|2000|Retry on error (milliseconds)|
|InvestInternal|15|Investment interval (calculated in minutes)|
|MoneyEveryMonth|5000|Amount of funds to be invested every month|
|SlidePrice|0.05|Slippage When Buying|




|Button|Default|Description|
|----|----|----|
|Pause|__button__|Pause Trading|
|Continue|__button__|Resume Trading|
|MoneyChange|false|Record fund recharge or withdrawal|
|StockChange|false|Record digital currency recharge or withdrawal|


> Source (javascript)

``` javascript
var initAccount;
var startTime; //unix timestamp
var pause = false; //pause execution of strategy or continue
var moneyDeposit = 0; // positive means deposit, negative means withdraw
var sotckDeposit = 0; // positive means deposit, negative means withdraw

function AdjustFloat(v) {
    return Math.floor(v * 1000)/1000;
}

function GetAccount() {
    var account = null;
    while (!(account = exchange.GetAccount())) {
        Log('Get Account Error');
        Sleep(ErrorInterval);
    }
    return account;
}

function GetCurrentPrice() {
    var ticker = null;
    while (!(ticker = exchange.GetTicker())) {
        Log('Get Ticker Error');
        Sleep(ErrorInterval);
    }
    return AdjustFloat(ticker.Last);
}

function GetOrders(){
    var orders = null;
    while (!(orders = exchange.GetOrders())) {
        Log('Get Orders Error');
        Sleep(ErrorInterval);
    }
    return orders;
}

function CancelPendingOrders() {
    while(true){
        var orders = GetOrders();
        if (orders.length === 0) {
            return;
        }

        for (var i = 0; i < orders.length; i++) {
            exchange.CancelOrder(orders[i].Id);
            if (i < (orders.length-1)) {
                Sleep(ErrorInterval);
            }
        }
    }
}

function ProcessCommand() {
    var command = GetCommand();

    if (command !== null) {
        Log('command:', command);
        if (command === 'pause') {
            pause = true;
        }
        if (command === 'Continue') {
            pause = false;
        }
        if(command.indexOf('MoneyChange:') === 0){
            moneyDeposit += parseFloat(command.replace("MoneyChange:", ""));
            Log('Deposit Money:', moneyDeposit);
        }
        if(command.indexOf('StockChange:') === 0){
            stockDeposit += parseFloat(command.replace("StockChange:", ""));
            Log('Deposit Stock:',stockDeposit);
        }
    }
}

function CaculateMoneyToInvest(currentPrice,investCount)
{
    var moneyEveryInvest = MoneyEveryMonth * InvestInternal / (30 * 24 * 60);
    var totalStockInvested = 0.0;
    var totalMoneyInvested = 0.0;
    var totalValueInvested = 0.0;
    var moneyToInvestThisTime = 0.0;

    CancelPendingOrders();
    var accountNow = GetAccount();
    totalMoneyInvested = initAccount.Balance + initAccount.FrozenBalance + moneyDeposit - accountNow.Balance - accountNow.FrozenBalance;
    totalStockInvested = accountNow.Stocks + accountNow.FrozenStocks - initAccount.Stocks - initAccount.FrozenStocks - stockDeposit;

    Log('Total Money Invested:',totalMoneyInvested);
    Log('Total Stock Invested:',totalStockInvested);

    totalValueInvested = AdjustFloat(totalStockInvested * currentPrice);
    Log('Total Value Invested:',totalValueInvested);

    var averagePrice = 0;
    if(totalStockInvested !== 0){
        averagePrice = AdjustFloat(totalMoneyInvested / totalStockInvested);
    }

    moneyToInvestThisTime = AdjustFloat(moneyEveryInvest * investCount - totalValueInvested);
    Log('Money to Invest This Time:', moneyToInvestThisTime);

    var profit = totalValueInvested - totalMoneyInvested;
    var totalValueNow = (accountNow.Stocks + accountNow.FrozenStocks) * currentPrice + accountNow.Balance + accountNow.FrozenBalance;
    LogStatus('Account Value Now:' + totalValueNow + '\n' + 'Count:',investCount,'  Money:', totalMoneyInvested, 'Stock:', totalStockInvested, 'Average:', averagePrice,'Profit:',profit);
    LogProfit(profit);

    return moneyToInvestThisTime;
}

function onTick(investCount) {
    var currentPrice = GetCurrentPrice();
    Log('Current Price', currentPrice);

    var moneyToInvestThisTime = CaculateMoneyToInvest(currentPrice,investCount);
    var stockToInvestThisTime = 0;
    if(moneyToInvestThisTime > 0){ //Buy
        stockToInvestThisTime = AdjustFloat(moneyToInvestThisTime / (currentPrice + SlidePrice));
    }else{ //Sell
        stockToInvestThisTime = AdjustFloat(moneyToInvestThisTime / (currentPrice - SlidePrice));
    }

    var minPrice = exchange.GetMinPrice();
    if(Math.abs(moneyToInvestThisTime) < minPrice){
        Log('Invest Less Than MinPrice:', minPrice);
        return;
    }

    var minStock = exchange.GetMinStock();
    if(Math.abs(stockToInvestThisTime) < minStock){
        Log('Invest Less Than MinStock:',minStock);
        return;
    }

    var account = GetAccount();
    if(stockToInvestThisTime > 0){ //Buy
        if(account.Balance < moneyToInvestThisTime){
            Log('Money not Enough.#ff0000@');
            return;
        }
    }else{ //Sell
        if(account.Stocks < Math.abs(stockToInvestThisTime)){
            Log('Stock not Enough.#ff0000@');
            return;
        }
    }

    var orderID = -1;
    if(stockToInvestThisTime > 0){ //Buy
        Log('Buy Stock:',stockToInvestThisTime);
        orderID = exchange.Buy(currentPrice + SlidePrice,stockToInvestThisTime);
    }

    if(stockToInvestThisTime < 0){ //Sell
        Log('Sell Stock:',Math.abs(stockToInvestThisTime));
        orderID = exchange.Sell(currentPrice - SlidePrice,Math.abs(stockToInvestThisTime));
    }


}

function main() {
    //exchange.IO("websocket");
    initAccount = _G('InitAccount');
    if(initAccount === null){
        initAccount = GetAccount();
        _G('InitAccount',initAccount);
        Log('Set Init account.');
        Log(exchange.GetName(), exchange.GetCurrency(), initAccount);
    }
    else{
        Log('Read Init Account:', initAccount);
    }

    startTime = _G('StartTime');
    if(startTime === null){
        startTime = new Date().getTime();
        _G('StartTime',startTime);
        Log('Set Start Time:', startTime);
    }else{
        Log('Read Start Time',new Date().setTime(startTime));
    }

    var investCount = _G('InvestCount' );
    if(investCount === null){
        investCount = 1;
        Log('Set Invest Starting from Count 1.');
    }
    else{
        Log('Invest Continuing from:', investCount);
    }

    moneyDeposit = _G('MoneyDeposit');
    if(moneyDeposit === null){
        moneyDeposit = 0;
        Log('Set Money Deposit 0.');
    }
    else{
        Log('Read Money Deposit:', moneyDeposit);
    }

    stockDeposit = _G('StockDeposit');
    if(stockDeposit === null){
        stockDeposit = 0;
        Log('Set Stock Deposit 0.');
    }
    else{
        Log('Read Stock Deposit:', stockDeposit);
    }

    while (true) {
        ProcessCommand();
        if (!pause) {
            Log('=================================================');
            Log('Invest Count', investCount);
            onTick(investCount);
            investCount += 1;
            _G('InvestCount',investCount);
        }
        Sleep(InvestInternal * 1000 * 60);
    }
}

function onexit(){
    _G('MoneyDeposit',moneyDeposit);
    _G('StockDeposit', stockDeposit);

    Log('Robot Stopped!#ff0000@');
}
```

> Detail

https://www.fmz.com/strategy/8602

> Last Modified

2016-06-14 10:42:59
