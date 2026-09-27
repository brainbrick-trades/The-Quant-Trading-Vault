
> Name

BTC-LTC-Address-Monitoring-SMS-Notification

> Author

Zero

> Strategy Description

There are new transactions, please be reminded immediately

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Type|0|Type: BTC|LTC|
|Addr|1LuckyY9fRzcJre7aou7ZhWVXktxjjBb9S|Address|
|Interval|3|Polling Interval|
|EnableSMS|false|Enable SMS notifications|
|SMSUser|***|SMSBao username|
|SMSPass|***|SMS MD5 password|
|PhoneNum|1111|Receive SMS mobile number|


> Source (javascript)

``` javascript
var LastMsg = "";
function SMSSend(msg) {
    if (msg == LastMsg) {
        return true;
    }
    Log('SMS:', msg);
    LastMsg = msg;
    var ret = false;
    var phones = PhoneNum.split(',');
    for (var i = 0; i < phones.length; i++) {
        ret = HttpQuery("http://www.smsbao.com/sms?u=" + encodeURIComponent(SMSUser) + "&p=" + SMSPass.toUpperCase() + "&m=" + phones[i] + "&c=" + encodeURIComponent(msg)) == "0";
        if (ret) {
            Log("SMS Notification", phones[i], "Success");
        } else {
            Log("SMS Notification", phones[i], "Failed");
        }
    }
    return ret;
}

function main() {
    var url = "http://open.qukuai.com/address/" + Addr + "?key=2ejf4jgfNoya8Y3GnQf68e4J23HherpUh1&limit=1";
    if (Type == 1) {
        url += "&ltc=true";
    }
    var lt = "";
    Log("Monitor: ", Addr, Type == 0 ? 'BTC' : 'LTC');
    if (EnableSMS) {
        if (!SMSSend("Strategy started successfully")) {
            return false;
        }
    }
    while (true) {
        try {
            var res = HttpQuery(url);
            if (res) {
                var obj = JSON.parse(res);
                if (typeof(obj.t0) !='undefined' && obj.t0.length > 0) {
                    if (obj.t0.toString() != lt) {
                        if (lt != "") {
                            LogProfit(obj.balance, obj.received);
                            if (EnableSMS) SMSSend('New Transaction, Current Balance: ' + obj.balance/100000000 + 'Total Received: ' + obj.received/100000000);
                        }
                        lt = obj.t0.toString();
                    }
                }
            }
        } catch(e) {
            Log(e);
        }
        Sleep(Interval*1000);
    }
}
```

> Detail

https://www.fmz.com/strategy/1295

> Last Modified

2014-11-07 19:41:42
