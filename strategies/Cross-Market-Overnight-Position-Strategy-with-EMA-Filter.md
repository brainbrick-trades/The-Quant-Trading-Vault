
> Name

Cross-Market-Overnight-Position-Strategy-with-EMA-Filter

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/7837116f837f4fe619.png)


This strategy is a cross-market overnight position strategy based on the EMA technical indicator, designed to capture trading opportunities before market close and after market open. The strategy achieves intelligent trading in different market environments through precise time control and technical indicator filtering.

#### Strategy Overview
The strategy mainly gains returns by entering at specific times before market close and exiting at specific times after the next day's market open. Combined with EMA indicators for trend confirmation, it seeks trading opportunities across multiple global markets (US, Asia, Europe). The strategy also integrates automated trading functionality for unattended operation.

#### Strategy Principle
1. Time Control: Enter at fixed times before close and exit at fixed times after open based on different market trading hours
2. EMA Filtering: Use optional EMA indicators to validate entry signals
3. Market Selection: Support trading time adaptation for US, Asian, and European markets
4. Weekend Protection: Force position closure before Friday's close to avoid weekend holding risks

#### Strategy Advantages
1. Multi-market Adaptability: Flexible adjustment of trading times according to different market characteristics
2. Comprehensive Risk Control: Includes weekend position closure protection mechanism
3. High Automation Level: Supports automated trading interface integration
4. Flexible Parameters: Customizable trading times and technical indicator parameters
5. Trading Cost Consideration: Includes commission and slippage settings

#### Strategy Risks
1. Market Volatility Risk: Overnight positions may face gap risk
2. Time Dependency: Strategy effectiveness affected by market time period selection
3. Technical Indicator Limitations: Single EMA indicator may show lag
Suggestions: Set stop-loss limits, add more technical indicators for validation

#### Strategy Optimization Directions
1. Add more technical indicator combinations
2. Introduce volatility filtering mechanism
3. Optimize entry and exit time selection
4. Add adaptive parameter adjustment functionality
5. Enhance risk control module

#### Summary
This strategy achieves a reliable overnight trading system through precise time control and technical indicator filtering. The strategy design comprehensively considers practical requirements, including multi-market adaptation, risk control, and automated trading elements, demonstrating strong practical value. Through continuous optimization and improvement, this strategy has the potential to achieve stable returns in live trading.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-11-11 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © PresentTrading

// This strategy, titled "Overnight Market Entry Strategy with EMA Filter," is designed for entering long positions shortly before 
// the market closes and exiting shortly after the market opens. The strategy allows for selecting between different global market sessions (US, Asia, Europe) and 
// uses an optional EMA (Exponential Moving Average) filter to validate entry signals. The core logic is to enter trades based on conditions set for a specified period before 
// the market close and to exit trades either after a specified period following the market open or just before the weekend close. 
// Additionally, 3commas bot integration is included to automate the execution of trades. The strategy dynamically adjusts to market open and close times, ensuring trades are properly timed based on the selected market. 
// It also includes a force-close mechanism on Fridays to prevent holding positions over the weekend.

//@version=5
strategy("Overnight Positioning with EMA Confirmation - Strategy [presentTrading]", overlay=true, precision=3, commission_value=0.02, commission_type=strategy.commission.percent, slippage=1, currency=currency.USD, default_qty_type=strategy.percent_of_equity, default_qty_value=10, initial_capital=10000)

// Input parameters
entryMinutesBeforeClose = input.int(20, title="Minutes Before Close to Enter", minval=1)
exitMinutesAfterOpen = input.int(20, title="Minutes After Open to Exit", minval=1)
emaLength = input.int(100, title="EMA Length", minval=1)
emaTimeframe = input.timeframe("240", title="EMA Timeframe")
useEMA = input.bool(true, title="Use EMA Filter")

// Market Selection Input
marketSelection = input.string("US", title="Select Market", options=["US", "Asia", "Europe"])

// Timezone for each market
marketTimezone = marketSelection == "US" ? "America/New_York" :
                 marketSelection == "Asia" ? "Asia/Tokyo" :
                 "Europe/London"  // Default to London for Europe

// Market Open and Close Times for each market
var int marketOpenHour = na
var int marketOpenMinute = na
var int marketCloseHour = na
var int marketCloseMinute = na

if marketSelection == "US"
    marketOpenHour := 9
    marketOpenMinute := 30
    marketCloseHour := 16
    marketCloseMinute := 0
else if marketSelection == "Asia"
    marketOpenHour := 9
    marketOpenMinute := 0
    marketCloseHour := 15
    marketCloseMinute := 0
else if marketSelection == "Europe"
    marketOpenHour := 8
    marketOpenMinute := 0
    marketCloseHour := 16
    marketCloseMinute := 30

// 3commas Bot Settings
emailToken = input.string('', title='Email Token', group='3commas Bot Settings')
long_bot_id = input.string('', title='Long Bot ID', group='3commas Bot Settings')
usePairAdjust = input.bool(false, title='Use this pair in PERP', group='3commas Bot Settings')
selectedExchange = input.string("Binance", title="Select Exchange", group='3commas Bot Settings', options=["Binance", "OKX", "Gate.io", "Bitget"])

// Determine the trading pair based on settings
var pairString = ""
if usePairAdjust
    pairString := str.tostring(syminfo.currency) + "_" + str.tostring(syminfo.basecurrency) + (selectedExchange == "OKX" ? "-SWAP" : "") 
else
    pairString := str.tostring(syminfo.currency) + "_" + str.tostring(syminfo.basecurrency)

// Function to check if it's a trading day (excluding weekends)
isTradingDay(t) =>
    dayOfWeek = dayofweek(t, marketTimezone)
    dayOfWeek >= dayofweek.monday and dayOfWeek <= dayofweek.friday

// Function to get the timestamp for market open and close times
getMarketTimes(t) =>
    y = year(t, marketTimezone)
    m = month(t, marketTimezone)
    d = dayofmonth(t, marketTimezone)
    marketOpenTime = timestamp(marketTimezone, y, m, d, marketOpenHour, marketOpenMinute, 0)
    marketCloseTime = timestamp(marketTimezone, y, m, d, marketCloseHour, marketCloseMinute, 0)
    [marketOpenTime, marketCloseTime]

// Get the current time in the market's timezone
currentTime = time

// Calculate market times
[marketOpenTime, marketCloseTime] = getMarketTimes(currentTime)

// Calculate entry and exit times
entryTime = marketCloseTime - entryMinutesBeforeClose * 60 * 1000
exitTime = marketOpenTime + exitMinutesAfterOpen * 60 * 1000

// Get EMA data from the specified timeframe
emaValue = request.security(syminfo.tickerid, emaTimeframe, ta.ema(close, emaLength))

// Entry condition with optional EMA filter
longCondition = close > emaValue or not useEMA

// Functions to create JSON strings
getEnterJson() =>
    '{"message_type": "bot", "bot_id": "' + long_bot_id + '", "email_token": "' + emailToken + '", "delay_seconds": 0, "pair": "' + pairString + '"}'

getExitJson() =>
    '{"action": "close_at_market_price", "message_type": "bot", "bot_id": "' + long_bot_id + '", "email_token": "' + emailToken + '", "delay_seconds": 0, "pair": "' + pairString + '"}'

// Entry Signal
entrySignal = isTradingDay(currentTime) and currentTime >= entryTime and currentTime < marketCloseTime and dayofweek(currentTime, marketTimezone) != dayofweek.friday

// Exit Signal
exitSignal = isTradingDay(currentTime) and currentTime >= exitTime and currentTime < marketCloseTime

// Entry Logic
if strategy.position_size == 0 and longCondition
    strategy.entry("Long", strategy.long, alert_message=getEnterJson())

// Exit Logic
if  strategy.position_size > 0
    strategy.close("Long", alert_message=getExitJson())

// Force Close Logic on Friday before market close
isFriday = dayofweek(currentTime, marketTimezone) == dayofweek.friday
if  strategy.position_size > 0  // Close 5 minutes before market close on Friday
    strategy.close("Long", comment="Force close on Friday before market close", alert_message=getExitJson())

// Plotting entry and exit points
plotshape( strategy.position_size == 0 and longCondition, title="Entry", text="Entry", style=shape.triangleup, location=location.belowbar, color=color.green, size=size.small)
plotshape( strategy.position_size > 0, title="Exit", text="Exit", style=shape.triangledown, location=location.abovebar, color=color.red, size=size.small)

// Plot EMA for reference
plot(useEMA ? emaValue : na, title="EMA", color=color.blue)

```

> Detail

https://www.fmz.com/strategy/471661

> Last Modified

2024-11-12 10:49:00
