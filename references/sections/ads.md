# Авито Реклама (`ads`)

Публичное API кабинета Авито Реклама

---

# API Авито Реклама

Публичное API кабинета Авито Реклама для управления рекламными аккаунтами, рекламодателями, договорами, кампаниями, группами объявлений, креативами и пользователями.

- **Базовый URL (prod):** `https://api.avito.ru/ads/`
- **Базовый URL (sandbox):** `https://api.avito.ru/ads-sandbox/`
- **Версия:** v1
- **Формат:** JSON
- **Авторизация:** OAuth 2.0 client credentials (Bearer token)

> Нашли ошибку в документации или что-то не хватает в API Авито Реклама? [Пройдите короткий опрос ↗](https://survey.uxfeedback.ru/WUP9kBTpyutd) — мы учитываем все обращения при планировании развития API Авито Реклама.

---

## Быстрый старт

Минимальный путь от нуля до первого запроса.

### 1. Получите ключи доступа

Во вкладке **API** кабинета Авито Реклама создайте `client_id` и `client_secret`. Действие доступно только пользователю с ролью Администратора. Полученные ключи привязаны к конкретному рекламному аккаунту — для дочерних аккаунтов выпускайте отдельные ключи.

### 2. Получите access token

```bash
curl --request POST \
  --url https://api.avito.ru/token \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data grant_type=client_credentials \
  --data client_id=ВАШ_CLIENT_ID \
  --data client_secret=ВАШ_CLIENT_SECRET
```

Ответ:

```json
{
  "access_token": "chGeRx_aRDqcz_fbGvPGSgebH_TMK_pKDOIzFxeR",
  "expires_in": 86400,
  "token_type": "Bearer"
}
```

Подробности — в [документации auth](https://developers.avito.ru/api-catalog/auth/documentation#operation/getAccessToken).

### 3. Проверьте, что токен работает

Запросите свой аккаунт:

```bash
curl --request GET \
  --url https://api.avito.ru/ads/v1/account/123456789 \
  --header 'Authorization: Bearer ВАШ_ТОКЕН'
```

Если в ответ пришли реквизиты ЮЛ — всё готово. Если `401` — токен просрочен или невалиден. Если `403` — токен выпущен для другого `accountID`.

### 4. Получите данные кампаний и статистику

Список кампаний (с пагинацией):

```bash
curl --request POST \
  --url https://api.avito.ru/ads/v1/account/123456789/campaigns \
  --header 'Authorization: Bearer ВАШ_ТОКЕН' \
  --header 'Content-Type: application/json' \
  --data '{"filter":{}, "limit":20, "page":1}'
```

Статистика по конкретной кампании за период (до 100 дней):

```bash
curl --request POST \
  --url https://api.avito.ru/ads/v1/account/123456789/campaigns/987654321/stats \
  --header 'Authorization: Bearer ВАШ_ТОКЕН' \
  --header 'Content-Type: application/json' \
  --data '{"dateFrom":"2025-01-01", "dateTo":"2025-01-31"}'
```

---

## Концепции и иерархия сущностей

Сущности API связаны иерархически:

```
Аккаунт (Account)
├── Рекламодатели (Advertiser)   ← ЮЛ, от лица которого размещается реклама
│   └── Договоры (Contract)      ← нужен, если рекламодатель ≠ аккаунт
├── Дочерние аккаунты (Child)    ← отдельные аккаунты на одном договоре с родителем
└── Кампании (Campaign)
    └── Группы (Group)           ← бюджет, ставка, таргетинг, расписание
        └── Креативы (Creative)  ← конкретные объявления
```

| Сущность | Что это |
|---|---|
| **Аккаунт** | Рекламный кабинет конкретного ЮЛ/ИП. Токен API всегда привязан к одному аккаунту. [Подробнее ↗](https://ads-help.avito.com/account) |
| **Рекламодатель** | Юридическое лицо (или ИП), от лица которого размещается реклама. У одного аккаунта может быть несколько рекламодателей. [Подробнее ↗](https://ads-help.avito.com/ads/advertiser) |
| **Договор** | Изначальный договор между аккаунтом и рекламодателем. Нужен, только если рекламодатель и аккаунт — **разные** ЮЛ/ИП. [Подробнее ↗](https://ads-help.avito.com/ord/contract) |
| **Дочерний аккаунт** | Отдельный аккаунт на одном договоре с родителем. У него собственный токен и баланс; деньги/бонусы переводятся с родителя. [Подробнее ↗](https://ads-help.avito.com/account/subaccount) |
| **Кампания** | Набор рекламных настроек с общей идеей и целью, моделью оплаты (`CPM`/`CPC`) и типом (`textImage`/`HTML`/`video`). [Подробнее ↗](https://ads-help.avito.com/ads) |
| **Группа** | Внутри кампании; задаёт бюджет, ставку, расписание и таргетинг. [Подробнее ↗](https://ads-help.avito.com/group) |
| **Креатив** | Конкретное объявление (баннер/видео/HTML) внутри группы. [Подробнее ↗](https://ads-help.avito.com/creative) |

> Через текущую версию API создавать кампании, группы и креативы пока нельзя — это делается в веб-интерфейсе.

---

## Авторизация

Все запросы к API требуют заголовка `Authorization: Bearer <access_token>`.

**Свойства токена:**
- Получается по client credentials (см. [Быстрый старт](#info/bystryy_start)).
- `expires_in` — срок жизни в секундах (по умолчанию сутки). Обновляйте заранее.
- Доступ ограничен **тем аккаунтом**, в котором были выпущены ключи. Для доступа к дочернему аккаунту выпускайте отдельные ключи в этом дочернем аккаунте.

**Получение ключей:** вкладка **API** кабинета Авито Реклама, доступна пользователю с ролью **Администратор**.

---

## Песочница

Песочница позволяет тестировать запросы без влияния на реальные данные. Достаточно заменить префикс `https://api.avito.ru/ads/` на `https://api.avito.ru/ads-sandbox/` и использовать тестовый аккаунт.

### Шаг 1. Создайте тестовый аккаунт

В песочнице доступен метод `POST /ads/v1/account/{accountID}` (в проде он недоступен — для боевого создания используется веб-интерфейс):

```bash
curl --request POST \
  --url https://api.avito.ru/ads-sandbox/v1/account/811469958 \
  --header 'Authorization: Bearer ВАШ_ТОКЕН' \
  --header 'Content-Type: application/json' \
  --data '{
    "inn": "123456789012",
    "shortName": "shortName",
    "longName": "longName",
    "ogrn": "123456789012345",
    "legalAddress": "legalAddress",
    "actualAddress": "actualAddress",
    "legalType": "ip",
    "contact": {
      "name": "name",
      "phone": "+78005553535"
    }
  }'
```

Ответ:

```json
{ "accountID": 998186750 }
```

Сохраните `accountID` — это ID тестового аккаунта.

### Шаг 2. Используйте sandbox-префикс в запросах

```bash
curl --request GET \
  --url https://api.avito.ru/ads-sandbox/v1/account/998186750 \
  --header 'Authorization: Bearer ВАШ_ТОКЕН'
```

### Ограничения песочницы

- Время жизни тестового аккаунта — до **00:00 текущего дня**.
- За сутки можно создать **не более 1** тестового аккаунта.
- Можно создать дочерний аккаунт и переводить на него деньги, но **пользоваться им не получится**: токен для дочерних аккаунтов, созданных в песочнице, использовать нельзя. Проверить факт создания можно через `GET /ads/v1/account/{accountID}/children`.

---

## Общие соглашения

### Пагинация и фильтры

Все list-методы (рекламодатели, договоры, кампании, группы, креативы) используют единый формат запроса:

```json
{
  "filter": { /* специфичные для сущности фильтры */ },
  "limit": 20,
  "page": 1
}
```

| Поле | Тип | Ограничения | По умолчанию |
|------|-----|-------------|--------------|
| `filter` | object | Обязательное; может быть `{}` — тогда фильтрация не применяется | — |
| `limit` | integer | 1–100 | 20 |
| `page` | integer | ≥ 1 | 1 |

В ответе всегда есть `total` (общее количество записей по фильтру) и массив сущностей. Для перебора всех страниц увеличивайте `page` до тех пор, пока возвращаемый массив не опустеет (или пока `page * limit ≥ total`).

### Деньги и бонусы

- Все денежные значения — **целые числа в рублях с НДС**.
- Минимальная сумма перевода — **1 рубль/бонус**.
- Поля `balance`, `bonusBalance`, `spend`, `spendBonus`, `budget`, `price`, `amount` — всегда целые.

### Даты и периоды

- Формат даты — `YYYY-MM-DD` (например, `2025-01-31`).
- Временные метки в статистике (`timestamp`) — ISO 8601 с дневной гранулярностью (`2025-01-01T00:00:00Z`).
- **Максимальный период между `dateFrom` и `dateTo` в статистике — 100 дней.**

### Заголовки ответа

| Заголовок | Описание |
|---|---|
| `Api-Point-Balance` | Остаток API-баллов после выполнения запроса. У каждого метода своя стоимость в баллах (см. `x-cost` в OpenAPI). |

### Ошибки

Все ошибки возвращаются с JSON-телом одинаковой схемы:

```json
{
  "code": "string",
  "message": "string"
}
```

| HTTP | Когда возникает |
|------|-----------------|
| `400` | Невалидное тело запроса: `amount < 1`, пустые обязательные поля, неверный формат дат, период статистики > 100 дней. |
| `401` | Access token отсутствует, просрочен или невалиден. |
| `403` | Токен не имеет прав на `accountID` в path. |
| `404` | Аккаунт/сущность не найдены в контексте доступов текущего токена. |
| `429` | Превышен лимит запросов. Используйте retry с экспоненциальным backoff. |
| `500` | Внутренняя ошибка сервера. |
| `503` | Сервис временно недоступен. |

---

## Справочник методов

### Аккаунты и балансы

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/ads/v1/account/{accountID}` | Получить аккаунт по ID |
| GET | `/ads/v1/account/{accountID}/balance` | Получить баланс аккаунта по ID |
| POST | `/ads/v1/account/{accountID}` | **Только sandbox.** Создать тестовый аккаунт |

Подробнее об аккаунте — в [справке по аккаунтам ↗](https://ads-help.avito.com/account).

#### GET — получить аккаунт

```bash
curl --request GET \
  --url https://api.avito.ru/ads/v1/account/123456789 \
  --header 'Authorization: Bearer ВАШ_ТОКЕН'
```

Ответ:

```json
{
  "account": {
    "inn": "7712345678",
    "shortName": "ООО Пример",
    "longName": "Общество с ограниченной ответственностью Пример",
    "ogrn": "1177746000000",
    "kpp": "771701001",
    "legalAddress": "г. Москва, ул. Примерная, д. 1",
    "actualAddress": "г. Москва, ул. Примерная, д. 1",
    "contact": { "name": "Иван Иванов", "phone": "+78005553535" },
    "manager": { "name": "Менеджер", "email": "manager@example.com" }
  }
}
```

Поля объекта `account`:

| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| `inn` | string | да | ИНН организации/ИП |
| `shortName` | string | да | Краткое название |
| `longName` | string | да | Полное наименование |
| `ogrn` | string | да | ОГРН или ОГРНИП |
| `kpp` | string | да | КПП организации (для ИП пусто) |
| `legalAddress` | string | да | Юридический адрес |
| `actualAddress` | string | да | Фактический адрес |
| `contact` | object | да | `{ name, phone }` — контактное лицо |
| `manager` | object | нет | `{ name, email }` — закреплённый менеджер MSD |

#### GET — получить баланс

```bash
curl --request GET \
  --url https://api.avito.ru/ads/v1/account/123456789/balance \
  --header 'Authorization: Bearer ВАШ_ТОКЕН'
```

Ответ:

```json
{
  "balance": 10000,
  "bonusBalance": 0
}
```

| Поле | Тип | Описание |
|------|-----|----------|
| `balance` | integer | Денежные средства, в рублях |
| `bonusBalance` | integer | Бонусы, в рублях |

### Дочерние аккаунты и переводы

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/ads/v1/account/{accountID}/children` | Список дочерних аккаунтов |
| GET | `/ads/v1/account/{accountID}/children-with-balances` | Список дочерних аккаунтов с балансами |
| POST | `/ads/v1/account/{accountID}/create-nonpayer-child-account` | Создать дочерний аккаунт на договоре родителя |
| POST | `/ads/v1/account/{accountID}/funds-transfer` | Перевести деньги между родителем и дочкой |
| POST | `/ads/v1/account/{accountID}/bonus-transfer` | Перевести бонусы между родителем и дочкой |

Дочерний аккаунт — это отдельный аккаунт на одном договоре с родителем. У него собственный токен и баланс. Подробнее — в [справке по дочерним аккаунтам ↗](https://ads-help.avito.com/account/subaccount).

#### Создание дочернего аккаунта

```bash
curl --request POST \
  --url https://api.avito.ru/ads/v1/account/123456789/create-nonpayer-child-account \
  --header 'Authorization: Bearer ВАШ_ТОКЕН' \
  --header 'Content-Type: application/json' \
  --data '{
    "shortName": "Дочка ООО Пример",
    "isSelfAdvertisingEnabled": false
  }'
```

Ответ:

```json
{
  "accountID": 998186750,
  "clientKey": "abc123...",
  "clientSecret": "def456..."
}
```

| Поле запроса | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| `shortName` | string | да | Краткое название дочернего аккаунта, меньше 64 символов |
| `isSelfAdvertisingEnabled` | boolean | да | Можно ли рекламировать родительский аккаунт. Если рекламируется новый рекламодатель, и реклама родителя не нужна — ставьте `false`. |

> В ответе возвращаются `clientKey` и `clientSecret` — это пара ключей для выпуска отдельного токена дочернего аккаунта. **В песочнице токен по этим ключам использовать нельзя.**

#### Список дочерних аккаунтов

```bash
curl --request GET \
  --url https://api.avito.ru/ads/v1/account/123456789/children \
  --header 'Authorization: Bearer ВАШ_ТОКЕН'
```

> У дочерних аккаунтов на одном договоре с родителем поле `contract` в ответе не передаётся.

#### Список дочерних аккаунтов с балансами

```bash
curl --request GET \
  --url https://api.avito.ru/ads/v1/account/123456789/children-with-balances \
  --header 'Authorization: Bearer ВАШ_ТОКЕН'
```

Ответ:

```json
{
  "children": [
    {
      "account": { "id": 987654321, "shortName": "Дочерний аккаунт" },
      "balance": { "balance": 2500, "bonusBalance": 100 }
    }
  ]
}
```

#### Перевод денег и бонусов

**Логика направления** одинакова для денег (`funds-transfer`) и бонусов (`bonus-transfer`):

- `accountID` в path — аккаунт-**источник** (с него списываются средства).
- `accountIdTo` в теле — аккаунт-**получатель**.
- Перевод выполняется **от имени аккаунта-источника**, поэтому:
  - для перевода с родителя на дочку нужен токен **родителя**;
  - для перевода с дочки на родителя нужен токен **дочернего аккаунта**.
- `accountIdTo` должен указывать на связанный аккаунт (пара родитель/дочка).
- `amount` — целое число ≥ 1.

| Сценарий | Метод | Чей токен |
|---|---|---|
| Родитель → дочка (деньги) | `POST /ads/v1/account/{PARENT}/funds-transfer` | родителя |
| Дочка → родитель (деньги) | `POST /ads/v1/account/{CHILD}/funds-transfer` | дочки |
| Родитель → дочка (бонусы) | `POST /ads/v1/account/{PARENT}/bonus-transfer` | родителя |
| Дочка → родитель (бонусы) | `POST /ads/v1/account/{CHILD}/bonus-transfer` | дочки |

Пример перевода денег:

```bash
curl --request POST \
  --url https://api.avito.ru/ads/v1/account/123456789/funds-transfer \
  --header 'Authorization: Bearer ВАШ_ТОКЕН' \
  --header 'Content-Type: application/json' \
  --data '{
    "accountIdTo": 987654321,
    "amount": 100
  }'
```

Ответ при успехе — пустой объект `{}`.

**End-to-end сценарий:**

1. Родитель → дочка: 100 ₽.

```bash
curl -X POST https://api.avito.ru/ads/v1/account/PARENT_ID/funds-transfer \
  -H 'Authorization: Bearer PARENT_TOKEN' -H 'Content-Type: application/json' \
  -d '{"accountIdTo": CHILD_ID, "amount": 100}'
```

2. Проверка балансов дочерних аккаунтов.

```bash
curl https://api.avito.ru/ads/v1/account/PARENT_ID/children-with-balances \
  -H 'Authorization: Bearer PARENT_TOKEN'
```

3. Дочка → родитель: вернуть 30 ₽ (нужен токен дочки).

```bash
curl -X POST https://api.avito.ru/ads/v1/account/CHILD_ID/funds-transfer \
  -H 'Authorization: Bearer CHILD_TOKEN' -H 'Content-Type: application/json' \
  -d '{"accountIdTo": PARENT_ID, "amount": 30}'
```

### Рекламодатели

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | `/ads/v1/account/{accountID}/create-advertiser` | Создать рекламодателя |
| POST | `/ads/v1/account/{accountID}/advertisers` | Список рекламодателей по фильтрам |

Рекламодатель — это ЮЛ/ИП, от лица которого размещается реклама. У одного аккаунта может быть несколько рекламодателей. Если рекламодатель и аккаунт — одно и то же ЮЛ/ИП, договор между ними создавать **не нужно**. Подробнее — в [справке по рекламодателям ↗](https://ads-help.avito.com/ads/advertiser).

#### Создание рекламодателя

```bash
curl --request POST \
  --url https://api.avito.ru/ads/v1/account/123456789/create-advertiser \
  --header 'Authorization: Bearer ВАШ_ТОКЕН' \
  --header 'Content-Type: application/json' \
  --data '{
    "shortName": "ООО Рекламодатель",
    "longName": "Общество с ограниченной ответственностью Рекламодатель",
    "inn": "7712345678",
    "ogrn": "1177746000000",
    "kpp": "771701001",
    "legalAddress": "г. Москва, ул. Рекламная, д. 1",
    "actualAddress": "г. Москва, ул. Рекламная, д. 1",
    "legalType": "ul",
    "legalRole": "rd"
  }'
```

Ответ:

```json
{ "id": 987654321 }
```

| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| `shortName`, `longName` | string | да | Краткое и полное наименование |
| `inn`, `ogrn` | string | да | ИНН и ОГРН (для ИП — ОГРНИП) |
| `kpp` | string | нет | КПП (для ИП пусто) |
| `legalAddress` | string | да | Юридический адрес |
| `actualAddress` | string | да | Фактический адрес |
| `legalType` | enum | да | `ul` (юр. лицо) / `ip` (ИП) |
| `legalRole` | enum | да | `rd` / `ra` / `rr` — см. [справочник enum'ов](#info/spravochnik_enum-znacheniy) |

> **Правила валидации адресов (`legalAddress`, `actualAddress`)**
>
> Поля адресов проходят обязательную валидацию по требованиям ОРД-А. Запрос с невалидным адресом будет отклонён.
>
> - Длина — от 10 до 500 символов.
> - Допускаются прописные и строчные буквы русского алфавита, арабские цифры, а также символы: `-` (дефис), `.` (точка), `,` (запятая), ` ` (пробел), `’` (апостроф — не более одного между словами, не в начале и не в конце), `(` и `)` (круглые скобки), `N` и `№` (знак номера), `/` (косая черта), символы римских чисел `I`, `V`, `X`, `L`, `C`, `D`, `M`.
> - Адрес не должен состоять только из разрешённых символов-разделителей (пробел, дефис, точка, апостроф, запятая, скобки, знак номера, символы римских чисел) — в нём должны быть буквы или цифры.
> - В начале и в конце адреса не должно быть пробелов.
>
> Пример валидного адреса: `127015, г. Москва, ул. Лесная, д. 7`

#### Список рекламодателей

```bash
curl --request POST \
  --url https://api.avito.ru/ads/v1/account/123456789/advertisers \
  --header 'Authorization: Bearer ВАШ_ТОКЕН' \
  --header 'Content-Type: application/json' \
  --data '{
    "filter": { "roles": ["rd"] },
    "limit": 20,
    "page": 1
  }'
```

Ответ:

```json
{
  "total": 1,
  "advertisers": [
    {
      "id": 987654321,
      "shortName": "ООО Рекламодатель",
      "longName": "Общество с ограниченной ответственностью Рекламодатель",
      "inn": "7712345678",
      "ogrn": "1177746000000",
      "kpp": "771701001",
      "legalAddress": "г. Москва, ул. Рекламная, д. 1",
      "actualAddress": "г. Москва, ул. Рекламная, д. 1",
      "legalType": "ul",
      "legalRole": "rd",
      "accountId": 123456789
    }
  ]
}
```

Доступные фильтры:

| Поле | Тип | Описание |
|------|-----|----------|
| `ids` | array of int | Список ID рекламодателей |
| `inns` | array of string | Список ИНН |
| `roles` | array of enum | Список ролей (`rd`/`ra`/`rr`) |

### Договоры

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | `/ads/v1/account/{accountID}/create-contract` | Создать изначальный договор |
| POST | `/ads/v1/account/{accountID}/contracts` | Список договоров по фильтрам |

Договор нужен, **только если рекламодатель и аккаунт — не одно и то же ЮЛ/ИП**. Если контрагенты совпадают — договор не создаётся. Подробнее — в [справке по договорам ↗](https://ads-help.avito.com/ord/contract).

#### Типы договоров

| Значение `type` | Описание |
|---|---|
| `service` | Договор на оказание услуг |
| `intermediary` | Посреднический договор |
| `external` | Внешний договор (требует поле `cid`) |

> Дополнительные соглашения создаются **не отдельным типом**, а указанием `parentId` к существующему родительскому договору.

#### Что обязательно по типу

| Тип | Обязательные поля | Что нельзя |
|-----|-------------------|------------|
| `service` | `subject`, `isReportingRequired`, `date`, `number` | `cid` |
| `intermediary` | `subject`, `object`, `isReportingRequired`, `isFundsAllocationToPrincipal`, `date`, `number` | `cid` |
| `external` | `cid` | `parentId` |

> Поля `date` и `number` можно не передавать **только** для `type = external`. Для доп. соглашений (`parentId` задан, `type` остаётся `service`/`intermediary`) они так же обязательны, как и для основного договора.

**Общие проверки** при создании:

- Если указан `advertiserId`, рекламодатель должен существовать.
- Для аккаунта должен существовать актуальный performance-договор с Авито, иначе создание упадёт с ошибкой.
- Поле `intermediary` (данные исполнителя) обязательно, **если не передан `parentId`**; при наличии `parentId` передавать `intermediary` нельзя.
- Родительский договор не может быть дополнительным соглашением.
- Рекламодатель и посредник не должны совпадать по ИНН.
- Аккаунт не может быть посредником, кроме случая `description = "direct_with_advertiser"`.
- Доп. соглашение к performance-договору допустимо только если форма родительского договора — `application`.

#### Создание посреднического договора

```bash
curl --request POST \
  --url https://api.avito.ru/ads/v1/account/123456789/create-contract \
  --header 'Authorization: Bearer ВАШ_ТОКЕН' \
  --header 'Content-Type: application/json' \
  --data '{
    "advertiserId": 987654321,
    "type": "intermediary",
    "subject": "mediation",
    "object": "commercial",
    "description": "direct_with_advertiser",
    "isReportingRequired": true,
    "isFundsAllocationToPrincipal": false,
    "date": "2025-01-15",
    "number": "ДА-2025/01",
    "intermediary": {
      "shortName": "ООО Реклама",
      "longName": "Общество с ограниченной ответственностью Реклама",
      "inn": "7712345678",
      "ogrn": "1177746123456",
      "kpp": "771701001",
      "legalAddress": "г. Москва, ул. Примерная, д. 1",
      "actualAddress": "г. Москва, ул. Примерная, д. 1",
      "legalType": "ul"
    }
  }'
```

Ответ:

```json
{ "id": 1122334455 }
```

#### Создание дополнительного соглашения

К существующему договору — через `parentId`. Поле `intermediary` передавать **нельзя**; `date` и `number` остаются обязательными (как и для любого договора с `type ≠ external`).

```bash
curl --request POST \
  --url https://api.avito.ru/ads/v1/account/123456789/create-contract \
  --header 'Authorization: Bearer ВАШ_ТОКЕН' \
  --header 'Content-Type: application/json' \
  --data '{
    "advertiserId": 987654321,
    "type": "intermediary",
    "subject": "distribution",
    "object": "distribution",
    "description": "direct_with_advertiser",
    "isReportingRequired": true,
    "isFundsAllocationToPrincipal": true,
    "date": "2025-03-01",
    "number": "ДС-2025/03",
    "parentId": 1122334455
  }'
```

#### Создание внешнего договора

Для `type: external` укажите `cid`, не передавайте `parentId`:

```bash
curl --request POST \
  --url https://api.avito.ru/ads/v1/account/123456789/create-contract \
  --header 'Authorization: Bearer ВАШ_ТОКЕН' \
  --header 'Content-Type: application/json' \
  --data '{
    "advertiserId": 987654321,
    "type": "external",
    "cid": "EXT-2024-001234",
    "subject": "representation",
    "object": "other",
    "description": "advertiser_intermediary",
    "isReportingRequired": false,
    "isFundsAllocationToPrincipal": false
  }'
```

#### Список договоров

```bash
curl --request POST \
  --url https://api.avito.ru/ads/v1/account/123456789/contracts \
  --header 'Authorization: Bearer ВАШ_ТОКЕН' \
  --header 'Content-Type: application/json' \
  --data '{"filter":{}, "limit":20, "page":1}'
```

Доступные фильтры:

| Поле | Тип | Описание |
|------|-----|----------|
| `ids` | array of int | ID договоров |
| `numbers` | array of string | Номера договоров |
| `contractors` | object (AdvertiserFilter) | Фильтр по исполнителям договора |
| `clients` | object (AdvertiserFilter) | Фильтр по заказчикам договора |

### Кампании

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | `/ads/v1/account/{accountID}/campaigns` | Список кампаний по фильтрам |

Создание кампаний через текущую версию API недоступно — используйте веб-интерфейс кабинета. Подробнее — в [справке по кампаниям ↗](https://ads-help.avito.com/ads).

#### Список кампаний

```bash
curl --request POST \
  --url https://api.avito.ru/ads/v1/account/123456789/campaigns \
  --header 'Authorization: Bearer ВАШ_ТОКЕН' \
  --header 'Content-Type: application/json' \
  --data '{
    "filter": {
      "statuses": ["active"],
      "paymentModels": ["CPC"],
      "timeFrame": { "from": "2025-01-01", "to": "2025-12-31" }
    },
    "limit": 20,
    "page": 1
  }'
```

Ответ:

```json
{
  "total": 1,
  "campaigns": [
    {
      "id": 1234567890,
      "name": "Кампания 1",
      "status": "active",
      "budget": 100000,
      "paymentModel": "CPC",
      "campaignType": "textImage",
      "startDate": "2025-01-01",
      "endDate": "2025-12-31",
      "accountId": 123456789,
      "advertiserId": 987654321,
      "contractId": 1122334455,
      "userId": 12345,
      "managerID": 67890,
      "createdAt": "2025-01-01T10:00:00Z",
      "updatedAt": "2025-01-15T12:30:00Z"
    }
  ]
}
```

Доступные фильтры:

| Поле | Тип | Описание |
|------|-----|----------|
| `ids` | array of int | ID кампаний |
| `paymentModels` | array of enum | `CPM`, `CPC` |
| `campaignTypes` | array of enum | `textImage`, `HTML`, `video` |
| `statuses` | array of enum | См. `CampaignStatus` в справочнике |
| `managers` | array of int | ID менеджеров |
| `advertisers` | array of int | ID рекламодателей |
| `contractIDs` | array of int | ID договоров |
| `additionalAgreementIDs` | array of int | ID доп. соглашений |
| `createdAt` | object `{from, to}` | Диапазон дат создания |
| `timeFrame` | object `{from, to}` | Диапазон периода размещения |

### Группы объявлений

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | `/ads/v1/account/{accountID}/groups` | Список групп по фильтрам |
| POST | `/ads/v1/account/{accountID}/group/{groupID}/change-budget` | Изменить бюджет группы |
| POST | `/ads/v1/account/{accountID}/group/{groupID}/change-price` | Изменить цену группы |

Подробнее — в [справке по группам ↗](https://ads-help.avito.com/group).

> **Важно:** методы `change-budget` и `change-price` работают **только для групп с ручным управлением ставкой**. Для групп с автоматическими стратегиями менять бюджет/цену через API нельзя.

#### Список групп

```bash
curl --request POST \
  --url https://api.avito.ru/ads/v1/account/123456789/groups \
  --header 'Authorization: Bearer ВАШ_ТОКЕН' \
  --header 'Content-Type: application/json' \
  --data '{
    "filter": { "campaignIDs": [1234567890] },
    "limit": 20,
    "page": 1
  }'
```

Доступные фильтры:

| Поле | Тип | Описание |
|------|-----|----------|
| `ids` | array of int | ID групп |
| `campaignIDs` | array of int | ID кампаний |
| `statuses` | array of enum | См. `GroupsStatus` в справочнике |
| `paces` | array of enum | Скорости показа |
| `managers` | array of int | ID менеджеров |
| `advertisers` | array of int | ID рекламодателей |
| `paymentModels` | array of enum | `CPM`, `CPC` |
| `timeFrame` | object `{from, to}` | Диапазон периода размещения |

#### Изменение бюджета

```bash
curl --request POST \
  --url https://api.avito.ru/ads/v1/account/123456789/group/987654321/change-budget \
  --header 'Authorization: Bearer ВАШ_ТОКЕН' \
  --header 'Content-Type: application/json' \
  --data '{ "budget": 2500 }'
```

`budget` — целое число ≥ 1, в рублях с НДС.

#### Изменение цены

```bash
curl --request POST \
  --url https://api.avito.ru/ads/v1/account/123456789/group/987654321/change-price \
  --header 'Authorization: Bearer ВАШ_ТОКЕН' \
  --header 'Content-Type: application/json' \
  --data '{ "price": 25 }'
```

`price` — целое число ≥ 1, в рублях с НДС. Семантика (CPC или CPM) определяется моделью оплаты кампании.

### Креативы

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | `/ads/v1/account/{accountID}/creatives` | Список креативов по фильтрам |

Подробнее — в [справке по креативам ↗](https://ads-help.avito.com/creative).

```bash
curl --request POST \
  --url https://api.avito.ru/ads/v1/account/123456789/creatives \
  --header 'Authorization: Bearer ВАШ_ТОКЕН' \
  --header 'Content-Type: application/json' \
  --data '{
    "filter": { "groupIDs": [111222333] },
    "limit": 20,
    "page": 1
  }'
```

> В ответе списка креативов поле `creative` **не содержит** отдельных `imageIDs`, `videoID`, `htmlID`, `legalAttachmentsIDs`. Медиафайлы приходят в массиве `media` со `storageID`.

Дополнительные поля в ответе списка креативов:

| Поле | Тип | Описание |
|------|-----|----------|
| `originUrl` | string | Оригинальная ссылка для аналитики |
| `previewUrl` | string | Ссылка на предпросмотр креатива |
| `landingID` | integer | ID посадочной страницы |

Доступные фильтры:

| Поле | Тип | Описание |
|------|-----|----------|
| `ids` | array of int | ID креативов |
| `groupIDs` | array of int | ID групп |
| `campaignIDs` | array of int | ID кампаний |
| `paymentModels` | array of enum | `CPM`, `CPC` |
| `campaignTypes` | array of enum | `textImage`, `HTML`, `video` |
| `statuses` | array of enum | См. `CreativesStatus` в справочнике |
| `managers` | array of int | ID менеджеров |
| `advertisers` | array of int | ID рекламодателей |
| `timeFrame` | object `{from, to}` | Диапазон периода размещения |

### Статистика

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | `/ads/v1/account/{accountID}/campaigns/{campaignID}/stats` | Статистика по кампании |
| POST | `/ads/v1/account/{accountID}/campaigns/{campaignID}/groups/stats` | Статистика по группам кампании |
| POST | `/ads/v1/account/{accountID}/campaigns/{campaignID}/creatives/stats` | Статистика по креативам кампании |

Общее для всех трёх методов:

- `dateFrom` и `dateTo` — формат `YYYY-MM-DD`.
- **Максимальный период — 100 дней.**
- Гранулярность данных в `data[]` — по дням; в `totalData` — агрегат за весь период.

Набор полей статистики (`StatsData`) одинаковый везде:

| Поле | Тип | Описание |
|------|-----|----------|
| `timestamp` | string (date-time) | Временная метка (по дням) |
| `views` | integer | Количество показов |
| `clicks` | integer | Количество кликов |
| `ctr` | number | CTR (Click-Through Rate) |
| `spend` | integer | Потрачено денег, в рублях |
| `spendBonus` | integer | Потрачено бонусов, в рублях |
| `cpm` | number | Средняя стоимость CPM |
| `cpc` | number | Средняя стоимость CPC |
| `videoViews25` | integer | Просмотров видео на 25% (для видео-кампаний) |
| `videoViews50` | integer | Просмотров видео на 50% (для видео-кампаний) |
| `videoViews75` | integer | Просмотров видео на 75% (для видео-кампаний) |
| `videoViews100` | integer | Просмотров видео на 100% (для видео-кампаний) |
| `q25` | number | Доля просмотров на 25% (для видео-кампаний) |
| `q50` | number | Доля просмотров на 50% (для видео-кампаний) |
| `q75` | number | Доля просмотров на 75% (для видео-кампаний) |
| `vtr` | number | View-Through Rate, доля просмотров на 100% (для видео-кампаний) |

#### Статистика по кампании

```bash
curl --request POST \
  --url https://api.avito.ru/ads/v1/account/123456789/campaigns/987654321/stats \
  --header 'Authorization: Bearer ВАШ_ТОКЕН' \
  --header 'Content-Type: application/json' \
  --data '{
    "dateFrom": "2025-01-01",
    "dateTo": "2025-01-31"
  }'
```

Ответ содержит подробную статистику кампании плюс агрегаты по её группам и креативам:

```json
{
  "campaign": {
    "id": 987654321,
    "name": "Кампания 1",
    "paymentModel": "CPM",
    "campaignType": "textImage",
    "data": [
      {
        "timestamp": "2025-01-01T00:00:00Z",
        "views": 1000, "clicks": 50, "ctr": 5.0,
        "spend": 1500, "spendBonus": 0,
        "cpm": 150.0, "cpc": 3000.0
      }
    ],
    "totalData": {
      "views": 1000, "clicks": 50, "ctr": 5.0,
      "spend": 1500, "spendBonus": 0,
      "cpm": 150.0, "cpc": 3000.0
    }
  },
  "groups": [
    {
      "id": 111222333, "name": "Группа 1",
      "data": [],
      "totalData": { "views": 1000, "clicks": 50, "ctr": 5.0, "spend": 1500, "spendBonus": 0, "cpm": 150.0, "cpc": 3000.0 }
    }
  ],
  "creatives": [
    {
      "id": 444555666, "groupId": 111222333, "name": "Креатив 1",
      "data": [],
      "totalData": { "views": 1000, "clicks": 50, "ctr": 5.0, "spend": 1500, "spendBonus": 0, "cpm": 150.0, "cpc": 3000.0 }
    }
  ]
}
```

#### Статистика по группам кампании

В отличие от метода выше, фильтруется по конкретным `groupIDs`:

```bash
curl --request POST \
  --url https://api.avito.ru/ads/v1/account/123456789/campaigns/987654321/groups/stats \
  --header 'Authorization: Bearer ВАШ_ТОКЕН' \
  --header 'Content-Type: application/json' \
  --data '{
    "dateFrom": "2025-01-01",
    "dateTo": "2025-01-31",
    "groupIDs": [111222333, 111222334]
  }'
```

Ответ:

```json
{
  "groups": [
    {
      "id": 111222333,
      "name": "Группа 1",
      "data": [
        { "timestamp": "2025-01-01T00:00:00Z", "views": 1000, "clicks": 50, "ctr": 5.0, "spend": 1500, "spendBonus": 0, "cpm": 150.0, "cpc": 3000.0 }
      ],
      "totalData": { "views": 1000, "clicks": 50, "ctr": 5.0, "spend": 1500, "spendBonus": 0, "cpm": 150.0, "cpc": 3000.0 }
    }
  ]
}
```

| Поле запроса | Тип | Обязательное |
|------|-----|--------------|
| `dateFrom`, `dateTo` | string (date) | да |
| `groupIDs` | array of int | да, минимум 1 элемент |

#### Статистика по креативам кампании

То же самое, но по `creativeIDs`:

```bash
curl --request POST \
  --url https://api.avito.ru/ads/v1/account/123456789/campaigns/987654321/creatives/stats \
  --header 'Authorization: Bearer ВАШ_ТОКЕН' \
  --header 'Content-Type: application/json' \
  --data '{
    "dateFrom": "2025-01-01",
    "dateTo": "2025-01-31",
    "creativeIDs": [444555666, 444555667]
  }'
```

### Пользователи

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/ads/v1/account/{accountID}/users` | Список пользователей аккаунта |
| POST | `/ads/v1/account/{accountID}/add-user` | Добавить пользователя |
| POST | `/ads/v1/account/{accountID}/set-user-role` | Изменить роль пользователя |
| DELETE | `/ads/v1/account/{accountID}/delete-user/{userID}` | Удалить пользователя |

#### Список пользователей

```bash
curl --request GET \
  --url https://api.avito.ru/ads/v1/account/123456789/users \
  --header 'Authorization: Bearer ВАШ_ТОКЕН'
```

Ответ:

```json
{
  "total": 2,
  "users": [
    { "id": 123456, "role": "admin", "hasLoggedIn": true },
    { "id": 654321, "role": "viewer", "hasLoggedIn": false }
  ]
}
```

#### Добавление пользователя

```bash
curl --request POST \
  --url https://api.avito.ru/ads/v1/account/123456789/add-user \
  --header 'Authorization: Bearer ВАШ_ТОКЕН' \
  --header 'Content-Type: application/json' \
  --data '{ "userId": 123456, "role": "admin" }'
```

| Роль | Описание |
|------|----------|
| `admin` | Полный доступ ко всем функциям |
| `viewer` | Только просмотр |

#### Изменение роли пользователя

```bash
curl --request POST \
  --url https://api.avito.ru/ads/v1/account/123456789/set-user-role \
  --header 'Authorization: Bearer ВАШ_ТОКЕН' \
  --header 'Content-Type: application/json' \
  --data '{ "userId": 123456, "role": "viewer" }'
```

#### Удаление пользователя

```bash
curl --request DELETE \
  --url https://api.avito.ru/ads/v1/account/123456789/delete-user/123456 \
  --header 'Authorization: Bearer ВАШ_ТОКЕН'
```

---

## Справочник enum-значений

Сводка значений всех enum-полей, встречающихся в API.

**`LegalType`** — тип юр. лица:

| Значение | Описание |
|---|---|
| `ul` | Юридическое лицо |
| `ip` | Индивидуальный предприниматель |

**`LegalRole`** — роль ЮЛ:

| Значение | Описание |
|---|---|
| `rd` | Рекламодатель |
| `ra` | Рекламное агентство |
| `rr` | Рекламораспространитель |

**`UserRole`** — роль пользователя:

| Значение | Описание |
|---|---|
| `admin` | Полный доступ |
| `viewer` | Только просмотр |

**`ContractType`** — тип договора:

| Значение | Описание |
|---|---|
| `service` | Договор на оказание услуг |
| `intermediary` | Посреднический договор |
| `external` | Внешний договор (требует `cid`) |

**`ContractSubject`** — предмет договора:

| Значение | Описание |
|---|---|
| `org-distribution` | Распространение от организации |
| `mediation` | Посредничество |
| `distribution` | Распространение |
| `representation` | Представительство |
| `other` | Иное |

**`ContractAction`** — действие договора (`object`):

| Значение | Описание |
|---|---|
| `distribution` | Распространение |
| `conclude` | Заключение |
| `commercial` | Коммерческое |
| `other` | Иное |

**`ContractCounterpartyType`** — описание сторон (`description`):

| Значение | Описание |
|---|---|
| `direct_with_advertiser` | Прямой договор с рекламодателем |
| `advertiser_intermediary` | Через посредника |

**`CampaignPaymentModel`** — модель оплаты:

| Значение | Описание |
|---|---|
| `CPM` | За показы |
| `CPC` | За клики |

**`CampaignType`** — тип кампании:

| Значение | Описание |
|---|---|
| `textImage` | Текстово-графические объявления |
| `HTML` | HTML-баннеры |
| `video` | Видеообъявления |

**`CampaignStatus`** — статус кампании:

| Значение | Описание |
|---|---|
| `draft` | Черновик |
| `in_moderation` | На модерации |
| `moderation_failed` | Модерация не пройдена |
| `partial_moderation` | Частичная модерация |
| `active` | Активна |
| `pausing` | Приостанавливается |
| `paused` | Приостановлена |
| `unpausing` | Возобновляется |
| `stopped` | Остановлена |
| `finished` | Завершена |
| `archived` | В архиве |

**`GroupsStatus`** — статус группы:

| Значение | Описание |
|---|---|
| `draft` | Черновик |
| `in_moderation` | На модерации |
| `moderation_failed` | Модерация не пройдена |
| `will_launch_soon` | Запустится скоро |
| `active` | Активна |
| `will_stop_soon` | Остановится скоро |
| `pausing` | Приостанавливается |
| `paused` | Приостановлена |
| `unpausing` | Возобновляется |
| `stopped` | Остановлена |
| `finished` | Завершена |
| `archived` | В архиве |

**`CreativesStatus`** — статус креатива:

| Значение | Описание |
|---|---|
| `draft` | Черновик |
| `ready_for_moderation` | Готов к модерации |
| `in_moderation` | На модерации |
| `moderation_failed` | Модерация не пройдена |
| `erir_registration` | Регистрация в ЕРИР |
| `active` | Активен |
| `pausing` | Приостанавливается |
| `paused` | Приостановлен |
| `unpausing` | Возобновляется |
| `stopped` | Остановлен |
| `finished` | Завершён |
| `archived` | В архиве |

---

## Ограничения

| Параметр | Значение |
|---|---|
| Rate limit | **500 запросов в минуту** по умолчанию |
| Стоимость метода в API-баллах | Указана в OpenAPI (`x-cost`), см. таблицу ниже |
| Остаток баллов | Возвращается в заголовке `Api-Point-Balance` |
| Период статистики | До **100 дней** между `dateFrom` и `dateTo` |
| Пагинация | `limit` — 1–100 (по умолчанию 20), `page` — от 1 |
| Минимальная сумма перевода | **1 рубль/бонус** |
| Создание тестового аккаунта в sandbox | **1 в сутки**, живёт до 00:00 текущего дня |

При получении `429` повторяйте запрос с экспоненциальным backoff (например: 1 → 2 → 4 → 8 секунд).

### Стоимость методов в API-баллах

| Метод | Стоимость |
|-------|----------:|
| `GET /ads/v1/account/{accountID}` | 1 |
| `POST /ads/v1/account/{accountID}` (sandbox) | 0 |
| `GET /ads/v1/account/{accountID}/balance` | 1 |
| `POST /ads/v1/account/{accountID}/create-nonpayer-child-account` | 1 |
| `POST /ads/v1/account/{accountID}/funds-transfer` | 1 |
| `POST /ads/v1/account/{accountID}/bonus-transfer` | 1 |
| `POST /ads/v1/account/{accountID}/create-advertiser` | 2 |
| `POST /ads/v1/account/{accountID}/advertisers` | 1 |
| `GET /ads/v1/account/{accountID}/children` | 1 |
| `GET /ads/v1/account/{accountID}/children-with-balances` | 5 |
| `POST /ads/v1/account/{accountID}/contracts` | 1 |
| `POST /ads/v1/account/{accountID}/create-contract` | 2 |
| `POST /ads/v1/account/{accountID}/campaigns` | 1 |
| `POST /ads/v1/account/{accountID}/campaigns/{campaignID}/stats` | 10 |
| `POST /ads/v1/account/{accountID}/campaigns/{campaignID}/groups/stats` | 5 |
| `POST /ads/v1/account/{accountID}/campaigns/{campaignID}/creatives/stats` | 1 |
| `POST /ads/v1/account/{accountID}/groups` | 1 |
| `POST /ads/v1/account/{accountID}/group/{groupID}/change-budget` | 3 |
| `POST /ads/v1/account/{accountID}/group/{groupID}/change-price` | 3 |
| `POST /ads/v1/account/{accountID}/creatives` | 1 |
| `POST /ads/v1/account/{accountID}/add-user` | 5 |
| `DELETE /ads/v1/account/{accountID}/delete-user/{userID}` | 5 |
| `POST /ads/v1/account/{accountID}/set-user-role` | 5 |
| `GET /ads/v1/account/{accountID}/users` | 1 |

---

## Обратная связь

Нашли ошибку в документации или хотите попросить новый метод API? [Пройдите короткий опрос ↗](https://survey.uxfeedback.ru/WUP9kBTpyutd) — это занимает пару минут и помогает нам приоритизировать улучшения API.
