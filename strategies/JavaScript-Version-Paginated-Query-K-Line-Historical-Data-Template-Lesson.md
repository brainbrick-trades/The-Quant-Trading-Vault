
> Name

JavaScript-Version-Paginated-Query-K-Line-Historical-Data-Template-Lesson

> Author

发明者量化-小小梦

> Strategy Description

Related article reference:https://www.fmz.com/bbs-topic/10105



> Source (javascript)

``` javascript
/**
 * desc: $.GetRecordsByLength This is the interface function of the template library, used to obtain candlestick data of a specified candlestick length
 * @param {Object} e - Exchange object
 * @param {Int} period - KLine period, in seconds
 * @param {Int} length - Specify the length of candlestick data to fetch, depending on the exchange interface limitations
 * @returns {Array<Object>} - KLine Data
 */
$.GetRecordsByLength = function(e, period, length) {
    if (!Number.isInteger(period) || !Number.isInteger(length)) {
        throw "params error!"
    }

    var exchangeName = e.GetName()
    if (exchangeName == "Futures_Binance") {
        return getRecordsForFuturesBinance(e, period, length)
    } else {
        throw "not support!"
    }
}

/**
 * desc: getRecordsForFuturesBinance Specific implementation of the function to obtain candlestick data from Binance Futures
 * @param {Object} e - Exchange object
 * @param {Int} period - KLine period, in seconds
 * @param {Int} length - Specify the length of candlestick data to fetch, depending on the exchange interface limitations
 * @returns {Array<Object>} - KLine Data
 */
function getRecordsForFuturesBinance(e, period, length) {
    var contractType = e.GetContractType()
    var currency = e.GetCurrency()
    var strPeriod = String(period)

    var symbols = currency.split("_")
    var baseCurrency = ""
    var quoteCurrency = ""
    if (symbols.length == 2) {
        baseCurrency = symbols[0]
        quoteCurrency = symbols[1]
    } else {
        throw "currency error!"
    }

    var realCt = e.SetContractType(contractType)["instrument"]
    if (!realCt) {
        throw "realCt error"
    }
    
    // m -> Minute; h -> Hour; d -> Sky/Heaven; w -> week; M -> Moon
    var periodMap = {}
    periodMap[(60).toString()] = "1m"
    periodMap[(60 * 3).toString()] = "3m"
    periodMap[(60 * 5).toString()] = "5m"
    periodMap[(60 * 15).toString()] = "15m"
    periodMap[(60 * 30).toString()] = "30m"
    periodMap[(60 * 60).toString()] = "1h"
    periodMap[(60 * 60 * 2).toString()] = "2h"
    periodMap[(60 * 60 * 4).toString()] = "4h"
    periodMap[(60 * 60 * 6).toString()] = "6h"
    periodMap[(60 * 60 * 8).toString()] = "8h"
    periodMap[(60 * 60 * 12).toString()] = "12h"
    periodMap[(60 * 60 * 24).toString()] = "1d"
    periodMap[(60 * 60 * 24 * 3).toString()] = "3d"
    periodMap[(60 * 60 * 24 * 7).toString()] = "1w"
    periodMap[(60 * 60 * 24 * 30).toString()] = "1M"
    
    var records = []
    var url = ""
    if (quoteCurrency == "USDT") {
        // GET https://fapi.binance.com  /fapi/v1/klines  symbol , interval , startTime , endTime , limit 
        // limit maximum value:1500

        url = "https://fapi.binance.com/fapi/v1/klines"
    } else if (quoteCurrency == "USD") {
        // GET https://dapi.binance.com  /dapi/v1/klines  symbol , interval , startTime , endTime , limit
        // startTime and endTime Can differ by at most200Sky/Heaven
        // limit maximum value:1500

        url = "https://dapi.binance.com/dapi/v1/klines"
    } else {
        throw "not support!"
    }

    var maxLimit = 1500
    var interval = periodMap[strPeriod]
    if (typeof(interval) !== "string") {
        throw "period error!"
    }

    var symbol = realCt
    var currentTS = new Date().getTime()

    while (true) {
        // Calculationlimit
        var limit = Math.min(maxLimit, length - records.length)
        var barPeriodMillis = period * 1000
        var rangeMillis = barPeriodMillis * limit
        var twoHundredDaysMillis = 200 * 60 * 60 * 24 * 1000
        
        if (rangeMillis > twoHundredDaysMillis) {
            limit = Math.floor(twoHundredDaysMillis / barPeriodMillis)
            rangeMillis = barPeriodMillis * limit
        }

        var query = `symbol=${symbol}&interval=${interval}&endTime=${currentTS}&limit=${limit}`
        var retHttpQuery = HttpQuery(url + "?" + query)
        
        var ret = null 
        try {
            ret = JSON.parse(retHttpQuery)
        } catch(e) {
            Log(e)
        }
        
        if (!ret || !Array.isArray(ret)) {
            return null
        }
        
        // Exceeds the exchange's queryable range, when data cannot be retrieved
        if (ret.length == 0 || currentTS <= 0) {
            break
        }

        for (var i = ret.length - 1; i >= 0; i--) {
            var ele = ret[i]
            var bar = {
                Time : parseInt(ele[0]),
                Open : parseFloat(ele[1]),
                High : parseFloat(ele[2]),
                Low : parseFloat(ele[3]), 
                Close : parseFloat(ele[4]),
                Volume : parseFloat(ele[5])
            }

            records.unshift(bar)
        }

        if (records.length >= length) {
            break
        }

        currentTS -= rangeMillis
        Sleep(1000)
    }

    return records
}

/**
 * desc: $.UpdataRecords This is the interface function of the template library, which is used to update candlestick data
 * @param {Object} e - Exchange object
 * @param {Array<Object>} records - candlestick data source that needs to be updated
 * @param {Int} period - Kperiod must match the candlestick data period passed in by the рекордs parameter
 * @returns {Bool}  - Is the update successful?
 */
$.UpdataRecords = function(e, records, period) {
    var r = e.GetRecords(period)
    if (!r) {
        return false 
    }

    for (var i = 0; i < r.length; i++) {
        if (r[i].Time > records[records.length - 1].Time) {
            // add newBar
            records.push(r[i])
            // Update the previous oneBar
            if (records.length - 2 >= 0 && i - 1 >= 0 && records[records.length - 2].Time == r[i - 1].Time) {
                records[records.length - 2] = r[i - 1]
            }            
        } else if (r[i].Time == records[records.length - 1].Time) {
            // UpdateBar
            records[records.length - 1] = r[i]
        }
    }
    return true
}

// Template test function
function main() {
    Log("Currently testing exchanges:", exchange.GetName())

    // If it is futures, a contract needs to be set
    exchange.SetContractType("swap")

    // Use$.GetRecordsByLengthGet the specified lengthKLine data, specified period is60seconds, that is, one minuteKLine, specified length is8000Root
    var r = $.GetRecordsByLength(exchange, 60, 8000)
    Log(r)

    // Detection data
    var diffTime = r[1].Time - r[0].Time 
    Log("diffTime:", diffTime, " ms")
    for (var i = 0; i < r.length; i++) {
        for (var j = 0; j < r.length; j++) {
            // Check for duplicatesBar
            if (i != j && r[i].Time == r[j].Time) {
                Log(r[i].Time, i, r[j].Time, j)
                throw "DuplicateBar"
            }
        }
        
        // CheckBarContinuity
        if (i < r.length - 1) {            
            if (r[i + 1].Time - r[i].Time != diffTime) {
                Log("i:", i, ", diff:", r[i + 1].Time - r[i].Time, ", r[i].Time:", r[i].Time, ", r[i + 1].Time:", r[i + 1].Time)
                throw "BarDiscontinuity"
            }            
        }
    }
    Log("Test passed")
    Log("$.GetRecordsByLengthData length returned by the function:", r.length)

    // UseGetRecordsData update obtained by the functionr
    while (true) {
        $.UpdataRecords(exchange, r, 60)
        LogStatus(_D(), ", r.length:", r.length)
        Log(_D(r[r.length - 1].Time), r[r.length - 1])
        Sleep(5000)
    }
}
```

> Detail

https://www.fmz.com/strategy/418803

> Last Modified

2023-06-27 15:24:55
