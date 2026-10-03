# Источники и актуальность

Проверка и выгрузка выполнены **03.10.2026**.

## Снимок каталога

- Источник: [официальный каталог Avito](https://www.avito.ru/developers/api-catalog). Портал переехал с `developers.avito.ru` (301-редирект); выгрузка — `GET https://www.avito.ru/web/1/openapi/list` и `GET https://www.avito.ru/web/1/openapi/info/<slug>` (JSON: `swagger` — OpenAPI строкой, `md` — руководство, `changelog` — история изменений).
- Все 27 разделов вернули HTTP 200 и валидный OpenAPI 3.0. Покрытие: **248 путей, 256 операций, 27 разделов**, 26 руководств; у `realty-reports` руководства в каталоге нет.
- Относительно снимка 16.07.2026: новые разделы `digital-goods` (Цифровые товары, 9 операций) и `tariff-composition` (Тариф, 1), новый `POST /promotion/v2/items/services/get`; `POST /promotion/v1/items/services/get` помечен deprecated. Удалённых операций нет.
- Сборка: `scripts/build_spec.py`. Правила мержа описаны в его docstring и в `info.description` спека: разделы с нестандартным хостом применяются первыми, поэтому `/token` канонический у `auth`; одноимённые компоненты с разным содержимым переименованы в `<name>__<slug>`; операции Автотеки получили `servers: https://pro.autoteka.ru`.
- Повторная сборка 03.10.2026 использовала сохранённую исходную выгрузку того же дня, которая точно воспроизводила предыдущий снимок. Исправлено слияние OAuth: `ClientCredentials` использует `https://api.avito.ru/token`, отдельная `ClientCredentials__autoteka` — `https://pro.autoteka.ru/token`. В 7 операциях `autostrategy` исправлена опечатка источника `Client Credentials` → объявленная `ClientCredentials`; исходное требование сохранено в `x-avito-original-security`.
- Повторную загрузку каталога выполнить не удалось: прямой запрос вернул HTTP 429, доступ через браузер заблокирован его политикой безопасности. Дата схемы относится к исходной выгрузке, а не к новой успешной загрузке.
- Схема получена с публичного портала, реальные вызовы API этой проверкой не выполнялись.

## Официальные SDK Авито Реклама

В GitHub API проверены текущие HEAD ветки `main`; README прочитаны по закреплённым ревизиям. Репозитории Python и Go не архивированы, последняя активность push — 08.06.2026. Проверка исходников не подтверждает работоспособность запросов с конкретным аккаунтом.

| Репозиторий | Проверенная ревизия и README |
|---|---|
| Python | [41a3c72cf4c18ed76e43925f6a7e5e6ae9238267](https://github.com/avito-tech/avito-ads-sdk-python3/blob/41a3c72cf4c18ed76e43925f6a7e5e6ae9238267/README.md) |
| Go | [7bc779aa973944aa119a85ebc303ea36b91a7145](https://github.com/avito-tech/avito-ads-sdk-go/blob/7bc779aa973944aa119a85ebc303ea36b91a7145/README.md) |
| TypeScript | [e2ab83b989783c02cb584dfe15799be98b3d5791](https://github.com/avito-tech/avito-ads-sdk-typescript/blob/e2ab83b989783c02cb584dfe15799be98b3d5791/README.md) |
| PHP | [6423fb50e74190c0a47a00bf649b5b6925727dcb](https://github.com/avito-tech/avito-ads-sdk-php/blob/6423fb50e74190c0a47a00bf649b5b6925727dcb/README.md) |

Практические указания: [ads-sdk.md](ads-sdk.md). SDK не заменяют полный каталог Business API и не служат источником схем для Messenger, Promo или Автозагрузки.

## Следующее обновление

1. Антибот отвечает HTTP 429 на curl и headless-браузер. Выгружай из обычного браузера с пройденной проверкой: открой каталог и выполни в консоли

   ```js
   const l = await (await fetch('/web/1/openapi/list')).json(), dump = {list: l, info: {}};
   for (const {slug} of l) { const r = await fetch('/web/1/openapi/info/' + slug); dump.info[slug] = {status: r.status, text: await r.text()}; await new Promise(r => setTimeout(r, 300)); }
   Object.assign(document.createElement('a'), {href: URL.createObjectURL(new Blob([JSON.stringify(dump)])), download: 'dump.json'}).click();
   ```

2. `python3 scripts/build_spec.py dump.json` пересоберёт `avito-api-openapi.json`, `index.md` и `sections/*.md`. Скрипт падает, если раздел вернул не 200 или не OpenAPI 3. Старый спек сравни с новым по операциям (`path + method`): добавленные, удалённые, новые `deprecated`.
3. Обнови числа, даты и указания по миграциям в `SKILL.md`, `README.md` и здесь. При неудаче выгрузки сохрани снимок и укажи причину; дату попытки не выдавай за дату свежей схемы.
4. Запусти `python3 -m unittest discover -s scripts -p 'test_*.py'` и несколько `search`/`show` для затронутых разделов. Проверь, что все локальные `$ref` и имена в `security` разрешаются, а адреса OAuth соответствуют продукту.
