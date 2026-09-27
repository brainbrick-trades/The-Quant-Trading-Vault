
> Name

Dynamic-Support-Resistance-Bollinger-Bands-Multi-Indicator-Cross-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/10280d58ad2fad7a65a.png)


#### Overview
This strategy combines dynamic support/resistance levels with Bollinger Bands and EMA21 for a multi-indicator crossing trading approach. It identifies breakouts of key price levels while using technical indicator crossovers to make trading decisions. The strategy not only dynamically identifies important support/resistance levels in market structure but also confirms trading signals through the coordination of Bollinger Bands and moving averages.

#### Strategy Principles
The strategy is based on several core components:
1. Dynamic Support/Resistance Calculation: Uses pivot point method to dynamically calculate market support/resistance levels, filtering effective price zones through channel width and minimum strength requirements.
2. Bollinger Bands: Employs 20-period, 2 standard deviation Bollinger Bands to define price volatility ranges.
3. EMA21: Serves as a reference line for medium-term trend judgment.
4. Trade Signal Generation: Executes trades when price breaks through support/resistance levels while triggering Bollinger Band signals simultaneously.

#### Strategy Advantages
1. Multi-dimensional Confirmation: Improves trading signal reliability by combining multiple technical indicators.
2. Dynamic Adaptation: Support/resistance levels automatically adjust with market structure changes.
3. Risk Management: Bollinger Bands provide clear overbought/oversold boundary definitions.
4. Trend Confirmation: EMA21 helps confirm medium-term trend direction.
5. Visualization: Strategy provides clear visual feedback for analysis and optimization.

#### Strategy Risks
1. Choppy Market Risk: May generate excessive false breakout signals in sideways markets.
2. Lag Risk: Technical indicators have inherent calculation delays, potentially missing optimal entry points.
3. Parameter Sensitivity: Strategy performance is sensitive to parameter settings, requiring optimization for different market environments.
4. False Breakout Risk: Support/resistance breakouts may be false, requiring confirmation from other indicators.

#### Optimization Directions
1. Incorporate Volume Indicators: Add volume analysis for breakout confirmation to improve signal reliability.
2. Optimize Parameter Adaptation: Develop adaptive parameter adjustment mechanisms for better market environment adaptation.
3. Enhance Stop-Loss Mechanisms: Design more comprehensive stop-loss strategies to control drawdown risk.
4. Add Trend Filters: Increase trend strength assessment to avoid trading in weak trend environments.
5. Timeframe Optimization: Study different timeframe combinations to find optimal configurations.

#### Summary
This strategy builds a relatively complete trading system by combining dynamic support/resistance, Bollinger Bands, and EMA21. Its strengths lie in multi-dimensional signal confirmation and dynamic market adaptation, while facing challenges in parameter optimization and false breakout risks. Through continuous optimization and improvement of risk control mechanisms, the strategy shows promise for better performance in actual trading.




> Source (PineScript)

``` pinescript
//@version=5
strategy("Support Resistance & Bollinger & EMA21", overlay=true)

// Parámetros de S/R
prd = input.int(defval=10, title='Pivot Period', minval=4, maxval=30, group='Setup')
ppsrc = input.string(defval='High/Low', title='Source', options=['High/Low', 'Close/Open'], group='Setup')
maxnumpp = input.int(defval=20, title='Maximum Number of Pivot', minval=5, maxval=100, group='Setup')
ChannelW = input.int(defval=10, title='Maximum Channel Width %', minval=1, group='Setup')
maxnumsr = input.int(defval=5, title='Maximum Number of S/R', minval=1, maxval=10, group='Setup')
min_strength = input.int(defval=2, title='Minimum Strength', minval=1, maxval=10, group='Setup')
labelloc = input.int(defval=20, title='Label Location', group='Colors', tooltip='Positive numbers reference future bars, negative numbers reference historical bars')
linestyle = input.string(defval='Solid', title='Line Style', options=['Solid', 'Dotted', 'Dashed'], group='Colors')
linewidth = input.int(defval=2, title='Line Width', minval=2, maxval=2, group='Colors')
resistancecolor = input.color(defval=color.black, title='Resistance Color', group='Colors')
supportcolor = input.color(defval=color.black, title='Support Color', group='Colors')
showpp = input(false, title='Show Point Points')

// Parámetros de Bandas de Bollinger y EMA21
periodo_bollinger = input.int(title="Periodo de Bollinger", defval=20)
multiplicador_bollinger = input.float(title="Multiplicador de Bollinger", defval=2.0)
periodo_ema21 = input.int(title="Periodo EMA21", defval=21)

// Cálculo de las Bandas de Bollinger y EMA21
[middle, superior, inferior] = ta.bb(close, periodo_bollinger, multiplicador_bollinger)
ema21 = ta.ema(close, periodo_ema21)

// Ploteo de las Bandas de Bollinger y EMA21
plot(middle, color=color.rgb(60, 60, 60), linewidth=2, title="Media Móvil de Bollinger")
plot(superior, color=color.rgb(184, 11, 8), linewidth=2, title="Banda Superior")
plot(inferior, color=color.rgb(6, 124, 4), linewidth=2, title="Banda Inferior")
plot(ema21, color=color.rgb(6, 150, 240), linewidth=1, style=plot.style_circles, title="EMA21")

// Condiciones para señales de compra y venta
senal_compra = close <= inferior
senal_venta = close >= superior

// Mostrar señales en el gráfico
plotshape(senal_compra, title="Compra", location=location.belowbar, color=color.green, style=shape.labelup, text="BUY")
plotshape(senal_venta, title="Venta", location=location.abovebar, color=color.red, style=shape.labeldown, text="SELL")

// Código de soporte y resistencia
float src1 = ppsrc == 'High/Low' ? high : math.max(close, open)
float src2 = ppsrc == 'High/Low' ? low : math.min(close, open)
float ph = ta.pivothigh(src1, prd, prd)
float pl = ta.pivotlow(src2, prd, prd)

plotshape(ph and showpp, text='H', style=shape.labeldown, color=na, textcolor=color.new(color.red, 0), location=location.abovebar, offset=-prd)
plotshape(pl and showpp, text='L', style=shape.labelup, color=na, textcolor=color.new(color.lime, 0), location=location.belowbar, offset=-prd)

// Calcular ancho máximo del canal S/R
prdhighest = ta.highest(300)
prdlowest = ta.lowest(300)
cwidth = (prdhighest - prdlowest) * ChannelW / 100

var pivotvals = array.new_float(0)

if ph or pl
    array.unshift(pivotvals, ph ? ph : pl)
    if array.size(pivotvals) > maxnumpp  // Limitar el tamaño del array
        array.pop(pivotvals)

get_sr_vals(ind) =>
    float lo = array.get(pivotvals, ind)
    float hi = lo
    int numpp = 0
    for y = 0 to array.size(pivotvals) - 1 by 1
        float cpp = array.get(pivotvals, y)
        float wdth = cpp <= lo ? hi - cpp : cpp - lo
        if wdth <= cwidth  // Ajusta al ancho máximo del canal?
            if cpp <= hi
                lo := math.min(lo, cpp)
            else
                hi := math.max(hi, cpp)
            numpp += 1
    [hi, lo, numpp]

var sr_up_level = array.new_float(0)
var sr_dn_level = array.new_float(0)
sr_strength = array.new_float(0)

find_loc(strength) =>
    ret = array.size(sr_strength)
    for i = ret > 0 ? array.size(sr_strength) - 1 : na to 0 by 1
        if strength <= array.get(sr_strength, i)
            break
        ret := i
    ret

check_sr(hi, lo, strength) =>
    ret = true
    for i = 0 to array.size(sr_up_level) > 0 ? array.size(sr_up_level) - 1 : na by 1
        if array.get(sr_up_level, i) >= lo and array.get(sr_up_level, i) <= hi or array.get(sr_dn_level, i) >= lo and array.get(sr_dn_level, i) <= hi
            if strength >= array.get(sr_strength, i)
                array.remove(sr_strength, i)
                array.remove(sr_up_level, i)
                array.remove(sr_dn_level, i)
                ret
            else
                ret := false
            break
    ret

// var sr_lines = array.new_line(11, na)
// var sr_labels = array.new_label(11, na)

// for x = 1 to 10 by 1
//     rate = 100 * (label.get_y(array.get(sr_labels, x)) - close) / close
//     label.set_text(array.get(sr_labels, x), text=str.tostring(label.get_y(array.get(sr_labels, x))) + '(' + str.tostring(rate, '#.##') + '%)')
//     label.set_x(array.get(sr_labels, x), x=bar_index + labelloc)
//     label.set_color(array.get(sr_labels, x), color=label.get_y(array.get(sr_labels, x)) >= close ? color.red : color.lime)
//     label.set_textcolor(array.get(sr_labels, x), textcolor=label.get_y(array.get(sr_labels, x)) >= close ? color.white : color.black)
//     label.set_style(array.get(sr_labels, x), style=label.get_y(array.get(sr_labels, x)) >= close ? label.style_label_down : label.style_label_up)
//     line.set_color(array.get(sr_lines, x), color=line.get_y1(array.get(sr_lines, x)) >= close ? resistancecolor : supportcolor)

if ph or pl
    // Debido a los nuevos cálculos, eliminar niveles S/R antiguos
    array.clear(sr_up_level)
    array.clear(sr_dn_level)
    array.clear(sr_strength)
    // Encontrar zonas S/R
    for x = 0 to array.size(pivotvals) - 1 by 1
        [hi, lo, strength] = get_sr_vals(x)
        if check_sr(hi, lo, strength)
            loc = find_loc(strength)
            // Si la fuerza está en los primeros maxnumsr sr, entonces insértala en los arrays
            if loc < maxnumsr and strength >= min_strength
                array.insert(sr_strength, loc, strength)
                array.insert(sr_up_level, loc, hi)
                array.insert(sr_dn_level, loc, lo)
                // Mantener el tamaño de los arrays = 5
                if array.size(sr_strength) > maxnumsr
                    array.pop(sr_strength)
                    array.pop(sr_up_level)
                    array.pop(sr_dn_level)

    // for x = 1 to 10 by 1
    //     line.delete(array.get(sr_lines, x))
    //     label.delete(array.get(sr_labels, x))

    for x = 0 to array.size(sr_up_level) > 0 ? array.size(sr_up_level) - 1 : na by 1
        float mid = math.round_to_mintick((array.get(sr_up_level, x) + array.get(sr_dn_level, x)) / 2)
        rate = 100 * (mid - close) / close
        // array.set(sr_labels, x + 1, label.new(x=bar_index + labelloc, y=mid, text=str.tostring(mid) + '(' + str.tostring(rate, '#.##') + '%)', color=mid >= close ? color.red : color.lime, textcolor=mid >= close ? color.white : color.black, style=mid >= close ? label.style_label_down : label.style_label_up))
        // array.set(sr_lines, x + 1, line.new(x1=bar_index, y1=mid, x2=bar_index - 1, y2=mid, extend=extend.both, color=mid >= close ? resistancecolor : supportcolor, style=line.style_solid, width=2))

f_crossed_over() =>
    ret = false
    for x = 0 to array.size(sr_up_level) > 0 ? array.size(sr_up_level) - 1 : na by 1
        float mid = math.round_to_mintick((array.get(sr_up_level, x) + array.get(sr_dn_level, x)) / 2)
        if close[1] <= mid and close > mid
            ret := true
    ret

f_crossed_under() =>
    ret = false
    for x = 0 to array.size(sr_up_level) > 0 ? array.size(sr_up_level) - 1 : na by 1
        float mid = math.round_to_mintick((array.get(sr_up_level, x) + array.get(sr_dn_level, x)) / 2)
        if close[1] >= mid and close < mid
            ret := true
    ret

crossed_over = f_crossed_over()
crossed_under = f_crossed_under()
alertcondition(crossed_over, title='Resistance Broken', message='Resistance Broken')
alertcondition(crossed_under, title='Support Broken', message='Support Broken')
alertcondition(crossed_over or crossed_under, title='Support or Resistance Broken', message='Support or Resistance Broken')

// Estrategia de compra y venta basada en el cruce de niveles S/R
if (crossed_over and senal_compra)
    strategy.entry("Compra", strategy.long)

if (crossed_under and senal_venta)
    strategy.close("Compra")
```

> Detail

https://www.fmz.com/strategy/478687

> Last Modified

2025-01-17 14:24:33
