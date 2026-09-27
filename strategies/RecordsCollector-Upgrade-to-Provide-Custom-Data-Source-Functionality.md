
> Name

RecordsCollector-Upgrade-to-Provide-Custom-Data-Source-Functionality

> Author

发明者量化-小小梦

> Strategy Description

Related articles:https://www.fmz.com/bbs-topic/5569

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|dropNames|[]|Delete table name|


> Source (python)

``` python
import _thread
import pymongo
import json
import math
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

def url2Dict(url):
    query = urlparse(url).query  
    params = parse_qs(query)  
    result = {key: params[key][0] for key in params}  
    return result

class Provider(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            dictParam = url2Dict(self.path)
            Log("Custom data source service receives request,self.path:", self.path, "query Parameters:", dictParam)
            
            # Currently, the backtesting system can only select the exchange name from a list. When adding a custom data source, set it to Binance, i.e.:Binance
            exName = exchange.GetName()                                     
            # Note: period refers to the underlying candlestick timeframe
            tabName = "%s_%s" % ("records", int(int(dictParam["period"]) / 1000))  
            priceRatio = math.pow(10, int(dictParam["round"]))
            amountRatio = math.pow(10, int(dictParam["vround"]))
            fromTS = int(dictParam["from"]) * int(1000)
            toTS = int(dictParam["to"]) * int(1000)
            
            
            # Connect to database
            Log("Connect to the database service to fetch data, database:", exName, "table:", tabName)
            myDBClient = pymongo.MongoClient("mongodb://localhost:27017")
            ex_DB = myDBClient[exName]
            exRecords = ex_DB[tabName]
            
            
            # Required Response Data
            data = {
                "schema" : ["time", "open", "high", "low", "close", "vol"],
                "data" : []
            }
            
            # Construct query conditions: greater than a certain value {'age': {'$gt': 20}} less than a certain value{'age': {'$lt': 20}}
            dbQuery = {"$and":[{'Time': {'$gt': fromTS}}, {'Time': {'$lt': toTS}}]}
            Log("Query conditions:", dbQuery, "Query the number of items:", exRecords.find(dbQuery).count(), "Total number of database entries:", exRecords.find().count())
            
            for x in exRecords.find(dbQuery).sort("Time"):
                # Data Precision Needs to Be Processed According to Request Parameters round and vround
                bar = [x["Time"], int(x["Open"] * priceRatio), int(x["High"] * priceRatio), int(x["Low"] * priceRatio), int(x["Close"] * priceRatio), int(x["Volume"] * amountRatio)]
                data["data"].append(bar)
            
            Log("Data:", data, "Respond to Backtesting System Requests.")
            # Data write response
            self.wfile.write(json.dumps(data).encode())
        except BaseException as e:
            Log("Provider do_GET error, e:", e)


def createServer(host):
    try:
        server = HTTPServer(host, Provider)
        Log("Starting server, listen at: %s:%s" % host)
        server.serve_forever()
    except BaseException as e:
        Log("createServer error, e:", e)
        raise Exception("stop")

def main():
    LogReset(1)
    exName = exchange.GetName()
    period = exchange.GetPeriod()
    Log("Collect", exName, "ExchangeKLine Data,", "KLine period:", period, "second")
    
    # Connect to the database service, service address mongodb://127.0.0.1:27017. Please refer to the mongodb settings installed on the server for details.
    Log("Connect to the Device of the CustodianmongodbService,mongodb://localhost:27017")
    myDBClient = pymongo.MongoClient("mongodb://localhost:27017")   
    # Create database
    ex_DB = myDBClient[exName]
    
    # Print Current Database Tables
    collist = ex_DB.list_collection_names()
    Log("mongodb ", exName, " collist:", collist)
    
    # Check Whether to Delete Table
    arrDropNames = json.loads(dropNames)
    if isinstance(arrDropNames, list):
        for i in range(len(arrDropNames)):
            dropName = arrDropNames[i]
            if isinstance(dropName, str):
                if not dropName in collist:
                    continue
                tab = ex_DB[dropName]
                Log("dropName:", dropName, "Delete:", dropName)
                ret = tab.drop()
                collist = ex_DB.list_collection_names()
                if dropName in collist:
                    Log(dropName, "Delete failed")
                else :
                    Log(dropName, "Deletion successful")
    
    # Start a thread to provide a custom data source service
    try:
        # _thread.start_new_thread(createServer, (("localhost", 9090), ))     # Local testing
        _thread.start_new_thread(createServer, (("0.0.0.0", 9090), ))         # VPSTest on server
        Log("Start the custom data source service thread", "#FF0000")
    except BaseException as e:
        Log("Failed to start custom data source service!")
        Log("Error message:", e)
        raise Exception("stop")
    
    # Create records Table
    ex_DB_Records = ex_DB["%s_%d" % ("records", period)]
    Log("Start collecting", exName, "KLine Data", "timeframe:", period, "Open (Create) Database Table:", "%s_%d" % ("records", period), "#FF0000")
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
                bar = r[i]
                # To write root by root, you need to determine whether the data already exists in the current database table. Based on the timestamp detection, if the data exists, skip it. If not, write it.
                retQuery = ex_DB_Records.find({"Time": bar["Time"]})
                if retQuery.count() > 0:
                    continue
                
                # Write Bar to Database Table
                ex_DB_Records.insert_one({"High": bar["High"], "Low": bar["Low"], "Open": bar["Open"], "Close": bar["Close"], "Time": bar["Time"], "Volume": bar["Volume"]})                
                index += 1
            preBarTime = r[-1]["Time"]
        elif preBarTime != r[-1]["Time"]:
            bar = r[-2]
            # Detect before writing data whether it already exists, based on timestamp checking
            retQuery = ex_DB_Records.find({"Time": bar["Time"]})
            if retQuery.count() > 0:
                continue
            
            ex_DB_Records.insert_one({"High": bar["High"], "Low": bar["Low"], "Open": bar["Open"], "Close": bar["Close"], "Time": bar["Time"], "Volume": bar["Volume"]})
            index += 1
            preBarTime = r[-1]["Time"]
        LogStatus(_D(), "preBarTime:", preBarTime, "_D(preBarTime):", _D(preBarTime/1000), "index:", index)
        # Add chart display
        ext.PlotRecords(r, "%s_%d" % ("records", period))
        Sleep(10000)
        

```

> Detail

https://www.fmz.com/strategy/205143

> Last Modified

2020-05-09 15:58:04
