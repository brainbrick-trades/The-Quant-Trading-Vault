
> Name

Binance-Multi-Trading-Pair-Price-Range-Reminder

> Author

轻轻的云

> Strategy Description

Because Aicoin's iOS version isn't a membership, it can't be used anymore, and there are no price reminders, so I'm thinking of making one myself.

But I really don't understand the code, so I copied and pasted it according to Mengda's code., https://www.fmz.com/digest-topic/8512
My English isn't good, so I use pinyin for both the upper and lower limits. The rest of the English is just copying Dream University. [Grinning]
Thanks, Meng Da [fist salute] [handshake]]!!!

If anyone knows any apps that can alert prices like Aicoin, please let me know, thank you.

This default is for contract trading and supports USDT BUSD. Set the upper and lower limits. If the latest price is higher than the upper limit or lower than the lower limit, a message notification will be sent.
If spot trading is needed, simply uncheck [Contract Trading] in the parameters, then select the exchange for spot Binance.
FMZ needs to be bound for push. I bound it to QQ mailbox, and then set a special reminder tone for QQ mailbox and bound WeChat at the same time. There will be two reminders.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|B_sleeptime|30|Polling time (seconds))|
|symbols|ETH_BUSD,ETC_USDT,LTC_USDT|trading pair|
|B_shangxian|3000,100,200|Price limit|
|B_xiaxian|2000,50,100|Price lower limit|
|B_heyue|true|Contract Trading|


> Source (javascript)

``` javascript
var arrSymbols = symbols.split(",")
var arrshangxian = B_shangxian.split(",")
var arrxiaxian = B_xiaxian.split(",")
var shang = parseFloat(arrshangxian[i])
var xia = parseFloat(arrxiaxian[i])

function main() {
    if (B_chongzhi) {
        LogReset()
        LogVacuum()
        Log("Reset all data", "#FF0000")
    }
    while (true) {
        for (var i = 0; i < arrSymbols.length; i++) {
            var symbol = arrSymbols[i]
            if (B_heyue == true) {
                exchange.SetContractType("swap")
            }
            exchange.SetCurrency(symbol)
            var ticker = _C(exchange.GetTicker).Last
            Log("trading pair:", symbol, "Latest price:", ticker)
            if (ticker > shang || ticker < xia) {
                Log(symbol, "Price jumps out of the range, current latest price:", ticker, "#FF0000", "@")
            }
            Sleep(B_sleeptime * 1000)
        }
        Sleep(5 * 1000)

    }
}
```

> Detail

https://www.fmz.com/strategy/342165

> Last Modified

2022-04-21 22:45:14
