
> Name

Huobi-U-Contract-Fund-Transfer-Plugin

> Author

xunfeng91



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|typeIndex|0|Transfer type: master-sub account transfer | transfer between different accounts of the same account|
|subuid||sub-accountUID|
|asset|USDT|Transfer Currency|
|from_margin_account|USDT|Margin account to transfer out from|
|to_margin_account|USDT|Margin account to transfer in to|
|amount|10000|Transfer Quantity|
|direct|0|Account transfer direction: Parent to child | Child to parent|


> Source (javascript)

``` javascript


/*
1,Parent-child account transfer
2,Transfer between different margin accounts under the same account
*/ 

var type = [1,2][typeIndex]
function swap_master_sub_transfer( e , cur , amount , direct ){
    try {
        var params = ''
        var Currency = cur
        var Transfer Quantity = amount
        var exname = e.GetName()
        var sub_uid = subuid
        if (!sub_uid){
            Log("Please correct accountUID")
            return
        }
        var frommarginaccount = from_margin_account=="USDT"?from_margin_account:from_margin_account+"-USDT"
        var tomarginaccount = to_margin_account=="USDT"?to_margin_account:to_margin_account+"-USDT"
        transdirect = ["master_to_sub","sub_to_master"][direct]
        params ={"contract_code":frommarginaccount}
        if (amount == -1){
            if(frommarginaccount=="USDT"){//Full Position
                var ret1 = e.IO("api", "POST", "/linear-swap-api/v1/swap_cross_account_info" )
                Transfer Quantity =parseFloat(ret1.data[0].withdraw_available)
            }else{
                var ret1 = e.IO("api", "POST", "/linear-swap-api/v1/swap_account_info" ,"",  JSON.stringify( params ) )
                Transfer Quantity =parseFloat(ret1.data[0].withdraw_available)
            }            
        }
        if( exname == 'Futures_HuobiDM'){
            var Transfer type = transdirect
            params ={
                "sub_uid": sub_uid , 
                "asset": Currency , 
                "from_margin_account":frommarginaccount,
                "to_margin_account":tomarginaccount,
                "amount": Transfer Quantity, 
                "type" : Transfer type,
                "timestamp" : new Date().getTime()    
			}
			Log( "Transfer Currency:",Currency,"Transfer Quantity:",Transfer Quantity,"Transfer type:",Transfer type)
            var ret1 = e.IO("api", "POST", "/linear-swap-api/v1/swap_master_sub_transfer" ,"",  JSON.stringify( params ) )
			Log(ret1)
        }
    } catch (error) { 
        Log( error )
    }  
}

function swap_transfer_inner( e , cur , amount ){
    try {
        var params = ''
        var Currency = cur
        var Transfer Quantity = amount
        var exname = e.GetName()
        var frommarginaccount = from_margin_account=="USDT"?from_margin_account:from_margin_account+"-USDT"
        var tomarginaccount = to_margin_account=="USDT"?to_margin_account:to_margin_account+"-USDT"
        params ={"contract_code":frommarginaccount}
        if (amount == -1){
            if(frommarginaccount=="USDT"){//Full Position
                var ret1 = e.IO("api", "POST", "/linear-swap-api/v1/swap_cross_account_info" )
                Transfer Quantity =_N(parseFloat(ret1.data[0].withdraw_available),6)
            }else{
                var ret1 = e.IO("api", "POST", "/linear-swap-api/v1/swap_account_info" ,"",  JSON.stringify( params ) )
                Transfer Quantity =_N(parseFloat(ret1.data[0].withdraw_available),6)
            }            
        }
        if( exname == 'Futures_HuobiDM'){
            params ={
                "asset": Currency , 
                "from_margin_account":frommarginaccount,
                "to_margin_account":tomarginaccount,
                "amount": Transfer Quantity, 
                "timestamp" : new Date().getTime()    
			}
			Log( "Transfer Currency:",Currency,"Transfer Quantity:",Transfer Quantity,)
            var ret1 = e.IO("api", "POST", "/linear-swap-api/v1/swap_transfer_inner" ,"",  JSON.stringify( params ) )
			Log(ret1)
        }
    } catch (error) { 
        Log( error )
    }

}

function main() {
    if (type==1){
        swap_master_sub_transfer( exchange , asset , amount , direct )
    }
    if (type==2){
        swap_transfer_inner( exchange , asset , amount )
    }
    
}
```

> Detail

https://www.fmz.com/strategy/255402

> Last Modified

2021-02-26 14:32:55
