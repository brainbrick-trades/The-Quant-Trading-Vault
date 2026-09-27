
> Name

KuCoin-Fund-Transfer-Plugin

> Author

makebit



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|assets|USDT|Transfer Currency|
|amount|10000|Transfer Quantity|
|typeIndex|0|Transfer Type: Transfer from Spot Account to USDT Contract Account | Transfer from USDT Contract Account to Spot Account|


> Source (javascript)

``` javascript
var adress = ['/api/v1/transfer-in','/api/v3/transfer-out'][typeIndex]

function UsdtTransfer( e , cur , amount ){
    var params = ''
    var Currency = cur
    var Transfer Quantity = amount
    var exname = e.GetName()
    if( exname == 'Futures_KuCoin'){
        if( typeIndex == 0 ){
            paraStr = '&payAccountType=TRADE'
        }else if( typeIndex == 1 ){
            paraStr = '&recAccountType=TRADE'
        }

        params = "amount="+amount+"&currency="+Currency + paraStr 
        ret = e.IO("api","POST",adress, params )
        Log( Currency , "Transfer Quantity:" , amount , ret)
    }
}

function main() {
    UsdtTransfer( exchange , assets , amount )
}
```

> Detail

https://www.fmz.com/strategy/428110

> Last Modified

2023-09-28 17:27:49
