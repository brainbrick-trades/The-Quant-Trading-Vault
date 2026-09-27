
> Name

RecordsCollector-Teaching

> Author

发明者量化-小小梦

> Strategy Description

Related articles:https://www.fmz.com/bbs-topic/5425

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|dropNames|[]|Delete table name|


> Source (python)

``` python
import pymongo
import json

def main():
    Log("Test data collection")
    
    # Connect to Database Service
    myDBClient = pymongo.MongoClient("mongodb://localhost:27017")   # mongodb://127.0.0.1:27017
    # Create database
    huobi_DB = myDBClient["huobi"]
    
    # Print Current Database Tables
    collist = huobi_DB.list_collection_names()
    Log("collist:", collist)
    
    # Check Whether to Delete Table
    arrDropNames = json.loads(dropNames)
    if isinstance(arrDropNames, list):
        for i in range(len(arrDropNames)):
            dropName = arrDropNames[i]
            if isinstance(dropName, str):
                if not dropName in collist:
                    continue
                tab = huobi_DB[dropName]
                Log("dropName:", dropName, "Delete:", dropName)
                ret = tab.drop()
                collist = huobi_DB.list_collection_names()
                if dropName in collist:
                    Log(dropName, "Delete failed")
                else :
                    Log(dropName, "Deletion successful")
    
    # Create records Table
    huobi_DB_Records = huobi_DB["records"]
    
    # Request data
    preBarTime = 0
    index = 1
    while True:
        r = _C(exchange.GetRecords)
        if len(r) < 2:
            Sleep(1000)
            continue
        if preBarTime == 0:
            # Write all BAR data for the first time
            for i in range(len(r) - 1):
                # Write root by root
                bar = r[i]
                huobi_DB_Records.insert_one({"index": index, "High": bar["High"], "Low": bar["Low"], "Open": bar["Open"], "Close": bar["Close"], "Time": bar["Time"], "Volume": bar["Volume"]})                
                index += 1
            preBarTime = r[-1]["Time"]
        elif preBarTime != r[-1]["Time"]:
            bar = r[-2]
            huobi_DB_Records.insert_one({"index": index, "High": bar["High"], "Low": bar["Low"], "Open": bar["Open"], "Close": bar["Close"], "Time": bar["Time"], "Volume": bar["Volume"]})
            index += 1
            preBarTime = r[-1]["Time"]
        LogStatus(_D(), "preBarTime:", preBarTime, "_D(preBarTime):", _D(preBarTime/1000), "index:", index)
        Sleep(10000)
        

```

> Detail

https://www.fmz.com/strategy/199120

> Last Modified

2020-04-16 15:18:28
