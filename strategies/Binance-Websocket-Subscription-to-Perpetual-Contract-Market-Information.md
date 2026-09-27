
> Name

Binance-Websocket-Subscription-to-Perpetual-Contract-Market-Information

> Author

GCC





> Source (python)

``` python
import json
def main():
    LogStatus("Connecting...")
    # client = Dial("wss://stream.binance.com:9443/stream?streams=btcusdt@aggTrade/ethusdt@aggTrade|reconnect=true")    #Multiple trading pairs
    # client = Dial("wss://stream.binance.com:9443/ws/btcusdt@aggTrade|reconnect=true")    #Single trading pair
    # client = Dial("wss://dstream.binance.com/ws/btcusd_perp@aggTrade|reconnect=true")    #Coin-based,ticker
    client = Dial("wss://fstream.binance.com/ws/btcusdt@aggTrade|reconnect=true")
    if not client:    
        Log("Connection failed, Program exited")
        return
    while True:
        buf = client.read(-2)
        Log('tt',buf)
        if buf:
            obj = json.loads(buf)
            # Log(obj)
            # Log('Trading pair',obj['data']['s'], 'price', obj['data']['p']) #Multiple trading pairs 
            Log(obj['p'])    #Test
        Sleep(5000)
    client.close()
```

> Detail

https://www.fmz.com/strategy/327491

> Last Modified

2021-11-24 14:29:50
