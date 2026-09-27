
> Name

OK-Confirms-That-the-Trading-Pair-Cannot-Be-Withdrawn

> Author

daniaoren

> Strategy Description

For personal use, simply list all coins currently non-withdrawable on OKEX; sometimes quite useful, requires manual retrieval



> Source (javascript)

``` javascript
function main() {
    var results = exchange.IO("api", "GET", "/api/account/v3/currencies", "" , "");
    var blacklist = []
    i = 0;
    var statusMsg = '';
	while (true)
    {
        if (results[i]["can_withdraw"] == "0"){
            Log(results[i]["currency"],"|",results[i]["name"], results[i]["can_deposit"]);
            statusMsg += results[i]["currency"] + " | " + results[i]["name"] + ' ' + results[i]["can_deposit"] + '\n';
            blacklist.push(results[i]);
        }
        i++;
        if (i >= results.length){
        	break;
        }
    }
    Log(blacklist.length);
    statusMsg = blacklist.length + '\n' + statusMsg;
    LogStatus(statusMsg);
    return blacklist;

}
```

> Detail

https://www.fmz.com/strategy/253278

> Last Modified

2021-02-10 15:29:08
