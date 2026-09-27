
> Name

Binance-Manual-Opening-and-Closing-Tool

> Author

高频量化



> Strategy Arguments





|Button|Default|Description|
|----|----|----|
|Symbols|ETC_USDT|Product|
|CloseAll|__button__|Close all positions button|
|CloseBuy|true|Close N coins of long positions|
|CloseSell|true|Close N coins of short positions|
|OpenBuy|true|Open long positions (N coins))|
|OpenSell|true|Open short positions (N coins))|


> Source (javascript)

``` javascript
var Symbols;
//----------------------------------------
//Button monitoring requires high frequency
function ButtonFun() {
    //-----------------Manually close long-----------------------  
    var cmd = GetCommand() //Get button change amount
    if (cmd) {
        //Button to switch products
        var arr = cmd.split(":")
       //exchange.SetContractType("swap") //Set to the product quarter
       //exchange.SetCurrency(Symbols) //Switch product (default product))
        if(arr[0] == "Symbols"){
        exchange.SetCurrency(arr[1]) //Switch product (default product))  
        Symbols=arr[1]
        Log("Trading product has been switched to:",arr[1])
        }
        if (arr[0] == "CloseAll") { //Close all positions
            let position = exchange.GetPosition() //Position order (Only get positions for the current product)
            if (position.length > 0) {
                if (position[0].Type == 0) { //close long
                    exchange.SetDirection("closebuy")
                    ticker = exchange.GetTicker() //Get current market priceticker.Buy,To ensure execution, may need to chase20Gear
                    let depth = exchange.GetDepth() //Get market data, large depth.Asks[20].Price    ,Small depth.Bids[20].Price
                    exchange.Sell(depth.Bids[20].Price, position[0].Amount)
                    Log(Symbols + "Manually close all long positions" + position[0].Amount )
                } else { //close short
                    exchange.SetDirection("closesell")
                    ticker = exchange.GetTicker() //Get current market priceticker.Sell,
                    let depth = exchange.GetDepth() //Get market data, large depth.Asks[20].Price    ,Small depth.Bids[20].Price                        
                    exchange.Buy(depth.Asks[20].Price, position[0].Amount)
                    Log(Symbols + "Manually close all short positions" + position[0].Amount )
                }
            }
        }

        if (arr[0] == "CloseBuy") { //Partial closing of long positions
            //Log("arr=", arr, "arr[0]", arr[0], "arr[1]", arr[1])
            exchange.SetDirection("closebuy")
            ticker = exchange.GetTicker() //Get current market priceticker.Buy,To ensure execution, may need to chase20Gear
            let depth = exchange.GetDepth() //Get market data, large depth.Asks[20].Price    ,Small depth.Bids[20].Price  
            exchange.Sell(depth.Bids[20].Price, Number(arr[1]))
            Log(Symbols, "Manually close part of long positions" + arr[1])
        }
        if (arr[0] == "OpenBuy") { //Partially open long
            //Log("arr=",arr,"arr[0]",arr[0],"arr[1]",arr[1])
            exchange.SetDirection("buy")
            ticker = exchange.GetTicker() //Get current market priceticker.Buy,To ensure execution, may need to chase20Gear
            let depth = exchange.GetDepth() //Get market data, large depth.Asks[20].Price    ,Small depth.Bids[20].Price
            exchange.Buy(depth.Asks[20].Price, Number(arr[1]))
            Log(Symbols + "Manual opening of multiple orders" + arr[1])
        }

        if (arr[0] == "CloseSell") { //Partial closing of short position
            exchange.SetDirection("closesell")
            ticker = exchange.GetTicker() //Get current market priceticker.Sell,To ensure execution, may need to chase20Gear
            let depth = exchange.GetDepth() //Get market data, large depth.Asks[20].Price    ,Small depth.Bids[20].Price 
            exchange.Buy(depth.Asks[20].Price, Number(arr[1]))
            Log(Symbols + "Manually close part of short positions" + arr[1])
        }
        if (arr[0] == "OpenSell") { //Manually open short
            exchange.SetDirection("sell")
            ticker = exchange.GetTicker() //Get current market priceticker.Buy,To ensure execution, may need to chase20Gear
            let depth = exchange.GetDepth() //Get market data, large depth.Asks[20].Price    ,Small depth.Bids[20].Price 
            exchange.Sell(depth.Bids[20].Price, Number(arr[1]))
            Log(Symbols + "Manual opening of short orders" + arr[1])
        }
    }
}

//---------------------------------------------------------------
//Main Function
//---------------------------------------------------------------
function main() {
    exchange.SetContractType("swap") //Set to the product quarter
    //exchange.SetCurrency(Symbols) //Switch product (default product))
    while (true) {
        ButtonFun() 
        let position = exchange.GetPosition() //Position order (Only get positions for the current product)
        if (position.length > 0) {
            LogStatus(_D(), "Current product direction: ", position[0].Type==0?"BUY":"SELL", "Holding amount:", position[0].Amount, "Open position profit:", position[0].Profit)
        } else {
            LogStatus(_D(), "Current product holdings: ", 0, "Open position profit:", 0)
        }
        Sleep(1000 *1); // Sleep for 3 seconds
    }
}
```

> Detail

https://www.fmz.com/strategy/335089

> Last Modified

2021-12-17 22:38:47
