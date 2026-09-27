
> Name

Account-Balance-Change-Email-Alerts-Supports-Adding-Multiple-Exchanges

> Author

Zero

> Strategy Description

Detect changes in currency and money in the account balance and send them to the designated email address. This does not support backtesting
Previously, Fetion's SMS was frozen, and because too many people used it, the account was frozen. It couldn't use the SMS interface anymore, so it switched to email.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|LoopInterval|10|Detection interval (seconds))|
|AlertMode|0|Reminder methods: Change reminder | Condition alarm | Minimum value alarm|
|MaxDiffCNY|false|Minimum change in money|
|MaxDiffCoin|false|Minimum coin fluctuation|
|MinCoin|false|Minimum coin value|
|MinCNY|false|Minimum value of money|
|SMTPServer|smtp.163.com|SMTPServer|
|SMTPUser|test@163.com|Sending email (SMTP username)|
|SMTPPass|***|Email password (SMTP password))|
|SendMode|0|Receiving email: Self | Other|
|DstMail|test@163.com|Recipient's email|


> Source (javascript)

``` javascript

function Notify(msg) {
    var ret = Mail(SMTPServer, SMTPUser, SMTPPass, SendMode == 0 ? SMTPUser : DstMail , msg, "Balance changes " + msg);
    if (ret) {
        Log("Email notification successful");
    } else {
        Log("Email notification failed");
    }
    Log(ret ? "Email sent successfully" : "Email sending failed");
    return ret;
}

function GetAccount(print) {
    var all = {
        Balance : 0,
        Stocks  : 0,
    };
    var currency = exchange.GetCurrency();
    for (var i = 0; i < exchanges.length; i++) {
        if (exchanges[i].GetCurrency() != currency) {
            throw "Different currencies";
        }
        var account;
        while (!(account = exchanges[i].GetAccount())) {
            Sleep(1000);
        }
        all.Stocks += (account.Stocks + account.FrozenStocks);
        all.Balance += (account.Balance + account.FrozenBalance);
        if (typeof(print) != 'undefined' && print) {
            Log(exchanges[i].GetName(), "Money: ", (account.Balance + account.FrozenBalance), "Currency: ", (account.Stocks + account.FrozenStocks));
        }
    }

    return all;
}

function main() {
    // Disable rate auto convert
    exchange.SetRate(1);
    if (Version() < 2.7) {
        throw "Only supports version 2.7 or above";
    }
    var preAccount = GetAccount(true);
    if (!Notify("Strategy started successfully, Total Money: " + preAccount.Balance + ", Currency: " + preAccount.Stocks)) {
        throw "Exit";
    }
    Log("Initial information: ", "Total Money:", preAccount.Balance, "Total Coins:", preAccount.Stocks);
    var alertAlrelady = false;
    while (true) {
        Sleep(LoopInterval * 1000);
        var account = GetAccount();
        if (AlertMode == 2) {
            if ((MinCoin > 0 && account.Stocks < MinCoin) || (MinCNY > 0 && account.Balance < MinCNY)) {
                if (!alertAlrelady) {
                    Log(account);
                    Notify(exchange.GetName() + "Insufficient funds Total money: " + account.Balance + ", Currency: " + account.Stocks);
                    alertAlrelady = true;
                }
            } else {
                alertAlrelady = false;
            }
        } else if (account.Stocks != preAccount.Stocks || account.Balance != preAccount.Balance) {
            if (AlertMode == 0 || (MaxDiffCoin > 0 && Math.abs(account.Stocks - preAccount.Stocks) >= MaxDiffCoin) || (MaxDiffCNY > 0 && Math.abs(account.Balance - preAccount.Balance) >= MaxDiffCNY)) {
                Log(account);
                preAccount = account;
                Notify(exchange.GetName() + "The account changes to total money: " + account.Balance + ", Currency: " + account.Stocks);
            }
        }
    }
}
```

> Detail

https://www.fmz.com/strategy/2006

> Last Modified

2014-12-24 23:22:24
