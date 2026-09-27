
> Name

Enhanced-Fibonacci-Trend-Following-and-Risk-Management-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/650da325313918bd30.png)


#### Overview
This strategy is a comprehensive trading system that combines Fibonacci retracement, trend following, and risk management. It primarily uses the 0.65 Fibonacci retracement level as a key price reference point, incorporates moving averages for trend confirmation, and integrates dynamic stop-loss and take-profit mechanisms based on ATR. The strategy operates on a 15-minute timeframe and aims to capture high-probability trading opportunities aligned with the current market trend.

#### Strategy Principles
The core logic of the strategy is based on several key components:
1. Calculates highest and lowest points over a 38-period lookback window to determine the 0.65 Fibonacci retracement level.
2. Uses a 181-period Simple Moving Average (SMA) as a trend filter to determine the overall market direction.
3. Employs a 12-period Average True Range (ATR) multiplied by 1.8 to set dynamic stop-loss and take-profit levels.
4. Generates long signals when price breaks above the 0.65 Fibonacci level during uptrends, and short signals when price breaks below this level during downtrends.

#### Strategy Advantages
1. Integrates multiple technical analysis tools for more reliable trading signals.
2. Implements dynamic stop-loss and take-profit levels that adapt to market volatility.
3. Ensures trade direction aligns with the main trend through trend filtering, improving success rate.
4. Uses percentage-based position sizing, defaulting to 5% of account equity for effective risk control.
5. Features clear logic and adjustable parameters, suitable for various market conditions.

#### Strategy Risks
1. May generate frequent false breakout signals in ranging markets, increasing trading costs.
2. The 181-period moving average might be slow to react to market changes, potentially leading to losses in rapidly reversing markets.
3. Fixed ATR multiplier may perform inconsistently across different market volatility environments.
4. Strategy relies on accurate high-low calculations, which may lead to misinterpretation with poor quality data.

#### Strategy Optimization Directions
1. Introduce volume indicators as confirmation to improve breakout signal reliability.
2. Consider implementing dynamic ATR multiplier adjustment mechanism for more adaptive stop-loss and take-profit levels.
3. Add market volatility filters to adjust or pause trading during high volatility periods.
4. Optimize trend determination mechanism by considering multiple-period moving average combinations.
5. Add trading time filters to avoid highly volatile market periods.

#### Summary
This is a well-designed medium-term trend following strategy that builds a complete trading system by combining Fibonacci theory, trend following, and risk management. The strategy's main feature is generating trading signals based on price breakouts of key levels while identifying market trends, managing risk through dynamic stop-loss and take-profit mechanisms. While there are areas for optimization, it provides a practical strategy framework with real-world application value.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-11-26 00:00:00
end: 2024-12-25 08:00:00
period: 3h
basePeriod: 3h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Refined Fibonacci Strategy - Enhanced Risk Management", overlay=true)

// Input parameters
fibonacci_lookback = input.int(38, minval=2, title="Fibonacci Lookback Period")
atr_multiplier = input.float(1.8, title="ATR Multiplier for Stop Loss and Take Profit")
sma_length = input.int(181, title="SMA Length")

// Calculating Fibonacci levels
var float high_level = na
var float low_level = na
if (ta.change(ta.highest(high, fibonacci_lookback)))
    high_level := ta.highest(high, fibonacci_lookback)
if (ta.change(ta.lowest(low, fibonacci_lookback)))
    low_level := ta.lowest(low, fibonacci_lookback)

fib_level_0_65 = high_level - ((high_level - low_level) * 0.65)

// Trend Filter using SMA
sma = ta.sma(close, sma_length)
in_uptrend = close > sma
in_downtrend = close < sma

// ATR for Risk Management
atr = ta.atr(12)
long_stop_loss = close - (atr * atr_multiplier)
long_take_profit = close + (atr * atr_multiplier)
short_stop_loss = close + (atr * atr_multiplier)
short_take_profit = close - (atr * atr_multiplier)

// Entry Conditions
buy_signal = close > fib_level_0_65 and close[1] <= fib_level_0_65 and in_uptrend
sell_signal = close < fib_level_0_65 and close[1] >= fib_level_0_65 and in_downtrend

// Execute Trades
if (buy_signal)
    strategy.entry("Buy", strategy.long)
if (sell_signal)
    strategy.entry("Sell", strategy.short)

// Exit Conditions
if (strategy.position_size > 0)
    strategy.exit("Exit Long", "Buy", stop=long_stop_loss, limit=long_take_profit)
if (strategy.position_size < 0)
    strategy.exit("Exit Short", "Sell", stop=short_stop_loss, limit=short_take_profit)

// Plotting
plot(fib_level_0_65, color=color.blue, title="Fibonacci 0.65 Level")
plot(sma, color=color.orange, title="SMA")

```

> Detail

https://www.fmz.com/strategy/476243

> Last Modified

2024-12-27 14:10:14
