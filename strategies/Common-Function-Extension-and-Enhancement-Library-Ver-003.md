
> Name

Common-Function-Extension-and-Enhancement-Library-Ver-003

> Author

ChaoZhang





> Source (javascript)

``` javascript
/*
 * @Project: Official Extended Enhancement Library
 * @Version: Ver 0.0.3
 * @Author: RedSword <redsword@gmail.com>
 * @Description:Collect and organize commonly used enhancement functions
 * @Date: 2021-05-06 11:02:29
 * @LastEditors: RedSword
 * @LastEditTime: 2021-09-07 11:35:52
 * @Copyright:: Copyright © 2020 FMZ Quant
 * Code specification reference: https://github.com/fex-team/styleguide/blob/master/javascript.md
 */

/* jshint esversion: 6 */
/**
 * @Title: Convert to Beijing Time
 * @description: Convert the server time where the host is located to Beijing time
 * @param {time} localtime time
 * @return {time} Beijing time
 * @example
 *  var localDate = $.ToBJTime(new Date());
 *  Log(localDate)  //Thu May 06 2021 11:19:45 GMT+0000
 *  Log(localDate.getTime())    //1620299985696
 */
$.ToBJTime = function (localDate) {
    return new Date(localDate.getTime() + localDate.getTimezoneOffset() * 60000 + 3600000 * 8);
};

/**
 * Format the date into a string in the specified format
 * @param date The date to be formatted. If not passed, it defaults to the current time, or it can be a timestamp.
 * @param fmt Target string format, supported characters include: y, M, d, q, w, H, h, m, S, by default.:yyyy-MM-dd HH:mm:ss
 * @returns Returns the formatted date string
 */
$.FormatDate = function (date, fmt) {
    date = !date ? new Date() : date;
    date = typeof date === "number" ? new Date(date) : date;
    fmt = fmt || "yyyy-MM-dd HH:mm:ss";
    var obj = {
        y: date.getFullYear(), // Year, Note Must UsegetFullYear
        M: date.getMonth() + 1, // Month, note that it starts from0-11
        d: date.getDate(), // Date
        q: Math.floor((date.getMonth() + 3) / 3), // Quarter
        w: date.getDay(), // Week, note it is0-6
        H: date.getHours(), // 24Hour format
        h: date.getHours() % 12 == 0 ? 12 : date.getHours() % 12, // 12Hour format
        m: date.getMinutes(), // Minute
        s: date.getSeconds(), // second
        S: date.getMilliseconds(), // Millisecond
    };
    var week = ["Sky/Heaven", "One", "Two", "Three", "Four", "Five", "Six"];
    for (var i in obj) {
        fmt = fmt.replace(new RegExp(i + "+", "g"), function (m) {
            var val = obj[i] + "";
            if (i == "w") return (m.length > 2 ? "Week" : "week") + week[val];
            for (var j = 0, len = val.length; j < m.length - len; j++) val = "0" + val;
            return m.length == 1 ? val : val.substring(val.length - m.length);
        });
    }
    return fmt;
};
/**
 * @Title: Get permanent cache
 * @description:Write to cache if it doesn't exist; if it exists, return the data, generally used to record the initial price.
 * @param {string} key Unique identifier
 * @param {*} data Data to be saved
 * @return {*}
 *
 */
$.ForeverCache = function (key, data) {
    key = "ForeverCache" + key;
    var getDate = _G(key);
    if (getDate == null) {
        _G(key, data);
        return data;
    }
    return getDate;
};

/**
 * @title: Cache for the day
 * @description:Get the cache of the day and reset the data at 0:00 Beijing time every day
 * @param {string} key Unique identifier
 * @param {*} data Data to be saved
 * @return {*}
 */
$.TodayCache = function (key, data) {
    key = "TodayCache" + key;
    var today = $.ToBJTime(new Date()).getDate();
    if (_G("TodayCacheToday_" + key) !== today) {
        _G("TodayCacheToday_" + key, today);
        _G(key, data);
        return data;
    } else {
        return _G(key);
    }
};

/**
 * @title: Scheduled function
 * @description: Specify the time interval to execute the function
 * @param {int} second Interval time, in seconds
 * @param {string} key Logo
 * @param {function} fun Function to execute
 * @return {*} Result of scheduled function execution
 * @example
 * //Execute the nowTime() function once every 60 seconds
 * Log($.ExecuteFuncForTime(60,"myTime",nowTime))
 */
$.ExecuteFuncForTime = function (second, key, fun) {
    var endSecond = second * 1000;
    var nowTime = new Date().getTime();
    if (_G("funcForTime_" + key) == null || nowTime - _G("funcForTime_" + key) > endSecond) {
        var data = fun();
        _G("funcForTime_" + key, nowTime);
        _G(key, data);
        return data;
    } else {
        return _G(key);
    }
};

/**
 * @title: ObjectSort
 * @description:Sort Object according to the specified identifier
 * @param {object} obj Object to be sorted
 * @param {string} key identifier
 * @return {object}
 * @example
 *  var obj = { aa: { f: 2 }, bb: { f: 1 }, cc: { f: 3 } };
 *	Log(sortobjkey(obj,'f')) //{"cc":{"f":3},"aa":{"f":2},"bb":{"f":1}}
 */
$.SortObjectKey = function (obj, key) {
    var o = {};
    Object.keys(obj)
        .map(function (k, i) {
            return [k, obj[k]];
        })
        .sort(function (a, b) {
            k = key;
            if (a[1][k] > b[1][k]) return -1;
            if (a[1][k] < b[1][k]) return 1;
            return 0;
        })
        .forEach(function (a) {
            o[a[0]] = a[1];
        });
    return o;
};

/**
 * @title:Strategy running time
 * @description:Record the first running time and calculate the number of running times
 * @return {object} Object
 * @example
 * Log($.RunTime())
 * //{"RunSeconds":18170,"NowUnix":1622821609901,"NowTime":"2021-06-04 23:46:49","FormatTime":"Running time: 0 days 5 hours 2 minutes 50 seconds","StartTime":"2021-06-04 18:43:59"}
 */
$.RunTime = function () {
    var startTime = new Date($.ForeverCache("startTime", new Date()));
    var between = $.TimeBetween(startTime, new Date());
    var timestamp = parseInt(UnixNano() / 1000000);
    let week = $.GetWeek($.ToBJTime(new Date()));
    return {
        RunSeconds: parseInt((timestamp - startTime.getTime()) / 1000), //Running seconds
        NowUnix: timestamp, //Current Timestamp
        NowTime: _D($.ToBJTime(new Date())), //Current Time
        NowYear: week.year,
        NowMonth: week.month,
        NowDay: week.day,
        NowWeek: week.week,
        FormatTime: "Running time: " + between.days + " Sky/Heaven " + between.hours + " hour " + between.minutes + " Minute " + between.seconds + " second", //Formatted run time
        StartTime: _D($.ToBJTime(startTime)), //Start time
        StartUnix: $.ForeverCache("StartUnix", timestamp),
    };
};

$.TimeBetween = function (startDate, endDate) {
    let delta = Math.abs(endDate - startDate) / 1000;
    const isNegative = startDate > endDate ? -1 : 1;
    return [
        ["days", 24 * 60 * 60],
        ["hours", 60 * 60],
        ["minutes", 60],
        ["seconds", 1],
    ].reduce((acc, [key, value]) => ((acc[key] = Math.floor(delta / value) * isNegative), (delta -= acc[key] * isNegative * value), acc), {});
};
$.GetAnalyze = function (totalAssets) {
    var sqlDB;
    try {
        sqlDB = DBExec("select * from profit");
    } catch (error) {
        return false;
    }

    var profits = sqlDB.values;
    if (profits.length == 0) {
        return {
            totalAssets: totalAssets,
            yearDays: 0,
            totalReturns: 0,
            annualizedReturns: 0,
            sharpeRatio: 0,
            volatility: 0,
            nowDrawdown: 0,
            maxDrawdown: 0,
            maxDrawdownTime: 0,
            maxAssetsTime: 0,
            maxDrawdownStartTime: 0,
            winningRate: 0,
            nowDrawdownFormat: {
                days: 0,
                hours: 0,
                minutes: 0,
                seconds: 0,
            },
            maxDrawdownFormat: {
                days: 0,
                hours: 0,
                minutes: 0,
                seconds: 0,
            },
        };
    }
    var yearDays = 365;
    // force by days
    var period = 86400000;
    //Log(profits[0], profits[10]);
    var ts = profits[0][3];
    var te = profits[profits.length - 1][3];

    var freeProfit = 0.03; // 0.04
    var yearRange = yearDays * 86400000;
    var totalReturns = profits[profits.length - 1][1] / totalAssets;
    var annualizedReturns = (totalReturns * yearRange) / (te - ts);

    // MaxDrawDown
    var maxDrawdown = 0;
    var maxAssets = totalAssets;
    var maxAssetsTime = 0;
    var maxDrawdownTime = 0;
    var maxDrawdownStartTime = 0;
    var winningRate = 0;
    var winningResult = 0;
    //var nowDrawdown = 0;

    for (var i = 0; i < profits.length; i++) {
        if (i == 0) {
            if (profits[i][1] > 0) {
                winningResult++;
            }
        } else {
            if (profits[i][1] > profits[i - 1][1]) {
                winningResult++;
            }
        }
        if (profits[i][1] + totalAssets > maxAssets) {
            maxAssets = profits[i][1] + totalAssets;
            maxAssetsTime = profits[i][3];
        }
        if (maxAssets > 0) {
            var drawDown = 1 - (profits[i][1] + totalAssets) / maxAssets;
            if (drawDown > maxDrawdown) {
                maxDrawdown = drawDown;
                maxDrawdownTime = profits[i][3];
                maxDrawdownStartTime = maxAssetsTime;
            }
        }
    }
    if (profits.length > 0) {
        winningRate = winningResult / profits.length;
    }
    //Log("Maximum assets",maxAssets,"Maximum asset time",_D(maxAssetsTime),"Current Assets",profits[profits.length - 1][1],"Current asset time",_D(profits[profits.length - 1][1]))
    var nowDrawdown = 1 - (profits[profits.length - 1][1] + totalAssets) / maxAssets;
    if (nowDrawdown < 0) {
        nowDrawdown = 0;
    }
    // trim profits
    var i = 0;
    var datas = [];
    var sum = 0;
    var preProfit = 0;
    var perRatio = 0;
    var rangeEnd = te;
    if ((te - ts) % period > 0) {
        rangeEnd = (parseInt(te / period) + 1) * period;
    }
    for (var n = ts; n < rangeEnd; n += period) {
        var dayProfit = 0.0;
        var cut = n + period;
        while (i < profits.length && profits[i][3] < cut) {
            dayProfit += profits[i][1] - preProfit;
            preProfit = profits[i][1];
            i++;
        }
        perRatio = ((dayProfit / totalAssets) * yearRange) / period;
        sum += perRatio;
        datas.push(perRatio);
    }

    var sharpeRatio = 0;
    var volatility = 0;
    if (datas.length > 0) {
        var avg = sum / datas.length;
        var std = 0;
        for (i = 0; i < datas.length; i++) {
            std += Math.pow(datas[i] - avg, 2);
        }
        volatility = Math.sqrt(std / datas.length);
        if (volatility !== 0) {
            sharpeRatio = (annualizedReturns - freeProfit) / volatility;
        }
    }
    return {
        totalAssets: totalAssets,
        yearDays: yearDays,
        totalReturns: totalReturns,
        annualizedReturns: annualizedReturns,
        sharpeRatio: sharpeRatio,
        volatility: volatility,
        nowDrawdown: nowDrawdown,
        maxDrawdown: maxDrawdown,
        maxDrawdownTime: maxDrawdownTime,
        maxAssetsTime: maxAssetsTime,
        maxDrawdownStartTime: maxDrawdownStartTime,
        winningRate: winningRate,
        nowDrawdownFormat: $.TimeBetween(maxAssetsTime, new Date()),
        maxDrawdownFormat: $.TimeBetween(maxDrawdownStartTime, maxDrawdownTime),
    };
};
//Which Week to Take
$.GetWeek = function (date) {
    let nowDate = new Date(date);
    let firstDay = new Date(date);
    firstDay.setMonth(0); //Settings1Moon
    firstDay.setDate(1); //Settings1Number
    let diffDays = Math.ceil((nowDate - firstDay) / (24 * 60 * 60 * 1000));
    let week = Math.ceil(diffDays / 7);
    week = week === 0 ? 1 : week;
    let month = nowDate.getMonth() + 1;
    if (month.toString().length == 1) {
        month = "0" + month;
    }
    let ret = {
        year: nowDate.getFullYear(),
        month: month,
        day: nowDate.getDate(),
        week: week,
    };
    return ret;
};
function main() {}

```

> Detail

https://www.fmz.com/strategy/277946

> Last Modified

2022-03-24 15:51:13
