
> Name

Indicator-Library-Python-Version

> Author

陈皮





> Source (python)

``` python
# 0Level: Core utility functions
# 1Level: Application layer function (implemented through level 0 core functions))
# 2Level: Technical indicator functions (all implemented through level 0 and level 1 functions)

import math
import numpy as np
import pandas as pd


#------------------ 0Level: Core utility functions --------------------------------------------      
def RD(N,D=3):   return np.round(N,D)        #Round To3decimal places 
def RET(S,N=1):  return np.array(S)[-N]      #Return the last in the sequenceNvalues,Default return the last one
def ABS(S):      return np.abs(S)            #ReturnNabsolute value
def MAX(S1,S2):  return np.maximum(S1,S2)    #Sequencemax
def MIN(S1,S2):  return np.minimum(S1,S2)    #Sequencemin
         
def MA(S,N):              #Request the sequenceNDaily average value, return the sequence                    
    return pd.Series(S).rolling(N).mean().values    

#QuoteXAt/InNValue from N periods ago
#For Example:REF(CLOSE,5)  #Indicates referencing the previous ... of the current period5The closing price of a period; if it is a daily period, it is the5Closing price of N trading days ago
def REF(S, N=1):          #Shift the entire sequence downwardN,Return the sequence(shiftWill generate afterwardNAN)    
    return pd.Series(S).shift(N).values  

def DIFF(S, N=1):         #Previous value minus next value,Will Occur Beforenan 
    return pd.Series(S).diff(N)  #np.diff(S)Delete directlynan,Will miss a line

def STD(S,N):             #Request the sequenceNDaily standard deviation, return sequence    
    return  pd.Series(S).rolling(N).std(ddof=0).values     

def IF(S_BOOL,S_TRUE,S_FALSE):   #Boolean sequence judgment return=S_TRUE if S_BOOL==True  else  S_FALSE
    return np.where(S_BOOL, S_TRUE, S_FALSE)

def SUM(S, N):            #Take the sequenceNCumulative sum over days, return sequence    N=0Sum all elements of the sequence in order         
    return pd.Series(S).rolling(N).sum().values if N>0 else pd.Series(S).cumsum()  

def HHV(S,N):             # HHV(C, 5)  # Recent5Daily closing highest price        
    return pd.Series(S).rolling(N).max().values     

def LLV(S,N):             # LLV(C, 5)  # Recent5Daily closing lowest price     
    return pd.Series(S).rolling(N).min().values    

def EMA(S,N):             #Exponential moving average,For accuracy S>4*N  EMAAt least needed120timeframe     alpha=2/(span+1)    
    return pd.Series(S).ewm(span=N, adjust=False).mean().values     

def SMA(S, N, M=1):        #Chinese-styleSMA,At least needed120Accurate Only in Cycle (Snowball180timeframe)    alpha=1/(1+com)
    return pd.Series(S).ewm(com=N-M, adjust=True).mean().values     

def AVEDEV(S,N):           #Average absolute deviation  (The average of the absolute difference between the sequence and its mean)   
    return pd.Series(S).rolling(N).apply(lambda x: (np.abs(x - x.mean())).mean()).values 

def SLOPE(S,N,RS=False):    #ReturnSSequenceNPeriod linear regression slope (By default, only return the slope,Do not return the entire line sequence)
    M=pd.Series(S[-N:]);   poly = np.polyfit(M.index, M.values,deg=1);    Y=np.polyval(poly, M.index); 
    if RS: return Y[1]-Y[0],Y
    return Y[1]-Y[0]

  
#------------------   1Level: Application layer function (implemented through level 0 core functions)) ----------------------------------
def COUNT(S_BOOL, N):                  # COUNT(CLOSE>O, N):  RecentNDays of satisfactionS_BOOdays  Truedays
    return SUM(S_BOOL,N)    

def EVERY(S_BOOL, N):                  # EVERY(CLOSE>O, 5)   RecentNWhether All Days AreTrue
    R=SUM(S_BOOL, N)
    return  IF(R==N, True, False)
  
def LAST(S_BOOL, A, B):                #FormerlyADays agoBDay Continuously MeetsS_BOOLcondition   
    if A<B: A=B                        #Requirement A>B Example: LAST(CLOSE>OPEN,5,3) Whether the positive line has been closed from 5 days ago to 3 days ago     
    return S_BOOL[-A:-B].sum()==(A-B)  #Return a single boolean value    

def EXIST(S_BOOL, N=5):                # EXIST(CLOSE>3010, N=5)  nWhether there is a day within the day greater than3000o'clock/point
    R=SUM(S_BOOL,N)    
    return IF(R>0, True ,False)

def BARSLAST(S_BOOL):                  #From the last condition met to the current period  
    M=np.argwhere(S_BOOL);             # BARSLAST(CLOSE/REF(CLOSE)>=1.1) Number of days from the last limit-up to today
    return len(S_BOOL)-int(M[-1])-1  if M.size>0 else -1

def FORCAST(S,N):                      #ReturnSSequenceNPredicted value after periodic linear regression
    K,Y=SLOPE(S,N,RS=True)
    return Y[-1]+K
  
def CROSS(S1,S2):                      #Determine crossing CROSS(MA(C,5),MA(C,10))               
    CROSS_BOOL=IF(S1>S2, True ,False)   
    return COUNT(CROSS_BOOL>0,2)==1    #Cross Up: Yesterday0 Today1   Cross Down: Yesterday1 Today0



#------------------   2Level: Technical indicator functions (all implemented through level 0 and level 1 functions) ------------------------------
def MACD(CLOSE,SHORT=12,LONG=26,M=9):            # EMARelationship,STake120Day, and Snowball decimal point2Same phase
    DIF = EMA(CLOSE,SHORT)-EMA(CLOSE,LONG);  
    DEA = EMA(DIF,M);      MACD=(DIF-DEA)*2
    return RD(DIF),RD(DEA),RD(MACD)

def KDJ(CLOSE,HIGH,LOW, N=9,M1=3,M2=3):         # KDJIndicator
    RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    K = EMA(RSV, (M1*2-1));    D = EMA(K,(M2*2-1));        J=K*3-D*2
    return K, D, J

def RSI(CLOSE, N=24):                           # RSIIndicator,And Tongdaxin decimal point2Same phase
    DIF = CLOSE-REF(CLOSE,1) 
    return RD(SMA(MAX(DIF,0), N) / SMA(ABS(DIF), N) * 100)  

def WR(CLOSE, HIGH, LOW, N=10, N1=6):            #W&R William's indicator
    WR = (HHV(HIGH, N) - CLOSE) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    WR1 = (HHV(HIGH, N1) - CLOSE) / (HHV(HIGH, N1) - LLV(LOW, N1)) * 100
    return RD(WR), RD(WR1)

def BIAS(CLOSE,L1=6, L2=12, L3=24):              # BIASDeviation rate
    BIAS1 = (CLOSE - MA(CLOSE, L1)) / MA(CLOSE, L1) * 100
    BIAS2 = (CLOSE - MA(CLOSE, L2)) / MA(CLOSE, L2) * 100
    BIAS3 = (CLOSE - MA(CLOSE, L3)) / MA(CLOSE, L3) * 100
    return RD(BIAS1), RD(BIAS2), RD(BIAS3)

def BOLL(CLOSE,N=20, P=2):                       #BOLLIndicator, Bollinger Bands    
    MID = MA(CLOSE, N); 
    UPPER = MID + STD(CLOSE, N) * P
    LOWER = MID - STD(CLOSE, N) * P
    return RD(UPPER), RD(MID), RD(LOWER)    

def PSY(CLOSE,N=12, M=6):  
    PSY=COUNT(CLOSE>REF(CLOSE,1),N)/N*100
    PSYMA=MA(PSY,M)
    return RD(PSY),RD(PSYMA)

def CCI(CLOSE,HIGH,LOW,N=20):  
    TP=(HIGH+LOW+CLOSE)/3
    return (TP-MA(TP,N))/(0.015*AVEDEV(TP,N))
        
def ATR(CLOSE,HIGH,LOW, N=20):                    #True volatilityNDaily average
    TR = MAX(MAX((HIGH - LOW), ABS(REF(CLOSE, 1) - HIGH)), ABS(REF(CLOSE, 1) - LOW))
    return MA(TR, N)

def BBI(CLOSE,M1=3,M2=6,M3=12,M4=20):             #BBILong-short indicator   
    return (MA(CLOSE,M1)+MA(CLOSE,M2)+MA(CLOSE,M3)+MA(CLOSE,M4))/4    

def DMI(CLOSE,HIGH,LOW,M1=14,M2=6):               #Trend indicator: results are completely consistent with Tonghuashun and Tongda Xin
    TR = SUM(MAX(MAX(HIGH - LOW, ABS(HIGH - REF(CLOSE, 1))), ABS(LOW - REF(CLOSE, 1))), M1)
    HD = HIGH - REF(HIGH, 1);     LD = REF(LOW, 1) - LOW
    DMP = SUM(IF((HD > 0) & (HD > LD), HD, 0), M1)
    DMM = SUM(IF((LD > 0) & (LD > HD), LD, 0), M1)
    PDI = DMP * 100 / TR;         MDI = DMM * 100 / TR
    ADX = MA(ABS(MDI - PDI) / (PDI + MDI) * 100, M2)
    ADXR = (ADX + REF(ADX, M2)) / 2
    return PDI, MDI, ADX, ADXR  

def TAQ(HIGH,LOW,N):                               #Donchian Channel(Turtle)Trading indicators, simple and simple, can go through bulls and bears
    UP=HHV(HIGH,N);    DOWN=LLV(LOW,N);    MID=(UP+DOWN)/2
    return UP,MID,DOWN

def KTN(CLOSE,HIGH,LOW,N=20,M=10):                 #Keltner Trading Channel, NChoose20day,ATRChoose10day
    MID=EMA((HIGH+LOW+CLOSE)/3,N)
    ATRN=ATR(CLOSE,HIGH,LOW,M)
    UPPER=MID+2*ATRN;   LOWER=MID-2*ATRN
    return UPPER,MID,LOWER       
  
def TRIX(CLOSE,M1=12, M2=20):                      #Triple exponential smoothing average line
    TR = EMA(EMA(EMA(CLOSE, M1), M1), M1)
    TRIX = (TR - REF(TR, 1)) / REF(TR, 1) * 100
    TRMA = MA(TRIX, M2)
    return TRIX, TRMA

def VR(CLOSE,VOL,M1=26):                            #VRCapacity ratio
    LC = REF(CLOSE, 1)
    return SUM(IF(CLOSE > LC, VOL, 0), M1) / SUM(IF(CLOSE <= LC, VOL, 0), M1) * 100

def EMV(HIGH,LOW,VOL,N=14,M=9):                     #Simple Volatility Indicator 
    VOLUME=MA(VOL,N)/VOL;       MID=100*(HIGH+LOW-REF(HIGH+LOW,1))/(HIGH+LOW)
    EMV=MA(MID*VOLUME*(HIGH-LOW)/MA(HIGH-LOW,N),N);    MAEMV=MA(EMV,M)
    return EMV,MAEMV


def DPO(CLOSE,M1=20, M2=10, M3=6):                  #Range Oscillation Line
    DPO = CLOSE - REF(MA(CLOSE, M1), M2);    MADPO = MA(DPO, M3)
    return DPO, MADPO

def BRAR(OPEN,CLOSE,HIGH,LOW,M1=26):                 #BRAR-ARBR Sentiment Indicator  
    AR = SUM(HIGH - OPEN, M1) / SUM(OPEN - LOW, M1) * 100
    BR = SUM(MAX(0, HIGH - REF(CLOSE, 1)), M1) / SUM(MAX(0, REF(CLOSE, 1) - LOW), M1) * 100
    return AR, BR

def DMA(CLOSE,N1=10,N2=50,M=10):                     #Parallel Line Difference Indicator  
    DIF=MA(CLOSE,N1)-MA(CLOSE,N2);    DIFMA=MA(DIF,M)
    return DIF,DIFMA

def MTM(CLOSE,N=12,M=6):                             #Momentum Indicator
    MTM=CLOSE-REF(CLOSE,N);         MTMMA=MA(MTM,M)
    return MTM,MTMMA

def MASS(HIGH,LOW,N1=9,N2=25,M=6):                   # Mesh line
    MASS=SUM(MA(HIGH-LOW,N1)/MA(MA(HIGH-LOW,N1),N1),N2)
    MA_MASS=MA(MASS,M)
    return MASS,MA_MASS
  
def ROC(CLOSE,N=12,M=6):                             #Rate of Change Indicator
    ROC=100*(CLOSE-REF(CLOSE,N))/REF(CLOSE,N);    MAROC=MA(ROC,M)
    return ROC,MAROC  

def EXPMA(CLOSE,N1=12,N2=50):                        #EMAExponential Moving Average indicator
    return EMA(CLOSE,N1),EMA(CLOSE,N2);

def OBV(CLOSE,VOL):                                  #Chaikin Money Flow Indicator
    return SUM(IF(CLOSE>REF(CLOSE,1),VOL,IF(CLOSE<REF(CLOSE,1),-VOL,0)),0)/10000

def MFI(CLOSE,HIGH,LOW,VOL,N=14):                    #MFIThe indicator is of volumeRSIIndicator
    TYP = (HIGH + LOW + CLOSE)/3
    V1=SUM(IF(TYP>REF(TYP,1),TYP*VOL,0),N)/SUM(IF(TYP<REF(TYP,1),TYP*VOL,0),N)  
    return 100-(100/(1+V1))     
  
def ASI(OPEN,CLOSE,HIGH,LOW,M1=26,M2=10):            #Oscillation Rise and Fall Indicator
    LC=REF(CLOSE,1);      AA=ABS(HIGH-LC);     BB=ABS(LOW-LC);
    CC=ABS(HIGH-REF(LOW,1));   DD=ABS(LC-REF(OPEN,1));
    R=IF( (AA>BB) & (AA>CC),AA+BB/2+DD/4,IF( (BB>CC) & (BB>AA),BB+AA/2+DD/4,CC+DD/4));
    X=(CLOSE-LC+(CLOSE-OPEN)/2+LC-REF(OPEN,1));
    SI=16*X/R*MAX(AA,BB);   ASI=SUM(SI,M1);   ASIT=MA(ASI,M2);
    return ASI,ASIT  

def VWAP(CLOSE,VOL,HIGH,LOW,N=14):                    #Volume weighted average price
    TYP = (HIGH + LOW + CLOSE)/3
    VWAP = SUM(VOL*TYP, N) / SUM(VOL, N)
    return VWAP


ext.MACD = MACD 
ext.KDJ = KDJ
ext.RSI = RSI
ext.WR = WR
ext.BIAS = BIAS
ext.BOLL = BOLL
ext.PSY = PSY
ext.CCI = CCI    
ext.ATR = ATR
ext.BBI = BBI
ext.DMI = DMI
ext.TAQ = TAQ
ext.KTN = KTN
ext.TRIX = TRIX
ext.VR = VR
ext.EMV = EMV
ext.DPO = DPO
ext.BRAR = BRAR
ext.DMA = DMA
ext.MTM = MTM
ext.MASS = MASS
ext.ROC = ROC
ext.EXPMA = EXPMA
ext.OBV = OBV
ext.MFI = MFI
ext.ASI = ASI
ext.VWAP = VWAP
```

> Detail

https://www.fmz.com/strategy/381042

> Last Modified

2024-04-09 19:55:31
