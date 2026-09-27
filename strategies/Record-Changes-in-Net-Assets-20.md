
> Name

Record-Changes-in-Net-Assets-20

> Author

中本姜

> Strategy Description

Explanation
- This strategy evolved from https://www.fmz.com/strategy/5349. It mainly calculates the changes in net income of the account strategy when borrowing currency is included.
- Net asset change: account net asset change situation
- The status information bar will display the following information:
   - Initial Net Assets / Initial Net Money / Initial Net Coin: Displays the initial net assets and net currency status
   - Current net assets / current net money / current net coins: show in red if going long, show in green if going short
  -  Changes in net assets/total income/monthly income/maximum drawdown: if net assets increase compared with the previous time, it will be displayed in red, if it decreased compared with the previous time, it will be displayed in green
  - Borrow money / Borrowing interest:
  - Borrow currency / Currency borrowing interest
@time: The "monthly income, net money, net currency, borrowed currency, and current interest owed" information will be notified every time hour; if the net currency is positive, it means you are doing long, and if the net currency is negative, you are short.
@shuaxintime: Notify the change in account net assets every shuaxintime minutes
@profit_base: Changes in net assets at the start
@borrow_bi: Total borrowed at start
@interest_bi_base: Total interest owed from borrowed coins at the start
@interest_bi: Borrowing interest, default0.001

-TODO
Directly call loan information and calculate changes in net assets

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|time|true|Notification interval (hours))|
|shuaxintime|30|Refresh interval (minutes))|
|profit_base|false|Change in initial net assets|
|borrow_bi|false|Borrowed Coins Quantity|
|interest_bi_base|false|The interest currently owed on the borrowed currency|
|interest_bi|0.001|Daily Interest on Borrowed Currency|
|borrow_qian|false|Borrowed Money Amount|
|interest_qian|0.001|Daily Interest on Borrowed Money|
|interest_qian_base|false|Interest owed on borrowed money now|
|log_reset|false|log reset|


> Source (javascript)

``` javascript
function EnsureCall(e, method) {
    var r;
    while (!(r = e[method].apply(this, Array.prototype.slice.call(arguments).slice(2)))) {
        Sleep(1500);
    }
    return r;
}

function adjustFloat(v) {
    return Math.floor(v*1000)/1000;
}

function main() {
    SetErrorFilter("502:|503:|unexpected|network|timeout|WSARecv|Connect|GetAddr|no such|reset|http|received|EOF");
    var zhouqi = time * 3600000;
    var shuaxin = shuaxintime * 60000;
    var time0 = new Date().getTime();
    var time_mail = time0 + zhouqi - 5000;
    var time1 = time0 + shuaxin - 5000;
    var accounts = new Array([exchanges.length]);
    var tickers = new Array([exchanges.length]);
    var qian = [0, 0];
    var bi = [0, 0];
    var bi_money = [0, 0];
    var pnow = 0;
    var profit = profit_base;
    var vv = 0;
    var lv = profit;
    var msg = "No data available for now";
    var n = 0;
    var history = 0;
    var last_history = 0;
    var max_history = 0;
    var min_history = 0;
    var max_down = 0;
    
    var net_msg = 0;
    var profit_msg = 0;
    var bi_interest_msg = 0;
    var qian_interest_msg = 0;
    var init_profit_msg = 0;
    var status_log= 0;
    var red_color = "#ff0000";
    var green_color = "#006600";
    
    
    exchanges[0].SetLimit(1000);
    accounts[0] = EnsureCall(exchanges[0], "GetAccount");
    Sleep(2000);
    tickers[0] = EnsureCall(exchanges[0], "GetTicker");
    Sleep(2000);
    if (log_reset) {
        LogProfitReset(); 
    }
    qian[0] = accounts[0].Balance + accounts[0].FrozenBalance - borrow_qian - interest_qian_base;
    bi[0] = accounts[0].Stocks + accounts[0].FrozenStocks - borrow_bi - interest_bi_base;
    bi_money[0] = bi[0] * tickers[0].Last;
    net0 = qian[0] + bi_money[0];
    msg = "Initial Net Assets / Initial Net Money / Initial Net Coins:" + net0 + " / " + qian[0] + " / " + bi[0] + "@";
    init_profit_msg = "Initial Net Assets / Initial Net Money / Initial Net Coins:" + net0 + " / " + qian[0] + " / " + bi[0];
    LogProfit(lv, msg);
    LogStatus(msg);
    LogProfit(lv, "All account initial data has been processed, waiting for notification......@");
    while (true) {
        if (new Date().getTime() > time1) {
            vv = profit;
            qian[1] = 0;
            bi[1] = 0;
            bi_money[1] = 0;
            profit = profit_base;
            lv = 0;
            exchanges[0].SetLimit(1000);
            accounts[0] = EnsureCall(exchanges[0], "GetAccount");
            Sleep(2000);
            tickers[0] = EnsureCall(exchanges[0], "GetTicker");
            Sleep(2000);
            qian[1] += accounts[0].Balance + accounts[0].FrozenBalance;
            interest_qian_all = interest_qian_base + borrow_qian * interest_qian * (new Date().getTime() - time0) / 86400000;
            borrow_qian_all = borrow_qian + interest_qian_all;
            qian[1] = qian[1] - borrow_qian_all;
            bi[1] = accounts[0].Stocks + accounts[0].FrozenStocks;
            interest_bi_all = interest_bi_base + borrow_bi * interest_bi * (new Date().getTime() - time0) / 86400000;
            borrow_bi_all = borrow_bi + interest_bi_all;
            bi[1] = bi[1] - borrow_bi_all;
            bi_money[1] = bi[1] * tickers[0].Last;
            profit += qian[1] + bi_money[1] - net0;
            lv = adjustFloat(profit * 259200000000 / ((net0) * (new Date().getTime() - time0)));
            history = Math.round(profit * 1000) / 1000;
            max_history = Math.max(history, max_history);
            if (max_history == history) {
                min_history = max_history;
            }
            min_history = Math.min(history, min_history);
            var present_maxdown = (min_history - max_history) / (max_history + net0) * 100;
            max_down = adjustFloat(Math.min(present_maxdown, max_down));
            var lv_total = adjustFloat(profit / net0 * 100);
            
            net_msg = "Current Net Assets / Current Net Money / Current Net Coins:" + (qian[1] + bi_money[1]) + " / " + qian[1] + " / " + bi[1];
            if (bi[1] > 0) {
                net_msg += red_color;
            }
            else if (bi[1] < 0) {
                net_msg += green_color;
            }
            profit_msg = "Net Asset Change / Total income / Monthly profit / Maximum drawdown:" + history + " / " + lv_total + "% / " + lv + "% / " + max_down + "%";
            if (last_history < history) {
                profit_msg += red_color;
            }
            else if (last_history > history) {
                profit_msg += green_color;
            }
            last_history = history;
            qian_interest_msg = "Borrow money / Borrowing interest:" + borrow_qian + " / " + interest_qian_all;
            bi_interest_msg = "Borrow currency / Currency borrowing interest:" + borrow_bi + " / " + interest_bi_all;
            msg = "Monthly profit / Net money / Net coins / Net assets / Borrow money / Borrowing interest / Borrow coins / Interest owed now:" + lv + " / " + qian[1] + " / " + bi[1] + " / " + (qian[1] + bi_money[1]) + " / " + borrow_qian + " / " + interest_qian_all + " / " + borrow_bi + " / " + interest_bi_all;
            if (new Date().getTime() > time_mail) {
                n += 1;
                LogProfit(history, msg);
                time_mail += zhouqi;
            } else {
                LogProfit(history, "Net Asset Variation");
            }
            time1 += shuaxin;
        }
        Sleep(5000);
        $.Draw();
        status_log = init_profit_msg + "\n" + net_msg + "\n" + profit_msg + "\n" + qian_interest_msg + "\n" + bi_interest_msg;
        LogStatus(status_log);
    }
}
```

> Detail

https://www.fmz.com/strategy/8916

> Last Modified

2016-06-14 09:04:20
