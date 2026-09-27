
> Name

JavaScript-Version-K-Line-Data-Market-Collector

> Author

发明者量化-小小梦

> Strategy Description

## JavaScriptVersion candlestick data collector

Related articles:https://www.fmz.com/bbs-topic/6744

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|tableName|testRecords_min1|The name of the table that stores candlestick data|




|Button|Default|Description|
|----|----|----|
|refreshRecords|__button__|Refresh candlestick chart|
|deleteBDTable|__button__|Delete database table|
|initCollecter|__button__|Initialize the collector|


> Source (javascript)

``` javascript
var collecter = {}
collecter.init = function(tableName) {
	this.preBarTS = 0
	this.tableName = tableName
    this.tableAvaliable = false 
    // DetecttableNametable
    if (typeof(tableName) == "undefined" || typeof(tableName) != "string") {
    	Log(tableName)
        throw "tableName error!"
    }

    // SELECT * FROM RECORDS_MIN1 LIMIT 1
    var strSql = "SELECT * FROM " + tableName + " LIMIT 1"
    var ret = DBExec(strSql)    
    if (!ret) {
    	// The table does not exist, create the table
        Log("Try to read the table", this.tableName, "The data failed to read, starting to create the table", this.tableName)
    	var strSql = [
            "CREATE TABLE " + tableName + "(", 
            "TS INT PRIMARY KEY NOT NULL,",
            "HIGH REAL NOT NULL,", 
            "OPEN REAL NOT NULL,", 
            "LOW REAL NOT NULL,", 
            "CLOSE REAL NOT NULL,", 
            "VOLUME REAL NOT NULL)"
        ].join("")
        ret = DBExec(strSql)
        if (!ret) {
        	throw "create" + tableName + "table failed!"
        }
        Log("create", tableName, "table", ret)
    }
    Log(this.tableName, ret)
    this.tableAvaliable = true 
}

collecter.run = function(records) {
    if (!this.tableAvaliable) {
        return 
    }
	var len = records.length
	var lastBar = records[len - 1]
	var beginBar = records[0]
	var ret = null 
    if (this.preBarTS == 0) {
        // initial
        /*
		DELETE FROM table_name WHERE [condition];
        */
        var strSql = "DELETE FROM " + this.tableName + " WHERE TS >= " + beginBar.Time + ";"
        ret = DBExec(strSql)
        Log("Delete the duplicate parts of the current record", ret)

        // write
        ret = DBExec("BEGIN")
        Log("BEGIN:", ret)
        for (var i = 0 ; i < len - 1 ; i++) {
        	var strSql = [
                "INSERT INTO " + this.tableName + " (TS, HIGH, OPEN, LOW, CLOSE, VOLUME) ", 
                `VALUES (${records[i].Time}, ${records[i].High}, ${records[i].Open}, ${records[i].Low}, ${records[i].Close}, ${records[i].Volume});`
            ].join("")
            DBExec(strSql)
        }
        ret = DBExec("COMMIT")
        Log("COMMIT:", ret)
        this.preBarTS = lastBar.Time
    } else if(this.preBarTS != lastBar.Time) {
        // Update
        var strSql = [
            "INSERT INTO " + this.tableName + " (TS, HIGH, OPEN, LOW, CLOSE, VOLUME) ", 
            `VALUES (${records[len-2].Time}, ${records[len-2].High}, ${records[len-2].Open}, ${records[len-2].Low}, ${records[len-2].Close}, ${records[len-2].Volume});`
        ].join("")
        ret = DBExec(strSql)
        Log("INSERT:", ret)
        this.preBarTS = lastBar.Time
    }
}

collecter.getRecords = function() {
	// Read database
    var strSql = "SELECT * FROM " + this.tableName + ";"
    var ret = DBExec(strSql)
    // Log("SELECT * FROM .. :", ret)
    // SELECT * FROM .. : {"columns":["TS","HIGH","OPEN","LOW","CLOSE","VOLUME"],"values":[[1616110200000,58085.9,57716.2,57664.3,57757.6,24.216], ...]}
    var arr = ret.values 
    var r = []
    for (var i = 0 ; i < arr.length ; i++) {
        r.push({
        	Time : arr[i][0],
        	High : arr[i][1],
        	Open : arr[i][2],
        	Low : arr[i][3],
        	Close : arr[i][4],
        	Volume : arr[i][5]
        })
    }
    return r
}

collecter.deleteTable = function() {
    // DROP TABLE database_name.table_name;
    var strSql = "DROP TABLE " + this.tableName
    var ret = DBExec(strSql)
    if (!ret) {
        Log("delete table", this.tableName, "Failed:", ret)
    } else {
        Log("delete table", this.tableName, " DROP TABLE:", ret)
        this.tableAvaliable = false 
    }
}

function main() {
	collecter.init(tableName)
    while(true) {    
    	var r = _C(exchange.GetRecords)
        // records tbl
        var rTbl = {
            type : "table", 
            title : "Data",
            cols : ["strTime", "Time", "High", "Open", "Low", "Close", "Volume"], 
            rows : [] 
        }
        var arrR = []
        if (collecter.tableAvaliable) {
            arrR = collecter.getRecords()
        }
        for (var i = arrR.length - 1; (i > arrR.length - 1 - 9) && (i >= 0); i--) {
            var bar = arrR[i]
            rTbl.rows.push([_D(bar.Time), bar.Time, bar.High, bar.Open, bar.Low, bar.Close, bar.Volume])
        }
    	LogStatus(_D(), "obtainedKLine data length:", arrR.length, ", collecter.tableAvaliable:", collecter.tableAvaliable, "\n", 
            "`" + JSON.stringify(rTbl) + "`")
    	collecter.run(r)

    	// Interactive testing
    	var cmd = GetCommand()
        if(cmd) {
            // Handle Interaction
            Log("Interaction Commands:", cmd)
            var arr = cmd.split(":")
            // Read from databaseKLine data, refresh chart
            if(arr[0] == "refreshRecords") {
                if (collecter.tableAvaliable) {
                    var records = collecter.getRecords()
                    $.PlotRecords(records, collecter.tableName)   // Use the line drawing library to draw pictures
                } else {
                    Log("The corresponding database table does not exist collecter.tableAvaliable:", collecter.tableAvaliable)
                }
            } else if (arr[0] == "deleteBDTable") {     // Delete database table
                collecter.deleteTable()
            } else if (arr[0] == "initCollecter") {     // Initialize the collector
                Log("Initialize the collector")
                collecter.init(tableName)
            }
        }
    	Sleep(5000)
    }
}



```

> Detail

https://www.fmz.com/strategy/267223

> Last Modified

2021-03-30 11:57:49
