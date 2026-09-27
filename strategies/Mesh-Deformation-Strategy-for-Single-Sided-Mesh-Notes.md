
> Name

Mesh-Deformation-Strategy-for-Single-Sided-Mesh-Notes

> Author

hk量

> Strategy Description

Grid can customize direction
Buy first and sell later:
The grid will place buy orders downwards from the first price. The interval between each buy order is the "price interval" parameter. The number of pending orders is "single quantity". If the "total quantity" of buy orders is placed, after any buy order is completed, the program will add the "spread (yuan)" parameter to the purchase price to place a sell order. After selling, the buy order will be placed again at the original price of this grid.
Sell first then buy:
Operation is exactly the opposite

The biggest risk of the strategy is a one-sided market, where price fluctuations exceed the grid range.

Grid has automatic stop loss and moving function


// Little dream, dream returns
// https://www.fmz.com/bbs-topic/334  In summary - Inventor Quantification Video and Text-Based Instruction
//https://www.fmz.com/bbs-topic/1069 Mesh deformation strategy for single-sided mesh (Annotated version)


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|OpType|0|Grid direction: Buy first, then sell | Sell first, then buy|
|FirstPriceAuto|true|First price automatically|
|FirstPrice|100|First price|
|AllNum|10|Total quantity|
|PriceGrid|true|Price interval|
|PriceDiff|2|Price difference (yuan)|
|AmountType|0|Order size: Same buy and sell volume | Custom quantity|
|AmountOnce|0.1|Single transaction quantity|
|BAmountOnce|0.1|Buy order size|
|SAmountOnce|0.1|Sell order size|
|AmountCoefficient|*1|volume difference|
|AmountDot|3|Maximum decimal places for quantity|
|EnableProtectDiff|false|Enable spread protection|
|ProtectDiff|20|Entry-point spread protection|
|CancelAllWS|true|Cancel all orders when stopping|
|CheckInterval|2000|Polling Interval|
|Interval|1300|Failed retry interval|
|RestoreProfit|false|Restore last profit|
|LastProfit|false|Last Profit|
|ProfitAsOrg|false|Last profit included in average price|
|EnableAccountCheck|true|Activate fund inspection|
|EnableStopLoss|false|Enable stop loss|
|StopLoss|100|Maximum floating loss (CNY))|
|StopLossMode|0|Action after stop loss: recover and exit | recover and redeploy|
|EnableStopWin|false|Enable take profit|
|StopWin|120|Maximum floating profit (CNY))|
|StopWinMode|0|Action after taking profit: recover and exit | recover and redeploy|
|AutoMove|false|Automatic movement|
|MaxDistance|20|Maximum distance (yuan).)|
|MaxIdle|7200|Maximum idle (seconds).)|
|EnableDynamic|false|Enable dynamic order placement|
|DynamicMax|30|Order expiration distance (CNY))|
|ResetData|true|Clear all data at startup|
|Precision|5|Price decimal place length|
|XPrecision|5|Decimal length for order quantity|
|MinStock|0.001|Minimum transaction volume|




|Button|Default|Description|
|----|----|----|
|Close network|__button__|stop and balance back to initial state|


> Source (javascript)

``` javascript



 

/*backtest
start: 2021-08-27 00:00:00
end: 2021-08-28 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Huobi","currency":"BTC_USDT"}]
args: [["OpType",1]]
*/


// Little dream, dream returns
// https://www.fmz.com/bbs-topic/334  In summary - Inventor Quantification Video and Text-Based Instruction
//https://www.fmz.com/bbs-topic/1069 Mesh deformation strategy for single-sided mesh (Annotated version)

/*  Interface parameters (reflected as global variables in the code))
Variable Description Type Default Value         
OpType                              Grid direction drop-down box (selected) Buy before selling | Sell before buying
FirstPriceAuto                      First price auto Boolean(true/false)         true
FirstPrice@!FirstPriceAuto          Opening price Numeric(number)             100
AllNum                              Total quantity Numeric(number)             10
PriceGrid                           Price interval Numeric(number)              1
PriceDiff                           Price difference (Yuan) Numeric(number)              2
AmountType                          Order size drop-down box (selected) Buy and sell the same amount | Custom amount
AmountOnce@AmountType==0            Single order quantity Numeric(number)             0.1
BAmountOnce@AmountType==1           Buy order size Numeric(number)             0.1
SAmountOnce@AmountType==1           Sell order size Numeric(number)             0.1
AmountCoefficient@AmountType==0     Volume difference String(string)             *1
AmountDot                           Maximum number of decimal places for volume Numeric type(number)             3
EnableProtectDiff                   Enable spread protection Boolean(true/false)         false
ProtectDiff@EnableProtectDiff       Market entry spread protection Numeric(number)              20
CancelAllWS                         Cancel all pending orders when stopping Boolean type(true/false)         true
CheckInterval                       Polling interval Numeric(number)              2000
Interval                            Retry interval on failure Numeric(number)              1300
RestoreProfit                       Restore last profit Boolean(true/false)          false
LastProfit@RestoreProfit            Last profit Numeric(number)               0
ProfitAsOrg@RestoreProfit           Include last profit in average price Boolean type(true/false)          false
EnableAccountCheck                  Enable funds verification Boolean(true/false)          true
EnableStopLoss@EnableAccountCheck   Enable stop loss Boolean(true/false)          false
StopLoss@EnableStopLoss             Maximum floating loss (CNY) Numeric type(number)              100
StopLossMode@EnableStopLoss         Operation after stop loss drop-down box (selected) Recycle and exit | Recycle and then cast the net
EnableStopWin@EnableAccountCheck    Enable take profit Boolean(true/false)           false
StopWin@EnableStopWin               Maximum floating profit (CNY) Numeric type(number)               120
StopWinMode@EnableStopWin           Operation after taking profit drop-down box (selected) Recycle and exit | Recycle and then cast the net
AutoMove@EnableAccountCheck         Auto-move Boolean(true/false)          false
MaxDistance@AutoMove                Maximum distance (yuan) Numeric(number)               20
MaxIdle@AutoMove                    Maximum idle time (seconds) Numeric(number)               7200
EnableDynamic                       Enable dynamic order boolean(true/false)          false
DynamicMax@EnableDynamic            Order expiration distance (CNY) Numeric(number)               30
ResetData                           Clear all data on startup Boolean type(true/false)           true
Precision                           Price decimal places length Numeric(number)                5
*/

function hasOrder(orders, orderId) //
{                           // Check whether there is an order with ID orderId in the parameter orders
    for (var i = 0; i < orders.length; i++) //
    {                  // Traverse orders to check if there is the same id, return if found true
        if (orders[i].Id == orderId) //
        {
            return true;
        }
    }
    return false;                                              // All traversed, none triggered if Not found ID is orderId Order of, return false
}


function cancelPending() //
{                                      // Cancel all orders function
    var ret = false;                                            // Set return success flag variable
    while (true) //
    {                                              // while Loop
        if (ret) //
        {                                              // If ret is true, sleep lasts for a certain period
            Sleep(Interval);
        }
        var orders = _C(exchange.GetOrders);                    // Call  API Get information on outstanding orders on the exchange
        if (orders.length == 0) //
        {                               // If it returns an empty array, it means the exchange has no pending orders.
            break;                                              // Break out of while loop
        }

        for (var j = 0; j < orders.length; j++) //
        {               // Traverse the unfinished order array, and use orders[j].Id one by one according to index j to cancel the order.
            exchange.CancelOrder(orders[j].Id, orders[j]);
            ret = true;                                         // Once there is a cancel operation, ret Assign value to true .Used to trigger above Sleep , Wait and then retry exchange.GetOrders Detect 
        }
    }
    return ret;                                                 // Return ret
}

function valuesToString(values, pos) //
{                      // Convert value to string
    var result = '';                                        // Declare an empty string for return  result
    if (typeof (pos) === 'undefined') //
    {                      // If the parameter pos is not passed in, assign a value to pos 0
        pos = 0;
    }
    for (var i = pos; i < values.length; i++) //
    {             // Handles the values array based on the input pos
        if (i > pos) //
        {                                      // Except for the first loop, add a single space ' ' after the result string
            result += ' ';
        }
        if (values[i] === null) //
        {                           // If the element of the current index of values (function parameter list array) is null, then result adds a 'null' string
            result += 'null';
        }//
        else if (typeof (values[i]) == 'undefined') //
        {      // If it is undefined, then add 'undefined'
            result += 'undefined';
        }//
        else //
        {                                            // Remaining types; use switch detection and handle separately
            switch (values[i].constructor.name) //
            {           // Check the name property of the constructor of values[i], i.e., the type name
                case 'Date':
                case 'Number':
                case 'String':
                case 'Function':
                    result += values[i].toString();         // If it is of date type, numeric type, string type, or function type, call it toString Convert function to string, then add
                    break;
                default:
                    result += JSON.stringify(values[i]);    // In other cases, useJSON.stringify Function convert to JSON String added to result 
                    break;
            }
        }
    }
    return result;                                          // Return result
}

function Trader() //
{                                                 // Trader Function, using closure.
    var vId = 0;                                                    // Order incrementID
    var orderBooks = [];                                            // Order book
    var hisBooks = [];                                              // Historical order book
    var orderBooksLen = 0;                                          // Order book length
    this.Buy = function (price, amount, extra) //
    {                     // Buy function, parameters: price, quantity, extended information
        if (typeof (extra) === 'undefined') //
        {                        // If the extra parameter is not passed, typeof returns undefined 
            extra = '';                                             // Assign an empty string to extra
        }//
        else //
        {
            extra = valuesToString(arguments, 2);                   // The parameters arguments passed in when calling this.Buy function are passed into the valuesToString function.
        }
        vId++;                                                      // 
        var orderId = "V" + vId;                                    //
        orderBooks[orderId] = //
        {                                     // Add the property orderId to the order book array and initialize it with the constructed object.
            Type: ORDER_TYPE_BUY,                                   // Constructed object Type attribute: Type Buy order
            Status: ORDER_STATE_PENDING,                            //                       Status Pending
            Id: 0,                                                  //                       OrderID  0
            Price: price,                                           //                       Price Parameter price
            Amount: amount,                                         //                       Order quantity Parameter amount 
            Extra: extra                                            //                       Extended information processed by valuesToString.
        };
        orderBooksLen++;                                            // Length of the order book is cumulatively added1
        return orderId;                                             // Return the constructed order of this time  orderId (Non-exchange orderID ,Don't confuse.)
    };
    this.Sell = function (price, amount, extra) //
    {                    // Very similar to thie.Buy, construct sell order.
        if (typeof (extra) === 'undefined') //
        {
            extra = '';
        }//
        else //
        {
            extra = valuesToString(arguments, 2);
        }
        vId++;
        var orderId = "V" + vId;
        orderBooks[orderId] = //
        {
            Type: ORDER_TYPE_SELL,
            Status: ORDER_STATE_PENDING,
            Id: 0,
            Price: price,
            Amount: amount,
            Extra: extra
        };
        orderBooksLen++;
        return orderId;
    };
    this.GetOrders = function () //
    {                                   // Get information about unfinished orders
        var orders = _C(exchange.GetOrders);                        // Call API GetOrders Get the pending order information and assign a value to orders
        for (orderId in orderBooks) //
        {                               // Traverse the Trader object in orderBooks 
            var order = orderBooks[orderId];                        // according to orderId Extract order
            if (order.Status !== ORDER_STATE_PENDING) //
            {             // If the status of order is not equal to the pending status, skip this loop
                continue;
            }
            var found = false;                                      // Initialize found Variable (flag whether found) is true
            for (var i = 0; i < orders.length; i++) //
            {               // Iterate through the data of uncompleted orders returned by the API  
                if (orders[i].Id == order.Id) //
                {                     // When an order with the same id as the unfinished order in orderBooks is found, assign true to found, which means it is found. 
                    found = true;
                    break;                                          // Break out of the current loop
                }
            }
            if (!found) //
            {                                           // If not found, then to orders push  orderBooks[orderId].
                orders.push(orderBooks[orderId]);                   // Why do this push ?
            }
        }
        return orders;                                              // Return orders
    }
    this.GetOrder = function (orderId) //
    {                             // Get order
        if (typeof (orderId) === 'number') //
        {                         // If the passed parameter orderId is a numeric type 
            return exchange.GetOrder(orderId);                      // Call API GetOrder according to orderId Retrieve order information and return it.
        }
        if (typeof (hisBooks[orderId]) !== 'undefined') //
        {            // typeof(hisBooks[orderId]) If not equal to undefined
            return hisBooks[orderId];                               // Return hisBooks Middle attribute is orderId Data
        }
        if (typeof (orderBooks[orderId]) !== 'undefined') //
        {          // Same as above, if orderBooks contains an attribute with the value orderId, return this data.
            return orderBooks[orderId];
        }
        return null;                                                // If the above conditions are not met, trigger and return null
    };
    this.Len = function () //
    {                                         // Returns the Trader's orderBookLen variable, i.e., the order book length.
        return orderBooksLen;
    };
    this.RealLen = function () //
    {                                     // Return the number of active orders in the order book.
        var n = 0;                                                  // Initial count is 0
        for (orderId in orderBooks) //
        {                               // Traverse the order book
            if (orderBooks[orderId].Id > 0) //
            {                       // If the Id of the current order in the traversal is greater than 0, that is, not the initial 0, it indicates that the order has been placed and the order has been activated.
                n++;                                                // Accumulate Orders that have already been activated
            }
        }
        return n;                                                   // Return nvalue, i.e., returns the real order book length. (Number of activated orders)
    };
    this.Poll = function (ticker, priceDiff) //
    {                       // 
        var orders = _C(exchange.GetOrders);                        // Get all unfinished orders
        for (orderId in orderBooks) //
        {                               // Traverse the order book
            var order = orderBooks[orderId];                        // Take out the current order and assign to order
            if (order.Id > 0) //
            {                                     // If the order is active, that is, order. Id is not 0 (an order has already been placed).)
                var found = false;                                  // Variables found(Tag found) as false
                for (var i = 0; i < orders.length; i++) //
                {           // Find the same order number in the pending order information returned by the exchange
                    if (order.Id == orders[i].Id) //
                    {                 // If found, assign true to found, which means it has been found.
                        found = true;
                    }
                }
                if (!found) //
                {                                       // If the order represented by the current orderId does not find the corresponding order in the uncompleted order array orders returned by the exchange.
                    order.Status = ORDER_STATE_CLOSED;              // Update the order corresponding to orderId in orderBooks (that is, the current order variable), and update the Status attribute to ORDER_STATE_CLOSED (that is, closed) 
                    hisBooks[orderId] = order;                      // Completed orders are recorded in the historical order book, i.e., hisBooks, unified and unique order numbers orderId
                    delete (orderBooks[orderId]);                    // Delete the property named orderId value from the order book (remove completed orders from it))
                    orderBooksLen--;                                // Order book length decrement
                    continue;                                       // The following code skips and continues the loop.
                }
            }
            var diff = _N(order.Type == ORDER_TYPE_BUY ? (ticker.Buy - order.Price) : (order.Price - ticker.Sell));
            // diff The difference between the planned opening price of the orders in the current order book and the current real-time opening price.

            var pfn = order.Type == ORDER_TYPE_BUY ? exchange.Buy : exchange.Sell;   // Based on the type of order, give pfn Assign corresponding  API Function reference.
            // That is, if order The type is a buy order , pfn That's it  exchange.Buy Function reference, same for sell orders.

            if (order.Id == 0 && diff <= priceDiff) //
            {                                // If the order order in the order book is not activated (that is, Id equals 0) and the current price distance from the order plan price is less than or equal to the parameter passed in priceDiff
                var realId = pfn(order.Price, order.Amount, order.Extra + "(distance: " + diff + (order.Type == ORDER_TYPE_BUY ? (" Buy one: " + ticker.Buy) : (" Sell one: " + ticker.Sell)) + ")");
                // Execute the order function, passing parameters such as price, quantity, and order extension information + Pending order distance + market data (best bid or best ask), returns exchange ordersid

                if (typeof (realId) === 'number') //
                {    // If the returned realId is of numeric type
                    order.Id = realId;                // Assign the Id property of the current order in the order book to order.
                }
            }//
            else if (order.Id > 0 && diff > (priceDiff + 1)) //
            {  // If the order is active and the current distance is greater than the distance passed in by the parameter
                var ok = true;                                    // Declare a variable for marking, initially true 
                do //
                {                                              // Execute 'do' first, then judge while
                    ok = true;                                    // ok Assignment true
                    exchange.CancelOrder(order.Id, "Unnecessary" + (order.Type == ORDER_TYPE_BUY ? "Buy Order" : "Sell Order"), "order price:", order.Price, "Amount:", order.Amount, ", distance:", diff, order.Type == ORDER_TYPE_BUY ? ("Buy one: " + ticker.Buy) : ("Sell one: " + ticker.Sell));
                    // Cancel the current orders that exceed the range; after logging this cancellation, print current order information and the current distance. diff.

                    Sleep(200);                                   // Wait 200 milliseconds
                    orders = _C(exchange.GetOrders);              // Call API Get uncompleted orders from the exchange.
                    for (var i = 0; i < orders.length; i++) //
                    {     // Traverse these unfinished orders.
                        if (orders[i].Id == order.Id) //
                        {           // If a canceled order is found that is still in the stack of uncompleted orders on the exchange
                            ok = false;                           // Assign the value false to the variable ok, that is, the cancellation is not successful.
                        }
                    }
                } while (!ok);                                    // If ok is false,Then !ok is true ,while It will continue to loop, repeatedly cancel this order, and check whether the cancellation is successful
                order.Id = 0;                                     // Assign 0 to order.Id, representing that the current order is inactive.
            }
        }
    };
}

function balanceAccount(orgAccount, initAccount) //
{               // Balance Account Function Parameters The initial account information when the strategy is started, the initial account information before this casting.
    cancelPending();                                             // Call the custom function cancelPending() to cancel all pending orders.
    var nowAccount = _C(exchange.GetAccount);                    // Declare a variable  nowAccount Used to record the latest account information at this moment.
    var slidePrice = 0.2;                                        // Set slippage when placing order to 0.2
    var ok = true;                                               // Tag variable initial  true
    while (true) //
    {                                               // while Loop
        var diff = _N(nowAccount.Stocks - initAccount.Stocks);   // Calculate the coin difference between the current account and the initial account diff
        if (Math.abs(diff) < exchange.GetMinStock()) //
        {           // If the absolute value of the coin difference is less than the exchange's minimum trading volume, break the loop and do not perform balancing.
            break;
        }
        var depth = _C(exchange.GetDepth);                       // Get the exchange depth information and assign it to the declared variable depth Variables 
        var books = diff > 0 ? depth.Bids : depth.Asks;          // According to whether the spread is greater than0 Or less than 0 ,extract depth The buy order array or sell order array (equals0 Will not process, judge for less thanGetMinStock alreadybreak)
        // Coin difference greater than0 To sell for balance, look at the buy order array, coin difference less than0 opposite.
        var n = 0;                                               // Statement n Initially 0
        var price = 0;                                           // Statement price initial 0
        for (var i = 0; i < books.length; i++) //
        {                 // Iterate over the array of buy or sell orders
            n += books[i].Amount;                                // According to the iterated index i , Accumulate each orderAmount (Order volume)
            if (n >= Math.abs(diff)) //
            {                           // If the accumulated order quantity n is greater than or equal to the currency difference, then:
                price = books[i].Price;                          // Get the price of the current index order, assign to price
                break;                                           // Break out of the current for loop
            }
        }
        var pfn = diff > 0 ? exchange.Sell : exchange.Buy;       // Based on the currency difference being greater than0 Or less than 0 , placed a sell order API(exchange.Sell) Or place a buy order API(exchange.Buy) Pass by reference to the declaration pfn
        var amount = Math.abs(diff);                             // Order quantity for the operation to be balanced is diff That is, the coin difference, assigned to the declared variable amount Variables
        var price = diff > 0 ? (price - slidePrice) : (price + slidePrice);    // Determine buy/sell direction based on coin spread, in price , add or subtract the sliding price (the sliding price is to make it easier to complete the transaction), and then assign the value to price
        Log("Start balancing", (diff > 0 ? "sell" : "buy"), amount, "Currency");            // Output log of balance in currency.
        if (diff > 0) //
        {                                                        // Check whether your account has enough coins or money to determine the buy and sell direction based on the currency difference.
            amount = Math.min(nowAccount.Stocks, amount);                      // ensure order quantity amount Will not exceed the available coins in the current account.
        }//
        else //
        {
            amount = Math.min(nowAccount.Balance / price, amount);             // ensure order quantity amount Will not exceed the available funds in the current account.
        }
        if (amount < exchange.GetMinStock()) //
        {                                 // Check whether the final order quantity is less than the minimum order quantity allowed by the exchange
            Log("Insufficient funds, Unable to balance to the initial state");                                    // If the order volume is too small, print a message.
            ok = false;                                                         // Tag balance failed
            break;                                                              // Break out of while loop
        }
        pfn(price, amount);                                                     // Execute order API (pfn reference))
        Sleep(1000);                                                            // Pause for 1 second
        cancelPending();                                                        // Cancel all pending orders.
        nowAccount = _C(exchange.GetAccount);                                   // Get current latest account information
    }
    if (ok) //
    {                                                                   // Execute the code inside curly braces when ok is true (balance successful)
        LogProfit(_N(nowAccount.Balance - orgAccount.Balance));                 // Use the Balance attribute of the incoming parameter orgAccount (account information before balancing) to subtract the Balance attribute of the current account information, that is, the difference in money, 
        // That is, profit and loss (since the number of coins remains unchanged, there may be slight discrepancies, because some very small quantities cannot be balanced).)
        Log("Balance completed", nowAccount);                                              // Output log: balance completed.
    }
}

var STATE_WAIT_OPEN = 0;                                                        // used for fishTable The state of each node in
var STATE_WAIT_COVER = 1;                                                       // ...
var STATE_WAIT_CLOSE = 2;                                                       // ...
var ProfitCount = 0;                                                            // Profit and loss times record
var BuyFirst = true;                                                            // Initial interface parameters
var IsSupportGetOrder = true;                                                   // Whether the exchange supports  GetOrder API Function, Global variable, used for main Judgment at the start of the function
var LastBusy = 0;                                                               // Record the last processed time object

function setBusy() //
{                            // Set Busy time
    LastBusy = new Date();                      // Assign the current time object to LastBusy
}

function isTimeout() //
{                                                          // Check for timeout
    if (MaxIdle <= 0) //
    {                                                         // Maximum idle time (based on whether to automatically move the grid), if the maximum idle time MaxIdle setting is less than or equal to0
        return false;                                                           // Return false, Do not judge timeout. That is, always returnfalse Not timed out.
    }
    var now = new Date();                                                       // Get the current time object
    if (((now.getTime() - LastBusy.getTime()) / 1000) >= MaxIdle) //
    {             // Use the getTime function of the current time object to obtain the timestamp and the timestamp of LastBusy to calculate the difference.,
        // divided by1000 Calculate the number of seconds between two time objects. Determine if it is greater than the maximum idle timeMaxIdle
        LastBusy = now;                                                         // If it is greater than, update LastBusy to the current time object now
        return true;                                                            // Return true ,About to time out.
    }
    return false;                                                               // Return false Not timed out
}

function onexit() //
{                             // Cleanup function when the program exits.
    if (CancelAllWS) //
    {                          // If all pending orders are canceled upon stopping, call the cancelPending() function to cancel all pending orders
        Log("Exiting, Try to cancel all pending orders");
        cancelPending();
    }
    Log("The strategy successfully stopped");
    Log(_C(exchange.GetAccount));               // Print account position information when exiting the program.
}


function fishing(orgAccount, fishCount) //
{    // Cast a net, parameters: account information, number of casts
    setBusy();                               // Set LastBuys to the current timestamp
    var account = _C(exchange.GetAccount);   // Declare a  account  Variable, get the current account information and assign.
    Log(account);                            // Output this call fishing Account information at the start of the function.
    var InitAccount = account;               // Declare a variable InitAccount and use account Assignment. This records the initial account funds before this net casting, used to calculate floating profit and loss.
    var ticker = _C(exchange.GetTicker);     // Get market data and assign it to the declared ticker Variables
    var amount = _N(AmountOnce);             // According to the interface parameter single order quantity, use _N handle decimal places(_N Default reserved2Bits), assign to amount .
    var amountB = [amount];                  // Declare a variable called  amountB  Is an array, used amount Initialize an element
    var amountS = [amount];                  // Declare a variable called  amountS  ...
    if (typeof (AmountType) !== 'undefined' && AmountType == 1) //
    {     // According to custom amount, order size type, if this interface parameter is not undefined,
        //And AmountType Set on the interface as a custom amount, that isAmountType value is 1 (Dropdown index) 
        for (var idx = 0; idx < AllNum; idx++) //
        {      // AllNum Total quantity. If you set a custom amount, loop a certain number of times based on the total amount and assign a value to amountB/amountS, which is the buy and sell order amount array.
            amountB[idx] = BAmountOnce;               // Use interface parameters to assign values to the buy quantity array
            amountS[idx] = SAmountOnce;               // ...         Give sell order...
        }
    }//
    else //
    {                                          // Others
        for (var idx = 1; idx < AllNum; idx++) //
        {      // Loop according to the total number of grids.
            switch (AmountCoefficient[0]) //
            {           // According to the interface parameter difference, the first character of this string, that is, AmountCoefficient[0] is '+','-','*','/'
                case '+':                             // construct a grid with gradually increasing order quantity based on interface parameters.
                    amountB[idx] = amountB[idx - 1] + parseFloat(AmountCoefficient.substring(1));
                    break;
                case '-':                             // ... 
                    amountB[idx] = amountB[idx - 1] - parseFloat(AmountCoefficient.substring(1));
                    break;
                case '*':
                    amountB[idx] = amountB[idx - 1] * parseFloat(AmountCoefficient.substring(1));
                    break;
                case '/':
                    amountB[idx] = amountB[idx - 1] / parseFloat(AmountCoefficient.substring(1));
                    break;
            }
            amountB[idx] = _N(amountB[idx], AmountDot);   // Buy order, buy order quantity is the same, handle the decimal places properly.
            amountS[idx] = amountB[idx];                  // Assignment.
        }
    }
    if (FirstPriceAuto) //
    {                                 // If the interface parameter sets firstPriceAuto to true, execute the code inside the if braces.
        FirstPrice = BuyFirst ? _N(ticker.Buy - PriceGrid, Precision) : _N(ticker.Sell + PriceGrid, Precision);
        // Interface parameter  FirstPrice according to BuyFirstGlobal variable (initial declaration astrue,At/InmainStart has already based onOpTypeAssign the first price using the current market ticker And interface parameters PriceGrid Use price spacing to set. 
    }
    // Initialize fish table    initialize grid
    var fishTable = //
        {};                         // Declare a grid object
    var uuidTable = //
        {};                         // Identifier table object
    var needStocks = 0;                         // Required currency amount variable
    var needMoney = 0;                          // Required money variable
    var actualNeedMoney = 0;                    // Actual required money
    var actualNeedStocks = 0;                   // Actual required currency
    var notEnough = false;                      // Insufficient funds flag variable, initially set tofalse
    var canNum = 0;                             // available grid
    for (var idx = 0; idx < AllNum; idx++) //
    {    // Traverse and construct according to the grid number AllNum.
        var price = _N((BuyFirst ? FirstPrice - (idx * PriceGrid) : FirstPrice + (idx * PriceGrid)), Precision);
        // The current index during traversal constructionidx Set the price according to BuyFirst Go to settings. The spacing between each index price is PriceGrid .
        needStocks += amountS[idx];                      // The number of coins required to sell is gradually accumulated through the cycle. (Accumulated one by one from the array of sell orders.) needStocks)
        needMoney += price * amountB[idx];               // The money required for buying accumulates gradually with the loop.(.... Accumulate the buy order volume array one by one...)
        if (BuyFirst) //
        {                                  // handle buy first 
            if (_N(needMoney) <= _N(account.Balance)) //
            {  // If the money required for the grid is less than the available money in the account
                actualNeedMondy = needMoney;             // Assign to the actual required amount of money
                actualNeedStocks = needStocks;           // Assign to the actual required number of coins This output has some issues?
                canNum++;                                // Accumulated available grid count
            }//
            else //
            {                                     // _N(needMoney) <= _N(account.Balance) If this condition is not met, set the insufficient funds flag variable to true
                notEnough = true;
            }
        }//
        else //
        {                                         // handle sell first
            if (_N(needStocks) <= _N(account.Stocks)) //
            {  // Check if the required number of coins is less than the account's available coins
                actualNeedMondy = needMoney;             // Assignment
                actualNeedStocks = needStocks;
                canNum++;                                // Accumulated available grid count
            }//
            else //
            {
                notEnough = true;                        // If the funding condition is not met, set  true
            }
        }
        fishTable[idx] = STATE_WAIT_OPEN;                // According to the current index idx, set the status of the idx member (grid node) of the grid object, initially STATE_WAIT_OPEN (waiting to open a position)
        uuidTable[idx] = -1;                             // The numbering object is also initialized based on the current idx. Its own idx value (corresponding to the node of fishTable) is -1
    }
    if (!EnableAccountCheck && (canNum < AllNum)) //
    {      // If capital verification is not enabled, and the number of openable nodes is less than the grid quantity set in the interface parameters (total number of nodes).
        Log("Warning, Current funds can only be used for", canNum, "Number of grids, Total network requires", (BuyFirst ? needMoney : needStocks), "Please keep funds sufficient");   // Log Output warning message.
        canNum = AllNum;                                                                                          // Update the available quantity according to the interface parameter setting
    }
    if (BuyFirst) //
    {                                                                         // Buy first
        if (EnableProtectDiff && (FirstPrice - ticker.Sell) > ProtectDiff) //
        {                // Activate price difference protection and enter price minus the current sell price greater than the entry price protection
            throw "First buy price compared to market sell1high price" + _N(FirstPrice - ticker.Sell, Precision) + ' element';  // Throw error message.
        }//
        else if (EnableAccountCheck && account.Balance < _N(needMoney)) //
        {                 // If fund verification is enabled and the available amount of funds in the account is less than the amount of funds required for the grid.
            if (fishCount == 1) //
            {                                                           // If this is the first grid placement
                throw "Insufficient funds, Need" + _N(needMoney) + "element";                                // Throw error: insufficient funds
            }//
            else //
            {
                Log("Insufficient funds, Need", _N(needMoney), "element, Program only does", canNum, "Number of grids #ff0000");  // If it is not the first net casting, output a prompt message.
            }
        }//
        else //
        {                                                                            // Other cases, fund verification, price difference protection, etc. are not enabled
            Log('Expected funds to be used: ', _N(needMoney), "element");                                        // Output estimated funds required.
        }
    }//
    else //
    {                                                                                // Sell first, similar to buying first
        if (EnableProtectDiff && (ticker.Buy - FirstPrice) > ProtectDiff) //
        {
            throw "First sell price compared to market buy1high price " + _N(ticker.Buy - FirstPrice, Precision) + ' element';
        }//
        else if (EnableAccountCheck && account.Stocks < _N(needStocks)) //
        {
            if (fishCount == 1) //
            {
                throw "Insufficient coins, Need " + _N(needStocks) + " Currency";
            }//
            else //
            {
                Log("Insufficient funds, Need", _N(needStocks), "Currency, Program only does", canNum, "Number of grids #ff0000");
            }
        }//
        else //
        {
            Log('Estimated amount of coins to be used: ', _N(needStocks), "Individual/Unit, Approximately", _N(needMoney), "element");
        }
    }

    var trader = new Trader();                                          // Construct a Trader Object, assigned to the declaration here trader Variables.
    var OpenFunc = BuyFirst ? exchange.Buy : exchange.Sell;             // Set up the open position function according to whether to buy first then sellOpenFunc Is a reference exchange.Buy Still exchange.Sell
    var CoverFunc = BuyFirst ? exchange.Sell : exchange.Buy;            // Same as above
    if (EnableDynamic) //
    {                                                // Depending on whether the interface parameter EnableDynamic (whether dynamic order placement) is enabled, reset again. OpenFunc/CoverFunc
        OpenFunc = BuyFirst ? trader.Buy : trader.Sell;                 // Reference the member function Buy of the trader object for dynamic pending orders (mainly because some exchanges limit the number of pending orders, so virtual dynamic pending orders are needed)
        CoverFunc = BuyFirst ? trader.Sell : trader.Buy;                // Same as above
    }
    var ts = new Date();                                                // Create the current time object (assign tots),Used to record the current time.
    var preMsg = "";                                                    // Declare a variable to record the last information, with an initial empty string
    var profitMax = 0;                                                  // Maximum Profit 
    while (true) //
    {                                                      // Main logic after the grid is laid out
        var now = new Date();                                           // Record the time at the start of the current loop
        var table = null;                                               // Declare a variable
        if (now.getTime() - ts.getTime() > 5000) //
        {                      // Calculate whether the difference between the current time now and the recorded time ts is greater than 5000 milliseconds
            if (typeof (GetCommand) == 'function' && GetCommand() == "close the net") //
            {         // Check whether a strategy interactive control command 'Close Net' is received, stop and balance to the initial state
                Log("Start executing commands to close network operations");                                          // output information 
                balanceAccount(orgAccount, InitAccount);                              // Execute the balance function, balance the coin quantity to the initial state
                return false;                                                         // This netting function  fishing Return false
            }
            ts = now;                                                                 // update ts with current time now, for the next time comparison
            var nowAccount = _C(exchange.GetAccount);                                 // Statement nowAccount Variable initialized with the current latest account information.
            var ticker = _C(exchange.GetTicker);                                      // Statement ticker Variable, initialized with the current market information
            if (EnableDynamic) //
            {                                                      // If dynamic order placement is enabled
                trader.Poll(ticker, DynamicMax);                                      // Call trader Of the object Poll Function, based on current ticker Market and interface parameters DynamicMax(Detect and handle all orders for order invalid distance.
            }
            var amount_diff = (nowAccount.Stocks + nowAccount.FrozenStocks) - (InitAccount.Stocks + InitAccount.FrozenStocks);  // Calculate the current currency difference
            var money_diff = (nowAccount.Balance + nowAccount.FrozenBalance) - (InitAccount.Balance + InitAccount.FrozenBalance); // Calculate the current money difference
            var floatProfit = _N(money_diff + (amount_diff * ticker.Last));           // Calculate the floating profit and loss of the current cast
            var floatProfitAll = _N((nowAccount.Balance + nowAccount.FrozenBalance - orgAccount.Balance - orgAccount.FrozenBalance) + ((nowAccount.Stocks + nowAccount.FrozenStocks - orgAccount.Stocks - orgAccount.FrozenStocks) * ticker.Last));
            // Calculate the overall floating profit and loss

            var isHold = Math.abs(amount_diff) >= exchange.GetMinStock();             // If the absolute value of the currency difference at this moment is greater than the minimum trading volume of the exchange, it means that the position has been held
            if (isHold) //
            {                                                             // If already holding a position, execute the setBusy() function, which updates LastBusy time.
                setBusy();                                                            // That is, start the opening mechanism after opening a position.
            }

            profitMax = Math.max(floatProfit, profitMax);                             // Refresh maximum floating profit and loss
            if (EnableAccountCheck && EnableStopLoss) //
            {                               // If account monitoring is enabled and stop-loss is enabled
                if ((profitMax - floatProfit) >= StopLoss) //
                {                          // If maximum floating profit and loss minus current floating profit and loss is greater than or equal to the maximum floating loss, then execute the code inside the curly braces.
                    Log("Current floating profit and loss", floatProfit, "Highest profit point: ", profitMax, "Start stop-loss");   // Output Information
                    balanceAccount(orgAccount, InitAccount);                          // Balance Account
                    if (StopLossMode == 0) //
                    {                                          // is processed according to the stop loss mode. If StopLossMode is equal to 0, that is, the program exits after the stop loss.
                        throw "Stop Exit"; // throws error "Stop Exit" strategy stopped.
                    }//
                    else //
                    {
                        return true;                                                   // except for exit mode after stop-loss, i.e., re-deploy the grid after stop-loss.
                    }
                }
            }
            if (EnableAccountCheck && EnableStopWin) //
            {                                 // If account detection is enabled and take profit is enabled
                if (floatProfit > StopWin) //
                {                                           // If floating profit and loss is greater than take profit
                    Log("Current floating profit and loss", floatProfit, "Start Taking Profit");                         // Output Log
                    balanceAccount(orgAccount, InitAccount);                           // Balance account, restores initial state (take profit))
                    if (StopWinMode == 0) //
                    {                                            // Handle according to take-profit mode.
                        throw "Take profit and exit"; // Exit after taking profit
                    }//
                    else //
                    {
                        return true;                                                    // Return after take profit true , Continue Casting Net
                    }
                }
            }
            var distance = 0;                                                           // Declare a variable to record the distance
            if (EnableAccountCheck && AutoMove) //
            {                                       // If account checking is enabled and the grid moves automatically
                if (BuyFirst) //
                {                                                         // If it is buy first, then sell 
                    distance = ticker.Last - FirstPrice;                                // Assign a value to distance: subtract the first price from the current price to calculate the distance 
                }//
                else //
                {                                                                // Other situations: sell first then buy
                    distance = FirstPrice - ticker.Last;                                // Assign a value to distance: Initial price minus current price to calculate distance
                }
                var refish = false;                                                     // Flag variable for whether to cast the net again
                if (!isHold && isTimeout()) //
                {                                           // If there is no position (isHold is false) and timeout occurs (isTimeout returns true)
                    Log("Empty position for too long, Start moving the mesh");
                    refish = true;                                                      // Mark for re-netting 
                }
                if (distance > MaxDistance) //
                {                                           // If the current distance is greater than the maximum distance set by the interface parameters, mark the net again.
                    Log("Prices exceed the grid range by too much, Start moving the mesh, Current distance: ", _N(distance, Precision), "Current Price:", ticker.Last);
                    refish = true;
                }
                if (refish) //
                {                                                           // If refish is true, the balance function is executed 
                    balanceAccount(orgAccount, InitAccount);
                    return true;                                                        // This net-casting function returns true
                }
            }

            var holdDirection, holdAmount = "--",                                       // Declaration Three variables: position direction, position quantity, and position price
                holdPrice = "--";
            if (isHold) //
            {                                                               // While holding position
                if (RestoreProfit && ProfitAsOrg) //
                {                                     // if 'restore last profit' is enabled and last profit is included in the average price
                    if (BuyFirst) //
                    {                                                     // If buying first then selling 
                        money_diff += LastProfit;                                       // Add the last profit money_diff ,That is, the last profit is converted into the money difference (in the case of buying first, the money difference is negative, that is, it is spent), and is converted into the cost of opening a position.
                    }//
                    else //
                    {                                                            // If selling first then buying
                        money_diff -= LastProfit;                                       // Sell first then buy, money difference is positive , why - ?
                    }
                }

                // Handle buy first then sell
                holdAmount = amount_diff;                                               // Assign the currency difference to the position quantity (at this moment the currency difference equals the position))
                holdPrice = (-money_diff) / amount_diff;                                // Use money difference divided by coin difference to calculate the average holding price, 
                // Note: if money_diff is negative, thenamount_diff Must be positive, so it must be in money_diff Add a negative sign in front, this way the calculated price is positive
                // Handle sell first then buy
                if (!BuyFirst) //
                {                                                        // If it is Sell First, Buy later, it triggers updates to Open Interest and Average Open Interest Price
                    holdAmount = -amount_diff;                                          // The currency difference is negative, so take the opposite
                    holdPrice = (money_diff) / -amount_diff;                            // Calculate average position price.
                }
                holdAmount = _N(holdAmount, 4);                                         // Position size, keep 4 decimal places.
                holdPrice = _N(holdPrice, Precision);                                   // Position average price, keep Precision decimal places.
                holdDirection = BuyFirst ? "Long" : "Short"; // According to buy first and then sell or sell first and then buy, assign the value long or short to holdDirection
            }//
            else //
            {                                                                    // If isHold is false, assign a value to holdDirection "--"
                holdDirection = "--";
            }
            table = //
            {                                                                   // Assign an object to the declared table variable, which is used to display table information on the status bar of the inventor quantification robot.
                type: 'table',                                                          // For details, please refer to the API document LogStatus function. Here, the type attribute is initialized to 'table' for displaying a table in the status bar.
                title: 'Running status', // Title of the table
                cols: ['Use funds', 'Position held', 'Position size', 'Average position price', 'Total floating profit and loss', 'Current grid profit and loss', 'Number of net casts', 'Grid offset', 'Real order', 'Latest currency price'], // Column names of the table
                rows: [                                                                                                                   // Row-by-row data of the table
                    [_N(actualNeedMondy, 4), holdDirection, holdAmount, holdPrice, _N(floatProfitAll, 4) + ' ( ' + _N(floatProfitAll * 100 / actualNeedMondy, 4) + ' % )', floatProfit, fishCount, (AutoMove && distance > 0) ? ((BuyFirst ? "upward" : "downward") + "deviation: " + _N(distance) + " element") : "--", trader.RealLen(), ticker.Last]
                    // One Line of Data
                ]
            };

        }                                                                               // Process some tasks every 5 seconds and update the robot status bar table object table 

        var orders = _C(trader.GetOrders);                                              // Get all unfinished orders
        if (table) //
        {                                                                    // If the table has already been assigned a table object
            if (!EnableDynamic) //
            {                                                       // If dynamic orders are not enabled
                table.rows[0][8] = orders.length;                                       // In the status bar table, first row, column9Column position, update the length of the order array
            }
            LogStatus('`' + JSON.stringify(table) + '`');                               // Call the inventor's quantification platform API LogStatus Display the set status bar table
        }
        for (var idx = 0; idx < canNum; idx++) //
        {                                        // Iterate over the number of available grid nodes.
            var openPrice = _N((BuyFirst ? FirstPrice - (idx * PriceGrid) : FirstPrice + (idx * PriceGrid)), Precision);        // Along with the node index idx traverse and construct the opening price for each node (the direction is determined by buy then sell, or sell first then buy).) 
            var coverPrice = _N((BuyFirst ? openPrice + PriceDiff : openPrice - PriceDiff), Precision);     // Opening and closing price difference, i.e., profit margin at each node
            var state = fishTable[idx];                                                                     // Assign the state of the fishing net node
            var fishId = uuidTable[idx];                                                                    // Number

            // The purpose of this judgment is: to filter unfinished orders
            if (hasOrder(orders, fishId)) //
            {                                                                 // If there are all uncompleted orders, that is, there is an order with ID fishId in the pending order array
                continue;                                                                                   // Skip this loop and continue looping
            }

            if (fishId != -1 && IsSupportGetOrder) //
            {                                                        // Grid node id is not equal to the initial value, meaning an order has been placed, and the exchange supports it GetOrder
                var order = trader.GetOrder(fishId);                                                        // Get This fishId order number
                // The judgment function here is: filter the grid nodes where the order is not found, the following judgment is made(state == STATE_WAIT_COVER) Logic like etc. will not be triggered
                if (!order) //
                {                                                                               // If !order is true, that is, order retrieval failed 
                    Log("Failed to get order information, ID: ", fishId);                                                     // Output Log
                    continue;                                                                               // Skip this iteration and continue the loop
                }
                // The judgment function here is to: filter grid nodes that are in a pending state, have not been completed, or have not been fully completed. The following judgments are made:(state == STATE_WAIT_COVER) Logic like etc. will not be triggered
                if (order.Status == ORDER_STATE_PENDING) //
                {                                                  // If the order status is pending on the exchange
                    //Log("Order status is not completed, ID: ", fishId);
                    continue;                                                                               // Skip this iteration and continue the loop
                }
            }

            if (state == STATE_WAIT_COVER) //
            {                                                                // If the current node status is waiting to close a position
                var coverId = CoverFunc(coverPrice, (BuyFirst ? amountS[idx] : amountB[idx]), (BuyFirst ? 'Buy order completed:' : 'Sell order completed:'), openPrice, 'Amount:', (BuyFirst ? amountB[idx] : amountS[idx]));
                // Call the close position function CoverFunc Place close order

                if (typeof (coverId) === 'number' || typeof (coverId) === 'string') //
                {        // Determine if the Id returned by the closing function is a numerical value (returned directly by the inventor's quantification API) or a string (returned by the Buy/Sell function of the trader object)
                    fishTable[idx] = STATE_WAIT_CLOSE;                                     // The closing order has been placed, and the updated status is: STATE_WAIT_CLOSE, which means waiting for the node task to be completed.
                    uuidTable[idx] = coverId;                                              // Store the order number in the idx position corresponding to uuidTable.
                }
            }//
            else if (state == STATE_WAIT_OPEN || state == STATE_WAIT_CLOSE) //
            {            // If the status is waiting to open or waiting to complete
                var openId = OpenFunc(openPrice, BuyFirst ? amountB[idx] : amountS[idx]);  // Next Open Order.
                if (typeof (openId) === 'number' || typeof (openId) === 'string') //
                {          // Determine whether the order was successful
                    fishTable[idx] = STATE_WAIT_COVER;                                     // Update status to waiting for closing
                    uuidTable[idx] = openId;                                               // Record current node orderID
                    if (state == STATE_WAIT_CLOSE) //
                    {                                       // If waiting for completion (will only trigger after the open order is placed))
                        ProfitCount++;                                                     // Cumulative profit count
                        var account = _C(exchange.GetAccount);                             // Get current account information
                        var ticker = _C(exchange.GetTicker);                               // Get current market information
                        var initNet = _N(((InitAccount.Stocks + InitAccount.FrozenStocks) * ticker.Buy) + InitAccount.Balance + InitAccount.FrozenBalance, 8);
                        // Calculate initial asset net value
                        var nowNet = _N(((account.Stocks + account.FrozenStocks) * ticker.Buy) + account.Balance + account.FrozenBalance, 8);
                        // Calculate current asset net value
                        var actualProfit = _N(((nowNet - initNet)) * 100 / initNet, 8);    // Calculate return rate
                        if (AmountType == 0) //
                        {                                             // Handle differently according to equal buy/sell quantity and custom quantity.
                            var profit = _N((ProfitCount * amount * PriceDiff) + LastProfit, 8);      // Calculation: The sum of the profits and losses of all profitable nodes and the last net casting profit and loss is the total profit and loss
                            Log((BuyFirst ? 'Sell order completed:' : 'Buy order completed:'), coverPrice, 'Amount:', (BuyFirst ? amountS[idx] : amountB[idx]), 'Closing Profit', profit);
                            // Output order completion information
                        }//
                        else //
                        {
                            Log((BuyFirst ? 'Sell order completed:' : 'Buy order completed:'), coverPrice, 'Amount:', (BuyFirst ? amountS[idx] : amountB[idx]));
                        }
                    }
                }
            }
        }
        Sleep(CheckInterval);                        // Grid logic mainly uses while loop detection, pausing for a certain period of time each time CheckInterval, that is: detection interval
    }
    return true;                                     // This netting completed return true
}

function main() //
{                                    // Main strategy function, the program starts execution from here.
    if (ResetData) //
    {                                 // RestData are interface parameters, default is true, controls whether all data is cleared at startup. By default, all data is cleared.
        LogProfitReset();                            // Execute the API LogProfitReset function to clear all earnings.
        LogReset();                                  // Execute API LogReset function to clear all logs.
    }
    // exchange.SetMaxDigits(Precision)              // Deprecated,Use exchange.SetPrecision instead.
    exchange.SetPrecision(Precision, 3)              // exchange.SetPrecision(2, 3); // Set price decimal precision to2bit, Decimal precision of order quantity for the product3bit
    // Precision as interface parameter.

    if (typeof (AmountType) === 'undefined') //
    {        // Order quantity type, 0: "Buy and sell the same amount", 1: "Customized amount", detection If this parameter is undefined, the default setting 0 .
        AmountType = 0;                              // typeof Will detect the type of AmountType. If it is undefined, that is, "undefined", assign a value to AmountType. 0.
    }
    if (typeof (AmountDot) === 'undefined') //
    {         // Order quantity Maximum number of decimal digits AmountDot If it is undefined, set AmountDot to 3 .
        AmountDot = 3;                               // actually already by exchange.SetPrecision(Precision, 3) Already set, will be truncated at the lower level.
    }
    if (typeof (EnableDynamic) === 'undefined') //
    {     // Check whether the dynamic pending order parameter is enabled. If EnableDynamic is undefined, set it to false, that is, it will not be enabled.
        EnableDynamic = false;
    }
    if (typeof (AmountCoefficient) === 'undefined') //
    { // If undefined, set default   "*1"
        AmountCoefficient = "*1";
    }
    if (typeof (EnableAccountCheck) === 'undefined') //
    {// If undefined, enable the fund verification parameter set to true, i.e., turned on.
        EnableAccountCheck = true;
    }
    BuyFirst = (OpType == 0);                        // According to the setting of OpType, assign a value to BuyFirst. OpType sets the grid type. 0: Buy first and then sell. 1: Sell first and then buy.
    IsSupportGetOrder = exchange.GetName().indexOf('itstamp') == -1;    // Detect the exchange name, if it is  Bitstamp  Then remind
    if (!IsSupportGetOrder) //
    {
        Log(exchange.GetName(), "Not SupportedGetOrder, May affect strategy stability.");
    }

    SetErrorFilter("502:|503:|S_U_001|unexpected|network|timeout|WSARecv|Connect|GetAddr|no such|reset|http|received|refused|EOF|When");
    // SetErrorFilter  Filter error messages  

    exchange.SetRate(1);
    Log('Exchange rate conversion has been disabled, Current currency is', exchange.GetBaseCurrency());    // Disable exchange rate conversion

    if (!RestoreProfit) //
    {     //  Restore the last profit. If it is false, assign LastProfit 0, meaning it will not be restored.
        LastProfit = 0;
    }

    var orgAccount = _C(exchange.GetAccount);     // Obtain account information. The initial account information when the strategy starts running is recorded here, which is used to calculate some returns, such as: overall floating profit and loss, etc. This strategy has several parameters, all of which are passed in through this variable.
    var fishCount = 1;                            // Initial netting times1
    while (true) //
    {                                // Strategy main loop
        if (!fishing(orgAccount, fishCount)) //
        {    // Net Casting Function fishing
            break;
        }
        fishCount++;                              // Accumulated netting times
        Log("No.", fishCount, "Recast net next time...");      // Output netting information.
        FirstPriceAuto = true;                    // Reset initial price automatically totrue
        Sleep(1000);                              // Polling interval 1000 milliseconds
    }
}
```

> Detail

https://www.fmz.com/strategy/311968

> Last Modified

2021-09-03 14:37:13
