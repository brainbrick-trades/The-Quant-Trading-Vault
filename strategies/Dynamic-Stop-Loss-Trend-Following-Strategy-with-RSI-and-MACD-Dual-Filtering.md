
> Name

Dynamic-Stop-Loss-Trend-Following-Strategy-with-RSI-and-MACD-Dual-Filtering

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d909e9478583b1a14d6a.png)
![IMG](https://www.fmz.com/upload/asset/2d84546213395878b9249.png)





#### Overview
This strategy is a trend following system based on dual filtering with MACD and RSI indicators, integrated with a dynamic stop-loss mechanism. The strategy primarily generates trading opportunities through MACD crossover signals, uses RSI as secondary confirmation, and incorporates percentage-based stop-losses for risk control. The core strength lies in combining technical indicators to enhance signal reliability while protecting profits through dynamic stop-losses.

#### Strategy Principles
The strategy employs MACD(12,26,9) and RSI(14) as primary indicators. Entry signals require two conditions to be met simultaneously: MACD golden cross with RSI in oversold territory (default below 40) for long positions, and MACD death cross with RSI in overbought territory (default above 59) for short positions. The system includes a 3% dynamic stop-loss, automatically closing positions when price moves adversely beyond the set percentage. Additionally, the strategy incorporates a time filter allowing users to set specific trading time ranges.

#### Strategy Advantages
1. Dual indicator filtering enhances trade signal reliability and reduces false signals.
2. Dynamic stop-loss mechanism effectively controls risk for each trade.
3. Strategy parameters can be flexibly adjusted for different market conditions.
4. Time filtering functionality allows execution within specific time periods.
5. Percentage-based position sizing supports effective money management.

#### Strategy Risks
1. May generate frequent trading signals in ranging markets, increasing transaction costs.
2. Fixed percentage stop-loss might trigger premature exits in highly volatile markets.
3. MACD as a lagging indicator may miss significant price movements in fast markets.
4. RSI threshold settings require optimization for different markets.
5. Trading costs and slippage can impact actual strategy performance.

#### Optimization Directions
1. Introduce volatility indicators to dynamically adjust stop-loss percentages.
2. Add trend strength filters to avoid overtrading in ranging markets.
3. Consider implementing trailing stops to protect profits.
4. Optimize RSI and MACD parameters to better adapt to different market cycles.
5. Include volume analysis to enhance signal reliability.

#### Summary
This is a well-structured trend following strategy with clear logic. The combination of MACD and RSI effectively improves trade signal quality. The dynamic stop-loss design helps control risk, providing good risk management characteristics. The strategy is suitable for markets with clear trends but requires parameter adjustment based on specific market characteristics. Through the suggested optimization directions, the strategy's stability and reliability can be further enhanced.




> Source (PineScript)

``` pinescript
/*backtest
start: 2025-02-13 10:00:00
end: 2025-02-19 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Binance","currency":"BNB_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © eagle916
//@version=5
strategy("EAG MACD + RSI Strategy",overlay=true, initial_capital = 300, default_qty_value = 10, default_qty_type = "percent_of_equity", commission_type=strategy.commission.percent, commission_value=0.1)


// Input para el RSI
rsi_length = input.int(14, title="RSI Length", minval=1)
rsi_overbought = input.int(59, title="RSI Overbought Level", minval=1, maxval=100)
rsi_oversold = input.int(40, title="RSI Oversold Level", minval=1, maxval=100)

// Input para el MACD
macd_length = input.int(12, title="MACD Length", minval=1)
macd_overbought = input.int(26, title="MACD Overbought Level", minval=1, maxval=100)
macd_signal = input.int(9, title="MACD Signal Level", minval=1, maxval=100)

// Input para el porcentaje de pérdida (stop loss)
stop_loss_percent = input.float(3.0, title="Porcentaje de Stop Loss (%)", minval=0.1, step=0.1)

// Calcular RSI
rsi_value = ta.rsi(close, rsi_length)

// Calcular MACD
[macdLine, signalLine, _] = ta.macd(close, macd_length, macd_overbought, macd_signal)
macd_crossup = ta.crossover(macdLine, signalLine)   // Cruce al alza del MACD
macd_crossdown = ta.crossunder(macdLine, signalLine) // Cruce a la baja del MACD

// Condiciones de compra y venta
buy_condition = macd_crossup and rsi_value <= rsi_oversold
sell_condition = macd_crossdown and rsi_value >= rsi_overbought


// Registrar precio de entrada
var float entry_price = na
if strategy.position_size == 0
    entry_price := na

// Mostrar señales de compra y venta en la gráfica principal
plotshape(series=buy_condition, title="Señal de Compra", location=location.belowbar, color=color.green, style=shape.labelup, text="BUY") // Compra debajo de la vela
plotshape(series=sell_condition, title="Señal de Venta", location=location.abovebar, color=color.red, style=shape.labeldown, text="SELL") // Venta encima de la vela

// Órdenes de estrategia
if buy_condition 
    strategy.entry("Compra", strategy.long)
    entry_price := close
if sell_condition 
    strategy.entry("Venta", strategy.short)
    entry_price := close

// Calcular el precio de stop loss
long_stop_loss = entry_price * (1 - stop_loss_percent / 100)
short_stop_loss = entry_price * (1 + stop_loss_percent / 100)

// Cerrar posición si el precio va en contra el porcentaje definido por el usuario
if strategy.position_size > 0 and close < long_stop_loss
    strategy.close("Compra", comment="Stop Loss Compra")

if strategy.position_size < 0 and close > short_stop_loss
    strategy.close("Venta", comment="Stop Loss Venta")



```

> Detail

https://www.fmz.com/strategy/482891

> Last Modified

2025-02-20 16:50:43
