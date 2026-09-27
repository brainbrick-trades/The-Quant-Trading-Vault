
> Name

TradingView-Order-Robot-11

> Author

夏天不打你

> Strategy Description

**For personal useTradingviewOrder bot, with the following functions:**
1,Supports ordering Huobi, OKEx, and Binance's coin-margined quarterly contracts and USDT perpetual contracts.
2,Supports simple interest mode and compound interest mode.
3,Supports counterparty-limited slippage orders and market orders.
4,supports multithreaded concurrent ordering.
5,Comprehensive data statistics.
6,All data supports local saving and recovery.

**This order bot needs to be used in conjunction with the server; download link:**
Link:https://pan.baidu.com/s/1RK08Ht4cAOAwTSb6X2TA4A 
Extraction code:3qo6 

**Usage:**
TVTerminal command sending method:
order_message2 = 'TradingView:order:ticker=OKEX:ETHUSDT' + ' levelRate=' + tostring(level_rate) + ' price=' + tostring(order_price) + ' size=' + tostring(order_size) + ' type=1' + ' robot=' + tostring(order_robot)
strategy.entry(id = "long", long = true, comment="go long", alert_message = order_message2)
levelRaterepresents the leverage ratio, price represents the price, and size represents the number of orders placed. order_robot represents the robot number above the inventor.
Mainly pay attention to the value of type, 1 means open long, 2 means open short, 3 means close long, 4 means close short, 5 means close long open short, 6 means close short open long.
The above code is **inserted into the TV strategy script** where an order needs to be placed.

Create alerts in policy,webhookFill in the address: the server running the serviceIPAddress, fill in message:{{strategy.order.alert_message}},Other parameters can be defaulted.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Interval|1000|(?Basic settings) program running cycle(ms)|
|Currency|ETH_USDT|trading pair|
|MarginLevel|4|Leverage multiple|
|IsUseHuobiOrder|false|Huobi perpetual USDT order|
|IsUseBinanceOrder|true|Whether to place an order on Binance perpetual USDT|
|UseQuarter|false|Quarterly Contract|
|IsMarketOrder|true|Market Order|
|UseOrderSync|false|(?Advanced settings) Use multithreading for order placement|
|UseOpponentOrder|false|Place order using counterparty|
|OpponentSlip|0.01|Counterparty order slippage|
|OpponentOrderTime|600|Maximum order time for opponent's orders(s)|
|UseSameTicker|false|Use the same order to trade|
|InitAsset|1,2,3,4,5,6,7,8,9,10|Initial Assets|
|OrderSize|1,2,3,4,5,6,7,8,9,10|Order Quantity|
|UseMutiOrderSize|false|Place orders using different quantities (fixed number of lots))|
|UseAutoAdjustOrderSize|false|Automatically calculate the number of orders placed|
|ThePercentOfAssetToOrder|0.5|Percentage of funds occupied by the order funds|
|UseAllInOrder|false|Full position mode (compounding))|
|UseLimitMaxOrderAmount|false|Whether to limit the order amount|
|LimitMaxOrderAmount|1400|Maximum order amount(USDT)|
|EnablePlot|true|Open Charting|
|KPeriod|60|candlestick period for drawing(min)|
|PricePrecision|5|(?Order settings) Order price precision|
|AmountPrecision|false|Order quantity precision|
|OneSizeInCurrentCoin|true|UIn a standard contract, the amount of currency represented by one lot|
|QuarterOneSizeValue|10|In the currency-based contract, the amount of USDT represented by one piece|
|UseAutoTransfer|true|(?Auto transfer) Use auto transfer|
|UseCertainAmountTransfer|true|Fixed Transfer|
|AccountMaxBalance|1100|Automatically remove when available assets exceed *U100U|
|UseProfitToTransfer|false|Transfer according to profit situation (double transfer))|
|ProfitPercentToTransfer|90|Percentage of profit to transfer for doubling|




|Button|Default|Description|
|----|----|----|
|LogPrint|Fixed some bugs. | Output logs|
|SaveLocalData|false|Save data locally|
|ClearLocalData|-1|Clear local data|
|ClearLog|true|Clear log information|
|LogStatusRefreshTime|5|Status bar update interval (seconds).)|
|SetStrategyRunTime|1627747200|Set strategy start timestamp (seconds))|
|SetUserStartTime|0,1627747200|Set user start time|
|SetUserInitAsset|0,1000|Set user initial assets|
|AdjustOrderSize|-1|Automatically adjust the number of single sheets|
|ManualOrder|-1,longopen,1|Manual Order|


> Source (javascript)

``` javascript

/*
Order Robot1.1
Version: 1.1
Author: summer
Date: 2021.9.9
Add:
1,Place orders with different quantities for multiple accounts
2,The opponent's order limit slippage (the market price will still be flat when closing the position))
3,Quarterly contract backtest statistics
4,Multi-account profit and loss statistics
5,Localization of account data
6,Status information table display
7,Multi-threaded order placement
8,Added manual order interaction
9,Fix issues with incorrect profit statistics
*/

// Order Settings
var _PricePrecision = PricePrecision;                           // Order price accuracy
var _AmountPrecision = AmountPrecision;                         // Order quantity precision
var _OneSizeInCurrentCoin = OneSizeInCurrentCoin;               // UIn the standard contract, oneETHRepresentsETHQuantity
var _QuarterOneSizeValue = QuarterOneSizeValue;                 // One coin-margined contractETHRepresentsUSDTQuantity
// Auto Transfer
var _UseAutoTransfer = UseAutoTransfer;                         // Use automatic transfer
var _UseCertainAmountTransfer = UseCertainAmountTransfer;       // Fixed Transfer
var _AccountMaxBalance = AccountMaxBalance;                     // Automatically remove when available assets exceed *U100U
var _UseProfitToTransfer = UseProfitToTransfer;                 // Transfer according to profit situation (double transfer))
var _ProfitPercentToTransfer = ProfitPercentToTransfer          // Percentage of profit to transfer for doubling

var _OKCoin = "Futures_OKCoin";
var _QuantitativeOrderHeader = "Quantitative:order:";
var _OrderSize = [];
var _InitAsset = [];
var _Accounts = [];
var _Positions = [];

var ProfitLocal = [];
var TotalAsset = [];
var TakeProfitCount = [];
var StopLossCount = [];
var WinRate = [];
var MaxLoss = [];
var MaxLossPercent = [];
var MaxProfit = [];
var MaxProfitPercent = [];
var ProfitPercent = [];
var _TransferAmount = [];
var _CurrentInitAssets = [];
var UserStartTime = [];
var UserDatas = [];
var StrategyRunTimeStampString = "strategy_run_time";
var StrategyDatas = { start_run_timestamp: 0, others: "" };

var _ClosePrice = 0;
var _MarginLevel = MarginLevel;

var _TradingFee = 0.0005;
var _RemainingSize = 20;            // In cross-margin mode, after calculating the maximum number of orders that can be placed, the number of free lots that need to be made available to avoid order failure due to large fluctuations
var _IsOpponentOrder = false;

var _LogStatusRefreshTime = 10;     // Status bar update period s
var _LastBarTime = 0;               // LatestKLine Time

// Save the program's start running time in seconds timestamp
function saveStrategyRunTime() {
    var local_data_strategy_run_time = _G(StrategyRunTimeStampString);

    if (local_data_strategy_run_time == null) {
        StrategyDatas.start_run_timestamp = Unix();
        _G(StrategyRunTimeStampString, StrategyDatas.start_run_timestamp);
    }
    else {
        StrategyDatas.start_run_timestamp = local_data_strategy_run_time;
    }
}

// Set the program's start running time in seconds timestamp
function setStrategyRunTime(timestamp) {
    _G(StrategyRunTimeStampString, timestamp);
    StrategyDatas.start_run_timestamp = timestamp;
}

// Calculate the number of days between two timestamps, the parameter is a second-level timestamp
function getDaysFromTimeStamp(start_time, end_time) {
    if (end_time < start_time)
        return 0;

    return Math.trunc((end_time - start_time) / (60 * 60 * 24));
}

function saveUserDatasLocal() {
    // Save the transaction statistics locally and click the interactive button to run
    // Before saving data, first put itUserDataData Reset
    UserDatas = null;
    UserDatas = new Array();

    for (var i = 0; i < exchanges.length; i++) {
        // Put the data intoUserData
        UserDatas.push({
            init_assets: _InitAsset[i],
            profit_local: ProfitLocal[i],
            max_profit_percent: MaxProfitPercent[i],
            max_loss_percent: MaxLossPercent[i],
            max_profit: MaxProfit[i],
            max_loss: MaxLoss[i],
            take_profit_count: TakeProfitCount[i],
            stop_loss_count: StopLossCount[i],
            start_time: UserStartTime[i], order_size: _OrderSize[i],
            transfer_amount: _TransferAmount[i],
            current_init_assets: _CurrentInitAssets[i]
        });
        // Save to local
        _G(exchanges[i].GetLabel(), UserDatas[i]);
    }
    Log("All account data has been saved locally.");
}

function readUserDataLocal(num) {
    // Read the user's local data and run it once when the program starts
    // Fixed hereUserDataThe correspondence with the account, that is, fixedUserDataLength of
    var user_data = _G(exchanges[num].GetLabel());
    if (user_data == null) {
        UserDatas.push({
            init_assets: 0,
            profit_local: 0,
            max_profit_percent: 0,
            max_loss_percent: 0,
            max_profit: 0,
            max_loss: 0,
            take_profit_count: 0,
            stop_loss_count: 0,
            start_time: Unix(),
            order_size: 0,
            transfer_amount: 0,
            current_init_assets: 0
        });
        // Log(exchanges[num].GetLabel(), ":No local data.");
    } else {
        UserDatas.push(user_data);
        // Log(exchanges[num].GetLabel(), ":Successfully read data from local.");
    }
}

function isHadLocalData(num) {
    if (_G(exchanges[num].GetLabel()) == null)
        return false;
    return true;
}

function clearUserDataLocal(num) {
    // Clear the user's local data, run by clicking the interactive button
    if (num == -1) {
        _G(null);
        Log("has cleared all local data.");
    } else {
        _G(exchanges[num].GetLabel(), null);
        Log(exchanges[num].GetLabel(), ":Local data cleared.");
    }
}

function resetPosition(num) {
    // Reset_Position
    _Positions[num].avg_cost = 0;
    _Positions[num].direction = "short";
    _Positions[num].size = 0;
    _Positions[num].order_count = 0;
}

function orderInBacktest(direction, price, size)
{
    for (var i = 0; i < exchanges.length; i++) {
        _Positions[i].avg_cost = price[i];
        _Positions[i].direction = direction;
        _Positions[i].size = size[i];
        _Positions[i].order_count = 1;
    }

    var t_direction = direction == "long" ? "go long" : "go short";
    Log("Place Order:", t_direction, ", Opening price:", price[0], ", Number of Open Positions:", size[0], "@");
}

// Auto Remove
function autoTransfer() {
    var transfer_amount = 100;
    var account = [];
    var had_transfer = false;
    for (let i = 0; i < exchanges.length; i++) {
        if (!isBinanceExchange(i)) {
            continue;
        }
        account[i] = _C(exchanges[i].GetAccount);
        if (_UseAutoTransfer) {
            if (_UseCertainAmountTransfer) {
                if (account[i].Balance > _AccountMaxBalance) {
                    if (transferToMain(transfer_amount, i)) {
                        _TransferAmount[i] += transfer_amount;
                        had_transfer = true;
                    }
                }
            } else if (_UseProfitToTransfer) {
                _CurrentInitAssets[i] = _CurrentInitAssets[i] == 0 ? _InitAsset[i] : _CurrentInitAssets[i];
                // Based on available account balance - Calculate current profit based on current actual initial assets
                var current_profit = account[i].Balance - _CurrentInitAssets[i];
                if (current_profit > _CurrentInitAssets[i]) {
                    transfer_amount = _N(current_profit * _ProfitPercentToTransfer, 0);
                    if (transferToMain(transfer_amount, i)) {
                        _TransferAmount[i] += transfer_amount;
                        _CurrentInitAssets[i] = account[i].Balance - transfer_amount;     // Account available balance - withdrawn amount = current initial assets
                        had_transfer = true;
                    }
                }
            }
        }
    }
    if (had_transfer) {
        saveUserDatasLocal();
    }
}

// fromUTransfer the specified amount from the contract wallet to the spot walletUSDT
function transferToMain(amount, num){
    var time = UnixNano() / 1000000;
    var param = "type=UMFUTURE_MAIN" + "&asset=USDT" + "&amount=" + amount.toString() + "&timestamp=" + time.toString();
    exchanges[num].SetBase('https://api.binance.com');
    var ret = exchanges[num].IO("api", "POST", "/sapi/v1/asset/transfer", param);
    exchanges[num].SetBase('https://fapi.binance.com');
    if (ret) {
        Log(exchanges[num].GetLabel(), ":Already fromUTransfer from base wallet to spot wallet: ", amount, " USDT");
        return true;
    } else {
        Log(exchanges[num].GetLabel(), ":Fund transfer failed");
        return false;
    }
}

function coverInBacktest(close_price, level_rate, print_data) {
    // Cumulative Profit and Loss
    var after_fee_profit = [];
    var asset_used = [];

    for (var i = 0; i < _Positions.length; i++) {
        if (_Positions[i].size == 0)
            continue;

        // Current total earnings - Last total profit = Earnings this time
        // getPositionSize(i, true);   // Force update position information first
        after_fee_profit[i] = (getAccountAsset(i, close_price[i]) + _TransferAmount[i] - _InitAsset[i]) - ProfitLocal[i];
        ProfitLocal[i] += after_fee_profit[i];

        // Calculate correct occupied assets for opening orders
        if (UseAllInOrder) {
            asset_used[i] = _InitAsset[i];
        } else {
            asset_used[i] = UseQuarter ? (_OrderSize[i] * _QuarterOneSizeValue / level_rate)
                                        : ((close_price[i] * _OneSizeInCurrentCoin / level_rate) * _OrderSize[i]);
        }

        // Calculate Win Rate
        if (after_fee_profit[i] > 0) {
            TakeProfitCount[i]++;
            var take_profit_percent = _N(after_fee_profit[i] / asset_used[i], 4);
            if (take_profit_percent > MaxProfitPercent[i]) {
                //Record the largest single profit
                MaxProfit[i] = after_fee_profit[i];
                MaxProfitPercent[i] = take_profit_percent;
            }
        } else {
            StopLossCount[i]++;
            var stop_loss_percnet = _N(after_fee_profit[i] / asset_used[i], 4);
            if (stop_loss_percnet < MaxLossPercent[i]) {
                // Record the largest single loss
                MaxLoss[i] = after_fee_profit[i];
                MaxLossPercent[i] = stop_loss_percnet;
            }
        }
        // Calculate asset balance and win rate
        TotalAsset[i] += after_fee_profit[i];
        WinRate[i] = TakeProfitCount[i] / (TakeProfitCount[i] + StopLossCount[i]);
        ProfitPercent[i] = ProfitLocal[i] / asset_used[i];
        // Print Information
        if (i == 0) {
            if (UseQuarter) {
                // Quarterly coin-margined contract
                // Log("Closing Price:", close_price[i], ", Single Trade Profit and Loss:", _N(after_fee_profit[i], 4), ", Overall Profit and Loss:", ProfitLocal[i], ", Win rate:", (WinRate[i] * 100), "%",
                   //  "; Account Balance:", TotalAsset[i], "; Profit and loss percentage:", (_N(ProfitPercent[i], 4) * 100), "%");
                // Log("Maximum profit per transaction:", MaxProfit[i], ", ", (_N(MaxProfitPercent[i], 4) * 100), "%", ", Maximum loss per transaction:", MaxLoss[i], ", ", (_N(MaxLossPercent[i], 4) * 100), "%",
                   //  ", Total number of trades:", (TakeProfitCount[i] + StopLossCount[i]), ", Number of Wins:", TakeProfitCount[i]);
                // Log(print_data, "@");
                LogProfit(ProfitLocal[i], "          Current Profit:", _N(after_fee_profit[i], 4));
            } else {
                // perpetualUSDTcontract
                // Log("Closing Price:", close_price[i], ", Single Trade Profit and Loss:", _N(after_fee_profit[i], 2), ", Overall Profit and Loss:", _N(ProfitLocal[i], 2), ", Win rate:", (_N(WinRate[i], 4) * 100), "%",
                   //  "; Account Balance:", _N(TotalAsset[i], 2), "; Profit and loss percentage:", (_N(ProfitPercent[i], 4) * 100), "%");
                // Log("Maximum profit per transaction:", _N(MaxProfit[i], 2), ", ", (_N(MaxProfitPercent[i], 4) * 100), "%", ", Maximum loss per transaction:", _N(MaxLoss[i], 2), ", ", (_N(MaxLossPercent[i], 4) * 100), "%",
                   //  ", Total number of trades:", (TakeProfitCount[i] + StopLossCount[i]), ", Number of Wins:", TakeProfitCount[i]);
                // Log(print_data, "@");
                LogProfit(ProfitLocal[i], "          Current Profit:", _N(after_fee_profit[i], 4));
            }
        } else {
            if (UseQuarter) {
                // Quarterly coin-margined contract
                Log(exchanges[i].GetLabel(), "Single Trade Profit and Loss: ", _N(after_fee_profit[i], 4), "; Overall Profit and Loss:", ProfitLocal[i], "; Account Balance:", TotalAsset[i], "; Profit and loss percentage:", (_N(ProfitPercent[i], 4) * 100), "%");
            } else {
                // perpetualUSDTcontract
                Log(exchanges[i].GetLabel(), "Single Trade Profit and Loss: ", _N(after_fee_profit[i], 2), "; Overall Profit and Loss:", _N(ProfitLocal[i], 2), "; Account Balance:", _N(TotalAsset[i], 2), "; Profit and loss percentage:", (_N(ProfitPercent[i], 4) * 100), "%");
            }
        }
    }

    // Save data locally
    saveUserDatasLocal();
    // Reset_Position
    for (var j = 0; j < _Positions.length; j++)
        resetPosition(j);

}

function resetAccountInfo(num) {
    _Accounts[num].balance = 0;
    _Accounts[num].frozen_balance = 0;
    _Accounts[num].stocks = 0;
    _Accounts[num].frozen_stocks = 0;
    _Accounts[num].max_order_size = 0;
}

function getPositionAsset(num, price) {
    var position_asset = 0;

    if (UseQuarter) {
        position_asset = _Positions[num].size * _QuarterOneSizeValue / price / _MarginLevel;
    } else {
        position_asset = _Positions[num].size * _OneSizeInCurrentCoin * price / _MarginLevel;
    }
    // Log("Account", num, "Held Assets:", position_asset);
    return position_asset;
}

function getAccountAsset(num, price) {
    // Calculate the initial assets of the account under different situations
    var account_asset = 0;
    // var position_profit = 0;
    if (UseQuarter) {
        if (_Positions[num].size != 0) {
            var position_stocks = getPositionAsset(num, price);
            // position_profit = _Positions[num].direction == "long" ? ((price - _Positions[num].avg_cost) / price) * _MarginLevel * position_stocks : ((_Positions[num].avg_cost - price) / price) * _MarginLevel * position_stocks;
            account_asset = _Accounts[num].stocks + _Accounts[num].frozen_stocks + position_stocks;
        }
        else {
            account_asset = _Accounts[num].stocks + _Accounts[num].frozen_stocks;
        }
    } else {
        if (_Positions[num].size != 0) {
            var position_balance = getPositionAsset(num, price);
            // position_profit = _Positions[num].direction == "long" ? ((price - _Positions[num].avg_cost) / price) * _MarginLevel * position_balance : ((_Positions[num].avg_cost - price) / price) * _MarginLevel * position_balance;
            account_asset = _Accounts[num].balance + _Accounts[num].frozen_balance + position_balance;
        } else {
            account_asset = _Accounts[num].balance + _Accounts[num].frozen_balance;
        }
    }
    // Log("Account", num, "Asset:", account_asset);
    return account_asset;
}

function refreshPosition(position, num) {
    if (position) {
        _Positions[num].avg_cost = position.Price;
        _Positions[num].direction = position.Type == PD_LONG ? "long" : "short";
        if (IsUseBinanceOrder)
            _Positions[num].size = position.Amount / _OneSizeInCurrentCoin;
        else
            _Positions[num].size = position.Amount;
    } else {
        resetPosition(num);
    }
}

function getMaxOrderSize(margin_level, ticker, account) {
    var max_order_size = 0;
    if (UseQuarter)
        max_order_size = account.Stocks * ticker.Last / _QuarterOneSizeValue * margin_level;
    else
        max_order_size = account.Balance * margin_level / (ticker.Last * _OneSizeInCurrentCoin);
    // Log("Current Account", num, "The maximum number of orders that can be placed is:", max_order_size);
    return Math.trunc(max_order_size);
}

function refreshAccountInfo(ticker, num) {
    var account = exchanges[num].GetAccount();
    if (ticker && account) {
        var max_order_size = 0;
        if (UseQuarter)
            max_order_size = account.Stocks * ticker.Last / _QuarterOneSizeValue * _MarginLevel;
        else
            max_order_size = account.Balance * _MarginLevel / (ticker.Last * _OneSizeInCurrentCoin);

        _Accounts[num].balance = account.Balance;
        _Accounts[num].frozen_balance = account.FrozenBalance;
        _Accounts[num].stocks = account.Stocks;
        _Accounts[num].frozen_stocks = account.FrozenStocks;
        _Accounts[num].max_order_size = Math.trunc(max_order_size);

        return 0;
    } else {
        return -1;
    }
}

function getPositionSize(num, enforce) {
    var position_size = 0;
    var position = null;
    if (enforce) {
        position = _C(exchanges[num].GetPosition);
    } else {
        position = exchanges[num].GetPosition();
    }
    if (position == null)
        return 0;

    if (position.length == 1) {
        if (IsUseBinanceOrder)
            position_size = position[0].Amount / _OneSizeInCurrentCoin;
        else
            position_size = position[0].Amount;
        if (position[0].Type == PD_SHORT)
            position_size = -1 * position_size;
        refreshPosition(position[0], num);
        return position_size;
    }

    return 0;
}

function cancelAllPendingOrders() {
    for (var i = 0; i < exchanges.length; i++) {
        var orders = exchanges[i].GetOrders();
        for (var j = 0; j < orders.length; j++) {
            exchanges[i].CancelOrder(orders[j].Id, orders[j]);
        }
        if (orders.length > 0)
            Log(exchanges[i].GetLabel(), ":Unfilled orders have been canceled!", "@");
    }
}

function calculateRealOrderSize(direction, max_order_size, position_size, order_size, num) {
    var real_order_size = 0;

    if (IsUseBinanceOrder) {
        // Binance Futures PerpetualUSDTIn contracts, the order unit is the number of coins, not lots
        if (UseAllInOrder) {
            // Cross Margin Mode
            if (direction == "buy" || direction == "sell") {
                real_order_size = max_order_size * _OneSizeInCurrentCoin;
            } else {
                real_order_size = Math.abs(position_size * _OneSizeInCurrentCoin);
            }
        } else {
            // Non-full position mode
            if (direction == "buy" || direction == "sell")
                real_order_size = UseMutiOrderSize ? _OrderSize[num] * _OneSizeInCurrentCoin : order_size * _OneSizeInCurrentCoin;
            else
                real_order_size = Math.abs(position_size * _OneSizeInCurrentCoin);
        }
    }
    else {
        // Place an order for non-Binance accounts, unit: lots
        if (UseAllInOrder) {
            // Cross Margin Mode
            if (direction == "buy" || direction == "sell") {
                // Open Position
                real_order_size = max_order_size;
            } else {
                // Close Position
                real_order_size = Math.abs(position_size);
            }
        } else {
            // Non-full position mode
            if (direction == "buy" || direction == "sell")
                real_order_size = UseMutiOrderSize ? _OrderSize[num] : order_size;
            else
                real_order_size = Math.abs(position_size);
        }
    }

    return real_order_size;
}

function calculateRealOrderPrice(direction, order_base_price, is_market_order) {
    var real_order_price = 0;

    if (direction == "buy" || direction == "closesell") {
        if (is_market_order) {
            real_order_price = -1;
        }
        else if (UseOpponentOrder) {
            real_order_price = order_base_price * (1 + OpponentSlip);
            _IsOpponentOrder = true;
        }
        else {
            real_order_price = order_base_price;
        }
    } else if (direction == "sell" || direction == "closebuy") {
        if (is_market_order) {
            real_order_price = -1;
        }
        else if (UseOpponentOrder) {
            real_order_price = order_base_price * (1 - OpponentSlip);
            _IsOpponentOrder = true;
        }
        else {
            real_order_price = order_base_price;
        }
    } else {
        Log("calculateRealOrderPrice: Order direction error.");
    }

    return real_order_price;
}

function calculateMaxOrderSize(ticker, account, num) {
    var max_order_size = 0;
    var limit_max_order_size = 0;

    if (UseAllInOrder) {
        max_order_size = getMaxOrderSize(_MarginLevel, ticker, account);
        limit_max_order_size = UseQuarter ? (LimitMaxOrderAmount * _MarginLevel / _QuarterOneSizeValue) : (LimitMaxOrderAmount * _MarginLevel / ticker.Last / _OneSizeInCurrentCoin);
        if (UseLimitMaxOrderAmount && max_order_size > limit_max_order_size)
            max_order_size = limit_max_order_size;
    }

    return max_order_size;
}

function orderDirectly(direction, order_price, order_size, num) {
    exchanges[num].SetDirection(direction);
    if (direction == "buy" || direction == "closesell") {
        // Closing positions are all default market full close
        // Log("Number of orders placed:", order_size);
        exchanges[num].Buy(direction == "buy" ? order_price : -1, order_size);
    } else if (direction == "sell" || direction == "closebuy") {
        // Log("Number of orders placed:", order_size);
        exchanges[num].Sell(direction == "sell" ? order_price : -1, order_size);
    }
}

function isNoPositionToClose(direction, position_size) {
    if ((position_size == 0) && (direction == "closebuy" || direction == "closesell"))
        return true;
    return false;
}

// Place order under a single account
function orderSingleAccount(num, direction, order_size, is_market_order) {
    // First obtain market depth and account information
    var ticker = exchanges[num].GetTicker();
    var account = exchanges[num].GetAccount();
    if (!ticker || !account) {
        Log(exchanges[num].GetLabel(), ":ObtaintickeroraccountAbnormal, do not place order.", "@");
        return;
    }
    // Get position situation
    var position_size = getPositionSize(num, false);
    // if (position_size != 0)
       // Log(exchanges[num].GetLabel(), "Position quantity of:", position_size);
    if (isNoPositionToClose(direction, position_size)) {
        Log(exchanges[num].GetLabel(), " No positions, do not close positions.");
        resetPosition(num);
        return;
    }

    // Calculate the maximum number of orders that can be placed
    var max_order_size = calculateMaxOrderSize(ticker, account, num);
    if (UseAllInOrder)
        Log(exchanges[num].GetLabel(), ":order:", "Maximum number of orders allowed = ", max_order_size);
    // Calculate order volume
    var real_order_size = calculateRealOrderSize(direction, max_order_size, position_size, order_size, num);
    // Calculate order price
    var order_base_price = ticker.Last;
    var real_order_price = calculateRealOrderPrice(direction, order_base_price, is_market_order);
    // Officially place an order
    orderDirectly(direction, real_order_price, real_order_size, num);
}

function order(direction, order_size, is_market_order) {
    var ticker = [];
    var account = [];
    var real_order_price = [];
    var max_order_size = 0;
    var real_order_size = [];
    var position_size = 0;
    var order_base_price = 0;
    var i = 0;

    // Log("Start ordering.Start timestamp:", Unix());
    for (i = 0; i < exchanges.length; i ++) {
        // First obtain market depth and account information
        ticker[i] = exchanges[i].GetTicker();
        account[i] = exchanges[i].GetAccount();
        if (!ticker[i] || !account[i]) {
            Log(exchanges[i].GetLabel(), ":ObtaintickeroraccountException, do not place order for now, skip.", "@");
            continue;
        }
        // Get position situation
        position_size = getPositionSize(i, false);
        // if (position_size != 0)
           //  Log(exchanges[i].GetLabel(), "Position quantity of:", position_size);
        if (isNoPositionToClose(direction, position_size)) {
            Log(exchanges[i].GetLabel(), " No positions, do not close positions.");
            resetPosition(i);
            continue;
        }

        // Calculate the maximum number of orders that can be placed
        max_order_size = calculateMaxOrderSize(ticker[i], account[i], i);
        if (UseAllInOrder)
            Log(exchanges[i].GetLabel(), ":order:", "Maximum number of orders allowed = ", max_order_size);
        // Calculate order volume
        real_order_size[i] = calculateRealOrderSize(direction, max_order_size, position_size, order_size, i);
        // Calculate order price
        order_base_price = UseSameTicker ? ticker[0].Last : ticker[i].Last;
        real_order_price[i] = calculateRealOrderPrice(direction, order_base_price, is_market_order);
        // Officially place an order
        orderDirectly(direction, real_order_price[i], real_order_size[i], i);

        // Remove slippage, used for statistics  
        real_order_price[i] = order_base_price;
        if (IsUseBinanceOrder)      // Fix BinanceUSDTNumber of orders for perpetual contracts, to unify globally
            real_order_size[i] = real_order_size[i] / _OneSizeInCurrentCoin;
    }

    // Log("Order placement completed.End timestamp:", Unix());
    return [real_order_price, real_order_size];
}

function orderSync(direction, order_size, is_market_order) {
    // Threads enabled
    var thread_get_ticker = [];
    var thread_get_account = [];
    var thread_get_position = [];
    var thread_order = [];
    // Corresponding to the results obtained by the thread
    var ticker = [];
    var account = [];
    var position = [];
    var order_id = [];
    // Other variables
    var real_order_price = [];
    var real_order_size = [];
    var max_order_size = 0;
    var position_size = 0;
    var order_base_price = 0;
    var i = 0;

    // Log("Start multi-threaded order placement.Start timestamp:", Unix());
    // While setting the trading direction, enable multi-threading to obtain data.
    for (i = 0; i < exchanges.length; i++) {
        // First start all threads at once, while simultaneously retrieving data
        exchanges[i].SetDirection(direction);
        thread_get_ticker[i] = exchanges[i].Go("GetTicker");
        thread_get_account[i] = exchanges[i].Go("GetAccount");
        thread_get_position[i] = exchanges[i].Go("GetPosition");
    }

    // Calculate the final number of orders and order prices based on the results returned by threads
    for (i = 0; i < exchanges.length; i++) {
        // Retrieve results from the data sequentially
        ticker[i] = thread_get_ticker[i].wait();
        account[i] = thread_get_account[i].wait();
        position[i] = thread_get_position[i].wait();
        if (!ticker[i] || !account[i] || !position[i]) {
            Log(exchanges[i].GetLabel(), ":Exception when fetching trading data, skip order for now.", "@");
            continue;
        }
        // Get position situation
        refreshPosition(position[i][0], i);
        position_size = _Positions[i].size;
        // if (position_size != 0)
           // Log(exchanges[i].GetLabel(), "Position quantity of:", position_size);
        if (isNoPositionToClose(direction, position_size)) {
            Log(exchanges[i].GetLabel(), ":No positions, do not close positions.");
            continue;
        }
        // Calculate the maximum number of orders that can be placed
        max_order_size = calculateMaxOrderSize(ticker[i], account[i], i);
        if (UseAllInOrder)
            Log(exchanges[i].GetLabel(), ":order:", "Maximum number of orders allowed = ", max_order_size);
        // Calculate order volume
        real_order_size[i] = calculateRealOrderSize(direction, max_order_size, position_size, order_size, i);
        // Calculate order price
        order_base_price = UseSameTicker ? ticker[0].Last : ticker[i].Last;
        real_order_price[i] = calculateRealOrderPrice(direction, order_base_price, is_market_order);

        // Enable multi-threaded order placement
        if (direction == "buy" || direction == "closesell") {
            // Closing positions are all default market full close
            thread_order.push(exchanges[i].Go("Buy", direction == "buy" ? real_order_price[i] : -1, real_order_size[i]));       // Note to use herepushTo assign valuethread_order,To avoid issues due to the previouscontinueSkipped situations cause the array contents to be discontinuous.
        } else if (direction == "sell" || direction == "closebuy") {
            thread_order.push(exchanges[i].Go("Sell", direction == "sell" ? real_order_price[i] : -1, real_order_size[i]));
        }

        // Remove slippage, used for statistics
        real_order_price[i] = order_base_price;
        if (IsUseBinanceOrder)      // Fix BinanceUSDTNumber of orders for perpetual contracts, to unify globally
            real_order_size[i] = real_order_size[i] / _OneSizeInCurrentCoin;
    }

    // Wait for the order to finish to release the thread
    for (i = 0; i < thread_order.length; i++) {
        order_id[i] = thread_order[i].wait();
    }

    // Log("Multi-threaded order placement finished.End timestamp:", Unix());
    return [real_order_price, real_order_size];
}

function trade(account_index, order_type, order_price, order_size) {
    var direction;
    var is_market_order = false;
    var real_order_size = [];
    var real_order_price = [];

    if (order_type == "longopen")
        direction = "buy";
    else if (order_type == "longclose")
        direction = "closebuy";
    else if (order_type == "shortopen")
        direction = "sell";
    else if (order_type == "shortclose")
        direction = "closesell";
    else
        Log("Order direction error.");

    if (IsMarketOrder)  
        is_market_order = true;

    if (account_index != -1) {
        // Place order under a single account
        orderSingleAccount(account_index, direction, order_size, is_market_order);
        Log(exchanges[account_index].GetLabel(), ": Order completed.");
        return;
    }

    [real_order_price, real_order_size] = UseOrderSync ? orderSync(direction, order_size, is_market_order) : order(direction, order_size, is_market_order);

    if (order_type == "longopen" || order_type == "shortopen") {
        orderInBacktest(order_type == "longopen" ? "long" : "short", real_order_price, real_order_size);
        if (EnablePlot) {
            if (order_type == "longopen")
                $.PlotFlag(_LastBarTime, ' ', 'open long', 'circlepin', 'green');
            else
                $.PlotFlag(_LastBarTime, ' ', 'open short', 'flag', 'red');
        }
    } else if (order_type == "longclose" || order_type == "shortclose") {
        coverInBacktest(real_order_price, _MarginLevel, "Close Position.");
        if (EnablePlot) {
            if (order_type == "longclose")
                $.PlotFlag(_LastBarTime, ' ', 'close long', 'circlepin', 'blue');
            else
                $.PlotFlag(_LastBarTime, ' ', 'close short', 'circlepin', 'blue');
        }
    }
}

function orderRobot() {
    var cmd = GetCommand();
    var cmd_data;
    var num;

    if (cmd) {
        // Detect interactive commands
        Log("Received command:", cmd, "#FF1CAE");
        if (cmd.includes(_QuantitativeOrderHeader)) {
            // $"symbol={symbol},type={type},level_rate={level_rate},price={price},size={size}";
            var order_cmd = cmd.replace(_QuantitativeOrderHeader, "");
            var symbol = order_cmd.substring(7, order_cmd.indexOf(","));
            order_cmd = order_cmd.replace("symbol=" + symbol + ",", "");
            var type = order_cmd.substring(5, order_cmd.indexOf(","));
            order_cmd = order_cmd.replace("type=" + type + ",", "");
            var level_rate = Number(order_cmd.substring(11, order_cmd.indexOf(",")));
            order_cmd = order_cmd.replace("level_rate=" + level_rate + ",", "");
            var price = Number(order_cmd.substring(6, order_cmd.indexOf(",")));
            order_cmd = order_cmd.replace("price=" + price + ",", "");
            var size = Number(order_cmd.substring(5));
            // Log("symbol = ", symbol, " type = ", type, " level_rate = ", level_rate, " price = ", price, " size = ", size);
            trade(-1, type, price, size);
        } else if (cmd.indexOf("ClearLocalData:") == 0) {
            // Clear local data
            var account_index = cmd.replace("ClearLocalData:", "");
            clearUserDataLocal(account_index);
        } else if (cmd.indexOf("SaveLocalData:") == 0) {
            // Save data locally
            saveUserDatasLocal();
        } else if (cmd.indexOf("ClearLog:") == 0) {
            // Clear log
            var log_reserve = cmd.replace("ClearLog:", "");
            LogReset(Number(log_reserve));
        } else if (cmd.indexOf("LogStatusRefreshTime:") == 0) {
            // Modify status bar update interval
            _LogStatusRefreshTime = cmd.replace("LogStatusRefreshTime:", "");
        } else if (cmd.indexOf("LogPrint:") == 0) {
            // Clear log
            var log_print = cmd.replace("LogPrint:", "");
            Log(log_print);
        } else if (cmd.indexOf("SetStrategyRunTime:") == 0) {
            // Set policy start time
            var strategy_run_time = cmd.replace("SetStrategyRunTime:", "");
            Log(strategy_run_time);
            setStrategyRunTime(strategy_run_time);
        } else if (cmd.indexOf("AdjustOrderSize:") == 0) {
            // Adjust order quantity
            num = Number(cmd.replace("AdjustOrderSize:", ""));
            var ticker;
            Log(num);
            if (num == -1) {
                for (var i = 0; i < exchanges.length; i++) {
                    ticker = _C(exchanges[i].GetTicker);
                    adjustOrderSizes(ticker, i);
                }
            } else {
                ticker = _C(exchanges[num].GetTicker);
                adjustOrderSizes(ticker, num);
            }
        } else if (cmd.indexOf("SetUserStartTime:") == 0) {
            // Set user start time
            cmd_data = cmd.replace("SetUserStartTime:", "");
            num = Number(cmd_data.split(",")[0]);
            var timestamp = cmd_data.split(",")[1];
            UserStartTime[num] = Number(timestamp);
        } else if (cmd.indexOf("SetUserInitAsset:") == 0) {
            // Set user initial assets
            cmd_data = cmd.replace("SetUserInitAsset:", "");
            num = Number(cmd_data.split(",")[0]);
            var init_asset = cmd_data.split(",")[1];
            _InitAsset[num] = Number(init_asset);
        } else if (cmd.indexOf("ManualOrder:") == 0) {
            // Manual order placement
            cmd_data = cmd.replace("ManualOrder:", "");
            num = Number(cmd_data.split(",")[0]);
            var order_type = cmd_data.split(",")[1];
            var order_size = Number(cmd_data.split(",")[2]);
            trade(num, order_type, 0, order_size);
        }
    }

    // Print status bar information
    printLogStatus();
    // holdKDraw the line
    plotRecords();
    // Check unfilled orders
    checkPendingOrders();
    // Automatically remove assets
    autoTransfer();
}

var _OpponentOrderCount = 0;
function checkPendingOrders() {
    if (_IsOpponentOrder && !IsMarketOrder) {
        _OpponentOrderCount++;
        if ((Interval / 1000) * _OpponentOrderCount >= OpponentOrderTime) {
            cancelAllPendingOrders();
            _OpponentOrderCount = 0;
            _IsOpponentOrder = false;
        }
    }
}

function plotRecords() {
    if (EnablePlot) {
        var records = exchange.GetRecords(KPeriod * 60);
        if (!records || (records.length < 1)) {
            Log("ObtainKMarket data exception.");
            return;
        }
        _LastBarTime = records[records.length - 1].Time;

        // holdKDraw the line
        $.PlotRecords(records, 'KLine');
    }
}

var _LogStatusCount = 0;
function printLogStatus() {
    var t_direction;
    var position_asset = 0;
    var position_profit = 0;
    var position_profit_percent = 0;
    var price = 0;
    var account_asset = 0;
    var balance = 0;
    var balance_frozen = 0;
    var account_profit = 0;
    var account_profit_percent = 0;
    var user_start_time;

    _LogStatusCount++;
    if (_LogStatusCount >= (_LogStatusRefreshTime / (Interval / 1000 ))) {
        // Print position and account information
        var table_overview = { type: 'table', title: 'Strategy Overview', cols: ['Start time', 'Days operated', 'trading pair', 'Current Price', 'Leverage multiple', 'Estimated monthly cost%', 'Cooperation contact WeChat'], rows: [] };
        var table_account = { type: 'table', title: 'Account funds', cols: ['Serial number', 'Account', 'Start time', 'Current Assets', 'Initial Assets', 'Assets removed', 'Available balance', 'Freeze balance', 'Order Quantity', 'Revenue', 'Revenue%'], rows: [] };
        var table_position = { type: 'table', title: 'Position status', cols: ['Serial number', 'Account', 'Average position price', 'Direction', 'Quantity', 'Margin', 'Floating profit and loss', 'Floating profit and loss%'], rows: [] };
        
        for (var i = 0; i < exchanges.length; i++) {
            var ticker = exchanges[i].GetTicker();
            if (!ticker) {
                Log(exchanges[i].GetLabel(), ":tickerFetch Failed.printLogStatus().");
                continue;
            }
            price = ticker.Last;

            // Strategy overview table
            if (i == 0) {       
                var the_running_days = getDaysFromTimeStamp(StrategyDatas.start_run_timestamp, Unix());
                var monthly_rate_of_profit = 0;
                if (the_running_days > 2)
                    monthly_rate_of_profit = ProfitLocal[i] / _InitAsset[i] / the_running_days * 30;
                table_overview.rows.push([_D(StrategyDatas.start_run_timestamp * 1000), the_running_days, exchanges[i].GetCurrency(), price, _MarginLevel, _N(monthly_rate_of_profit * 100, 2) + "%", 'wd1061331106']);
            }

            if (getPositionSize(i, false) == 0)    // If there are no positions, reset the position information to avoid errors in backtest statistics
                resetPosition(i);
            if (refreshAccountInfo(ticker, i) == -1)    // If account information is not obtained, reset first
                resetAccountInfo(i);

            if (_Positions[i].size != 0) {
                position_profit_percent = _Positions[i].direction == "long" ? ((price - _Positions[i].avg_cost) / _Positions[i].avg_cost) * _MarginLevel : ((_Positions[i].avg_cost - price) / _Positions[i].avg_cost) * _MarginLevel;
                position_asset = getPositionAsset(i, price);
                position_profit = position_asset * position_profit_percent;
            } else {
                position_profit_percent = 0;
                position_asset = 0;
                position_profit = 0;
            }
            account_asset = getAccountAsset(i, ticker.Last);
            t_direction = _Positions[i].direction == "long" ? "Long Position" : "Short Position";
            if (_Positions[i].size == 0)
                t_direction = "No position";
            account_profit = account_asset + _TransferAmount[i] - _InitAsset[i];
            account_profit_percent = account_profit / _InitAsset[i];
            balance = UseQuarter ? _N(_Accounts[i].stocks, 4) : _N(_Accounts[i].balance, 2);
            balance_frozen = UseQuarter ? _Accounts[i].frozen_stocks : _N(_Accounts[i].frozen_balance, 2);
            user_start_time = _D(UserStartTime[i] * 1000, "yyyy-MM-dd");

            table_account.rows.push([i, exchanges[i].GetLabel(), user_start_time, _N(account_asset, 4), _N(_InitAsset[i], 4), _N(_TransferAmount[i], 4), balance, balance_frozen,
                _OrderSize[i] + " / " + _Accounts[i].max_order_size, _N(account_profit, 4), _N((account_profit_percent * 100), 2) + "%"]);
            table_position.rows.push([i, exchanges[i].GetLabel(), _N(_Positions[i].avg_cost, 2), t_direction, _N(_Positions[i].size, 2), _N(position_asset, 4), _N(position_profit, 4), _N((position_profit_percent * 100), 2) + "%"]);
        }

        LogStatus('`' + JSON.stringify(table_overview) + '`\n'
            // + '\n' + print_info + '\n' + '\n'
            + '`' + JSON.stringify([table_account, table_position]) + '`\n');
        _LogStatusCount = 0;
    }
}

function adjustOrderSizes(ticker, num) {
    var account = _C(exchanges[num].GetAccount);
    var max_order_size = getMaxOrderSize(_MarginLevel, ticker, account) + _Positions[num].size;
    _OrderSize[num] = Math.trunc(max_order_size * ThePercentOfAssetToOrder);
    if (_OrderSize[num] < 1 && _Positions[num].size != 0)
        _OrderSize[num] = 1;
}

// Determine whether it is a Binance exchange
function isBinanceExchange(num) {
    if (exchanges[num].GetName() == "Futures_Binance") {
        return true;
    }
    return false;
}

function setContract() {
    var order_sizes = OrderSize.split(",");
    var init_assets = InitAsset.split(",");
    var ticker;

    saveStrategyRunTime();

    for (var i = 0; i < exchanges.length; i++) {
        // Log(exchanges[i].GetLabel());
        // exchanges[i].IO("simulate", true);
        if (UseQuarter) {
            exchanges[i].SetContractType("quarter"); // Quarterly Contract
        }
        else {
            exchanges[i].SetContractType("swap"); // Perpetual Contract
        }
        exchanges[i].SetCurrency(Currency);
        exchanges[i].SetMarginLevel(_MarginLevel);
        exchanges[i].IO("cross", true);     // Cross Margin Mode
        exchanges[i].SetPrecision(_PricePrecision, _AmountPrecision);

        // Get your holdings and account information
        ticker = _C(exchanges[i].GetTicker);
        _Positions.push({ avg_cost: 0, direction: "short", size: 0, order_count: 0 });
        _Accounts.push({ balance: 0, frozen_balance: 0, stocks: 0, frozen_stocks: 0, max_order_size: 0 });
        if (getPositionSize(i, false) == 0)    // If there are no positions, reset the position information to avoid errors in backtest statistics
            resetPosition(i);
        if (refreshAccountInfo(ticker, i) == -1)    // If account information is not obtained, reset first
            resetAccountInfo(i);

        // Read local data while constructingUserData
        readUserDataLocal(i);
        // Calculate the initial assets of the account under different situations
        if (!isHadLocalData(i)) {
            // No local data
            if ((UseQuarter && _Accounts[i].stocks == 0 && _Accounts[i].frozen_stocks == 0 && _Positions[i].size == 0)
                || (!UseQuarter && _Accounts[i].balance == 0 && _Accounts[i].frozen_balance == 0 && _Positions[i].size == 0)) {
                _InitAsset[i] = Number(init_assets[i]);
            } else {
                _InitAsset[i] = getAccountAsset(i, ticker.Last);
            }
            TotalAsset[i] = _InitAsset[i];
        } else {
            // If local data exists, read directly
            _InitAsset[i] = UserDatas[i].init_assets;
            TotalAsset[i] = _InitAsset[i] + UserDatas[i].profit_local;
        }

        // Initialize data
        ProfitPercent[i] = 0;
        WinRate[i] = 0;

        // Copy local data,If no local data, default to0
        ProfitLocal[i] = UserDatas[i].profit_local;
        TakeProfitCount[i] = UserDatas[i].take_profit_count;
        StopLossCount[i] = UserDatas[i].stop_loss_count;
        MaxLoss[i] = UserDatas[i].max_loss;
        MaxLossPercent[i] = UserDatas[i].max_loss_percent;
        MaxProfit[i] = UserDatas[i].max_profit;
        MaxProfitPercent[i] = UserDatas[i].max_profit_percent;
        UserStartTime[i] = UserDatas[i].start_time;
        _TransferAmount[i] = UserDatas[i].transfer_amount ? UserDatas[i].transfer_amount : 0;
        _CurrentInitAssets[i] = UserDatas[i].current_init_assets ? UserDatas[i].current_init_assets : 0;

        // Adjust order quantity
        if (UseAutoAdjustOrderSize) {
            if (UserDatas[i].order_size == 0) {
                adjustOrderSizes(ticker, i);
            } else {
                _OrderSize[i] = UserDatas[i].order_size;
            }
        } else {
            _OrderSize[i] = Number(order_sizes[i]);
        }
    }
}

function main() {
    setContract();
    while(true) {
        orderRobot();
    	Sleep(Interval);
    }
}
```

> Detail

https://www.fmz.com/strategy/301404

> Last Modified

2022-02-22 23:20:20
