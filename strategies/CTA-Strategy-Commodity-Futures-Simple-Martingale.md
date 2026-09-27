
> Name

CTA-Strategy-Commodity-Futures-Simple-Martingale

> Author

Zer3192

> Strategy Description

#### I. Summary
The Martingale strategy first originated in France in the 18th century, but at that time it was mostly used on gambling tables, and it did not take long to become well-known in Europe. In theory, this is a strategy with a winning rate close to 100%. It has been used in many trading markets until now, such as foreign exchange, futures and digital currency markets. But is it really reliable? Is it really the legendary invincible? This article demonstrates the creation of a simple Martingale strategy for commodity futures.

#### 2. Principle of Martingale strategy
Martingale is neither a trading strategy nor a trading mechanism, but a money management method. The principle is simple: every time a trader loses a certain amount, he will double the next order volume until he returns to the initial value when he makes a profit. In this way, you only need to make a profit once, not only to recover the previous losses, but also to obtain the profit from the first order amount. Obviously, this is a fund management method that doubles the position against the trend.

Now suppose there is a coin with heads and tails of equal weight, and we keep flipping the coin. The probability of getting heads or tails is approximately 50%. Next, we use this coin to gamble. The initial bet is 1 yuan; if it comes up heads, you win 1 yuan, and if it comes up tails, you lose 1 yuan. In theory, the probability of getting heads or tails is the same because each outcome is independent and unaffected by the previous results, that is50%.

According to the principle of Martin strategy, every time you lose money, adjust the bet amount to twice the last bet amount. You only need to win once to recover all previous losses. But when you lose money continuously, you will lose everything. If the principal is only 10 yuan, the first bet is 1 yuan, and the loss is 1 yuan, and the account balance is 9 yuan; the second bet is 2 yuan, and the loss is 2 yuan, and the account balance is 7 yuan; the third bet is 4 yuan, and the loss is 4 yuan, and the account balance is 3 yuan; at this time, there is not enough funds to place a bet.

#### III. Strategy backtesting
- Backtesting start date:2015-06-01
- Backtesting end date:2021-04-01
- Data product: Rapeseed Meal Index
- Data cycle: daily
- Slippage: 2 ticks for opening and closing positions

**Backtest Configuration**
 ![IMG](https://www.fmz.com/upload/asset/39df3d9ffd96e830c2f4.png) 
**Backtest Performance**
 ![IMG](https://www.fmz.com/upload/asset/3a0b9d36caf93df156c0.png) 
**Capital Curve**
 ![IMG](https://www.fmz.com/upload/asset/3992048c1b248823b8e0.png) 
**Log Information**
 ![IMG](https://www.fmz.com/upload/asset/3979363f6bf790113495.png) 

#### 4. Upgrades of Martingale strategy
The biggest risk of the Martingale strategy is that the market has always been in a unilateral trend. If the trader's position direction runs counter to the market direction, the accumulated positions will be very scary. If a trader's initial capital is 10,000 yuan and he increases his position by 2 times when he loses, he will only need to lose 7 times in a row before his position will be liquidated. But if the multiplier is changed to 1.5, the situation will be much better. It will take 12 consecutive losses before the position will be liquidated. If the multiplier is changed to 1.1, it will take 49 consecutive losses before the position will be liquidated. Because the amount of funds occupied is relatively small, the risk of operation is relatively small.

 ![IMG](https://www.fmz.com/upload/asset/390720a08054ffca4d39.png) 

The above picture is a chart of investment multiples and capital investment ratios. It can be seen that using a lower investment multiples will occupy very small funds, and the strategy will have stronger risk resistance. Therefore, in order to ensure the safety of funds, it is recommended to use low investment multiples for real offers. It is recommended to calculate the multiple investment multiples before the actual offer. It is best to have a multiple investment multiple that can withstand more than ten consecutive losses.


#### V. Conclusion
The probability of a trade is the essence of trading; no one can guarantee a 100% profit on every order. It can be said that when you place an order with an excellent reason and timing, the risk already exists. The Martingale strategy is particularly suitable for trending markets. As long as the trader can reasonably judge the trend, open positions in the direction of the trend, and set a proper risk-reward ratio, they can also achieve very steady returns.



> Source (javascript)

``` javascript
/*backtest
start: 2015-06-01 00:00:00
end: 2022-04-01 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_usdt"}]
*/

MarginLevel =20//Contract Leverage 
unit =0.015//Initial order quantity
profits =1//Profit and loss interval
bei =1//Multiplier



function main() {
    exchange.SetContractType("swap")
    exchange.SetMarginLevel(MarginLevel)
    while (true) {
        let depth = exchange.GetDepth();
        if (!depth) return;
        let ask = depth.Asks[0].Price==-1;
        let bid = depth.Bids[0].Price==-1;
        let position = exchange.GetPosition()
        if (position.length == 0) {
            let redom = Math.random()
            unit =0.015
            if (redom > 0.5) {
                exchange.SetDirection("sell")
                exchange.Sell(-1, unit, "open short")
            }
            if (redom < 0.5 ) {
                exchange.SetDirection("buy")
                exchange.Buy(-1, unit, "open long")
            }
        }
        if (position.length > 0) {
            let type = position[0].Type;
            let profit = position[0].Profit;
            let amount = position[0].Amount;
            if (type == 0) {
                if (profit > profits) {
                    exchange.SetDirection("closebuy")
                    exchange.Sell(-1, amount, "Long take profit, current profit:" + profit)
                      unit = 0.015
                }       
            
                if (profit <-profits ) {
                    unit = unit * bei
                    exchange.SetDirection("buy")
                    exchange.Buy(-1, unit, "Long add position, current profit:" + profit)
                }
            }
        
        
            if (type == 1) {
                if (profit > profits) {
                    exchange.SetDirection("closesell")
                    exchange.Buy(-1, amount, "Short take profit, current profit:" + profit)
                    unit = 0.015
            }
                    
                
                if (profit < -profits) {
                    unit = unit * bei
                    exchange.SetDirection("sell")
                    exchange.Sell(-1, unit, "Short add position, current profit:" + profit)
                }
            
              }
          } 

        Sleep(1000 )
    }
}



```

> Detail

https://www.fmz.com/strategy/275287

> Last Modified

2022-04-05 07:47:26
