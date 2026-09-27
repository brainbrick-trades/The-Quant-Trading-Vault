
> Name

Time-Format-Tool

> Author

huangsibo





> Source (javascript)

``` javascript
/*
 * @Author: sibohuang
 * @Date: 2019-08-10 09:36:03
 * @LastEditors: sibohuang
 * @LastEditTime: 2019-08-10 09:45:11
 * @Description: 
 * @Email: 3570411064@qq.com
 * @Company: igola
 */

/**
 * Format the date into a string in the specified format
 * @param date The date to be formatted. If not passed, it defaults to the current time, or it can be a timestamp.
 * @param fmt Target string format, supported characters include: y, M, d, q, w, H, h, m, S, by default.:yyyy-MM-dd HH:mm:ss
 * @returns Returns the formatted date string
 */
$.formatDate = function (date, fmt) {
    date = !date ? new Date() : date;
    date = typeof date === 'number' ? new Date(date) : date;
    fmt = fmt || 'yyyy-MM-dd HH:mm:ss';
    var obj =
        {
            'y': date.getFullYear(), // Year, Note Must UsegetFullYear
            'M': date.getMonth() + 1, // Month, note that it starts from0-11
            'd': date.getDate(), // Date
            'q': Math.floor((date.getMonth() + 3) / 3), // Quarter
            'w': date.getDay(), // Week, note it is0-6
            'H': date.getHours(), // 24Hour format
            'h': date.getHours() % 12 == 0 ? 12 : date.getHours() % 12, // 12Hour format
            'm': date.getMinutes(), // Minute
            's': date.getSeconds(), // second
            'S': date.getMilliseconds() // Millisecond
        };
    var week = ['Sky/Heaven', 'One', 'Two', 'Three', 'Four', 'Five', 'Six'];
    for (var i in obj) {
        fmt = fmt.replace(new RegExp(i + '+', 'g'), function (m) {
            var val = obj[i] + '';
            if (i == 'w') return (m.length > 2 ? 'Week' : 'week') + week[val];
            for (var j = 0, len = val.length; j < m.length - len; j++) val = '0' + val;
            return m.length == 1 ? val : val.substring(val.length - m.length);
        });
    }
    return fmt;
}
/**
 * Parse string into date
 * @param str Input date string, such as'2014-09-13'
 * @param fmt String format, default 'yyyy-MM-dd', supports the following: y, M, d, H, m, s, S, w andq
 * @returns Parsed Date type date
 */

$.parseDate = function(str, fmt) {
    fmt = fmt || 'yyyy-MM-dd';
    var obj = {y: 0, M: 1, d: 0, H: 0, h: 0, m: 0, s: 0, S: 0};
    fmt.replace(/([^yMdHmsS]*?)(([yMdHmsS])\3*)([^yMdHmsS]*?)/g, function (m, $1, $2, $3, $4, idx, old) {
        str = str.replace(new RegExp($1 + '(\\d{' + $2.length + '})' + $4), function (_m, _$1) {
            obj[$3] = parseInt(_$1);
            return '';
        });
        return '';
    });
    obj.M--; // Months start from 0, so subtract 11
    var date = new Date(obj.y, obj.M, obj.d, obj.H, obj.m, obj.s);
    if (obj.S !== 0) date.setMilliseconds(obj.S); // If milliseconds are set
    return date;
}
/**
 * Format a date into a friendly format, for example, return "Just now" within 1 minute.",
 * Return hour and minute for the day, month and day for the year, otherwise return year, month, and day
 * @param {Object} date
 */
$.formatDateToFriendly = function(date) {
    date = date || new Date();
    date = typeof date === 'number' ? new Date(date) : date;
    invariant(date instanceof Date, 'date is not date type');
    var now = new Date();
    if ((now.getTime() - date.getTime()) < 60 * 1000) return 'Just Now'; // 1Considered within minutes"Just Now"
    var temp = this.formatDate(date, 'yyyyYearMMoond');
    if (temp == this.formatDate(now, 'yyyyYearMMoond')) return this.formatDate(date, 'HH:mm');
    if (date.getFullYear() == now.getFullYear()) return this.formatDate(date, 'MMoondday');
    return temp;
}

/**
 * Convert a duration into a friendly format, such as:
 * 147->"2Every 27 seconds"
 * 1581->"26Every 21 seconds"
 * 15818->"424 hours 24 minutes"
 * @param {Object} second
 */

$.formatDurationToFriendly = function(second) {
    if (second < 60) return second + 'second';
    else if (second < 60 * 60) return (second - second % 60) / 60 + 'Minute' + second % 60 + 'second';
    else if (second < 60 * 60 * 24) return (second - second % 3600) / 60 / 60 + 'Hour' + Math.round(second % 3600 / 60) + 'Minute';
    return (second / 60 / 60 / 24).toFixed(1) + 'Sky/Heaven';
}
/**
 * Convert time into MM:SS format
 */

$.formatTimeToFriendly = function(second) {
    var m = Math.floor(second / 60);
    m = m < 10 ? ( '0' + m ) : m;
    var s = second % 60;
    s = s < 10 ? ( '0' + s ) : s;
    return m + ':' + s;
}
/**
 * Calculate the number of days between 2 dates, using the method of comparing milliseconds
 * The incoming date is either of Date type or a string date in yyyy-MM-dd format
 * @param date1 Date one
 * @param date2 Date two
 */
$.countDays = function(date1, date2) {
    var fmt = 'yyyy-MM-dd';
    // Convert the date to a string; the purpose of the conversion is to remove"Hours, minutes, seconds"
    if (date1 instanceof Date && date2 instanceof Date) {
        date1 = this.formatDate(date1, fmt);
        date2 = this.formatDate(date2, fmt);
    }
    if (typeof date1 === 'string' && typeof date2 === 'string') {
        date1 = this.parseDate(date1, fmt);
        date2 = this.parseDate(date2, fmt);
        return (date1.getTime() - date2.getTime()) / (1000 * 60 * 60 * 24);
    }
    else {
        console.error('Invalid parameter format!');
        return 0;
    }
}
function main() {
    Log($.formatDate(new Date()))
    // Log($.parseDate(new Date()))
    // Log($.formatDateToFriendly(new Date()))
    // Log($.formatTimeToFriendly(new Date()))
    // Log($.formatDurationToFriendly(new Date()))
    // Log($.countDays(new Date()))
}
```

> Detail

https://www.fmz.com/strategy/161505

> Last Modified

2019-08-10 09:45:12
