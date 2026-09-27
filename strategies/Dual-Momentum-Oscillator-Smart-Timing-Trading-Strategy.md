
> Name

Dual-Momentum-Oscillator-Smart-Timing-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/19fff97fb75cf2a2d78.png)


#### Overview
This strategy is an intelligent trading system based on dual momentum indicators: RSI and Stochastic RSI. It identifies market overbought and oversold conditions by combining signals from two momentum oscillators, capturing potential trading opportunities. The system supports period adaptation and can flexibly adjust trading cycles according to different market environments.

#### Strategy Principle
The core logic of the strategy is based on the following key elements:
1. Uses 14-period RSI indicator to calculate price momentum
2. Employs 14-period Stochastic RSI for secondary confirmation
3. Triggers buy signal when RSI is below 35 and Stochastic RSI is below 20
4. Triggers sell signal when RSI is above 70 and Stochastic RSI is above 80
5. Applies 3-period SMA smoothing to Stochastic RSI for signal stability
6. Supports switching between daily and weekly timeframes

#### Strategy Advantages
1. Dual signal confirmation mechanism significantly reduces false signal interference
2. Indicator parameters can be flexibly adjusted to market volatility
3. SMA smoothing effectively reduces signal noise
4. Supports multi-period trading to meet different investors' needs
5. Visual interface intuitively displays buy/sell signals for analysis
6. Clear code structure, easy to maintain and develop further

#### Strategy Risks
1. May generate excessive trading signals in sideways markets
2. Potential signal lag during rapid trend reversals
3. Improper parameter settings may lead to missed trading opportunities
4. False signals may occur during high market volatility
5. Requires proper stop-loss settings for risk control

#### Strategy Optimization Directions
1. Introduce trend judgment indicators like MACD or EMA to improve signal reliability
2. Add volume factors to enhance signal quality
3. Implement dynamic stop-loss mechanisms to optimize risk management
4. Develop adaptive parameter optimization system for strategy stability
5. Consider incorporating market volatility indicators to optimize trading timing

#### Summary
The strategy builds a reliable trading system by combining the advantages of RSI and Stochastic RSI. The dual signal confirmation mechanism effectively reduces false signals, while flexible parameter settings provide strong adaptability. Through continuous optimization and improvement, the strategy shows promise in maintaining stable performance across various market conditions.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-11-16 00:00:00
end: 2024-12-15 08:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("BTC Buy & Sell Strategy (RSI & Stoch RSI)", overlay=true)

// Input Parameters
rsi_length = input.int(14, title="RSI Length")
stoch_length = input.int(14, title="Stochastic Length")
stoch_smooth_k = input.int(3, title="Stochastic %K Smoothing")
stoch_smooth_d = input.int(3, title="Stochastic %D Smoothing")

// Threshold Inputs
rsi_buy_threshold = input.float(35, title="RSI Buy Threshold")
stoch_buy_threshold = input.float(20, title="Stochastic RSI Buy Threshold")
rsi_sell_threshold = input.float(70, title="RSI Sell Threshold")
stoch_sell_threshold = input.float(80, title="Stochastic RSI Sell Threshold")

use_weekly_data = input.bool(false, title="Use Weekly Data", tooltip="Enable to use weekly timeframe for calculations.")

// Timeframe Configuration
timeframe = use_weekly_data ? "W" : timeframe.period

// Calculate RSI and Stochastic RSI
rsi_value = request.security(syminfo.tickerid, timeframe, ta.rsi(close, rsi_length))
stoch_rsi_k_raw = request.security(syminfo.tickerid, timeframe, ta.stoch(close, high, low, stoch_length))
stoch_rsi_k = ta.sma(stoch_rsi_k_raw, stoch_smooth_k)
stoch_rsi_d = ta.sma(stoch_rsi_k, stoch_smooth_d)

// Define Buy and Sell Conditions
buy_signal = (rsi_value < rsi_buy_threshold) and (stoch_rsi_k < stoch_buy_threshold)
sell_signal = (rsi_value > rsi_sell_threshold) and (stoch_rsi_k > stoch_sell_threshold)

// Strategy Execution
if buy_signal
    strategy.entry("Long", strategy.long, comment="Buy Signal")

if sell_signal
    strategy.close("Long", comment="Sell Signal")

// Plot Buy and Sell Signals
plotshape(buy_signal, style=shape.labelup, location=location.belowbar, color=color.green, title="Buy Signal", size=size.small, text="BUY")
plotshape(sell_signal, style=shape.labeldown, location=location.abovebar, color=color.red, title="Sell Signal", size=size.small, text="SELL")

// Plot RSI and Stochastic RSI for Visualization
hline(rsi_buy_threshold, "RSI Buy Threshold", color=color.green)
hline(rsi_sell_threshold, "RSI Sell Threshold", color=color.red)

plot(rsi_value, color=color.blue, linewidth=2, title="RSI Value")
plot(stoch_rsi_k, color=color.purple, linewidth=2, title="Stochastic RSI K")
plot(stoch_rsi_d, color=color.orange, linewidth=1, title="Stochastic RSI D")

```

> Detail

https://www.fmz.com/strategy/475313

> Last Modified

2024-12-17 14:36:46
