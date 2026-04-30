#!/usr/bin/env python3
"""Get an Avito OAuth2 access token via Client Credentials flow.

Usage:
    AVITO_CLIENT_ID=... AVITO_CLIENT_SECRET=... python3 get_token.py

Prints the access_token to stdout. Token TTL is 24h; cache it yourself if you
make many calls. Avito returns 401 for expired tokens — refresh and retry.
"""
import json
import os
import sys
import urllib.parse
import urllib.request

TOKEN_URL = "https://api.avito.ru/token"


def get_token(client_id: str, client_secret: str) -> dict:
    body = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }).encode()
    req = urllib.request.Request(
        TOKEN_URL,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def main() -> int:
    cid = os.environ.get("AVITO_CLIENT_ID")
    secret = os.environ.get("AVITO_CLIENT_SECRET")
    if not cid or not secret:
        print("error: set AVITO_CLIENT_ID and AVITO_CLIENT_SECRET", file=sys.stderr)
        return 2
    try:
        data = get_token(cid, secret)
    except urllib.error.HTTPError as e:
        print(f"error: HTTP {e.code} from token endpoint: {e.read().decode(errors='replace')}", file=sys.stderr)
        return 1
    if "--json" in sys.argv:
        print(json.dumps(data, ensure_ascii=False))
    else:
        print(data["access_token"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
