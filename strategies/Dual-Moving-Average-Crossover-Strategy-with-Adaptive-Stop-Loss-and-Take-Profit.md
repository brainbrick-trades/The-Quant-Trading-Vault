
> Name

Dual-Moving-Average-Crossover-Strategy-with-Adaptive-Stop-Loss-and-Take-Profit

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/be287ad2e93353686e.png)


#### Overview
This is an adaptive trading strategy based on dual moving average crossover signals. The strategy utilizes 14-period and 28-period Simple Moving Averages (SMA) to generate trading signals, combined with adjustable stop-loss and take-profit mechanisms to achieve balanced risk-reward management. The strategy employs fixed money management with an initial capital of 2000 and 200 per trade.

#### Strategy Principles
The core logic is based on the crossover relationship between two SMAs of different periods. A long signal is generated when the short-term (14-period) MA crosses above the long-term (28-period) MA, and a short signal is generated when the short-term MA crosses below the long-term MA. The strategy incorporates percentage-based stop-loss and take-profit mechanisms set at 2% and 4% respectively, allowing for automatic adjustment of exit points based on market prices.

#### Strategy Advantages
1. Clear Signals: The moving average crossover provides clear and objective signals, eliminating subjective judgment.
2. Robust Risk Control: The percentage-based stop-loss and take-profit levels automatically adjust with market prices, adapting to different market conditions.
3. Rational Money Management: The fixed allocation approach prevents risks associated with excessive leverage.
4. Good Visualization: The strategy displays trading signals and moving average trends on the chart, facilitating understanding and monitoring.
5. Flexible Parameters: Stop-loss and take-profit parameters can be adjusted according to different market conditions and personal risk preferences.

#### Strategy Risks
1. Choppy Market Risk: Frequent crossovers during sideways markets may generate false signals.
2. Slippage Risk: During high volatility periods, actual execution prices may deviate from signal prices.
3. Fixed Stop-Loss Range: Although stop-loss points adjust with price, the fixed percentage may not suit all market conditions.
4. Capital Efficiency: Fixed money allocation might lead to suboptimal capital utilization in certain scenarios.

#### Strategy Optimization Directions
1. Implement Trend Filters: Add additional trend indicators like MACD or RSI to reduce false signals.
2. Dynamic Stop-Loss Mechanism: Adjust stop-loss percentages based on market volatility for better adaptability.
3. Optimize Money Management: Introduce volatility-based position sizing to improve capital efficiency.
4. Add Time Filters: Implement trading time restrictions to avoid highly volatile periods.
5. Incorporate Drawdown Control: Set maximum drawdown limits to pause trading when specific thresholds are reached.

#### Summary
This is a well-structured and logically sound trading strategy. It captures trading opportunities through dual moving average crossovers while controlling risks with adaptive stop-loss and take-profit mechanisms. While there is room for optimization, the overall design adheres to fundamental quantitative trading principles. Through the suggested optimization directions, the strategy's stability and profitability potential can be further enhanced.




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
strategy('My Custom Strategy', overlay = true)

// Parámetros de las SMAs (Medias Móviles Simples)
sma14 = ta.sma(close, 14)
sma28 = ta.sma(close, 28)

// Stop Loss y Take Profit configurables
stop_loss_percent = input.float(2, title="Stop Loss %", minval=0.1, step=0.1)
take_profit_percent = input.float(4, title="Take Profit %", minval=0.1, step=0.1)

// Cálculo de stop loss y take profit
stop_loss = close * (1 - stop_loss_percent / 100)
take_profit = close * (1 + take_profit_percent / 100)

// Condiciones de entrada para compra (long)
longCondition = ta.crossover(sma14, sma28)
if (longCondition)
    strategy.entry('Long', strategy.long, stop=stop_loss, limit=take_profit)
plotshape(series=longCondition, color=color.new(color.blue, 0), style=shape.labelup, location=location.belowbar, text="BUY")

// Condiciones de entrada para venta (short)
shortCondition = ta.crossunder(sma14, sma28)
if (shortCondition)
    strategy.entry('Short', strategy.short, stop=stop_loss, limit=take_profit)
plotshape(series=shortCondition, color=color.new(color.red, 0), style=shape.labeldown, location=location.abovebar, text="SELL")

// Visualización de las SMAs en el gráfico
plot(sma14, color=color.blue, title="SMA 14")
plot(sma28, color=color.red, title="SMA 28")

```

> Detail

https://www.fmz.com/strategy/473135

> Last Modified

2024-11-27 15:05:02
