"""WeChat Official Account signature verification.

WeChat verifies your webhook by signing the developer-chosen Token with the
request's timestamp and nonce:

    sha1(''.join(sorted([token, timestamp, nonce])))
"""
from __future__ import annotations

import argparse
import hashlib
import hmac


def make_signature(token: str, timestamp: str, nonce: str) -> str:
    """Return the WeChat SHA1 signature for token/timestamp/nonce."""
    parts = [str(token), str(timestamp), str(nonce)]
    parts.sort()
    return hashlib.sha1("".join(parts).encode("utf-8")).hexdigest()


def verify_signature(token: str, timestamp: str | None, nonce: str | None, signature: str | None) -> bool:
    """Constant-time verification of a WeChat webhook signature."""
    if not token or timestamp is None or nonce is None or signature is None:
        return False
    expected = make_signature(token, timestamp, nonce)
    return hmac.compare_digest(expected, signature)


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify a WeChat Official Account signature")
    parser.add_argument("--token", required=True)
    parser.add_argument("--timestamp", required=True)
    parser.add_argument("--nonce", required=True)
    parser.add_argument("--signature")
    args = parser.parse_args()
    sig = make_signature(args.token, args.timestamp, args.nonce)
    print(sig)
    if args.signature is not None:
        print("valid" if hmac.compare_digest(sig, args.signature) else "invalid")


if __name__ == "__main__":
    main()
