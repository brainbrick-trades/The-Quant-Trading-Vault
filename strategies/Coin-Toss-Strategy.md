
> Name

Coin-Toss-Strategy

> Author

扁豆子

> Strategy Description

Complete T-Shen public account, Lv Shen's special strategic translation.
The following is reprinted content,
Please pay more attention to "Qianqian's Quantitative World" to obtain more strategy source codes!!
Also give yourself an ad~
Official account "Flat Bean's Quantitative Journal"" 
Publicly execute online quantitative bankruptcies daily for everyone~
There are many more benefits for you to get~

--------

Make good use of volatility and outperform the BTC market is that simple!
Original by Lu Yangyang Qianqian's Quantitative World 3 days ago
" The research and development of quantitative strategies actually has two sides. It is very difficult for those who are just getting started. It is not only the code at the "technical" level, but also the strategic and logical thinking at the "strategic" level. Both are important and must not be biased."





Hello to all the Qianqian quantification enthusiasts!!!



This article is the second issue of special invitations. Qianqian is honored to invite Master Lu Yangyang (WeChat ID LE_CHIFFRE1) to introduce to you: how to use the volatility factor to easily outperform the BTC market and achieve "dimensionality reduction strike""!

Lu Shen comes from a traditional quantitative investment institution. He has also been deeply involved in the currency exchange business and has rich experience and unique insights in the quantitative field. The content of this issue of Lu Shen covers inspiration, coding implementation, personal insights, etc. It is full of useful information. Qianqian herself felt that she benefited a lot from reading it. She really admires and thanks Lu Shen. I strongly recommend everyone to read it carefully.!

Let's welcome Lu Shen to introduce the volatility strategy to everyone.


01

-



Introduction



Hello everyone, today I am honored to post an article on the "Qianqian's Quantification" public account, and I would also like to thank Boss T (one of Qianqian's nicknames) for the invitation. This is my first time writing an article for Boss T. I am completely free to use my spare time after work. Please correct the quality and errors and include them in the article. Thank you all.
 

TThe boss said to write something quantitative, but he didn't give any scope. I really don't know where to start. Then start with the topics you most enjoy discussing with others. Quantitative indicators and strategies (which can be assisted or automated). Of course, in the end we have to add a cliché: "Investment is risky, so you need to be cautious when entering the market." Strategies only provide ideas and reference for everyone, and you are responsible for your profits and losses. All profits and losses from using this strategy have nothing to do with myself and the main body of the "Qianqian Quantitative World" public account.


Disclaimer finished, now let's start the main topic.




02

-



A simple volatility strategy





People who are familiar with me actually know that personally, I don't like Alpha's gameplay very much. Relatively speaking, I believe in Beta more and study Beta more. As for why, e.........mmmmm, I don't know how to answer~~, please make up your own mind. If you are interested, you can send a private message or leave a message to the author of the public account. If the logic is clear and distinctive, the author himself will send you a small red envelope.

The research and development of quantitative strategies actually has two sides. It is very difficult for those who are just getting started. It is not only the code at the "technical" level, but also the strategic and logical thinking at the "strategic" level. Both are important and must not be taken in either direction. The strategy I will introduce to you today is actually inspired by a research report from Huatai many years ago. Please read it carefully and it is just an inspiration. The reason why I say this is because the logic of this strategy is completely different from what was mentioned in the research report. Let's talk privately with Mr. T about the specific research report.

This strategy algorithm adopts the rolling yield fluctuation principle of the logarithmic price rise and fall in a certain period, and calculates the rolling highest value and the minimum value in a certain period based on the fluctuation interval. The highest value is used as the upper channel, and the minimum value is used as the lower channel. Break through the upper channel and open a position. The rolling average of the upper and lower pipelines is used as the closing line. (Knock on the blackboard here!)

For the specific graphic visualization interface, please refer to the PPT below. This graphic was drawn by me using Pyecharts. Please contact Mr. T privately for the specific code.

 ![IMG](https://www.fmz.com/upload/asset/95f6e8b8196998728de6.png) 



Actually, this strategy was the one I used before for broad-based ETFs, and of course it was also used for stock trading with index timing. Later, I directly applied it to the cryptocurrency world and was astonished to find that it really was a dimensionality reduction strike, and the parameters didn't need to be changed.



 ![IMG](https://www.fmz.com/upload/asset/95c0d34f79df83ec85c5.png) 





The figure below shows the performance of the backtesting for the year. Screenshots of some of the code logic are as follows:


 ![IMG](https://www.fmz.com/upload/asset/951f56f73aeb0da6ffa1.png) 




The above is actually to calculate the indicator data through pandas after reading the data.


 ![IMG](https://www.fmz.com/upload/asset/951a76802f3a22a6da7c.png) 




After calculation, you can usepd.to_csv()The function outputs data and is used in the screenshot abovepyechartsPerform visual output (Note: I use the old versionpyecharts).



For all the specific strategies, visualizations, and performance indicator code, I still messaged Mr. T privately.




03

-

Casual Talk on Quant



Next I will mainly talk about two points. First: Some people have a lot of questions or say why you people can publish real strategies. Are you fake liars? Or is it really about saving all sentient beings? Haha~~. First of all, a good strategy is not afraid of disclosure. This is not a weapon development for war-level confrontation, which will determine life or death. Therefore, I and other organizations or individuals are not afraid of so-called strategic secrets, because in my opinion, CTA has no secrets. It's just ideas that everyone thinks of and doesn't think of. Secondly, this version is my oldest version. On this basis, I have made several upgrades, such as adding other conditional judgments, take-profit and stop-loss, etc., and of course it also includes parameter adjustments for other types of cycles, etc.



Secondly: Many people, whether beginners, those who have just started, or even experienced players, need sources of inspiration, including factor discovery in stocks, ideas for timing strategies, and so on. These often come from subjective experience, research reports, communication within the community, etc. It does not exclude the possibility of buying some strategies available in the market and then reading and understanding them, and modifying them according to one's own risk tolerance and specific needs.



Finally, to summarize, quantification is originally an imported product, and programmed trading is a subset of quantification. As early as when I was in college (around 2009), some people had been involved in programmed methods such as TB and Pyramid. If we continue to do it today, it can be said that these people who were the first to foresee and foresight have been there for 10 years, and this does not include those who "brought back" high-frequency strategies and systems from Wall Street. Therefore, quantitative strategies or programmatic strategies have been going on in China for some time, but in terms of current market share, participants, and policy support, quantification is still a very small part of the market, even though research reports on multi-factor analysis and strategy modeling are flying everywhere. Some people like to use brainless logic to compare this with the United States, believing that China's quantitative future development trends will be the same as those of the United States, with explosive growth and so on. However, this is not Ruixing's "coffee and small pot of tea" business logic. China has Chinese characteristics, and the road ahead is still thorny and bumpy. Therefore, we have also gathered a large circle of institutional and individual investors. We hope that everyone can get to know each other, communicate and grow together, and make a small contribution to this industry.



Finally, I would like to thank the 'Qianqian's Quantification' public account for trusting my professional expertise and inviting me to contribute articles. If anyone has specific questions about code or strategies, please private message me or Master T. I am also in Master T's group.





Finally, thanks again to Lü Shen for his wonderful explanation!

If you haven't joined the quantitative discussion group yet, come join us quickly to get your study materials!!!

Qianqian Honorable Guardian!


 ![IMG](https://www.fmz.com/upload/asset/9576f0337a4b9144925e.png) 



Scan on WeChat
Follow This Public Account

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|tp_first|0.03|tp_first|
|trailing_tp|0.01|trailing_tp|
|st|0.05|st|


> Source (javascript)

``` javascript
/*backtest
start: 2020-01-20 00:00:00
end: 2021-01-19 23:59:00
period: 15m
basePeriod: 5m
exchanges: [{"eid":"Futures_BitMEX","currency":"XBT_USD","fee":[0.008,0.1]}]
args: [["st",0.1]]
*/

// Initialize
exchange.SetContractType('XBTUSD')
_CDelay(100)
// take profit and stop loss
var TP_status = false // Whether to trigger trailing take profit 
var TP_HH = 0
var TP_LL = 0
var B = 1

// Get exchange information
function UpdateInfo() {
    account = exchange.GetAccount()
    pos = exchange.GetPosition()
    records = exchange.GetRecords()
    ticker = exchange.GetTicker()
}

// Customize this profit and loss
function Onept() {
    // Update user information
    UpdateInfo()
    // If the current balance is greater than the previous balance, Then the number of profits+1, andpt_1Set as current balance
    if (account.Stocks - pt_1 > 0) {
        pt_times = pt_times + 1
        Log('Make money this time~~~~ (＾Ｕ＾)ノ~ＹＯ', account.Stocks - pt_1)
        B = 1
        pt_1 = account.Stocks
    }
    // If the current balance is less than the previous balance, Then the number of losses+1, andpt_1Set as current balance
    if (account.Stocks - pt_1 < 0) {
        st_times = st_times + 1
        Log('I lost money this time.... /(ㄒoㄒ)/~~', account.Stocks - pt_1)
        B = B * 1.618
        pt_1 = account.Stocks
    }
}

// Draw lines
function PlotMA_Kline(records) {
    $.PlotRecords(records, "K")
}

// Trailing Take Profit Initial%, TrackingU
function TP() {
    var TP_first_long = pos[0].Price + tp_first * ticker.Last
    var TP_trailing_long = TP_HH - trailing_tp * ticker.Last
    var TP_first_short = pos[0].Price - tp_first * ticker.Last
    var TP_trailing_short = TP_LL + trailing_tp * ticker.Last
    // When holding a long position, Current price greater than opening+Initial Take Profit Price -> Trigger trailing take profit 
    if ((pos[0].Type == 0) && (ticker.Last > TP_first_long)) {
        // Log('When holding a long position, Current price greater than opening+Initial Take Profit Price -> Trigger trailing take profit', TP_HH)
        TP_status = true
        // Trigger trailing take profit, Uninitialized maximum opening price -> After opening a position, update the maximum price to the current price
        if (TP_status === true && TP_HH == 0) {
            Log('Trigger trailing take profit, Uninitialized maximum opening price -> After opening a position, update the maximum price to the current price', TP_HH)
            TP_HH = ticker.Last
        }
        // Trigger trailing take profit, Maximum price after existing positions opened, The current price is greater than the maximum price after opening the position -> After opening a position, update the maximum price to the current price
        else if (TP_status === true && TP_HH != 0 && ticker.Last > TP_HH) {
            Log('Trigger trailing take profit, Maximum price after existing positions opened, The current price is greater than the maximum price after opening the position -> After opening a position, update the maximum price to the current price', TP_HH)
            TP_HH = ticker.Last
        }
        // Trigger trailing take profit, Maximum price after existing positions opened, Current price is less than (Maximum price reduction after opening a position - RetracementUSD) -> Close short position with take profit
        else if (TP_status === true && TP_HH != 0 && ticker.Last < TP_trailing_long) {
            Log('Trigger trailing take profit, Maximum price after existing positions opened, Current price is less than (Maximum price reduction after opening a position - RetracementUSD) -> Close short position with take profit', TP_HH)
            exchange.SetDirection("closebuy")
            exchange.Sell(ticker.Buy, pos[0].Amount, "At/In" + ticker.Last + "Take Profit Close Long Position!! Opening price: " + pos[0].Price + "Quantity: " + pos[0].Amount)
            $.PlotFlag(new Date().getTime(), 'Sell', 'PT_BK' + ticker.Sell)
            Onept()
            TP_status = false
            TP_HH = 0
        }
    }
    // When holding a short position, Current price less than opening-Initial Take Profit Price -> Trigger trailing take profit
    else if ((pos[0].Type == 1) && (ticker.Last < TP_first_short)) {
        // Log('When holding a short position, Current price less than opening-Initial Take Profit Price -> Trigger trailing take profit', TP_LL)
        TP_status = true
        // Trigger trailing take profit, Uninitialized maximum opening price -> After opening a position, update the minimum price to the current price
        if (TP_status === true && TP_LL == 0) {
            Log('Trigger trailing take profit, Uninitialized maximum opening price -> After opening a position, update the minimum price to the current price', TP_LL)
            TP_LL = ticker.Last
        }
        // Trigger trailing take profit, Minimum price after existing positions opened, The current price is less than the minimum price after opening the position -> After opening a position, update the minimum price to the current price
        else if (TP_status === true && TP_LL != 0 && ticker.Last < TP_LL) {
            Log('Trigger trailing take profit, Minimum price after existing positions opened, The current price is less than the minimum price after opening the position -> After opening a position, update the minimum price to the current price', TP_LL)
            TP_LL = ticker.Last
        }
        // Trigger trailing take profit, Minimum price after existing positions opened, Current price is greater than (After opening a position, the minimum price is reduced + RetracementUSD) -> Close long position with take profit
        else if (TP_status === true && TP_LL != 0 && ticker.Last > TP_trailing_short) {
            Log('Trigger trailing take profit, Minimum price after existing positions opened, Current price is greater than (After opening a position, the minimum price is reduced + RetracementUSD) -> Close long position with take profit', TP_LL)
            exchange.SetDirection("closesell")
            exchange.Buy(ticker.Sell, pos[0].Amount, "At/In" + ticker.Last + "Take Profit Close Short Position!! Opening price: " + pos[0].Price + "Quantity: " + pos[0].Amount)
            $.PlotFlag(new Date().getTime(), 'Buy', 'PT_SK' + ticker.Sell)
            Onept()
            TP_status = false
            TP_LL = 0
        }
    }
}

// stop loss %
function Stoploss() {
    // When holding a long position, Current price less than opening-Stop loss price, Short to close long
    if ((pos[0].Type == 0) && (ticker.Last < pos[0].Price - st * ticker.Last)) {
        Log('When holding a long position, Current price less than opening-Stop loss price, Short to close long')
        exchange.SetDirection("closebuy")
        exchange.Sell(ticker.Buy, pos[0].Amount, "At/In" + ticker.Last + "Stop Loss Close Long Position!! Opening price: " + pos[0].Price + "Quantity: " + pos[0].Amount)
        $.PlotFlag(new Date().getTime(), 'Sell', 'ST_BK' + ticker.Buy)
        Onept()
    }
    // When holding a short position, Current price greater than opening+Stop loss price, Long to close short
    else if ((pos[0].Type == 1) && (ticker.Last > pos[0].Price + st * ticker.Last)) {
        Log('When holding a short position, Current price greater than opening+Stop loss price, Long to close short')
        exchange.SetDirection("closesell")
        exchange.Buy(ticker.Sell, pos[0].Amount, "At/In" + ticker.Last + "Stop Loss Close Short Position!! Opening price: " + pos[0].Price + "Quantity: " + pos[0].Amount)
        $.PlotFlag(new Date().getTime(), 'Buy', 'ST_SK' + ticker.Sell)
        Onept()
    }
}

// Calculate Kelly formula position
function PriceAmount() {
    // How much can be won 
    y = tp_first
    // How much will you lose if you lose? 
    s = st
    //Odds
    b = y / s
    // Probability of Winning
    if (total_times < 10) {
        p = 0.382
    } else {
        p = pt_times / total_times
    }
    // Probability of Losing
    q = 1 - p
    // Kelly Formula
    f = (b * p - q) / b
    // LimitBmaximum value
    if (B > 16.18) {
        B = 16.18
    }
    //Amount = _N(Math.abs(f) * account.Stocks * ticker.Last * B, 0)
    Amount = _N(0.618 * account.Stocks * ticker.Last, 0)
    //Log(Amount)
}

// Transaction logic
function onTick() {
    // Get uniform distribution 0-9 random number
    ToTheMoon = Math.floor(Math.random() * 10)
    // When no position
    if (pos.length == 0) {
        // Long 
        if (ToTheMoon > 5) {
            exchange.SetDirection("buy")
            exchange.Buy(ticker.Sell, Amount)
            $.PlotFlag(new Date().getTime(), 'Buy', 'BK' + ticker.Sell)
            total_times = total_times + 1
        }
        // Short 
        if (ToTheMoon < 4) {
            exchange.SetDirection("sell")
            exchange.Sell(ticker.Buy, Amount)
            $.PlotFlag(new Date().getTime(), 'Sell', 'SK' + ticker.Buy)
            total_times = total_times + 1
        }
    }
        // When Long
    if (pos.length > 0 && pos[0].Type == 0) {
        // close long 
        if (ToTheMoon < 1) {
            exchange.SetDirection("closebuy")
            exchange.Sell(ticker.Buy, pos[0].Amount)
            $.PlotFlag(new Date().getTime(), 'Sell', 'PBK')
            Onept()
        }
    }
    // When Short
    if (pos.length > 0 && pos[0].Type == 1) {
        // close short 
        if (ToTheMoon > 8) {
            exchange.SetDirection("closesell")
            exchange.Buy(ticker.Sell, pos[0].Amount)
            $.PlotFlag(new Date().getTime(), 'Buy', 'PSK')
            Onept()
        }
    }
}


function main() {
    UpdateInfo()
    // Statistics
    pt_1 = account.Stocks
    total_times = 0
    pt_times = 0
    st_times = 0
    while (1) {
        UpdateInfo()
        PriceAmount()
        onTick()
        PlotMA_Kline(records)
        if (pos.length > 0) {
            TP()
        }
        if (pos.length > 0) {
            Stoploss()
        }
        LogStatus("Total Balance: " + _N(ticker.Last * account.Stocks, 2), " Order Quantity: " + Amount, " Order Multiplier: " + B, " ToTheMoon: " + ToTheMoon, " Order Size Ratio: " + _N(Amount * 100 / _N(ticker.Last * account.Stocks, 2), 2), "% Win rate: " + _N(p * 100, 2), "%", total_times, pos)
    }
}
```

> Detail

https://www.fmz.com/strategy/201007

> Last Modified

2021-01-21 18:16:19
