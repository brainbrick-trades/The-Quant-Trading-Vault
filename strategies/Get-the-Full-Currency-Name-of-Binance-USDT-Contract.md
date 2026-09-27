
> Name

Get-the-Full-Currency-Name-of-Binance-USDT-Contract

> Author

鑫

> Strategy Description

1,Put into FMZ debugging tool, can run directly
2,Get the full currency name and number of Binance usdt contract



> Source (javascript)

``` javascript
function unique (str) {
	var arr = str.split(',');
	return Array.from(new Set(arr)).join(',')
}

function main() {
    var exchange_info = JSON.parse(HttpQuery('https://fapi.binance.com/fapi/v1/exchangeInfo'));
    var str = '';
    exchange_info.symbols.forEach(function(exitem, index) {
        if (exitem.symbol.indexOf('USDT') == -1) {return}
        if (exitem.symbol.indexOf('BTCST') !== -1) {return}
        if (exitem.symbol.indexOf('BTCDOM') !== -1) {return}
        var content = ',';
        if (index == exchange_info.symbols.length - 1) {
            content = '';
        }
        str += exitem.baseAsset + content;
    });
	Log('Total number of contract currencies:', unique(str).split(',').length)
    Log('Names of all contract currencies:',unique(str))
    // return leverageBracket;

    let leverageBracket = exchange.IO("api", "GET", "/fapi/v1/leverageBracket", "timestamp=" + new Date().getTime())
    let newList = leverageBracket.map((item) => {
        return {
            symbol: item.symbol,
            leverage: item.brackets[0].initialLeverage
        }
    })
    let selectLeverage = 25;
    newList = newList.filter((item) => {
        return item.leverage >= selectLeverage;
    })
    Log('Number of filtered coins:' , newList.length);
    let str2 = ''

    newList.forEach(function(exitem, index) {
        if (exitem.symbol.indexOf('USDT') == -1) {return}
        if (exitem.symbol.indexOf('BTCST') !== -1) {return}
        if (exitem.symbol.indexOf('BTCDOM') !== -1) {return}
        var content = ',';
        if (index == newList.length - 1) {
            content = '';
        }
        str2 += exitem.baseAsset + content;
    });
    Log('Name of filtered coins:', str);
}

```

> Detail

https://www.fmz.com/strategy/327743

> Last Modified

2023-09-26 20:50:01
