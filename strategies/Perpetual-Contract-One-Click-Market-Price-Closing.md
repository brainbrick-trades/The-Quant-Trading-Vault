
> Name

Perpetual-Contract-One-Click-Market-Price-Closing

> Author

GCC

> Strategy Description

One-click to close all perpetual contract positions



> Source (javascript)

``` javascript
function main(){
        exchange.SetContractType('swap')
        exchange.SetCurrency('BNB_USDT')
        Log(exchange.GetPosition())
        acc = exchange.GetAccount()
        //Log(exchange.GetAccount().Info)
        var pos = exchange.GetAccount().Info.positions
        var positioned = false
        for(var i=0;i<pos.length;i++){
            if (pos[i].positionAmt != 0){
                positioned = true
                var symbol = pos[i].symbol.replace('USDT','_USDT')
                //var symbol = pos[i].symbol.replace('BUSD','_BUSD')
                exchange.SetCurrency(symbol)
                var amount = parseFloat(pos[i].positionAmt.replace('-',''))
                if(pos[i].positionSide == 'LONG'){
                    exchange.SetDirection('closebuy')
                    exchange.Sell(-1, amount)
                }
                if(pos[i].positionSide == 'SHORT'){
                    exchange.SetDirection('closesell')
                    exchange.Buy(-1, amount)
                }
            }
        }
        if(positioned == false){
            Log('No position')
            return ('No position')
        }
        else{
            Log('Complete position closing')
            return ('Complete position closing')
        }
}
```

> Detail

https://www.fmz.com/strategy/322449

> Last Modified

2022-03-25 10:48:05
