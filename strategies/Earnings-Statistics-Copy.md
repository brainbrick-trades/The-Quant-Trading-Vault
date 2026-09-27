
> Name

Earnings-Statistics-Copy

> Author

总值约: 23938.37 元

> Strategy Description

Statistics of total profits from OK and Bitvc futures; OK is the main exchange;

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|LXT|20|Cycle period (seconds).)|


> Source (javascript)

``` javascript
var okrights=0;
var vcright=0;
var InitRights=0;
var totalrights=0;
var profit=0;
var oldprofit=0;

SetErrorFilter("502:|503:|unexpected|network|timeout|WSARecv|Connect|GetAddr|no such|reset|http|received|EOF");



function Rights() {
        
        var accountok;
        var accountvc;
        while (!(accountok = exchanges[0].GetAccount())) {
            Sleep(500);
        }
        while (!(accountvc = exchanges[1].GetAccount())) {
            Sleep(500);
        }
        var objok;
        var objvc;
        
        objok=JSON.parse(exchanges[0].GetRawJSON());
        objvc=JSON.parse(exchanges[1].GetRawJSON());
        
        okrights=objok.info["btc"].rights;
        vcrights=objvc.dynamicRights;
        totalrights=okrights+vcrights;
        
        
}

function main(){
    Rights();
    InitRights=totalrights;
   Log("Initial equity total_BTC",InitRights);
   while(true){
    Rights();
    profit=totalrights-InitRights;
    if(profit!==oldprofit){
    LogProfit(profit,"BTC");
    oldprofit=profit;
    }
    Sleep(LXT*1000);
   }
   
 
}




```

> Detail

https://www.fmz.com/strategy/4489

> Last Modified

2015-02-28 19:17:29
