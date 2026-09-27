
> Name

blackcat-L1-MartinGale-Scalping-Strategy

> Author

Zer3192

> Strategy Description

MartinGale(The Martingale strategy is a popular money management strategy commonly used in trading. It is often used when traders seek to recover by increasing their position size after each loss. Therefore, MartinGale does not refer to a specific strategy, but a general term for a type of strategies to cover and increase positions.

In the MartinGale strategy, the trader doubles the position size after each losing trade. The idea is to eventually have a winning trade that will recover the previous losses and generate a profit.

MartinGaleThe idea behind the strategy is to exploit the law of averages. By increasing the position size after each loss, the strategy assumes that a winning trade will eventually occur, which will not only cover the previous losses but also generate profits. This may be particularly attractive for traders looking to recover quickly from losses.

However, it should be noted that there are significant risks in the MartinGale strategy. This strategy can result in huge losses if the trader goes through a sustained losing phase or lacks sufficient capital. This strategy relies on the assumption that profitable trades will occur within a certain time frame, which is dangerous because there is no guarantee that a profitable trade will occur within a specific time frame.
Traders considering implementing a MartinGale strategy should carefully evaluate their risk tolerance and be fully aware of the potential drawbacks. It is important to establish a solid risk management plan to mitigate potential losses. Additionally, traders should be aware that this strategy may not work in all market conditions and may need to be adjusted based on market fluctuations.

To summarize, the MartinGale strategy is a money management strategy that involves increasing the position size after each loss in an attempt to recover from the losing phase. While it can offer the potential for rapid recovery, there are significant risks that traders should consider carefully before implementing this trading method.

Although I don't really agree with this trading view, someone sent a private message and asked me to talk about this topic, so I wrote a simple 38-line framework for short-term purposes.MartinGale.

MartinGaleThe scalping strategy is a trading strategy that generates profits through frequent transactions. It uses moving average crossovers to generate entry and exit signals. The strategy is implemented using TradingView's Pine scripting language.

The strategy first defines input variables such as take profit and stop loss levels, as well as the trading mode (long, short, or two-way). It then sets a rule that only allows entries if the trading mode is set to "Long".

The strategy logic uses crossover signals and crossover signals of the Simple Moving Average (SMA) definition. It calculates the short-term SMA (SMA3) and the long-term SMA (SMA8) and plots them on the chart. The crossoverSignal and crossunderSignal variables are used to track the occurrence of crossover and crossover events, while the crossoverState and crossunderState variables determine the status of crossover and crossover conditions.

Strategy execution is based on current position size. If the position size is zero (no position), the strategy checks for crossover and crossover events. A long position will be entered if a crossover event occurs and the trading pattern allows long entries. The entry price, stop loss price, take profit price and stop loss price are calculated based on the current closing price and the SMA8 value. Similarly, if a crossover event occurs and the trading pattern allows a short entry, a short position will be entered and the corresponding price calculation will be performed.
If a long position exists and the current closing price reaches the take profit price or stop loss price, and a crossover event occurs, the long position will be closed. Entry Price, Stop Loss Price, Take Profit Price and Stop Loss Price will be reset to zero.

Likewise, if a short position exists and the current closing price reaches the take profit price or the stop loss price, and a crossover event occurs, the short position is closed and the price variables are reset.

This strategy also uses the plotshape function to plot entry and exit points on the chart. It shows an upward-pointing triangle for a buy entry, a downward-pointing triangle for a buy exit, a downward-pointing triangle for a sell entry, and an upward-pointing triangle for a sell exit.

Overall, the MartinGale head-shaving strategy is designed to capture small profits by taking advantage of crossovers of short-term moving averages. It enables risk management through take-profit and stop-loss levels and allows for different trading modes to suit different market conditions.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|1.03|Take Profit|
|v_input_2|0.95|Stop Loss|
|v_input_string_1|0|Trading Mode: Long|Short|BiDir|


> Source (PineScript)

``` pinescript
//@version=5
 strategy('[blackcat] L1 MartinGale Scalping Strategy', overlay=true, pyramiding = 5)
 
 // Define input variables
// martingaleMultiplier = input(2, title="Multiplier")
 takeProfit = input(1.03, title='Take Profit')
 stopLoss = input(0.95, title='Stop Loss')
 inputTradingMode = input.string(defval='Long', options=['Long', 'Short', 'BiDir'], title='Trading Mode')
 
 //The purpose of this rule is to forbid short entries, only long etries will be placed. The rule affects the following function: 'entry'.
strategy.risk.allow_entry_in(inputTradingMode == 'Long' ? strategy.direction.long : inputTradingMode == 'Short' ? strategy.direction.short : strategy.direction.all)

// Define strategy logic 
entryPrice = 0.0
stopPrice = 0.0
takeProfitPrice = 0.0
stopLossPrice = 0.0

// Define SMA crossover and crossunder signals
sma3 = ta.sma(close, 3)
sma8 = ta.sma(close, 8)
plot(sma3, color=color.yellow)
plot(sma8, color=color.fuchsia)
crossoverSignal = ta.crossover(sma3, sma8)
crossunderSignal = ta.crossunder(sma3, sma8)
crossoverState = sma3 > sma8
crossunderState = sma3 < sma8

if strategy.position_size == 0
    if crossoverState
       strategy.entry('Buy',strategy.long)
       entryPrice := close
       stopPrice := close - stopLoss * sma8[1]
       takeProfitPrice := close + takeProfit * sma8[1]
       stopLossPrice := stopPrice
       stopLossPrice
    if crossunderState
        strategy.entry('Sell', strategy.short)
        entryPrice := close
        stopPrice := close + stopLoss *  sma8[1]
        takeProfitPrice := close - takeProfit *  sma8[1]
        stopLossPrice := stopPrice
        stopLossPrice

if strategy.position_size > 0
    if (close > takeProfitPrice or close < stopLossPrice) and crossunderState
        strategy.close('Buy')
        entryPrice := 0.0
        stopPrice := 0.0
        takeProfitPrice := 0.0
        stopLossPrice := 0.0
        stopLossPrice
    else
        strategy.entry('Buy', strategy.long)
        entryPrice := close
        stopPrice := close - stopLoss *  sma8[1]
        takeProfitPrice := close + takeProfit *  sma8[1]
        stopLossPrice := stopPrice
        stopLossPrice

if strategy.position_size < 0
    if (close > takeProfitPrice or close < stopLossPrice) and crossoverState
        strategy.close('Sell')
        entryPrice := 0.0
        stopPrice := 0.0
        takeProfitPrice := 0.0
        stopLossPrice := 0.0
        stopLossPrice
    else
        strategy.entry('Sell', strategy.short)
        entryPrice := close
        stopPrice := close + stopLoss *  sma8[1]
        takeProfitPrice := close - takeProfit *  sma8[1]
        stopLossPrice := stopPrice
        stopLossPrice

// Plot entry and exit points
plotshape(strategy.position_size > 0 and crossoverSignal, 'Buy Entry', shape.triangleup, location.belowbar, color.new(color.green, 0), size=size.small)
plotshape(strategy.position_size > 0 and (close >= takeProfitPrice or close <= stopLossPrice), 'Buy Exit', shape.triangledown, location.abovebar, color.new(color.red, 0), size=size.small)
plotshape(strategy.position_size < 0 and crossunderSignal, 'Sell Entry', shape.triangledown, location.abovebar, color.new(color.red, 0), size=size.small)
plotshape(strategy.position_size < 0 and (close >= takeProfitPrice or close <= stopLossPrice), 'Sell Exit', shape.triangleup, location.belowbar, color.new(color.green, 0), size=size.small)
```

> Detail

https://www.fmz.com/strategy/428756

> Last Modified

2023-11-03 17:27:45
