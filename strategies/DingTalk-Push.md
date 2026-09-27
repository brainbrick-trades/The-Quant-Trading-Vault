
> Name

DingTalk-Push

> Author

一拳男孩

> Strategy Description

- $.ddNotice(title, content)
> title: String type, the title of the push notification
> content: Array type, markdown format

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|DING_URI|DingTalk URI | DingTalkURI|


> Source (javascript)

``` javascript
$.ddNotice = function(title, content) {
    content = content == null ? title : content instanceof Array ? content.join('\n') : content
    HttpQuery(DING_URI, {
        method: 'POST',
        timeout: 3000,
        data: JSON.stringify({
            msgtype: 'markdown',
            markdown: {
                title: title,
                text: content
            }
        })
    }, null, 'Content-Type: application/json')
}
```

> Detail

https://www.fmz.com/strategy/159668

> Last Modified

2019-08-13 22:38:39
