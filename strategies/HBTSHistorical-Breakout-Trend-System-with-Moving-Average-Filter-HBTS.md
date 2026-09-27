
> Name

HBTSHistorical-Breakout-Trend-System-with-Moving-Average-Filter-HBTS

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1566a8474aeecdb43c4.png)


#### Overview
This strategy is a trend following system based on historical price breakouts and moving average filters. It combines multi-period price breakout signals with moving averages to identify market trends, using strict entry and exit rules to capture medium to long-term market movements. The strategy uses 55-day price breakouts for long signals, 20-day price breakouts for exits, and incorporates a 200-day moving average as a trend filter to effectively reduce false breakout risks.

#### Strategy Principles
The core logic is built on price breakouts and trend following. Specifically:
1. Entry Signal: System generates a long signal when price makes a 55-day high and closes above the 200-day moving average
2. Exit Signal: System closes positions when price breaks below the 20-day low
3. Trend Filter: Uses 200-day moving average as major trend indicator, only entering longs above the average
4. Position Management: Uses 10% of account equity for each trade
5. Moving Average Options: Supports SMA, EMA, WMA, VWMA, allowing flexibility based on market characteristics

#### Strategy Advantages
1. Clear Logic: Strategy uses classic price breakout and moving average indicators, easy to understand and execute
2. Robust Risk Control: Has clear stop-loss conditions, manages risk through moving average filters and position control
3. High Adaptability: Can be adjusted through parameters to suit different market environments
4. Strong Trend Capturing: Uses multiple timeframe price breakouts to confirm trend direction
5. High Automation: Clear strategy rules facilitate programmatic implementation

#### Strategy Risks
1. Choppy Market Risk: Prone to false breakouts during consolidation phases
2. Slippage Risk: May experience significant slippage in less liquid markets
3. Trend Reversal Risk: Potential for large drawdowns near major trend turning points
4. Parameter Sensitivity: Optimal parameters may vary significantly across different market environments
5. Money Management Risk: Fixed proportion positioning may be too risky in certain situations

#### Optimization Directions
1. Signal Confirmation: Can add volume breakout and other auxiliary indicators to filter false breakouts
2. Dynamic Stop Loss: Incorporate ATR and other volatility indicators for dynamic stop loss
3. Position Management: Dynamically adjust position size based on market volatility
4. Multi-timeframe Analysis: Add more timeframe analysis to improve signal reliability
5. Market Environment Recognition: Add trend strength indicators to judge current market conditions

#### Summary
This is a strategic system that combines classic turtle trading rules with modern technical analysis tools. It captures trends through price breakouts, confirms direction using moving averages, and controls risk with reasonable position management. The strategy logic is clear, practical, and has good scalability. While it may underperform in choppy markets, through proper parameter optimization and risk control, it can still achieve stable returns in trending markets. Traders are advised to adjust parameters based on specific market characteristics and establish comprehensive money management systems when applying to live trading.




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
strategy("Turtle Traders - Andrei", overlay=true, 
     default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// ====== Inputs ======
// Período para a máxima das compras
lookback_buy = input.int(title="Período para Máxima de Compra", defval=55, minval=1)

// Período para a mínima das vendas
lookback_sell = input.int(title="Período para Mínima de Venda", defval=20, minval=1)

// Período da Média Móvel
ma_length = input.int(title="Período da Média Móvel", defval=200, minval=1)

// Tipo de Média Móvel
ma_type = input.string(title="Tipo de Média Móvel", defval="SMA", options=["SMA", "EMA", "WMA", "VWMA"])

// ====== Cálculos ======
// Cálculo da Média Móvel baseada no tipo selecionado
ma = switch ma_type
    "SMA" => ta.sma(close, ma_length)
    "EMA" => ta.ema(close, ma_length)
    "WMA" => ta.wma(close, ma_length)
    "VWMA" => ta.vwma(close, ma_length)

// Cálculo da máxima dos últimos 'lookback_buy' candles
highest_buy = ta.highest(high, lookback_buy)

// Cálculo da mínima dos últimos 'lookback_sell' candles
lowest_sell = ta.lowest(low, lookback_sell)

// ====== Condições de Negociação ======
// Condição de entrada: fechamento acima da máxima dos últimos 'lookback_buy' candles E acima da MA
longCondition = (high == highest_buy) and (close > ma)

if (longCondition)
    strategy.entry("Comprar", strategy.long)

// Condição de saída: fechamento abaixo da mínima dos últimos 'lookback_sell' candles
exitCondition = (low == lowest_sell)

if (exitCondition)
    strategy.close("Comprar")

// ====== Plotagens ======
// Plotar a máxima de 'lookback_buy' candles
plot(highest_buy, color=color.green, title="Máxima", linewidth=2)

// Plotar a mínima de 'lookback_sell' candles
plot(lowest_sell, color=color.red, title="Mínima", linewidth=2)

// Plotar a Média Móvel
plot(ma, color=color.blue, title="Média Móvel", linewidth=2)

// ====== Sinais Visuais ======
// Sinal de entrada
plotshape(series=longCondition, location=location.belowbar, color=color.green, 
          style=shape.labelup, title="Sinal de Compra", text="")

// Sinal de saída
plotshape(series=exitCondition, location=location.abovebar, color=color.red, 
          style=shape.labeldown, title="Sinal de Venda", text="")

```

> Detail

https://www.fmz.com/strategy/474020

> Last Modified

2024-12-05 14:40:05
