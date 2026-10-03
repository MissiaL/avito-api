# Official Avito Ads SDKs

Use this guide when integrating **Авито Реклама**. These SDKs cover the advertising cabinet, not Business API listings, Messenger, Autoload or the **Авито Promo** agency API. Check the SDK's operation coverage before selecting it; use direct HTTP for an operation it does not expose.

Verified against official `avito-tech` repositories on **2026-10-03**. Exact revisions are in [sources.md](sources.md). Published runtime minima below come from the SDK documentation, not a recommendation to use an unsupported runtime.

| Language | Official repository | Documented installation | Runtime minimum |
|---|---|---|---|
| Python | [avito-ads-sdk-python3](https://github.com/avito-tech/avito-ads-sdk-python3) | `pip install avito-ads` | Python 3.8 |
| Go | [avito-ads-sdk-go](https://github.com/avito-tech/avito-ads-sdk-go) | `go get github.com/avito-tech/avito-ads-sdk-go/avito` | Go 1.21 |
| TypeScript / JavaScript | [avito-ads-sdk-typescript](https://github.com/avito-tech/avito-ads-sdk-typescript) | `npm install avito-ads` | Node.js 18 with native `fetch` |
| PHP | [avito-ads-sdk-php](https://github.com/avito-tech/avito-ads-sdk-php) | `composer require avito-tech/avito-ads-sdk-php` | PHP 7.4, ext-json, Guzzle 7 |

Choose the SDK matching the existing project. Python offers sync and async clients; Go uses the standard library; TypeScript uses native `fetch`; PHP uses Guzzle. Verify and pin the selected package version using the project's dependency workflow. Package installation and live API access were not tested as part of this documentation refresh.

## Credentials and environments

An administrator creates keys in the **API** tab of the advertising cabinet. Keys belong to one advertising account; child accounts need their own keys. Supply its `account_id` alongside `client_id` and `client_secret`. Treat the advertising account ID separately from the Business API `user_id` returned by `/core/v1/accounts/self`.

| Purpose | URL |
|---|---|
| Production Ads base | `https://api.avito.ru/ads/` |
| Sandbox Ads base | `https://api.avito.ru/ads-sandbox/` |
| OAuth token, both environments | `https://api.avito.ru/token` |

The SDK adds its operation paths beneath the selected base. For direct HTTP, use the complete documented path; avoid duplicating `/ads/`. The bundled `get_token.py` can obtain an Ads token from Ads credentials because the token endpoint and grant match, but it neither selects a sandbox nor caches tokens between invocations. SDK clients handle token caching themselves.

## Read-only Python example

Configure `AVITO_ADS_CLIENT_ID`, `AVITO_ADS_CLIENT_SECRET` and `AVITO_ADS_ACCOUNT_ID` locally. These names keep Ads credentials separate from Business API credentials.

```python
import os
from avito_ads import Client, Configuration

config = Configuration.create(
    os.environ["AVITO_ADS_CLIENT_ID"],
    os.environ["AVITO_ADS_CLIENT_SECRET"],
    int(os.environ["AVITO_ADS_ACCOUNT_ID"]),
).production()

with Client(config) as client:
    balance = client.account.get_balance()
    print(balance.balance)
```

Use `.sandbox()` for the sandbox. The async equivalent uses `AsyncClient`, `async with`, and `await client.account.get_balance()`.

## Retries and partial results

SDKs advertise automatic retries on `429`/`5xx` and token refresh on `401`. In the verified **Python** implementation, network errors are also retried, and retry decisions do not distinguish reads from writes. Thus a money transfer or creation request can be sent again after an ambiguous failure.

For a write without documented idempotency, create the Python configuration with `.with_max_retries(0)` and verify the resulting state before manually retrying. This disables its `429`/`5xx`/network retry loop; the separate one-time retry after `401` remains. For other languages, inspect the selected SDK's retry implementation before enabling write retries. See the pinned [Python sync transport](https://github.com/avito-tech/avito-ads-sdk-python3/blob/41a3c72cf4c18ed76e43925f6a7e5e6ae9238267/avito_ads/_sync/transport.py) and [response retry policy](https://github.com/avito-tech/avito-ads-sdk-python3/blob/41a3c72cf4c18ed76e43925f6a7e5e6ae9238267/avito_ads/_core/transport.py).

For rate-limited reads, use bounded retries and the server's `Retry-After`; `Api-Point-Balance` exposes the remaining API point balance. Do not apply an Ads-wide default limit to other Avito products.

The bundled [Ads guide](sections/ads.md) documents `207 Multi-Status` for sandbox account creation when preparation of test data is incomplete. Inspect its `warnings` and the created account before retrying creation. Do not interpret every `2xx` as completion of every requested sub-operation.
