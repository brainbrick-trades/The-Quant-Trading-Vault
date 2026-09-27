
> Name

My-Language-Position-Change-Push-Notification

> Author

发明者量化





> Source (MyLanguage)

``` pascal

C>HV(H, 10),SPK;
C<LV(L, 15),BPK;
AUTOFILTER;

%%
// The following code is appended to anyMyLanguage strategies can ultimately push position changes to your phoneAppAnd WeChat
if (typeof(scope._tmp) !== 'number') {
    scope._tmp = 0;
}
var pos = scope.get_locals('BKVOL') - scope.get_locals('SKVOL');
if (pos != scope._tmp) {
   scope._tmp = pos;
   Log('Notify position changes:', scope.symbol, pos, '@');
}
%%
```

> Detail

https://www.fmz.com/strategy/305745

> Last Modified

2021-08-09 14:01:30
