
> Name

Check-Whether-https-quantla-Argus-Is-Normal

> Author

小草





> Source (python)

``` python
import urllib2
def main():
    Log("Start Checking@")
    while True:
        try:
            urllib2.urlopen("https://quant.la/API/Argus/predict", timeout=15)
            Log("Service Normal")
        except:
            Log(_D()," Service Abnormal@")
        Sleep(10*60*1000)

```

> Detail

https://www.fmz.com/strategy/100344

> Last Modified

2018-06-22 10:29:01
