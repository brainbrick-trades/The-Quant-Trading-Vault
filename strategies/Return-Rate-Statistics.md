
> Name

Return-Rate-Statistics

> Author

春哥

> Strategy Description

Statistical Yield

BotVSThe profit statistics can only record a single curve and cannot perform technical analysis. This template can automatically calculate profits, profit rates, monthly returns, annualized returns, and maximum drawdowns for the most recent 1 day, the previous 1 day, the most recent 7 days, the previous 7 days, the most recent 30 days, the previous 30 days, and all time. (Monthly and annualized returns calculated over short periods do not use a compound interest formula.).)

Usage: Import this template to replace the original strategyLogProfitFunction is$.LogProfit.  And LogStatus Place to add $.ProfitSummary(Initial capital) Return String of

For Example:
function main() {
    while(true) {
        var t = exchange.GetTicker();
        $.LogProfit(t.Last);
        LogStatus($.ProfitSummary(10000));
        Sleep(3600000);
    }
}

Display effect:

1day: Receive-78.44element(-0.537%),Monthly-16.781%,Annualized-204.169%,Retracement1.106%
upper1day: Receive176.08element(1.221%),Monthly38.226%,Annualized465.087%,Retracement1.236%
7day: Receive771.74element(5.599%),Monthly24.141%,Annualized293.719%,Retracement1.517%
upper7day: Receive223.15element(1.64%),Monthly7.071%,Annualized86.039%,Retracement0.9%
30day: Receive1570.31element(12.094%),Monthly12.111%,Annualized147.352%,Retracement3.251%
upper30day: Receive200.12element(1.565%),Monthly1.567%,Annualized19.076%,Retracement1.521%
Total: Receive4554.11element(45.541%),Maximum drawdown3.251%,Statistical time74Sky/Heaven23Hour

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|SYS_LOGPROFIT|true|Whether to also record to the system's built-inLogProfit|


> Source (javascript)

``` javascript
$.LogProfit = function(profit) {
    var args = Array.prototype.slice.call(arguments);
    if (SYS_LOGPROFIT) {
        LogProfit.apply(this, args);
    } else {
        args.unshift('Revenue');
        Log.apply(this,args);
    }

    var _history = $.GetAllProfit();
    _history.push([ Math.floor(new Date().getTime()/1000), profit]);
    _G('profit_history', JSON.stringify(_history));
};

$.GetAllProfit = function() {
	var old = _G('profit_history') || '[]';
    try {
    	var _history = JSON.parse(old);
    	return _history;
    } catch(e) {
    	_G('profit_history', null);
    	return [];
    }
};

function filterProfit(from, to) {
	var arr = $.GetAllProfit();
	if (!arr || arr.length === 0) return;
	var re, maxdrawback=0, lastProfit=0, maxProfit=false, maxdrawbackProfit=0;
	var earlest, latest;
	for(var i=0;i<arr.length;i++) {
		if (!arr[i]) continue;
		if (arr[i][0] > from && arr[i][0] <= to) {
			var profit = arr[i][1];
			if (!earlest) earlest = arr[i];
			latest = arr[i];
			if (!lastProfit) lastProfit = profit;
			if (maxProfit === false || maxProfit < profit) maxProfit = profit;
			var drawback = maxProfit - profit;
			if (drawback > maxdrawback) {
				maxdrawback = drawback;
				maxdrawbackProfit = maxProfit;
			}
		}
	}
	if (!earlest || !latest) return;
	return [earlest, latest, maxdrawback, maxdrawbackProfit];
}

function daysProfit(offset, days) {
	var from = getDaySecond( -offset+days);
	var to = getDaySecond(-offset);
	var arr = filterProfit( from, to );
	if (!arr || !arr[0] || !arr[1]) return;
	var profitTime = arr[1][0] - arr[0][0];
	if (!profitTime) return;
	var periodTime = to - from;
	var profit = arr[1][1] - arr[0][1];
	var realPercent = profitTime*100 / periodTime;
	var expectedProfit = profit * 100 / realPercent;
	return {
		profit:profit, 
		expectedProfit:expectedProfit,
		profitTime:profitTime,
		periodTime:periodTime,
		open: arr[0][1],
		close: arr[1][1],
		drawback: arr[2],
		drawbackProfit: arr[3]
	};
}

function getDaySecond(days) {
	var d = new Date();
	var now = d.getTime();
	now -= days*86400000;
	d.setTime(now);
	return Math.floor(d.getTime() / 1000);
} 

$.DaysProfit = function(days) {
	return filterProfit(days)[2];
};

$.ProfitSummary = function(initialBalance) {
	if (!initialBalance) return 'No initial funds provided';

	var day = daysProfit(0, 1);
	var lastDay = daysProfit(-1, 1);
	var week = daysProfit(0,7);
	var lastWeek = daysProfit(-7,7);
	var month = daysProfit(0,30);
	var lastMonth = daysProfit(-30,30);
	var all = daysProfit(0, 10000);
	if (!all) return '';
	var _days = Math.floor(all.profitTime / 86400);

	var text = [];
	var t = profitSummary(day, initialBalance);
	if (t) text.push('1day: '+t);
	t = profitSummary(lastDay, initialBalance);
	if (t) text.push('upper1day: '+t);
	t = profitSummary(week, initialBalance);
	if (t && _days >= 7) text.push('7day: '+t);
	t = profitSummary(lastWeek, initialBalance);
	if (t) text.push('upper7day: '+t);
	t = profitSummary(month, initialBalance);
	if (t && _days>=30) text.push('30day: '+t);
	t = profitSummary(lastMonth, initialBalance);
	if (t) text.push('upper30day: '+t);
	
	if (all) {
		var _days = Math.floor(all.profitTime / 86400);
		all.profitTime %= 86400;
		var _hours = Math.floor(all.profitTime / 3600);
		var drawback = _N( all.drawback*100/(all.drawbackProfit+initialBalance), 3 )+'%';
		text.push('Total: Receive'+_N(all.close,2)+'element('+_N(all.close*100/initialBalance,3)+'%),Maximum drawdown'+drawback+',Statistical time'+_days+'Sky/Heaven'+_hours+'Hour');
	}
	return text.join('\n');
};

function profitSummary(p, base) {
	if (!p) return '';
	var text = [];
	text.push('Receive'+_N(p.profit,2)+'element('+_N(p.profit*100/(base+p.open), 3)+'%)');
	var month = expectProfit(p, 30, base);
	if (month) {
		text.push('Monthly'+month.percent+'%');
	}
	var year = expectProfit(p, 365, base);
	if (year) {
		text.push('Annualized'+year.percent+'%');
	}
	text.push('Retracement'+ _N( p.drawback*100/(p.drawbackProfit+base), 3 )+'%' );
	return text.join(',');
}


function expectProfit(p, days, base) {
	var expectSeconds = days*86400;
	if (expectSeconds < p.profitTime) return;
	return {
		profit: _N(p.profit * expectSeconds / p.profitTime, 2),
		percent: _N(p.profit * expectSeconds *100 / (p.profitTime * (base+p.open)),3)
	};
}

function main() {
    while(true) {
        var t = exchange.GetTicker();
        $.LogProfit(t.Last);
        LogStatus($.ProfitSummary(10000));
        Sleep(3600000);
    }
}
```

> Detail

https://www.fmz.com/strategy/19329

> Last Modified

2016-08-11 11:41:36
