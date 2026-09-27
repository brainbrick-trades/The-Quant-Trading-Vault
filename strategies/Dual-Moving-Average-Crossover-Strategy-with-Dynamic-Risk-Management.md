
> Name

Dual-Moving-Average-Crossover-Strategy-with-Dynamic-Risk-Management

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/17b7b3b5abada8902d8.png)

#### Overview
This strategy is a quantitative trading system based on dual moving average crossover signals, which identifies market trend changes through the intersection of short-term and long-term moving averages, combined with dynamic stop-loss and take-profit management for risk control. The strategy uses market orders for trading, automatically closes existing positions and opens new positions when signals are triggered, and protects capital safety by setting stop-loss and take-profit levels.

#### Strategy Principle
The strategy uses two Simple Moving Averages (SMA) of different periods as the main basis for trading signals. A long signal is generated when the short-term MA crosses above the long-term MA, and a short signal is generated when the short-term MA crosses below the long-term MA. The system checks the current position status when signals occur, closes any counter positions first, then opens new positions according to the signal direction. Each trade automatically sets stop-loss and take-profit levels based on preset percentages, achieving dynamic management of risk-reward ratios.

#### Strategy Advantages
1. Clear Signal Mechanism - Dual MA crossover is a classic technical indicator with clear and easy-to-understand signals
2. Comprehensive Risk Management - Controls risk for each trade through dynamic stop-loss and take-profit
3. High Automation Level - Fully automated execution from signal identification to position management
4. Strong Adaptability - Can adapt to different market environments through parameter adjustment
5. Simple Structure - Clear code logic, easy to maintain and optimize
6. Real-time Monitoring - Includes trade alert functionality for easy strategy execution tracking

#### Strategy Risks
1. Choppy Market Risk - May result in frequent trading losses in range-bound markets
2. Slippage Risk - Market orders may face significant slippage
3. Parameter Sensitivity - MA period selection significantly impacts strategy performance
4. False Breakout Risk - Possible quick reversals after short-term breakouts
5. Money Management Risk - Fixed percentage stops may not suit all market conditions

#### Strategy Optimization Directions
1. Add trend filters to avoid frequent trading in choppy markets
2. Incorporate volatility indicators for dynamic stop-loss and take-profit ratio adjustment
3. Add volume confirmation signals to improve trade quality
4. Optimize entry timing by considering price pullback mechanisms
5. Enhance money management system for dynamic position sizing
6. Include market sentiment indicators to improve signal reliability

#### Summary
This is a comprehensive quantitative trading strategy with clear logic. It captures trend changes through dual MA crossover and manages risk with dynamic stop-loss and take-profit levels. The strategy's strengths lie in its systematic approach and risk control, but attention must be paid to various market risks in live trading. Through continuous optimization and improvement, the strategy can maintain stable performance in different market environments. It is recommended to conduct thorough backtesting before live implementation and adjust parameters according to actual conditions.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-10-01 00:00:00
end: 2024-10-31 23:59:59
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("BTCUSD Daily Strategy - Market Orders Only", overlay=true, initial_capital=10000, currency=currency.USD)

// Configurable Inputs
stop_loss_percent = input.float(title="Stop Loss (%)", defval=1.0, minval=0.0, step=0.1)
take_profit_percent = input.float(title="Take Profit (%)", defval=2.0, minval=0.0, step=0.1)
short_ma_length = input.int(title="Short MA Length", defval=9, minval=1)
long_ma_length = input.int(title="Long MA Length", defval=21, minval=1)

// Moving Averages
short_ma = ta.sma(close, short_ma_length)
long_ma = ta.sma(close, long_ma_length)

// Plotting Moving Averages
plot(short_ma, color=color.blue, title="Short MA")
plot(long_ma, color=color.red, title="Long MA")

// Buy and Sell Signals
buy_signal = ta.crossover(short_ma, long_ma)
sell_signal = ta.crossunder(short_ma, long_ma)

// Market Buy Logic
if (buy_signal and strategy.position_size <= 0)
    // Close any existing short position
    if (strategy.position_size < 0)
        strategy.close(id="Market Sell")
    
    // Calculate Stop Loss and Take Profit Prices
    entry_price = close
    long_stop = entry_price * (1 - stop_loss_percent / 100)
    long_take_profit = entry_price * (1 + take_profit_percent / 100)

    // Enter Long Position
    strategy.entry(id="Market Buy", direction=strategy.long)
    strategy.exit(id="Exit Long", from_entry="Market Buy", stop=long_stop, limit=long_take_profit)

    // Alert for Market Buy
    alert("Market Buy Signal at price " + str.tostring(close) + ". Stop Loss: " + str.tostring(long_stop) + ", Take Profit: " + str.tostring(long_take_profit), alert.freq_once_per_bar_close)

// Market Sell Logic
if (sell_signal and strategy.position_size >= 0)
    // Close any existing long position
    if (strategy.position_size > 0)
        strategy.close(id="Market Buy")

    // Calculate Stop Loss and Take Profit Prices
    entry_price = close
    short_stop = entry_price * (1 + stop_loss_percent / 100)
    short_take_profit = entry_price * (1 - take_profit_percent / 100)

    // Enter Short Position
    strategy.entry(id="Market Sell", direction=strategy.short)
    strategy.exit(id="Exit Short", from_entry="Market Sell", stop=short_stop, limit=short_take_profit)

    // Alert for Market Sell
    alert("Market Sell Signal at price " + str.tostring(close) + ". Stop Loss: " + str.tostring(short_stop) + ", Take Profit: " + str.tostring(short_take_profit), alert.freq_once_per_bar_close)

```

> Detail

https://www.fmz.com/strategy/472246

> Last Modified

2024-11-18 15:54:16
