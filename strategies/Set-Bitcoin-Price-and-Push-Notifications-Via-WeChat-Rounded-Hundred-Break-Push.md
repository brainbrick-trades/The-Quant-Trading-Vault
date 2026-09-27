
> Name

Set-Bitcoin-Price-and-Push-Notifications-Via-WeChat-Rounded-Hundred-Break-Push

> Author

FMZ_JH

> Strategy Description

Teaching Strategies:
When the price is an integer of 100, WeChat pushes a notification, which outputs an array containing 10 elements.

Prefer locking the data in the current range
Polling whether the data crosses this range
Above this interval is an upward breakthrough. Compare with the previous trigger data. If different, record it.
Above this range is a downward breakout, and it should be compared with the data from the previous trigger. If different, record it. Note, there is a 100 range that needs to be added here because they all fall into the bottom integer range.
Array Shift Forward 
Loop

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Interval|true|interval|


> Source (javascript)

``` javascript
/*backtest
start: 2020-10-13 00:00:00
end: 2020-10-14 01:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"OKEX","currency":"BTC_USDT"}]
*/
var a=[1,2,3,4,5,6,7,8,9,10]
var ticker= _C(exchange.GetTicker)

function lock(){                                //Lock the current price in which integer range
    P=parseInt(ticker.Last/100)*100
    HP=P+100
    lock_tickLast=ticker.Last
//    Log(P,HP,ticker.Last)
} 

function stack(){
    for(var k=0;k<a.length;k++)
        a[k]=a[k+1]
}    

function onTick(){
    ticker = _C(exchange.GetTicker) 
    var get=parseInt(ticker.Last/100)*100
    if(get>P){
        a[9]=get 
        if(a[8]!=a[9]){
            str=a.toString()
            if(a[9]-a[8]>100)
                Log("Successful upward gap breakthrough",get,ticker.Last,"{",str,"}",'@')
            else                        
                Log("Successful breakthrough upward",get,ticker.Last,"{",str,"}",'@' )
            lock()
            stack()
        }
    } 
    else if(get<P){
        a[9]=get+100
        if(a[9]!=a[8]){
            str=a.toString()
            if(a[8]-a[9]>100)
                Log("Successful downward gap breakthrough",a[9],ticker.Last,"{",str,"}",'@')
            else
                Log("Successfully broke downward",a[9],ticker.Last,"{",str,"}",'@' )
            lock()
            stack()
        }
    }
}

function main(){

    lock()
    a[8]=P
//    var ticker=0
    Log("The program runs and starts pushing",ticker.Last,'@')
    
    while(true){ 

            onTick()  

        Sleep(Interval*1000)                      
            
    }    
}


```

> Detail

https://www.fmz.com/strategy/231955

> Last Modified

2020-10-29 15:09:21
