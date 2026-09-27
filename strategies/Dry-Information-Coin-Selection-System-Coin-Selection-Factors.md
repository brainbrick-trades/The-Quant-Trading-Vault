
> Name

Dry-Information-Coin-Selection-System-Coin-Selection-Factors

> Author

陈皮





> Source (python)

``` python
import numpy as np
from scipy.stats import norm
from sklearn import preprocessing
import json

#Calculate Volatility Factor Value
def GetAtrFactorService(records):
    atrlength = 14
    atrs = TA.ATR(records, atrlength)
    acs = sorted(range(len(atrs)), key=lambda k: atrs[k])
    ac = acs[-1]
    arr_mean = np.mean(acs)
    arr_std = np.std(acs,ddof=1)
    p = norm.cdf(x=ac, loc=arr_mean, scale = arr_std)
    #PThe larger the value, the greater the volatility
    atrFactor = _N(p,3)
    return atrFactor 

#Calculate the behavior trace factor value of the organization        
def GetITFactorService(records):
    #Benford's law distribution frequency
    PN = [301, 176, 125, 97, 79, 67, 58, 51, 46]
    FN = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(records)):
        valume = records[i]['Volume']*10000
        strValume = str(valume)
        num = strValume[0]
        for j in range(len(FN)):
            key = j + 1
            if int(num) == key:
                FN[j] += 1
    if sum(FN) == 0:
        FN = PN
    X = 0
    for i in range(len(PN)):
        X += (FN[i] - PN[i])**2
    ITFactor = X
    #X The larger the value, the greater the deviation of transaction volume data from Benford's ideal distribution, and the more pronounced the traces of institutional behavior.
    return ITFactor

#Calculate the price factor value
def GetPriceFactorService(records):
    record = records[-1]
    price = record["Close"]
    PFactor = 1/price 
    #PFactorThe larger the value, the lower the price 
    return PFactor 

#Standardization   --The calculated factor values need to be standardized due to different magnitudes. Missing values and outliers are not handled for now.
def StandardizedService(factor):
    # Standardization
    factorArray = np.asarray(factor)
    factorArray = preprocessing.scale(factorArray)
    factor = factorArray.tolist()

ext.GetAtrFactorService = GetArtFactorService 
ext.GetITFactorService = GetITFactorService 
ext.GetPriceFactorService = GetPriceFactorService 
ext.StandardizedService = StandardizedService
```

> Detail

https://www.fmz.com/strategy/344801

> Last Modified

2022-02-12 11:17:18
