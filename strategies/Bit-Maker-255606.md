
> Name

Bit-Maker-255606

> Author

AutoBitMaker-ABM

> Strategy Description

**AutoBitMaker** Currently officially launched risk-free arbitrage strategy.
The strategy principle is hedging between spot and futures, which can also be done manually.
However, compared to manual operation, BOT will capture the profit margins of all trading pairs in the market and conduct hundreds of transactions every day. Free up your hands and reduce market risks.

The current code is only for account monitoring. The source code is published. You can check it yourself or use it.
Monitor spot USDT value.

We are **AutoBitMaker**, referred to as **ABM Capital**. Please carefully identify the team name and WeChat ID to identify the authenticity.
We currently only communicate with domestic customers through WeChat and Email contact methods, and do not use other methods such as QQ.

**ABM Team**Currently Available3types of strategies
* Contract Trading
* Spot trading
* Arbitrage Trading

Self-learning grids are based on traditional grid strategies, but after long-term live trading and backtesting data, dozens of parameter configurations such as opening logic, timing of additional positions, take-profit levels, position ratio, and grid spacing have been optimized. An intelligent dynamic additional position model and take-profit positions have been implemented, which can avoid the high risks that traditional grids face in one-sided market situations, achieving good return-to-drawdown ratios with very low positions.

The strategy configuration parameters are extremely rich. The team will assign dedicated personnel to customize a unique parameter combination for your account based on customer risk and return needs, and have all-weather manual + automated market monitoring.

We have self-developed a unique index trading collection. Each index trading collection contains a variety of high-quality single trading pairs, and each trading pair has a unique weight ratio. The robot runs a self-learning grid strategy on the index set to avoid the unilateral risk of a single trading pair.
In addition to the built-in static index, we define dynamic indexes of multiple currency selection models for the index set, and select the leading currencies in each section to form an index level to further reduce risks.

A single account can be configured to run multiple single-currency trading pairs and index trading pairs at the same time, which can not only share risks but also help you make profits in various complex market conditions.

Currently, the team's strategy server cluster has reached 80 units, with more than 50 supporting servers. They check account stop-loss conditions at an average rate of 2 times per second, allowing for a quick exit when risks arise.

Using the heterogeneous hybrid cloud architecture of Alibaba Cloud, Amazon Cloud, and Microsoft Cloud, the management and execution nodes are separated, and clusters are formed between multiple nodes to ensure redundancy, thereby safely and effectively achieving the smooth operation of the business and ensuring the security of funds.

About Trial:
Depending on your capital size, we provide a trial run of about 2 weeks. During the trial period, we do not charge commissions.
Bot After taking over your account, please do not do any operations on your own. When any other manual positions are detected, all Bots will exit immediately.

About Commission:
This depends on your bankroll. We can talk more about it after the trial run. If you create an account using our referral link, we will charge a low commission.

Contact Information:
1. Interviews are available nationwide
2. WeChat:DuQi_SEC/autobitmaker/autobitmaker_001/Shawn_gb2312/ABM_DD 
3. Email:  liuhongyu.louie@autobitmaker.com/autobitmaker_master@autobitmaker.com

* Special reminder (WeChat ID autobitmaker001 is not us!! We are not called makebit!! WeChat ID autobitmaker_001 is us)

Submit trial application via WeChat Mini Program:
![WeChat mini program code](https://www.fmz.cn![IMG](https://www.fmz.com/upload/asset/1281e73989f891ac26aa9.jpg))

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|baseOriginalBalance|10000|baseOriginalBalance|


> Source (javascript)

``` javascript
//exchanges[0] is spot

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

function updateAccountDetailChart(ObjChart, totalBalance) {
    var nowTime = new Date().getTime();
    var account = exchanges[0].GetAccount();
    try {
        if (account !== null && account.Info !== null && totalBalance > 0) {
            ObjChart.add([0, [nowTime, Number(totalBalance)]]);
        }
    } catch (err) {
        Log('ERROR ' + account + ',' + err)
    }
}

function getSpotBalanceInUSDT() {
    var ticker = JSON.parse(HttpQuery('https://api.binance.com/api/v1/ticker/24hr'));
    var currentBalance = 0;
    var account = exchanges[0].GetAccount();
    var priceMap = {};
    try {
        if (ticker !== null) {
            for (var index in ticker) {
                priceMap[ticker[index].symbol] = ticker[index].lastPrice;
            }
        }
        if (account !== null && account.Info !== null) {
            for (var index in account.Info.balances) {
                var obj = account.Info.balances[index];
                if (obj.asset !== 'USDT' && priceMap[obj.asset + 'USDT']) {
                    currentBalance += Number(Number(priceMap[obj.asset + 'USDT']) * Number((Number(obj.free) + Number(obj.locked))));
                }
                if (obj.asset === 'USDT') {
                    currentBalance += Number((Number(obj.free) + Number(obj.locked)));
                }
            }
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
        cols: ['Symbol', 'Type', 'CurrentPrice', 'Position', 'USDT Value'],
        rows: []
    }
    table.rows.push([{
        body: 'This strategy is USDT-based, low-risk spot smart dynamic parameter grid',
        colspan: 5
    }]);
    table.rows.push([{
        body: 'Any trading pair',
        colspan: 5
    }]);
    var ticker = JSON.parse(HttpQuery('https://api.binance.com/api/v1/ticker/24hr'));
    var account = exchanges[0].GetAccount();
    var priceMap = {};
    try {
        if (ticker !== null) {
            for (var index in ticker) {
                priceMap[ticker[index].symbol] = ticker[index].lastPrice;
            }
        }
        if (account !== null && account.Info !== null) {
            for (var index in account.Info.balances) {
                var obj = account.Info.balances[index];
                if (obj.asset !== 'USDT' && priceMap[obj.asset + 'USDT']) {
                    if (Number((Number(obj.free) + Number(obj.locked))) > 0) {
                        table.rows.push([obj.asset, ('LONG #1eda1bab'), Number(priceMap[obj.asset + 'USDT']), Number((Number(obj.free) + Number(obj.locked))), Number(Number(priceMap[obj.asset + 'USDT']) * Number((Number(obj.free) + Number(obj.locked)))).toFixed(4)]);
                    }
                }
            }
        }
    } catch (err) {
        Log('ERROR ' + account + ',' + err)
    }
    Sleep(168);
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
            var currentSpotBalance = getSpotBalanceInUSDT();
            var totalBalance = Number(currentSpotBalance).toFixed(4);
            printProfitInfo(totalBalance);
            updateAccountDetailChart(ObjChart, totalBalance);
            for (var i = 0; i < 120; i++) {
                try {
                    var avaliableMargin = 100;
                    ObjChart.update([chart, getChartPosition(avaliableMargin)]);
                    var profit = Number((totalBalance) - baseOriginalBalance).toFixed(5);
                    var profitRate = Number((((totalBalance) - baseOriginalBalance) / baseOriginalBalance) * 100).toFixed(4);
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

https://www.fmz.com/strategy/255606

> Last Modified

2021-02-20 11:36:38
