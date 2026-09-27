
> Name

Dual-Moving-Average-Crossover-with-Trading-Window-and-Risk-Management-Strategy

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d8b78d92814175c3d674.png)
![IMG](https://www.fmz.com/upload/asset/2d8c5ee8ca7e59ad7ec21.png)


#### Overview

This strategy is a trading system based on dual moving average crossovers, combined with a specific trading time window and risk management mechanisms. The core logic utilizes the crossover relationship between a fast moving average and a slow moving average to determine changes in market trends, thereby generating buy and sell signals. The strategy also implements trade execution within fixed time periods and sets stop-loss and take-profit mechanisms to control risk. This is a complete trading system that combines technical analysis and risk management, suitable for intraday traders and short-term trend-following investors.

#### Strategy Principles

The core principle of this strategy is based on a moving average crossover system, implemented as follows:

1. **Dual Moving Average Calculation**: 
   - Fast Moving Average (Fast MA) uses a 10-period Simple Moving Average (SMA)
   - Slow Moving Average (Slow MA) uses a 25-period Simple Moving Average (SMA)

2. **Trade Signal Generation**:
   - Buy Signal (Long): Triggered when the fast moving average crosses above the slow moving average
   - Sell Signal (Short): Triggered when the fast moving average crosses below the slow moving average

3. **Trading Time Window**:
   - The strategy only executes trades during market open hours (08:30-15:00)
   - Forces closing of all positions at 15:00

4. **Risk Management Mechanism**:
   - Stop Loss: Set at entry price minus a specified number of ticks
   - Take Profit: Set at entry price plus a specified number of ticks
   - Default trading quantity set to 2 units

5. **System Logic Flow**:
   - Check if within trading time window
   - Determine if moving average crossover conditions are met
   - Execute trade entry
   - Set stop-loss and take-profit prices
   - Force position closure at market closing time

Through this systematic approach, the strategy achieves an organic combination of trend identification and risk control.

#### Strategy Advantages

Analyzing the code implementation of this strategy, the following significant advantages can be summarized:

1. **Effectiveness of Trend Following**: The dual moving average crossover is a classic trend identification method that can effectively capture medium and short-term market trend changes. The fast moving average (10-period) responds sensitively to price changes, while the slow moving average (25-period) filters out short-term market noise.

2. **Standardized Trading Time Management**: By setting a specific trading window (08:30-15:00), the strategy avoids low liquidity risks during non-primary trading sessions and focuses on trading during the most active market hours.

3. **Comprehensive Risk Control Mechanism**: The strategy incorporates built-in stop-loss and take-profit functions, with each trade having preset risk and reward targets, ensuring standardized fund management.

4. **Forced Closing Mechanism**: By forcing position closure at 15:00 daily, overnight position risks are avoided, making it particularly suitable for intraday traders who do not wish to bear overnight risks.

5. **Flexible Adjustable Parameters**: Key parameters in the strategy (moving average periods, stop-loss and take-profit ticks, trading quantity) are designed as input parameters, allowing users to adjust according to different market environments and personal risk preferences.

6. **Clear Trading Logic**: The strategy implements clear entry and exit conditions without complex decision logic, making it easy to understand and execute, reducing the possibility of operational errors.

#### Strategy Risks

Despite the relatively comprehensive design of this strategy, the following potential risks still exist:

1. **Moving Average Lag Risk**: Moving averages are inherently lagging indicators and may generate delayed signals in rapidly changing markets, leading to untimely entries or exits, especially producing frequent false signals during sideways, oscillating markets.
   - Solution: Consider adding additional filtering conditions, such as volatility indicators or trend strength indicators, to reduce false signals.

2. **Fixed Stop-Loss Risk**: The strategy uses a fixed number of ticks as stop-loss settings without considering changes in market volatility. The stop-loss might be too small in high-volatility environments and too large in low-volatility environments.
   - Solution: Introduce dynamic stop-loss mechanisms based on ATR (Average True Range) to adapt stop-loss levels to current market volatility.

3. **Time Window Limitations**: Fixed trading time windows may miss important trading opportunities outside the window, especially when significant market events occur during non-trading sessions.
   - Solution: Consider dynamically adjusting trading time windows based on different market characteristics and seasonal factors.

4. **Insufficient Fund Management**: The strategy uses a fixed trading quantity without dynamically adjusting position size based on account size and risk level.
   - Solution: Implement position size calculations based on account equity proportions, such as the Kelly criterion or fixed risk percentage methods.

5. **Lack of Market Environment Adaptability**: Dual moving average crossover strategies perform well in trending markets but may lead to frequent trading and losses in oscillating markets.
   - Solution: Add market type identification mechanisms to apply different trading parameters or pause trading in different market environments.

#### Strategy Optimization Directions

Based on code analysis and strategy characteristics, the following are several possible optimization directions:

1. **Dynamic Stop-Loss and Take-Profit Mechanism**:
   - Change fixed tick stop-loss and take-profit to dynamic values based on ATR, such as setting stop-loss at 1.5 times the current ATR and take-profit at 2.5 times the current ATR
   - This allows risk management to better adapt to changes in market volatility, with wider stop-loss positions during high volatility and tighter positions during low volatility

2. **Add Trend Filters**:
   - Introduce long-period moving averages (such as 50-period or 200-period) as trend filtering conditions, trading only in the direction of the main trend
   - Consider adding the ADX indicator to judge trend strength, executing trades only when trends are clear
   - This can reduce false signals in oscillating markets and improve signal quality

3. **Optimize Moving Average Types**:
   - Replace Simple Moving Averages (SMA) with Exponential Moving Averages (EMA) or Weighted Moving Averages (WMA), which are more sensitive to recent price changes
   - Consider using adaptive moving averages such as Kaufman's Adaptive Moving Average (KAMA) to better adapt to different market conditions
   - This can reduce signal lag and improve the timeliness of trend capture

4. **Add Trailing Stop-Loss Mechanism**:
   - Implement trailing stop functionality to automatically adjust stop-loss positions as prices move in favorable directions
   - Set to move stop-loss to breakeven or profit position after achieving a certain level of profit
   - This protects already gained profits while allowing trends to continue developing

5. **Refine Trading Time Window**:
   - Analyze performance during different time periods, potentially avoiding certain periods such as the high volatility 30 minutes before market opening
   - Consider adjusting trading times according to market seasonal characteristics, as summer and winter may have different optimal trading sessions
   - This further optimizes trade execution timing and avoids inefficient trading periods

6. **Implement Dynamic Position Management**:
   - Calculate trading size based on account equity proportions, for example, risking no more than 1-2% of the account per trade
   - Consider adjusting position size based on signal strength and market conditions, increasing trade size on more confident signals
   - This implements more professional fund management, balancing risk and reward

#### Summary

The "Dual Moving Average Crossover with Trading Window and Risk Management Strategy" is a complete trading system that combines trend following and risk management functionality. It identifies market trend changes through the crossover relationship between fast and slow moving averages, while combining specific trading time windows and stop-loss/take-profit mechanisms to achieve a systematic trading decision process.

The main advantages of this strategy lie in its clear logic, comprehensive risk control, and standardized operations. However, as a system based on moving averages, it also faces inherent risks such as signal lag and false signals. By introducing dynamic stop-loss, trend filters, optimizing moving average types, implementing trailing stops, and dynamic position management, the strategy's robustness and adaptability can be significantly enhanced.

For intraday traders and short-term trend followers, this strategy combining technical analysis and risk management provides a solid trading framework. Through continuous optimization of parameters and adaptive adjustments to market environments, this strategy has the potential to maintain relatively stable performance under different market conditions.




> Source (PineScript)

``` pinescript
/*backtest
start: 2025-02-24 00:00:00
end: 2025-02-28 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"SOL_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © szapatamejia193

//@version=5
strategy("Custom MACrossOver", overlay=true)

// Parámetros configurables
fastLength = input(10, title="Fast Period")
slowLength = input(25, title="Slow Period")
stopLossTicks = input(50, title="Stop (Ticks)")
profitTargetTicks = input(50, title="Target (Ticks)")
defaultQuantity = input(2, title="Default Quantity")

// Cálculo de medias móviles
fastMA = ta.sma(close, fastLength)
slowMA = ta.sma(close, slowLength)

// Condiciones de cruce
longCondition = ta.crossover(fastMA, slowMA)
shortCondition = ta.crossunder(fastMA, slowMA)

// Guardar precio de entrada
var float tradeEntryPrice = na

// Definir rango de mercado abierto (08:30 - 15:00)
market_open = (hour >= 8 and minute >= 30) and (hour < 15)

// Apertura de operaciones
if (market_open)
    if (longCondition)
        strategy.entry("Long", strategy.long, defaultQuantity)
        tradeEntryPrice := close
    else if (shortCondition)
        strategy.entry("Short", strategy.short, defaultQuantity)
        tradeEntryPrice := close

// Definir Stop Loss y Take Profit
if (not na(tradeEntryPrice))
    stopLossPrice = tradeEntryPrice - stopLossTicks * syminfo.mintick
    takeProfitPrice = tradeEntryPrice + profitTargetTicks * syminfo.mintick

    if (strategy.position_size > 0) // Si estamos en largo
        strategy.exit("SL/TP", from_entry="Long", stop=stopLossPrice, limit=takeProfitPrice)
    else if (strategy.position_size < 0) // Si estamos en corto
        strategy.exit("SL/TP", from_entry="Short", stop=stopLossPrice, limit=takeProfitPrice)

// Salir de todas las operaciones a las 15:00
if (hour == 15 and minute == 0)
    strategy.close_all()

// Dibujar medias móviles
plot(fastMA, title="Fast MA", color=color.blue)
plot(slowMA, title="Slow MA", color=color.red)

```

> Detail

https://www.fmz.com/strategy/484771

> Last Modified

2025-03-04 10:59:50
