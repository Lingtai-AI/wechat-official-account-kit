# Deployment checklist

## Public endpoint

- HTTPS URL reachable by WeChat servers.
- Stable route, e.g. `/wechat/mp/webhook`.
- Logs for GET verification and POST message IDs.

## Official Account backend

- URL set to webhook endpoint.
- Token matches server `WECHAT_MP_TOKEN`.
- EncodingAESKey recorded; plaintext mode for MVP, safe mode later.

## Tests

- GET verification with valid signature returns `echostr`.
- GET invalid signature returns 403.
- POST sample text returns XML in under 5 seconds.
- Duplicate `MsgId` returns `success` or is deduped.
- Slow agent timeout returns `success` instead of hanging.

## Observability

- Log dedupe key, MsgType, latency, response mode (`xml`, `success`, `error`).
- Do not log AppSecret/access_token.
