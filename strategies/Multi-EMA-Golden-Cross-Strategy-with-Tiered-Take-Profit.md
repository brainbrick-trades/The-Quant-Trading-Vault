
> Name

Multi-EMA-Golden-Cross-Strategy-with-Tiered-Take-Profit

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/15c6d44f30f5f8daac7.png)


#### Overview
This strategy is a trend-following trading system based on multiple Exponential Moving Averages (EMAs). It uses three EMAs (25, 50, and 100) to form a golden cross pattern confirming strong upward trends, and enters positions when price breaks above EMA25. The strategy employs dynamic stop-loss and tiered take-profit mechanisms for risk and profit management.

#### Strategy Principles
The core logic includes several key components:
1. Trend Confirmation: Uses three EMAs of different periods (25,50,100), forming a golden cross pattern when the shorter-term EMA is above the medium-term EMA, which is above the longer-term EMA.
2. Entry Signal: After the golden cross formation, enters long positions in two 50% batches when the closing price breaks above EMA25.
3. Stop-Loss Setting: Sets dynamic stop-loss based on the lowest price of the past 20 periods, with an additional buffer zone (0.0003) to avoid false breakouts.
4. Tiered Take-Profit: Establishes two different take-profit targets (1.0x and 1.5x), exiting the first position at the lower target and the second at the higher target.
5. Trend Protection: Triggers position closure when price falls below EMA100 to protect against trend reversals.

#### Strategy Advantages
1. Multiple Confirmation Mechanism: Effectively filters false signals through the use of multiple EMAs.
2. Dynamic Risk Management: Stop-loss levels adjust dynamically based on market volatility.
3. Tiered Position Building and Profit-Taking: Maximizes profits while securing partial gains through staged operations.
4. Trend Protection Mechanism: Uses long-term EMA as a trend reversal warning line to prevent significant drawdowns.

#### Strategy Risks
1. Lag Risk: EMA indicators have inherent lag, potentially leading to delayed entries.
2. Range-Bound Market Risk: Frequent false breakouts in sideways markets may cause consecutive losses.
3. Fixed Buffer Risk: Using a fixed stop-loss buffer may not suit all market conditions.
4. Position Sizing Risk: Fixed 50% position allocation may lack flexibility.

#### Optimization Directions
1. Dynamic Parameter Optimization: Automatically adjust EMA periods and stop-loss buffer based on market volatility.
2. Market Environment Filtering: Add trend strength and volatility indicators to adjust parameters in different market conditions.
3. Position Management Optimization: Dynamically adjust position sizes based on volatility and account equity.
4. Entry Timing Optimization: Incorporate additional technical indicators (RSI, MACD, etc.) to optimize entry timing.
5. Take-Profit Optimization: Introduce trailing stop mechanisms for better profit protection.

#### Summary
The strategy builds a comprehensive trend-following trading system through multiple EMAs and tiered operations. Its strength lies in combining key elements of trend following and risk management, though it requires parameter optimization and rule improvements based on actual market conditions. Through the suggested optimization directions, the strategy has the potential to maintain stable performance across different market environments.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-11-19 00:00:00
end: 2024-12-18 08:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("Golden Cross with Customizable TP/SL", overlay=true)

// Parameters for EMA
ema_short_length = 25
ema_mid_length = 50
ema_long_length = 100

// Parameters for stop-loss and take-profit
lookback_bars = input.int(20, title="Lookback bars for lowest low")
pip_buffer = input.float(0.0003, title="Stop-loss buffer (pips)")  // Fixed default pip value (e.g., 3 pips for 5-digit pairs)
tp_multiplier1 = input.float(1.0, title="Take-profit multiplier 1")
tp_multiplier2 = input.float(1.5, title="Take-profit multiplier 2")

// Calculate EMAs
ema25 = ta.ema(close, ema_short_length)
ema50 = ta.ema(close, ema_mid_length)
ema100 = ta.ema(close, ema_long_length)

// Golden Cross condition (EMA25 > EMA50 > EMA100)
golden_cross = ema25 > ema50 and ema50 > ema100

// Entry condition: Candle crosses above EMA25 after a golden cross
cross_above_ema25 = ta.crossover(close, ema25)
entry_condition = golden_cross and cross_above_ema25

// Stop-loss and take-profit calculation
lowest_low = ta.lowest(low, lookback_bars)
var float entry_price = na
var float stop_loss = na
var float take_profit1 = na
var float take_profit2 = na

if (entry_condition)
    entry_price := close
    stop_loss := lowest_low - pip_buffer
    take_profit1 := entry_price + (entry_price - stop_loss) * tp_multiplier1
    take_profit2 := entry_price + (entry_price - stop_loss) * tp_multiplier2
    strategy.entry("Buy1", strategy.long, qty=0.5)  // First 50%
    strategy.entry("Buy2", strategy.long, qty=0.5)  // Second 50%

// Separate exit conditions for each entry
cross_below_ema100 = ta.crossunder(close, ema100)
exit_condition1 = close >= take_profit1
exit_condition2 = close >= take_profit2
exit_condition_sl = close <= stop_loss

if (exit_condition1 or cross_below_ema100)
    strategy.close("Buy1")
if (exit_condition2 or cross_below_ema100 or exit_condition_sl)
    strategy.close("Buy2")

// Plot EMAs
plot(ema25, color=color.blue, title="EMA 25")
plot(ema50, color=color.orange, title="EMA 50")
plot(ema100, color=color.red, title="EMA 100")

```

> Detail

https://www.fmz.com/strategy/475633

> Last Modified

2024-12-20 16:54:43
