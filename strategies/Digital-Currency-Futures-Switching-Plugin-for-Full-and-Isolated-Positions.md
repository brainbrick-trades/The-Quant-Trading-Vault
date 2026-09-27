
> Name

Digital-Currency-Futures-Switching-Plugin-for-Full-and-Isolated-Positions

> Author

发明者量化-小小梦



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|type|0|Cross/Isolated margin mode: Isolated|Cross|


> Source (javascript)

``` javascript
function main() {
    var posType = [false, true][type]
    var name = exchange.GetName()
    if (name == "Futures_Binance") {
        exchange.IO("cross", posType)
    } else if (name == "Futures_HuobiDM") {
        exchange.IO("cross", posType)    
    } else if (name == "Futures_Bibox") {
        exchange.IO("cross", posType)        
    } else if (name == "Futures_Bitget") {
        exchange.IO("cross", posType)        
    } else if (name == "Futures_AOFEX") {
        exchange.IO("cross", posType)      
    } else if (name == "Futures_Pionex") {
        exchange.IO("cross", posType)      
    } else {
        throw "not support!"
    }
    return name + "Switch cross :" + posType
}
```

> Detail

https://www.fmz.com/strategy/351758

> Last Modified

2023-09-06 10:36:47
