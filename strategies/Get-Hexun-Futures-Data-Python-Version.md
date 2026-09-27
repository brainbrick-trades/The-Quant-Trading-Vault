
> Name

Get-Hexun-Futures-Data-Python-Version

> Author

edwardgyw

> Strategy Description

Shukuang wrote a js version of third-party data acquisition a long time ago. I followed his example and rewrote a python version. You can download it and introduce your own package on the cloud server, so that it can also be used during research.
update 12.01 The Hexun interface has changed to include 60-minute and weekly line information. In the original version, selecting 1440 will get the 60-minute candlestick. This is fixed.



> Source (python)

``` python
#coding: utf-8
import urllib2 as url
import json
import time

def hxRecords(instrument,timeFrame=1,size=1,includeLastBar=True,to_df=True):
    ##Get real-time futures data from Hexun
    pInst=instrument.lower()
    if pInst[-4]!='1':
        pInst=pInst[:-3]+'1'+pInst[-3:]
    xchg=None
    for i in instList:
        if pInst[:-4] in i['inst']:
            xchg=i['xchg']
    if xchg is None:
        print ("Error occurred when fetching candlestick: contract not found")
        return None
    tfs=[1,5,15,30,60,'D','W']
    tf=None
    for i in range(len(tfs)):
        if timeFrame==tfs[i]:
            tf=i
    if tf is None:
        print("An error occurred when obtaining the candlestick: The candlestick period is incorrect")
        return None
    now=time.localtime()
    timestr=str(now.tm_year+1)+str(12)+str(31)+'000000'
    resp='http://webftcn.hermes.hexun.com/shf/kline?code=' + xchg + pInst + '&start=' + timestr + '&number=-' + str(size) + '&type=' + str(tf)
    try:
        resp=url.urlopen(resp)
        resp=resp.read()[1:-2]
        resp=json.loads(resp)['Data']
    except:
        print 'Error occurred when fetching candlestick: incomplete JSON data'
        return None
    re=[]
    pw=float(resp[4])
    for i in resp[0]:
        res=dict(Time=time.mktime(time.strptime(str(i[0]),'%Y%m%d%H%M%S'))*1000,Open=i[2]/pw,High=i[4]/pw
                ,Low=i[5]/pw,Close=i[3]/pw,Volume=i[6])
        re.append(res)
    if to_df:
        re=pd.DataFrame(re)
        col=[]
        for i in re.columns:
            if i is 'Time':
                i='Date'
            col.append(i.lower())
        re.columns=col
        re['date']=re['date'].map(ts_dt64)
    return re
        

instList = [{
    "xchg": "SHFE",
    "inst": ["fu", "ru", "wr"]
}, {
    "xchg": "SHFE2",
    "inst": ["ag", "au"]
}, {
    "xchg": "SHFE3",
    "inst": ["al", "bu", "cu", "hc", "ni", "pb", "rb", "sn", "zn"]
}, {
    "xchg": "CZCE",
    "inst": ["cf", "fg", "lr", "ma", "oi", "pm", "ri", "rm", "rs", "sf", "sm", "sr", "ta", "wh", "zc"]
}, {
    "xchg": "DCE",
    "inst": ["a", "b", "bb", "c", "cs", "fb", "i", "j", "jd", "jm", "l", "m", "p", "pp", "v", "y"]
}]

def main():
    Log(exchange.GetAccount())

```

> Detail

https://www.fmz.com/strategy/26017

> Last Modified

2016-12-01 00:28:00
