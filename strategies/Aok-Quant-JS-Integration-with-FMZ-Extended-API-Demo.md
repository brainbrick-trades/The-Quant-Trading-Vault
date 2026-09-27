
> Name

Aok-Quant-JS-Integration-with-FMZ-Extended-API-Demo

> Author

奥克量化





> Source (javascript)

``` javascript

var URL = "https://www.fmz.com/api/v1?";
var AK = "b3a53d3XXXXXXXXXXXXXXXXXXX866fe5";//Replace here with your ownAccessKey
var SK = "1d9ddd7XXXXXXXXXXXXXXXXXXX85be17";//Replace here with your ownSecretKey

//Get Base5Object of parameters
function getParam(version,ak,args){
    return {
        'version': version,
        'access_key': ak,
        'method': 'GetNodeList',
        'args': JSON.stringify(args),
        'nonce': new Date().getTime()
    }
}

//Executemd5Encrypt
function md5(param){
    var paramUrl = param.version+"|"+param.method+"|"+param.args+"|"+param.nonce+"|"+SK
    Log("paramUrl:",paramUrl);
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

function main() {
    //Obtain5basic parameter objects
    var param = getParam("1.0.0",AK,getArgs());
    Log("param:",param);
    //Get concatenated parametersmd5Encrypted result
    var md5Result = md5(param);
    //assign the encryption result to the base parameter object
    param.sign = md5Result;
    //Get RequestapiofURL
    var finalUrl = getFinalUrl(param);
    Log("finalUrl:",finalUrl);
    //Execute the request and print the result
    var info = HttpQuery(finalUrl);
    Log("info:",info);
}
```

> Detail

https://www.fmz.com/strategy/208065

> Last Modified

2020-05-16 21:35:13
