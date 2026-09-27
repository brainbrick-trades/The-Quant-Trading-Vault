
> Name

Simple-Bitcoin-High-Frequency-Strategy-Bot-from-2014

> Author

小草

> Strategy Description

**Introduction to strategy**

Strategy sharing address:
https://www.fmz.com/strategy/1088
This strategy has been my main strategy since I started doing virtual currency. After continuous improvement and modification, it has become a lot more complicated, but the main idea has not changed. The version I shared is the original version without obvious bugs. It is the simplest and clearest. There is no position management, every transaction is full, there is no restart after death, etc., but it is enough to explain the problem.
The strategy ran from August 2014 until the exchange charged fees at the beginning of this year. It ran pretty well during this period, with very few losses. The funds went from the initial 200 yuan to 80 bitcoins. For the specific process, you can read the series of articles in [Xiao Cao's Sina Blog](http://blog.sina.com.cn/u/2389357153) [The Road to Automated Trading of Virtual Currency](http://blog.sina.com.cn/s/blog_8e6ab2610102v6sq.html).

**Why share this strategy**

1.After the exchange charged handling fees, it almost killed all high-frequency strategies, and mine was no exception. But it may still work if you change the strategy. You can study it.
2.It's been a long time since I shared something; I've wanted to write this article for a long time.
3.Communicate and learn together with everyone.

**Principle of strategy**

The principle of this strategy is extremely simple. It can be understood as a quasi-high-frequency market-making strategy. After reading this, some of you might want to hit someone, thinking, 'You can make money with this?' Back then, almost anyone could write it. I also didn't anticipate it would be so effective. It shows that if you have an idea in mind, you should quickly put it into practice; you never know, you might get a pleasant surprise. In 2014, when Bitcoin bots were first gaining popularity, it was very easy to come up with profitable strategies.
Like all high-frequency strategies, this strategy is also based on orderbook. The following figure is the order distribution of a typical Bitcoin exchange., 
 https://dn-filebox.qbox.me/0d8ec18c831404d3d1c19e17299c78017abcfd48.png 
You can see that the left side is the buy order, showing the number of pending orders at different prices, and the right side is the sell order. It can be imagined that if a person wants to buy Bitcoin, if he does not want to wait for the order, he can only choose to take the order. If he has a lot of orders, a large number of sell orders and pending orders will be completed, which will have an impact on the price. However, this impact generally does not last forever. There are still people who want to take orders and sell, and the price is likely to recover in a very short period of time. On the other hand, it is similar to understand that someone wants to sell coins.
Take the pending order in the picture as an example. If you want to buy 5 coins directly, the price will reach 10377. At this time, if someone wants to sell 5 coins directly, the price will reach 10348. This space is the profit space. The strategy will be discussed later. If you place an order at a price lower than 10377, such as 10376.99, you will buy at a price slightly higher than 10348, such as 10348.01. If the situation just happened, you will obviously earn the price difference. Although it won't be so perfect every time, under the influence of probability, the chance of making money is actually surprisingly high.
Let's use the parameters of the current strategy to explain the specific operation. Of course, this parameter cannot be used, and it is just an explanation. It will look upwards for a price with a cumulative sell order volume of 8 coins, here is 10377, then the selling price at this time is this price minus 0.01 (the amount of subtraction can be random), similarly it will look downwards for a cumulative buy pending order volume of 8 coins, here is 10348, then the selling price at this time is 10348.01, and the buying and selling price at this time The price difference is 10376.99-10348.01=28.98, which is greater than the strategy's preset price difference of 1.5. The order will be placed at these two prices and waited for the transaction. If the price difference is less than 1.5, a price will be found to place the order. For example, the market price is plus or minus 10, and waiting for the leak (it is more appropriate to continue to search for the depth of the long position).).

**Further explanation**

1. What to do if there is no money or coins?
This situation is very common when I have less money. Most of the time I only place one side of the order, but it is not a big problem. In fact, the logic of currency balance can be added, but losses will inevitably occur in the balancing process. After all, every transaction is favored by probability. I chose to wait for the transaction on one side. Of course, this also wastes the transaction opportunity on the other side.
2. How positions are managed?
Initially, all positions are fully bought and sold, later divided into different groups based on different parameters, preventing one-time full execution.
3. Is there no stop loss??
The strategy has a complete logic of buying and selling pending orders. I don't think there is a need for stop loss (can be discussed). There is also the importance of probability. Transaction is an opportunity. Stop loss is a pity.
4. How to adjust to a coin-earning strategy?
At this time, the parameters are symmetrical, that is, cumulative sell orders for 8 coins upward and cumulative buy orders for 8 coins downward. If it is slightly unbalanced, for example, changing the upward to cumulative sell orders for 15 coins, it makes selling coins more difficult, and there is a greater chance of buying them back at a lower price, thus earning coins, and conversely making a profit. In fact, this strategy is so effective in the early stage that both coins and money increase.

**Code Explanation**

The complete code can be found in my strategy sharing at www.fmz.com. Only the core logic functions are explained here. Without any changes, the simulation disk that comes with botvs is running completely normally. This is a strategy from more than 3 years ago, and the platform still supports it to this day. It is so touching.
First is the function GetPrice() for obtaining buy and sell prices, which requires obtaining order book depth information. Note that the length of order book depth information differs across platforms, and there may be cases where even after traversing all orders, the required amount is still not obtained (this situation can occur later when many 0.01 grid orders are placed). Calling GetPrice('Buy') retrieves the buying price.
```
function GetPrice(Type) {
   //_C()Is the platform's fault-tolerant function
    var depth=_C(exchange.GetDepth);
    var amountBids=0;
    var amountAsks=0;
    //Calculate buy price, get cumulative depth to reach preset price
    if(Type=="Buy"){
       for(var i=0;i<20;i++){
           amountBids+=depth.Bids[i].Amount;
           //ParametersfloatamountbuyIs the preset cumulative depth
           if (amountBids>floatamountbuy){
               //Add a little more0.01,Makes the order ahead
              return depth.Bids[i].Price+0.01;}
        }
    }
    //Calculate the selling price in the same way
    if(Type=="Sell"){
       for(var j=0; j<20; j++){
    	   amountAsks+=depth.Asks[j].Amount;
            if (amountAsks>floatamountsell){
            return depth.Asks[j].Price-0.01;}
        }
    }
    //If the demand is still not met after traversing all depths, a price will be returned to avoidbug
    return depth.Asks[0].Price
}
```
The main function onTick() of each cycle, the cycle time set here is 3.5s. Each cycle will cancel the original order and re-register the order. The simpler it is, the less likely it will be encountered.bug.
```
function onTick() {
    var buyPrice = GetPrice("Buy");
    var sellPrice= GetPrice("Sell");
    //diffpriceis a preset spread. If the bid-ask spread is less than the preset spread, it will be set at a relatively deeper price
    if ((sellPrice - buyPrice) <= diffprice){
            buyPrice-=10;
            sellPrice+=10;}
    //Cancel all the original orders. In fact, it often happens that the new price is the same as the price of the pending order. In this case, there is no need to cancel it.
    CancelPendingOrders() 
    //Get account information and determine how much money and tokens are currently in your account
    var account=_C(exchange.GetAccount);
    //Amount of Bitcoin that can be bought,_N()Is the platform's precision function
    var amountBuy = _N((account.Balance / buyPrice-0.1),2); 
    //Amount of Bitcoin to sell, noting there is no position limit-buy and sell as much as you have because I had very little money at the time
    var amountSell = _N((account.Stocks),2); 
    if (amountSell > 0.02) {
        exchange.Sell(sellPrice,amountSell);}
    if (amountBuy > 0.02) {
        exchange.Buy(buyPrice, amountBuy);}
    //Dormant, enter the next loop
    Sleep(sleeptime);
}
```

**Tail**

The whole program only has more than 40 lines, which looks very simple, but it took me more than a week at the time, and this was still on the botvs platform. The biggest advantage is that I started early. In 2014, the market was dominated by moving bricks, and there were not many high-frequency grid and handicap grabs, which made the strategy a fish in water. Later, the competition inevitably became more and more intense, and I made more and more money. I faced many challenges and had to make major changes every once in a while to deal with it, but overall it went smoothly. When the trading platform does not charge handling fees, it is a paradise for programmed trading. Retail investors do not charge handling fees and tend to operate, which provides room for high frequency and arbitrage. All of this basically ends with the two-way handling fees of 0.1-0.2%. It is not only a problem of being charged, but also a decrease in the activity of the entire market.
But there is still a lot of room for non-high-frequency quantitative strategies.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|sleeptime|3500|Dormant Time|
|floatamountbuy|8|Buy Order Depth|
|floatamountsell|8|Sell Order Height|
|diffprice|1.5|Arbitrage Spread|


> Source (javascript)

``` javascript
/*
This is the source code I started writing for the bot, with almost no changes, and the parameters remain the original ones. There are many programs in this version
Areas that need improvement, but even so, it showed amazing profitability at the time, and when my principal was not large, it performed without leverage.
all have daily profits of around 5%. Of course, from any angle, it doesn't fit today's market.
I also posted an article in the community; everyone can take a look.
by Grass
*/

//Made a slight change and used the platform's fault tolerance function._C(),and precision function_N().
//Cancel all orders
function CancelPendingOrders() {
    var orders = _C(exchange.GetOrders);
    for (var j = 0; j < orders.length; j++) {
          exchange.CancelOrder(orders[j].Id, orders[j]);}
}

//Calculate the price to be ordered
function GetPrice(Type,depth) {
    var amountBids=0;
    var amountAsks=0;
    //Calculate buy price, get cumulative depth to reach preset price
    if(Type=="Buy"){
       for(var i=0;i<20;i++){
           amountBids+=depth.Bids[i].Amount;
           //floatamountbuyIt is the preset cumulative buy order depth
           if (amountBids>floatamountbuy){
               //Add a little more0.01,Makes the order ahead
              return depth.Bids[i].Price+0.01;}
        }
    }
    //Calculate the selling price in the same way
    if(Type=="Sell"){
       for(var j=0; j<20; j++){
    	   amountAsks+=depth.Asks[j].Amount;
            if (amountAsks>floatamountsell){
            return depth.Asks[j].Price-0.01;}
        }
    }
    //If the demand is still not met after traversing all depths, a price will be returned to avoidbug
    return depth.Asks[0].Price
}
 
function onTick() {
    var depth=_C(exchange.GetDepth);
    var buyPrice = GetPrice("Buy",depth);
    var sellPrice= GetPrice("Sell",depth);
    //If the buy-sell spread is less than the preset valuediffprice,Then it will place an order at a relatively deeper price
    if ((sellPrice - buyPrice) <= diffprice){
            buyPrice-=10;
            sellPrice+=10;}
    //Cancel all the original orders. In fact, it often happens that the new price is the same as the price of the pending order. In this case, there is no need to cancel it.
    CancelPendingOrders() 
    //Get account information and determine how much money and tokens are currently in your account
    var account=_C(exchange.GetAccount);
    //Amount of Bitcoin that can be bought
    var amountBuy = _N((account.Balance / buyPrice-0.1),2); 
    //Amount of Bitcoin to sell, noting there is no position limit-buy and sell as much as you have because I had very little money at the time
    var amountSell = _N((account.Stocks),2); 
    if (amountSell > 0.02) {
        exchange.Sell(sellPrice,amountSell);}
    if (amountBuy > 0.02) {
        exchange.Buy(buyPrice, amountBuy);}
    //Dormant, enter the next loop
    Sleep(sleeptime);
}
    
function main() {
    while (true) {
        onTick();
    }
}
```

> Detail

https://www.fmz.com/strategy/1088

> Last Modified

2019-06-06 12:30:10
