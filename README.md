# avito-api

Agent Skill в формате [agentskills.io](https://agentskills.io) для работы с [Avito Business API](https://developers.avito.ru/api-catalog) — управление объявлениями, чатами Messenger, Авито.Доставка, Авито.Работа, Автозагрузка, Автотека, Авито Promo, статистика, тарифы, CPA, продвижение, Авито Реклама и остальные разделы официального каталога.

В коробке: полный официальный OpenAPI 3.0 спек (238 путей / 245 операций / 25 разделов), родная per-section документация Avito, OAuth2-хелпер для токена, и CLI для поиска по спеку без необходимости тащить ~2.0 МБ JSON в контекст.

## Структура

```
avito-api/
├── SKILL.md                        инструкции для агента
├── scripts/
│   ├── get_token.py                OAuth2 Client Credentials → access_token
│   └── lookup_endpoint.py          tags / search / show по OpenAPI
└── references/
    ├── avito-api-openapi.json      полный мерженый спек
    ├── index.md                    плоский per-section индекс эндпоинтов
    └── sections/<slug>.md          официальные интеграционные доки Avito
```

## Установка

Скопируй папку `avito-api/` в каталог скиллов своего агента. Для Claude Code:

```bash
cp -r avito-api ~/.claude/skills/avito-api
```

Для других совместимых клиентов (Cursor, Goose, Copilot, OpenCode, OpenHands, Letta, и др. — [полный список](https://agentskills.io/clients)) — см. их инструкцию по подключению Agent Skills, обычно тоже папка с `SKILL.md`.

## Использование

После установки скилл триггерится сам, когда агент видит запросы вида «Avito API», «авито апи», «объявления на авито», «чаты авито», «Автозагрузка», «Автотека» и т.д. От пользователя нужны только credentials.

### Получить credentials

В личном кабинете Avito продавца: **Настройки → Avito API → Регистрация нового приложения**. Получишь `client_id` и `client_secret`. Передавай агенту через переменные окружения:

```bash
export AVITO_CLIENT_ID=...
export AVITO_CLIENT_SECRET=...
```

### Что агент сделает дальше

1. Прочитает [SKILL.md](SKILL.md), узнает про auth, base URL и навигацию.
2. Через `lookup_endpoint.py search/show` найдёт нужный эндпоинт и его схему — без чтения ~2.0 МБ JSON.
3. На сложных интеграциях откроет `references/sections/<slug>.md` (например, `delivery-sandbox.md` — 200 КБ родного гайда от Avito).
4. Запросит токен через `get_token.py`, дёрнет API, вернёт результат.

## Источник и атрибуция

OpenAPI-спек и per-section markdown в `references/` собраны напрямую из официального каталога **`developers.avito.ru/api-catalog`** (через внутренний API `GET /web/1/openapi/list` и `GET /web/1/openapi/info/<slug>`, которые отдаёт сам дев-портал без авторизации). Содержимое — собственность ООО «КЕХ еКоммерц», воспроизводится здесь в технических целях для интероперабельности агентских клиентов с Avito Business API.

Условия использования API: <https://www.avito.ru/legal/pro_tools/public-api> ([PDF](https://developers.avito.ru/docs/APITermsOfServiceV1.pdf)). На момент сборки скилла ToS не содержат ограничений на перераспространение технической документации, но Avito могут изменить условия в любой момент — проверь актуальную редакцию перед коммерческим использованием.

## Лицензия

- Код в `scripts/` и `SKILL.md` — **MIT** © 2026 Petr Alexeev.
- Файлы в `references/` (OpenAPI и markdown) — собственность ООО «КЕХ еКоммерц», см. раздел выше.

## Disclaimer

Этот скилл **не аффилирован с Avito** (ООО «КЕХ еКоммерц») и не одобрен ими. Если ты из Avito и хочешь, чтобы что-то было удалено или изменено — напиши <https://t.me/PetrAlexeev>.
