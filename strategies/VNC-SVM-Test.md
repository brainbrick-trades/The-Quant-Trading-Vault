
> Name

VNC-SVM-Test

> Author

virtualpeer





> Source (python)

``` python
import numpy as np
import pandas as pd

data = DataAPI.MktIdxdGet(indexID=u"",ticker=u"000300",tradeDate=u"",beginDate=u"20100101",endDate=u"20180501",exchangeCD=u"XSHE,XSHG",field=u"",pandas="1")
data.set_index('tradeDate', inplace = True)
# Obtain daily price data of HS300

for i in range(1, 21, 1):
    data['close-' + str(i) + 'd'] = data['closeIndex'].shift(i)
# For the closing price, 20 columns of data were added to the data, ranging from the closing price 1 day ago to the closing price 20 days ago.
    
hs_close = data[[x for x in data.columns if 'close' in x]].iloc[20:]
# Select the closing price of today and 1-20 days ago, iloc[20:] eliminates invalid data

hs_close = hs_close.iloc[:, ::-1]
# Arrange the columns of the new DataFrame in reverse order
################################################################################################
from sklearn import svm
# Import the svm algorithm from the sklearn library

days = 1500
# Set global variables and split the data of the training set and the test set. 1500 accounts for approximately 1500 in the above data.75%

clf_close = svm.SVR(kernel='linear')
# Use the SVR algorithm under SVM, where 'linear' represents the linear kernel
f_close_train = hs_close[:days]
# Training setfeatures
l_close_train = hs_close['closeIndex'].shift(-1)[:days]
# Training set labels: shift the closing price by (-1) to represent predicting the next day's closing price.
f_close_test = hs_close[days:]
# Test setfeatures
l_close_test = hs_close['closeIndex'].shift(-1)[days:]
# Training set labels: shift the closing price by (-1) to represent predicting the next day's closing price.
clf_close.fit(f_close_train, l_close_train)
# Training Model

######################################################################################

p_close_train = clf_close.predict(f_close_train)
# Import the training set features into the model for prediction and generate the predicted closing price
df_close_train = pd.DataFrame(l_close_train)
# Create a new DataFrame with content as training set labels, i.e., the next day's closing price
df_close_train.columns = ['next close']
# Column renamed to'next close'
df_close_train['predicted next close'] = p_close_train
# Add a column of predicted closing price data
df_close_train['next open'] = data['openIndex'][20:20 + days].shift(-1)
# Add a column of data on the opening price of the next day, obtain it from data instead of hs_close, and need to be sliced

trigger = 1.0
df_close_train['position'] = np.where(df_close_train['predicted next close'] > df_close_train['next open'] * trigger, 1, 0)
# Judging by the np.where function, when the predicted closing price of the next day > the opening price of the next day is multiplied or added by a trigger, the position is set to 1, otherwise it is0
df_close_train['PL'] = np.where(df_close_train['position'] == 1, (df_close_train['next close'] - df_close_train['next open']) / df_close_train['next open'], 0)
# When the position is 1, buy when the market opens on the next day and sell when the market closes. Record the return rate that should be obtained on the next day. Otherwise, the return rate is0

df_close_train['strategy'] = (df_close_train['PL'].shift(1) + 1).cumprod()
# The cumulative rate of return of the strategy's daily income, where shift(1) means that the rate of return recorded on that day is the rate of return that can only be obtained on the next day and cannot be obtained on that day.
df_close_train['return'] = (df_close_train['next close'].pct_change() + 1).cumprod()
# benchmarkCumulative return

df_close_train[['strategy', 'return']].dropna().plot()
# Draw the cumulative return chart of strategy and benchmark

##########################################################################
def main():
    Log(exchange.GetAccount())

```

> Detail

https://www.fmz.com/strategy/112188

> Last Modified

2018-08-18 20:34:19
