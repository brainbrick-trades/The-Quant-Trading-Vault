
> Name

Oak-Quantification-Use-Extended-API-to-Obtain-Robot-Information-and-Display-It

> Author

奥克量化





> Source (javascript)

``` javascript


var URL = "https://www.fmz.com/api/v1?";
var AK = "b3a53d3XXXXXXXXXXXXXXXXXXX866fe5";//Replace here with your ownAccessKey
var SK = "1d9ddd7XXXXXXXXXXXXXXXXXXX85be17";//Replace here with your ownSecretKey
var OFF_SET = 0;//Query page number subscript
var PAGE_LENGTH = 5;//Query the data length of the page

function main() {
    LogReset();
    while(true){
        //Get the bot list information
        var robotListJson = getAPIInfo('GetRobotList',getArgs(OFF_SET,PAGE_LENGTH,-1));
        //Retrieve the bot list information
        var robotList = robotListJson.data.result.robots;
        //Create an array to display robot information
        var infoArr = new Array();
        var infoArr_index = 0;
        for (index = 0; index < robotList.length; index++) {
            var robot = robotList[index];
            //Remove the currently looped robotID
            var robotId = robot.id;
            //Get detailed information about the robot
            var robotDetailJson = getAPIInfo('GetRobotDetail',getArgs(robotId));
            var robotDetail = robotDetailJson.data.result.robot;
            //Convert the details into array objects
            var arr = getLogPrientItem(robotDetail);
            infoArr[infoArr_index] = arr;
            infoArr_index++;
        }
        Log("infoArr:",infoArr);
        LogStatus('`' + JSON.stringify(getLogPrient(infoArr)) + '`');
        Sleep(30000);
    }
}

function getLogPrient(infoArr){
    return table = {
            type: 'table',
            title: 'OK Quant robot display',
            cols: ['Robot ID', 'Robot name', 'Strategy name', 'Next deduction time', 'Time consumed ms', 'Amount CNY consumed', 'Latest active time', 'Whether it is public'],
            rows: infoArr
        };
}

//Fetch via parametersAPIInformation
function getAPIInfo(method,dateInfo){
    //Obtain5basic parameter objects
    var param = getParam("1.0.0",AK,method,dateInfo);
    //Log("param:",param);
    //Get concatenated parametersmd5Encrypted result
    var md5Result = md5(param);
    //assign the encryption result to the base parameter object
    param.sign = md5Result;
    //Get RequestapiofURL
    var finalUrl = getFinalUrl(param);
    //Log("finalUrl:",finalUrl);
    //Execute the request and print the result
    var info = HttpQuery(finalUrl);
    //Log("info:",info);
    return JSON.parse(info);
}

//Get Base5Object of parameters
function getParam(version,ak,method,args){
    return {
        'version': version,
        'access_key': ak,
        'method': method,
        'args': JSON.stringify(args),
        'nonce': new Date().getTime()
    }
}

//Executemd5Encrypt
function md5(param){
    var paramUrl = param.version+"|"+param.method+"|"+param.args+"|"+param.nonce+"|"+SK
    //Log("paramUrl:",paramUrl);
    return Hash("md5", "hex", paramUrl)
}

//Get the final requestURL
function getFinalUrl(param){
    return URL+"access_key="+AK+"&nonce="+param.nonce+"&args="+param.args+"&sign="+param.sign+"&version="+param.version+"&method="+param.method;
}

//jsNot Supported...argsNaming method, so use insteadargumentsKeyword to get the parameter array
function getArgs(){
    return [].slice.call(arguments);
}

//Get display details object'Robot ID', 'Robot name', 'Strategy name', 'Next deduction time', 'Time consumed ms', 'Amount CNY consumed', 'Latest active time', 'Whether it is public'],
function getLogPrientItem(robotDetail){
    var itemArr = new Array();
    var iteArr_index = 0;
    itemArr[iteArr_index++] = robotDetail.id;
    itemArr[iteArr_index++] = robotDetail.name;
    itemArr[iteArr_index++] = robotDetail.strategy_name;
    itemArr[iteArr_index++] = robotDetail.charge_time;
    itemArr[iteArr_index++] = robotDetail.charged;
    itemArr[iteArr_index++] = robotDetail.consumed/1e8;
    itemArr[iteArr_index++] = robotDetail.refresh;
    itemArr[iteArr_index++] = robotDetail.public == 0?"Public":"Not disclosed";
    return itemArr;
}

```

> Detail

https://www.fmz.com/strategy/208526

> Last Modified

2020-05-18 21:28:05
