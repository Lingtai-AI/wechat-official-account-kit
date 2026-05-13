# Slow tasks and customer-service fallback

Passive replies are constrained by the 5-second response window. Agent work that may exceed this window should not block the webhook response.

## Recommended slow path

1. Verify signature and parse message.
2. Store job with user OpenID, incoming message, and dedupe key.
3. Return `success` immediately (or a short passive ack if you can build it fast).
4. Run slow work in background.
5. Deliver result by:
   - customer-service message API if the account has permission and the user is within the allowed interaction window;
   - asking the user to send a keyword such as “结果” to fetch;
   - linking to an H5 page if appropriate.

## Do not

- Keep the POST open while a large model or image generator runs.
- Return JSON to WeChat for passive replies.
- Ignore retries; duplicate jobs are common if you exceed 5 seconds.
