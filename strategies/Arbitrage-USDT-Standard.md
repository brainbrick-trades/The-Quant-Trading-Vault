
> Name

Arbitrage-USDT-Standard

> Author

AutoBitMaker-ABM

> Strategy Description

Self-learning grid:

Self-learning grids are based on traditional grid strategies, but after long-term live trading and backtesting data, dozens of parameter configurations such as opening logic, timing of additional positions, take-profit levels, position ratio, and grid spacing have been optimized. An intelligent dynamic additional position model and take-profit positions have been implemented, which can avoid the high risks that traditional grids face in one-sided market situations, achieving good return-to-drawdown ratios with very low positions.

The strategy configuration parameters are extremely rich. The team will assign dedicated personnel to customize a unique parameter combination for your account based on customer risk and return needs, and have all-weather manual + automated market monitoring.

We have self-developed a unique index trading collection. Each index trading collection contains a variety of high-quality single trading pairs, and each trading pair has a unique weight ratio. The robot runs a self-learning grid strategy on the index set to avoid the unilateral risk of a single trading pair.
In addition to the built-in static index, we define dynamic indexes of multiple currency selection models for the index set, and select the leading currencies in each section to form an index level to further reduce risks.

A single account can be configured to run multiple single-currency trading pairs and index trading pairs at the same time, which can not only share risks but also help you make profits in various complex market conditions.

About optimization + risk control:
The historical backtesting server operates year-round, automatically backtesting all the latest data and calculating optimal parameters in real time.
Our strategy cluster contains more than 50 auxiliary servers, which check the stop-loss conditions of the account at an average speed of 2 times per second, so that we can exit quickly when risks come.

Using the heterogeneous hybrid cloud architecture of Alibaba Cloud, Amazon Cloud, and Microsoft Cloud, the management and execution nodes are separated, and clusters are formed between multiple nodes to ensure redundancy, thereby safely and effectively achieving the smooth operation of the business and ensuring the security of funds.

About Trial:
Depending on your capital size, we provide a trial run of about 2 weeks. During the trial period, we do not charge commissions.
Bot After taking over your account, please do not do any operations on your own. When any other manual positions are detected, all Bots will exit immediately.

About Commission:
This depends on your bankroll. We can talk more about it after the trial run. If you create an account using our referral link, we will charge a low commission.

Contact Information:
WeChat:DuQi_SEC/autobitmaker/Shawn_gb2312/ABM_DD
Email:  liuhongyu.louie@autobitmaker.com/autobitmaker_master@autobitmaker.com

Submit trial application via WeChat Mini Program:
![WeChat mini program code](https://www.fmz.cn![IMG](https://www.fmz.com/upload/asset/1281e73989f891ac26aa9.jpg))

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|baseOriginalBalance|1000|baseOriginalBalance|
|showInfo|false|showInfo|


> Source (javascript)

``` javascript
var chart = {
    __isStock: false,
    extension: {
        layout: 'single',
        col: 8,
        height: '300px'
    },
    tooltip: {
        xDateFormat: '%Y-%m-%d %H:%M:%S, %A'
    },
    title: {
        text: 'Account_Balance_Detail'
    },
    xAxis: {
        type: 'datetime'
    },
    yAxis: {
        title: {
            text: 'USDT'
        },
        opposite: false
    },
    series: []
};

function initChart() {
    chart.series.push({
        name: "Account_" + (Number(0)) + "_Detail",
        id: "Account_" + (Number(0)) + "_Detail",
        data: []
    });
}

function getChartPosition(avaliableMargin) {
    return {
        __isStock: false,
        extension: {
            layout: 'single',
            col: 4,
            height: '300px'
        },
        title: {
            text: 'Margin ratio(%)'
        },
        series: [{
            type: 'pie',
            name: 'one',
            data: [{
                name: 'Available Margin(%)',
                y: avaliableMargin,
                color: '#dff0d8',
                sliced: true,
                selected: true
            }, {
                name: 'Margin occupation(%)',
                y: 100 - avaliableMargin,
                color: 'rgb(217, 237, 247)',
                sliced: true,
                selected: true
            }]
        }]
    };
}

function updateAccountDetailChart(ObjChart) {
    var nowTime = new Date().getTime();
    var account = exchanges[0].GetAccount();
    try {
        if (account !== null && account.Info !== null && account.Info.totalMarginBalance > 0) {
            ObjChart.add([0, [nowTime, Number(account.Info.totalMarginBalance)]]);
        }
    } catch (err) {
        Log('ERROR ' + account + ',' + err)
    }
}

function getBalance() {
    var currentBalance = 0;
    var account = exchanges[0].GetAccount();
    try {
        if (account !== null && account.Info !== null && account.Info.totalWalletBalance > 0) {
            currentBalance += Number(account.Info.totalWalletBalance);
        }
    } catch (err) {
        Log('ERROR ' + account + ',' + err)
    }
    Sleep(666);
    return Number(currentBalance).toFixed(6);
}

function getMarginBalance() {
    var currentBalance = 0;
    var account = exchanges[0].GetAccount();
    try {
        if (account !== null && account.Info !== null && account.Info.totalMarginBalance > 0) {
            currentBalance += Number(account.Info.totalMarginBalance);
        }
    } catch (err) {
        Log('ERROR ' + account + ',' + err)
    }
    Sleep(666);
    return Number(currentBalance).toFixed(6);
}

function printProfitInfo(currentBalance) {
    var profit = Number((currentBalance) - baseOriginalBalance).toFixed(5);
    var profitRate = Number((((currentBalance) - baseOriginalBalance) / baseOriginalBalance) * 100).toFixed(4);
    LogProfit(Number(profitRate), '&');
    Log('The current balance is ' + currentBalance + ', the profit is ' + profit + ', the profit rate is ' + profitRate + '%');
}

function printPositionInfo(exchangeInnerArray, totalProfitUSDT, totalProfitRate) {
    var totalProfit = 0.0
    var table = {
        type: 'table',
        title: 'POSITIONS',
        cols: ['Symbol', 'Type', 'AvgPrice', 'Position', 'Profit'],
        rows: []
    }
    if (showInfo) {
        table.rows.push([{
            body: '* 2020-09-07 Previously, the RMB 1 million real offer was running. Now the strategy has been updated to automatically transfer the idle funds of the contract to Binance Treasure, which not only improves the security of funds, but also makes bilateral profits. When the required margin of the contract increases or decreases, the balances on both sides will be automatically adjusted. Since FMZ is currently unable to monitor the balance of Binance Treasure, it stripped off the 10W RMB and continued to run the original strategy for demonstration purposes.',
            colspan: 5
        }]);
    }
    table.rows.push([{
        body: 'This strategy is USDT-based, a Binance contract arbitrage strategy based on mean reversion, and assisted by low-risk grid parallelism (BitMEX supports BTC-based)',
        colspan: 5
    }]);
    table.rows.push([{
        body: 'The main arbitrage currencies are BTC/USDT and ETH/USDT, and the grid covers all currency trading pairs of Binance perpetual contracts.',
        colspan: 5
    }]);
    for (var index in exchangeInnerArray) {
        var position = exchangeInnerArray[index].GetPosition()
        for (var indexInner in position) {
            var profit = Number(position[indexInner].Info.unRealizedProfit);
            totalProfit = totalProfit + profit
            table.rows.push([position[indexInner].Info.symbol, (position[indexInner].Type == 1 ? 'SHORT #da1b1bab' : 'LONG #1eda1bab'), position[indexInner].Price, position[indexInner].Amount, profit.toFixed(5)]);
        }
        Sleep(168);
    }
    table.rows.push([{
        body: 'TOTAL PROFIT OF CURRENT POSITION',
        colspan: 4
    }, totalProfit.toFixed(6) + ' USDT']);
    table.rows.push([{
        body: 'TOTAL PROFIT',
        colspan: 4
    }, totalProfitUSDT + ' USDT']);
    table.rows.push([{
        body: 'TOTAL PROFIT RATE',
        colspan: 4
    }, totalProfitRate + ' %']);
    LogStatus('`' + JSON.stringify(table) + '`');
}

function main() {
    initChart();
    var ObjChart = Chart([chart, getChartPosition(100)]);
    while (true) {
        try {
            var currentBalance = getBalance();
            printProfitInfo(currentBalance);
            updateAccountDetailChart(ObjChart);
            for (var i = 0; i < 120; i++) {
                try {
                    var avaliableMargin = ((getMarginBalance()) / (getBalance())) * 100;
                    ObjChart.update([chart, getChartPosition(avaliableMargin)]);
                    var profit = Number((currentBalance) - baseOriginalBalance).toFixed(5);
                    var profitRate = Number((((currentBalance) - baseOriginalBalance) / baseOriginalBalance) * 100).toFixed(4);
                    printPositionInfo(exchanges, profit, profitRate);
                    Sleep(1000 * 120);
                } catch (errInner) {
                    throw errInner;
                }
            }
        } catch (err) {
            throw err;
        }
    }
}
```

> Detail

https://www.fmz.com/strategy/178712

> Last Modified

2021-01-07 08:40:45
