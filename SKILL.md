---
name: wechat-official-account-kit
description: >
  Build an AI/agent integration for a WeChat Official Account (微信公众号 / 服务号)
  using passive reply webhooks. Use this when a human asks to make an AI act as
  public-account customer service, implement 公众号被动回复, validate
  signature/timestamp/nonce/echostr, handle POST XML, respect the 5-second reply
  SLA, or bridge slow tasks to the customer-service API. This is distinct from
  personal-WeChat/iLink MCP integrations such as lingtai-wechat.
version: 0.1.0
---

# WeChat Official Account passive-reply agent kit

Use this skill when the task involves **WeChat Official Account / 公众号 / 服务号** webhooks, especially passive replies. Do **not** use it for personal WeChat iLink bots; those are a different protocol and product surface.

## Decision tree

1. Human wants a public account/service account AI assistant → use this kit.
2. Human wants personal WeChat direct messaging / QR login / iLink bot token → use the personal-WeChat MCP path (`lingtai-wechat`).
3. Human wants enterprise customer-service operations / staff tooling → evaluate WeCom / 微信客服 separately.

## MVP architecture

```text
WeChat user
  -> sends message to Official Account
  -> WeChat server POSTs XML to your HTTPS webhook
  -> webhook verifies signature, parses XML
  -> fast AI path returns XML text reply within 5s
```

For slow tasks:

```text
POST XML arrives
  -> verify + parse
  -> enqueue job
  -> immediately return success or short ack
  -> later send via customer-service API if window/permission allows
     OR ask user to send a keyword to retrieve result
```

## Server verification

Official Account backend setup sends a GET request to your URL with:

- `signature`
- `timestamp`
- `nonce`
- `echostr`

Verification:

```python
from wechat_mp_agent_kit.signature import verify_signature

if verify_signature(token, timestamp, nonce, signature):
    return echostr
return 403
```

The signature is `sha1(''.join(sorted([token, timestamp, nonce])))`.

## POST XML handling

Incoming text message shape is roughly:

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

Text reply swaps sender/receiver:

```python
from wechat_mp_agent_kit.reply import text_reply

xml = text_reply(
    to_user=incoming['FromUserName'],
    from_user=incoming['ToUserName'],
    content='AI reply here',
)
```

## 5-second rule

WeChat disconnects if no response arrives within 5 seconds and retries up to 3 total attempts. Therefore:

- Use a fast model or deterministic answer for direct passive replies.
- Put a hard timeout around LLM calls, e.g. 2–3 seconds.
- If timeout is likely, return `success` and queue work.
- Dedupe by `MsgId`; for events use `FromUserName + CreateTime`.

## First implementation checklist

1. Clone this repo.
2. Run the FastAPI template locally.
3. Expose it over HTTPS.
4. Configure Official Account URL + Token.
5. Pass GET verification.
6. Send a text message to the account.
7. Confirm the webhook returns text XML within 5 seconds.
8. Add logging and retry dedupe.
9. Only then add customer-service API and media uploads.

## Security checklist

- Always verify signatures on GET and POST.
- Treat incoming XML as untrusted input; use `defusedxml` where possible.
- Do not log AppSecret/access_token/user secrets.
- Use HTTPS.
- Start in plaintext message mode for MVP; support safe/encrypted mode later if needed.
- Escape/split CDATA safely in replies.

## Files to read next

- `templates/fastapi_wechat_mp.py` — runnable webhook template.
- `reference/passive-reply.md` — distilled official constraints.
- `reference/slow-task-and-customer-service.md` — async strategy.
- `reference/deployment-checklist.md` — operational checklist.
