# Passive reply distilled notes

Official doc: <https://developers.weixin.qq.com/doc/subscription/guide/product/message/Passive_user_reply_message.html>

## Mechanism

When a user sends a message to an Official Account, WeChat sends a POST request to the developer server URL. The developer replies by returning a specific XML body in the HTTP response.

Strictly speaking, passive reply is not a separate API call; it is the response to WeChat's POST.

## Timeout and retry

WeChat waits about 5 seconds for the response. If no response arrives, it disconnects and retries, up to 3 total attempts.

If you cannot process in 5 seconds, reply one of:

- `success` (recommended)
- empty string (zero bytes)

This suppresses retries and avoids user-facing service-error prompts.

## Dedupe

- Ordinary messages: dedupe with `MsgId`.
- Events: dedupe with `FromUserName + CreateTime`.

## Text reply XML

```xml
<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>12345678</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[你好]]></Content>
</xml>
```

For replies, `toUser` is the incoming `FromUserName`; `fromUser` is the incoming `ToUserName`.

## Media replies

Image/voice/video/music replies require a `MediaId` obtained by uploading material to WeChat. Do not make media part of the first MVP unless access_token/material upload is already working.
