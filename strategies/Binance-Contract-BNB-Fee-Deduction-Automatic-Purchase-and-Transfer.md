
> Name

Binance-Contract-BNB-Fee-Deduction-Automatic-Purchase-and-Transfer

> Author

Xueqiu Bot

> Strategy Description

Contact : ck@xueqiubot.com / WeChat@stay37
This strategy automatically transfers USDT from the futures account to the spot account to buy BNB, then transfers BNB back to the futures account to offset fees.
Need to add the BNB_USDT trading pair in advance



> Source (python)

``` python
# Contact : ck@xueqiubot.com / WeChat@stay37

import time


def supply_bnb(transfer_usdt,i):
    Log("CurrentBNBInsufficient, supplementBNBUsed as fee deduction")
    #Get CurrentBNB_USDTPrice
    depth = _C(exchanges[i].GetDepth)
    #Transfer outtransfer_usdtIndividual/UnitUSDT
    timestamp = time.time() * 1000
    transfer = exchanges[i].IO("api","POST","/sapi/v1/futures/transfer","asset=USDT&amount="+str(transfer_usdt)+"&type=2&timestamp=+"+str(timestamp))
    time.sleep(1)
    #ObtainBNBDepth, place buy order
    depth = _C(exchanges[i].GetDepth)
    buyamount = round(transfer_usdt / (depth.Asks[0].Price + 0.2) , 2)
    buyid = exchanges[i].Buy(round(depth.Asks[0].Price + 0.1 , 4) , buyamount)
    time.sleep(1)
    #Query purchase results after buyingBNBAnd the remainingUSDTTransfer to contract account
    acc = _C(exchanges[i].GetAccount)
    transfer_usdt = acc.Balance
    transfer_bnb = acc.Stocks
    timestamp = time.time() * 1000
    transfer = exchanges[i].IO("api","POST","/sapi/v1/futures/transfer","asset=USDT&amount="+str(transfer_usdt)+"&type=1&timestamp=+"+str(timestamp))
    transfer = exchanges[i].IO("api","POST","/sapi/v1/futures/transfer","asset=BNB&amount="+str(transfer_bnb)+"&type=1&timestamp=+"+str(timestamp))
    Log("BNBSupplement completed")




def main():
    if 'Insufficient BNB in the contract account':
        #transfer_usdt: Amount of USDT required to purchase
        #i: bnb_usdtIndex of spot trading pair
        supply_bnb(transfer_usdt,i)

```

> Detail

https://www.fmz.com/strategy/236437

> Last Modified

2020-11-11 22:38:54
