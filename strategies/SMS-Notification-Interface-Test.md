
> Name

SMS-Notification-Interface-Test

> Author

Zero

> Strategy Description

To test the SMS notification interface, please register an account on an SMS platform that supports APIs (SMS Treasure is recommended), and then enter the sent URL into the interface.
For example http://www.xxxx.com/sms.php?phone=1111111&c={BODY}
Test whether the SMS can be received

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|SMSAPI|http://|SMS interface|
|Msg|Hello, test successful | sent message|


> Source (javascript)

``` javascript
function main() {
    if (SMSAPI.length > 10 && SMSAPI.indexOf('http') == 0 && SMSAPI.indexOf('{BODY}') != -1) {
        Log('Send: ', Msg);
        HttpQuery(SMSAPI.replace('{BODY}', encodeURIComponent(Msg)));
        Log('Sending completed, Please check if the SMS is received');
    } else {
        Log('Parameter configuration error, Please retest the SMS interface');
    }
}
```

> Detail

https://www.fmz.com/strategy/653

> Last Modified

2014-09-25 17:35:46
