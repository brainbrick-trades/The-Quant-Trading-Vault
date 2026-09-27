
> Name

Intelligent-Trend-Following-Strategy-System-Based-on-Nadaraya-Watson-Kernel-Estimation-and-Moving-Average-Crossover

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d7e82ea4f002da018304.png)
![IMG](https://www.fmz.com/upload/asset/2d92fe0ff1857f4356699.png)




#### Overview
This strategy is a trend following trading system based on Nadaraya-Watson kernel estimation method and moving average crossover. The strategy uses a Gaussian kernel function to smooth price data and combines moving average crossover signals to capture market trends, achieving intelligent trend following trading. The strategy adopts percentage position management, using 10% of account equity by default for each trade.

#### Strategy Principles
The core of the strategy is the Nadaraya-Watson kernel estimation method, which uses a Gaussian kernel function for non-parametric smoothing of price data. The specific implementation includes the following steps:
1. Calculate weights using Gaussian kernel function with bandwidth parameter h set to 8.0
2. Perform weighted smoothing on past 500 price data points
3. Calculate Simple Moving Average (SMA) of smoothed data with 15-period lookback
4. Generate long signal when smoothed curve crosses above moving average
5. Generate short signal when smoothed curve crosses below moving average
6. Use position state variable to track current holdings and avoid duplicate entries

#### Strategy Advantages
1. Uses non-parametric estimation method, no assumption of data distribution needed
2. Gaussian kernel smoothing effectively reduces noise impact and improves signal quality
3. Moving average crossover validation reduces false signals
4. Position management system controls risk exposure
5. Code implementation is concise and efficient, easy to maintain and optimize
6. Clear strategy logic suitable for trading across various timeframes

#### Strategy Risks
1. Parameter sensitivity risk: choice of bandwidth h and moving average period significantly affects strategy performance
2. Lag risk: both kernel estimation and moving average have inherent lag, may miss sharp market moves
3. Choppy market risk: prone to false signals in sideways markets
4. Computational overhead: processing large historical data may affect real-time performance
5. Overfitting risk: parameter optimization may lead to overfitting historical data

#### Strategy Optimization Directions
1. Introduce adaptive bandwidth: dynamically adjust bandwidth parameter based on market volatility
2. Add market environment filtering: incorporate trend strength indicators, only enter positions in strong trend markets
3. Optimize stop-loss mechanism: design volatility-based dynamic stop-loss
4. Improve position management: adjust position size based on signal strength and market volatility
5. Introduce multi-timeframe analysis: combine trend judgment from longer timeframes

#### Summary
This strategy innovatively combines Nadaraya-Watson kernel estimation with traditional technical analysis to build a robust trend following system. Through Gaussian kernel smoothing and moving average crossover, it effectively captures market trends while controlling risk. The strategy has good scalability and optimization potential, suitable for further development and practical application. Traders are advised to conduct thorough parameter optimization and backtesting before live trading.




> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-21 00:00:00
end: 2025-02-18 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © UniCapInvest

//@version=5
strategy("Nadaraya-Watson Strategy with Moving Average Crossover", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10, max_bars_back=500)

// Girdiler
h = input.float(8.,'Bandwidth', minval = 0)
src = input(close,'Source')
lookback = input.int(15, "Moving Average Lookback", minval=1)

// Gaussian fonksiyonu
gauss(x, h) => math.exp(-(math.pow(x, 2)/(h * h * 2)))

// Nadaraya-Watson smoothed değerini hesaplama
var float smoothed = na
sum_w = 0.0
sum_xw = 0.0

for i = 0 to 499
    w = gauss(i, h)
    sum_w += w
    sum_xw += src[i] * w

smoothed := sum_w != 0 ? sum_xw / sum_w : na

// Hareketli ortalama hesaplama
ma = ta.sma(smoothed, lookback)

// Alım ve satım koşulları (kesişimlere göre)
longCondition = ta.crossover(smoothed, ma)
shortCondition = ta.crossunder(smoothed, ma)

// Pozisyon durumu
var bool inPosition = false

// Strateji giriş ve çıkış koşulları
if (longCondition and not inPosition)
    strategy.entry("Long", strategy.long)
    inPosition := true

if (shortCondition and inPosition)
    strategy.entry("Short", strategy.short)
    inPosition := false

// Plotting
plot(smoothed, color=color.blue, title="Nadaraya-Watson Smoothed")
plot(ma, color=color.red, title="Moving Average")
```

> Detail

https://www.fmz.com/strategy/482809

> Last Modified

2025-02-20 14:54:41
