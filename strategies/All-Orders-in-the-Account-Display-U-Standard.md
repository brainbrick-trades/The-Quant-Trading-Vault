
> Name

All-Orders-in-the-Account-Display-U-Standard

> Author

高频量化





> Source (javascript)

``` javascript
function main() {
    //exchange.SetContractType("swap"); // Set as a perpetual contract, pay attention to coin-based andUSDTPerpetual exists in all base currencies
    const binanceFundingRate = {//Array of open positions
        type: 'table',
        title: 'Binance USDT-margined position order',
        cols: ['Trading pair', 'Trading direction', 'Opening volume', 'Opening price', 'Position value', 'Leverage', 'Occupied margin', 'Position profit'], //List header
        rows: null //List array
    };
        const binanceHangingOrder = {//Pending Orders Array
        type: 'table',
        title: 'Binance USDT-margined orders',
        cols: ['Trading pair', 'Trading direction', 'Pending order status', 'Opening volume', 'Opening price', 'Pending order value', 'Order ID', 'Order time'], //List header
        rows: null //List array
    };
    const gateFundingRate = {//Personal Information
        type: 'table',
        title: 'Contact Information',
        cols: ['WeChat: 18826683356, Binance tools rental']
    }
    //Loop body
    while (true) {
        binanceFundingRate.rows = []
        binanceHangingOrder.rows = [] //Temporary array for pending orders
        var y = 0 //It can be judged even without the product
        var yy = 0 //It can be judged even without the product        
        var exchangeInfo = HttpQuery('https://fapi.binance.com/fapi/v1/exchangeInfo');//If access is not possible, it can be resolved by setting up a product pool.
        exchangeInfo = JSON.parse(exchangeInfo) //ProcessjsonFile
        for (var i = 0; i < exchangeInfo.symbols.length; i++) {
            var bas = exchangeInfo.symbols[i];
            var symbols1 = bas.baseAsset + "_" + bas.quoteAsset //Synthetic Product Name
            var symbolstr = String(symbols1) //Forced String
            if (symbolstr == "BTCST_USDT") continue //I don't know why, but an already nonexistent product has appeared.
            exchange.SetCurrency(symbolstr) //Switch product
            if(exchangeInfo.symbols[i].contractType=="NEXT_QUARTER"){//Next quarter
                exchange.SetContractType("next_quarter")
            }else if(exchangeInfo.symbols[i].contractType=="CURRENT_QUARTER"){//Current Quarter
                exchange.SetContractType("quarter")
            }else if(exchangeInfo.symbols[i].contractType=="PERPETUAL"){//perpetual
                exchange.SetContractType("swap")
            }else {
                Log("Product Expired",symbolstr)              
            }
            let depth = exchange.GetDepth(); //Obtain market data. If the product is not changed, the market data will not be obtained.
            if (!depth) {
                Log("This product does not exist:", symbolstr, "Or the product list format is incorrect") // Used for testing
                continue; //Did not obtain market data for this product
            }
            //-------------------------------------------------------
            var position = exchange.GetPosition() //Get account position information
            //Perpetual and non-uniform coin-margined cross-futures contracts are placed in one array. Perpetual contracts are different.
            var positionLength = position.length
            if (positionLength > 0) {
            for(var iii= 0;iii <positionLength;iii++){
                if(exchange.GetContractType()==position[iii].ContractType){//Why judge? Because all the positions in the spread contract are grouped together
                binanceFundingRate.rows[y] = [position[iii].Info.symbol, position[iii].Type==0?"BUY":"SELL", position[iii].Amount, 
                                             position[iii].Price, position[iii].Amount* position[iii].Price,
                                             position[iii].MarginLevel,position[iii].Margin,position[iii].Profit]
                y = y + 1
                }
            }
            } //Ensure the product exists, otherwise an array error will occur 
            //-------------------------------------------------------
             var GetOrder=  exchange.GetOrders() //Get the pending orders for this product in the account
             //Contracts with different coin-denominated spaches are not placed in a single array. Perpetual contracts are not the same
             var GetOrderLength = GetOrder.length
             if (GetOrderLength > 0) {
                 //Loop Orders
                 for(var ii = 0;ii <GetOrderLength;ii++ ){
                     binanceHangingOrder.rows[yy]=[
                                             GetOrder[ii].Info.symbol,GetOrder[ii].Info.side,GetOrder[ii].Info.type,GetOrder[ii].Amount, 
                                             GetOrder[ii].Price, GetOrder[ii].Amount* GetOrder[ii].Price,
                                             GetOrder[ii].Id,_D(GetOrder[ii].Info.time)]
                  yy = yy + 1 
                 }
             }
        }
        //binanceFundingRate.rows = binanceFundingRaterows
        //binanceHangingOrder.rows = binanceFundingRaterowsOrder
        //Log("binanceFundingRate.rows", binanceFundingRate.rows)
        LogStatus('\n`' + JSON.stringify([binanceFundingRate,binanceHangingOrder, gateFundingRate]) + '`\n'); //Column box display
        Sleep(1000*10); //one minute   
    }
}
```

> Detail

https://www.fmz.com/strategy/335519

> Last Modified

2021-12-17 23:22:30
