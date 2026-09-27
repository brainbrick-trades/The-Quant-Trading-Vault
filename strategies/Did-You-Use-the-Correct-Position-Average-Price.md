
> Name

Did-You-Use-the-Correct-Position-Average-Price

> Author

LiteFly

> Strategy Description

Get the average holding price, most people use
position = exchanges[0].GetPosition()
avgPrice = position[0]["Price"]
But this is actually not allowed. Print the Binance contract position information.:
[map[Amount:5 ContractType:swap FrozenAmount:0 Info:map[entryPrice:55173.32071038 isAutoAddMargin:false isolatedMargin:0.00000000 isolatedWallet:0 leverage:20 liquidationPrice:0 marginType:cross markPrice:55171.20000000 maxQty:50 notionalValue:-0.00906269 positionAmt:-5 positionSide:BOTH symbol:BTCUSD_PERP unRealizedProfit:0.00000034] Margin:0.0004531349689693174 MarginLevel:20 Price:55173.32071038 Profit:3.4e-07 Type:1]]

It was found that there are two prices, entryPrice Price, and contract transactions are settled on different exchanges every day. After settlement, Price will change, and entryPrice is the real original position price.,
If you use Price to calculate the yield for take-profit and stop-loss at this time, it may result in significant losses.

For the above reasons, packaged the average position price functions of three major exchanges, take it without thanks



> Source (python)

``` python
def  getAvgPrice(position):
    if hasattr(position[0],'Info') and hasattr(position[0].Info,'cost_open'):# Huobi
        return position[0].Info.cost_open
    elif hasattr(position[0],'Info') and  hasattr(position[0].Info,'avg_cost'):#OKex
        return position[0].Info.avg_cost
    elif hasattr(position[0],'Info') and  hasattr(position[0].Info,'entryPrice'):#binance
        return position[0].Info.entryPrice
    else:
        return position[0]["Price"] 

def main():
    Log(exchange.GetAccount())
    position = exchanges[0].GetPosition()
    if len(position)>0:
        avgPrice = getAvgPrice(position)
        Log(avgPrice)
    
    

```

> Detail

https://www.fmz.com/strategy/261288

> Last Modified

2021-03-11 14:45:53
