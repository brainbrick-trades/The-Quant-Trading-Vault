
> Name

Ghost-Trend-Following-Strategy

> Author

陈皮



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|leverage|true|leverage|
|tickInterval|3000|Polling interval time (milliseconds)|
|orderValue|50|Order value(%)|
|bfCount|168|Number of nodes|
|isFlag|false|Reversal Signal|
|stopSurplus|3|Percentage position reduction|
|stopSurplusCount|50|Reduce position amount(%)|




|Button|Default|Description|
|----|----|----|
|One-click clearance|__button__|One-click clearance|
|Spot=="Contract|10|Transfer USDT from spot account to contract account|
|Contract=="Spot|10|Transfer USDT from contract account to spot account|


> Source (python)

``` python
import json
import traceback
#SYMBOLS = ['1INCH_USDT','ADA_USDT','ALGO_USDT','ATOM_USDT','AVAX_USDT','AAVE_USDT','AXS_USDT',
#           'BAND_USDT','BCH_USDT','BTC_USDT','COMP_USDT','CHZ_USDT','CRV_USDT','CVC_USDT','DOGE_USDT'
#           ,'DOT_USDT','DYDX_USDT','DASH_USDT','EGLD_USDT','ENJ_USDT','ENS_USDT','EOS_USDT','ETH_USDT',
#           'ETC_USDT','FIL_USDT','FTM_USDT','GALA_USDT','GRT_USDT','IOTA_USDT','ICP_USDT','KSM_USDT',
#           'LINK_USDT','LRC_USDT','LTC_USDT','MANA_USDT','MATIC_USDT','NEAR_USDT','OMG_USDT','SAND_USDT',
 #          'SC_USDT','1000SHIB_USDT','SOL_USDT','SRM_USDT','STORJ_USDT','SUSHI_USDT','THETA_USDT','TRX_USDT',
  #         'UNI_USDT','XRP_USDT','XLM_USDT','XMR_USDT','XTZ_USDT','YFI_USDT','ZEC_USDT','PEOPLE_USDT',
  #         'APE_USDT','GMT_USDT','ZIL_USDT','KNC_USDT']
SYMBOLS = ['1INCH_USDT','ALGO_USDT','ATOM_USDT','AVAX_USDT','AAVE_USDT','AXS_USDT',
           'BAND_USDT','BCH_USDT','BTC_USDT','COMP_USDT','CVC_USDT','DOGE_USDT'
           ,'DOT_USDT','DYDX_USDT','DASH_USDT','EGLD_USDT','ENJ_USDT','ENS_USDT','EOS_USDT','ETH_USDT',
           'ETC_USDT','FTM_USDT','GALA_USDT','GRT_USDT','IOTA_USDT','KSM_USDT',
           'LINK_USDT','LRC_USDT','LTC_USDT','MANA_USDT','MATIC_USDT','NEAR_USDT','OMG_USDT','SAND_USDT',
           'SC_USDT','SOL_USDT','SRM_USDT','SUSHI_USDT','THETA_USDT','TRX_USDT',
           'UNI_USDT','XRP_USDT','XLM_USDT','XMR_USDT','XTZ_USDT','YFI_USDT','ZEC_USDT','PEOPLE_USDT',
           'APE_USDT','ZIL_USDT','KNC_USDT']
#Main Function
def main():
    try:
        while True:
            flage = ext.GetStopService()
            if flage == 1:
                break
            #Strategy Interaction
            ext.GetCommandService()
            #Coin Selection Function
            ext.GetSymbolService()
            #Order Signal 
            ext.FirstSignalService()
            #Reduce Position Signal
            ext.StopSurplusService()
            #Display Data
            ext.UpdateLogStatusService()
            Sleep(tickInterval)
    except Exception as e:
        Log(traceback.format_exc())
        Log("Strategy has stopped, please check promptly@")
    
#Initialization function        
def init():
    Log("Strategy Start")
    #Set contract perpetual
    if len(exchanges) != 2:
        Log("Need to set up two sets of trading pairs")
        return
    symbolRecord = _G("symbolRecord")
    Log("symbolRecord:",symbolRecord)
    if symbolRecord is not None:
        symbol = symbolRecord['symbol']
        exchange.SetCurrency(symbol) 
    _G("symbolRecord",None)
    exchange.SetContractType("swap")
    exchange.SetMarginLevel(leverage)
    exchanges[1].SetContractType("swap")
    exchanges[1].SetMarginLevel(leverage)
    _G("orderValue",orderValue)
    _G("leverage",leverage)
    _G("bfCount",bfCount)
    _G("symbols",SYMBOLS)
    _G("isFlag",isFlag)
    _G("isUpdate",0)
    _G("stopSurplus",stopSurplus)
    _G("stopSurplusCount",stopSurplusCount)
    Log("All trading targets:",SYMBOLS)
    if _G("initialTotalMarginBalance") is None:
        info = exchange.GetAccount().Info
        if info is None or info == {}:
            Log("Unable to obtain futures data, cannot operate")
            return
        _G("initialTotalMarginBalance", round(float(info.totalMarginBalance),2))#Initial amount
    if _G("drawIn") is None:
        _G("drawIn",0)
    if _G("drawOut") is None:
        _G("drawOut",0)
    ext.ClearAllService()
    
    
#Cleanup Function   
def onexit():
     #Close Position
    #ext.ClearanceService()
    ext.UpdateLogStatusService()
    #Log("All positions closed")
    Log("Strategy stopped")    
    
```

> Detail

https://www.fmz.com/strategy/363409

> Last Modified

2022-10-01 01:51:21
