
> Name

Multi-Indicator-Dynamic-Moving-Average-Crossover-Quantitative-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/163d9ad87c928761362.png)


#### Overview
This strategy is a quantitative trading system based on multiple moving average crossover signals. It integrates seven different types of moving averages, including Simple Moving Average (SMA), Exponential Moving Average (EMA), Weighted Moving Average (WMA), Volume Weighted Moving Average (VWMA), Hull Moving Average (HMA), Smoothed Moving Average (RMA), and Arnaud Legoux Moving Average (ALMA). The strategy supports both two-line and three-line crossover systems and offers flexible long and short trading options.

#### Strategy Principle
The core logic of the strategy is to determine market trends by observing the crossover relationships between moving averages of different periods. A long signal is generated when the fast moving average crosses above the slow moving average, and vice versa for short signals. The system provides two entry methods: one based on direct moving average crossovers, and another based on the closing price's position relative to the moving averages. The three-line system introduces a medium-term moving average to enhance signal reliability and stability.

#### Strategy Advantages
1. High Adaptability: Integration of seven different moving averages allows the strategy to adapt to various market environments and trading instruments
2. Signal Stability: Multiple confirmation mechanisms help avoid false signals
3. Flexible Parameters: Supports customizable period settings for optimization and backtesting
4. Risk Control: Includes short-selling mechanism for capturing bilateral trading opportunities
5. Clear Visualization: Strategy provides intuitive graphical interface with visual aids like trend area filling

#### Strategy Risks
1. Lag Effect: Moving averages are inherently lagging indicators, potentially missing optimal entry points in volatile markets
2. Poor Performance in Ranging Markets: May generate frequent false signals in sideways markets
3. Parameter Dependency: Performance varies significantly with different parameter combinations, requiring continuous optimization
4. Systematic Risk: May not respond quickly enough to sudden market events for stop-loss

#### Strategy Optimization Directions
1. Incorporate Volatility Indicators: Suggest integrating ATR or similar indicators for dynamic position sizing
2. Add Market Environment Filters: Can include trend strength indicators to filter out signals in ranging markets
3. Optimize Stop-Loss Mechanism: Recommend adding trailing stop-loss functionality to improve risk control
4. Enhanced Volume Analysis: Suggest incorporating volume changes to confirm trend validity

#### Summary
This strategy is a comprehensive trend-following system that provides a reliable quantitative trading framework through the integration of multiple moving average indicators and flexible parameter settings. While it has some inherent lag, the strategy maintains practical value through proper parameter optimization and risk control measures. Traders are advised to optimize the strategy based on specific market characteristics in live trading.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2025-01-04 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Cruce de Medias Total", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=100,max_bars_back=1000)

// Parámetros de entrada
periodo_rapida = input.int(50, title="Periodos para media rápida", minval=1)
periodo_lenta = input.int(200, title="Periodos para media lenta", minval=1)

// Selección del tipo de media móvil
tipo_de_media = input.string(title="Elige el tipo de media móvil", defval="Simple sma", options=["Simple sma", "Exponencial ema", "Ponderada wma", "Volumen ponderada vwma", "Hull hma", "Media suavizada rma", "Media de Arnaud Legoux alma"])

// Posibilidad de estrategia con cruce de tres medias móviles
tres_medias = input.bool(false, title="Estrategia con cruce de 3 medias móviles")
periodo_media = input.int(100, title="Periodos para media media", minval=1)

// Opción de operar en corto
permitir_corto = input.bool(false, title="Permitir operaciones en corto")

// Opción de cuando comprar
cuando_comprar = input.string(title="Cuando comprar", defval="Cruce de medias", options=["Vela anterior cierra por encima de las medias", "Cruce de medias"])
// Opción de cuando vender
cuando_vender = input.string(title="Cuando vender", defval="Cruce de medias", options=["Vela anterior cierra por debajo de las medias", "Cruce de medias"])

float media_mov_rapida = na
float media_mov_media = na
float media_mov_lenta = na

// Definición de las medias móviles
if tipo_de_media == "Simple sma"
    media_mov_rapida := ta.sma(close, periodo_rapida)
    media_mov_media := ta.sma(close, periodo_media)
    media_mov_lenta := ta.sma(close, periodo_lenta)
else if tipo_de_media == "Exponencial ema"
    media_mov_rapida := ta.ema(close, periodo_rapida)
    media_mov_media := ta.ema(close, periodo_media)
    media_mov_lenta := ta.ema(close, periodo_lenta)
else if tipo_de_media == "Ponderada wma"
    media_mov_rapida := ta.wma(close, periodo_rapida)
    media_mov_media := ta.wma(close, periodo_media)
    media_mov_lenta := ta.wma(close, periodo_lenta)
else if tipo_de_media == "Volumen ponderada vwma"
    media_mov_rapida := ta.vwma(close, periodo_rapida)
    media_mov_media := ta.vwma(close, periodo_media)
    media_mov_lenta := ta.vwma(close, periodo_lenta)
else if tipo_de_media == "Hull hma"
    media_mov_rapida := ta.hma(close, periodo_rapida)
    media_mov_media := ta.hma(close, periodo_media)
    media_mov_lenta := ta.hma(close, periodo_lenta)
else if tipo_de_media == "Media suavizada rma"
    media_mov_rapida := ta.rma(close, periodo_rapida)
    media_mov_media := ta.rma(close, periodo_media)
    media_mov_lenta := ta.rma(close, periodo_lenta)
else if tipo_de_media == "Media de Arnaud Legoux alma"
    offset = input.int(0, title="Desfase para ALMA", minval=-100, maxval=100)
    sigma = input.float(6, title="Sigma para ALMA", minval=0.1, maxval=10)
    media_mov_rapida := ta.alma(close, periodo_rapida, offset, sigma)
    media_mov_media := ta.alma(close, periodo_media, offset, sigma)
    media_mov_lenta := ta.alma(close, periodo_lenta, offset, sigma)

// Graficar las medias móviles en el gráfico
plot_rapida = plot(media_mov_rapida, color=color.green, linewidth=2, title="Media Móvil Rápida")
plot_media = plot(tres_medias ? media_mov_media : na, color=color.blue, linewidth=2, title="Media Móvil Media")
plot_lenta = plot(media_mov_lenta, color=color.red, linewidth=2, title="Media Móvil Lenta")

// Rellenar el área entre las medias móviles con color condicionado
fill(plot_rapida, plot_lenta, media_mov_rapida > media_mov_lenta ? color.new(color.green, 90) : color.new(color.red, 90), title="Relleno entre Medias")

// Lógica de la estrategia para cruce de medias
comprado = strategy.position_size > 0  // Verifica si ya hay una posición abierta
vendido = strategy.position_size < 0 

if not comprado  // Solo compra si no hay una posición abierta
    if tres_medias and cuando_comprar == "Cruce de medias"
        if media_mov_rapida > media_mov_media and media_mov_media > media_mov_lenta
            strategy.entry("Largo", strategy.long)
            label.new(bar_index, low, "Largo", style=label.style_label_up, color=color.green, textcolor=color.white)
    else if not tres_medias and cuando_comprar == "Cruce de medias"
        if ta.crossover(media_mov_rapida, media_mov_lenta)
            strategy.entry("Largo", strategy.long)
            label.new(bar_index, low, "Largo", style=label.style_label_up, color=color.green, textcolor=color.white)
    else if tres_medias and cuando_comprar == "Vela anterior cierra por encima de las medias"
        if close[1] > media_mov_rapida and close[1] > media_mov_media and close[1] > media_mov_lenta
            strategy.entry("Largo", strategy.long)
            label.new(bar_index, low, "Largo", style=label.style_label_up, color=color.green, textcolor=color.white)
    else if not tres_medias and cuando_comprar == "Vela anterior cierra por encima de las medias"
        if close[1] > media_mov_rapida and close[1] > media_mov_lenta
            strategy.entry("Largo", strategy.long)
            label.new(bar_index, low, "Largo", style=label.style_label_up, color=color.green, textcolor=color.white)

// Condición de cierre de la posición
if comprado
    if tres_medias and cuando_vender == "Cruce de medias"
        if media_mov_rapida < media_mov_media and media_mov_media < media_mov_lenta
            strategy.close("Largo")
            label.new(bar_index, high, "Cierre Largo", style=label.style_label_down, color=color.red, textcolor=color.white)
    else if not tres_medias and cuando_vender == "Cruce de medias"
        if ta.crossunder(media_mov_rapida, media_mov_lenta)
            strategy.close("Largo")
            label.new(bar_index, high, "Cierre Largo", style=label.style_label_down, color=color.red, textcolor=color.white)
    else if tres_medias and cuando_vender == "Vela anterior cierra por debajo de las medias"
        if close[1] < media_mov_rapida and close[1] < media_mov_media and close[1] < media_mov_lenta
            strategy.close("Largo")
            label.new(bar_index, high, "Cierre Largo", style=label.style_label_down, color=color.red, textcolor=color.white)
    else if not tres_medias and cuando_vender == "Vela anterior cierra por debajo de las medias"
        if close[1] < media_mov_rapida and close[1] < media_mov_lenta
            strategy.close("Largo")
            label.new(bar_index, high, "Cierre Largo", style=label.style_label_down, color=color.red, textcolor=color.white)

// Condición de entrar en corto
if not vendido and permitir_corto
    if tres_medias
        if media_mov_rapida < media_mov_media and media_mov_media < media_mov_lenta
            strategy.entry("Short", strategy.short)
            label.new(bar_index, low, "Short", style=label.style_label_up, color=color.blue, textcolor=color.white)
    else
        if ta.crossunder(media_mov_rapida, media_mov_lenta)
            strategy.entry("Short", strategy.short)
            label.new(bar_index, low, "Short", style=label.style_label_up, color=color.blue, textcolor=color.white)

// Condición de cierre de posición corta
if vendido
    if tres_medias
        if media_mov_rapida > media_mov_media and media_mov_media > media_mov_lenta
            strategy.close("Short")
            label.new(bar_index, high, "Cierre Short", style=label.style_label_down, color=color.purple, textcolor=color.white)
    else
        if ta.crossover(media_mov_rapida, media_mov_lenta)
            strategy.close("Short")
            label.new(bar_index, high, "Cierre Short", style=label.style_label_down, color=color.purple, textcolor=color.white)

```

> Detail

https://www.fmz.com/strategy/477552

> Last Modified

2025-01-06 13:46:47
