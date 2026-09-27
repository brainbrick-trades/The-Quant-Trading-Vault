
> Name

Dynamic-Stop-Loss-Multi-Period-RSI-Trend-Following-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/bd6db7b22f0963d028.png)


#### Overview
This is a trend-following strategy based on a combination of technical indicators, primarily using RSI overbought/oversold conditions, EMA crossovers, and dynamic stop-loss for trading. The strategy employs 1.5% risk control combined with leverage to amplify returns. Its core lies in confirming trends through multiple technical indicators while using dynamic take-profit and stop-loss levels to protect capital. The strategy is specifically designed for small-account characteristics, suitable for quick and frequent trading.

#### Strategy Principles
The strategy utilizes three main technical indicators: RSI (Relative Strength Index), EMA (Exponential Moving Average), and ATR (Average True Range). Entry signals are confirmed by crossovers between short-term EMA (9-period) and long-term EMA (21-period), while requiring RSI to be within reasonable ranges (long RSI<70, short RSI>30). The strategy employs ATR-based dynamic stop-loss, with take-profit levels set at 4 times the stop-loss, allowing for profit protection while controlling risk. Each trade risks 1.5% of the account, using 2x leverage to enhance profit potential.

#### Strategy Advantages
1. Strict risk control: Fixed percentage risk management, limiting each trade risk to 1.5%
2. Dynamic stop-loss design: ATR-based dynamic stops better adapt to market volatility
3. Multiple signal confirmation: EMA crossovers filtered by RSI improve signal reliability
4. Optimized risk-reward ratio: Take-profit at 4x stop-loss favors better expected returns
5. Suitable for small accounts: Moderate leverage enhances return potential
6. High automation: All parameters adjustable for market condition optimization

#### Strategy Risks
1. Market volatility risk: Frequent stop-losses possible in volatile markets
2. Leverage risk: 2x leverage amplifies losses
3. False breakout risk: EMA crossovers may generate false signals
4. Slippage risk: Significant slippage possible in fast markets
5. Money management risk: Requires proper position sizing control

#### Strategy Optimization Directions
1. Add trend filters: Incorporate longer-period trend determination
2. Optimize entry timing: Improve entry points using volume indicators
3. Dynamic parameter adjustment: Automatically adjust ATR multipliers based on volatility
4. Introduce market sentiment indicators: Filter high-risk market environments
5. Enhanced money management: Add dynamic position sizing mechanisms

#### Summary
This is a well-designed trend-following strategy that uses multiple technical indicators to improve trading success rates. The strategy features comprehensive risk control mechanisms suitable for small accounts. However, in live trading, attention must be paid to changing market conditions, with timely parameter adjustments to adapt to different market states. It is recommended to conduct thorough backtesting before live implementation and gradually adapt to the strategy's characteristics using small positions.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-12-04 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Aggressive Scalper Strategy", overlay=true)

// Parameters
account_balance = input.float(28.37, title="Account Balance", tooltip="Update this with your balance")
risk_per_trade = input.float(0.015, title="Risk per Trade", tooltip="1.5% risk")
leverage = input.int(2, title="Leverage", minval=1)
stop_loss_percentage = input.float(0.015, title="Stop Loss Percentage", tooltip="1.5% stop loss")
take_profit_multiplier = input.float(4, title="Take Profit Multiplier", tooltip="Take Profit is 4x Stop Loss")
stop_loss_multiplier = input.float(2, title="Stop Loss Multiplier", tooltip="Dynamic Stop Loss Multiplier")

// Trade Size Calculation
position_size = account_balance * risk_per_trade / (stop_loss_percentage / leverage)
trade_qty = position_size / close // This gives you the qty in terms of contracts

// Indicators
rsiLength = input.int(14, title="RSI Length")
emaShort = input.int(9, title="Short-term EMA Length")
emaLong = input.int(21, title="Long-term EMA Length")
rsi = ta.rsi(close, rsiLength)
emaShortLine = ta.ema(close, emaShort)
emaLongLine = ta.ema(close, emaLong)

// Entry Conditions
longCondition = ta.crossover(emaShortLine, emaLongLine) and rsi < 70
shortCondition = ta.crossunder(emaShortLine, emaLongLine) and rsi > 30

// ATR for dynamic stop loss and take profit levels
atrLength = input.int(14, title="ATR Length")
atrMultiplier = input.float(1.5, title="ATR Multiplier")
atr = ta.atr(atrLength)

// Dynamic Take Profit and Stop Loss Levels
longTakeProfitLevel = close + (atr * take_profit_multiplier)
longStopLossLevel = close - (atr * stop_loss_multiplier)
shortTakeProfitLevel = close - (atr * take_profit_multiplier)
shortStopLossLevel = close + (atr * stop_loss_multiplier)

// Strategy Execution
if (longCondition)
    strategy.entry("Long", strategy.long, qty=trade_qty)
    strategy.exit("Take Profit/Stop Loss", from_entry="Long", limit=longTakeProfitLevel, stop=longStopLossLevel)

if (shortCondition)
    strategy.entry("Short", strategy.short, qty=trade_qty)
    strategy.exit("Take Profit/Stop Loss", from_entry="Short", limit=shortTakeProfitLevel, stop=shortStopLossLevel)

// Alert Conditions
alertcondition(longCondition, title="Buy Signal", message="Long position entry signal detected.")
alertcondition(shortCondition, title="Sell Signal", message="Short position entry signal detected.")

// Display Information on Chart
var table_info = table.new(position.top_right, 2, 2, frame_color=color.blue, frame_width=1)
if (bar_index == na)
    table.cell(table_info, 0, 0, text="Aggressive Scalper", bgcolor=color.blue)
    table.cell(table_info, 1, 0, text="Account Balance: $" + str.tostring(account_balance), text_color=color.white)
    table.cell(table_info, 1, 1, text="Risk per Trade: " + str.tostring(risk_per_trade * 100) + "%", text_color=color.white)
    table.cell(table_info, 0, 1, text="Leverage: " + str.tostring(leverage) + "x", text_color=color.white)

```

> Detail

https://www.fmz.com/strategy/474052

> Last Modified

2024-12-05 16:25:17
