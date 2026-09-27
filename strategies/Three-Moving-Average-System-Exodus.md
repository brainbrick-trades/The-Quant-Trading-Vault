
> Name

Three-Moving-Average-System-Exodus

> Author

Exodus[策略代写]

> Strategy Description

This system is a two-way contract strategy. When the conditions are met, whether to go long or short, the order amount is the number of contracts. When using Binance, the order amount is a few BTC. When using Huobi, the order amount unit is Zhang.
[7-31Update]
The parameters of this strategy are suitable for operation at the 1-hour level, but the number of orders opened at the hour-level is too small, so the minute-level is updated. However, parameters need to be modified manually at the minute level.

The following backtest results are in hourly intervals
**** 4-27to7-25****
Principal 300, order quantity0.04btc
 ![IMG](https://www.fmz.com/upload/asset/1f4e9984f53d575c506c1.png) 
**** 1-1to7-25****
Principal 300, order amount 0.03 BTC, order quantity 0.04 is insufficient principal
If you want to use it yourself, please conduct a backtest to determine your order volume.
 ![IMG](https://www.fmz.com/upload/asset/1f47c59a9ac1f93694193.png) 
 
 If you make money, consider supporting the author
  ![IMG](https://www.fmz.com/upload/asset/1f4c36c1fca8b23e727c7.jpg) 
  

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|afterEmaCrossTime|4|Only Allow Operation if MACD Meets Conditions Within a Few Candles After K-Line Golden Cross or Death Cross|
|buyVolume|0.016|Transaction quantity(0.016BTC)|
|stopLossRate|true|Stop loss rate (leverage not calculated))|
|winLossRate|5|Profit and Loss Ratio|
|period|60|Period (minutes)|
|EMA1|8|Fastest moving average period|
|EMA2|34|Medium-speed moving average period|
|EMA3|89|Slowest moving average period|
|MACD1|16|MACDParameters1|
|MACD2|26|MACDParameters2|
|MACD3|9|MACDParameters3|


> Source (javascript)

``` javascript
/*backtest
start: 2021-04-27 00:00:00
end: 2021-07-25 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT","balance":300}]
args: [["afterEmaCrossTime",4],["buyVolume",0.04],["winLossRate",5]]
*/

function GetCrossStatus(a, lastA, b, lastB) {
    let lastStatus = lastA < lastB;
    let curStatus = a < b;
    let crosssStaus = 0; //0Indicates no crossover,1means golden cross,2means death cross
    //Determine golden cross or death cross,Simultaneously determine if it is greater at the moment0Axis or less than0axis,Because in this system it requires a golden cross whenmacd>0Only then does it make sense; during a death crossmacd<0makes sense
    if (curStatus != lastStatus) //Different states indicate golden cross or death cross
    {
        if (a > b) {
            crosssStaus = 1; //golden cross
        }
        if (a < b)
            crosssStaus = 2; //death cross
    }
    return crosssStaus;
}
var lastOpenTime;

function GetCurRecord(records) {
    return records[records.length - 1];
}

function GetCurTime(records) {
    return GetCurRecord(records).Time;
}

function GetCurPrice(records) {
    return GetCurRecord(records).Close;
}

function Open(direction) {
    let pos = exchange.GetPosition()[0];

    if (pos != null) {
        return;
    }
    let amount = buyVolume;
    if (direction == 1) { //go long
        Log("go long", amount);
        exchange.SetDirection("buy");
        exchange.Buy(-1, amount);
    }
    if (direction == 2) { //go short
        Log("go short", amount);
        exchange.SetDirection("sell");
        exchange.Sell(-1, amount);
    }
    
}

function Close(ticker,fastLine,midLine) {
    let pos = exchange.GetPosition()[0];

    if (pos == null) {
        return;
    }
    
    if (pos.Type == PD_LONG) {
        if (ticker.Last < pos.Price*(1- stopLossRate/100) || ticker.Last > pos.Price*(1+(stopLossRate*winLossRate)/100)) {
            Log("close long,The opening price is:",pos.Price,"This profit:",pos.Profit);
            exchange.SetDirection("closebuy");
            exchange.Sell(-1, pos.Amount);
            
        }
    }
    if (pos.Type == PD_SHORT) {
        if (ticker.Last > pos.Price*(1+ stopLossRate/100) || ticker.Last < pos.Price*(1-(stopLossRate*winLossRate)/100) ) {
            Log("close short,The opening price is:",pos.Price,"This profit:",pos.Profit);
            exchange.SetDirection("closesell");
            exchange.Buy(-1, pos.Amount);
        }
    }
}




var lastEmaCrossTime = 0;
var lastMacdCrossTime = 0;

function NearMacdCross(time) {
    //Log("MACD",time,lastMacdCrossTime,time - lastMacdCrossTime);
    return time - lastMacdCrossTime <= afterEmaCrossTime * 1000 * 3600;
}

function NearEmaCross(time) {
    //Log("EMA",time,lastMacdCrossTime,time - lastMacdCrossTime);
    return time - lastEmaCrossTime <= afterEmaCrossTime * 1000 * 3600;
}


var emaMeet = 0; //0Indicates not satisfied,1Meets long condition,2Meets short condition
var macdMeet = 0; //JudgmentmacdWhether the condition is met,0Indicates not satisfied,1Indicates long conditions are met,2Indicates short conditions are met
function main() {
    exchange.SetContractType("swap");
    while (1) {
        let r = exchange.GetRecords(PERIOD_M1*period);

        //************moving averageEMA****************
        let emaChart8 = TA.EMA(r, EMA1);
        let emaChart34 = TA.EMA(r, EMA2);
        let emaChart89 = TA.EMA(r, EMA3);

        let ema8 = emaChart8;
        let curEma8 = ema8[emaChart8.length - 1];
        let lastEma8 = ema8[emaChart8.length - 2];

        let ema34 = emaChart34;
        let curEma34 = ema34[emaChart34.length - 1];
        let lastEma34 = ema34[emaChart34.length - 2];

        let ema89 = emaChart89;
        let curEma89 = ema89[emaChart89.length - 1];
        let lastEma89 = ema89[emaChart89.length - 2];

        //Judgment8Average sum34The death cross and golden cross of moving averages; when a golden cross occurs, if the current bar is onema89Go long above moving average; when death cross occurs, if the body is onema89Short when below      
        let ticker = exchange.GetTicker();
        let low = ticker.Low;
        let high = ticker.High;
        let close = ticker.Close;

        Close(ticker,curEma8,curEma34);

        let crossStatus1 = GetCrossStatus(curEma8, lastEma8, curEma34, lastEma34);

        if (crossStatus1 != emaMeet) { //Update status when status changes
            if (crossStatus1 == 1) {
                emaMeet = 1;
                Log("emaGolden cross, time:", GetCurTime(r),talib.LINEARREG_SLOPE(ema8));
                lastEmaCrossTime = r[r.length - 1].Time;
            }
            if (crossStatus1 == 2) {
                emaMeet = 2;
                //Log("emaDeath cross, time:", GetCurTime(r));
                lastEmaCrossTime = r[r.length - 1].Time;
                //Log("Ema 2");
            }
        }

        //***************Macd*************
        let macdChart = TA.MACD(r, MACD1, MACD2, MACD3);

        let macd = macdChart[2]; //Kinetic energy column
        let curMacd = macd[r.length - 1]; //Current momentum bar
        let lastMacd = macd[r.length - 2]; //the previous momentum bar, directly judge based on the polarity of the momentum barmacdGolden cross and death cross of
        //auto lastMacd = macd[r.size() - 2]; //Previous momentum bar

        //Determine golden cross or death cross
        let dif = macdChart[0];
        let curDif = dif[r.length - 1];
        let lastDif = dif[r.length - 2];


        //Determine golden cross or death cross,Simultaneously determine if it is greater at the moment0Axis or less than0axis,Because in this system it requires a golden cross whenmacd>0Only then does it make sense; during a death crossmacd<0makes sense

        //MacdThe moment when a golden cross or a death cross is formed
        if (curMacd < 0 != lastMacd < 0) {

            if (curMacd > 0) {
                macdMeet = 1;
                //Log("macdgolden cross", lastMacd, curMacd);
                lastMacdCrossTime = GetCurTime(r);
            }
            if (curMacd < 0) {
                macdMeet = 2;
                //Log("macddeath cross", lastMacd, curMacd);
                lastMacdCrossTime = GetCurTime(r);

            }
        }


        let Account = exchange.GetAccount();
        let curBalance = exchange.GetAccount().Balance; //Balance
        let curStock = exchange.GetAccount().Stocks; //Coin amount

        //Moving average system
        var curTime = GetCurTime(r);
       
        if (NearEmaCross(curTime) && NearMacdCross(curTime)) {
            
            if (emaMeet == 1 && macdMeet == 1 && curDif >= 0) {
                Open(1);
            }
           
            if (emaMeet == 2 && macdMeet == 2 && curDif < 0) {
                Open(2);
            }
        }
        



        var myDate = new Date();
        var myDataM = myDate.getMinutes();
        var myDateS = myDate.getSeconds() * 1000;
        var myDateMs = myDate.getMilliseconds(); //Get milliseconds to reduce error
        Sleep(Math.abs(period - myDataM % period) * 60000 - myDateS - myDateMs);


    }


}
```

> Detail

https://www.fmz.com/strategy/301620

> Last Modified

2021-11-28 07:20:15
