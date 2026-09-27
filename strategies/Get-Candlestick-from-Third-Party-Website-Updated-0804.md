
> Name

Get-Candlestick-from-Third-Party-Website-Updated-0804

> Author

数·狂

> Strategy Description

For platforms that do not support obtaining candlestick data (BitVC futures, BTCC's BTC spot, Chinese Bitcoin's ETH, ETC), if enough candlesticks must be obtained at the beginning of the strategy, you can use this template to directly obtain the platform's historical candlestick data from a third-party website.
NOTE:
KLine data is updated every 3 seconds, so it cannot be called frequently.
Only applicable for live trading.
The author does not guarantee the accuracy of third-party data or the correctness of the procedures; this is for study reference only.

0427Update: Handled possible exceptions thrown when parsing JSON data; when an exception occurs, the return value is uniformlynull.



> Source (javascript)

``` javascript

$.AltRecords = function(exchange, timeframe, size, includeLastBar) {
    var symbol;
    var info;
    var record = [];
    if (!size) size="";
    // Currently, only the following three exchanges are supported; the interfaces of other exchanges can be referencedhttps://www.btc123.com/api
    if (exchange.GetName().indexOf('Futures_BitVC') != -1) { 
        symbol = "bitvcbtccnyfuture";
    }
    else if (exchange.GetName().indexOf('BTCC') != -1 && exchange.GetCurrency().indexOf('BTC') != -1) {
        symbol = "btcchinabtccny";
    }
    else if (exchange.GetName().indexOf('CHBTC') != -1 && exchange.GetCurrency().indexOf('ETH') != -1) {
        symbol = "chbtcethcny";
    }
    else if (exchange.GetName().indexOf('CHBTC') != -1 && exchange.GetCurrency().indexOf('ETC') != -1) {
        symbol = "chbtcetccny";
    }
    
    if (symbol) {
        try {
            info = JSON.parse(HttpQuery('https://www.btc123.com/market/kline?symbol='+symbol+'&type='+timeframe+'&size='+(includeLastBar ? size : size+1)));
            if (info && info.isSuc) {
                info = JSON.parse(info.datas.data);
            }
            else {
                Log("ObtainKAn error occurred while threading:", info && info.des ? info.des : "Network error");
                return null;
            }
        } catch (e) {
            Log("ObtainKAn error occurred while threading:", info && info.des ? info.des : "Network error");
            return null;
        }
        for (var i = 0; i < (includeLastBar ? info.length : info.length-1); i++) {
            record.push({"Time": info[i][0], "Open": info[i][1], "High": info[i][2], "Low": info[i][3], "Close": info[i][4], "Volume": info[i][5]});
        }
        return record;
    }
    return exchange.GetRecords(); // Unsupported exchanges are processed in the default way (ignoring all parameters, such as time period, length, etc.).
};

function main() {
    Log(exchange.GetName());
    var rec = $.AltRecords(exchange, "5min", 100); // Obtain5MinuteKLine, 100items, Excluding the last itemBar
    if (rec) Log(rec.length, rec[rec.length-1]);
    rec = $.AltRecords(exchange, "4hour", 100, 1); // Obtain4HourKLine, 100items, including the last oneBar
    if (rec) Log(rec.length, rec[rec.length-1]);
}
```

> Detail

https://www.fmz.com/strategy/12977

> Last Modified

2016-08-04 22:35:27
