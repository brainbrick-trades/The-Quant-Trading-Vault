
> Name

Backtesting-System-Random-Market-Generator

> Author

发明者量化-小小梦

> Strategy Description

Related articles: https://www.fmz.com/bbs-topic/10545

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|filePathForCSV|CSVFile path | CSV file path|
|startTime|The starting time for generating candlestick data, format: 2023-11-01 00:00:00|Starting time (UTC time)|
|endTime|The end time of the generated candlestick data, format: 2023-11-02 00:00:00|End time (UTC time)|
|KLinePeriod|The candlestick period of the candlestick data to be generated, 1h, 1d, 1m, etc. |candlestick cycle|
|firstPrice|KStarting price of the candlestick data | Starting price of the candlestick data|
|ratio|Volatility coefficient | Volatility coefficient|
|trendType|Volatility type | Volatility type|
|pround|Price precision, the price precision of candlestick data | price precision|
|vround|Order quantity accuracy|Order quantity accuracy|
|ct|Contract code, swap is a perpetual contract. |Contract code|




|Button|Default|Description|
|----|----|----|
|createRecords|Generate random candlestick data | Generate random candlestick data|


> Source (python)

``` python
import _thread
import json
import math
import csv
import random
import os
import datetime as dt
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

arrTrendType = ["down", "slow_up", "sharp_down", "sharp_up", "narrow_range", "wide_range", "neutral_random"]

def url2Dict(url):
    query = urlparse(url).query  
    params = parse_qs(query)  
    result = {key: params[key][0] for key in params}  
    return result

class Provider(BaseHTTPRequestHandler):
    def do_GET(self):
        global filePathForCSV, pround, vround, ct
        try:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            dictParam = url2Dict(self.path)
            Log("Custom data source service receives request,self.path:", self.path, "query Parameters:", dictParam)            
            
            eid = dictParam["eid"]
            symbol = dictParam["symbol"]
            arrCurrency = symbol.split(".")[0].split("_")
            baseCurrency = arrCurrency[0]
            quoteCurrency = arrCurrency[1]
            fromTS = int(dictParam["from"]) * int(1000)
            toTS = int(dictParam["to"]) * int(1000)
            priceRatio = math.pow(10, int(pround))
            amountRatio = math.pow(10, int(vround))

            data = {
                "detail": {
                    "eid": eid,
                    "symbol": symbol,
                    "alias": symbol,
                    "baseCurrency": baseCurrency,
                    "quoteCurrency": quoteCurrency,
                    "marginCurrency": quoteCurrency,
                    "basePrecision": vround,
                    "quotePrecision": pround,
                    "minQty": 0.00001,
                    "maxQty": 9000,
                    "minNotional": 5,
                    "maxNotional": 9000000,
                    "priceTick": 10 ** -pround,
                    "volumeTick": 10 ** -vround,
                    "marginLevel": 10,
                    "contractType": ct
                },
                "schema" : ["time", "open", "high", "low", "close", "vol"],
                "data" : []
            }
            
            listDataSequence = []
            with open(filePathForCSV, "r") as f:
                reader = csv.reader(f)
                header = next(reader)
                headerIsNoneCount = 0
                if len(header) != len(data["schema"]):
                    Log("CSVThe file format is wrong and the number of columns is different, please check!", "#FF0000")
                    return 
                for ele in header:
                    for i in range(len(data["schema"])):
                        if data["schema"][i] == ele or ele == "":
                            if ele == "":
                                headerIsNoneCount += 1
                            if headerIsNoneCount > 1:
                                Log("CSVFile format error, please check!", "#FF0000")
                                return 
                            listDataSequence.append(i)
                            break
                
                while True:
                    record = next(reader, -1)
                    if record == -1:
                        break
                    index = 0
                    arr = [0, 0, 0, 0, 0, 0]
                    for ele in record:
                        arr[listDataSequence[index]] = int(ele) if listDataSequence[index] == 0 else (int(float(ele) * amountRatio) if listDataSequence[index] == 5 else int(float(ele) * priceRatio))
                        index += 1
                    data["data"].append(arr)            
            Log("Datadata.detail:", data["detail"], "Respond to Backtesting System Requests.")
            self.wfile.write(json.dumps(data).encode())
        except BaseException as e:
            Log("Provider do_GET error, e:", e)
        return 

def createServer(host):
    try:
        server = HTTPServer(host, Provider)
        Log("Starting server, listen at: %s:%s" % host)
        server.serve_forever()
    except BaseException as e:
        Log("createServer error, e:", e)
        raise Exception("stop")

class KlineGenerator:
    def __init__(self, start_time, end_time, interval):
        self.start_time = dt.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        self.end_time = dt.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        self.interval = self._parse_interval(interval)
        self.timestamps = self._generate_time_series()

    def _parse_interval(self, interval):
        unit = interval[-1]
        value = int(interval[:-1])

        if unit == "m":
            return value * 60
        elif unit == "h":
            return value * 3600
        elif unit == "d":
            return value * 86400
        else:
            raise ValueError("Unsupported candlestick period, please use 'm', 'h', or 'd'.")

    def _generate_time_series(self):
        timestamps = []
        current_time = self.start_time
        while current_time <= self.end_time:
            timestamps.append(int(current_time.timestamp() * 1000))
            current_time += dt.timedelta(seconds=self.interval)
        return timestamps

    def generate(self, initPrice, trend_type="neutral", volatility=1):
        data = []
        current_price = initPrice
        angle = 0
        for timestamp in self.timestamps:
            angle_radians = math.radians((angle + random.uniform(0, 360)) % 360)
            cos_value = math.cos(angle_radians)   #  -1 ~ 1

            if trend_type == "down":
                change = random.uniform(-0.5, 0.4) * volatility * abs(cos_value) 
            elif trend_type == "slow_up":
                change = random.uniform(-0.4, 0.5) * volatility * abs(cos_value) 
            elif trend_type == "sharp_down":
                change = random.uniform(-10, 7) * volatility * abs(cos_value) 
            elif trend_type == "sharp_up":
                change = random.uniform(-7, 10) * volatility * abs(cos_value) 
            elif trend_type == "narrow_range":
                change = random.uniform(-0.2, 0.2) * volatility * abs(cos_value) 
            elif trend_type == "wide_range":
                change = random.uniform(-20, 20) * volatility * abs(cos_value) 
            else:
                change = random.uniform(-1, 1) * volatility * abs(cos_value) 
            
            open_price = current_price
            close_price = open_price + change
            high_price = open_price + random.uniform(0, abs(change)) if open_price > close_price else close_price + random.uniform(0, abs(change))
            low_price = close_price - random.uniform(0, abs(change)) if open_price > close_price else open_price - random.uniform(0, abs(change))

            if low_price <= 0:
                change = random.uniform(1, 5) * volatility * abs(cos_value) 
                close_price = open_price + change
                high_price = open_price + random.uniform(0, abs(change)) if open_price > close_price else close_price + random.uniform(0, abs(change))
                low_price = open_price * random.uniform(0.8, 1)


            if (high_price >= open_price and open_price >= close_price and close_price >= low_price) or (high_price >= close_price and close_price >= open_price and open_price >= low_price):
                pass
            else:
                Log("Abnormal data:", high_price, open_price, low_price, close_price, "#FF0000")

            base_volume = random.uniform(1000, 5000)
            volume = base_volume * (1 + abs(change) * 0.2)

            kline = {
                "Time": timestamp,
                "Open": round(open_price, 2),
                "High": round(high_price, 2),
                "Low": round(low_price, 2),
                "Close": round(close_price, 2),
                "Volume": round(volume, 2),
            }
            data.append(kline)
            current_price = close_price
            angle += 1
        return data

    def save_to_csv(self, filename, data):
        with open(filename, mode="w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["", "open", "high", "low", "close", "vol"])
            for idx, kline in enumerate(data):
                writer.writerow(
                    [kline["Time"], kline["Open"], kline["High"], kline["Low"], kline["Close"], kline["Volume"]]
                )
        
        Log("Current path:", os.getcwd())
        with open("data.csv", "r") as file:
            lines = file.readlines()
            if len(lines) > 1:
                Log("File successfully written, here is a part of the file content:")
                Log("".join(lines[:5]))
            else:
                Log("File writing failed and the file is empty!")

def main():
    Chart({})
    LogReset(1)
    
    try:
        # _thread.start_new_thread(createServer, (("localhost", 9090), ))
        _thread.start_new_thread(createServer, (("0.0.0.0", 9090), ))
        Log("Start a custom data source service thread, data provided byCSVDocument provided.", ", Address/Port:0.0.0.0:9090", "#FF0000")
    except BaseException as e:
        Log("Failed to start custom data source service!")
        Log("Error message:", e)
        raise Exception("stop")
    
    while True:
        cmd = GetCommand()
        if cmd:
            if cmd == "createRecords":
                Log("Generator parameters:", "Start time:", startTime, "End time:", endTime, "KLine period:", KLinePeriod, "Initial price:", firstPrice, "Volatility type:", arrTrendType[trendType], "Volatility coefficient:", ratio)
                generator = KlineGenerator(
                    start_time=startTime,
                    end_time=endTime,
                    interval=KLinePeriod,
                )
                kline_data = generator.generate(firstPrice, trend_type=arrTrendType[trendType], volatility=ratio)
                generator.save_to_csv("data.csv", kline_data)
                ext.PlotRecords(kline_data, "%s_%s" % ("records", KLinePeriod))
        LogStatus(_D())
        Sleep(2000)
```

> Detail

https://www.fmz.com/strategy/473286

> Last Modified

2024-12-07 18:32:50
