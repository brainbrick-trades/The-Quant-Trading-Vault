
> Name

Time-based-Strategy-with-ATR-Take-Profit

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1036cf76fbff6016d6f.png)
 
## Overview

The main idea of this strategy is to combine time and ATR indicator to achieve automated stop loss and take profit. The strategy will open positions at fixed time points for buying or selling, and use the ATR indicator to calculate reasonable stop loss and take profit prices. This allows efficient automated trading, reduces the frequency of manual operations, and effectively controls risks through the ATR indicator.

## Strategy Principle 

This strategy uses the hour and minute variables combined with if conditions to trigger opening positions at the time point specified in the tradeTime strategy parameter. For example, setting it to 0700 means it will trigger opening positions at 7am Beijing time.

After opening positions, the strategy will use the ta.atr() function to calculate the ATR indicator value over the last 5 mins, and use this as the basis for stop loss and take profit. For example, after buying, take profit price = buy price + ATR value; after selling, take profit price = sell price - ATR value.

This achieves automated opening based on time points, and stop loss and take profit based on the ATR indicator. Thus reducing the frequency of manual operations, while effectively controlling risks.

## Advantage Analysis

This strategy has the following advantages:

1. High degree of automation. It can open positions unattended at the specified time, greatly reducing the frequency of manual operations. 

2. Stop loss and take profit based on the ATR indicator can effectively control single loss. The ATR indicator can dynamically capture market volatility to set reasonable stop loss distance.

3. Strong scalability. It is easy to combine more indicators or machine learning algorithms to assist decisions. For example, combine moving average to determine trends.

4. Easy to implement inter-commodity arbitrage. Simply set the same trading time for different products to easily implement spread trading strategies.

5. Easy to integrate into automated trading systems. Combined with scheduled task management, the strategy program can run 24 hours unattended to achieve full automation.

## Risk Analysis

This strategy also has some risks:

1. Market event risk. Major black swan events may cause extreme price fluctuations, triggering stops and larger losses. 

2. Liquidity risk. Some products have poor liquidity and cannot be fully closed at the limit take profit point.

3. ATR parameter optimization risk. ATR parameters need repeated testing and optimization, improper settings will affect strategy performance.

4. Time point optimization risk. Fixed opening time may miss market opportunities, needs adjustment based on more indicators.

## Strategy Optimization

This strategy can be further optimized in the following dimensions:

1. Combine more indicators to judge market conditions, avoid opening in unfavorable environments. Such as MACD, RSI etc.

2. Use machine learning algorithms to predict optimal time points. Collect more historical data, use LSTM etc models.  

3. Expand to inter-commodity arbitrage using platforms like Heartbeat. Find opportunities based on industry correlations.  

4. Optimize ATR parameters and stop loss/take profit settings through more backtesting.

5. Run the strategy on a server, integrate timed tasks, achieve fully automated 24x7 trading. Steady profits unattended.  

## Conclusion

This strategy integrates timing and ATR to achieve efficient automated stop loss and take profit trading. Through parameter optimization, stable alpha can be obtained. It also has great scalability and integration capabilities as a recommended quant strategy.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|700|(?Time Settings)Trade Execution Time (HHMM)|
|v_input_2|14|(?ATR Settings)ATR Length|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-12-01 00:00:00
end: 2023-12-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Time-based Strategy with ATR Take Profit Sell", overlay=true)

// Initialize take profit levels
var float takeProfitLevel = na
var float takeProfitLevelForSell = na
var float buyprice = na
var float sellprice = na



// Input for the time when the trade should be executed
tradeTime = input(0700, "Trade Execution Time (HHMM)", "Specify the time in HHMM format", group="Time Settings")

// Calculate ATR for the last 5 minutes
atrLength = input(14, "ATR Length", "Specify ATR length", group="ATR Settings")
atrValue = request.security(syminfo.tickerid, "5", ta.atr(atrLength))

// Define conditions for buy and sell
buyCondition = hour * 100 + minute == tradeTime // and strategy.position_size == 0
sellCondition = hour * 100 + minute == tradeTime // and strategy.position_size > 0
// Execute Buy and Sell orders


// if (buyCondition)
//     strategy.entry("Buy", strategy.long)
//     buyprice := close
//     takeProfitLevel := buyprice + atrValue
// strategy.exit("Take Profit BUY", from_entry="Buy", limit =takeProfitLevel) 
    

  

if (sellCondition)
    strategy.entry("Sell", strategy.short)
    sellprice := close
    takeProfitLevelForSell := sellprice -atrValue
strategy.exit("Take Profit Sell", from_entry="Sell", limit=takeProfitLevelForSell)


// Plot horizontal lines for take profit levels


plot(takeProfitLevel, color=color.green, title="Take Profit Level (Buy)")
plot(takeProfitLevelForSell, color=color.red, title="Take Profit Level (Sell)")

```

> Detail

https://www.fmz.com/strategy/440364

> Last Modified

2024-01-29 16:13:57
