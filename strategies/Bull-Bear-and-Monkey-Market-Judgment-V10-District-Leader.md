
> Name

Bull-Bear-and-Monkey-Market-Judgment-V10-District-Leader

> Author

区班量化

> Strategy Description

We found that the most important thing in quantitative investment is timing, which is to determine whether the current market is a bear market, a bull market, or a monkey market. In this article, the district class leader will discuss how to make timing strategies.
   
   There are many ways to do timing: moving average judgment, Bollinger Bands, trading volume, and cycle highs and lows.

   Moving average judgment is to judge whether the current market is rising or falling through the inclination of the moving average. By judging whether it stands above the 5-day moving average, it is judged whether it is a bull market, and by judging whether it falls below the 120-day moving average, it is judged whether it has entered a bear market. Several factors combine to determine the current market strength.
   
   Bollinger Bands is a good way to judge whether the market is rising or falling based on the inclination of the center line of Bollinger Bands. Selling high and buying low based on the highs and lows of the Bollinger Bands is a good practice in the monkey market. If the opening of Bollinger Bands increases, it is a precursor to market fluctuations.
   
   Trading volume is generally an auxiliary means, and generally there will be increased volume at the bottom and top. One benefit of digital currencies is that trading depth is easy to obtain. By analyzing the status of pending orders and combined with trading volume, we can also determine the current market heat.
   
   The above strategy is somewhat difficult to implement and needs to be slowly tuned. Cycle high and low points are the key strategies discussed in this article, which have the advantages of simple implementation and direct effect. The idea of ​​cycle high and low points is very simple. It is to combine the short cycle high and low points and the long cycle high and low points to determine whether the current market is a bull market, a calf market, a bear market, a bear market, or a monkey market. With this timing judgment, we can cooperate with certain strategies when the market turns. For example, from calf to bull, you can increase your position. If the bull comes to the monkey market, you can close your position. From the monkey market to the bear market, you can initially establish a short position. If you enter Big Bear, go short.
   
   Let's post part of the code first. The main ideas are in the comments, so people who are interested can naturally understand it. For long periods, choose the daily line, and 5 days is the period. For short periods, choose the 30-minute line, and 10 is the period, which is 5 hours. Parameters can be adjusted based on the volatility and position adjustment of related digital currencies.
![![IMG](https://www.fmz.com/upload/asset/131028f566a19a2df8d71.png) ](https://www.fmz.com![IMG](https://www.fmz.com/upload/asset/131028f566a19a2df8d71.png)) 
![![IMG](https://www.fmz.com/upload/asset/1311782042b83c9281493.png) ](https://www.fmz.com![IMG](https://www.fmz.com/upload/asset/1311782042b83c9281493.png)) 

   Let's post the execution results again. It can be seen that the little bear turned into a big bear from September 24 to September 25, the shock monkey market added a little bear from September 26 to October 7, and the calf signal appeared on October 9, all have correct prompts. It can be seen that the cycle high and low point strategy is simple but not simple.
![ ![IMG](https://www.fmz.com/upload/asset/130e0870276675121b757.png) ](https://www.fmz.com![IMG](https://www.fmz.com/upload/asset/130e0870276675121b757.png))
![ ![IMG](https://www.fmz.com/upload/asset/130dd6af2327f75a3e071.png) ](https://www.fmz.com![IMG](https://www.fmz.com/upload/asset/130dd6af2327f75a3e071.png))

   Combining digital currency selection strategies and hedging strategies, there are more ways to play. If the top 20 digital currencies with market capitalization are sorted out in terms of bullish and bearish status, and two digital currencies, big bears and bulls, are selected for hedging each time, low-risk arbitrage can basically be achieved. This will be a strategy that can be improved later.

   Interested friends can also [find me on Bihu](https://m.bihu.com/signup?i=1ewtKO&c=4&s=4). Bihu is a place where you can earn digital currency by writing articles.
![![IMG](https://www.fmz.com/upload/asset/1314562ca57eb3ea873e1.jpg)](https://www.fmz.com![IMG](https://www.fmz.com/upload/asset/1314562ca57eb3ea873e1.jpg))

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Interval|60|Polling interval (seconds))|
|dnum|5|Daily cycle|
|mnum|10|30Minute line period|


> Source (javascript)

``` javascript
/*backtest
start: 2019-01-01 00:00:00
end: 2019-10-10 00:00:00
period: 1d
exchanges: [{"eid":"Bitfinex","currency":"BTC_USD"}]
*/
//Determine the current market by the highs and lows of fast and slow cycles
//After registering on Bihuhttps://m.bihu.com/signup?i=1ewtKO&s=4&c=4
//Search IoT blockchain to contact the author or group leader
function main() {
    var dhigh;
    var dlow;
    var mhigh;
    var mlow;
    var status_name=["Monkey City","Daniel","Mavericks","Big Bear","Little Bear"];  //Define and assign value
    var before_status=0;
    var now_status=0;
    while (true) {
        var drecords = exchange.GetRecords(PERIOD_D1);
        var mrecords = exchange.GetRecords(PERIOD_M30);
        //Daily line5High and low points within days(Does not include currentBar)
        dhigh=TA.Highest(drecords, dnum, 'High');
        dlow=TA.Lowest(drecords, dnum, 'Low');
       
        //30Minute chart10Highs and lows within the cycle(Does not include currentBar)
        mhigh=TA.Highest(mrecords, mnum, 'High');
        mlow=TA.Lowest(mrecords, mnum, 'Low');
        
        if(mlow>dhigh){ //Minute low breaks above the daily high, big bull begins
            now_status=1;
            //Log("Daniel");
        }else if(mhigh>dhigh&&mlow<=dhigh){ //The minute high broke through the daily high, but the minute low did not break through the daily high, and the Mavericks started
            now_status=2;
            //Log("Mavericks");
        }else if(mhigh<dlow){  //Minute low breaks below the daily low, big bear begins
            now_status=3;
            //Log("Big Bear");
        }else if(mlow<dlow&&mhigh>dlow){  //The minute low fell below the daily low, but the minute high did not fall below the daily low, and the bear began
            now_status=4;
            //Log("Little Bear");
        }else{  //no direction, monkey market
            now_status=0;
            //Log("Monkey City");
        }
        if(now_status!=before_status){
            Log("Daily high",dhigh," Daily low",dlow,"30Minute chart high",mhigh," 30Minute chart low",mlow);
            Log(status_name[before_status],"Transfer",status_name[now_status]);
            before_status=now_status;
        }
        Sleep(Interval*1000);
    }
}
```

> Detail

https://www.fmz.com/strategy/170014

> Last Modified

2019-11-15 15:48:27
