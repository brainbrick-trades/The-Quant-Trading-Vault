
> Name

Backtesting-Saves-Candlestick-to-Local-CSV

> Author

小草





> Source (python)

``` python
'''
/*backtest
start: 2017-10-01        
end: 2017-11-16          
period: 1440
periodBase: 15
mode: 0                 
*/
'''

#Requiredpandasof the library, and only with my own hosted backtesting can it be saved locally
#import numpy as np
import pandas as pd

#Save path
path = 'C:\\Users\\Public\\Documents\\'

def main():
    df=pd.DataFrame()
    while True:
        records = _C(exchange.GetRecords)
        df_new = pd.DataFrame(records)  #holdrecordsConvert todataframe
        df_new['Time'] = pd.to_datetime(df_new['Time'],unit='ms')+pd.Timedelta('8 h')
        df_new.index = df_new['Time']
        if df.empty or df_new['Time'].min() >= df['Time'].max():
            df=df.combine_first(df_new)
            Log(df['Time'].max())
        #Confirm the last time for saving data
        if df_new['Time'].max() == pd.Timestamp('2017-11-15 23:45:00'):
            Log('Save data')
            df=df.combine_first(df_new)
            df.to_csv(path+'records15.csv',index=False)
            break
        #Sleep time is the selected period
        Sleep(15*60*1000)

```

> Detail

https://www.fmz.com/strategy/61867

> Last Modified

2017-12-15 13:31:31
