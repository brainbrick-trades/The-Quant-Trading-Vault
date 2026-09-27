
> Name

API-Availability-Statistics-of-Major-Platforms

> Author

Zero

> Strategy Description

supports multiple exchanges and multithreading. If you want to learn multithreading or charting, you can try this strategy

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Interval|10|Detection frequency (seconds)|
|TickCount|200|Sample quantity|




|Button|Default|Description|
|----|----|----|
|Clear log|__button__|Clear log|


> Source (javascript)

``` javascript

function _D(t) {
    if (typeof(t) == 'undefined') {
        t = new Date();
    }
    var year = t.getFullYear();
    var month = t.getMonth() + 1;
    var day = t.getDate();
    var hour = t.getHours();
    var minute = t.getMinutes();
    var second = t.getSeconds();

    if (month < 10) {
        month = '0' + month;
    }
    if (day < 10) {
        day = '0' + day;
    }
    if (hour < 10) {
        hour = '0' + hour;
    }
    if (minute < 10) {
        minute = '0' + minute;
    }
    if (second < 10) {
        second = '0' + second;
    }

    return year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second;
}

function ExchangeManager(e, idx) {
    var arr = [];
    this.Last = 0;
    this.e = e;
    this.idx = idx;
    this.Go = e.Go;
    this.GetName = e.GetName;
    this.GetLabel = e.GetLabel;
    this.health = 100;
    this.tickerChanged = false;
    this.init = function() {
        if (e.GetName() == "Futures_BitVC") {
            e.SetContractType("week");
        }
        var ticker = e.GetTicker();
        if (!ticker) {
            this.Last = 0;
        } else {
            this.Last = _N(ticker.Last, 3);
        }
        this.ticker = ticker;
        this.tickerChanged = true;
    };
    
    this.updateHealth = function(ticker) {
        if (ticker) {
            this.tickerChanged = _N(ticker.Last, 3) != this.Last;
            this.Last = _N(ticker.Last, 3);
            this.ticker = ticker;
        }
        arr.push(ticker);
        if (arr.length > TickCount) {
            arr.shift();
        }
    };
    this.getHealth = function() {
        var ratio = 0;
        var n = Math.min(TickCount, arr.length);
        for (var i = n-1; i >=0; i--) {
            if (arr[i]) {
                ratio++;
            }
        }
        return parseFloat(((ratio * 100) / n).toFixed(3));
    };
}

function multiCall(tasks, callback, isRetry) {
    var ret = [];
    var n = 0;
    if (typeof(isRetry) == 'undefined') {
        isRetry = true;
    }
    var ts = new Date();
    while (true) {
        var now = new Date();
        if ((now.getTime() - ts.getTime()) > 1000) {
            ts = now;
            var waitNames = [];
            for (var i = 0; i < tasks.length; i++) {
                if (typeof(ret[i]) == 'undefined' || typeof(ret[i].wait) != "undefined") {
                    waitNames.push(tasks[i][0].GetName() + "("+tasks[i].slice(1).join(",")+")");
                }
            }
            if (waitNames.length > 0) {
                // add api status as extra
                LogStatus("Wait: " + waitNames.join(", ") + " Current Time:" + _D() + " Try again" + (isRetry ? "Turn On" : "Close"));
            }
        }
        for (var i = 0; i < tasks.length; i++) {
            if (typeof(ret[i]) != 'undefined' && typeof(ret[i].wait) != "undefined") {
                var r = ret[i].wait(0);
                if (r) {
                    ret[i] = r;
                    n++;
                    if (typeof(callback) != 'undefined') {
                        callback(tasks[i], r);
                    }
                } else if (typeof(r) != 'undefined') {
                    if (isRetry) {
                        // null retry
                        delete ret[i];
                    } else {
                        n++;
                        // ignore
                        ret[i] = true;
                        if (typeof(callback) != 'undefined') {
                            callback(tasks[i], r);
                        }
                    }
                }
            }
            if (typeof(ret[i]) == 'undefined') {
                ret[i] = tasks[i][0].Go.apply(this, tasks[i].slice(1));
            }
        }
        if (n == tasks.length) {
            break;
        }
        Sleep(50);
    }
    return ret;
}

function EnsureCall(method) {
    var r;
    while (!(r = method.apply(this, Array.prototype.slice.call(arguments).slice(1)))) {
        Sleep(300);
    }
    return r;
}


function main() {
    var keys = [];
    var table = {
        type: 'table',
        title: 'Market information',
        cols: ['Exchange, bid price, ask price, last transaction price, high, low, trading volume.'],
        rows: []
    };
    var es = [];
    for (var i = 0; i < exchanges.length; i++) {
        var m = new ExchangeManager(exchanges[i], i);
        m.init();
        es.push(m);
        keys.push(exchanges[i].GetLabel());
    }

    var chart = Chart({
        __isStock: false,
        chart: { type: 'column' },
        title: { text: 'Exchange API availability' },
        subtitle: { text: 'Sampled recently ' + TickCount + ' times, Every ' + Interval +' Updates once every second' },
        xAxis: { categories: keys },
        yAxis: [{
            min: 0,
            max: 100,
            title: {text: 'Availability'}
            },{
                min: 1000,
                title: {text: 'Last transaction price'},
                style: {color: '#4572A7'},
                opposite: true
            }
        ],
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [
            { name: 'Availability', data: [], tooltip: {valueSuffix: ' %'}, dataLabels: {color: '#000000', rotation: -35, enabled: true, x:2, y:50}},
            { name: 'Transaction price', color: '#bbbbbb', yAxis: 1, data: [], tooltip: {valueSuffix: ' yuan'}, dataLabels: {color: '#000000', rotation: -35, enabled: true, x:2, y:120}}
            ]
    });
    chart.reset();

    // Initialize chart
    for (var i = 0; i < es.length; i++) {
        chart.add([0, 100]);
        chart.add([1, es[i].Last]);
    }
    Log("Initialization successful.");
    Sleep(5000);
    while (true) {
        var tasks = [];
        for (var i = 0; i < es.length; i++) {
            tasks.push([es[i], "GetTicker"]);
        }

        multiCall(tasks, function(r, result) {
            r[0].updateHealth(result);
        }, false);

        for (var i = 0; i < es.length; i++) {
            var health = es[i].getHealth();
            if (health != es[i].health) {
                chart.add([0, health, es[i].idx]);
                es[i].health = health;
            }
            if (es[i].tickerChanged) {
                chart.add([1, es[i].Last, es[i].idx]);
            }
            var ticker = es[i].ticker;
            if (ticker) {
                table.rows[i] = [es[i].GetLabel(), ticker.Buy, ticker.Sell, ticker.Last + '#ff0000', ticker.High, ticker.Low, ticker.Volume];
            }
        }
        LogStatus('Last updated on: ' + _D() +'\n`' + JSON.stringify(table) + '`');
        var cmd = GetCommand();
        if (cmd && cmd.indexOf('Clear log') === 0) {
            LogReset();
            Log("Log has been reset");
        }
        Sleep(Interval*1000);
    }
}

```

> Detail

https://www.fmz.com/strategy/4404

> Last Modified

2016-09-26 09:01:12
