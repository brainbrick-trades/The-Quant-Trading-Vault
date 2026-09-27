
> Name

TableTemplet

> Author

职业养鸡户

> Strategy Description

//by Chicken farming specialist 17/6/21



> Source (javascript)

``` javascript
var listener = Array();
//----------DrawTable-----------
{	
	TableButton = function(cmd,name){
		var self = {}
		self.type = "button";
		self.cmd = cmd;
		self.name = name;
		return self;
	}
	
	$.TableInfo = function() {
		var self = {}
		self.cols = [];
		self.rows = [];
		self.pushBtn = function(col,cmd,name,callback){
			var btn = TableButton(cmd,name)
			self.cols.push(col)
			self.rows.push({'type':'button','cmd':cmd,'name':name})
			listener[cmd] = callback;
		}
		self.push = function(col,row){
			self.cols.push(col)
			self.rows.push(row)
		}
		return self;
	}
	function createTable(){
	    var self = {}
	    self.type = "table"
	    self.title = "Position information"
	    self.cols = []
	    self.rows = []

	    self.SetRowByTableInfo = function(index,argument) {
	    	if(argument.cols != null)
	    		self.cols = argument.cols;
	    	self.rows[index] = argument.rows;
	    }

	    self.SetRow = function (index,rowself){
	        if(self.rows.length < index)
	            self.push("")
	        self.rows[index] = rowself
	    }

	    self.SetRowCount = function(count){
	        while(self.rows.length<count){
	            self.rows.push("")
	        }
	        if(self.rows.length > count){
	            self.rows.splice(count,self.rows.length-count)
	        }
	    }

	    self.GetRow = function(index){
	        return self.rows[index]
	    }

	    self.Init = function(title,cols,rows){
	        self.title =title;
	        if(cols!=null)
	            self.cols = cols;
	        if(rows!=null){
	            
	            for(var i =0;i < rows.length;i++){
	                rows.push("r"+i)
	            }
	        }
	    }
	    return self;
	}

	$.createTableMgr = function(){
	    var self = {}
	    self.table =[]
		
	    self.GetTable = function(index){
	    	if(typeof(index) === 'number'){
	    		return self.table[index]
	    	}else{
		        for(var i = 0;i < self.table.length;i++){
		            if(self.table[i].title == index)
		                return self.table[i]
		        }
	        }
	    }

	    self.AddTable = function(title,cols,rows){
	        var tb = createTable();
	        tb.Init(title,cols,rows);

	        self.table.push(tb)
	        return tb;
	    }
	    self.AddListener = function(key,value){
	    	self.listener[key] = value;
	    }
	    self.UpdateCMD = function(){
	    	var cmd = GetCommand()
	        if (cmd) {
	        	var cmdstr = cmd+"";
	        	if(!!listener[cmdstr]){
	        		listener[cmdstr](cmdstr);
	        	}else{
	        		Log("Cannot find named:"+cmdstr+"command")
	        	}
	        }
	    }	

	    self.LogStatus = function(before,end){	
	        self.UpdateCMD();
	        LogStatus(before+'\n`' + JSON.stringify(self.table)+'`\n'+end); // Support multiple tables displayed simultaneously, Will useTABShow in a group
	        
	    }
	    return self;
	}
}

function main(){
    var tbMgr = $.createTableMgr();
	var tb = tbMgr.AddTable("A Status Bar")
	var tbInfo = $.TableInfo();
	tbInfo.push("Name","Zhang San")
    tbInfo.pushBtn("Button","ButtonCmd","This is a button",function(){
        Log("Hehehe");
    })
	tb.SetRowByTableInfo(0,tbInfo)
    tbMgr.LogStatus("upper","lower")
}
```

> Detail

https://www.fmz.com/strategy/44319

> Last Modified

2017-06-21 11:27:08
