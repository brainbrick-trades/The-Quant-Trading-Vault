
> Name

SMS-Notification-Class-Library

> Author

Zero

> Strategy Description

> Support gateway

*  SMS Bao http://www.smsbao.com/
* SUBMAIL http://submail.cn/

> example

```
$.SMSNotify("abc SMS test");
```

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|PhoneNum|138XXXXXXXX|Mobile number|
|SMSGate|0|SMS gateway: SMSBao|SUBMAIL|
|SMSBaoUserName|username|Username|
|SMSBaoPWD|$$$__enc__$$$password|Password|
|AppId|11111|APPID|
|AppKey|$$$__enc__$$$11111|APPKEY|
|VarName|content|Variable name|
|Project|5x1X03|Project Tag|


> Source (javascript)

``` javascript
$.SMSNotify = function(content) {
    if (IsVirtual()) {
        throw "This template only supports live trading";
    }
    if (SMSGate === 0) {
        var retCode = HttpQuery("http://api.smsbao.com/sms?u="+SMSBaoUserName+"&p="+MD5(SMSBaoPWD)+"&m="+PhoneNum+"&c="+encodeURIComponent(content));
        var retDict = {
            '30': 'Incorrect Password',
            '40': 'Account does not exist',
            '41': 'Insufficient Balance',
            '42': 'Account Expired',
            '43': 'IPAddress Restriction',
            '50': 'content contains sensitive words',
            '51': 'incorrect mobile phone number'
        };
        if (typeof(retCode) === 'string' && typeof(retDict[retCode]) === 'string') {
            Log('SMS notification response:', retDict[retCode]);
        } else if (retCode === '0') {
            Log('SMS notification successful:', content);
        } else {
            Log('SMS notification failed:', content, '#ff0000');
        }
    } else if (SMSGate == 1) {
        var vars = {};
        vars[VarName] = content;
        var ret = HttpQuery('https://api.submail.cn/message/xsend.json', 'appid='+AppId+'&to='+PhoneNum+'&project='+Project+'&signature='+AppKey+'&vars='+encodeURIComponent(JSON.stringify(vars)));
        if (ret && ret.indexOf('"status"') != -1) {
            var obj = JSON.parse(ret);
            Log("SMS Notification:", obj.status, typeof(obj.msg) != 'undefined' ? obj.msg : '');
        } else {
            Log("SMS notification failed");
        }
    }
}

function main() {
    $.SMSNotify("abc SMS test");
}
```

> Detail

https://www.fmz.com/strategy/26921

> Last Modified

2016-12-05 17:31:11
