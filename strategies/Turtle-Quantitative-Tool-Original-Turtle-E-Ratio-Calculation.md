
> Name

Turtle-Quantitative-Tool-Original-Turtle-E-Ratio-Calculation

> Author

道长





> Source (javascript)

``` javascript
/*backtest
start: 2018-01-01 00:00:00
end: 2021-03-04 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"OKEX","currency":"BTC_USDT"}]
*/

/**
 * ATRCalculation
 * @param records
 * @private
 */
function _ATR(records, period) {
     var acount = 0;
     var len = records.length;

     for (var i = len-1; i >= len-period; i--) {
          var decide = Math.abs(records[i].High - records[i].Low);
          acount += decide;
     }

     return (acount / period);
}

/**
 * Generate a random number from minNum to maxNum
 * @param minNum
 * @param maxNum
 * @return {number}
 */
function randomNum(minNum,maxNum){
     switch(arguments.length){
          case 1:
               return parseInt(Math.random()*minNum+1,10);
          case 2:
               return parseInt(Math.random()*(maxNum-minNum+1)+minNum,10);
          default:
               return 0;
     }
}

/**
 * Query time interval
 * @param periodTime
 * @param periodType
 */
function getTimeInter(periodTime, periodType) {
     if("day" == periodType) {
          return (1000 * 60 * 60 * 24) * parseInt(periodTime);
     }else if("hour" == periodType) {
          return (1000 * 60 * 60) * parseInt(periodTime);
     }else {
          return (1000 * 60) * parseInt(periodTime);
     }
}

/**
 * ERatio entry signal record: called each time a position is opened
 * @direction "BUY"-Long; "SELL": Short
 * @param kPeriod The candlestick period used for ATR calculation at market entry
 *        atrPeriodThe time range selected for ATR calculation at market entry
 *        kPeriod = PERIOD_D1; atrPeriod = 20 Represents calculating the average volatility for each of the past 20 days
 * @private
 */
function _Enter_Market_Record(ex, price, direction, kPeriod, atrPeriod) {
     // CalculationATR
     var records = ex.GetRecords(kPeriod);
     var atr = _ATR(records, atrPeriod);

     var now = new Date().getTime();
     var enterMarketRecord = {"enterId" : randomNum(1000000, 9999999), "date" : now, "dateStr": _D(now), "price" : price, "direction" : direction, "atr" : atr};
     Log("market entry point:" + JSON.stringify(enterMarketRecord));

     var enterMarketRecords = _G("enterMarketRecords");
     if(enterMarketRecords == null) {
          enterMarketRecords = new Array();
     }
     enterMarketRecords.push(enterMarketRecord);

     _G("enterMarketRecords", enterMarketRecords);
}

/**
 * ERatio calculation:
 * @param periodTime=1;periodType=day Indicates calculation of the E ratio 1 day after entering the market
 *        periodTime=1;periodType=hour Represents calculating the E ratio 1 hour after entering the market
 *        periodTime=1;periodType=min Represents calculating the E ratio 1 minute after entering the market
 * @private
 */
function _E(periodTime, periodType, ex) {
     var enterMarketRecords = _G("enterMarketRecords");

     if (enterMarketRecords != null && enterMarketRecords.length > 0) {

          var ticker = ex.GetTicker();
          var currPrice = parseFloat(ticker.Last);

          //Calculate the time interval for the set period
          var timeInter = getTimeInter(periodTime, periodType);
          // Current time node
          var now = new Date().getTime();

          // Record the highest and lowest points for a period of time after each entry point at every moment (viaKThe time range obtained by the line has an error)
          for (var i=0; i<enterMarketRecords.length; i++) {
               var enterMarketRec = enterMarketRecords[i];
               var inter = now - parseInt(enterMarketRec.date);
               if (inter < timeInter) {
                    // Record the highest and lowest points after entering the market
                    var high_low = _G((enterMarketRec.enterId+""));
                    if (high_low == null) {
                         var high = currPrice > enterMarketRec.price ? currPrice : enterMarketRec.price;
                         var low = currPrice < enterMarketRec.price ? currPrice : enterMarketRec.price;

                         high_low = {"highest" : high, "lowest" : low};
                         _G((enterMarketRec.enterId+""), high_low);
                    } else {
                         var high = currPrice > high_low.highest ? currPrice : high_low.highest;
                         var low = currPrice < high_low.lowest ? currPrice : high_low.lowest;

                         high_low = {"highest" : high, "lowest" : low};
                         _G((enterMarketRec.enterId+""), high_low);
                    }
                    //Log("high_low" + JSON.stringify(high_low));
               }
          }

          // Each time, check whether the initial entry point has reached the detection time. Once reached, calculate and remove the entry point from the queue.
          var enterMarketRecord0 = enterMarketRecords[0];

          if (now - enterMarketRecord0.date >= timeInter) {
               // CalculationMAEandMFE
               var l_h = _G((enterMarketRecord0.enterId+""));

               var mae = 0;
               var mfe = 0;
               if (enterMarketRecord0.direction == 'UP') {
                    if (l_h.highest > enterMarketRecord0.price) {
                         mae = l_h.highest - enterMarketRecord0.price;
                    }
                    if (l_h.lowest < enterMarketRecord0.price) {
                         mfe = enterMarketRecord0.price - l_h.lowest;
                    }
               }
               if (enterMarketRecord0.direction == 'DOWN') {
                    if (l_h.lowest < enterMarketRecord0.price) {
                         mae = enterMarketRecord0.price - l_h.lowest;
                    }
                    if (l_h.highest > enterMarketRecord0.price) {
                         mfe = l_h.highest - enterMarketRecord0.price;
                    }
               }

               // WillMAEandMFEDivide separately by the entryATR(Adjust according to volatility and standardize different markets)
               mae = parseFloat(mae/enterMarketRecord0.atr);
               mfe = parseFloat(mfe/enterMarketRecord0.atr);

               // Calculate averageMAEandMFEand record
               var mae_avg = _G("mae_avg");
               var mfe_avg = _G("mfe_avg");

               if (mae_avg == null) {
                    mae_avg = {"mae":mae, "times":1};
               } else {
                    mae = parseFloat((mae_avg.mae + mae)/2);
                    mae_avg = {"mae":mae, "times":mae_avg.times+1};
               }
               if (mfe_avg == null) {
                    mfe_avg = {"mfe":mfe, "times":1};
               } else {
                    mfe = parseFloat((mfe_avg.mfe + mfe)/2);
                    mfe_avg = {"mfe":mfe, "times":mfe_avg.times+1};
               }

               var E_ = parseFloat(mae_avg.mae/mfe_avg.mfe);
               Log("E-Ratio=" + E_ + "Calculate latest entry point:" + JSON.stringify(enterMarketRecord0) + "After,[Total market entry points]" + mfe_avg.times + ",[Recorded high and low points]" + JSON.stringify(l_h) + "#ff0000");

               // Record calculationsMAEandMFEAnd remove this entry point from the queue
               _G("mae_avg", mae_avg);
               _G("mfe_avg", mfe_avg);
               enterMarketRecords.shift();

               // Rejoin the market entry point before recording the highest and lowest points
               _G((enterMarketRecord0.enterId+""), null);
               _G((enterMarketRecord0.enterId+""), null);
          }
     }
}

/**
 * Use Donchian channel breakout + trend filter combination to determine the market entry point, and use the tool method to calculate the E-rate
 * Here we only simply measure the market entry points when rising changes to falling and falling changes to rising. It is not a complete Tang Qian breakthrough to enter the market.
 */
function tqaTest(ex) {
     // Get past20Highest and lowest points of the day
     var records = ex.GetRecords(PERIOD_D1);
     var highest = TA.Highest(records, 20, 'High');
     var lowest = TA.Lowest(records, 20, 'Low');
     //Log("highest:" + highest + ",lowest:" + lowest);

     var ticker = ex.GetTicker();
     var currPrice = parseFloat(ticker.Last);

     var times = 0;

     if (currPrice > highest || currPrice < lowest) {
          var ma50 = TA.MA(records, 50);
          var ma300 = TA.MA(records, 300);

          var lastDirection = _G("lastDirection");

          if (currPrice > highest && ma50[ma50.length-1] > ma300[ma300.length-1]) {
               // Start long,Record entry point
               if (lastDirection == null || lastDirection == "DOWN") {
                    _Enter_Market_Record(ex, currPrice, "UP", PERIOD_D1, 20);
                    _G("lastDirection", "UP");
               }
          }
          if (currPrice < lowest && ma50[ma50.length-1] < ma300[ma300.length-1]) {
               // Start short,Record entry point
               if (lastDirection == null || lastDirection == "UP"){
                    _Enter_Market_Record(ex, currPrice, "DOWN", PERIOD_D1, 20);
                    _G("lastDirection", "DOWN");
               }
          }
     }

     //CalculationE70:after entering the market70within daysE-Ratio, should be inwhile(true)Call inside loop
     _E(70, "day", ex);

}

function main() {

     while (true) {

          tqaTest(exchanges[0]);

          Sleep(500);
     }
}
```

> Detail

https://www.fmz.com/strategy/259135

> Last Modified

2021-03-05 15:49:20
