
> Name

Dynamic-Multi-Period-Exponential-Moving-Average-Cross-Strategy-with-Pullback-Optimization-System

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/b439ab441bbe875b53.png)


#### Overview
This strategy is a quantitative trading system based on multiple Exponential Moving Average (EMA) crossovers and pullback optimization. It utilizes five EMAs (EMA5, EMA8, EMA13, EMA21, and EMA50) to observe the crossover relationships between different period averages and the price-EMA relationships to implement staged position building and dynamic position closing. The strategy employs a capital management system that divides positions into different proportions like 20% and 40%, gradually building or reducing positions based on various market signals.

#### Strategy Principles
The core logic includes three main entry conditions and two exit conditions:
1. Entry signals: Open 20% position when EMA5 crosses above EMA8; Add 20% when EMA5 crosses above EMA13; Add 40% when EMA8 crosses above EMA21
2. Pullback optimization system: Open 20% position when price touches EMA50; Add 20% when price breaks above EMA50
3. Exit signals: Close 50% position when EMA5 crosses below EMA13; Close all positions when EMA8 crosses below EMA21
4. Risk control: Immediately clear all positions when price, EMA5, and EMA8 are all below EMA50

#### Strategy Advantages
1. Multiple confirmation mechanism: Provides more reliable trading signals through multiple EMA crossovers
2. Dynamic position management: Employs different position sizes based on signal strength for effective risk control
3. Pullback optimization design: Uses EMA50 as support for pullback entries, improving entry accuracy
4. Flexible exit mechanism: Adopts stepped position closing strategy to preserve profits while controlling drawdown
5. Comprehensive risk control: Sets clear stop-loss conditions to prevent losses from significant downtrends

#### Strategy Risks
1. EMA lag: Moving averages have inherent lag, which may cause delayed signals
2. Sideways market risk: May generate frequent false breakouts in ranging markets
3. Overtrading risk: Multiple entry conditions may lead to excessive trading
4. Execution costs: Frequent trading may result in high commission expenses
5. Systematic risk: May not exit positions quickly enough in highly volatile markets

#### Optimization Directions
1. Introduce trend filters: Add indicators like ADX to execute trades only in strong trends
2. Optimize position management: Dynamically adjust position sizes based on volatility
3. Incorporate price pattern recognition: Combine candlestick patterns to improve entry accuracy
4. Enhance profit-taking mechanism: Set dynamic take-profit levels to better secure gains
5. Add market sentiment indicators: Introduce indicators like RSI to filter market conditions

#### Summary
This strategy constructs a relatively complete trading system through multiple EMA crossovers and pullback optimization. Its strengths lie in its multiple confirmation mechanism and flexible position management, though it has inherent limitations like EMA lag. The strategy's stability and profitability can be further enhanced by introducing trend filters and other optimizations. It is suitable for trending markets, and traders need to optimize parameters based on actual market conditions.




> Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-12-25 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("EMA Strategy with Price & EMA5 & EMA8 < EMA50 Condition", overlay=true, margin_long=100, initial_capital=10000, commission_type=strategy.commission.percent, commission_value=0.1)

// ==============================
// INPUTS
// ==============================
lengthEMA5 = input.int(5, "EMA5 Length")
lengthEMA8 = input.int(8, "EMA8 Length")
lengthEMA13 = input.int(13, "EMA13 Length")
lengthEMA21 = input.int(21, "EMA21 Length")
lengthEMA50 = input.int(50, "EMA50 Length")

// Tam pozisyon boyutu (örnek: 100 birim)
full_position = 100.0 
qty20 = full_position * 0.2
qty40 = full_position * 0.4

// ==============================
// EMA HESAPLAMALARI
// ==============================
ema5 = ta.ema(close, lengthEMA5)
ema8 = ta.ema(close, lengthEMA8)
ema13 = ta.ema(close, lengthEMA13)
ema21 = ta.ema(close, lengthEMA21)
ema50 = ta.ema(close, lengthEMA50)

// ==============================
// KESİŞİMLERİ TESPİT FONKSİYONLARI
// ==============================
crossUp(src1, src2) => ta.crossover(src1, src2)
crossDown(src1, src2) => ta.crossunder(src1, src2)

// ==============================
// STRATEJİ KOŞULLARI
// ==============================

// Adım 1: EMA5, EMA8'i yukarı keserse %20'lik alım
step1_condition = crossUp(ema5, ema8)

// Adım 2: EMA5, EMA8'i yukarı kestikten sonra EMA5, EMA13'ü de yukarı keserse %20 daha alım
step2_condition = crossUp(ema5, ema13)

// Adım 3: EMA8, EMA21'i yukarı keserse %40 alım
step3_condition = crossUp(ema8, ema21)

// Çıkış koşulları:
// EMA5, EMA13'ü aşağı keserse pozisyonun %50'sini kapat.
// EMA8, EMA21'i aşağı keserse tüm pozisyonu kapat.
half_close_condition = crossDown(ema5, ema13)
full_close_condition = crossDown(ema8, ema21)

// Düşüşlerde EMA50'ye dokunma -> %20 alım
pullback_condition = low <= ema50 or close <= ema50

// Fiyat tekrar EMA50'nin üzerine çıkarsa -> %20 alım
above_ema50_condition = crossUp(close, ema50)

// Yeni ek koşul:  
// Fiyat, EMA5 ve EMA8'in herbiri EMA50'nin altındaysa tüm pozisyon kapat.
// Bu durum tam bir düşüş senaryosunu işaret eder.
all_below_condition = (close < ema50) and (ema5 < ema50) and (ema8 < ema50)

// Mevcut pozisyon büyüklüğü
pos_size = strategy.position_size

// ==============================
// POZİSYON GİRİŞLERİ
// ==============================
if (step1_condition and pos_size == 0)
    strategy.entry("Step1", strategy.long, qty=qty20)

if (step2_condition and strategy.opentrades < 2)
    strategy.entry("Step2", strategy.long, qty=qty20)

if (step3_condition and strategy.opentrades < 3)
    strategy.entry("Step3", strategy.long, qty=qty40)

// Pullback: Fiyat EMA50'ye temas ederse ve pozisyon yoksa %20 alım
if (pullback_condition and strategy.opentrades == 0)
    strategy.entry("Pullback", strategy.long, qty=qty20)

// Fiyat EMA50'nin üzerine çıkarsa ve pozisyon %100'e ulaşmamışsa %20 alım
if (above_ema50_condition and strategy.opentrades < 4)
    strategy.entry("Above50", strategy.long, qty=qty20)

// ==============================
// POZİSYON YÖNETİMİ (ÇIKIŞLAR)
// ==============================
if (all_below_condition and strategy.opentrades > 0)
    // Tüm pozisyonu kapat çünkü sert düşüş senaryosuna girildi
    strategy.close("Step3")
    strategy.close("Step2")
    strategy.close("Step1")
    strategy.close("Pullback")
    strategy.close("Above50")
else
    // Yarı kapatma (EMA5, EMA13 aşağı kesişimi)
    if (half_close_condition)
        totalTrades = strategy.opentrades
        // Öncelikle en son açılan en büyük pozisyonu kapatarak kademeli küçültme
        if (totalTrades >= 3)
            strategy.close("Step3")     // Bu 40% kapatır
        else if (totalTrades == 2)
            strategy.close("Step2")     // Bu 20% kapatır
        else if (totalTrades == 1)
            strategy.close("Step1")     // Bu da 20% kapatır (tamamen çıkar, ama basitlik için böyle)

    // Tam kapatma (EMA8, EMA21 aşağı kesişimi)
    if (full_close_condition)
        // Açık olan tüm pozisyonları kapat
        strategy.close("Step3")
        strategy.close("Step2")
        strategy.close("Step1")
        strategy.close("Pullback")
        strategy.close("Above50")

// ==============================
// GÖRSELLEŞTİRME
// ==============================
plot(ema5, "EMA5", color=color.new(color.yellow, 0))
plot(ema8, "EMA8", color=color.new(color.blue, 0))
plot(ema13, "EMA13", color=color.new(color.green, 0))
plot(ema21, "EMA21", color=color.new(color.red, 0))
plot(ema50, "EMA50", color=color.new(color.purple, 0))

```

> Detail

https://www.fmz.com/strategy/476264

> Last Modified

2024-12-27 15:29:38
