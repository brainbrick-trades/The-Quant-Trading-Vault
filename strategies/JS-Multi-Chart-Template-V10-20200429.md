
> Name

JS-Multi-Chart-Template-V10-20200429

> Author

中本姜



> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|LogLevel|3|LogLevel|
|IsAsync|false|Asynchronously call API to obtain data|
|LoopInterval|3|Polling time (seconds))|
|MinDiff|0.8|Minimum Spread|


> Source (javascript)

``` javascript
/*
v2.0 (20200429)
 * Solve the problem of tag affiliation
v2.0 (20171225)
 * Support dynamic column chart
v1.0 (20170725)
 * Basic multi-chart plotting template
 * This template can plot various types of time series charts on multiple charts
   Includes time series charts of curves, candles, and histograms
 * This template does not consider non-timeline scenarios
 * chart = $.ChartObj("title0"): Create a chart
 * series = chart.CreateSeries("series0", 'spline'): Draw a picture in the chart
 * series.AddData(100): Fill numbers in the graph for real-time plotting
*/
$.PlotFlag = function(time, text, title, shape, color) {
    var obj = {
        x: time,
        color: color,
        shape: shape,
        title: title,
        text: text
    }
    if (preFlagTime != time) {
        preFlagTime = time
        chart.add(seriesIdx, obj)
    } else {
        chart.add(seriesIdx, obj, -1)
    }
    return chart
}


function EasyReadTime(millseconds) {
    if (typeof millseconds == 'undefined' ||
        !millseconds) {
        millseconds = new Date().getTime();
    }
    var newDate = new Date();
    newDate.setTime(millseconds);
    return newDate.toLocaleString();
}

var RedColor = "#ff0000"; // Red Marker
var GreenColor = "#006600"; // Green Marker
var YellowColor = "#FFA500"; // Orange Marker

$.DuoColor = GreenColor
$.KongColor = RedColor
$.PingColor = YellowColor

$.RedColor = RedColor;
$.GreenColor = GreenColor;
$.YellowColor = YellowColor;

// Critical Log, Appearslog, the entire program will exit
LOG_CRT = 0;
LOG_ERR = 1;
LOG_WARN = 2;
LOG_INFO = 3;
LOG_DA_DBG = 4;
LOG_WK_DBG = 5;

var LogLevelStr = ["LOG_CRT ", "LOG_ERR ", "LOG_WARN", "LOG_INFO ", "LOG_DA_DBG ", "LOG_WK_DBG "];
var LogColorStr = [RedColor, RedColor, YellowColor, GreenColor, "", ""];

function LogPush()
{
    var args = [].slice.call(arguments);
    var _LogLevel = args[0];

    if (_LogLevel <= LogLevel) {
        args[0] = LogLevelStr[_LogLevel];
        args.push(LogColorStr[_LogLevel]);
        if (_LogLevel == LOG_CRT) {
            throw args;
        } else {
            Log.apply(this, args);
        }
    }
}

// GlobalChartObject used for actual plotting
var G_Chart = null;
// GlobalChartObjArray is used to store charts
var G_ChartObjList = [];

/* Define a picture
 * name: Chart Name
 * type: Chart Type
 	- candlestick: Candlestick Chart
 	- spline: Line Chart
 	- column: Bar Chart
 * color: Chart Color
*/
function _SeriesObj(name, type, color, yAxis, is_primary) {
	this._Name = name;
	this._Type = type;
	this._Color = color;
	this._Index = null;
	this._LastTime = null;
    this._yAxis = yAxis;
    this._is_primary = is_primary
    this._ColumnIndex = [];
    this._Rec = {'Time': null, 'High': null, 'Low': null, 'Close': null, 'Open': null}
    if (this._Type == 'column') {
        this._xAxis = 1;
    } else {
        this._xAxis = 0;
    }

	this.GetCfg = function() {
		var cfg;
        var xAxis_value;
		if (!color || this._Color == '') {
			cfg = {
				type: this._Type,
				name: this._Name,
				data: [],
                xAxis: this._xAxis,
                yAxis: this._yAxis};
		} else {
			cfg = {
				type: this._Type,
				name: this._Name,
				color: this._Color,
				data: [],
                xAxis: this._xAxis,
                yAxis: this._yAxis};
		}
        if (this._Type == 'candlestick') {
            cfg.color = '#DD2200';
            cfg.upColor = '#33AA11';
            cfg.lineColor = '#DD2200'; 
            cfg.upLineColor = '#33AA11';
        }
        if (this._Type == 'flags') {
			cfg = {
				type: this._Type,
				name: this._Name,
				data: []}
            cfg.onSeries = 'primary';
        }
        //if (this._Type == 'column') {
        //    cfg.dataLabels = {
        //            enabled: true,
        //            formatter: function() {        //Formatted output display
        //              return (this.y) + "%";
        //            },
        //            verticalAligh: "top",
        //    };
        //}
        if (typeof(this._is_primary) != 'undefined' && this._is_primary != null &&
            this._is_primary) {
            cfg.id = "primary";
        }
		return cfg;
	}; 
    
    this.AddFData = function(time, title, text, color, shape) {
        if (this._Type != 'flags') {
			LogPush(LOG_CRT, this._Name, this._Type, "Label data cannot be added if it is not a labeled graph.");
        }
        var obj = {
            x: time,
            color: color,
            shape: shape,
            title: title,
            text: text
        }
        if (this._LastTime != time) {
            this._LastTime = time
            G_Chart.add(this._Index, obj)
        } else {
            /* Allow repeated drawing of data */
            G_Chart.add(this._Index, obj)
            //G_Chart.add(this._Index, obj, -1)
        }
    };
    
    this.AddKData = function(time, close, high, low, open) {
        if (this._Type != 'candlestick') {
			LogPush(LOG_CRT, this._Name, this._Type, "candlestick data cannot be added if it is not a candle chart");
        }
        
        var _RECS = function(k_change, rec, data) {
            if (k_change) {
                rec.High = data.High;
                rec.Low = data.Low;
                rec.Open = data.Open;
                rec.Time = data.Time;
            }
            rec.Close = data.Close;
            rec.Low = Math.min(rec.Low, data.Low);
            rec.High = Math.max(rec.High, data.High);
            return [rec];
        };
        
        if (typeof(high) == 'undefined') {
            high = close;
        }
        if (typeof(low) == 'undefined') {
            low = close;
        }
        if (typeof(open) == 'undefined') {
            open = close;
        }
        var k_change = false;
        if (!this._LastTime || this._LastTime != time) {
            k_change = true;
        }
        var new_data = _RECS(k_change, this._Rec,
                             {'High': high, 'Low': low, 'Open': open, 'Close': close, 'Time': time});
        this.AddData(new_data, time);
    };

	/* Add Data
     * data: Raw Data
     * time(optional): Mark the time point of the current data, with the current time used by default 
     * is_time_data(Optional): Whether the data is time series related, defaulttrue
	 */
	this.AddData = function(data, time, is_time_data) {
		if (!G_Chart) {
			LogPush(LOG_CRT, "Cannot draw the graph because the global graph is not defined!");
		}

        if (this._Type == 'column') {
            var column_name = data[0];
            var value = data[1];
            if (this._ColumnIndex[column_name] == null) {
		        G_Chart.add([this._Index, [column_name, value]]);
                for (var i in this._ColumnIndex) {
                    this._ColumnIndex[i] += -1;
                }
                this._ColumnIndex[column_name] = -1;
                //Log(column_name, this._ColumnIndex[column_name]);
            } else {
                //Log(this._Index, column_name, value, this._ColumnIndex[column_name]);
                G_Chart.add([this._Index, [column_name, value, this._ColumnIndex[column_name]]]);
            }
            return;
        }
        
		if (typeof(is_time_data) == 'undefined' || !is_time_data) {
			is_time_data = true;
		}
        
        var now_time;
        if (typeof(time) == 'undefined' || !time) {
		    now_time = new Date().getTime();
        } else {
            now_time = time;
        }
		if (is_time_data || this._Type == 'candlestick') {
			if (this._Type == 'candlestick') {
				var now_record = data[data.length-1];
				var now_data = [now_record.Time, now_record.Open, now_record.High,
                                now_record.Low, now_record.Close];
				var last_data = null;
				if (data.length > 1) {
					var last_record = data[data.length-2];
					last_data = [last_record.Time, last_record.Open, last_record.High,
                	             last_record.Low, last_record.Close];
				}
				now_time = now_data[0];
				if (!this._LastTime) {
					this._LastTime = now_time;
				}
				if (now_time == this._LastTime) {
					G_Chart.add([this._Index, now_data, -1]);
				} else {
					if (last_data) {
						G_Chart.add([this._Index, last_data, -1]);
					}
					G_Chart.add([this._Index, now_data]);
				}
			} else if (Array.isArray(data)) {
				now_time = data[0];
                if (now_time == this._LastTime) {
				    G_Chart.add([this._Index, data, -1]);
                } else {
				    G_Chart.add([this._Index, data]);
                }
			} else {
				time_data = [now_time, data];
                if (now_time == this._LastTime) {
				    G_Chart.add([this._Index, time_data, -1]);
                } else {
				    G_Chart.add([this._Index, time_data]);
                }
			}
		} else {
			G_Chart.add([this._Index, data]);
		}

		this._LastTime = now_time;
	};

	this.GetName = function() {
		return this._Name;
	};
}

/* Define a chart
 * parm title: Chart Name
 * parm is_stock: Whether to use HighStock to draw charts
 * You can draw various types of pictures on the chart(series)
 */
function _ChartObj(title, is_stock) {
	this._Title = title;
	if (typeof(is_stock) == 'undefined') {
		is_stock = true;
	}
	this._IsStock = is_stock;
	// Chart Array
	this._Series = [];
	// Figure configuration information
	this._SeriesCfg = [];
    this._yAxis = 0;
	
    /* Create a plot on the chart 
        @series_name(Required): Figure title
        @series_type(Required): Chart type 'column' (dynamic column chart), 'candlestick' (candle chart), 'spline' (curve chart), 'flags' (label), 'line' (straight line))
        @series_color(Optional): Use color for line drawing, default is automatic
        @is_right(Optional): whether to use the right vertical axis, default is to use the left vertical axis for all
        @is_primary(Optional): Whether to designate this series as primary. The flag will attach to it
    */
	this.CreateSeries = function(series_name, series_type, series_color, is_right, is_primary) {
		for (var name in this._Series) {
			if (name == series_name) {
				//LogPush(LOG_CRT, "Figures with the same name cannot be created in the same table");
				//return null;
                LogPush(LOG_INFO, name, "Will be returned directly if it already exists");
                return this._Series[name]
			}
		}
        var yAxis = 0;
        if (typeof(is_right) != 'undefined') {
            yAxis = is_right ? 1: 0;
        } else {
            yAxis = this._yAxis;
        }
		var series = new _SeriesObj(series_name, series_type, series_color, yAxis, is_primary);
		this._Series[series_name] = series;
		var series_cfg = series.GetCfg();
		this._SeriesCfg.push(series_cfg);
		_UpdateSeriesIndex();
		return series;
	};

	this.AddData = function(series_name, data, is_time_data) {
		var series = this._Series[series_name];
		if (!series) {
			LogPush(LOG_ERROR, "Cannot find graph in graph ", this._Title, " ", series_name);
		}
		series.AddData(data, is_time_data);
		$.ChartUpdate();
	};

	this.GetCfg = function() {
		var cfg = {
			__isStock: this._IsStock,
			legend: {enabled: true},
    		tooltip: {xDateFormat: '%Y-%m-%d %H:%M:%S, %A'},
			chart: {zoomType: 'x',
                    panning: true},
			title: {text: this._Title},
			
    		rangeSelector: {
    	        buttons:  [
					{type: 'hour',count: 1, text: '1h'},
					{type: 'hour',count: 3, text: '3h'},
					{type: 'hour', count: 8, text: '8h'},
					{type: 'all',text: 'All'}],
    	        selected: 0,
    	        inputEnabled: false
    	    },
    		xAxis: [{type: 'datetime'},
                    {categories: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}],
    		yAxis: [{
    		        title: {text: 'Price line'},//Title
    		        style: {color: '#4572A7'},//Style 
    		        opposite: false  //Generate left Y-axis
    		        },
    		        {
    		        title: {text: 'Price amplitude line
    		        opposite: true  //Generate right Y-axis
    		        }
    		],
			series: this._SeriesCfg,
		};
		return cfg;
	};

	this.GetName = function() {
		return this._Title;
	};
}

function _UpdateSeriesIndex() {
	var index = 0;
	$.ChartUpdate();
	for (var i = 0; i < G_ChartObjList.length; i++) {
		var chart = G_ChartObjList[i];
		for (var series_name in chart._Series) {
			var series = chart._Series[series_name];
			series._Index = index;
			LogPush(LOG_WK_DBG, "Chart ", chart.GetName(), " Mid Chart ",
                    series.GetName(), ", Index Number is:", series._Index);
			index += 1;
		}
	}
}

$.G_Chart = function() {
    return G_Chart;
}

$.ChartUpdate = function() {
	cfg_list = [];
	for (var i = 0; i < G_ChartObjList.length; i++) {
		var chart = G_ChartObjList[i];
		var cfg = chart.GetCfg();
		cfg_list.push(cfg);
	}
	if (!G_Chart) {
		G_Chart = Chart(cfg_list);
		//G_Chart.reset();
	} else {
		G_Chart.update(cfg_list);
	}
};

/* Create a new chart.
   @title: Chart Title
   @is_stock: Whether to use HighStock for plotting, defaulttrue
              Candlestick must betrue
              Dynamic column chart must befalse
   return: Returns a chart, in which various graphs can be created
*/
$.ChartObj = function(title, is_stock) {
	var chart = new _ChartObj(title, is_stock);
	G_ChartObjList.push(chart); 
	return chart;
};

$.GetTickersAsync = function(exchanges) {
	tickers = [];
	var exchange_handlers = [];
	for (var i in exchanges) {
		if (IsAsync) {
			exchange_handlers[i] = exchanges[i].Go("GetTicker");
		} else {
			exchange_handlers[i] = exchanges[i].GetTicker();
		}
	}
	for (var i in exchange_handlers) {
		if (IsAsync) {
			tickers[i] = exchange_handlers[i].wait(500);
		} else {
			tickers[i] = exchange_handlers[i];
		}
	}
	return tickers;
};

var CoinNameMapping = {
	'BTC_CNY': 'BTC',
	'LTC_CNY': 'LTC',
	'ETH_CNY': 'ETH',
	'BTS_CNY': 'BTS',
};

function GetCoinType(currency) {
	coin_type = CoinNameMapping[currency];
	if (!coin_type) {
		coin_type = currency;
	}
	return coin_type;
}

function main() {
	var ticker_chart_list = [];
	// Spread Chart
	var diff_chart_list = [];
	var exchange_dict = [];
	var coin_type;

	for (var i = 0; i < exchanges.length; i++) {
		var platform_name = exchanges[i].GetName();
		coin_type = GetCoinType(exchanges[i].GetCurrency());
		if (!exchange_dict[coin_type]) {
			exchange_dict[coin_type] = [];
		}
		if (!exchange_dict[coin_type][platform_name]) {
			exchange_dict[coin_type][platform_name] = exchanges[i];
		}
	}

	for (coin_type in exchange_dict) {
		var title_name = coin_type + "Price charts of each trading platform";
		var chart = $.ChartObj(title_name);
		LogPush(LOG_INFO, "Add Chart:", title_name);
		ticker_chart_list[coin_type] = chart;

		coin_exchanges = exchange_dict[coin_type];
		for (var name in coin_exchanges) {
			var series_name = name + "Current Price";
			var series = chart.CreateSeries(series_name, 'spline', '');
			ticker_chart_list[coin_type][name] = series;
		}
	}

    var column_chart = $.ChartObj("Column Chart", false);
    var column_series = column_chart.CreateSeries("Column Chart", 'column');
	for (coin_type in exchange_dict) {
		var title_name = coin_type + "Price difference chart of each trading platform";
		var chart = $.ChartObj(title_name);
		LogPush(LOG_INFO, "Add Chart:", title_name);
		diff_chart_list[coin_type] = chart;

		coin_exchanges = exchange_dict[coin_type];
		for (var left_name in coin_exchanges) {
			var find = false;
			for (var right_name in coin_exchanges) {
				if (right_name == left_name) {
					find = true;
					continue;
				}
				if (find) {
					var series_name = left_name + "_" + right_name + "Price difference";
					var series = chart.CreateSeries(series_name, 'spline', '');
					if (!diff_chart_list[coin_type][left_name]) {
						diff_chart_list[coin_type][left_name] = [];
					}
					var ele = [];
					ele['left_name'] = left_name;
					ele['right_name'] = right_name;
					ele['series'] = series;
					diff_chart_list[coin_type][left_name].push(ele);
					LogPush(LOG_INFO, "Add a graph in the chart: ", title_name, ":", series_name);
				}
			}
		}
	}

    var n = 0;
	while (true) {
		for (var coin_type in exchange_dict) {
			var tickers = $.GetTickersAsync(exchange_dict[coin_type]);
			var time = new Date().getTime();
			for (var pname in exchange_dict[coin_type]) {
				//var exchange = exchange_dict[coin_type][pname];
				var series = ticker_chart_list[coin_type][pname];
				var records = exchange.GetRecords();
				var ticker = tickers[pname];
				if (!ticker || !ticker.Last || ticker.Sell < ticker.Buy) {
					continue;
				}
				series.AddData([time, ticker.Last]);

				var diff_series_list = diff_chart_list[coin_type][pname];
				if (diff_series_list) {
					for (var i in diff_series_list) {
						diff_series_dict = diff_series_list[i];
						var left_name = diff_series_dict['left_name'];
						var right_name = diff_series_dict['right_name'];
						var diff_series = diff_series_dict['series'];
						var left_ticker = ticker;
						var right_ticker = tickers[right_name];
                        LogPush(LOG_WK_DBG, "left_ticker: ", left_ticker, "right_ticker:", right_ticker);
						if (!right_ticker || !right_ticker.Last || right_ticker.Sell < right_ticker.Buy) {
							continue;
						}
						var sell_diff = left_ticker.Buy - right_ticker.Sell;
						var buy_diff = left_ticker.Sell - right_ticker.Buy;
						if (sell_diff >= 0 && buy_diff >= 0) {
                            if (Math.abs(sell_diff) >= MinDiff) {
							    diff_series.AddData([time, sell_diff]);
                            }
						}
						else if (sell_diff <= 0 && buy_diff <= 0) {
                            if (Math.abs(buy_diff) >= MinDiff) {
							    diff_series.AddData([time, buy_diff]);
                            }
						} 
                        //else {
						//	diff_series.AddData([time, 0]);
						//}
					}
				}
			}
		}
        if (n < 15) {
            column_series.AddData([n%5, n]);
        }
        n++;
        n++;
		Sleep(LoopInterval * 1000);
	}
}
```

> Detail

https://www.fmz.com/strategy/48731

> Last Modified

2020-04-29 16:35:59
