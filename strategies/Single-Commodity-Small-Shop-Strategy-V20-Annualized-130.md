
> Name

Single-Commodity-Small-Shop-Strategy-V20-Annualized-130

> Author

区班量化

> Strategy Description

According to some statistics, in terms of market trends, 80% of the time it is in a volatile trend. The grid strategy is a strategy to deal with shocks. There are many ways to implement the grid strategy, but the essence is to set a relatively stable position-adding strategy, and execute the position-adding as long as the price fluctuation meets the conditions of the strategy. Let's take an example. For example, every time the price drops by 5%, we will increase the position by 20% of the total funds. In this way, we will fully use the funds after executing up to five positions. Here we can also reduce the position by 20% of the initial capital for every 5% increase. Then we will clear the position after five times. This is the basic idea of the grid strategy.
Today, the district leader introduced a quantitative strategy, which is similar to grid trading, but based on this, some improvements have been made. In some cases, it can achieve an annualized return of 130%. The district leader named it the canteen strategy, imagining that the operator is a canteen operator. He aims at a fair price in the market. Once it is higher than the fair price, he will sell the goods. If it is lower than the fair price, he will buy the goods. In addition, he has a small book that records the last transaction price. Once the price of the product is lower than the last transaction price, he can also buy suddenly, and vice versa. In order to avoid unlimited operations, stop operations when the funds are less than 10% or more than 10%.
Describe the steps specifically:
Step 1: Observe the volatility of the commodity and find a fair price indicator, which can be a moving average (20 periods of the 30-minute line) or the Bollinger Middle Line; buy 50% of the position by default and record the transaction price;
Step two: If it is below the fair price indicator by 3%, it signals a buy; if it is above the fair price by 3%, it signals a sell; and the transaction price is recorded.;
		    If the transaction price is 5% lower than the previous transaction price, then instruct to buy; If it is 5% higher than the transaction price, then instruct to sell; And record the transaction price;
Step 3: Based on the current position, decide how to operate when receiving a buy order; the position fluctuates between 10% and 90%. If it exceeds this range, no operation will be performed, but the transaction price can be recorded; each operation only buys 20% or 10% of the position to avoid unlimited operations.
The reason why this strategy is called the single-commodity store strategy is because the store has only one product. As a future direction for improvement, we hope to increase the rotation of multiple commodities and even back-to-back short hedging.
Let's run a backtest. First, we choose ETH, which has high volatility, as this type of asset. The period is from January 1, 2019, to October 10, 2019. This interval includes both sharp rises and sharp falls.
It can be seen that the backtest effect is still good, reaching an annualized rate of 130%, and creating a transaction fee of 1,651 yuan. This result should be a strategy that both exchanges and traders are happy with.
The disadvantage is that the maximum drawdown is still a bit high, reaching about 30%. Major retracements occur during the phase of a sharp decline in the commodity. It's easy to understand when you think about it, because this strategy is anchored in trading commodities. If the price of commodities falls, you may have stocked up at a high level and haven't had time to release it to the market. As time goes by, it should be able to make up for it.
After registering on Bihu https://m.bihu.com/signup?i=1ewtKO&s=4&c=4, search for IoT blockchain to contact the author area leader.
In addition, readers need to be reminded that this strategy is also related to product selection. Try to choose commodities that are highly volatile and will appreciate in value over the long term. From another perspective, if you can adjust the parameters based on the product, then no matter how small the fluctuation is, as long as it can cover the handling fee, it shouldn't be a problem.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Interval|10|Polling interval (seconds))|
|mnum|20|30Minute line period|
|initRatio|0.5|Initial position ratio|


> Source (javascript)

``` javascript
/*backtest
start: 2019-01-01 00:00:00
end: 2019-10-10 00:00:00
period: 1d
exchanges: [{"eid":"OKEX","currency":"ETH_USDT","stocks":0}]
args: [["OpMode",1,10989],["MaxAmount",1,10989],["TradeFee",0.001,10989]]
*/
//After registering on Bihuhttps://m.bihu.com/signup?i=1ewtKO&s=4&c=4
//Search IoT blockchain to contact the author or group leader
function main() {
    var isInit = 1; //Indicates initial state
    var allAmount;
    var cashRatio;
    var initAccount = _C(exchange.GetAccount);
    var lastPrice;
    var wantRatio;
    var wantOper=0;//Expected operation,0no operation,1buy,-1sell
    Log(initAccount);
    var mhigh;
    var mlow;
    while (true) {
        var mrecords = exchange.GetRecords(PERIOD_M30);
        //High and low points within a certain period
        mhigh=TA.Highest(mrecords, mnum, 'High');
        mlow=TA.Lowest(mrecords, mnum, 'Low');
        
        var midLine = (mhigh+mlow)/2;
        var ticker = _C(exchange.GetTicker);
        var account = _C(exchange.GetAccount);
        var nowPrice=ticker.Sell;
        var obj;
        
        if (isInit == 1) {  //The initialization state is the default warehouse;     
            //Account cash multiplied by the ratio, divided by the current price, before decimals3bit
            obj = $.Buy(_N(account.Balance * initRatio / ticker.Sell, 3));
            if (obj) { //If the purchase is successful, mark the opening position
                      opAmount = obj.amount;
                      lastPrice = obj.price;
                      isInit=0; //Initialization successful
                      account = _C(exchange.GetAccount);
                      Log("Initial Position Opened:Purchase quantity", opAmount);
                      Log("Current Holdings", account.Stocks);
            }
        }else{ //Routine operation check
            if(nowPrice>midLine*1.03||nowPrice>lastPrice*1.07){
                wantOper=-1;
            }else if(nowPrice<midLine*0.97||nowPrice<lastPrice*0.93){
                wantOper=1;
            }else{
                wantOper=0;
            }
            
            if (wantOper==-1) { //Close the position after exiting the market
                lastPrice=nowPrice; //Whether you bought it or not, the price was adjusted a bit
                allAmount=account.Balance+account.Stocks*ticker.Sell; //Calculate total amount
                cashRatio=parseFloat((account.Balance/allAmount).toFixed(3));
                
                if(cashRatio>0.9){ //Cash ratio greater than 0.9, do nothing 
                    wantRatio=0;
                }else if(cashRatio>0.8){ //Cash ratio exceeds 0.8, can sell 10% of positions 
                    wantRatio=0.1;
                }else{ //In other cases, you can sell 20% of the position
                    wantRatio=0.2;
                }
                
                obj = $.Sell(_N(allAmount*wantRatio/ticker.Sell, 3)); 
                if(obj){
                    opAmount = obj.amount;
                    Log("Close position: sell quantity",opAmount);
                    nowAccount = _C(exchange.GetAccount);
                    Log("Current cash",nowAccount.Balance,"Profit",allAmount - initAccount.Balance);
                }
            }else if (wantOper==1) { //Open a buying position
                lastPrice=nowPrice; //Whether you bought it or not, the price was adjusted a bit
                allAmount=account.Balance+account.Stocks*ticker.Sell; //Calculate total amount
                cashRatio=parseFloat((account.Balance/allAmount).toFixed(3));
                //Log("Ready to Buy",cashRatio);
                if(cashRatio<0.1){ //Cash ratio is less than 0.1, and I have no money left to buy
                    wantRatio=0;
                }else if(cashRatio<0.2){ //Cash ratio exceeds 0.2, can buy 10% of positions 
                    wantRatio=0.1;
                }else{ //In other cases, you can buy 20% of the position
                    wantRatio=0.2;
                }
                
                obj = $.Buy(_N(allAmount*wantRatio/ticker.Sell, 3)); 
                if(obj){
                    opAmount = obj.amount;
                    Log("Buy: buy quantity",opAmount);
                    nowAccount = _C(exchange.GetAccount);
                    Log("Current cash",nowAccount.Balance,"Profit",allAmount - initAccount.Balance);
                }
            }
        }
        Sleep(Interval*1000);
    }
}
```

> Detail

https://www.fmz.com/strategy/170557

> Last Modified

2019-10-20 15:52:19
