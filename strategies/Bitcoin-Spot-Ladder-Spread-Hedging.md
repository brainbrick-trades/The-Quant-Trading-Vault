
> Name

Bitcoin-Spot-Ladder-Spread-Hedging

> Author

我要发

> Strategy Description

Ladder price difference hedging, beginner strategy

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|jizhun|true|Benchmark|
|fanwei|5|Scope|
|maxliang|0.5|Maximum Order|
|xianbijia|6000|Recent Coin Price|
|lirun|true|profit|
|zhanghushu|12|Account Quantity|


> Source (javascript)

``` javascript
function main() {

    var dongjieqian = 0;
    var lessbuyx = 33;
    var lesssellx = 33;
    var lastlessbuyx = 0
    var lastlesssellx = 0
    var huai = 0;
    var hbss;
    var okss;
    var accounthb;
    var accountok;
    var depthok;
    var depthhb;
    var bok;
    var bokl;
    var sok;
    var sokl;
    var bhb;
    var bhbl;
    var shb;
    var shbl;
    var qok;
    var cok;
    var qhb;
    var chb;
    var xx = 0;
    var yy = 0;
    var lastdepthhb = exchanges[0].GetDepth();
    var lastdepthok = exchanges[1].GetDepth();
    var hbx; //Huobi Sell Level
    var hby; //Huobi Buy Level
    var cps; //Trigger price for Huobi sell
    var iam; //Trading Quantity
    var huajia; //Slippage
    var ii; //Used to determine whether Huobi is trading
    var shiyongjizhun; //Use Benchmark
    shiyongjizhun = jizhun;
    while (true) {
        var tss = new Date();
        Log("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        var ts = new Date();
        Log("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@");

        Log("Start time for retrieving account funds", ts.getSeconds());

        // Below is account retrieval
        var accounts = [];
        while (true) {
            for (var i = 0; i < exchanges.length; i++) {
                if (accounts[i] == null) {
                    // Create Asynchronous Operation
                    accounts[i] = exchanges[i].Go("GetAccount");
                }
            }
            var failed = 0;
            for (var i = 0; i < exchanges.length; i++) {
                if (typeof(accounts[i].wait) != "undefined") {
                    // Waiting for results
                    var ret = accounts[i].wait();
                    if (ret) {
                        accounts[i] = ret;
                        Log(exchanges[i].GetName(), accounts[i]);
                    } else {
                        // Try again
                        accounts[i] = null;
                        failed++;
                    }
                }
            }
            if (failed == 0) {
                break;
            } else {
                break;
            }
        }

        Log("Time taken to retrieve account funds ", (new Date().getTime() - ts.getTime()) / 1000, "second");
        Log("*********************************************************************");

       




        var ts = new Date();
        Log("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@");

        Log("Start fetching Huobi unfulfilled orders", ts.getSeconds());
        var orders = exchanges[0].GetOrders()
        Log(orders);
        var fb = 0,
            fs = 0;
        if (orders === null) {} else {
            for (var i = 0; i < orders.length; i++) {
                if (orders[i].Type === 1) {
                    fs = fs + orders[i].Amount - orders[i].DealAmount
                }

                if (orders[i].Type === 0) {
                    fb = fb + orders[i].Amount * orders[i].Price - orders[i].DealAmount * orders[i].AvgPrice
                }
            }
        }


        Log("Huobi Frozen Funds ", fb, "Frozen coins", fs);
        Log("Time taken to fetch Huobi unfulfilled orders ", (new Date().getTime() - ts.getTime()) / 1000, "second");
        Log("*********************************************************************");


        accounthb = accounts[0];
        accountok = accounts[1];
        Log(accounts[0]);
        Log(accounts[1]);

        if (!accounthb) {
            Log("Failed to get Huobi account information");
            continue;
        }
        if (!accountok) {
            Log("ObtainokAccount Information Failed");
            continue;
        }


        qok = accountok.Balance;
        cok = accountok.Stocks;
        qhb = accounthb.Balance;
        chb = accounthb.Stocks;


        Log("Total Frozen Funds=", accountok.FrozenBalance + fb + accountok.FrozenStocks * xianbijia + fs * xianbijia)
        if (accountok.FrozenBalance + fb + accountok.FrozenStocks * xianbijia + fs * xianbijia > 2500) {
            Log("Frozen funds exceed the limit");
            continue;
        }
        //Sellable Amount on Huobi chb 
        //okBuyable Amount qok/sok 
        //Take the Smaller of the TwoMath.min(chb,qok/sok)
        //Already Sold Amount on Huobi qhb/bhb 
        //okAmount Already Bought cok 
        //Take the Smaller of the TwoMath.min(cok,qhb/bhb)
        //Extent already sold on Huobi hbx=Math.min(cok,qhb/bhb)/(Math.min(chb,qok/sok)+Math.min(cok,qhb/bhb))



        //---------------
        // Get Market Depth
        var ts = new Date();
        Log("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@");

        Log("Start time for retrieving market depth", ts.getSeconds());
        var depths = [];
        while (true) {
            for (var i = 0; i < exchanges.length; i++) {
                if (depths[i] == null) {
                    // Create Asynchronous Operation
                    depths[i] = exchanges[i].Go("GetDepth");
                }
            }
            var failed = 0;
            for (var i = 0; i < exchanges.length; i++) {
                if (typeof(depths[i].wait) != "undefined") {
                    // Waiting for results         
                    var ret = depths[i].wait();
                    if (ret) {
                        depths[i] = ret;

                        Log(exchanges[i].GetName(), depths[i]);
                    } else {
                        // Try again
                        depths[i] = null;
                        failed++;
                    }
                }
            }
            if (failed == 0) {
                break;
            } else {
                break;


            }
        }
        depthhb = depths[0];
        depthok = depths[1];
        //Determine whether depth is valid
        if (!depthhb) {
            Log("Failed to get Huobi depth information");
            continue;
        }
        if (!depthok) {
            Log("ObtainokDepth Information Failed");
            continue;
        }




        if (depthhb.Bids[0].Price === lastdepthhb.Bids[0].Price && depthhb.Bids[0].Amount === lastdepthhb.Bids[0].Amount && depthhb.Asks[0].Price === lastdepthhb.Asks[0].Price && depthhb.Asks[0].Amount === lastdepthhb.Asks[0].Amount) {

            ++xx;
  Log(xx);

        } else {
            xx = 0;
        }
    if(depthok.Bids[0].hasOwnProperty("Price") ){Log("ContainspriceAttribute")}else{Log("Not includedpriceAttribute");continue}
       
    if (depthok.Bids[0].Price === lastdepthok.Bids[0].Price && depthok.Bids[0].Amount === lastdepthok.Bids[0].Amount && depthok.Asks[0].Price === lastdepthok.Asks[0].Price && depthok.Asks[0].Amount === lastdepthok.Asks[0].Amount) {

            ++yy;
             Log(yy);
        } else {
            yy = 0;
        }
        lastdepthhb = depthhb;
        lastdepthok = depthok;
        if (xx> 20) {
            Log("Invalid Huobi Depth");
            continue;
        }
        if (yy > 20) {
            Log("okDepth Invalid");
            continue;
        }
        bok = depthok.Bids[0].Price;
        bokl = depthok.Bids[0].Amount;
        sok = depthok.Asks[0].Price;
        sokl = depthok.Asks[0].Amount;
        bhb = depthhb.Bids[0].Price;
        bhbl = depthhb.Bids[0].Amount;
        shb = depthhb.Asks[0].Price;
        shbl = depthhb.Asks[0].Amount;
        Log("Huobi Buy One", bhb, "Huobi Sell One", shb, "Huobi Order Book Spread", shb - bhb);
        Log("okSell one", sok, "okBuy one", bok, "okMarket depth difference", sok - bok);
        Log("Time taken to get market depth ", (new Date().getTime() - ts.getTime()) / 1000, "second");
        Log("*********************************************************************");


        //Calculating buy and sell supplemental coefficients below
        //If=33 Calculate if not equal to33,Not calculated
        if (lesssellx === 33) {
            Log("Calculate the quantity to buy or sell less")

            dongjieqian = accountok.FrozenBalance + fb;
            if (dongjieqian < 5) {
                dongjieqian = 0
            }
            lesssellx = dongjieqian / (bok * zhanghushu)
            lessbuyx = (accountok.FrozenStocks + fs) / zhanghushu
        }


        Log("Short selling quantity=", lesssellx, "Buy fewer=", lessbuyx)




        //Calculating Huobi selling situation below
        while (true) {
            ii = 0; //Huobi Untraded
            //Sellable Amount on Huobi chb 
            //okBuyable Amount qok/sok 
            //Take the Smaller of the TwoMath.min(chb,qok/sok)
            //Already Sold Amount on Huobi qhb/bhb 
            //okAmount Already Bought cok 
            //Take the Smaller of the TwoMath.min(cok,qhb/bhb)

            hbx = Math.min(cok, qhb / bhb) / (Math.min(chb, qok / sok) + Math.min(cok, qhb / bhb));
            Log("Huobi Selling Degree", hbx);
          /*  if (hbx > 0.5) {
                if (shiyongjizhun + fanwei * 0.5 > 0) {
                    Log("Center right, move right, speed reduction coefficient=", 1 - (shiyongjizhun + fanwei * 0.5) / 5);
                    shiyongjizhun = shiyongjizhun + 0.001 * (1 - (shiyongjizhun + fanwei * 0.5) / 5) * (hbx - 0.5);
                    Log("Use Benchmark=", shiyongjizhun, "Increase", 0.001 * (1 - (shiyongjizhun + fanwei * 0.5) / 5) * (hbx - 0.5));
                } else {
                    Log("Center left, move right, speed increase coefficient=", 1 - (shiyongjizhun + fanwei * 0.5) / 5);

                    shiyongjizhun = shiyongjizhun + 0.001 * (1 - (shiyongjizhun + fanwei * 0.5) / 5) * (hbx - 0.5);
                    Log("Use Benchmark=", shiyongjizhun, "Increase", 0.001 * (1 - (shiyongjizhun + fanwei * 0.5) / 5) * (hbx - 0.5));
                }

            } else {
                if (shiyongjizhun + fanwei * 0.5 > 0) {
                    Log("Center right, move left, speed increase coefficient=", 1 + (shiyongjizhun + fanwei * 0.5) / 5);
                    shiyongjizhun = shiyongjizhun + 0.001 * (1 + (shiyongjizhun + fanwei * 0.5) / 5) * (hbx - 0.5);
                    Log("Use Benchmark=", shiyongjizhun, "Reduce", 0.001 * (1 + (shiyongjizhun + fanwei * 0.5) / 5) * (hbx - 0.5));
                } else {
                    Log("Center left, move left, speed reduction coefficient=", 1 + (shiyongjizhun + fanwei * 0.5) / 5);
                    shiyongjizhun = shiyongjizhun + 0.001 * (1 + (shiyongjizhun + fanwei * 0.5) / 5) * (hbx - 0.5);
                    Log("Use Benchmark=", shiyongjizhun, "Reduce", 0.001 * (1 + (shiyongjizhun + fanwei * 0.5) / 5) * (hbx - 0.5));


                }

            }*/


            cps = shiyongjizhun + fanwei * hbx;
            if (cps > ((bhb - sok))) {
                Log("Huobi Sold Level", hbx,"First Trigger Spread", cps, "Actual Difference", bhb-sok, "Will not trigger the first type");
                break;
            }
            huajia = Math.abs((bhb - sok - cps) / 2) + 0.25 * lirun;
            huajia = _N(huajia, 2);
            iam = Math.min(chb, qok / (sok + huajia), bhbl, sokl, maxliang);
            iam = _N(iam, 2);
            Log("First Largest Volume=", maxliang)
            Log("Degree", hbx, "Sell on Huobi to at least earn the price difference", cps, "Actual Profit Spread", bhb - sok, "Slippage=(1/2Actual Profit Spread-Minimum Profit Spread)+0.25profit=", huajia, "Order Quantity", iam);

            if (iam < 0.01) {
                break;
            } else {
                var hbid = exchanges[0].Go("Sell", bhb - huajia, Math.max((iam - lesssellx), 0.01));
                var okid = exchanges[1].Buy(sok + huajia, Math.max((iam - lessbuyx), 0.01));
                lastlesssellx = lesssellx;
                lastlessbuyx = lessbuyx;
                lesssellx = 33;
                lessbuyx = 33;
                ++ii; //Huobi has traded
                ++huai;
                /* Do not calculate loss rate, accelerate      
         Sleep(200);
          
    hbid = hbid.wait()
                if (!hbid) {
                   
                    break;
                }
                var order = exchanges[0].GetOrder(hbid);
                if (!order) {
                   
                    break;
                }
                hbss = bhb * Math.max((iam-lastlesssellx),0.01) - order.DealAmount * order.AvgPrice - (bhb - huajia) * (Math.max((iam-lastlesssellx),0.01) - order.DealAmount);
                Log(order);
                Log(hbss, "Lost Money=", "Huobi Buy One", bhb, "*", "Order Quantity", Math.max((iam-lastlesssellx),0.01), "-", "Transaction volume", order.DealAmount, "*", "Average Transaction Price", order.AvgPrice, "-(", "Huobi Buy One", bhb, "-", "Slippage", huajia, ")", "*", "(", "Order Quantity", Math.max((iam-lastlesssellx),0.01), "-", "Transaction volume", order.DealAmount);
                Log(Math.max((iam-lastlesssellx),0.01) * huajia);
                Log("Huobi sell loss rate=", hbss / (Math.max((iam-lastlesssellx),0.01) * huajia))
                
           */

                /* Do not calculate loss rate, accelerate 
                  if (!okid) {

                      break;
                  }
                  var order = exchanges[1].GetOrder(okid);
                  if (!order) {
                    
                      break;
                  }

                  okss = 0 - sok * Math.max((iam-lastlessbuyx),0.01) + order.DealAmount * order.AvgPrice + (sok + huajia) * (Math.max((iam-lastlessbuyx),0.01) - order.DealAmount);
                  Log(order);

                  Log(okss, "Lost Money=", "-okSell one", sok, "*", "Order Quantity", Math.max((iam-lastlessbuyx),0.01), "+", "Transaction volume", order.DealAmount, "*", "Average Transaction Price", order.AvgPrice, "+(", "okSell one", sok, "+", "Slippage", huajia, ")", "*", "(", "Order Quantity", Math.max((iam-lastlessbuyx),0.01), "-", "Transaction volume", order.DealAmount);
                  Log(Math.max((iam-lastlessbuyx),0.01) * huajia);
                  Log("okBuy loss rate=", okss / (Math.max((iam-lastlessbuyx),0.01) * huajia))
                  
                    */


                break;


            }

            //Trigger pricecps=jizhun+fanwei*hbx
            //Order quantityMath.min(chb,qok/(sok+Slippage),bhbl,sokl,maxliang)
            //If the order quantity is less than0.01 break else Place Huobi Sell Order okPlace an order next break
        }
        //Calculating Huobi buying situation below
        while (true) {
            if (ii) {
                Log("Already traded on Huobi");
                break;
            } //Already traded on Huobi
            Log("Never traded before, check the latter situation");
            //Amount Huobi can buy qhb/shb
            //okAmount that can be sold cok 
            //Take the Smaller of the TwoMath.min(cok,qhb/shb)
            //Amount already bought on Huobi   chb
            //okAmount sold qok/bok
            //Take the Smaller of the TwoMath.min(chb,qok/bok)
            hby = Math.min(chb, qok / bok) / (Math.min(chb, qok / bok) + Math.min(cok, qhb / shb)); //The range already bought on Huobi
            cps = shiyongjizhun + fanwei - lirun - fanwei * hby;
            if (cps < ((shb - bok))) {
                Log("Degree of purchase on Huobi", hby,"Second trigger price difference", cps, "Actual Difference", shb-bok, "Did not trigger the second type");
                break;
            }
            huajia = Math.abs((cps - shb + bok) / 2) + 0.25 * lirun;
            huajia = _N(huajia, 2); //Go here
            iam = Math.min(cok, qhb / (shb + huajia), bokl, shbl, maxliang);
            iam = _N(iam, 2);
            Log("The second largest=", maxliang)
            Log("Second degree", hby, "Buy the most on Huobi to minimize loss from price difference", cps, "Actual Loss Spread", shb - bok, "Slippage=(1/2Maximum Loss Spread-Actual Loss Spread)+0.25profit=", huajia, "Order Quantity", iam);

            if (iam < 0.01) {
                break;
            } else {
                var hbid = exchanges[0].Go("Buy", shb + huajia, Math.max((iam - lessbuyx), 0.01));
                var okid = exchanges[1].Sell(bok - huajia, Math.max((iam - lesssellx), 0.01));
                lastlesssellx = lesssellx;
                lastlessbuyx = lessbuyx;
                lesssellx = 33;
                lessbuyx = 33;
                ++huai;
                /* Do not calculate loss rate, accelerate      
                 Sleep(200);
                 hbid = hbid.wait()
                 if (!hbid) {

                     break;
                 }
                 var order = exchanges[0].GetOrder(hbid);
                 if (!order) {
                     
                     break;
                 }

                 hbss = 0 - shb * Math.max((iam-lastlessbuyx),0.01) + order.DealAmount * order.AvgPrice + (shb + huajia) * (Math.max((iam-lastlessbuyx),0.01) - order.DealAmount);
                 Log(order);

                 Log(hbss, "Lost Money=", "-Huobi Sell One", shb, "*", "Order Quantity", Math.max((iam-lastlessbuyx),0.01), "+", "Transaction volume", order.DealAmount, "*", "Average Transaction Price", order.AvgPrice, +"(", "Huobi Sell One", shb, "+", "Slippage", huajia, ")", "*", "(", "Order Quantity", Math.max((iam-lastlessbuyx),0.01), "-", "Transaction volume", order.DealAmount);
                 Log(Math.max((iam-lastlessbuyx),0.01) * huajia);
                 Log("Huobi buy loss rate=", hbss / (Math.max((iam-lastlessbuyx),0.01) * huajia))

               
                 if (!okid) {
                    
                     break;
                 }
                 var order = exchanges[1].GetOrder(okid);
                 if (!order) {
                    
                     break;
                 }
                 okss = bok * Math.max((iam-lastlesssellx),0.01) - order.DealAmount * order.AvgPrice - (bok - huajia) * (Math.max((iam-lastlesssellx),0.01) - order.DealAmount);
                 Log(order);
                 Log(okss, "Lost Money=", "okBuy one", bok, "*", "Order Quantity", Math.max((iam-lastlesssellx),0.01), "-", "Transaction volume", order.DealAmount, "*", "Average Transaction Price", order.AvgPrice, "-(", "okBuy one", bok, "-", "Slippage", huajia, ")", "*", "(", "Order Quantity", Math.max((iam-lastlesssellx),0.01), "-", "Transaction volume", order.DealAmount);
                 Log(Math.max((iam-lastlesssellx),0.01) * huajia);
                 Log("okSelling loss rate=", okss / (Math.max((iam-lastlesssellx),0.01) * huajia))
                 
                  */
                break;
            }


        }
        Log("Total usage time ", (new Date().getTime() - tss.getTime()) / 1000, "second!!!!!!!");
        if ((new Date().getTime() - ts.getTime()) < 500) {
            Sleep(500 - (new Date().getTime() - ts.getTime()))
        }


    }
}
```

> Detail

https://www.fmz.com/strategy/30573

> Last Modified

2017-01-26 22:10:43
