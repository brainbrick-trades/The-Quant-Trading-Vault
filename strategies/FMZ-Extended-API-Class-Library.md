
> Name

FMZ-Extended-API-Class-Library

> Author

ChaoZhang

> Strategy Description

Article from Mr. Ao<<Ok teaches you how to use JS to connect FMZ extensionAPI>>
https://www.fmz.com/digest-topic/5631

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|AccessKey|AccessKey|AccessKey|
|SecretKey|SecretKey|SecretKey|


> Source (javascript)

``` javascript
var URL = "https://www.fmz.com/api/v1?";
function GetUrl(method, dateInfo) {
	var param = getParam("1.0.0", AccessKey, method, dateInfo);
	//Log("param:",param);
	//Get concatenated parametersmd5Encrypted result
	var md5Result = md5(param);
	//assign the encryption result to the base parameter object
	param.sign = md5Result;
	//Get RequestapiofURL
	return getFinalUrl(param);
}
//Fetch via parametersAPIInformation
$.getAPIInfo = function (method, dateInfo) {
	var info;
	while (true) {
        try {
		info = HttpQuery(GetUrl(method, dateInfo));
		if (!info && info.indexOf("result") == -1) {
			Log("infoError", info,method,dateInfo);
			Sleep(2000);
		} else {
			break;
		}
        } catch (error) {
           Log(error.massage)
        }

	}

	return JSON.parse(info);
}

//Get Base5Object of parameters
function getParam(version, ak, method, args) {
	return {
		version: version,
		access_key: ak,
		method: method,
		args: JSON.stringify(args),
		nonce: new Date().getTime(),
	};
}

//Executemd5Encrypt
function md5(param) {
	var paramUrl = param.version + "|" + param.method + "|" + param.args + "|" + param.nonce + "|" + SecretKey;
	//Log("paramUrl:",paramUrl);
	return Hash("md5", "hex", paramUrl);
}

//Get the final requestURL
function getFinalUrl(param) {
    //Log(param)
	return URL + "access_key=" + AccessKey + "&nonce=" + param.nonce + "&args=" + escape(param.args) + "&sign=" + param.sign + "&version=" + param.version + "&method=" + param.method;
}

//jsNot Supported...argsNaming method, so use insteadargumentsKeyword to get the parameter array
$.getArgs = function () {
	return [].slice.call(arguments);
}
function init(){
    //Log("mode")
    if (AccessKey == "" || SecretKey == "") {
        throw "AccessKeyOr the SecretKey cannot be empty";
    }
    
    //let robotId = _G();
    //$.getAPIInfo("CommandRobot",$.getArgs(robotId,"coverAll"))
}
$.AccessKey = AccessKey;
$.SecretKey = SecretKey;


```

> Detail

https://www.fmz.com/strategy/318271

> Last Modified

2024-06-01 18:40:01
