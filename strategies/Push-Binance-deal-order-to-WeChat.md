
> Name

Push-Binance-deal-order-to-WeChat

> Author

小草

> Strategy Description

Push Binance transaction information to WeChat through the websocket protocol, which can be used as an exercise for the wss protocol.
The specific principle is to update the listenKey every 30 minutes and then subscribe to the account.datastream.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|APIKEY||your binance API Key|


> Source (javascript)

``` javascript
function main() {
    var listenKey = JSON.parse(HttpQuery('https://api.binance.com/api/v1/userDataStream','',null,'X-MBX-APIKEY:'+APIKEY)).listenKey;
    HttpQuery('https://api.binance.com/api/v1/userDataStream', {method:'DELETE',data:'listenKey='+listenKey}, null,'X-MBX-APIKEY:'+ APIKEY);
    listenKey = JSON.parse(HttpQuery('https://api.binance.com/api/v1/userDataStream','',null,'X-MBX-APIKEY:'+ APIKEY)).listenKey;
    var datastream = Dial("wss://stream.binance.com:9443/ws/"+listenKey, 100);
    var update_listenKey_time =  Date.now()/1000;
    while (true){
        if (Date.now()/1000 - update_listenKey_time > 1800){
            update_listenKey_time = Date.now()/1000;
            HttpQuery('https://api.binance.com/api/v1/userDataStream', {method:'PUT',data:'listenKey='+listenKey}, null,'X-MBX-APIKEY:'+ APIKEY);
            Log('keep listenKey alive');
        }
        var data = datastream.read();
        if(data){
            data = JSON.parse(data);
            if(data.e == 'executionReport' && data.x == 'TRADE'){
                Log(data.S, data.s,  'amount is ', data.l, 'at price:', data.p, '@');
            }
        }
    }
}
```

> Detail

https://www.fmz.com/strategy/122649

> Last Modified

2019-07-03 16:27:05
