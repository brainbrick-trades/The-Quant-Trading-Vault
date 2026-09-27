
> Name

Get-cryptocurrency-current-and-max-supply

> Author

小草

> Strategy Description

Use the API provided by CoinMarketCap to obtain cryptocurrency supply and circulation, which can be used to calculate total market capitalization.



> Source (javascript)

``` javascript
function GetSupply(symbol, max){
    var ids = null
    if(_G('ids')){
        ids = _G('ids')
    }else{
        ids = JSON.parse(HttpQuery('https://api.coinmarketcap.com/v2/listings/')).data
        _G('ids', ids)
    }
    var coinId = null
    for (var i=0; i<ids.length; i++){
        if(ids[i].symbol.toLowerCase() == symbol.toLowerCase() ){
            coinId = ids[i].id
            break
        }
    }
    if(coinId){
        var ticker = JSON.parse(HttpQuery('https://api.coinmarketcap.com/v2/ticker/'+ coinId + '/')).data
        return parseFloat(max == undefined ? ticker.total_supply: ticker.max_supply)
    }else{
        throw 'symbol not found'
    }
}
function main() {
    Log(GetSupply('BTC')) // Get total current supply
    Log(GetSupply('BTC', true)) // Get max supply
}
```

> Detail

https://www.fmz.com/strategy/122370

> Last Modified

2019-07-03 16:33:08
