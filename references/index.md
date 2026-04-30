# Avito API — индекс категорий

Источник: официальный каталог `developers.avito.ru/api-catalog` (`/web/1/openapi/list` + `/web/1/openapi/info/<slug>`). Полный спек: [avito-api-openapi.json](./avito-api-openapi.json) (~1.7 МБ, 197 путей / 203 операций / 23 разделов).

Документация по разделам — в [sections/](./sections/) (интеграция, примеры, sandbox).

**Не читай OpenAPI целиком.** Используй `scripts/lookup_endpoint.py` (`tags`/`search`/`show`).

Категории отсортированы по числу эндпоинтов.

## Доставка (31) — [docs](./sections/delivery-sandbox.md)

- `POST   /cancelAnnouncement` — Отмена анонса в СД
- `POST   /createAnnouncement` — Создание анонса в СД
- `POST   /createParcel` — Создание посылки
- `POST   /delivery-sandbox/announcements/create` — Создание анонса в Avito
- `POST   /delivery-sandbox/announcements/track` — Трекинг анонсов
- `POST   /delivery-sandbox/areas/custom-schedule` — Установка графика работы на определённый день
- `POST   /delivery-sandbox/cancelParcel` — Отмена посылки
- `POST   /delivery-sandbox/order/checkConfirmationCode` — Проверка кода подтверждения
- `POST   /delivery-sandbox/order/properties` — Добавление / изменение параметров доставки посылки
- `POST   /delivery-sandbox/order/realAddress` — Фактический адрес приёма / возврата посылки
- `POST   /delivery-sandbox/order/tracking` — Трекинг
- `POST   /delivery-sandbox/prohibitOrderAcceptance` — Запрет приёма посылки от отправителя
- `GET    /delivery-sandbox/sorting-center` — Получить список сортировочных центров
- `POST   /delivery-sandbox/tariffs/sorting-center` — Загрузить сортировочные центры
- `POST   /delivery-sandbox/tariffs/{tariff_id}/areas` — Загрузить области доставки
- `POST   /delivery-sandbox/tariffs/{tariff_id}/tagged-sorting-centers` — Установка тэгов своим и/или чужим сортировочным центрам
- `POST   /delivery-sandbox/tariffs/{tariff_id}/terminals` — Загрузить терминалы
- `POST   /delivery-sandbox/tariffs/{tariff_id}/terms` — Обновить сроки по тарифу
- `POST   /delivery-sandbox/tariffsV2` — Загрузить новый тариф v2
- `GET    /delivery-sandbox/tasks/{task_id}` — Получение информации по задаче
- `POST   /delivery-sandbox/v1/cancelAnnouncement` — Отправка события об отмене тестового анонса
- `POST   /delivery-sandbox/v1/cancelParcel` — Отмена тестовой посылки
- `POST   /delivery-sandbox/v1/changeParcel` — Создание заявки на изменение данных тестовой посылки
- `POST   /delivery-sandbox/v1/createAnnouncement` — Создание тестового анонса
- `POST   /delivery-sandbox/v1/getAnnouncementEvent` — Получение последнего события тестового анонса
- `POST   /delivery-sandbox/v1/getChangeParcelInfo` — Получение информации об изменении тестовой посылки
- `POST   /delivery-sandbox/v1/getParcelInfo` — Получение информации о тестовой посылке
- `POST   /delivery-sandbox/v1/getRegisteredParcelID` — Получение ID зарегистрированной тестовой посылки
- `POST   /delivery-sandbox/v2/createParcel` — Создание тестовой посылки
- `POST   /delivery/order/changeParcelResult` — Отправка результата исполнения заявки
- `POST   /sandbox/changeParcels` — Обновление свойств посылок

## Автотека (27) — [docs](./sections/autoteka.md)

- `POST   /autoteka/v1/catalogs/resolve` — Получение актуальных параметров Автокаталога
- `POST   /autoteka/v1/get-leads/` — Получение событий сервиса Сигнал
- `POST   /autoteka/v1/monitoring/bucket/add` — Добавить идентификаторы (vin/frame) на мониторинг
- `POST   /autoteka/v1/monitoring/bucket/delete` — Полная очистка списка мониторинга
- `POST   /autoteka/v1/monitoring/bucket/remove` — Удаление идентификаторов из мониторинга (vin/frame)
- `GET    /autoteka/v1/monitoring/get-reg-actions/` — Получение событий мониторинга
- `GET    /autoteka/v1/packages/active_package` — Запрос остатка отчётов пользователя
- `POST   /autoteka/v1/previews` — Превью по VIN или номеру кузова
- `GET    /autoteka/v1/previews/{previewId}` — Получение превью по его ID
- `POST   /autoteka/v1/reports` — Отчет по превью
- `POST   /autoteka/v1/reports-by-vehicle-id` — Отчет по идентификатору авто (vin/frame)
- `GET    /autoteka/v1/reports/list/` — Получение списка отчётов
- `GET    /autoteka/v1/reports/{report_id}` — Получение отчета по его ID
- `POST   /autoteka/v1/request-preview-by-external-item` — Превью по ID объявления другой площадки
- `POST   /autoteka/v1/request-preview-by-item-id` — Превью по ID объявления Авито
- `POST   /autoteka/v1/request-preview-by-regnumber` — Превью по государственному номеру
- `POST   /autoteka/v1/scoring/by-vehicle-id` — Скоринг рисков по идентификатору авто (vin/frame)
- `GET    /autoteka/v1/scoring/{scoring_id}` — Получение скоринга рисков по его ID
- `POST   /autoteka/v1/specifications/by-plate-number` — Запрос характеристик по регистрационному номеру
- `POST   /autoteka/v1/specifications/by-vehicle-id` — Запрос характеристик по идентификатору авто (vin/frame)
- `GET    /autoteka/v1/specifications/specification/{specificationID}` — Получение характеристик по ID запроса
- `POST   /autoteka/v1/sync/create-by-regnumber` — Синхронное создание отчета по ГРЗ
- `POST   /autoteka/v1/sync/create-by-vin` — Синхронное создание отчёта по VIN или номеру кузова
- `POST   /autoteka/v1/teasers` — Тизер по идентификатору авто (vin/frame)
- `GET    /autoteka/v1/teasers/{teaser_id}` — Получение тизера по ID тизера
- `POST   /autoteka/v1/valuation/by-specification` — Получение оценки по параметрам
- `POST   /token` — Получение access token

## Авито.Работа (25) — [docs](./sections/job.md)

- `POST   /job/v1/applications/apply_actions` — Батчевая смена статуса откликов
- `POST   /job/v1/applications/get_by_ids` — Получение списка откликов
- `GET    /job/v1/applications/get_ids` — Получение идентификаторов откликов
- `GET    /job/v1/applications/get_states` — Получение списка возможных статусов откликов
- `POST   /job/v1/applications/set_is_viewed` — Изменение статуса отклика
- `DELETE /job/v1/applications/webhook` — Отключение уведомлений по откликам (webhook)
- `GET    /job/v1/applications/webhook` — Получение информации о подписках (webhook)
- `PUT    /job/v1/applications/webhook` — Включение уведомлений по откликам (webhook)
- `GET    /job/v1/applications/webhooks` — Получение списка подписок (webhook)
- `GET    /job/v1/resumes/` — Поиск резюме
- `GET    /job/v1/resumes/{resume_id}/contacts/` — Доступ к контактным данным соискателя
- `POST   /job/v1/vacancies` — Публикация вакансии
- `PUT    /job/v1/vacancies/archived/{vacancy_id}` — Остановка публикации вакансии
- `PUT    /job/v1/vacancies/{vacancy_id}` — Редактирование вакансии
- `POST   /job/v1/vacancies/{vacancy_id}/prolongate` — Реактивация вакансии
- `GET    /job/v2/resumes/{resume_id}` — Просмотр данных резюме
- `GET    /job/v2/vacancies` — Поиск вакансий
- `POST   /job/v2/vacancies` — Публикация вакансии v2
- `POST   /job/v2/vacancies/batch` — Просмотр данных вакансий
- `POST   /job/v2/vacancies/statuses` — Получение статуса публикации вакансий V2
- `POST   /job/v2/vacancies/update/{vacancy_uuid}` — Редактирование вакансии v2
- `GET    /job/v2/vacancies/{vacancy_id}` — Просмотр данных вакансии
- `PUT    /job/v2/vacancies/{vacancy_uuid}/auto_renewal` — Автопродление вакансии v2
- `GET    /job/v2/vacancy/dict` — Получение списка доступных словарей
- `GET    /job/v2/vacancy/dict/{dictionary_id}` — Получение доступных значений списка по ID словаря

## Автозагрузка (17) — [docs](./sections/autoload.md)

- `GET    /autoload/v1/profile` — Получение профиля пользователя автозагрузки (deprecated) ⚠️ deprecated
- `POST   /autoload/v1/profile` — Создание/редактирование настроек профиля пользователя автозагрузки (deprecated) ⚠️ deprecated
- `POST   /autoload/v1/upload` — Загрузка файла по ссылке
- `GET    /autoload/v1/user-docs/node/{node_slug}/fields` — Получения полей категории
- `GET    /autoload/v1/user-docs/tree` — Получение дерева категорий
- `GET    /autoload/v2/items/ad_ids` — ID объявлений из файла
- `GET    /autoload/v2/items/avito_ids` — ID объявлений на Авито
- `GET    /autoload/v2/profile` — Получение профиля пользователя автозагрузки
- `POST   /autoload/v2/profile` — Создание/редактирование настроек профиля пользователя автозагрузки
- `GET    /autoload/v2/reports` — Список отчётов автозагрузки
- `GET    /autoload/v2/reports/items` — Объявления по ID в автозагрузке
- `GET    /autoload/v2/reports/last_completed_report` — Статистика по последней выгрузке (deprecated) ⚠️ deprecated
- `GET    /autoload/v2/reports/{report_id}` — Статистика по конкретной выгрузке (deprecated) ⚠️ deprecated
- `GET    /autoload/v2/reports/{report_id}/items` — Все объявления из конкретной выгрузки
- `GET    /autoload/v2/reports/{report_id}/items/fees` — Списания за объявления в конкретной выгрузке
- `GET    /autoload/v3/reports/last_completed_report` — Статистика по последней выгрузке
- `GET    /autoload/v3/reports/{report_id}` — Статистика по конкретной выгрузке

## Мессенджер (13) — [docs](./sections/messenger.md)

- `POST   /messenger/v1/accounts/{user_id}/chats/{chat_id}/messages` — Отправка сообщения
- `POST   /messenger/v1/accounts/{user_id}/chats/{chat_id}/messages/image` — Отправка сообщения с изображением
- `POST   /messenger/v1/accounts/{user_id}/chats/{chat_id}/messages/{message_id}` — Удаление сообщения
- `POST   /messenger/v1/accounts/{user_id}/chats/{chat_id}/read` — Прочитать чат
- `GET    /messenger/v1/accounts/{user_id}/getVoiceFiles` — Получение голосовых сообщений
- `POST   /messenger/v1/accounts/{user_id}/uploadImages` — Загрузка изображений
- `POST   /messenger/v1/subscriptions` — Получение подписок (webhooks)
- `POST   /messenger/v1/webhook/unsubscribe` — Отключение уведомлений (webhooks)
- `POST   /messenger/v2/accounts/{user_id}/blacklist` — Добавление пользователя в blacklist
- `GET    /messenger/v2/accounts/{user_id}/chats` — Получение информации по чатам
- `GET    /messenger/v2/accounts/{user_id}/chats/{chat_id}` — Получение информации по чату
- `GET    /messenger/v3/accounts/{user_id}/chats/{chat_id}/messages/` — Получение списка сообщений V3
- `POST   /messenger/v3/webhook` — Включение уведомлений V3 (webhooks)

## Управление заказами (12) — [docs](./sections/order-management.md)

- `POST   /order-management/1/markings` — Передача честного знака
- `POST   /order-management/1/order/acceptReturnOrder` — Выбор отделения отделения Почты России для получения возврата
- `POST   /order-management/1/order/applyTransition` — Изменение статуса заказа
- `POST   /order-management/1/order/checkConfirmationCode` — Метод для проверки кода подтверждения заказа.
- `POST   /order-management/1/order/cncSetDetails` — Метод для подготовки заказа с самовывозом
- `GET    /order-management/1/order/getCourierDeliveryRange` — Метод получения доступных временных промежутков приезда курьера
- `POST   /order-management/1/order/setCourierDeliveryRange` — Метод выбора определённого доступного временного промежутка для приезда курьера
- `POST   /order-management/1/order/setTrackingNumber` — Передача трек-номера
- `GET    /order-management/1/orders` — Получение информации о заказах
- `POST   /order-management/1/orders/labels` — Создать задачу на генерацию этикеток (до 100).
- `POST   /order-management/1/orders/labels/extended` — Создать задачу на генерацию этикеток (до 1000).
- `GET    /order-management/1/orders/labels/{taskID}/download` — Скачать сгенерированный PDF-файл (этикетку).

## CPA Авито (11) — [docs](./sections/cpa.md)

- `GET    /cpa/v1/call/{call_id}` — Запись звонка (deprecated) ⚠️ deprecated
- `GET    /cpa/v1/chatByActionId/{actionId}` — Чат
- `POST   /cpa/v1/chatsByTime` — Чаты по времени (deprecated)
- `POST   /cpa/v1/createComplaint` — Создание жалобы для звонков
- `POST   /cpa/v1/createComplaintByActionId` — Создание жалобы для звонков/чатов
- `POST   /cpa/v1/phonesInfoFromChats` — Информация по номерам телефонов из целевых чатов
- `POST   /cpa/v2/balanceInfo` — Баланс (deprecated) ⚠️ deprecated
- `POST   /cpa/v2/callById` — Звонок ⚠️ deprecated
- `POST   /cpa/v2/callsByTime` — Звонки по времени
- `POST   /cpa/v2/chatsByTime` — Чаты по времени
- `POST   /cpa/v3/balanceInfo` — Баланс

## Объявления (11) — [docs](./sections/item.md)

- `POST   /core/v1/accounts/{userId}/vas/prices` — Получение информации о стоимости услуг продвижения и доступных значках
- `POST   /core/v1/accounts/{user_id}/calls/stats/` — Получение статистики по звонкам
- `GET    /core/v1/accounts/{user_id}/items/{item_id}/` — Получение информации по объявлению
- `PUT    /core/v1/accounts/{user_id}/items/{item_id}/vas` — Применение дополнительных услуг
- `GET    /core/v1/items` — Получение информации по объявлениям
- `POST   /core/v1/items/{item_id}/update_price` — Обновление цены объявления
- `PUT    /core/v2/accounts/{user_id}/items/{item_id}/vas_packages` — Применение пакета дополнительных услуг
- `PUT    /core/v2/items/{itemId}/vas/` — Применение услуг продвижения
- `POST   /stats/v1/accounts/{user_id}/items` — Получение статистики по списку объявлений
- `POST   /stats/v2/accounts/{user_id}/items` — Получение статистических показателей по профилю
- `POST   /stats/v2/accounts/{user_id}/spendings` — Получение статистики расходов профиля

## Автостратегия (7) — [docs](./sections/autostrategy.md)

- `POST   /autostrategy/v1/budget` — Расчет бюджета кампании
- `POST   /autostrategy/v1/campaign/create` — Создание новой кампании
- `POST   /autostrategy/v1/campaign/edit` — Редактирование кампании
- `POST   /autostrategy/v1/campaign/info` — Получение полной информации о кампании
- `POST   /autostrategy/v1/campaign/stop` — Остановка кампании
- `POST   /autostrategy/v1/campaigns` — Получение списка кампаний
- `POST   /autostrategy/v1/stat` — Получение статистики по кампании

## Продвижение (7) — [docs](./sections/promotion.md)

- `POST   /promotion/v1/items/services/bbip/forecasts/get` — BBIP. Прогноз продвижения
- `PUT    /promotion/v1/items/services/bbip/orders/create` — BBIP. Подключение услуги продвижения
- `POST   /promotion/v1/items/services/bbip/suggests/get` — BBIP. Варианты бюджета продвижения
- `POST   /promotion/v1/items/services/dict` — Словарь типов услуг продвижения
- `POST   /promotion/v1/items/services/get` — Список услуг продвижения
- `POST   /promotion/v1/items/services/orders/get` — Список заявок
- `POST   /promotion/v1/items/services/orders/status` — Статус заявки

## Иерархия Аккаунтов (5) — [docs](./sections/accounts-hierarchy.md)

- `GET    /checkAhUserV1` — Получение информации о статусе пользователя в ИА
- `GET    /getEmployeesV1` — Получение списка сотрудников иерархии
- `POST   /linkItemsV1` — Прикрепление сотрудника иерархии к объявлениям, перезакрепление объявлений между сотруд…
- `GET    /listCompanyPhonesV1` — Получение списка телефонов компании
- `POST   /listItemsByEmployeeIdV1` — Получение списка объявлений по сотруднику

## Краткосрочная аренда (5) — [docs](./sections/str.md)

- `POST   /core/v1/accounts/{user_id}/items/{item_id}/bookings` — Заполнение календаря занятости объекта недвижимости
- `GET    /realty/v1/accounts/{user_id}/items/{item_id}/bookings` — Получение списка броней по объявлению
- `POST   /realty/v1/accounts/{user_id}/items/{item_id}/prices` — Актуализация параметров для выбранных периодов
- `POST   /realty/v1/items/intervals` — Заполнение доступности объекта недвижимости с квотами и без
- `POST   /realty/v1/items/{item_id}/base` — Установка базовых параметров

## Настройка цены целевого действия (5) — [docs](./sections/cpxpromo.md)

- `GET    /cpxpromo/1/getBids/{itemId}` — Получение детализированной информации о действующих и доступных ценах за целевые действ…
- `POST   /cpxpromo/1/getPromotionsByItemIds` — Получение текущих цен за целевое действие и бюджетов по нескольким объявлениям
- `POST   /cpxpromo/1/remove` — Остановка продвижения
- `POST   /cpxpromo/1/setAuto` — Применение автоматической настройки
- `POST   /cpxpromo/1/setManual` — Применение ручной настройки

## Рассылка скидок и спецпредложений в мессенджере (beta-version) (5) — [docs](./sections/sbc-gateway.md)

- `POST   /special-offers/v1/available` — Получение информации об объявлениях
- `POST   /special-offers/v1/multiConfirm` — Отправка и оплата рассылки
- `POST   /special-offers/v1/multiCreate` — Создание рассылки
- `POST   /special-offers/v1/stats` — Получение статистики
- `POST   /special-offers/v1/tariffInfo` — Получение информации о тарифе

## Рейтинги и отзывы (4) — [docs](./sections/ratings.md)

- `POST   /ratings/v1/answers` — Отправка ответа на отзыв
- `DELETE /ratings/v1/answers/{answer_id}` — Запрос на удаление ответа на отзыв
- `GET    /ratings/v1/info` — Получение информации о рейтинге пользователя
- `GET    /ratings/v1/reviews` — Получение списка активных отзывов на пользователя с пагинацией

## CallTracking[КТ] (3) — [docs](./sections/calltracking.md)

- `POST   /calltracking/v1/getCallById/` — Звонок по идентификатору
- `POST   /calltracking/v1/getCalls/` — Звонки по времени
- `GET    /calltracking/v1/getRecordByCallId/` — Получение аудиозаписи звонка по идентификатору

## TrxPromo (3) — [docs](./sections/trxpromo.md)

- `POST   /trx-promo/1/apply` — Запуск продвижения
- `POST   /trx-promo/1/cancel` — Остановка продвижения
- `GET    /trx-promo/1/commissions` — Проверка доступности продвижения и размера комиссий

## Информация о пользователе (3) — [docs](./sections/user.md)

- `POST   /core/v1/accounts/operations_history/` — Получение истории операций пользователя
- `GET    /core/v1/accounts/self` — Получение информации об авторизованном пользователе
- `GET    /core/v1/accounts/{user_id}/balance/` — Получение баланса кошелька пользователя

## CPA-аукцион (2) — [docs](./sections/auction.md)

- `GET    /auction/1/bids` — Получение информации о действующих и доступных ставках
- `POST   /auction/1/bids` — Сохранение новых ставок

## Авторизация (2) — [docs](./sections/auth.md)

- `POST   /token‎` — Получение access token
- `POST   /token‎‎` — Обновление access token

## Аналитика по недвижимости (2)

- `GET    /realty/v1/marketPriceCorrespondence/{itemId}/{price}` — Получение соответствия переданной цены рыночной цене
- `POST   /realty/v1/report/create/{itemId}` — Получение аналитического отчета по недвижимости

## Управление остатками (2) — [docs](./sections/stock-management.md)

- `POST   /stock-management/1/info` — Получение остатков
- `PUT    /stock-management/1/stocks` — Редактирование остатков

## Тарифы (1) — [docs](./sections/tariff.md)

- `GET    /tariff/info/1` — Информация по тарифу
