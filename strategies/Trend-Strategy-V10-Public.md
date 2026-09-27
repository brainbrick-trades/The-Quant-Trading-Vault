
> Name

Trend-Strategy-V10-Public

> Author

夏天不打你

> Strategy Description

#### This is a complete set of trend strategies written a long time ago. The previous backtesting effect on ETH was very obvious, but the market did not adapt to it later. So use real offers with caution.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|TradeCurrency|ETH_USD|(?Basic settings) Trading pair (use USD ending for coin-margined, use USDT ending for U-margined))|
|Interval|5000|Program runtime period(ms)|
|UseQuarter|false|Quarterly contracts, default USDT perpetual contracts|
|OnlyTrendJudgment|false|Only perform trend judgment, do not place orders|
|EnableMessageSend|false|Push message|
|RunInKLinePeriod|true|(?Trend judgment) Execute the core strategy according to the candlestick cycle|
|KLinePeriod|60|KLine period(min)|
|EmaLength|90|EMALength|
|EmaCoefficient|0.004|EMAEffective coefficient|
|UseStddev|true|Use standard deviation|
|UseRecordsMiddleValue|true|Use the median of the candlestick to calculate standard deviation; otherwise, use the candlestick closing price|
|StddevLength|33|Standard deviation length|
|StddevDeviations|true|Standard deviation offset|
|MarginLevel|5|(?Place order) leverage multiplier|
|OrderSize|10|Order quantity / number of contracts|
|OrderByMargin|true|Determine order quantity based on the order margin|
|OrderMarginPercent|50|Order margin percentage (calculated based on initial funds)%|
|PricePrecision|2|Order price precision (decimal places))|
|AmountPrecision|false|Order quantity precision (decimal places)|
|OneSizeInCurrentCoin|true|UIn the base contract, the amount of the currency represented by one contract|
|QuarterOneSizeValue|10|In the currency-based contract, the amount of USDT represented by one piece|
|UseStopLoss|false|(?Take profit and stop loss) use stop loss|
|StopLossPercent|1.4|Stop Loss Percentage%|
|UseTakeProfit|false|Use take profit|
|TakeProfitPercent|10|Take profit percentage%|
|UseTrackingTakeProfit|false|Use callback take profit|
|UsePositionRetracement|false|Use position drawdown percentage for take-profit, otherwise use price drawdown percentage for take-profit|
|TakeProfitTriggerPercent|5|Callback take-profit price trigger percentage%|
|CallBakcPercent|true|Callback percentage%|




|Button|Default|Description|
|----|----|----|
|SaveLocalData|false|Save data locally|
|ClearLocalData|false|Clear local data|
|ClearLog|true|Clear log|
|OrderSize|10|Order Quantity|
|OrderMarginPercent|25|Order margin percentage%|


> Source (javascript)

``` javascript

/*
Trend StrategyV1.0
Version: 1.0
Author: summer
Date: 2021.9.27
*/


// Strategy parameter variables
// Basic settings
var _Currency = TradeCurrency;                                  // trading pair
var _Interval = Interval;                                       // Program runtime period
var _UseQuarter = UseQuarter;                                   // Quarterly contracts, default USDT perpetual contracts
var _OnlyTrendJudgment = OnlyTrendJudgment;                     // Only do trend judgment, not trading
var _EnableMessageSend = EnableMessageSend;                     // Push message
// Trend judgment
var _RunInKLinePeriod = RunInKLinePeriod;                       // According toKLine cycle execute strategy core
var _KLinePeriod = KLinePeriod;                                 // KLine period(min)
var _EmaLength = EmaLength;                                     // EMALength
var _EmaCoefficient = EmaCoefficient;                           // EMAEffective coefficient
var _UseStddev = UseStddev;                                     // Use standard deviation
var _UseRecordsMiddleValue = UseRecordsMiddleValue;             // Use the median of the candlestick to calculate standard deviation; otherwise, use the candlestick closing price
var _StddevLength = StddevLength;                               // Standard deviation length
var _StddevDeviations = StddevDeviations;                       // Standard deviation offset
// Order Settings
var _MarginLevel = MarginLevel;                                 // Leverage multiple
var _OrderSize = OrderSize;                                     // Order quantity / number of contracts
var _OrderByMargin = OrderByMargin;                             // Determine order quantity based on the order margin
var _OrderMarginPercent = OrderMarginPercent;                   // Order margin percentage%(Calculated based on initial capital)
var _PricePrecision = PricePrecision;                           // Order price accuracy
var _AmountPrecision = AmountPrecision;                         // Order quantity progress
var _OneSizeInCurrentCoin = OneSizeInCurrentCoin;               // UIn the standard contract, oneETHRepresentsETHQuantity
var _QuarterOneSizeValue = QuarterOneSizeValue;                 // One coin-margined contractETHRepresentsUSDTQuantity
// take profit and stop loss
var _UseStopLoss = UseStopLoss;                                 // Use stop loss
var _StopLossPercent = StopLossPercent;                         // Stop Loss Percentage%
var _UseTakeProfit = UseTakeProfit;                             // Use take profit
var _TakeProfitPercent = TakeProfitPercent;                     // Take profit percentage%
var _UseTrackingTakeProfit = UseTrackingTakeProfit;             // Use callback take profit
var _UsePositionRetracement = UsePositionRetracement;           // Use position drawdown percentage for take-profit, otherwise use price drawdown percentage for take-profit
var _TakeProfitTriggerPercent = TakeProfitTriggerPercent;       // Callback take-profit price trigger percentage%
var _CallBakcPercent = CallBakcPercent;                         // Callback percentage%

// Strategy variables
var _LastBarTime = 0;                                    // LatestKLine Time
var _TrendWhenTakeProfitOrStopLoss = 0;                  // The status of the trend when taking profit and stop loss  1Indicates long -1Indicates short
var _HadStopLoss = false;                                // Stop loss occurred
var _TriggeredTakeProfit = false;                        // Whether callback take profit was triggered
var _PeakPriceInPosition = 0;                            // The peak price point during holding (highest/Lowest point)
var _HadTakeProfit = false;                              // Take profit occurs
var _PriceCrossEMAStatus = 0;                            // Used to determine whether the price crosses the moving average.0:Initial state, not worn(Status after policy restart) -1:Initial state below moving average 1:Initial state above moving average 2:Already completed crossing

// Statistical variables
var _InitAsset = 0;
var _ProfitLocal = 0;
var _TakeProfitCount = 0;
var _TradeCount = 0;
var StrategyRunTimeStampString = "strategy_run_time";
var _StrategyDatas = { start_run_timestamp: 0, others: "" };
var _UserDatas = null;

// Relatively fixed parameters
var _MaintenanceMarginRate = 0.004  // Maintain margin ratio
var _TakerFee = 0.0005;             // Taker Fee
var _IsUsdtStandard = false;        // USDTMargined order placement and settlement


// Save the program's start running time in seconds timestamp
function saveStrategyRunTime() {
    var local_data_strategy_run_time = _G(StrategyRunTimeStampString);

    if (local_data_strategy_run_time == null) {
        _StrategyDatas.start_run_timestamp = Unix();
        _G(StrategyRunTimeStampString, _StrategyDatas.start_run_timestamp);
    }
    else {
        _StrategyDatas.start_run_timestamp = local_data_strategy_run_time;
    }
}

// Set the program's start running time in seconds timestamp
function setStrategyRunTime(timestamp) {
    _G(StrategyRunTimeStampString, timestamp);
    _StrategyDatas.start_run_timestamp = timestamp;
}

// Calculate the number of days between two timestamps, the parameter is a second-level timestamp
function getDaysFromTimeStamp(start_time, end_time) {
    if (end_time < start_time)
        return 0;

    return Math.trunc((end_time - start_time) / (60 * 60 * 24));
}

// Save data locally
function saveUserDatasLocal() {
    _UserDatas = {
        init_assets: _InitAsset,
        profit_local: _ProfitLocal,
        take_profit_count: _TakeProfitCount,
        trade_count: _TradeCount
    };
    // Save to local
    _G(exchange.GetLabel(), _UserDatas);
    Log("All data has been saved locally.");
}

// Read the user's local data and run it once when the program starts
function readUserDataLocal() {
    var user_data = _G(exchange.GetLabel());
    if (user_data == null) {
        _InitAsset = getAccountAsset(_C(exchange.GetPosition), _C(exchange.GetAccount), _C(exchange.GetTicker));
        _UserDatas = {
            init_assets: _InitAsset,
            profit_local: 0,
            take_profit_count: 0,
            trade_count: 0
        };
    } else {
        _UserDatas = user_data;
    }
}

// Clear the user's local data, run by clicking the interactive button
function clearUserDataLocal() {
    _G(exchange.GetLabel(), null);
    Log(exchange.GetLabel(), ":Local data cleared.");
}

// Strategy Interaction
function runCmd() {
    var cmd = GetCommand();

    if (cmd) {
        // Detect interactive commands
        Log("Received command:", cmd, "#FF1CAE");
        if (cmd.indexOf("ClearLocalData:") == 0) {
            // Clear local data
            clearUserDataLocal();
        } else if (cmd.indexOf("SaveLocalData:") == 0) {
            // Save data locally
            saveUserDatasLocal();
        } else if (cmd.indexOf("ClearLog:") == 0) {
            // Clear log
            var log_reserve = cmd.replace("ClearLog:", "");
            LogReset(Number(log_reserve));
        } else if (cmd.indexOf("OrderSize:") == 0) {
            // Modify order quantity
            if (_OrderByMargin) {
                Log("The order has already been placed using the margin amount, so you cannot directly modify the order quantity!");
            } else {
                var order_size = Number(cmd.replace("OrderSize:", ""));
                _OrderSize = order_size;
                Log("Order quantity has been changed to:", _OrderSize);
            }
        } else if (cmd.indexOf("OrderMarginPercent:") == 0) {
            // Modify order margin percentage
            if (_OrderByMargin) {
                var order_margin_percent = Number(cmd.replace("OrderMarginPercent:", ""));
                _OrderMarginPercent = order_margin_percent;
                Log("Order margin percentage:", _OrderMarginPercent, "%");
            } else {
                Log("The order based on the margin amount is not enabled, unable to modify the order margin percentage!");
            }
        }
    }
}

// Trading function
function orderDirectly(distance, price, amount) {
    var tradeFunc = null;

    if (amount <= 0) {
        throw "Parameter set incorrectly, order quantity is already less than0!"
    }

    if (distance == "buy") {
        tradeFunc = exchange.Buy;
    } else if (distance == "sell") {
        tradeFunc = exchange.Sell;
    } else if (distance == "closebuy") {
        tradeFunc = exchange.Sell;
    } else {
        tradeFunc = exchange.Buy;
    }

    exchange.SetDirection(distance);
    return tradeFunc(price, amount);
}

function openLong(price, amount) {
    var real_amount = getRealOrderSize(price, amount);
    return orderDirectly("buy", price, real_amount);
}

function openShort(price, amount) {
    var real_amount = getRealOrderSize(price, amount);
    return orderDirectly("sell", price, real_amount);
}

function coverLong(price, amount) {
    return orderDirectly("closebuy", price, amount);
}

function coverShort(price, amount) {
    return orderDirectly("closesell", price, amount);
}

// Recalculate order quantity
function getRealOrderSize(price, amount) {
    var real_price = price == -1 ? _C(exchange.GetTicker).Last : price;
    if (_OrderByMargin) {
        if (_IsUsdtStandard) {
            _OrderSize = _N(_InitAsset * (_OrderMarginPercent / 100) / real_price * _MarginLevel / _OneSizeInCurrentCoin, _AmountPrecision);
        } else {
            _OrderSize = _N(_InitAsset * (_OrderMarginPercent / 100) * _MarginLevel * real_price / _QuarterOneSizeValue, _AmountPrecision);
        }
    } else {
        _OrderSize = amount;
    }
    return _OrderSize;
}

// Get the profit and earnings of one-way positions%
function getSinglePositionProfit(position, ticker) {
    if (position.length == 0)
        return [0, 0];

    var price = ticker.Last;
    var position_margin = getSinglePositionMargin(position, ticker);

    var position_profit_percent = position[0].Type == PD_LONG ? ((price - position[0].Price) / position[0].Price) * _MarginLevel : ((position[0].Price - price) / position[0].Price) * _MarginLevel;
    var position_profit = position_margin * position_profit_percent;

    return [position_profit, position_profit_percent];
}

// Calculate forced liquidation price
function calculateForcedPrice(account, position, ticker) {
    var position_profit = 0;
    var total_avail_balance = 0;
    var forced_price = 0;

    var position_margin = getSinglePositionMargin(position, ticker);
    [position_profit, position_profit_percent] = getSinglePositionProfit(position, ticker);

    if (_IsUsdtStandard) {
        total_avail_balance = position_profit > 0 ? account.Balance + position_margin + account.FrozenBalance - position_profit : account.Balance + position_margin + account.FrozenBalance;
        if (position[0].Type == PD_LONG) {
            forced_price = (((_MaintenanceMarginRate + _TakerFee) * _MarginLevel * account.FrozenBalance - total_avail_balance) / _OneSizeInCurrentCoin + (position[0].Amount * position[0].Price))
                / (position[0].Amount - (_MaintenanceMarginRate + _TakerFee) * position[0].Amount);
        } else {
            forced_price = (((_MaintenanceMarginRate + _TakerFee) * _MarginLevel * account.FrozenBalance - total_avail_balance) / _OneSizeInCurrentCoin - (position[0].Amount * position[0].Price))
                / (-1 * position[0].Amount - (_MaintenanceMarginRate + _TakerFee) * position[0].Amount);
        }
    } else {
        total_avail_balance = position_profit > 0 ? account.Stocks + position_margin + account.FrozenStocks - position_profit : account.Stocks + position_margin + account.FrozenStocks;
        if (position[0].Type == PD_LONG) {
            forced_price = (_MaintenanceMarginRate * position[0].Amount + position[0].Amount) / (total_avail_balance / _QuarterOneSizeValue + position[0].Amount / position[0].Price);
        } else {
            forced_price = (_MaintenanceMarginRate * position[0].Amount - position[0].Amount) / (total_avail_balance / _QuarterOneSizeValue - position[0].Amount / position[0].Price);
        }
    }

    if (forced_price < 0)
        forced_price = 0;

    return forced_price;
}

// Calculate the maximum number of orders that can be placed
function getMaxOrderSize(margin_level, ticker, account) {
    var max_order_size = 0;

    if (_IsUsdtStandard) {
        max_order_size = account.Balance * margin_level / (_OneSizeInCurrentCoin * ticker.Last);
    } else {
        max_order_size = account.Stocks * ticker.Last / _QuarterOneSizeValue * margin_level;
    }

    return _N(max_order_size, _AmountPrecision);
}

// Get the margin occupied by a single position 
function getSinglePositionMargin(position, ticker) {
    var position_margin = 0;

    if (position.length > 0) {
        if (_IsUsdtStandard) {
            position_margin = position[0].Amount * _OneSizeInCurrentCoin * ticker.Last / _MarginLevel;
        } else {
            position_margin = position[0].Amount * _QuarterOneSizeValue / ticker.Last / _MarginLevel;
        }
    }

    return position_margin;
}

// Get account assets
function getAccountAsset(position, account, ticker) {
    // Calculate the initial assets of the account under different situations
    var account_asset = 0;
    var position_margin = getSinglePositionMargin(position, ticker);

    if (_IsUsdtStandard) {
        if (position.length > 0) {
            account_asset = account.Balance + account.FrozenBalance + position_margin;
        } else {
            account_asset = account.Balance + account.FrozenBalance;
        }
    } else {
        if (position.length > 0) {
            account_asset = account.Stocks + account.FrozenStocks + position_margin;
        } else {
            account_asset = account.Stocks + account.FrozenStocks;
        }
    }

    return account_asset;
}

// Revenue statistics
function calculateProfit(ticker) {
    // Re-fetch account positions and assets
    var position = _C(exchange.GetPosition);
    var account = _C(exchange.GetAccount);
    // Current total earnings - Last total profit = Earnings this time
    var current_profit = (getAccountAsset(position, account, ticker) - _InitAsset) - _ProfitLocal;
    _ProfitLocal += current_profit;

    if (current_profit > 0) {
        _TakeProfitCount++;
    }
    _TradeCount++;

    LogProfit(_N(_ProfitLocal, 4), "        Current Profit:", _N(current_profit, 6));
    saveUserDatasLocal();
}

// Check if there is enough funds to place an order
function isEnoughAssetToOrder(order_size, ticker) {
    var is_enough = true;
    var account = _C(exchange.GetAccount);

    if (_IsUsdtStandard) {
        if (account.Balance < order_size * ticker.Last * _OneSizeInCurrentCoin / _MarginLevel) {
            is_enough = false;
        }
    } else {
        if (account.Stocks < order_size * _QuarterOneSizeValue / ticker.Last / _MarginLevel) {
            is_enough = false;
        }
    }

    return is_enough;
}

// According toKLine cycle run strategy core
function runInKLinePeriod(records) {
    var bar_time = records[records.length - 1].Time;
    if (_RunInKLinePeriod && _LastBarTime == bar_time) {
        return false;
    }

    _LastBarTime = bar_time;
    return true;
}

// Check if the price crosses the moving average
function checkPriceCrossEma(price, ema_value) {
    if (_PriceCrossEMAStatus == 0) {
        if (price <= ema_value) {
            _PriceCrossEMAStatus = -1;
        } else {
            _PriceCrossEMAStatus = 1;
        }
    } else if ((_PriceCrossEMAStatus == -1 && price >= ema_value) || (_PriceCrossEMAStatus == 1 && price <= ema_value)) {
        _PriceCrossEMAStatus = 2;   // Completed the crossing
    } 
}

// EMALong/short judgment
function emaJudgment(records) {
    var ema_long = false;
    var ema_short = false;
    var price = records[records.length - 2].Close;  // Already closedKClosing price of the line
    var ema = TA.EMA(records, _EmaLength);
    var ema_value = ema[ema.length - 2];            // CloseKCorresponding lineemavalue
    var ema_upper = ema_value * (1 + _EmaCoefficient);
    var ema_lower = ema_value * (1 - _EmaCoefficient);

    checkPriceCrossEma(price, ema_value);
    if (price > ema_upper) {
        ema_long = true;
    } else if (price < ema_lower) {
        ema_short = true;
    }

    return [ema_long, ema_short];
}

// Standard deviation judgment
function stddevJudgment(records) {
    var in_trend = false;
    if (_UseStddev) {
        var records_data = [];
        for (var i = 0; i < records.length; i++) {
            records_data.push(_UseRecordsMiddleValue ? ((records[i].High + records[i].Low) / 2) : records[i].Close);
        }

        var stddev = talib.STDDEV(records_data, _StddevLength, _StddevDeviations);
        if (stddev[stddev.length - 1] > stddev[stddev.length - 2]) {
            in_trend = true;
        }
    } else {
        in_trend = true;
    }
    return in_trend;
}

// Trend judgment
function trendJudgment(records) {
    var long = false;
    var short = false;
    [long, short] = emaJudgment(records);

    var in_trend = stddevJudgment(records);
    long = (in_trend && long) ? true : false;
    short = (in_trend && short) ? true : false;

    if (long) {
        Log("Current trend: Long", _EnableMessageSend ? "@" : "#00FF7F");
    }
    else if (short) {
        Log("Current trend: Short", _EnableMessageSend ? "@" : "#FF0000");
    } else {
        Log("Current trend: oscillating", _EnableMessageSend ? "@" : "#007FFF");
    }

    return [long, short];
}

// stop loss
function stopLoss(position, ticker) {
    var stop_loss_price = 0;
    var price = ticker.Last;

    if (position.length == 1 && _UseStopLoss) {
        if (position[0].Type == PD_LONG) {
            stop_loss_price = position[0].Price * (1 - _StopLossPercent / 100);
            if (price < stop_loss_price) {
                coverLong(-1, position[0].Amount);
                calculateProfit(ticker);
                _TrendWhenTakeProfitOrStopLoss = 1;
                _HadStopLoss = true;
                Log("Long position stop loss. Stop loss price:", _N(stop_loss_price, 6), ", Position Price:", _N(position[0].Price), _EnableMessageSend ? "@" : "#FF1CAE");
            }
        } else if (position[0].Type == PD_SHORT) {
            stop_loss_price = position[0].Price * (1 + _StopLossPercent / 100);
            if (price > stop_loss_price) {
                coverShort(-1, position[0].Amount);
                calculateProfit(ticker);
                _TrendWhenTakeProfitOrStopLoss = -1;
                _HadStopLoss = true;
                Log("Short position stop loss. Stop loss price:", _N(stop_loss_price, 6), ", Position Price:", _N(position[0].Price), _EnableMessageSend ? "@" : "#FF1CAE");
            }
        }
    }
}

// take profit
function takeProfit(position, ticker) {
    var take_profit_price = 0;
    var price = ticker.Last;

    if (position.length == 1 && _UseTakeProfit) {
        if (position[0].Type == PD_LONG) {
            take_profit_price = position[0].Price * (1 + _TakeProfitPercent / 100);
            if (price > take_profit_price) {
                coverLong(-1, position[0].Amount);
                calculateProfit(ticker);
                _TrendWhenTakeProfitOrStopLoss = 1;
                _HadTakeProfit = true;
                Log("Take profit for long orders. Take profit price:", _N(take_profit_price, 6), ", Position Price:", _N(position[0].Price), _EnableMessageSend ? "@" : "#FF1CAE");
            }
        } else if (position[0].Type == PD_SHORT) {
            take_profit_price = position[0].Price * (1 - _TakeProfitPercent / 100);
            if (price < take_profit_price) {
                coverShort(-1, position[0].Amount);
                calculateProfit(ticker);
                _TrendWhenTakeProfitOrStopLoss = -1;
                _HadTakeProfit = true;
                Log("Take profit for short orders. Take profit price:", _N(take_profit_price, 6), ", Position Price:", _N(position[0].Price), _EnableMessageSend ? "@" : "#FF1CAE");
            }
        }
    }
}

// Callback to take profit
function trackingTakeProfit(position, ticker) {
    var take_profit_price = 0;
    var trigger_price = 0;
    var price = ticker.Last;

    if (position.length > 0 && _UseTrackingTakeProfit) {
        if (position[0].Type == PD_LONG) {
            // Long positions
            if (_TriggeredTakeProfit) {
                // Trigger price reached, monitor whether to take profit
                _PeakPriceInPosition = price > _PeakPriceInPosition ? price : _PeakPriceInPosition;                                           // Update price peak
                if (_UsePositionRetracement) {
                    take_profit_price = _PeakPriceInPosition - (_PeakPriceInPosition - position[0].Price) * (_CallBakcPercent / 100);         // Calculate the take profit price of the callback
                } else {
                    take_profit_price = _PeakPriceInPosition * (1 - _CallBakcPercent / 100);                                                  // Calculate the take profit price of the callback
                }
                if (price < take_profit_price) {
                    coverLong(-1, position[0].Amount);              // close long
                    calculateProfit(ticker);
                    _TriggeredTakeProfit = false;                   // Reset trigger flag
                    _TrendWhenTakeProfitOrStopLoss = 1;             // Record the trend when taking profit
                    _HadTakeProfit = true;                          // A take-profit has occurred
                    Log("Long position pullback take profit: highest price in the position:", _N(_PeakPriceInPosition, 6), ", Take profit price:", _N(take_profit_price, 6), ", Current Price:", _N(price, 6),
                        ", Position Price:", _N(position[0].Price, 6), _EnableMessageSend ? "@" : "#FF1CAE");
                }
            } else {
                // Monitor whether the trigger price for callback take-profit is reached
                trigger_price = position[0].Price * (1 + _TakeProfitTriggerPercent / 100);
                if (price > trigger_price) {
                    _TriggeredTakeProfit = true;                      // Trigger callback take profit
                    _PeakPriceInPosition = price;                     // Record price peak
                    Log("Long position has reached the trigger price for pullback take profit:", _N(trigger_price, 6), ", Current Price:", _N(price, 6), ", Position Price:", _N(position[0].Price, 6));
                }
            }
        } else if (position[0].Type == PD_SHORT) {
            // Short position
            if (_TriggeredTakeProfit) {
                // Trigger price reached, monitor whether to take profit
                _PeakPriceInPosition= price < _PeakPriceInPosition ? price : _PeakPriceInPosition;                                            // Update low price
                if (_UsePositionRetracement) {
                    take_profit_price = _PeakPriceInPosition + (position[0].Price - _PeakPriceInPosition) * (_CallBakcPercent / 100);         // Calculate the take profit price of the callback
                } else {
                    take_profit_price = _PeakPriceInPosition * (1 + _CallBakcPercent / 100);                                                  // Calculate the take profit price of the callback
                }
                if (price > take_profit_price) {
                    coverShort(-1, position[0].Amount);             // close short
                    calculateProfit(ticker);
                    _TriggeredTakeProfit = false;                   // Reset trigger flag
                    _TrendWhenTakeProfitOrStopLoss = -1;            // Record the trend when taking profit
                    _HadTakeProfit = true;                          // A take-profit has occurred
                    Log("Short position pullback take profit: lowest price in the position:", _N(_PeakPriceInPosition, 6), ", Take profit price:", _N(take_profit_price, 6), ", Current Price:", _N(price, 6),
                        ", Position Price:", _N(position[0].Price, 6), _EnableMessageSend ? "@" : "#FF1CAE");
                }
            } else {
                // Monitor whether the trigger price for callback take-profit is reached
                trigger_price = position[0].Price * (1 - _TakeProfitTriggerPercent / 100);
                if (price < trigger_price) {
                    _TriggeredTakeProfit = true;                      // Trigger callback take profit
                    _PeakPriceInPosition = price;                     // Record low price
                    Log("Short position has reached the trigger price for pullback take profit:", _N(trigger_price, 6), ", Current Price:", _N(price, 6), ", Position Price:", _N(position[0].Price, 6));
                }
            }
        }
    }
}

// Place Order
function order(long, short, position, ticker) {
    var position_size = position.length > 0 ? position[0].Amount : 0;
    var position_type = position.length > 0 ? position[0].Type : null;

    if (long) {
        //Trend long
        if ((_HadStopLoss || _HadTakeProfit) && _TrendWhenTakeProfitOrStopLoss == 1) {
            // take-profit or stop-loss occurred, and when it happened, the trend was long, do not go long anymore
            return;
        }
        if (position_size > 0 && position_type == PD_SHORT) {
            coverShort(-1, position_size);
            calculateProfit(ticker);
        } else if (position_size > 0 && position_type == PD_LONG) {
            // Hold multiple positions and do not place repeated orders
            return;
        } else {
            // No position, if it is the first run or strategy restart, need to wait for the price to cross onceEMAOnly place orders with moving average
            if (_PriceCrossEMAStatus != 2) {
                return;
            }
        }
        if (isEnoughAssetToOrder(_OrderSize, ticker)) {
            openLong(-1, _OrderSize);
            _HadStopLoss = false;
            _HadTakeProfit = false;
        } else {
            throw "Not enough money to place an order!";
        }
    } else if (short) {
        // Trend short
        if ((_HadStopLoss || _HadTakeProfit) && _TrendWhenTakeProfitOrStopLoss == -1) {
            // take-profit or stop-loss occurred, and when it happened, the trend was empty, do not go short anymore
            return;
        }
        if (position_size > 0 && position_type == PD_LONG) {
            coverLong(-1, position_size);
            calculateProfit(ticker);
        } else if (position_size > 0 && position_type == PD_SHORT) {
            // Hold a short position and do not place repeated orders
            return;
        } else {
            // No position, if it is the first run or strategy restart, need to wait for the price to cross onceEMAOnly place orders with moving average
            if (_PriceCrossEMAStatus != 2) {
                return;
            }
        }
        if (isEnoughAssetToOrder(_OrderSize, ticker)) {
            openShort(-1, _OrderSize);
            _HadStopLoss = false;
            _HadTakeProfit = false;
        } else {
            throw "Not enough money to place an order!";
        }
    }
}

// Trend Strategy
function trendStrategy() {
    var ticker = _C(exchange.GetTicker);
    var position = _C(exchange.GetPosition);
    var account = _C(exchange.GetAccount);
    var records = _C(exchange.GetRecords, _KLinePeriod * 60);
    if (position.length > 1) {
        Log(position);
        throw "Holding both long and short positions simultaneously!";
    }
    // Strategy Interaction
    runCmd();
    // Status bar information print
    printLogStatus(ticker, account, position);
    // stop loss
    stopLoss(position, ticker);
    // take profit
    takeProfit(position, ticker);
    // Callback to take profit
    trackingTakeProfit(position, ticker);

    // According toKStrategy running on time frame
    if (!runInKLinePeriod(records)) {
        return;
    }
    // Trend judgment and order placement
    var long = false;
    var short = false;
    [long, short] = trendJudgment(records);
    if (!_OnlyTrendJudgment) {
        order(long, short, position, ticker);
    }
}

// Status bar information print
function printLogStatus(ticker, account, position) {
    var table_overview = { type: 'table', title: 'Strategy Overview', cols: ['Start time', 'Days operated', 'Number of Trades', 'Win rate', 'Estimated monthly cost%', 'Estimated annualized%', 'For strategy writing, please contact WeChat'], rows: [] };
    var table_account = { type: 'table', title: 'Account funds', cols: ['Current Assets', 'Initial Assets', 'Available balance', 'Freeze balance', 'Number of orders that can be placed', 'Revenue', 'Revenue%'], rows: [] };
    var table_position = { type: 'table', title: 'Position status', cols: ['Transaction currency', 'Leverage multiple', 'Average position price', 'Direction', 'Quantity', 'Margin', 'Estimated liquidation price', 'Floating profit and loss', 'Floating profit and loss%'], rows: [] };
    var i = 0;

    // Strategy Overview
    var the_running_days = getDaysFromTimeStamp(_StrategyDatas.start_run_timestamp, Unix());
    var monthly_rate_of_profit = 0;
    if (the_running_days > 1)
        monthly_rate_of_profit = _ProfitLocal / _InitAsset / the_running_days * 30;
    table_overview.rows.push([_D(_StrategyDatas.start_run_timestamp * 1000), the_running_days, _TradeCount, _TradeCount == 0 ? 0 : (_N(_TakeProfitCount / _TradeCount * 100, 2) + "%"),
        _N(monthly_rate_of_profit * 100, 2) + "%", _N(monthly_rate_of_profit * 12 * 100, 2) + "%", 'wd1061331106']);
    // Account funds
    var current_asset = getAccountAsset(position, account, ticker);
    var max_order_size = getMaxOrderSize(_MarginLevel, ticker, account);
    var asset_profit = current_asset - _InitAsset;
    var asset_profit_percent = asset_profit / _InitAsset;
    table_account.rows.push([_N(current_asset, 4), _N(_InitAsset, 4), _N(_IsUsdtStandard ? account.Balance : account.Stocks, 4), _N(_IsUsdtStandard ? account.FrozenBalance : account.FrozenStocks, 4),
        max_order_size, _N(asset_profit, 4), _N(asset_profit_percent * 100, 2) + "%"]);
    // Position status
    var position_direction = "";
    var forced_cover_up_price = 0;
    var position_profit_percent = 0;
    var position_profit = 0;
    var position_margin = 0;
    if (position.length == 0) {
        table_position.rows.push(["No position", "-", "-", "-", "-", "-", "-", "-", "-"]);
    } else {
        position_direction = position[0].Type == PD_LONG ? "Long Position" : "Short Position";
        [position_profit, position_profit_percent] = getSinglePositionProfit(position, ticker);
        position_margin = getSinglePositionMargin(position, ticker);
        forced_cover_up_price = calculateForcedPrice(account, position, ticker);
        table_position.rows.push([exchange.GetCurrency(), _MarginLevel, _N(position[0].Price, 4), position_direction, position[0].Amount,
            _N(position_margin, 4), _N(forced_cover_up_price, 4), _N(position_profit, 4), _N((position_profit_percent * 100), 2) + "%"]);
    }
    // Print form
    LogStatus('`' + JSON.stringify(table_overview) + '`\n'
        + '`' + JSON.stringify(table_account) + '`\n'
        + '`' + JSON.stringify(table_position) + '`\n');
}

// Initialize data
function initDatas() {
    saveStrategyRunTime();
    readUserDataLocal();

    _InitAsset = _UserDatas.init_assets;
    _ProfitLocal = _UserDatas.profit_local;
    _TakeProfitCount = _UserDatas.take_profit_count;
    _TradeCount = _UserDatas.trade_count;

    if (_OrderByMargin) {
        getRealOrderSize(-1, _OrderSize);
        Log("The number of orders has been recalculated:", _OrderSize);
    }
    if (_UseTakeProfit && _UseTrackingTakeProfit) {
        throw "Take-profit and trailing take-profit cannot be used simultaneously!";
    }
}

// Set Contract
function setContract() {
    _IsUsdtStandard = _Currency.includes("USDT") ? true : false;
    if (!IsVirtual()) {
        // Real disk settings
        exchange.SetCurrency(_Currency);
        if (_UseQuarter) {
            exchange.SetContractType("quarter");
        } else {
            exchange.SetContractType("swap");
        }
    } else {
        // Backtest settings
        if (_IsUsdtStandard) {
            exchange.SetContractType("swap");
        } else {
            exchange.SetContractType("quarter");
        }
    }
    exchange.SetMarginLevel(_MarginLevel);
    exchange.SetPrecision(_PricePrecision, _AmountPrecision);
}

// main
function main() {
    setContract();
    initDatas();
    while (true) {
        trendStrategy();
        Sleep(_Interval);
    }
}
```

> Detail

https://www.fmz.com/strategy/320782

> Last Modified

2021-12-15 15:31:53
