
> Name

bitmex-api-IDBitmex-position-change-pushwebsocket

> Author

小草

> Strategy Description

Use the websocket protocol and the platform's latest HMAC method to obtain signatures, and push changes in positions to WeChat



> Source (javascript)

``` javascript
function main() {
    var APIKEY = "your Access Key(Bitmex API ID)"
    var expires = parseInt(Date.now() / 1000) + 10
    var signature = exchange.HMAC("sha256", "hex", "GET/realtime" + expires, "{{secretkey}}")//secretkeyAutomatically replaced during execution, no need to fill in
    var client = Dial("wss://www.bitmex.com/realtime", 60)
    var auth = JSON.stringify({args: [APIKEY, expires, signature], op: "authKeyExpires"})
    var pos = 0
    client.write(auth)
    client.write('{"op": "subscribe", "args": "position"}')
    while (true) {
        bitmexData = client.read()
        if(bitmexData.table == 'position' && pos != parseInt(bitmexData.data[0].currentQty)){
            Log('position change', pos, parseInt(bitmexData.data[0].currentQty), '@')
            pos = parseInt(bitmexData.data[0].currentQty)
        }
    }
}
```

> Detail

https://www.fmz.com/strategy/128624

> Last Modified

2018-12-24 09:26:09
