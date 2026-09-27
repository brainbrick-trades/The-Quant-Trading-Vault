
> Name

Binance-New-Trading-Pair-Launch-Monitoring

> Author

ChaoZhang





> Source (javascript)

``` javascript


let SaveSymbol = _G("SaveSymbol") || [];
//Define a variable,Save projects that have already been notified
var Notified = _G("Notified") || [];

function TimeBetween(startDate, endDate) {
    let delta = Math.abs(endDate - startDate) / 1000;
    const isNegative = startDate > endDate ? -1 : 1;
    return [
        ["days", 24 * 60 * 60],
        ["hours", 60 * 60],
        ["minutes", 60],
        ["seconds", 1],
    ].reduce((acc, [key, value]) => ((acc[key] = Math.floor(delta / value) * isNegative), (delta -= acc[key] * isNegative * value), acc), {});
}
function getLaunchpad() {
    var Launchpad = {
        coming: {}, //Upcoming projects
        tracking: {}, //Ongoing projects
    };
    let data = HttpQuery("https://launchpad.binance.com/bapi/lending/v1/friendly/launchpool/project/listV3?pageIndex=1&pageSize=5");
    if (!data) {
        Log("Failed to obtain data");
        return false;
    }
    try {
        data = JSON.parse(data);
    } catch (e) {
        Log("ParseJSONData failed: ", e.message, "Raw Data: ", data);
        return false;
    }
    // return data
    if (!data.data) {
        Log("DataError", data)
        return false;
    }
    let tracking = data.data.tracking;
    let coming = data.data.coming;
    for (let i = 0; i < tracking.length; i++) {
        let item = tracking[i];
        if (!Launchpad.tracking[item.rebateCoin]) {
            Launchpad.tracking[item.rebateCoin] = item;
            //If there has been no notification,Then notify
            // if (Notified.indexOf(item.rebateCoin) == -1) {
            //     Notified.push(item.rebateCoin);
            //     Log("Found a new project in mining", item.rebateCoin, item.detailAbstract);
            // }
            // Log("New mining projects", item.rebateCoin, item.detailAbstract);
        }
    }
    if (coming.length > 0) {
        // Log("Upcoming projects", coming.length, coming);
        for (let i = 0; i < coming.length; i++) {
            let item = coming[i];
            if (!Launchpad.coming[item.rebateCoin]) {
                Launchpad.coming[item.rebateCoin] = item;
                //If there has been no notification,Then notify
                if (Notified.indexOf(item.rebateCoin) == -1) {
                    Notified.push(item.rebateCoin);
                    Log("Found that a new project is about to start", item.rebateCoin, item.detailAbstract, "@");
                }
                // Log("New project about to start", item.rebateCoin, item.detailAbstract);
            }
        }
    }
    return Launchpad;
}
function onTick() {
    // Get exchange information
    let exchangeInfo = exchange.IO("api", "GET", "/fapi/v1/exchangeInfo");
    let symbolList = exchangeInfo.symbols;

    // Initialize trading pair information table
    let symbolTable = {
        type: "table",
        title: "Coin information",
        cols: ["Numbering, "Currency", "Trading Pair", "Delivery Date", "Launch Date""],
        rows: [],
    };
    let trackingTable = {
        type: "table",
        title: "Mining",
        cols: ["Currency", "Total reward", "Mining cycle", "Start time", "End time", "Remaining time", "Status"],
        rows: [],
    };
    let comingTable = {
        type: "table",
        title: "About to start",
        cols: ["Cryptocurrency, "Total Rewards", "Mining Cycle", "Start Time", "End Time", "Countdown to Launch""],
        rows: [],
    };
    let Launchpad = getLaunchpad();
    for (let key in Launchpad.tracking) {
        let item = Launchpad.tracking[key];
        let row = [
            item.rebateCoin, //Currency
            _N(parseInt(item.rebateTotalAmount), 0),
            item.duration + " Sky/Heaven",
            _D(parseInt(item.investStartTime)), //Format as Beijing time
            _D(parseInt(item.mineEndTime)),
            //Remaining time countdown,Calculation method: end time-Current Time,End time is a millisecond timestamp
            JSON.stringify(TimeBetween(Date.now(), item.mineEndTime)),
            item.status,
        ];
        trackingTable.rows.push(row);
    }
    for (let key in Launchpad.coming) {
        let item = Launchpad.coming[key];
        let row = [
            item.rebateCoin, //Currency
            _N(parseInt(item.rebateTotalAmount), 0),
            item.duration + " Sky/Heaven",
            _D(parseInt(item.investStartTime)), //Format as Beijing time
            _D(parseInt(item.mineEndTime)),
            //Remaining time countdown,Calculation method: end time-Current Time,End time is a millisecond timestamp
            Math.floor((item.investStartTime - Date.now()) / 1000 / 3600) + " Hour",
        ];
        comingTable.rows.push(row);
    }
    let isNewRun = SaveSymbol.length === 0;
    let symbolCount = 0;

    // Iterate through the trading pair list and filter
    symbolList.forEach((symbol) => {
        // Filter criteria: In transaction, perpetual contract, quote currency isUSDT,Non-exponential type
        if (symbol.status === "TRADING" && symbol.contractType === "PERPETUAL" && symbol.quoteAsset === "USDT" && symbol.underlyingType !== "INDEX") {
            // Add eligible trading pairs to the table
            symbolTable.rows.unshift([
                ++symbolCount, // Number
                symbol.baseAsset,
                symbol.symbol,
                _D(symbol.deliveryDate),
                _D(symbol.onboardDate),
            ]);

            // Check and record new trading pairs
            if (!SaveSymbol.includes(symbol.symbol)) {
                SaveSymbol.push(symbol.symbol);
                if (!isNewRun) {
                    Log("Add new trading pair", symbol.symbol, "@");
                }
            }
        }
    });

    // Record trading pair information table
    LogStatus("`" + JSON.stringify([trackingTable, comingTable, symbolTable]) + "`");
}

function main() {
    while (true) {
        try {
            onTick();
            Sleep(1000 * 60 * 1);
        } catch (e) {
            Log("e.name:", e.name, "e.stack:", e.stack, "e.message:", e.message)
        }
    }
}
function saveData() {
    _G("SaveSymbol", SaveSymbol);
    _G("Notified", Notified);
}
function onexit() {
    saveData();
}
function onerror() {
    saveData();
}

```

> Detail

https://www.fmz.com/strategy/439766

> Last Modified

2024-04-11 22:05:30
