
> Name

Trading-Strategy-Based-on-Consecutive-MACD-Golden-and-Death-Crosses

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/138d87076b2183cdd38.png)


#### Overview
This strategy is based on the consecutive golden cross and death cross signals of the MACD indicator for trading. When consecutive golden cross signals appear, it opens a long position; when consecutive death cross signals appear, it opens a short position. At the same time, the strategy allows users to set take-profit and stop-loss levels to control risk. Additionally, the strategy provides the option to select the backtest time range, allowing users to evaluate the strategy's performance within a specified time period.

#### Strategy Principle
The core of this strategy is to use the golden cross and death cross signals of the MACD indicator to determine the turning points of market trends. The MACD indicator consists of a fast moving average (EMA) and a slow moving average (EMA). When the fast EMA crosses the slow EMA, it forms a golden cross or death cross signal. Consecutive golden cross signals indicate that the market may enter an upward trend, at which point a long position is opened; consecutive death cross signals indicate that the market may enter a downward trend, at which point a short position is opened. By capturing these trend turning points, the strategy attempts to profit from market trends.

#### Strategy Advantages
1. Simple and easy to understand: The strategy is based on the widely used MACD indicator, which has a simple principle and is easy to understand and implement.
2. Trend tracking: By capturing consecutive golden cross and death cross signals, the strategy can track the main trends of the market, which helps to profit from trends.
3. Risk control: The strategy allows users to set take-profit and stop-loss levels, helping to control potential risks and losses.
4. Flexible backtesting: The strategy provides the option to select the backtest time range, allowing users to evaluate the strategy's performance over different time periods as needed.

#### Strategy Risks
1. Parameter sensitivity: The performance of the MACD indicator depends on the selection of fast and slow EMA periods, and different parameter settings may lead to different trading signals.
2. Market noise: In oscillating or uncertain market conditions, the MACD indicator may generate more false signals, leading to frequent trades and potential losses.
3. Trend lag: The MACD indicator is a lagging indicator, and trading signals may appear after the trend has already been established, missing the best entry point.
4. Stop-loss risk: If the market fluctuates sharply, prices may quickly break through the stop-loss level, resulting in larger losses than expected.

#### Strategy Optimization Directions
1. Combine with other indicators: Consider combining the MACD indicator with other technical indicators (such as RSI, Bollinger Bands, etc.) to improve the reliability of signals and filter out false signals.
2. Parameter optimization: Through backtesting and optimization of different fast and slow EMA periods, find the parameter combination that best suits the specific market and asset.
3. Dynamic take-profit and stop-loss: Dynamically adjust take-profit and stop-loss levels based on market volatility or price levels to better adapt to market changes and control risk.
4. Introduce position management: Adjust the position size of each trade based on signal strength or market conditions to optimize the risk-reward ratio.

#### Summary
This strategy trades based on consecutive MACD golden cross and death cross signals, attempting to capture turning points in market trends. It is simple and easy to understand, can track main trends, and provides risk control and flexible backtesting capabilities. However, the strategy's performance may be influenced by factors such as parameter selection, market noise, and trend lag. To further improve, one can consider combining it with other indicators, optimizing parameters, introducing dynamic take-profit and stop-loss, and position management. Overall, the strategy provides a basic framework for trend trading, but in practical application, it needs to be carefully evaluated and adjusted to suit specific market conditions and personal risk preferences.


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|12|Fast EMA period|
|v_input_int_2|26|Slow EMA period|
|v_input_int_3|9|Signal line smoothing period|
|v_input_float_1|0.01|Multi order take profit setting|
|v_input_float_2|0.01|Multi order stop loss setting|
|v_input_float_3|0.01|Short order take profit setting|
|v_input_float_4|0.01|Short stop loss setting|
|v_input_bool_1|true|(?Backtest range) Enable time backtest range|
|v_input_1|timestamp(1 Jan 2023)|Start time|
|v_input_2|timestamp(1 Jan 2024)|End time|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-03-01 00:00:00
end: 2024-03-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Consecutive MACD crosses and backtest range")
//Strategy Initialization Time Settings
useDateFilter = input.bool(true, title="Enable time backtest range", group="Backtest range")
backtestStartDate = input(timestamp("1 Jan 2023"), title="Start Time")
backtestEndDate = input(timestamp("1 Jan 2024"), title="End Time")
inTradeWindow = true

// DefinitionMACDMetric parameters
fastLength = input.int(12, "Fast EMA period")
slowLength = input.int(26, "Slow EMA period")
signalSmoothing = input.int(9, "Signal line smoothing period")
long_win = input.float(defval = 0.01,title = "Multi order take profit setting", tooltip = "0.01Represent1%" )
long_lose= input.float(0.01,"Multi order stop loss setting")
short_win = input.float(0.01,"Short order take profit setting")
short_lose = input.float(0.01,"Short stop loss setting")

// CalculationMACDvalue
[macdLine, signalLine, _] = ta.macd(close, fastLength, slowLength, signalSmoothing)

// Define the conditions for a golden cross and a death cross
crossUp = ta.crossover(macdLine, signalLine)
crossDown = ta.crossunder(macdLine, signalLine)

// Use historical states to record the last crossover situation
var lastCrossUp = false
var lastCrossDown = false

// Update historical status
if crossUp
    lastCrossUp := true
else if crossDown
    lastCrossUp := false

if crossDown
    lastCrossDown := true
else if crossUp
    lastCrossDown := false

// Transaction execution logic: Check whether there are consecutive golden crosses or death crosses
if lastCrossUp and crossUp and inTradeWindow
    strategy.entry("Buy to open long", strategy.long)
    strategy.exit("Buy take profit and stop loss", "Buy to open long", limit=close * (1 + long_win), stop=close * (1 - long_lose))

if lastCrossDown and crossDown and inTradeWindow
    strategy.entry("Sell to open short", strategy.short)
    strategy.exit("Sell Take Profit Stop Loss", "Sell to open short", limit=close * (1 - short_win), stop=close * (1 + short_lose))

// DisplayMACDLine and signal line
plot(macdLine, "MACDLine", color=color.blue)
plot(signalLine, "Signal Line", color=color.orange)

```

> Detail

https://www.fmz.com/strategy/449967

> Last Modified

2024-04-30 17:26:19
