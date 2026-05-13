# XML format notes

## Incoming text

```xml
<xml>
  <ToUserName><![CDATA[gh_xxx]]></ToUserName>
  <FromUserName><![CDATA[o_user_openid]]></FromUserName>
  <CreateTime>1234567890</CreateTime>
  <MsgType><![CDATA[text]]></MsgType>
  <Content><![CDATA[hello]]></Content>
  <MsgId>...</MsgId>
</xml>
```

## Passive text reply

```xml
<xml>
  <ToUserName><![CDATA[o_user_openid]]></ToUserName>
  <FromUserName><![CDATA[gh_xxx]]></FromUserName>
  <CreateTime>1234567890</CreateTime>
  <MsgType><![CDATA[text]]></MsgType>
  <Content><![CDATA[AI reply]]></Content>
</xml>
```

## Safe CDATA

If content can contain `]]>`, split it before wrapping in CDATA. See `wechat_mp_agent_kit.reply._cdata`.
