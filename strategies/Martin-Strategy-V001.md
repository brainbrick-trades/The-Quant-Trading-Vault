
> Name

Martin-Strategy-V001

> Author

superMan



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|DF|0,1,2,3,4,5,6,7|The ratio of each decrease, converted from string to array.|
|JYD|$$$__enc__$$$BTC|Trading pairs you bought yourself|
|startNum|true|The quantity bought at the very beginning, unitUSTD|
|minWin|1.3|Take profit percentage|


> Source (javascript)

``` javascript




var DFlist = DF.split(',').map(item => 0 - item)  // Array of declining ranges, initially replaced by a string because array cannot be set;
var JYDlist = JYD.split(',')                   // Selected trading pair.
var account = 0;                               // Account balance
var index = 0;                                 // Number of positions covered
var accountNum = 0                             // Total Position Volume
var countPrice = false;                        // Total Position Value
var YKBL = 0                                   // Profit and loss ratio
var copyStartNum = startNum;
var FrozenBalance = 0;                         // Current frozen balance on the platform


// Function method area
// Initialization function
function initFn(isFirst){  
    account = _C(exchange.GetAccount)
    if(isFirst){
        Log('robot starts to run')
    } else {
        Log('robot Repeating')
    }
}

// Loop Function
function onTick() {
    
}

// Loop to ensure the order has been bought
function onSureBuy(FrozenBalance){
    
}

// Buy Function 
function onBuy(){
    let account = _C(exchange.GetAccount)
    if ((account.Balance / currentPrice > copyStartNum && accountNum == 0) || DFlist[index] > YKBL){
        exchange.Buy(currentPrice, copyStartNum);
        Log(`Order bought, the price is${currentPrice},Quantity is${copyStartNum}`,'#ff0000')
        FrozenBalance = currentPrice * copyStartNum
        let i = 0
        while(FrozenBalance){
            FrozenBalance = _C(exchange.GetAccount).FrozenBalance;
            if(i >= 5 ){
                let order = _C(exchange.GetOrders) 
                order = JSON.stringify(order)
                for(let i = 0; i < order.legnth; i++){
                    exchange.CancelOrder(order[i].Id);
                }
                Log('Cancel Buy,The platform's frozen balance is:',FrozenBalance, '#00ff00')
                break
            } else if(FrozenBalance) {
                i++
            } else {
                break
            }
            Sleep(200)
        }
                
        
        if(i >= 5 && FrozenBalance){
            FrozenBalance = 0
            return false 
        } else {
          // Reaching this point indicates the buy order was successful
          Log(`Order bought successfully, price is${currentPrice},Quantity is${copyStartNum}`,'#00ff00')
          accountNum += copyStartNum
          countPrice += currentPrice * copyStartNum
          copyStartNum = copyStartNum*2
          index++  
        }
            
    } 
    if(account.Balance / currentPrice < copyStartNum){
        // Log("Account balance is insufficient")
    }
}

// Entry Function
function main() {
    initFn(true)
    var num = 1;
    while(1){
        
        account = _C(exchange.GetAccount)
        currentPrice = _C(exchange.GetTicker).Low;
        //Log(`Loop Number${num}times`,'account',account,'currentPrice',currentPrice,'countPrice',countPrice,'YKBL',YKBL,'copyStartNum',copyStartNum)
    
        num++
        // Get the current price change
        if(!countPrice){
            countPrice = currentPrice * copyStartNum
        } else {
            // Calculate the current profit and loss ratio
            YKBL = (countPrice * copyStartNum - currentPrice * copyStartNum) / countPrice * copyStartNum *100
        }
    
        Log(`Current loop number${num}Secondary profit and loss ratio is`,YKBL)
        if(YKBL > 1000 ){
            Log('Current Total Price',YKBL,'Current total coin holdings',copyStartNum,'Current Selling Price',currentPrice,'#ff0000')
        }
        
    
        // Sell when the take-profit percentage is reached
        if(YKBL > minWin){
            // var diffStock = _N(countPrice / accountNum);
        
            var diffStock = _N(account.Stocks, 4);
            exchange.Sell(currentPrice, diffStock)
            countPrice = 0
            accountNum = 0
            copyStartNum = startNum
            Log("Sell price is:",currentPrice,diffStock,account,'#00ff00')
            index = 0
        
        }
        
        // buy
        onBuy()
    
        Sleep(1000*60)
    }
    
}

```

> Detail

https://www.fmz.com/strategy/288966

> Last Modified

2021-06-10 13:30:52
