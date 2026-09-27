
> Name

Cover-all-contracts

> Author

小草

> Strategy Description

Close all futures positions under this trading pair.
Position closing method: Taking a long position that has been closed as an example, keep placing a sell one and then cancel it after 0.5 seconds. Continue to place a sell one until the position is completely closed. The amount of each pending order is all current positions that can be closed.

The plug-in can be started with one click on the trading terminal, free of charge, and convenient for manual trading. Detailed introduction:https://www.fmz.com/digest-topic/5051



> Source (javascript)

``` javascript

function main(){
    while(ture){
        var pos = exchange.GetPosition()
        var ticker = exchange.GetTicekr()
        if(!ticker){return 'Unable to obtainticker'}
        if(!pos || pos.length == 0 ){return 'No positions left'}
        for(var i=0;i<pos.length;i++){
            if(pos[i].Type == PD_LONG){
                exchange.SetContractType(pos[i].ContractType)
                exchange.SetDirection('closebuy')
                exchange.Sell(ticker.Buy, pos[i].Amount - pos[i].FrozenAmount)
            }
            if(pos[i].Type == PD_SHORT){
                exchange.SetContractType(pos[i].ContractType)
                exchange.SetDirection('closesell')
                exchange.Buy(ticker.Sell, pos[i].Amount - pos[i].FrozenAmount)
            }
        }
        var orders = exchange.Getorders()
        Sleep(500)
        for(var j=0;j<orders.length;j++){
            if(orders[i].Status == ORDER_STATE_PENDING){
                exchange.CancelOrder(orders[i].Id)
            }
        }
    }
}

```

> Detail

https://www.fmz.com/strategy/191363

> Last Modified

2020-04-02 09:40:01
