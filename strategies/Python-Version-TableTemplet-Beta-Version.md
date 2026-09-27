
> Name

Python-Version-TableTemplet-Beta-Version

> Author

发明者量化-小小梦





> Source (python)

``` python
# TableTemplet
import json
listener = {}

class Table():
    """docstring for Table"""
    def __init__(self):
        self.tb = {
            "type" : "table",
            "title" : "Table",
            "cols" : [],
            "rows" : []
        }

    def SetColRow(self, col_index, row_index, row):
        if (type(col_index) is int) and (type(row_index) is int) :
            if (col_index > len(self.tb["cols"])) or (row_index > len(self.tb["rows"])) :
                Log("Index out of range!col_index:", col_index, "row_index:", row_index)
            else :
                self.tb["rows"][row_index - 1][col_index - 1] = row
        else :
            Log("col_index:", col_index, "row_index:", row_index)
            raise "SetColRow Parameter error!"

    def SetBtn(self, col_index, row_index, cmd, name, callback):
        global listener
        if (type(col_index) is int) and (type(row_index) is int) :
            if (col_index > len(self.tb["cols"])) or (row_index > len(self.tb["rows"])) :
                Log("Index out of range!col_index:", col_index, "row_index:", row_index)
            else :
                self.tb["rows"][row_index - 1][col_index - 1] = {"type" : "button", "cmd" : cmd, "name" : name}
                listener[cmd] = callback
        else :
            Log("col_index:", col_index, "row_index:", row_index)
            raise "SetColRow Parameter error!"
    
    def SetRows(self, row_index, Rows):
        pass

    def SetCols(self, Cols):
        self.tb["cols"] = Cols

    def GetRows(self, row_index):
        if (type(row_index) is int) and (row_index < len(self.tb["rows"])) :
            return self.tb["rows"][row_index - 1]
        else :
            Log("Parameter error! Or parameter index out of range!")

    def Init(self, title, col_length, row_length):  
        self.tb["title"] = title
        for i in range(1, row_length + 1) :
            if i == 1 :
                for n in range(1, col_length + 1) :
                    self.tb["cols"].append(n)
            self.tb["rows"].append([])
            for m in range(1, col_length + 1) :
                self.tb["rows"][i - 1].append(str(i) + "/" + str(m))


class CreateTableManager():
    """docstring for CreateTableManager"""
    def __init__(self):        # CreateTableManager Constructor
        self.tables = []       # Used to store table objects
    
    def GetTable(self, index):
        if type(index) is int :
            return self.tables[index]
        elif type(index) is str :
            for i in range(len(self.tables)) :
                if self.tables[i]["title"] == index:
                    return self.tables[i]
        else :
            Log("GetTableParameters:", index)
            raise "GetTable Parameter error!"
    
    def AddTable(self, title, col_length, row_length):    # cols, rows
        tb = Table()
        tb.Init(title, col_length, row_length)
        self.tables.append(tb.tb)
        return tb

    def UpdateCMD(self):
        global listener
        cmd = GetCommand()
        if cmd :
            cmdList = cmd.split(":")
            if len(cmdList) == 2 :                                         # Added conflict detection for interactions with the main strategy.
                Log("Received TableTemplet Interactive commands outside the template!", cmdList)     
                return
            if listener[cmd] :
                listener[cmd](cmd)
            else :
                Log("TableTemplet Template does not contain a name called:" + cmd + "command")
    
    def LogStatus(self, before, end):
        self.UpdateCMD()
        LogStatus(before + '\n`' + json.dumps(self.tables) + '`\n' + end)

# Export Function
ext.CreateTableManager = CreateTableManager

# Test Code

def test1(cmd):        # used as function callback
    Log(_D(), cmd)

def main():
    account = exchange.GetAccount()
    array1 = ["aa", "bb", "cc"]
    array2 = [1, 2, 4, 55]

    TbM = ext.CreateTableManager()
    tb1 = TbM.AddTable("tb1", 6, 7)
    
    tb1.SetColRow(3, 4, "hello")
    tb1.SetColRow(3, 5, 12)
    tb1.SetColRow(3, 6, account)
    tb1.SetColRow(3, 7, array1)
    tb1.SetColRow(3, 2, array2)
    tb1.SetBtn(3, 1, "Cover", "Close Position", test1)    # Due to python No multi-line anonymous functions (such asJS of function(){...})So you can declare ordinary functions to pass in.
    tb_1 = TbM.GetTable(0)
    tb_2 = TbM.GetTable("tb1")
    Log(tb_1)
    Log(tb_2, "#FF0000")
    tb1_row1 = tb1.GetRows(1)
    Log(tb1_row1)
    tb1_row1[0] = "Modify"
    x = 0
    
    # tb2
    tb2 = TbM.AddTable("tb2", 4, 4)

    while True :
        x = x + 1
        tb1_row1[0] = _D()
        tb1.SetCols([x + 1, x + 2, x + 3, x + 4, x + 5, x + 6])
        TbM.LogStatus("begin", "end")
        Sleep(1000)













```

> Detail

https://www.fmz.com/strategy/46031

> Last Modified

2022-03-09 14:03:32
