
> Name

MartinGale-Strategy1

> Author

Zer3192





> Source (javascript)

``` javascript
// At/InFMZExample of implementing Martingale on the platform
function main() {
  // Set basic parameters
  var initAsset = 1000000; // Initial Assets
  var baseBet = 0.001; // Base Unit Price
  var profitRate = 0.2; // Add-on ratio when profitable
  var lossRate = 0.5; // Add-on ratio when losing
  var maxBetTimes = 10; // Maximum number of add-ons
  var maxLoseTimes = 4; // Consecutive loss count

  // Initialize parameters
  var asset = initAsset; // Current Assets
  var bet = baseBet; // Current Lot Size
  var betTimes = 0; // Current add-on count
  var loseTimes = 5; // Current consecutive loss count
  var win = 0; // Current consecutive win count

  // Order Function
  function placeOrder(direction) {
    var amount = bet; // Order Quantity
    if (direction == "buy") {
      // buy
      exchange.Buy(-1,bet);
      Log("buy", bet);
    } else if (direction == "sell") {
      // sell
      exchange.Sell(-1,bet);
      Log("sell", bet);
    }
  }

  // Trading Loop
  while (true) {
    // Get CurrentKInformation Above the Line
    var records = exchange.GetRecords();
    var lastRecord = records[records.length - 1];
    var currPrice = lastRecord.Close;

    // Determine current trend
    var trend = "none";
    if (lastRecord.Open < lastRecord.Close) {
      trend = "up";
    } else if (lastRecord.Open > lastRecord.Close) {
      trend = "down";
    }

    // Execute trades based on trend
    if (trend == "up") {
      // If rising
      if (loseTimes > 0) {
        // If there were previous losses, reset the number of added bets and consecutive losses
        betTimes = 0;
        loseTimes = 0;
      }
      placeOrder("buy");
      
      win++;
      if (win == maxBetTimes) {
        // If the number of consecutive wins reaches the maximum number of raises, reset
        betTimes = 0;
        win = 0;
      }
    } else if (trend == "down") {
      // If falling
      if (win > 0) {
        // If there was a previous win, reset the number of add-on bets
        betTimes = 0;
      }
      if (loseTimes == maxLoseTimes) {
        // If the number of consecutive losses reaches the maximum number, stop trading
        break;
      }
      if (betTimes == 0) {
        // If it is the first add-on, calculate the add-on amount
        bet *= (1 + lossRate);
      } else {
        // If it is not the first time to raise, calculate the amount of the raise
        bet *= 1.1;
      }
      placeOrder("sell");
      loseTimes++;
      betTimes++;
    }

    // Update Assets
    var currAsset = exchange.GetAccount().Balance;
    if (currAsset > asset) {
      // Profit, Add Bet
      bet *= (1 + profitRate);
    }
    asset = currAsset;

    // Wait for next trade
    Sleep(1000);
  }
}

```

> Detail

https://www.fmz.com/strategy/416875

> Last Modified

2023-07-12 17:41:56
