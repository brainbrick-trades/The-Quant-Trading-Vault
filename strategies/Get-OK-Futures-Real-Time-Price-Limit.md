
> Name

Get-OK-Futures-Real-Time-Price-Limit

> Author

数·狂

> Strategy Description

Get OKEx futures real-time limit price, only valid for live trading.
Code is for learning purposes only. The author does not guarantee the correctness of the program. Any consequences of trading based on this are your own responsibility.



> Source (javascript)

``` javascript
$.GetLimit = function(currStr, contract) {
    var url = "https://www.okcoin.com/api/v1/future_price_limit.do?symbol=" + currStr + "_usd&contract_type=" + contract;
    var httpResp = HttpQuery(url);
    if (httpResp.indexOf("false") != -1) return null;
    var parsedResp;
    try {
        parsedResp = JSON.parse(httpResp);
    } catch (e) {
        return null;
    }
    return parsedResp;
};

function main() {
    var limit = $.GetLimit('btc', 'quarter'); // Get Bitcoin quarterly contract limit price
    Log(limit.high, limit.low); // Highest buy, lowest sell limit price
    limit = $.GetLimit('ltc', 'this_week'); // Get Litecoin weekly contract limit price
    Log(limit.high, limit.low); // Highest buy, lowest sell limit price
    limit = $.GetLimit('btc', 'next_week'); // Get Bitcoin next week contract limit price
    Log(limit.high, limit.low); // Highest buy, lowest sell limit price
    
}
```

> Detail

https://www.fmz.com/strategy/17028

> Last Modified

2016-06-19 11:15:05
