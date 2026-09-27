
> Name

Price-Amplitude-Moving-Average-330000-Times-Earnings-in-3-Years

> Author

xiaode123





> Source (javascript)

``` javascript
/*backtest
start: 2020-01-01 00:00:00
end: 2023-03-24 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"ETH_USDT","fee":[0.018,0.036]}]
*/

//Addresshttps://www.fmz.com/strategy/405725

const QuotePrecision = 10;//Order price accuracy
const BasePrecision = 10;//Order quantity accuracy

const long = 'long';//go long-futures
const closelong = 'closelong';//go long-Close Position
const short = 'short';//go short-futures
const closeshort = 'closeshort';//go short-Close Position
const isTest = true;//Is it a Binance test?API

const minPriceNum = 2;//Keep a few decimal places (minimum buy/sell price setting is similar)1660.17usdt)
const marginLevel = 1;//Lever size

let lastKLineTime = 0;//The last one to finishkLine timestamp(For example now10:30,That is9point timestamp)

const priceAdd = 0.01;//Changed during transaction1%Set price
let lastOrderTime = 0;//Timestamp of last order placement-second

const serviceCharge = 0.0004;//trading fee0.04%
let signalData = {};//Order data-Used when an order transaction is successful
let maintMarginPro = 0.005;//Maintenance margin ratio0.50%
let maintMarginNum = 0;//Maintain margin quick calculation amount (USDT)

const cfgName1 = "kLine chart";
var registerInfo = {};
var chart = null;
var arrCfg = [];
const maxBufferLen = 10;//

let beginMoney = 0;//Total assets at startup
let exchangeNum = 0;//Number of transactions this time(Open Position+Closing calculation2times)
const lastNumPro_MarketPrice = 0.02;//Because it is difficult to grasp the price using the market price, please leave more space.
const buyMinPro = 0.02;//The remaining money is less than the total amount2%,Do not operate to avoid small trades

let period = 0;//KLine period-second

const atrNum = 6;
const stopKLineNum = 0;//Stop loss occurs,Rest()KLine
const pp = 12;//The larger the number, the smaller the grid gap
const StopGrid = 16;//Stop-loss grid price multiple

let lastStopTime = 0;

const checkTime = 1500;//Check the code every few seconds-1Hour
let lastCheckTime = 0;//Last detection timestamp-second

let currency;
let nowMarkPrice = 0;
let nowPosition;
let nowAccount;

function main() {
    testLog("Callmain");
    let extension = {
        layout: 'single',//single:Charts will not be superimposed (will not be displayed as paging labels), but will be displayed individually (tiled display). The default is grouping. 'group'
        col: 12,//Set the page width of the chart,1-12
        height: '700px'//Chart height
    }
    Sleep(1000);

    while (true) {
        setNowData();
        let bars = _C(exchange.GetRecords);//can only get the latest300data for periods?
        PlotMultRecords(bars, cfgName1, "kLine", extension);//Draw candlestick chart
        drawLine(bars);//Draw SMA line, strategy

        Sleep(1000 * 10);//Run the code every second
    }

}

/** Latest activity data */
function setNowData() {
    setMarkPrice();
    setNowPosition();
    setNowAccount();
}

// Initialization function
function init() {
    _CDelay(1000 * 10);// Adjust the _C() function retry interval to n seconds

    testLog("Initialize!");
    // Set precision (decimal places, not supported in backtesting))
    exchange.SetPrecision(QuotePrecision, BasePrecision);

    exchange.SetContractType("swap");//Perpetual Contract
    if (isTest) {
        exchange.SetBase("https://testnet.binancefuture.com");// Switch to test address
    }
    let arr = exchange.GetCurrency().split('_');//ETH_USDT=>ETH_USDT
    currency = arr[0] + arr[1];
    Log('trading pair:' + currency);

    setNowData();
    log_ticker("Initialize");
    log_account("Initialize");

    beginMoney = getAllMoney();

    chart = Chart(arrCfg);

    period = _C(exchange.GetPeriod);//KLine period
    let periodTxt = getTimeTxt(period);
    testLog("KLine period:" + periodTxt);
}


/** Paintingsmamoving average */
function drawLine(bars) {
    // Test using the spot exchange object, getKLine data. If testing with a futures exchange object, you need to set the contract first
    if (!bars) {
        return;
    }

    if (lastKLineTime == 0) {//First launch, start from scratch
        var begin = atrNum - 1;
    } else {
        begin = bars.length - 2;//In theory, you only need to look at the latest data, but to avoid errors, look2Individual/Unit
    }
    if (begin < 0) {
        return;
    }

    let atr = talib.ATR(bars, atrNum);//Calculate average price amplitude

    for (let i = begin; i < bars.length; i++) {
        let bar = bars[i];
        if (bar.Time <= lastKLineTime) {//Already calculated and plotted
            continue;
        }

        let avg_pra = atr[i] / bar.Close

        let hl2 = (bar.High + bar.Low) / 2;
        //Computational Grid
        let grid = hl2 * avg_pra / pp;
        let p1 = hl2 + grid * StopGrid;
        let p2 = hl2 + grid * 2;
        let p0 = hl2;
        let p3 = hl2 - grid * 2;
        let p4 = hl2 - grid * StopGrid;

        //------------PaintingkLine chart, etc.
        if (i < bars.length - 1) {
            lastKLineTime = bar.Time;
            //The last data point is incomplete, finish drawing
            PlotMultLine(cfgName1, "p1", p1, bar.Time, '#FF9800');
            PlotMultLine(cfgName1, "p2", p2, bar.Time, '#265ec5');
            PlotMultLine(cfgName1, "p0", p0, bar.Time, '#7c7c7c');
            PlotMultLine(cfgName1, "p3", p3, bar.Time, '#265ec5');
            PlotMultLine(cfgName1, "p4", p4, bar.Time, '#FF9800');
            continue;
        }

        //------------Obtained from the last piece of datasmaValue for transaction judgment(forLoop only goes to the last time)
        // ======================== Strategy operations - Start ============================
        if (hasOrder()) {//There are unfinished orders
            return;
        }

        let nowTime = getNowTime();
        if ((lastCheckTime + checkTime) <= nowTime) {
            lastCheckTime = nowTime;//Check the code every few seconds
        } else {
            return;
        }

        if ((lastStopTime + stopKLineNum * period * 1000) > bar.Time) {
            return;
        }

        //Only go long
        if (bar.Close < p4) {
            let funTxt = 'Fun_stop loss';
            let isSuccess = ExchangeFun(closelong, funTxt);
            if (isSuccess) {
                lastStopTime = bar.Time;
            }
        } else if (bar.Close < p3) {
            let funTxt = 'Fun_go long';
            ExchangeFun(long, funTxt);
        } else if (bar.Close > p2) {
            let funTxt = 'Fun_take profit';
            ExchangeFun(closelong, funTxt);
        }
    }
}


/** Are there any unfinished orders */
function hasOrder() {
    let orders = _C(exchange.GetOrders);//Get all unfinished orders
    if (!orders) {
        return true;
    }
    if (orders.length == 0 && signalData && signalData.FunTxt) {
        let order = _C(exchange.GetOrder, signalData.Id);
        if (order) {
            exchangeNum++;
            let nowTime = getNowTime();

            let timeTxtxt = getTimeTxt(nowTime - lastOrderTime);
            let txt = signalData.FunTxt + ',Quotation:' + order.Price + ',Average Price:' + order.AvgPrice
                + ',Amount:' + order.Amount + '%' + ",Frequency:" + exchangeNum
                + ",Action:" + signalData.Action + ",time-consuming:" + timeTxtxt;
            Log("endOrder successful----" + txt);
            log_account("end----");
            PlotMultFlag(cfgName1, "flag1", new Date().getTime(), txt, signalData.FunTxt);
            signalData = {};
        }
    }
    if (orders.length > 0) {
        return true;
    } else {
        return false;
    }
}



//Actual functions like long and short positions
function ExchangeFun(action, funTxt, percent = 1) {
    let amount;
    let tradeInfo;
    let markPrice = getMarkPrice();//Mark price
    if (action == long || action == closeshort) {//Buy
        var price = markPrice * (1 + priceAdd);
    } else if (action == short || action == closelong) {//Sell
        price = markPrice * (1 - priceAdd);
    }
    price = _floor(markPrice, minPriceNum);

    let min = getMinNum();//ethMinimum operation0.001Individual/Unit
    if (action == long) {//go long
        if (!canBuy()) {//Avoid small transactions
            return false;
        }
        amount = getBuyNum(price, 0);//How many to buyeth
        if (amount >= min) {
            beginTrans();
            exchange.SetMarginLevel(marginLevel);//Set the lever size
            exchange.SetDirection("buy");
            tradeInfo = exchange.Buy(-1, amount);//market price
        }
    } else if (action == short) {//go short
        if (!canBuy()) {//Avoid small transactions
            return false;
        }
        amount = getBuyNum(price, 1);//How many units to sell short?eth
        if (amount >= min) {
            beginTrans();
            exchange.SetMarginLevel(marginLevel);//Set the lever size
            exchange.SetDirection("sell");
            tradeInfo = exchange.Sell(-1, amount);
        }
    } else if (action == closelong) {//Close Position-go long
        amount = getCoinNum(0) * percent;//How many futures to selleth
        if (amount >= min) {
            beginTrans();
            exchange.SetDirection("closebuy");
            tradeInfo = exchange.Sell(-1, amount);
        }
    } else if (action == closeshort) {//Close Position-go short
        amount = getCoinNum(1) * percent;
        if (amount >= min) {
            beginTrans();
            exchange.SetDirection("closesell");
            tradeInfo = exchange.Buy(-1, amount);
        }
    }

    if (tradeInfo) {
        signalData = { 'Action': action, 'Id': tradeInfo, 'FunTxt': funTxt };
        log_ticker("end----,OrderAction:" + action + ",price:" + price);
        return true;
    }
    return false;
}


/** Start trading */
function beginTrans() {
    lastOrderTime = getNowTime();
    log_account("bengin----");
}

function log_account(txt) {
    let acc = GetAcc();
    let markPrice = getMarkPrice();

    testLog(txt + ",Available balance:" + acc.Balance + ",Mark price:" + markPrice + ",Account:" + JSON.stringify(acc));

    let position = getNowPosition();
    if (position.length > 0) {
        let data = position[0];//Default position is1Individual/Unit
        let typeTxt = '';
        if (data.Type == 0) {
            typeTxt = 'go long';
        } else if (data.Type == 1) {
            typeTxt = 'go short';
        }
        let leverageTxt = '';
        if (data.Info) {//Not available during backtesting?
            leverageTxt = ",leverage:" + data.Info.leverage;
        }
        testLog("Position information eth:" + data.Amount + ",Price:" + data.Price
            // , ",profit:", data.Profit
            + ",Type:" + typeTxt + leverageTxt + ",Details:" + JSON.stringify(data));
    }
}

/** Obtain account information */
function GetAcc() {
    return nowAccount;
}
/** Set account information */
function setNowAccount() {
    let acc = _C(exchange.GetAccount);
    if (acc.Info) {
        acc.Info.assets = null;
        acc.Info.positions = null;
    }
    nowAccount = acc;
}

function log_ticker(txt) {
    testLog(txt);
}



/** Estimated number that can be purchasedeth 0go long,1go short */
function getBuyNum(price, type) {
    let acc = GetAcc();
    let balance = acc.Balance;//How manyusdt
    if (balance < 100000) {
        maintMarginPro = 0.005;//Maintenance margin ratio
        maintMarginNum = 0;//Maintain margin quick calculation amount (USDT)
    } else if (balance < 250000) {
        maintMarginPro = 0.0065;
        maintMarginNum = 150;
    } else if (balance < 2000000) {
        maintMarginPro = 0.01;
        maintMarginNum = 1025;
    } else if (balance < 10000000) {
        maintMarginPro = 0.02;
        maintMarginNum = 21025;
    } else {
        //Not processed yet
    }
    balance -= maintMarginNum;

    let markPrice = getMarkPrice();//Mark price
    let lossType;//Loss at opening position:Order direction
    //Buy as much as possible, avoid small multiple transactions
    if (type == 0) {//go long
        lossType = 1;
    } else if (type == 1) {//go short
        lossType = -1;
    }
    if (type == 0) {//go long
        var usePrice = price;
    } else if (type == 1) {//go short
        usePrice = Math.max(price, markPrice);
    }

    // Loss at opening position=Contract quantity* Absolute value{min[0, Order direction* (Mark price- Order price)]}
    let losePro = Math.abs(Math.min(0, lossType * (markPrice - price)));

    // Order price: Limit order:The price I set Market order:Sell one
    // Buy Order(go long),Maximum available funds available/{Order price/Leverage multiple+Absolute value(min0,Mark price-Order price)}
    // Sell Order(go short),Maximum available funds available/{max(Mark price, order price)/Leverage multiple+Absolute value(min0,Order price-Mark price)}
    let amount = balance / (usePrice / marginLevel + losePro);//Calculate open position loss

    //Deduct money calculated as total purchase
    amount /= (1 + serviceCharge);//Calculate fees
    amount /= (1 + maintMarginPro);//Calculate maintenance margin
    amount *= (1 - lastNumPro_MarketPrice);//Reserved point
    amount = _floor(amount);

    return amount;
}

/** How many in the futures warehouseeth,type:0Long position,1Short position */
function getCoinNum(type) {
    var position = getNowPosition();
    if (position.length > 0) {
        let data = position[0];//Default position is1Individual/Unit
        // let num = _floor(data.Amount);
        let num = data.Amount;
        if (data.Type == type) {
            return num;
        }
    }
    return 0;
}


/** The remaining money is less than the total amount2%,Do not operate to avoid small trades */
function canBuy() {
    var position = getNowPosition();
    if (position.length > 0) {
        let acc = GetAcc();
        let allMoney = getAllMoney();
        if (acc.Balance / allMoney < (buyMinPro + maintMarginPro)) {
            return false;
        }
    }
    return true;
}

/** Estimate current total assets */
function getAllMoney() {
    let acc = GetAcc();
    let allMoney = acc.Balance;//Available balance
    allMoney += acc.FrozenBalance;//Freeze balance
    var position = getNowPosition();
    if (position.length > 0) {
        let data = position[0];//Default position is1Individual/Unit
        let markPrice = getMarkPrice();

        if (data.Type == 0) {//go long
            allMoney += data.Amount * markPrice;
        } else if (data.Type == 1) {//go short
            allMoney += data.Amount * data.Price;//Principal before shorting
            allMoney += (data.Price - markPrice) * data.Amount;//Short selling profit
        }
    }
    return allMoney;
}


/** Get mark price */
function getMarkPrice() {
    return nowMarkPrice;
}
/** Get mark price */
function setMarkPrice() {
    //Simulated backtest
    let ticker = _C(exchange.GetTicker);//Get market data at most10Minute
    nowMarkPrice = ticker.Last;//Last trading price
}

/** Minimum purchase0.001Individual/Uniteth */
function getMinNum() {
    return 0.001;
}

/** Round down, keep3Decimal places (position size: minimum setting0.001Individual/UnitETH) */
function _floor(num, min = 3) {
    num = Math.floor(num * Math.pow(10, min)) / Math.pow(10, min);
    num = parseFloat(num);//stringTransferFloat
    return num;
}

/** Return current timestamp-second */
function getNowTime() {
    return Unix();
}

/** PaintingkLine Chart */
function PlotMultRecords(bars, cfgName, seriesName, extension) {
    var index = -1;
    var eleIndex = -1;

    do {
        var cfgInfo = registerInfo[cfgName];
        if (typeof (cfgInfo) == "undefined") {
            var cfg = {
                name: cfgName,
                __isStock: true,
                title: {
                    text: cfgName
                },
                tooltip: {
                    xDateFormat: '%Y-%m-%d %H:%M:%S, %A'
                },
                legend: {
                    enabled: true,
                },
                plotOptions: {
                    candlestick: {
                        color: '#d75442',
                        upColor: '#6ba583'
                    }
                },
                rangeSelector: {
                    buttons: [{
                        type: 'hour',
                        count: 1,
                        text: '1h'
                    }, {
                        type: 'hour',
                        count: 3,
                        text: '3h'
                    }, {
                        type: 'hour',
                        count: 8,
                        text: '8h'
                    }, {
                        type: 'all',
                        text: 'All'
                    }],
                    selected: 2,
                    inputEnabled: true
                },
                series: [{
                    type: 'candlestick',
                    name: seriesName,
                    id: seriesName,
                    data: []
                }],
            }

            if (typeof (extension) != "undefined") {
                cfg.extension = extension;
            }

            registerInfo[cfgName] = {
                "cfgIdx": arrCfg.length,
                "seriesIdxs": [{
                    seriesName: seriesName,
                    index: arrCfg.length,
                    type: "candlestick",
                    preBarTime: 0
                }],
            };
            arrCfg.push(cfg);
            updateSeriesIdx();
        }

        chart.update(arrCfg);//Refresh all charts

        _.each(registerInfo[cfgName].seriesIdxs, function (ele, i) {
            if (ele.seriesName == seriesName && ele.type == "candlestick") {
                index = ele.index;
                eleIndex = i;
            }
        });
        if (index == -1) {
            arrCfg[registerInfo[cfgName].cfgIdx].series.push({
                type: 'candlestick',
                name: seriesName,
                id: seriesName,
                data: []
            });
            registerInfo[cfgName].seriesIdxs.push({
                seriesName: seriesName,
                index: arrCfg.length,
                type: "candlestick",
                preBarTime: 0
            });
            updateSeriesIdx();
        }
    } while (index == -1)

    for (var i = 0; i < bars.length; i++) {
        let bar = bars[i];
        let data = [bar.Time, bar.Open, bar.High, bar.Low, bar.Close];//Write a period of data to the chart
        let preBarTime = registerInfo[cfgName].seriesIdxs[eleIndex].preBarTime;
        if (bar.Time == preBarTime) {
            chart.add(index, data, -1);//Update current period
        } else if (bar.Time > preBarTime) {
            registerInfo[cfgName].seriesIdxs[eleIndex].preBarTime = bar.Time
            chart.add(index, data);//Add history(Unchanged)
        }
    }

}

function updateSeriesIdx() {
    var index = 0
    var map = {}
    _.each(arrCfg, function (cfg) {
        _.each(cfg.series, function (series) {
            var key = cfg.name + "|" + series.name
            map[key] = index
            index++
        })
    })

    for (var cfgName in registerInfo) {
        _.each(arrCfg, function (cfg, cfgIdx) {
            if (cfg.name == cfgName) {
                registerInfo[cfgName].cfgIdx = cfgIdx
            }
        })

        for (var i in registerInfo[cfgName].seriesIdxs) {
            var seriesName = registerInfo[cfgName].seriesIdxs[i].seriesName
            var key = cfgName + "|" + seriesName
            if (typeof (map[key]) != "undefined") {
                registerInfo[cfgName].seriesIdxs[i].index = map[key]
            }

            if (registerInfo[cfgName].seriesIdxs[i].type == "candlestick") {
                registerInfo[cfgName].seriesIdxs[i].preBarTime = 0
            } else if (registerInfo[cfgName].seriesIdxs[i].type == "line") {
                registerInfo[cfgName].seriesIdxs[i].preDotTime = 0
            } else if (registerInfo[cfgName].seriesIdxs[i].type == "flag") {
                registerInfo[cfgName].seriesIdxs[i].preFlagTime = 0
            }
        }
    }

    if (!chart) {
        chart = Chart(arrCfg)
    }
    chart.update(arrCfg)
    chart.reset()

    _G("registerInfo", registerInfo)
    _G("arrCfg", arrCfg)

    for (var cfgName in registerInfo) {
        for (var i in registerInfo[cfgName].seriesIdxs) {
            var buffer = registerInfo[cfgName].seriesIdxs[i].buffer
            var index = registerInfo[cfgName].seriesIdxs[i].index
            if (buffer && buffer.length != 0 && registerInfo[cfgName].seriesIdxs[i].type == "line" && registerInfo[cfgName].seriesIdxs[i].preDotTime == 0) {
                _.each(buffer, function (obj) {
                    chart.add(index, [obj.ts, obj.dot])
                    registerInfo[cfgName].seriesIdxs[i].preDotTime = obj.ts
                })
            } else if (buffer && buffer.length != 0 && registerInfo[cfgName].seriesIdxs[i].type == "flag" && registerInfo[cfgName].seriesIdxs[i].preFlagTime == 0) {
                _.each(buffer, function (obj) {
                    chart.add(index, obj.data)
                    registerInfo[cfgName].seriesIdxs[i].preFlagTime = obj.ts
                })
            }
        }
    }
}


function checkBufferLen(buffer, maxLen) {
    while (buffer.length > maxLen) {
        buffer.shift()
    }
}

/** Draw line */
function PlotMultLine(cfgName, seriesName, dot, ts, color, extension) {
    var index = -1;
    var eleIndex = -1;

    do {
        var cfgInfo = registerInfo[cfgName]
        if (typeof (cfgInfo) == "undefined") {
            var cfg = {
                name: cfgName,
                __isStock: true,
                title: {
                    text: cfgName
                },
                xAxis: {
                    type: 'datetime'
                },
                series: [{
                    type: 'line',
                    name: seriesName,
                    id: seriesName,
                    color: color,
                    data: [],
                }]
            };

            if (extension) {
                cfg.extension = extension;
            }

            registerInfo[cfgName] = {
                "cfgIdx": arrCfg.length,
                "seriesIdxs": [{
                    seriesName: seriesName,
                    index: arrCfg.length,
                    type: "line",
                    color: color,
                    buffer: [],
                    preDotTime: 0
                }],
            };
            arrCfg.push(cfg);
            updateSeriesIdx();
        }

        chart.update(arrCfg);

        _.each(registerInfo[cfgName].seriesIdxs, function (ele, i) {
            if (ele.seriesName == seriesName && ele.type == "line") {
                index = ele.index;
                eleIndex = i;
            }
        })
        if (index == -1) {
            arrCfg[registerInfo[cfgName].cfgIdx].series.push({
                type: 'line',
                name: seriesName,
                id: seriesName,
                color: color,
                data: [],
            });
            registerInfo[cfgName].seriesIdxs.push({
                seriesName: seriesName,
                index: arrCfg.length,
                type: "line",
                color: color,
                buffer: [],
                preDotTime: 0
            });
            updateSeriesIdx();
        }
    } while (index == -1)

    if (typeof (ts) == "undefined") {
        ts = new Date().getTime();
    }

    var buffer = registerInfo[cfgName].seriesIdxs[eleIndex].buffer;
    if (registerInfo[cfgName].seriesIdxs[eleIndex].preDotTime != ts) {
        registerInfo[cfgName].seriesIdxs[eleIndex].preDotTime = ts;
        chart.add(index, [ts, dot]);
        buffer.push({
            ts: ts,
            dot: dot
        });
        checkBufferLen(buffer, maxBufferLen);
    } else {
        chart.add(index, [ts, dot], -1);
        buffer[buffer.length - 1].dot = dot;
    }

}

/** Paintingflag */
function PlotMultFlag(cfgName, seriesName, ts, text, title, shape, color, onSeriesName) {
    if (typeof (cfgName) == "undefined" || typeof (registerInfo[cfgName]) == "undefined") {
        throw "need cfgName!";
    }

    var index = -1;
    var eleIndex = -1;

    do {
        chart.update(arrCfg);

        _.each(registerInfo[cfgName].seriesIdxs, function (ele, i) {
            if (ele.seriesName == seriesName && ele.type == "flag") {
                index = ele.index;
                eleIndex = i;
            }
        });
        if (index == -1) {
            arrCfg[registerInfo[cfgName].cfgIdx].series.push({
                type: 'flags',
                name: seriesName,
                onSeries: onSeriesName || arrCfg[registerInfo[cfgName].cfgIdx].series[0].id,
                data: []
            });
            registerInfo[cfgName].seriesIdxs.push({
                seriesName: seriesName,
                index: arrCfg.length,
                type: "flag",
                buffer: [],
                preFlagTime: 0
            });
            updateSeriesIdx();
        }
    } while (index == -1)

    if (typeof (ts) == "undefined") {
        ts = new Date().getTime();
    }

    var buffer = registerInfo[cfgName].seriesIdxs[eleIndex].buffer;
    var obj = {
        x: ts,
        color: color,
        shape: shape,
        title: title,
        text: text
    };
    if (registerInfo[cfgName].seriesIdxs[eleIndex].preFlagTime != ts) {
        registerInfo[cfgName].seriesIdxs[eleIndex].preFlagTime = ts;
        chart.add(index, obj);
        buffer.push({
            ts: ts,
            data: obj
        });
        checkBufferLen(buffer, maxBufferLen);
    } else {
        chart.add(index, obj, -1);
        buffer[buffer.length - 1].data = obj;
    }

}



function testLog(txt) {
    Log(txt);
}

function getNowPosition() {
    return nowPosition;
}
function setNowPosition() {
    nowPosition = _C(exchange.GetPosition);
}

/** Convert time from seconds to days\Hour, etc. */
function getTimeTxt(time) {
    if (time < 60) {
        var timeTxt = time;
        var key = 'second';
    } else if (time < 3600) {
        timeTxt = time / 60;
        key = 'Minute';
    } else if (time < 3600 * 24) {
        timeTxt = time / 3600;
        key = 'Hour';
    } else {
        timeTxt = time / 3600 / 24;
        key = 'Sky/Heaven';
    }
    timeTxt = Math.floor(timeTxt * 10) / 10 + key;//Keep1decimal places
    return timeTxt;
}
```

> Detail

https://www.fmz.com/strategy/405725

> Last Modified

2023-04-19 15:04:59
