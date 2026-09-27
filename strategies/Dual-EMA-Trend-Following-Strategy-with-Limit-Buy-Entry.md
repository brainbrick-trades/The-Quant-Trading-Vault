
> Name

Dual-EMA-Trend-Following-Strategy-with-Limit-Buy-Entry

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/124509167bb4ccdd5ac.png)


#### Overview
This strategy is a trend-following trading system based on a dual exponential moving average (EMA) framework, implementing limit buy orders at the EMA20 level. It employs a conservative money management approach, utilizing only 10% of account equity per trade and incorporating take-profit and stop-loss levels for risk management. The strategy uses two EMA periods (30 and 300 days) to determine market trends and only seeks entry opportunities during upward trending markets.

#### Strategy Principles
The core logic of the strategy is based on several key elements:
1. Uses EMA300 as a trend filter, only considering long positions when price is above EMA300, ensuring trade direction aligns with the main trend.
2. Places limit buy orders at the EMA20 level when trend conditions are met, allowing for entries at relatively lower prices during pullbacks to moving average support.
3. Implements fixed percentage-based take-profit and stop-loss levels, defaulting to 10% for profit targets and 5% for stop-losses, maintaining a risk-reward ratio greater than 2:1.
4. Employs position sizing at 10% of account equity, effectively reducing risk exposure per trade through conservative money management.

#### Strategy Advantages
1. Trend Following Characteristics: Effectively identifies and follows market trends by combining long and short-term moving averages, improving trade success rate.
2. Comprehensive Risk Control: Implements fixed stop-losses and money management rules to effectively control risk per trade.
3. Optimized Entry Prices: Uses limit orders at EMA20 to achieve better entry prices, enhancing overall returns.
4. High Automation Level: Fully systematic approach reduces emotional interference in trading decisions.
5. Rational Money Management: Uses fixed percentage of account equity for trading, enabling compound growth of capital.

#### Strategy Risks
1. Consolidation Market Risk: Strategy may experience frequent stop-losses during sideways, choppy markets leading to consecutive losses.
2. Slippage Risk: Limit orders may not fully execute or experience significant slippage during volatile market conditions.
3. Trend Reversal Risk: Despite using long-term moving average as a filter, significant losses may occur during initial trend reversals.
4. Capital Efficiency Issues: Conservative money management approach may limit profit potential during strong trending markets.

#### Strategy Optimization Directions
1. Dynamic Stop Levels: Adjust take-profit and stop-loss percentages based on market volatility to improve strategy adaptability.
2. Multiple Trend Confirmation: Add supplementary technical indicators like RSI or MACD to enhance entry signal reliability.
3. Market Environment Filtering: Incorporate volatility indicators like ATR to adjust strategy parameters or pause trading in different market conditions.
4. Money Management Optimization: Consider dynamic position sizing based on account performance, moderately increasing exposure during profitable periods.
5. Entry Mechanism Enhancement: Consider implementing a price range around EMA20 to increase execution opportunities.

#### Summary
This strategy combines a moving average system with strict risk control rules to create a relatively robust trading system. Its core strengths lie in its trend-following characteristics and comprehensive risk management mechanisms, optimizing entry prices through limit orders while maintaining conservative money management. Although the strategy may underperform in ranging markets, the suggested optimization directions can further enhance its stability and profitability. For investors seeking stable returns, this quantitative trading strategy represents a worthy consideration.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-12-09 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Limit Buy at EMA20 (Last 30 Days)", overlay=true)

// Inputs for EMAs
ema20Length = input.int(30, title="EMA 20 Length")
ema300Length = input.int(300, title="EMA 300 Length")
tpPercentage = input.float(10.0, title="Take Profit (%)", step=0.1) / 100
slPercentage = input.float(5.0, title="Stop Loss (%)", step=0.1) / 100  // Stop loss at 15%

// Calculate EMAs
ema20 = ta.ema(close, ema20Length)
ema300 = ta.ema(close, ema300Length)

// Plot EMAs
plot(ema20, color=color.blue, title="EMA 20")
plot(ema300, color=color.red, title="EMA 300")

// Limit backtesting to the last 30 days
startTime = timestamp(year(timenow), month(timenow), dayofmonth(timenow) - 30, 0, 0)
if (time < startTime)
    strategy.close_all()
    strategy.cancel_all()

// Entry Condition: Price above EMA300
longCondition = close > ema300 and time >= startTime

// Calculate position size (10% of equity)
positionSize = strategy.equity * 0.10 / ema20  // Use EMA20 as the limit price

// Place a limit buy order at EMA20
if (longCondition)
    strategy.order("Limit Buy", strategy.long, qty=positionSize, limit=ema20)

// Calculate TP and SL levels
tpPrice = ema20 * (1 + tpPercentage)
slPrice = ema20 * (1 - slPercentage)

// Set take profit and stop loss
if (strategy.position_size > 0)
    strategy.exit("Take Profit/Stop Loss", "Limit Buy", stop=slPrice, limit=tpPrice)

```

> Detail

https://www.fmz.com/strategy/474633

> Last Modified

2024-12-11 11:11:32
