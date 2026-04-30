# Доставка (`delivery-sandbox`)

Методы API для партнеров для работы с API Логистики.
**Avito API предоставляется согласно [Условиям использования](https://www.avito.ru/legal/pro_tools/public-api).**
<!-- ReDoc-Inject: <security-definitions> -->

---

# Термины и сокращения

- 3PL (от англ. third party logistics) – служба доставки, исполняющая полный цикл логистических услуг. Т.е. приемку, 
магистральную перевозку, выдачу и т.д.
- Посылка (от англ. parcel, PARCEL) – отслеживаемый объект, который едет в физическом мире от точки отправки до точки вручения.
- PUDO (от англ. Pick Up Drop Off) – пункт выдачи / получения заказов. Может быть постаматом.
- Заказ (сделка, от англ. order) – набор товаров, которые заказал покупатель на Avito.
- ПВЗ – пункт выдачи / получения заказов. ПВЗ == PUDO.
- Постамат – автоматизированная станция приема и выдачи посылок. Тот же ПВЗ, только без живых людей и более ограниченной
пропускной способностью из-за своих габаритов.
- Посылка (от англ. parcel) – отслеживаемый объект, который движется в реальном мире от точки отправки до
точки вручения.
- СД – служба доставки.
- СЦ – сортировочный центр.
- Терминал – узел маршрута доставки. Например, "терминалом" может быть ПВЗ, СЦ или постамат.
- ЦиК – процедура проверки целостности и комплектности посылки. Может осуществляться как на приёме посылки,
так и на выдаче.
- Прямой поток – процесс доставки посылки от отправителя к получателю.
- Обратный поток – процесс доставки возврата от получателя к отправителю. Обратный поток начинается после агентского или 
клиентского возвратов.
- Агентский возврат – возврат без выдачи посылки получателю. Возможен в случае отказа получателя от получения 
посылки в ПВЗ без вручения. Либо получатель не пришел за посылкой вовсе, она оказалась невостребованной. Агентский возврат 
осуществляется под номером прямой посылки Avito.
- Клиентский возврат – возврат, который инициирует получатель после того, как посылка ему была выдана. Возможностью 
клиентского возврата управляет Avito, позволяя или не позволяя получателю инициировать создание новой возвратной посылки.
- ВГХ – весогабаритные характеристики. Употребляем как в отношении посылки, так и в отношении отдельного взятого товара,
которые могут лежать в посылки. ВГХ – вес, длина, ширина, высота.
- C2C (от англ. client to client) – этот термин употребляется по отношению к бизнес-процессам, в которых конечными 
клиентами являются физические лица. Классическая сделка купли-продажи на Avito происходит между продавцом-физлицом и 
покупателем, который тоже физическое лицо.
- B2C (от англ. business to client) – этот термин употребляется по отношению к бизнес-процессам, в которых конечными
клиентами являются юридическое и физическое лица. Например, юридическое лицо "ИП Иванов" отправил с доставкой
свой товар физическому лицу Сергееву Сергею Сергеевичу.
- КГТ - крупногабаритные товары.

# C2C-ПВЗ сценарий
C2C-ПВЗ сценарий называется так, потому что посылка “едет” от отправителя-физлица к получателю, который тоже является
физическим лицом.

Это простейший сценарий, который является "базовым" для всех остальных сценариев вроде B2C и кросс-доставки. Несмотря на
то, что он простейший, на нем при первичном подключении служба доставки реализует и настраивает бОльшую часть интеграций
с Avito.

### Примеры запросов на создание посылок

<details>
<summary>Пример запроса на создание C2C-посылки</summary>

```json
{
  "orderID": "37476980088635974",
  "parcelID": "P00037988",
  "items": [
    {
      "id": 2639716187,
      "title": "Подставки",
      "description": "Подставки с рекламой,  в наборе 17 штук.",
      "cost": 30000,
      "quantity": 1,
      "breadcrumbs": [
        {
          "name": "Москва"
        },
        {
          "name": "Хобби и отдых"
        },
        {
          "name": "Коллекционирование"
        },
        {
          "name": "Модели"
        }
      ],
      "dimensions": {
        "accuracy": "APPROXIMATE",
        "values": [
          40,
          15,
          30
        ]
      },
      "weight": {
        "accuracy": "APPROXIMATE",
        "value": 1000
      },
      "imagesUrls": {
        "listing": "//01-img-staging-proxy.k.avito.ru/image/1/1.3D5hCra-cNdXo7LSVQnoRGUFohLVqXbT1Sl4FdCpdN_VoXI.4Q-_IforWBTgJ_4VUeJcI9o4Vj4p2CBZPZbcP7ISH0s",
        "list": [
          "//01-img-staging-proxy.k.avito.ru/image/1/1.3D5hCra-cNdXo7LSVQnoRGUFohLVqXbT1Sl4FdCpdN_VoXI.4Q-_IforWBTgJ_4VUeJcI9o4Vj4p2CBZPZbcP7ISH0s"
        ]
      }
    }
  ],
  "sender": {
    "type": "PRIVATE",
    "phones": [
      "79999999999"
    ],
    "email": "email4321@avito-test.ru",
    "name": "the_best_seller_in_the_world",
    "delivery": {
      "type": "TERMINAL",
      "terminal": {
        "provider": "pochta",
        "id": "117525",
        "accuracy": "APPROXIMATE"
      },
      "completenessAndIntegrity": [
        "DIRECT_FLOW",
        "RETURN_FLOW"
      ]
    }
  },
  "receiver": {
    "type": "PRIVATE",
    "phones": [
      "79999999999"
    ],
    "email": "email1234@avito-test.ru",
    "name": "Иванов Иван Иванович",
    "delivery": {
      "type": "TERMINAL",
      "terminal": {
        "provider": "pochta",
        "id": "119296",
        "accuracy": "EXACT"
      },
      "completenessAndIntegrity": [
        "DIRECT_FLOW"
      ]
    }
  },
  "payment": {
    "items": {
      "status": "PAID",
      "cost": 30000
    },
    "delivery": {
      "status": "PAID",
      "costWithoutVat": 10000
    }
  },
  "options": {
    "return": {
      "refused": {
        "action": "RETURN_TO_DEPARTURE_POINT"
      },
      "unclaimed": {
        "action": "RETURN_TO_DEPARTURE_POINT",
        "after": {
          "unit": "DAY",
          "value": 14
        }
      },
      "returned": {
        "action": "DESTROY",
        "after": {
          "unit": "DAY",
          "value": 14
        }
      }
    },
    "tags": [
      "C2C"
    ]
  }
}
```

</details>

<details>
<summary>Пример успешного ответа</summary>

```json
{
  "data": {
    "dispatchNumber": "80512198042480",
    "trackingNumber": "80512198042480"
  }
}
```

</details>

### Схема движения С2С-ПВЗ посылок на прямом потоке
Начнем с визуализации бизнес-процесса.

Действующие лица:
- Покупатель, он же получатель.
- Продавец, он же отправитель.
- Avito.
- Служба доставки.

Схема движения C2C-ПВЗ посылок глазами Avito выглядит максимально просто. Партнерская служба доставки решает
задачу приема посылки от отправителя, доставляет её и выдает получателю.

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/delivery-c2c-flow-direct.png" />

1. Отправитель (физ. лицо) относит посылку PARCEL в ПВЗ сдачи 3PL PUDO 1.
2. Служба доставки 3PL доставляет посылку в пункт получения 3PL PUDO 2.
3. Получатель (физ. лицо) забирает посылку PARCEL.

Детализируем эту простую схему. На ней покажем как в целом устроен процесс доставки, в каких точках есть взаимодействие
по API с Avito.

<details>
<summary>Детальная схема доставки</summary>

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/delivery-c2c-flow-direct-detailed-sequence-v2.png" />

Замечания по схеме:
- Последовательность треков может отличаться у разных посылок, это норма. Где-то может не быть промежуточного
сортировочного центра, где-то их может быть больше одного. Поэтому отправку треков нужно реализовывать, опираясь на 
события, которые происходят в реальном мире.
- Обмер и взвешивание у всех партнеров происходит в разных точках. У кого-то единственный обмер и взвешивание происходит
на ПВЗ приема, у кого-то на первом в цепочке сортировочном центре, у кого-то посылка обмеряется дважды, как на схеме. 
Важно то, чтобы в Avito гарантированно приходили настоящие ВГХ посылки.
- В Avito обязательно нужно присылать фактический ПВЗ сдачи посылки и настоящую стоимость доставки посылки, которая, как
правило, становится известна после её обмера и взвешивания.

</details>

Итого, для реализации простейшего сценария C2C-доставки нужно поддержать работу с Avito по нескольким методам API:
- [Создание посылки](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/createParcel) 
([описание](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/sozdanie_posylki)).
- [Трекинг](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/treking) 
([описание](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/treking)).
- [Установка фактического адреса приема посылки](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/setOrderRealAddress).
- [Установка настоящих ВГХ, стоимости доставки посылки](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/ChangeParcels).
- [Запрет приема посылки](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/prohibitOrderAcceptance) 
([описание](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/zapret_priema_posylki)).

### Схема движения С2С-ПВЗ посылок на обратном потоке

В C2C-ПВЗ сценарии есть агентские возвраты. Получатель может прийти в пункт получения, осмотреть на месте посылку и 
товар в течение ограниченного времени и, если что-то не понравится, вернуть посылку. Или же получатель может не прийти 
вовсе, и посылка оказывается невостребованной. Это тоже агентский возврат.

> [!IMPORTANT]
> Агентский возврат во всех сценариях осуществляется под номером прямой посылки Avito. Мы ожидаем, что по "прямому" номеру посылки от
> службы доставки будут приходить треки с возвратными статусами `IN_TRANSIT_RETURN`, `ON_DELIVERY_RETURN`, `RETURNED`.

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/delivery-c2c-flow-return.png" />

1. Отправитель (физ. лицо) относит посылку PARCEL в ПВЗ сдачи 3PL PUDO 1.
2. Посылка едет в ПВЗ получения 3PL PUDO 2 к получателю.
3. Получатель приходит на пункт выдачи. Сотрудник выдает ему посылку для проверки на месте.
4. Получатель возвращает посылку, т.к. она ему не нравится. Та же посылка PARCEL едет назад в пункт, в который сдавал отправитель.
5. Отправитель забирает возврат. Если не забирает, то он утилизируется.

<details>
<summary>Детальная схема доставки</summary>

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/delivery-c2c-flow-return-detailed-sequence-v3.png" />

Замечания по схеме:
- В C2C-ПВЗ сценарии статус `DELIVERED` ("выдано") проставляется посылке тогда, когда получатель подтверждает получение.
Отправка `DELIVERED` в Avito заблокирует агентский возврат, т.к. статус `DELIVERED` у посылки – терминальный.
- Аналогично прямому потоку, последовательность треков может отличаться у разных посылок. Где-то может не быть 
промежуточного сортировочного центра, где может их быть больше одного. Поэтому отправку треков нужно реализовывать, 
опираясь на события, которые происходят в реальном мире.
- Комбинация `IN_TRANSIT_RETURN` \+ `STORE_TERM_FINISHED` в случае невостребования посылки может быть только в том случае, 
если вы гарантируете, что после истечения срока хранения посылка больше не может быть получена получателем. 
Если какое-то время посылка после истечения срока хранения может быть получена получателем, то присылайте 
`ON_DELIVERY` \+ `STORE_TERM_FINISHED`.

</details>

### Трекинг C2C-ПВЗ посылок
В этом разделе на одной картинке приводим последовательность смены статуса посылок в случае успешной выдачи или возврата.

Про физический смысл трекинга, про статусы посылок, чем они отличаются от событий и прочие подробности рассказываем в
разделе [Трекинг](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/treking).

Когда какие треки со статусами следует присылать, лучше видно на детализированных схемах доставки, которые были выше под 
катами.

Схема движения посылки по статусам в случае успешной выдачи:

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/delivery-c2c-tracking-success.png" />

Схема движения посылки по статусам в случае агентского возврата:

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/delivery-c2c-tracking-agent-return.png" />

### Теги в C2C-ПВЗ посылках
У посылок будет в запросе указан единственный тег `C2C`, который указывает на то, что посылка – C2C-ПВЗ. 

# B2C-ПВЗ сценарий
B2C-ПВЗ сценарий называется так, потому что посылка “едет” от отправителя-юрлица к получателю, который является
физическим лицом.

На прямом потоке B2C-доставка очень схожа с обычной C2C-ПВЗ доставкой. Отправитель относит посылку в пункт приема,
получатель получает посылку в пункте выдачи.

Но есть отличия:
- Отправитель – юридическое, а не физическое лицо.
- ЦиК на приеме посылки от отправителя не проводится. По умолчанию считаем, что продавец приносит товар в заводской
упаковке, которую вскрывать нельзя.
- Статус юридического лица отправителя (продавца) подразумевает, что получатель (он же покупатель) может вернуть 
неподходящий ему товар в течение 14 дней.
- Получатель посылки через Avito может создать отдельную возвратную посылку, которую он отправит назад изначальному
отправителю.
- ЦиК на приеме возврата от получателя проводится.
- Для службы доставки процесс создания возвратной посылки прозрачен. Выглядит это так, как будто Avito создает посылку с 
некоторыми особенностями.

### Примеры запросов на создание посылок

<details>
<summary>Пример запроса на создание B2C-посылки</summary>

```json
{
  "orderID": "37476980088635974",
  "parcelID": "P00037988",
  "items": [
    {
      "id": 2639716187,
      "title": "Подставки",
      "description": "Подставки с рекламой,  в наборе 17 штук.",
      "cost": 30000,
      "quantity": 1,
      "breadcrumbs": [
        {
          "name": "Москва"
        },
        {
          "name": "Хобби и отдых"
        },
        {
          "name": "Коллекционирование"
        },
        {
          "name": "Модели"
        }
      ],
      "dimensions": {
        "accuracy": "APPROXIMATE",
        "values": [
          40,
          15,
          30
        ]
      },
      "weight": {
        "accuracy": "APPROXIMATE",
        "value": 1000
      },
      "imagesUrls": {
        "listing": "//01-img-staging-proxy.k.avito.ru/image/1/1.3D5hCra-cNdXo7LSVQnoRGUFohLVqXbT1Sl4FdCpdN_VoXI.4Q-_IforWBTgJ_4VUeJcI9o4Vj4p2CBZPZbcP7ISH0s",
        "list": [
          "//01-img-staging-proxy.k.avito.ru/image/1/1.3D5hCra-cNdXo7LSVQnoRGUFohLVqXbT1Sl4FdCpdN_VoXI.4Q-_IforWBTgJ_4VUeJcI9o4Vj4p2CBZPZbcP7ISH0s"
        ]
      }
    }
  ],
  "sender": {
    "type": "LEGAL",
    "phones": [
      "79999999999"
    ],
    "email": "email4321@avito-test.ru",
    "name": "ИП Сергеев С.С.",
    "delivery": {
      "type": "TERMINAL",
      "terminal": {
        "provider": "pochta",
        "id": "117525",
        "accuracy": "APPROXIMATE"
      },
      "completenessAndIntegrity": [
        "DIRECT_FLOW",
        "RETURN_FLOW"
      ]
    }
  },
  "receiver": {
    "type": "PRIVATE",
    "phones": [
      "79999999999"
    ],
    "email": "email1234@avito-test.ru",
    "name": "Иванов Иван Иванович",
    "delivery": {
      "type": "TERMINAL",
      "terminal": {
        "provider": "pochta",
        "id": "119296",
        "accuracy": "EXACT"
      },
      "completenessAndIntegrity": [
        "DIRECT_FLOW"
      ]
    }
  },
  "payment": {
    "items": {
      "status": "PAID",
      "cost": 30000
    },
    "delivery": {
      "status": "PAID",
      "costWithoutVat": 10000
    }
  },
  "options": {
    "return": {
      "refused": {
        "action": "RETURN_TO_DEPARTURE_POINT"
      },
      "unclaimed": {
        "action": "RETURN_TO_DEPARTURE_POINT",
        "after": {
          "unit": "DAY",
          "value": 14
        }
      },
      "returned": {
        "action": "DESTROY",
        "after": {
          "unit": "DAY",
          "value": 14
        }
      }
    },
    "tags": [
      "B2C"
    ]
  }
}
```

Отличия от запроса на создание C2C-посылки:
- В `sender.type` указан тип `LEGAL`, т.е. отправитель – юридическое лицо.
- В `options.tags` есть тег `B2C`.

</details>

<details>
<summary>Пример запроса на создание возвратной B2C-посылки</summary>

```json
{
  "orderID": "37476980088635974",
  "parcelID": "P00037988R",
  "items": [
    {
      "id": 2639716187,
      "title": "Подставки",
      "description": "Подставки с рекламой,  в наборе 17 штук.",
      "cost": 30000,
      "quantity": 1,
      "breadcrumbs": [
        {
          "name": "Москва"
        },
        {
          "name": "Хобби и отдых"
        },
        {
          "name": "Коллекционирование"
        },
        {
          "name": "Модели"
        }
      ],
      "dimensions": {
        "accuracy": "APPROXIMATE",
        "values": [
          40,
          15,
          30
        ]
      },
      "weight": {
        "accuracy": "APPROXIMATE",
        "value": 1000
      },
      "imagesUrls": {
        "listing": "//01-img-staging-proxy.k.avito.ru/image/1/1.3D5hCra-cNdXo7LSVQnoRGUFohLVqXbT1Sl4FdCpdN_VoXI.4Q-_IforWBTgJ_4VUeJcI9o4Vj4p2CBZPZbcP7ISH0s",
        "list": [
          "//01-img-staging-proxy.k.avito.ru/image/1/1.3D5hCra-cNdXo7LSVQnoRGUFohLVqXbT1Sl4FdCpdN_VoXI.4Q-_IforWBTgJ_4VUeJcI9o4Vj4p2CBZPZbcP7ISH0s"
        ]
      }
    }
  ],
  "sender": {
    "type": "PRIVATE",
    "phones": [
      "79999999999"
    ],
    "email": "email1234@avito-test.ru",
    "name": "Иванов Иван Иванович",
    "delivery": {
      "type": "TERMINAL",
      "terminal": {
        "provider": "pochta",
        "id": "119296",
        "accuracy": "APPROXIMATE"
      },
      "completenessAndIntegrity": [
        "DIRECT_FLOW"
      ]
    }
  },
  "receiver": {
    "type": "LEGAL",
    "phones": [
      "79999999999"
    ],
    "email": "email4321@avito-test.ru",
    "name": "ИП Сергеев С.С.",
    "delivery": {
      "type": "TERMINAL",
      "terminal": {
        "provider": "pochta",
        "id": "117525",
        "accuracy": "EXACT"
      },
      "completenessAndIntegrity": [
        "DIRECT_FLOW"
      ]
    }
  },
  "payment": {
    "items": {
      "status": "PAID",
      "cost": 30000
    },
    "delivery": {
      "status": "PAID",
      "costWithoutVat": 10000
    }
  },
  "options": {
    "return": {
      "refused": {
        "action": "DESTROY",
        "after": {
          "unit": "DAY",
          "value": 14
        }
      },
      "unclaimed": {
        "action": "DESTROY",
        "after": {
          "unit": "DAY",
          "value": 14
        }
      }
    },
    "tags": [
      "B2C",
      "RETURN"
    ]
  }
}
```

Отличия от запроса на создание прямой B2C-посылки:
- Изначальный отправитель становится получателем возвратной посылки, а изначальный получатель – отправителем возвратной посылки.
- Посылка – невозвратная. Поэтому в `options.return` описана возвратная политика, которая препятствует возврату посылки
  отправителю в случае невостребования.
- ЦиК только на приеме у отправителя и на выдаче получателю. Это следствие того, что посылка невозвратная.
- В `options.tags` есть тег `RETURN`.

</details>

<details>
<summary>Пример успешного ответа</summary>

```json
{
  "data": {
    "dispatchNumber": "80512198042480",
    "trackingNumber": "80512198042480"
  }
}
```

</details>

### Схема движения B2С-ПВЗ посылок на прямом и обратном потоке

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/delivery-b2c-flow-with-return.png" />

1. Отправитель относит посылку в пункт 3PL PUDO 1.
2. Посылка едет в пункт получения 3PL PUDO 2 к получателю.
3. Получатель забирает посылку.
4. Если получатель захочет вернуть полученный товар, он инициирует создание возвратной посылки и относит её в ПВЗ.
5. Возвратная посылка в общем случае едет в ПВЗ, в который прямую посылку сдавал отправитель.
6. Отправитель забирает возврат. Если не забирает, то он утилизируется.

<details>
<summary>Детальная схема доставки на прямом потоке</summary>

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/delivery-b2c-flow-direct-detailed-sequence-v2.png" />

Замечания по схеме:
- ЦиК при приеме посылки от отправителя отсутствует, т.к. в B2C-ПВЗ сценарии его нет. Предполагается, что отправитель
приносит товар в заводской упаковке, которую вскрывать нельзя.
- Последовательность треков может отличаться у разных посылок, это норма. Где-то может не быть промежуточного
сортировочного центра, где-то их может быть больше одного. Поэтому отправку треков нужно реализовывать, опираясь на
события, которые происходят в реальном мире.
- В Avito обязательно нужно присылать фактический ПВЗ сдачи посылки. 
- Обмер и взвешивание у всех партнеров происходит в разных точках. У кого-то единственный обмер и взвешивание происходит
на ПВЗ приема, у кого-то на первом в цепочке сортировочном центре, у кого-то посылка обмеряется дважды, как на схеме.
Важно то, чтобы в Avito гарантированно приходили настоящие ВГХ посылки.
- В Avito обязательно нужно присылать настоящую стоимость доставки посылки, которая, как правило, становится известна 
после её обмера и взвешивания.

</details>

<details>
<summary>Детальная схема доставки при агентском возврате</summary>

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/delivery-b2c-flow-return-detailed-sequence-v3.png" />

Замечания по схеме.
- Аналогично прямому потоку, последовательность треков может отличаться у разных посылок. Где-то может не быть
промежуточного сортировочного центра, где может их быть больше одного. Поэтому отправку треков нужно реализовывать,
опираясь на события, которые происходят в реальном мире.
- Комбинация `IN_TRANSIT_RETURN` \+ `STORE_TERM_FINISHED` в случае невостребования посылки может быть только в том случае,
если вы гарантируете, что после истечения срока хранения посылка больше не может быть получена получателем.
Если какое-то время посылка после истечения срока хранения может быть получена получателем, то присылайте
`ON_DELIVERY` \+ `STORE_TERM_FINISHED`.

</details>

<details>
<summary>Детальная схема доставки при клиентском возврате</summary>

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/delivery-b2c-flow-return-client-detailed-sequence-v3.png" />

Замечания по схеме:
- ЦиК при приеме возвратной посылки есть. Сотрудник должен проверить комплектность.
- Несмотря на то, что PARCEL 2 – возвратная, она едет по прямым статусам `IN_TRANSIT`, `ON_DELIVERY` и `DELIVERED`.
- Отказ от возврата не стали отображать на схеме, чтобы её не загромождать. Здесь действия аналогичны агентскому возврату.

</details>

> [!IMPORTANT]
> Для того, чтобы Avito могло создать возвратную посылку критически необходимо проставлять ПВЗ реальной сдачи продавцом
> через соответствующий [метод](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/setOrderRealAddress).
> Именно этот ПВЗ Avito будет указывать в качестве точки получения при создании возвратной посылки.

<br />

> [!IMPORTANT]
> Возвратная посылка в случае невостребования / отказа изначальным отправителем-продавцом не должна уезжать обратно получателю-покупателю. Avito будет указывать специальные параметры в запросе. См. примеры.

Итого, для реализации сценария B2C-доставки нужно как и в C2C поддержать работу с Avito по нескольким методам API:
- [Создание посылки](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/createParcel)
([описание](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/sozdanie_posylki)).
- [Трекинг](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/treking)
([описание](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/treking)).
- [Установка фактического адреса приема посылки](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/setOrderRealAddress).
- [Установка настоящих ВГХ, стоимости доставки посылки](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/ChangeParcels).
- [Запрет приема посылки](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/prohibitOrderAcceptance)
([описание](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/zapret_priema_posylki)).

### Трекинг B2C-ПВЗ посылок
В этом разделе на одной картинке приводим последовательность смены статуса посылок в случае успешной выдачи или возвратов.

Про физический смысл трекинга, про статусы посылок, чем они отличаются от событий и прочие подробности рассказываем в
разделе [Трекинг](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/treking).

Когда какие треки со статусами следует присылать, лучше видно на детализированных схемах доставки, которые были выше под
катами.

Схема движения посылки по статусам в случае успешной выдачи:

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/delivery-b2c-tracking-success.png" />

Схема движения посылки по статусам в случае агентского возврата:

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/delivery-b2c-tracking-agent-return.png" />

Схема движения посылок по статусам в случае клиентского возврата:

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/delivery-b2c-tracking-client-return.png" />

### Теги в B2C-ПВЗ посылках
У посылок будет в запросе указан единственный тег `B2C`, который указывает на то, что посылка – B2C-ПВЗ.

# C2C постаматный сценарий
Сценарий называется постаматным, потому что посылку отправитель закладывает в постамат, и получатель её тоже забирает 
из постамата.

Постаматный сценарий есть только в C2C.

С точки зрения содержимого запрос на создание постаматной посылки ничем не отличается от запроса на создание C2C-ПВЗ 
посылки. Avito ожидает, что служба доставки сама поймет по содержимому `sender.delivery.terminal.id` и 
`receiver.delivery.terminal.id` что доставка осуществляется из постамата в постамат.

### Примеры запросов на создание посылок

<details>
<summary>Пример запроса на создание постаматной посылки</summary>

```json
{
  "orderID": "37476980088635974",
  "parcelID": "P00037988",
  "items": [
    {
      "id": 2639716187,
      "title": "Подставки",
      "description": "Подставки с рекламой,  в наборе 17 штук.",
      "cost": 30000,
      "quantity": 1,
      "breadcrumbs": [
        {
          "name": "Москва"
        },
        {
          "name": "Хобби и отдых"
        },
        {
          "name": "Коллекционирование"
        },
        {
          "name": "Модели"
        }
      ],
      "dimensions": {
        "accuracy": "APPROXIMATE",
        "values": [
          40,
          15,
          30
        ]
      },
      "weight": {
        "accuracy": "APPROXIMATE",
        "value": 1000
      },
      "imagesUrls": {
        "listing": "//01-img-staging-proxy.k.avito.ru/image/1/1.3D5hCra-cNdXo7LSVQnoRGUFohLVqXbT1Sl4FdCpdN_VoXI.4Q-_IforWBTgJ_4VUeJcI9o4Vj4p2CBZPZbcP7ISH0s",
        "list": [
          "//01-img-staging-proxy.k.avito.ru/image/1/1.3D5hCra-cNdXo7LSVQnoRGUFohLVqXbT1Sl4FdCpdN_VoXI.4Q-_IforWBTgJ_4VUeJcI9o4Vj4p2CBZPZbcP7ISH0s"
        ]
      }
    }
  ],
  "sender": {
    "type": "PRIVATE",
    "phones": [
      "79999999999"
    ],
    "email": "email4321@avito-test.ru",
    "name": "the_best_seller_in_the_world",
    "delivery": {
      "type": "TERMINAL",
      "terminal": {
        "provider": "five-post",
        "id": "16004c6e-a5cd-489e-a62b-4b7c224a0cbd",
        "accuracy": "APPROXIMATE"
      },
      "completenessAndIntegrity": [
        "DIRECT_FLOW",
        "RETURN_FLOW"
      ]
    }
  },
  "receiver": {
    "type": "PRIVATE",
    "phones": [
      "79999999999"
    ],
    "email": "email1234@avito-test.ru",
    "name": "Иванов Иван Иванович",
    "delivery": {
      "type": "TERMINAL",
      "terminal": {
        "provider": "five-post",
        "id": "8cf66bc8-b4a0-472e-9b2a-7d0db93c309a",
        "accuracy": "EXACT"
      },
      "completenessAndIntegrity": [
        "DIRECT_FLOW"
      ]
    }
  },
  "payment": {
    "items": {
      "status": "PAID",
      "cost": 30000
    },
    "delivery": {
      "status": "PAID",
      "costWithoutVat": 10000
    }
  },
  "options": {
    "return": {
      "refused": {
        "action": "RETURN_TO_DEPARTURE_POINT"
      },
      "unclaimed": {
        "action": "RETURN_TO_DEPARTURE_POINT",
        "after": {
          "unit": "DAY",
          "value": 14
        }
      },
      "returned": {
        "action": "DESTROY",
        "after": {
          "unit": "DAY",
          "value": 14
        }
      }
    },
    "tags": [
      "C2C"
    ]
  }
}
```

</details>

<details>
<summary>Пример успешного ответа</summary>

```json
{
  "data": {
    "dispatchNumber": "094472739",
    "trackingNumber": "P000147647124"
  }
}
```

> [!TIP]
> `dispatchNumber` – это код закладки и получения посылки. После его использования он может быть повторно возвращен
> в теле ответа для другой посылки, которую создает Avito.
>
> `trackingNumber` – это по-прежнему трек-номер и для постаматных посылок он должен быть уникален.

</details>

### Схема движения постаматных посылок на прямом потоке
Схема движения постаматных посылок аналогична схеме в C2C-ПВЗ.

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/delivery-c2c-flow-direct.png" />

1. Отправитель относит посылку PARCEL в постамат сдачи 3PL PUDO 1.
2. Служба доставки 3PL доставляет посылку в постамат 3PL PUDO 2.
3. Получатель забирает посылку PARCEL.

<details>
<summary>Детальная схема доставки на прямом потоке</summary>

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/delivery-c2c-locker-flow-direct-detailed-sequence-v3.png" />

Замечания по схеме:
- ЦиК на приеме посылки от отправителя схеме намеренно опущен, т.к. при закладке в постамат он отсутствует.
- Последовательность треков может отличаться у разных посылок, это норма. Где-то может не быть промежуточного
сортировочного центра, где-то их может быть больше одного. Поэтому отправку треков нужно реализовывать, опираясь на
события, которые происходят в реальном мире.
- В Avito обязательно нужно присылать фактический ПВЗ сдачи посылки.
- Обмер и взвешивание, скорее всего, будет происходить на первом в цепочке сортировочном центре. Важно то, чтобы в Avito 
гарантированно приходили настоящие ВГХ посылки.
- В Avito обязательно нужно присылать настоящую стоимость доставки посылки, которая, как правило, становится известна
после её обмера и взвешивания.
- После вскрытия ячейки получатель посылки не может её заложить обратно для возврата. Вскрытие ячейки в постамате 
означает статус `DELIVERED` для посылки. Этот статус – терминальный.

</details>

Для реализации сценария нужно поддержать работу с Avito по нескольким методам API:
- [Создание посылки](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/createParcel)
([описание](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/sozdanie_posylki)).
- [Трекинг](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/treking)
([описание](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/treking)).
- [Установка фактического адреса приема посылки](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/setOrderRealAddress).
- [Установка настоящих ВГХ, стоимости доставки посылки](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/ChangeParcels).
- [Запрет приема посылки](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/prohibitOrderAcceptance) 
([описание](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/zapret_priema_posylki)).

### Схема движения постаматных посылок на обратном потоке
В постаматном сценарии есть агентские возвраты только в случае невостребования посылки.

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/delivery-c2c-locker-return-flow.png" />

1. Отправитель относит посылку PARCEL в постамат сдачи 3PL PUDO 1.
2. Посылка едет в постамат получения 3PL PUDO 2 к получателю.
3. Получатель не забирает посылку, она оказывается невостребованной. Та же посылка PARCEL едет назад в постамат, в который 
сдавал отправитель.
4. Отправитель забирает возврат из постамата 3PL PUDO 1. Если не забирает, то он утилизируется.

<details>
<summary>Детальная схема доставки при агентском возврате</summary>

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/delivery-c2c-locker-flow-return-detailed-sequence-v3.png" />

Замечания по схеме.
- Аналогично прямому потоку, последовательность треков может отличаться у разных посылок. Где-то может не быть
  промежуточного сортировочного центра, где может их быть больше одного. Поэтому отправку треков нужно реализовывать,
  опираясь на события, которые происходят в реальном мире.
- Комбинация `IN_TRANSIT_RETURN` \+ `STORE_TERM_FINISHED` в случае невостребования посылки может быть только в том случае,
  если вы гарантируете, что после истечения срока хранения посылка больше не может быть получена получателем.
  Если какое-то время посылка после истечения срока хранения может быть получена получателем, то присылайте
  `ON_DELIVERY` \+ `STORE_TERM_FINISHED`.
- Аналогично прямому потоку после вскрытия ячейки отправитель не может её заложить обратно. Вскрытие ячейки в постамате
  означает статус `RETURNED` для посылки. Этот статус – терминальный.

</details>

### Трекинг постаматных посылок
В этом разделе на одной картинке приводим последовательность смены статуса посылок в случае успешной выдачи или возвратов.

Про физический смысл трекинга, про статусы посылок, чем они отличаются от событий и прочие подробности рассказываем в
разделе [Трекинг](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/treking).

Когда какие треки со статусами следует присылать, лучше видно на детализированных схемах доставки, которые были выше под
катами.

Схема движения посылки по статусам в случае успешной выдачи:

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/delivery-c2c-tracking-success.png" />

Схема движения посылки по статусам в случае агентского возврата:

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/delivery-c2c-tracking-agent-return.png" />

### Теги в постаматных посылках
Постаматные посылки сейчас никак не выделяются тегами. У них есть только тег `C2C`, как у C2C-ПВЗ посылок.

# C2C Терминал-Дверь сценарий
Терминал-Дверь сценарий называется так, потому что посылка “едет” от терминала отправителя прямо до двери получателя.
Доставка до двери осуществляется курьером СД.

Cценарий Терминал-Дверь пока есть только в C2C. В этом сценарии возможна доставка только КГТ товаров.

С точки зрения содержимого запрос на создание С2С Терминал-Дверь посылки отличается от запроса на создание C2C-ПВЗ посылки
тем, что к получателю приедет курьер с товаром. Детали курьерской доставки будут в поле `receiver.delivery.courier`.

### Примеры запросов на создание посылок

<details>
<summary>Пример запроса на создание C2C Терминал-Дверь посылки</summary>

```json
{
  "orderID": "58108624273277776",
  "parcelID": "P00012345",
  "items": [
    {
      "id": 2639716187,
      "title": "Подставки",
      "description": "Подставки с рекламой,  в наборе 17 штук.",
      "cost": 30000,
      "quantity": 1,
      "breadcrumbs": [
        {
          "name": "Москва"
        },
        {
          "name": "Хобби и отдых"
        },
        {
          "name": "Коллекционирование"
        },
        {
          "name": "Модели"
        }
      ],
      "dimensions": {
        "accuracy": "APPROXIMATE",
        "values": [
          40,
          15,
          30
        ]
      },
      "weight": {
        "accuracy": "APPROXIMATE",
        "value": 1000
      },
      "imagesUrls": {
        "listing": "//01-img-staging-proxy.k.avito.ru/image/1/1.3D5hCra-cNdXo7LSVQnoRGUFohLVqXbT1Sl4FdCpdN_VoXI.4Q-_IforWBTgJ_4VUeJcI9o4Vj4p2CBZPZbcP7ISH0s",
        "list": [
          "//01-img-staging-proxy.k.avito.ru/image/1/1.3D5hCra-cNdXo7LSVQnoRGUFohLVqXbT1Sl4FdCpdN_VoXI.4Q-_IforWBTgJ_4VUeJcI9o4Vj4p2CBZPZbcP7ISH0s"
        ]
      }
    }
  ],
  "sender": {
    "type": "PRIVATE",
    "phones": [
      "88005553535"
    ],
    "email": "email4321@avito-test.ru",
    "name": "Петров Петр Петрович",
    "delivery": {
      "type": "TERMINAL",
      "terminal": {
        "provider": "pecom-t2d",
        "id": "419",
        "accuracy": "APPROXIMATE"
      },
      "completenessAndIntegrity": [
        "DIRECT_FLOW",
        "RETURN_FLOW"
      ]
    }
  },
  "receiver": {
    "type": "PRIVATE",
    "phones": [
      "88005553535"
    ],
    "email": "any_email@mail.com",
    "name": "Иванов Иван Иванович",
    "delivery": {
      "type": "COURIER",
      "courier": {
        "provider": "pecom-t2d",
        "address": {
          "addressRow": "Москва, ул. Лесная, 20с2",
          "details": {
            "house": "20с2",
            "floor": "4",
            "porch": "2",
            "flat": "23"
          },
          "coordinates": {
            "latitude": 55.779003,
            "longitude": 37.591746
          }
        },
        "dateTimeInterval": {
          "start": "2025-02-01T10:26:15+03:00",
          "end": "2025-02-01T16:26:15+03:00"
        },
        "options": {
          "deliveryType": "DELIVERY_TO_DOOR",
          "deliveryConfirmationType": "PHONE",
          "elevatorAvailable": true,
          "comment": "Позвоните как подъедете"
        }
      }
    }
  },
  "payment": {
    "items": {
      "status": "PAID",
      "cost": 10000
    },
    "delivery": {
      "status": "PAID",
      "costWithoutVat": 10000
    }
  },
  "options": {
    "return": {
      "refused": {
        "action": "RETURN_TO_DEPARTURE_POINT"
      },
      "unclaimed": {
        "action": "RETURN_TO_DEPARTURE_POINT",
        "after": {
          "unit": "DAY",
          "value": 14
        }
      },
      "returned": {
        "action": "DESTROY",
        "after": {
          "unit": "DAY",
          "value": 14
        }
      }
    },
    "tags": [
      "C2C",
      "T2D"
    ]
  }
}

```

</details>

<details>
<summary>Пример успешного ответа</summary>

```json
{
  "data": {
    "dispatchNumber": "80512198042480",
    "trackingNumber": "80512198042480"
  }
}
```

</details>

### Схема движения Терминал-Дверь посылок на прямом потоке
Начнем с визуализации бизнес-процесса.

Действующие лица:
- Покупатель, он же получатель.
- Продавец, он же отправитель.
- Avito.
- Служба доставки (3PL).
- Курьер 3PL.

Схема движения посылок глазами Avito выглядит максимально просто. Партнерская служба доставки решает
задачу приема посылки от отправителя, доставляет её через своего курьера и выдает получателю.

<img style="max-width:100%" src="https://avito.st/static/ims/37404eed-c312-45c7-a9f6-d56d23586bd4_delivery_c2c_t2d_direct_flow_common_2138x1032.png" />

1. Отправитель (физ. лицо) относит посылку PARCEL в терминал сдачи 3PL terminal 1.
2. Служба доставки 3PL доставляет посылку в терминал 3PL terminal 2 в городе получателя.
3. Курьер 3PL забирает посылку PARCEL из терминала 3PL terminal 2 для доставки получателю.
4. Курьер 3PL успешно вручает посылку PARCEL получателю.

Детализируем эту простую схему. На ней покажем как в целом устроен процесс доставки, в каких точках есть взаимодействие
по API с Avito.

<details>
<summary>Детальная схема доставки</summary>

<img style="max-width:100%" src="https://avito.st/static/ims/2a972b39-aebf-45f1-88bc-8b3d648b9fe2_delivery_c2c_t2d_flow_direct_detailed_sequence_common_1264x3729.png" />

Замечания по схеме:
- Обмер и взвешивание посылки происходит после проверки ЦИК. Если посылка не прошла проверку по ВГХ, то ожидаем получить в трекинге
`CONFIRMED` \+ `DIMENSIONS_CHECK_FAILED`.
- В Avito обязательно нужно присылать фактический терминал сдачи посылки и настоящую стоимость доставки посылки, которая, как
  правило, становится известна после её обмера и взвешивания.
- В Avito необходимо передавать признак выполнения обрешетки на терминале отправителя.
- Возможны несколько попыток доставки до получателя (кол-во попыток контролируется на стороне СД), для каждой попытки
  ожидаем получить соответствующую последовательность треков. В случае исчерпания кол-ва попыток доставки, посылка отправляется
  на возврат.

</details>

Итого, для реализации простейшего сценария Терминал-Дверь доставки нужно поддержать работу с Avito по нескольким методам API:
- [Создание посылки](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/createParcel)
  ([описание](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/sozdanie_posylki)).
- [Трекинг](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/treking)
  ([описание](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/treking)).
- [Установка фактического адреса приема посылки](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/setOrderRealAddress).
- [Установка настоящих ВГХ, стоимости доставки посылки, признака выполнения обрешетки](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/setOrderProperties).
- [Запрет приема посылки](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/prohibitOrderAcceptance)
  ([описание](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/zapret_priema_posylki)).

### Схема движения Терминал-Дверь посылок на обратном потоке
В Терминал-Дверь сценарии пока есть только агентские возвраты - получатель при курьере может осмотреть посылку и отказаться
"на месте".
Если после нескольких попыток вручения, получатель не вышел на связь, то такая посылка считается невостребованной.
Это тоже агентский возврат.

> [!IMPORTANT]
> Агентский возврат во всех сценариях осуществляется под номером прямой посылки Avito. Мы ожидаем, что по "прямому" номеру посылки от
> службы доставки будут приходить треки с возвратными статусами `IN_TRANSIT_RETURN`, `ON_DELIVERY_RETURN`, `RETURNED`.

<img style="max-width:100%" src="https://avito.st/static/ims/f1cd7435-e35c-4597-a252-b3070c8693aa_delivery_c2c_t2d_return_flow_common_2164x1414.png" />

1. Отправитель (физ. лицо) относит посылку PARCEL в терминал сдачи 3PL terminal 1.
2. Служба доставки 3PL доставляет посылку в терминал 3PL terminal 2 в городе получателя.
3. Курьер 3PL забирает посылку PARCEL из терминала 3PL terminal 2 для доставки получателю.
4. Курьер 3PL доставляет посылку PARCEL получателю.
5. Получатель проверяет посылку PARCEL и отказывается от нее. Курьер отвозит посылку PARCEL обратно в терминал 3PL terminal 2.
6. Посылка PARCEL приезжает обратно на терминал отправителя 3PL terminal 1.
7. Отправитель приходит на терминал 3PL terminal 1 и забирает посылку PARCEL.

<details>
<summary>Детальная схема доставки</summary>

<img style="max-width:100%" src="https://avito.st/static/ims/cc568a5e-1689-4249-bc35-e689079267e3_delivery_c2c_t2d_flow_return_detailed_sequence_common_1449x2189.png" />

Замечания по схеме:
- В Терминал-Дверь сценарии статус `DELIVERED` ("выдано") проставляется посылке тогда, когда получатель подтверждает получение.
  Отправка `DELIVERED` в Avito заблокирует агентский возврат, т.к. статус `DELIVERED` у посылки – терминальный.
- Комбинация `IN_TRANSIT_RETURN` \+ `STORE_TERM_FINISHED` в случае невостребования посылки может быть только в том случае,
  если вы гарантируете, что после истечения срока хранения посылка больше не может быть получена получателем.

</details>

### Трекинг Терминал-Дверь посылок
В этом разделе на одной картинке приводим последовательность смены статуса посылок в случае успешной выдачи или возврата.

Про физический смысл трекинга, про статусы посылок, чем они отличаются от событий и прочие подробности рассказываем в
разделе [Трекинг](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/treking).

Когда какие треки со статусами следует присылать, лучше видно на детализированных схемах доставки, которые были выше под
катами.

Схема движения посылки по статусам в случае успешной выдачи:

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/delivery-c2c-tracking-success.png" />

Схема движения посылки по статусам в случае агентского возврата:

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/delivery-c2c-tracking-agent-return.png" />

### Теги в Терминал-Дверь посылках
У посылок будет в запросе указаны два тега - `C2C` и `T2D`.

# Кросс-доставка

#### Термины и сокращения
- 3PL1 – служба доставки, которая везет посылку по Плечу 1.
- Плечо 1 – участок пути от отправителя, сдающего посылку в 3PL1, до сортировочного центра 3PL2. На Плече 1
осуществляется переброска посылки от 3PL1 в 3PL2.
- Сортировочный центр (СЦ) - сортировочный центр, в котором осуществляется комплектации посылок для отгрузки в службу
доставки следующего плеча, а также прием посылок от службы доставки предыдущего плеча.
- PARCEL 1 – посылка, которая едет по Плечу 1.
- 3PL2 – служба доставки, которая везет посылку по Плечу 2.
- Плечо 2 – участок пути от сортировочного центра 3PL2 до пункта получателя.
- PARCEL 2 – посылка, которая едет по Плечу 2.
- Плечо 3 (агентский возврат) – опциональное возвратное плечо, если Покупатель отказывается от посылки или не приходит
за ней. Начинается от сортировочного центра 3PL2, заканчивается в пункте отправителя 3PL1.
- Плечо 3 (клиентский возврат) – опциональное возвратное плечо, если Покупатель решает вернуть посылку в течение
некоторого ограниченного срока. Начинается от пункта получателя 3PL2, заканчивается в сортировочном центре 3PL2.
- Плечо 4 (клиентский возврат) – опциональное возвратное плечо. Начинается в сортировочном центре 3PL2, заканчивается в
пункте отправителя 3PL1.
- PARCEL 3 – посылка, которая едет по Плечу 3.
- PARCEL 4 – посылка, которая едет по Плечу 4.

## Механика работы кросс-доставки

Кросс-доставкой называем процесс доставки посылки, в которой участвуют больше одной службы доставки.

### Создание кросс-доставочных посылок

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/xdelivery-creating-parcels.png" />

Кросс-доставка "возникает" в момент, когда для отправки отправитель (продавец товара) или Avito выбирает
для отправки не ту службу доставки, которую для получения товара выбрал получатель (покупатель товара).

Пусть отправитель выбрал службу доставки 3PL1, которую дальше на схемах будем обозначать синим цветом. А получатель
выбрал службу доставки 3PL2, которую обозначим красным цветом.

После выбора 3PL1 отправителем Avito должно построить логистическую цепочку, состоящую из двух посылок PARCEL 1 и
PARCEL 2.

- PARCEL 1 – посылка, перевозимая 3PL1 из пункта приема (в который посылку принес отправитель) в сортировочный центр
3PL2. В этом сортировочном происходит передача посылки от 3PL1 к 3PL2.
- PARCEL 2 – посылка, перевозимая 3PL2 из своего сортировочного центра в пункт выдачи, в который доставку заказал
получатель.

Посылки PARCEL 1 и PARCEL 2 на текущий момент создаются в соответствующих службах доставки последовательно друг за
другом. Так сделано для того, чтобы работала передача посылки от 3PL1 к 3PL2, основанная на штрихкодах.

### Примеры запросов на создание посылок

<details>
<summary>Пример запроса на создание PARCEL 1</summary>

```json
{
  "orderID": "37476980088635974",
  "parcelID": "P00037988",
  "items": [
    {
      "id": 2639716187,
      "title": "Подставки",
      "description": "Подставки с рекламой,  в наборе 17 штук.",
      "cost": 30000,
      "quantity": 1,
      "breadcrumbs": [
        {
          "name": "Москва"
        },
        {
          "name": "Хобби и отдых"
        },
      ],
      "dimensions": {
        "accuracy": "APPROXIMATE",
        "values": [
          40,
          15,
          30
        ]
      },
      "weight": {
        "accuracy": "APPROXIMATE",
        "value": 1000
      },
      "imagesUrls": {
        "listing": "//01-img-staging-proxy.k.avito.ru/image/1/1.3D5hCra-cNdXo7LSVQnoRGUFohLVqXbT1Sl4FdCpdN_VoXI.4Q-_IforWBTgJ_4VUeJcI9o4Vj4p2CBZPZbcP7ISH0s",
        "list": [
          "//01-img-staging-proxy.k.avito.ru/image/1/1.3D5hCra-cNdXo7LSVQnoRGUFohLVqXbT1Sl4FdCpdN_VoXI.4Q-_IforWBTgJ_4VUeJcI9o4Vj4p2CBZPZbcP7ISH0s"
        ]
      }
    }
  ],
  "sender": {
    "type": "PRIVATE",
    "phones": [
      "79999999999"
    ],
    "email": "email4321@avito-test.ru",
    "name": "Иванов Иван",
    "delivery": {
      "type": "TERMINAL",
      "terminal": {
        "provider": "logsis",
        "id": "117525",
        "accuracy": "APPROXIMATE"
      },
      "completenessAndIntegrity": [
        "DIRECT_FLOW",
        "RETURN_FLOW"
      ]
    }
  },
  "receiver": {
    "type": "3PL",
    "phones": [
      "8-800-600-00-01"
    ],
    "email": "email@russianpost.ru",
    "name": "ООО Почта России",
    "delivery": {
      "type": "SORTING_CENTER",
      "sortingCenter": {
        "provider": "pochta",
        "id": "109316",
        "accuracy": "EXACT"
      }
    }
  },
  "payment": {
    "items": {
      "status": "PAID",
      "cost": 30000
    },
    "delivery": {
      "status": "PAID",
      "costWithoutVat": 10000
    }
  },
  "options": {
    "return": {
      "refused": {
        "action": "DISABLED"
      },
      "unclaimed": {
        "action": "DESTROY",
        "after": {
          "unit": "DAY",
          "value": 7
        }
      }
    },
    "tags": [
      "X_DELIVERY",
      "X_DELIVERY_FIRST_LEG",
      "C2C"
    ]
  }
}
```

</details>

<details>
<summary>Пример запроса на создание PARCEL 2</summary>

```json
{
  "orderID": "37476980088635974",
  "parcelID": "P00037989",
  "barcodes": [
    "000020335046100001"
  ],
  "items": [
    {
      "id": 2639716187,
      "title": "Подставки",
      "description": "Подставки с рекламой,  в наборе 17 штук.",
      "cost": 30000,
      "quantity": 1,
      "breadcrumbs": [
        {
          "name": "Москва"
        },
        {
          "name": "Хобби и отдых"
        }
      ],
      "dimensions": {
        "accuracy": "APPROXIMATE",
        "values": [
          40,
          15,
          30
        ]
      },
      "weight": {
        "accuracy": "APPROXIMATE",
        "value": 1000
      },
      "imagesUrls": {
        "listing": "//01-img-staging-proxy.k.avito.ru/image/1/1.3D5hCra-cNdXo7LSVQnoRGUFohLVqXbT1Sl4FdCpdN_VoXI.4Q-_IforWBTgJ_4VUeJcI9o4Vj4p2CBZPZbcP7ISH0s",
        "list": [
          "//01-img-staging-proxy.k.avito.ru/image/1/1.3D5hCra-cNdXo7LSVQnoRGUFohLVqXbT1Sl4FdCpdN_VoXI.4Q-_IforWBTgJ_4VUeJcI9o4Vj4p2CBZPZbcP7ISH0s"
        ]
      }
    }
  ],
  "sender": {
    "type": "3PL",
    "phones": [
      "8-800-100-00-00"
    ],
    "email": "logsis@logsis.ru",
    "name": "ООО Логсис",
    "delivery": {
      "type": "SORTING_CENTER",
      "sortingCenter": {
        "provider": "pochta",
        "id": "109316",
        "accuracy": "EXACT"
      }
    }
  },
  "receiver": {
    "type": "PRIVATE",
    "phones": [
      "79999999999"
    ],
    "email": "email1234@avito-test.ru",
    "name": "Иванов Иван",
    "delivery": {
      "type": "TERMINAL",
      "terminal": {
        "provider": "pochta",
        "id": "215",
        "accuracy": "EXACT"
      },
      "completenessAndIntegrity": [
        "DIRECT_FLOW"
      ]
    }
  },
  "payment": {
    "items": {
      "status": "PAID",
      "cost": 30000
    },
    "delivery": {
      "status": "PAID",
      "costWithoutVat": 10000
    }
  },
  "options": {
    "return": {
      "receiver": {
        "type": "3PL",
        "phones": [
          "8-800-100-00-00"
        ],
        "email": "logsis@logsis.ru",
        "name": "ООО Логсис",
        "delivery": {
          "type": "SORTING_CENTER",
          "sortingCenter": {
            "provider": "pochta",
            "id": "109316",
            "accuracy": "EXACT"
          },
          "secondPartyLogist": {
            "provider": "logsis"
          }
        }
      },
      "refused": {
        "action": "RETURN_TO_RECEIVER"
      },
      "unclaimed": {
        "action": "RETURN_TO_RECEIVER",
        "after": {
          "unit": "DAY",
          "value": 7
        }
      }
    },
    "tags": [
      "X_DELIVERY",
      "X_DELIVERY_LAST_LEG",
      "C2C"
    ]
  }
}
```

</details>

### Схема движения кросс-доставочных посылок

Посылки PARCEL 1 и PARCEL 2 отражают процесс доставки по своим плечам.

- Плечо 1 – участок пути от отправителя, сдающего посылку в 3PL1, до сортировочного центра 3PL2. На Плече 1
осуществляется переброска посылки от 3PL1 в 3PL2.
- Плечо 2 – участок пути от сортировочного центра 3PL2 до пункта получателя.

На текущий момент Плечо 1 всегда "короткое", а Плечо 2 – "длинное". То есть 3PL1 принимает посылку от отправителя и передает 3PL2 в городе отправителя. А 3PL2 везет посылку из города отправителя в город получателя. В дальнейшем
это может поменяться, и плечи будут строиться по другим алгоритмам.

<img style="max-width:100%" src="https://avito.st/static/ims/b6452be3-ac9a-400a-a604-664f93dda575_fbs_xdelivery_common_direct_flow_common_1445x560.png" />

1. Отправитель относит посылку PARCEL 1 в пункт сдачи 3PL1 PUDO.
2. 3PL1 доставляет свою посылку PARCEL 1 в сортировочный центр 3PL2 sorting center.
3. В 3PL2 sorting center происходит передача посылки от 3PL1 к 3PL2.
4. 3PL2 доставляет свою посылку PARCEL 2 в пункт получения 3PL2 PUDO.
5. Получатель забирает посылку PARCEL 2.

<details>
<summary>Детальная схема доставки</summary>

<img style="max-width:100%" src="https://avito.st/static/ims/3c75ce1f-f00a-46da-91f6-5058cd6e7ac5_direct_detailed_sequence_common_2489x9292.png" />

Замечания по схеме:
- Аналогично С2С-ПВЗ последовательность треков может отличаться у разных посылок, это норма. Где-то может не быть промежуточного
сортировочного центра, где-то их может быть больше одного. Поэтому отправку треков нужно реализовывать, опираясь на
события, которые происходят в реальном мире.
- Обратите внимание, что для PARCEL 1 не нужно присылать трек со статусом `ON_DELIVERY`. Этот статус означает готовность
выдачи посылки получателю, а в кросс-доставке 3PL1 самостоятельно привозит посылку PARCEL 1 получателю 3PL2. 
- Обмер, взвешивание и отправка реального ПВЗ сдачи посылки в кросс-доставке тоже обязательны на всех плечах.
- Подробности по передаче посылки от 3PL1 к 3PL2 см. ниже в соответствующем разделе.
- Подробности по обмену анонсами см. ниже в соответствующем разделе.

</details>

Для реализации кросс-доставки нужно поддержать работу с Avito по методам API:
- [Создание посылки](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/createParcel)
([описание](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/sozdanie_posylki)).
- [Трекинг](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/treking)
([описание](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/treking)).
- [Установка фактического адреса приема посылки](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/setOrderRealAddress).
- [Установка настоящих ВГХ, стоимости доставки посылки](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/setOrderProperties).
- [Запрет приема посылки](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/prohibitOrderAcceptance) 
([описание](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/zapret_priema_posylki)).
- Анонсов ([описание](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/anonsy)):
  - [Создание анонса в Avito](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/CreateAnnouncement).
  - [Создание анонса в СД](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/CreateAnnouncement3PL).
  - [Отмена анонса](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/CancelAnnouncement3PL).
  - [Трекинг анонсов](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/TrackAnnouncement).

> [!IMPORTANT]
> Если переклейка ШК не выполняется на стороне вашей СД, в ответе метода создания посылки в поле `barcode` необходимо передавать ШК предыдущего плеча.

### Передача посылки от 3PL1 к 3PL2
Так как в процессе кросс-доставки участвуют больше двух служб доставок, поэтому где-то должна состояться передача
посылки от одной службы к другой. Сейчас передача происходит между первым и вторым плечами на сортировочном центре 3PL2.

Передача посылки построена на распознавании 3PL2 штрихкодов, наклеенных на коробку посылки предыдущей службой доставки
3PL1.

<img style="max-width:100%" src="https://avito.st/static/ims/a912eb24-7c0c-4dda-b1c5-0f4f27730e8c_lpop_tech_skhema_nakl_ei_ki_shtrikhkodov_na_korobku_i_raspoznavaniya_common_2398x1667.jpeg" />

1. При приеме PARCEL 1 от отправителя 3PL1 наклеивает на коробку свой штрихкод "0001".
2. PARCEL 1 доезжает до сортировочного центра 3PL2, где сотрудник 3PL2 сканирует штрихкод "0001". В момент сканирования
   IT-система 3PL2 должна сообщить, что этому штрихкоду соответствует посылка PARCEL 2.
3. Сотрудник 3PL2 наклеивает на коробку штрихкод "0002".

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/xdelivery-barcodes-handling.png" />

1. Avito создает PARCEL 1 в 3PL1. 3PL1 в ответе возвращает штрихкод, который она будет клеить на коробку посылки.
2. Avito создает PARCEL 2 в 3PL2. В запросе Avito указывает в поле barcodes штрихкод PARCEL 1.
3. 3PL2 запоминает, что PARCEL 2 соответствует штрихкод от 3PL 1.

> [!NOTE]
> Штрихкоды в поле barcodes передаются в порядке, в котором посылки выстроены в логистической цепочке.

Например, при создании возвратной посылки PARCEL 3 в случае агентского возврата, сначала будет указан штрихкод PARCEL 1,
а затем PARCEL 2.

### Возвраты в кросс-доставке

В кросс-доставке возможны как агентские, так и клиентские возвраты. Схема движения обоих типов возвратов предполагает возврат посылки на СЦ 3PL2 в городе отправителя (продавца) и последующий забор посылки со стороны 3PL1 из СЦ 3PL2.

> [!IMPORTANT]
> Для корректной работы как агентских, так и клиентских возвратов критически важно присылать Avito реальные ПВЗ отправки с
> помощью соответствующего [метода](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/setOrderRealAddress).
> 
> Как будет видно далее, все возвраты в кросс-доставке требуют создания новых посылок. При создании новой посылки Avito
> должно указать ПВЗ получения возврата, коим как раз является реальный ПВЗ отправки.

#### Агентский возврат

Агентский возврат в кросс-доставке, как и в простом C2C-ПВЗ сценарии, возможен в случае, если получатель не придет за 
посылкой, и она окажется невостребованной. Или если получатель откажется от посылки в ПВЗ во время предварительного осмотра.

В случае агентского возврата PARCEL 2 должна быть отправлена в пункт, который указан в поле `options.return.receiver`.

В случае отказа или невостребования 3PL2 присылает по PARCEL 2 трек со статусом `IN_TRANSIT_RETURN`.

> [!IMPORTANT]
> Если на возвратном потоке `dispatchNumber`, `trackingNumber` и `barcode` отличаются от прямых, то присылайте новые номера в треке.
> В запросе [метода](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/tracking) под эти нужды
> есть специальные поля в теле запроса.

Это важно потому, что возвратная посылка PARCEL 3 создается при условиях:
- PARCEL 2 развернулась, т.е. перешла в `IN_TRANSIT_RETURN`.
- Пришли новые `dispatchNumber`, `trackingNumber` и `barcode`, если они меняются. Avito на своей стороне "помнит", у каких партнеров
номера меняются. Новый `barcode` мы укажем в запросе на создание PARCEL 3, чтобы работала переброска на возвратном потоке.

Также отметим, что PARCEL 3, будучи "возвратной" посылкой, является невозвратной. То есть в случае невостребования она
не должна уезжать своему отправителю, то есть 3PL2. А должна уезжать, например, на склад временного хранения до
востребования.

##### Примеры запросов на создание посылок

<details>
<summary>Пример запроса на создание агентской PARCEL 3</summary>

```json
{
  "orderID": "37476980088635974",
  "parcelID": "P00037989R",
  "barcodes": [
    "000020335046100001",
    "1000187026762"
  ],
  "items": [
    {
      "id": 2639716187,
      "title": "Подставки",
      "description": "Подставки с рекламой,  в наборе 17 штук.",
      "cost": 30000,
      "quantity": 1,
      "breadcrumbs": [
        {
          "name": "Москва"
        },
        {
          "name": "Хобби и отдых"
        }
      ],
      "dimensions": {
        "accuracy": "APPROXIMATE",
        "values": [
          40,
          15,
          30
        ]
      },
      "weight": {
        "accuracy": "APPROXIMATE",
        "value": 1000
      },
      "imagesUrls": {
        "listing": "//01-img-staging-proxy.k.avito.ru/image/1/1.3D5hCra-cNdXo7LSVQnoRGUFohLVqXbT1Sl4FdCpdN_VoXI.4Q-_IforWBTgJ_4VUeJcI9o4Vj4p2CBZPZbcP7ISH0s",
        "list": [
          "//01-img-staging-proxy.k.avito.ru/image/1/1.3D5hCra-cNdXo7LSVQnoRGUFohLVqXbT1Sl4FdCpdN_VoXI.4Q-_IforWBTgJ_4VUeJcI9o4Vj4p2CBZPZbcP7ISH0s"
        ]
      }
    }
  ],
  "sender": {
    "type": "3PL",
    "phones": [
      "8-800-600-00-01"
    ],
    "email": "email@russianpost.ru",
    "name": "ООО Почта России",
    "delivery": {
      "type": "SORTING_CENTER",
      "sortingCenter": {
        "provider": "pochta",
        "id": "127092",
        "accuracy": "EXACT"
      }
    }
  },
  "receiver": {
    "type": "PRIVATE",
    "phones": [
      "79999999999"
    ],
    "email": "email1234@avito-test.ru",
    "name": "Гедеоныч",
    "delivery": {
      "type": "TERMINAL",
      "terminal": {
        "provider": "logsis",
        "id": "117525",
        "accuracy": "EXACT"
      },
      "completenessAndIntegrity": [
        "DIRECT_FLOW"
      ]
    }
  },
  "payment": {
    "items": {
      "status": "PAID",
      "cost": 30000
    },
    "delivery": {
      "status": "PAID",
      "costWithoutVat": 10000
    }
  },
  "options": {
    "return": {
      "refused": {
        "action": "DESTROY",
        "after": {
          "unit": "DAY",
          "value": 7
        }
      },
      "unclaimed": {
        "action": "DESTROY",
        "after": {
          "unit": "DAY",
          "value": 7
        }
      }
    },
    "tags": [
      "X_DELIVERY",
      "X_DELIVERY_LAST_LEG",
      "RETURN",
      "C2C",
      "PICKUP"
    ]
  }
}
```

</details>

##### Схема движения

<img style="max-width:100%" src="https://avito.st/static/ims/ddc4b6c2-232c-4683-94af-02e633ec09ec_fbs_xdelivery_common_return_agent_flow_common_1952x1060.png" />

1. Отправитель относит посылку PARCEL 1 в ПВЗ сдачи 3PL1 PUDO.
2. 3PL1 доставляет свою посылку PARCEL 1 в сортировочный центр 3PL2 sorting center.
3. В 3PL2 sorting center происходит передача посылки от 3PL1 к 3PL2.
4. 3PL2 доставляет свою посылку PARCEL 2 в ПВЗ получения 3PL2 PUDO.
5. 3PL2 возвращает свою посылку PARCEL 2 в 3PL2 sorting center.
6. 3PL1 забирает возвратную посылку PARCEL 2 и везет свою посылку PARCEL 3 в ПВЗ реальной отправки 3PL1 PUDO.
7. Отправитель забирает возвратную посылку PARCEL 3.

<details>
<summary>Детальная схема доставки</summary>

<img style="max-width:100%" src="https://avito.st/static/ims/387df3f4-7638-4cda-b22a-8e77d89d7ab3_agent_return_detailed_sequence_common_1332x5070.png" />

Замечания по схеме:
- Еще раз обращаем внимание на то, что нужно присылать новые номера по PARCEL 2, если в случае возврата они меняются. Это
  критически важно для создания PARCEL 3 в 3PL1.
- PARCEL 2 едет по возвратным статусам `IN_TRANSIT_RETURN`, `ON_DELIVERY_RETURN`, `RETURNED`. А вот возвратная посылка PARCEL 3 едет уже
  по прямым статусам `IN_TRANSIT`, `ON_DELIVERY` и `DELIVERED`.
- Движение и переброска аналогичны по своей сути прямому потоку.

</details>

#### Клиентский возврат

Клиентский возврат инициирует получатель после того, как посылка ему была выдана. Возможностью клиентского возврата
управляет Avito, позволяя или не позволяя получателю инициировать создание новой возвратной посылки.

Клиентские возвраты на текущий момент доступны только в B2C кросс-доставке. Поэтому примеры ниже содержат B2C-теги.

Клиентские возвратные посылки PARCEL 3 и PARCEL 4 точно также – "невозвратные".

##### Примеры запросов на создание посылок

<details>
<summary>Пример запроса на создание "клиентской" PARCEL 3</summary>

```json
{
  "orderID": "37476980088635974",
  "parcelID": "P00037989R",
  "barcodes": [
    "000020335046100001",
    "1000187026762"
  ],
  "items": [
    {
      "id": 2639716187,
      "title": "Подставки",
      "description": "Подставки с рекламой,  в наборе 17 штук.",
      "cost": 30000,
      "quantity": 1,
      "breadcrumbs": [
        {
          "name": "Москва"
        },
        {
          "name": "Хобби и отдых"
        }
      ],
      "dimensions": {
        "accuracy": "APPROXIMATE",
        "values": [
          40,
          15,
          30
        ]
      },
      "weight": {
        "accuracy": "APPROXIMATE",
        "value": 1000
      },
      "imagesUrls": {
        "listing": "//01-img-staging-proxy.k.avito.ru/image/1/1.3D5hCra-cNdXo7LSVQnoRGUFohLVqXbT1Sl4FdCpdN_VoXI.4Q-_IforWBTgJ_4VUeJcI9o4Vj4p2CBZPZbcP7ISH0s",
        "list": [
          "//01-img-staging-proxy.k.avito.ru/image/1/1.3D5hCra-cNdXo7LSVQnoRGUFohLVqXbT1Sl4FdCpdN_VoXI.4Q-_IforWBTgJ_4VUeJcI9o4Vj4p2CBZPZbcP7ISH0s"
        ]
      }
    }
  ],
  "sender": {
    "type": "PRIVATE",
    "phones": [
      "79999999999"
    ],
    "email": "email4321@avito-test.ru",
    "name": "Иванов Иван Иванович",
    "delivery": {
      "type": "TERMINAL",
      "terminal": {
        "provider": "pochta",
        "id": "215",
        "accuracy": "APPROXIMATE"
      },
      "completenessAndIntegrity": [
        "DIRECT_FLOW"
      ]
    }
  },
  "receiver": {
    "type": "3PL",
    "phones": [
      "8-800-100-00-00"
    ],
    "email": "logsis@logsis.ru",
    "name": "ООО Логсис",
    "delivery": {
      "type": "SORTING_CENTER",
      "sortingCenter": {
        "provider": "pochta",
        "id": "127092",
        "accuracy": "EXACT"
      }
    }
  },
  "payment": {
    "items": {
      "status": "PAID",
      "cost": 30000
    },
    "delivery": {
      "status": "PAID",
      "costWithoutVat": 10000
    }
  },
  "options": {
    "return": {
      "refused": {
        "action": "DISABLED"
      },
      "unclaimed": {
        "action": "DESTROY",
        "after": {
          "unit": "DAY",
          "value": 14
        }
      }
    },
    "tags": [
      "X_DELIVERY",
      "X_DELIVERY_FIRST_LEG",
      "RETURN",
      "B2C"
    ]
  }
}
```

</details>

<details>
<summary>Пример запроса на создание "клиентской" PARCEL 4</summary>

```json
{
  "orderID": "37476980088635974",
  "parcelID": "P00037989R",
  "barcodes": [
    "000020335046100001",
    "1000187026762"
  ],
  "items": [
    {
      "id": 2639716187,
      "title": "Подставки",
      "description": "Подставки с рекламой,  в наборе 17 штук.",
      "cost": 30000,
      "quantity": 1,
      "breadcrumbs": [
        {
          "name": "Москва"
        },
        {
          "name": "Хобби и отдых"
        }
      ],
      "dimensions": {
        "accuracy": "APPROXIMATE",
        "values": [
          40,
          15,
          30
        ]
      },
      "weight": {
        "accuracy": "APPROXIMATE",
        "value": 1000
      },
      "imagesUrls": {
        "listing": "//01-img-staging-proxy.k.avito.ru/image/1/1.3D5hCra-cNdXo7LSVQnoRGUFohLVqXbT1Sl4FdCpdN_VoXI.4Q-_IforWBTgJ_4VUeJcI9o4Vj4p2CBZPZbcP7ISH0s",
        "list": [
          "//01-img-staging-proxy.k.avito.ru/image/1/1.3D5hCra-cNdXo7LSVQnoRGUFohLVqXbT1Sl4FdCpdN_VoXI.4Q-_IforWBTgJ_4VUeJcI9o4Vj4p2CBZPZbcP7ISH0s"
        ]
      }
    }
  ],
  "sender": {
    "type": "3PL",
    "phones": [
      "8-800-600-00-01"
    ],
    "email": "client@russianpost.ru",
    "name": "ООО Почта России",
    "delivery": {
      "type": "SORTING_CENTER",
      "sortingCenter": {
        "provider": "pochta",
        "id": "127092",
        "accuracy": "EXACT"
      }
    }
  },
  "receiver": {
    "type": "LEGAL",
    "phones": [
      "72002378003"
    ],
    "email": "ooo_romashka@avito-test.ru",
    "name": "ООО Ромашка",
    "delivery": {
      "type": "TERMINAL",
      "terminal": {
        "provider": "logsis",
        "id": "109012",
        "accuracy": "EXACT"
      },
      "completenessAndIntegrity": [
        "DIRECT_FLOW"
      ]
    }
  },
  "payment": {
    "items": {
      "status": "PAID",
      "cost": 30000
    },
    "delivery": {
      "status": "PAID",
      "costWithoutVat": 10000
    }
  },
  "options": {
    "return": {
      "refused": {
        "action": "DESTROY",
        "after": {
          "unit": "DAY",
          "value": 14
        }
      },
      "unclaimed": {
        "action": "DESTROY",
        "after": {
          "unit": "DAY",
          "value": 14
        }
      }
    },
    "tags": [
      "X_DELIVERY",
      "X_DELIVERY_LAST_LEG",
      "RETURN",
      "B2C"
    ]
  }
}
```

</details>

##### Схема движения

<img style="max-width:100%" src="https://avito.st/static/ims/c66eac2a-3ac9-43f4-9b16-45b802b15654_fbs_xdelivery_common_client_return_flow_common_2114x1158.png" />

1. Отправитель относит посылку PARCEL 1 в ПВЗ сдачи 3PL1 PUDO.
2. Посылка едет в сортировочный центр 3PL2 sorting center, где происходит переброска от 3PL1 к 3PL2.
3. PARCEL 2 едет из 3PL2 sorting center в ПВЗ получения 3PL2 PUDO.
4. Получатель приходит, проверяет PARCEL 2 и забирает ее
5. Получатель проверяет посылку и решает вернуть ее.
6. PARCEL 3 едет из ПВЗ получения 3PL2 PUDO в сортировочный центр 3PL2 sorting center, где происходит переброска от 3PL2 к 3PL1.
7. PARCEL 4 едет из сортировочного центра 3PL2 в изначальный ПВЗ отправителя 3PL1 PUDO.
8. Отправитель забирает возврат.

<details>
<summary>Детальная схема доставки</summary>

<img style="max-width:100%" src="https://avito.st/static/ims/b1f0cda9-0042-4ee8-8234-bd85d41af7a7_client_return_detailed_sequence_common_2645x10914.png" />

Замечания по схеме:
- Несмотря на то, что PARCEL 3 и PARCEL 4 – возвратные, они едут по прямым статусам `IN_TRANSIT`, `ON_DELIVERY` и `DELIVERED`.
- Движение и переброска аналогичны по своей сути прямому потоку.
- Отказ от возврата не стали отображать на схеме, чтобы её не загромождать. Здесь действия аналогичны C2C-ПВЗ.

</details>

### Трекинг кросс-доставочных посылок
Трекинг кросс-доставочных посылок несколько отличается от обычного трекинга: 
1. На первом плече 3PL1 не должна отправлять трек `ON_DELIVERY`.
2. На возвратном движении 3PL2 должна отправить трек `ON_DELIVERY_RETURN` (`ON_DELIVERY` в случае клиентского возврата) в тот момент, когда посылка готова к выдаче на СЦ 3PL2.

Cхемы трекинга подробно отражены на детализированных схемах доставки, приведенных ранее для каждого сценария.

Схема движения посылок по статусам в случае успешной выдачи:

<img style="max-width:100%" src="https://avito.st/static/ims/9b989df2-c5f4-405a-a13b-6068279726c2_lpop_tech_skhema_dvizheniya_posylok_po_statusam_v_sluchae_uspeshnoi_vydachi_common_3791x1054.jpeg" />

Схема движения посылок по статусам в случае агентского возврата:

<img style="max-width:100%" src="https://avito.st/static/ims/42cd0cb5-5fda-4d10-9ccb-7386bdb962e2_lpop_tech_skhema_dvizheniya_posylok_po_st_atusam_v_sluchae_agentskogo_vozvrata_common_3830x1044.jpeg" />

Схема движения посылок по статусам в случае клиентского возврата:

<img style="max-width:100%" src="https://avito.st/static/ims/c0fd350f-4324-42a7-95c7-7ac8ea6297fc_lpop_tech_skhema_dvizheniya_posylok_po_statusam_v_sluchae_klientsko_go_vozvrata_common_3507x1140.jpeg" />

### Теги в кросс-доставочных посылках
Кросс-доставочные посылки помечаются в запросах специальными тегами:

- `X_DELIVERY`. Означает, что посылка кросс-доставочная.
- `X_DELIVERY_FIRST_LEG`. Означает, что отправитель этой посылки – реальный конечный клиент. Это всегда продавец, исключение - клиентский возврат.
- `X_DELIVERY_LAST_LEG`. Означает, что получатель этой посылки – реальный конечный клиент. Это всегда покупатель, исключение - клиентский возврат.

### Загрузка сортировочных центров
TO BE described.

## Анонсы
#### Термины и сокращения
- Грузоместо – скомплектованный набор из нескольких посылок, который является логистической сущностью, имеет
соответствующую маркировку (идентификатор) и пломбу, может представлять собой мешок, коробку или паллет.
- Первичная приемка – приемка по грузоместам.
- Вторичная приемка – приемка по посылкам.
- Анонс – список подготовленных к передаче в службу доставки следующего плеча посылок, сформированных в грузоместа,
передаваемый в утвержденном json формате между участниками инфообмена.

#### Описание
Зачем нужны анонсы:
- Для информирования службы доставки следующего плеча о планируемой передаче посылок Avito.
- Сделать процесс передачи посылок между СД более прозрачным для всех сторон.
- Ускорить время реакции на возможные инциденты при передаче посылок между службами доставки, за счет сверки статусов
  посылок заявленных в анонсе.

Типы анонсов:
- `DELIVERY`: анонс о доставке посылок отправителем (sender) получателю (receiver).
- `PICKUP`: анонс о готовности отправителя (sender) передать посылки получателю (receiver), получатель должен забрать посылки сам.

> [!NOTE]
> Для лучшего понимания, что из себя представляет анонс, предлагаем внимательно посмотреть на метод создания анонса в API, предоставляемым Avito: [OpenAPI-описание метода создания анонса](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/CreateAnnouncement).


### Схемы взаимодействия
#### Передача посылок из 3PL1 в 3PL2

<details>
<summary>Детальная схема передачи посылок</summary>
<img style="max-width:100%" src="https://avito.st/static/ims/af7dec7a-b80d-4972-8fb9-db3ed2b39106_direct_flow_exchange_with_delivery_announcement_common_1117x1800.png" />
</details>

1. 3PL1 в своем СЦ собирает посылки, которые предназначены для передачи на СЦ 3PL2. Посылки комплектуются в грузоместа.
   Скомплектованные грузоместа загружаются в ТС для доставки посылок в 3PL2.
2. 3PL1 формирует список грузомест, которые были фактически загружены в ТС и готовы к отгрузке, и
   отправляет в Avito по API 3PL интеграции этот список в виде DELIVERY-анонса. В DELIVERY-анонсе помимо информации по запланированным к отгрузке
   посылкам должна быть информация откуда и куда будет доставлен заявленный анонс.
3. Avito отправляет, полученный анонс по API интеграции в 3PL2, которая была указана, как получатель анонса.
4. 3PL2 ожидает заявленной в DELIVERY-анонсе партии посылок. По факту приезда транспортного средства от службы доставки
   предыдущего плеча, осуществляется первичная приемка по грузоместам.
5. 3PL1 отправляет в Avito по API 3PL интеграции трек по анонсу, что анонс доставлен.
6. 3PL1 отправляет в Avito треки по доставленным посылкам.
7. 3PL2 отправляет в Avito по API 3PL интеграции трек по анонсу, что анонс получен.
8. 3PL2 осуществляет вторичную приемку по посылкам. По принятым посылкам в Avito по API 3PL интеграции отправляется трек
   статус, что посылка принята. 
9. После вторичной приемки всех посылок, 3PL2 отправляет в Avito по API 3PL интеграции трек статус по анонсу, что
   вторичная приемка посылок по анонсу завершена.

#### Передача посылок из 3PL2 в 3PL1

<details>
<summary>Детальная схема передачи посылок</summary>
<img style="max-width:100%" src="https://avito.st/static/ims/00d443f6-7b3f-4e97-9198-a3310a6eab53_return_flow_exchange_with_pickup_announcement_common_1314x1915.png" />
</details>

1. 3PL2 в своем СЦ собирает посылки, которые предназначены для передачи на СЦ 3PL2. Посылки комплектуются в грузоместа.
2. 3PL2 отправляет в Avito треки по посылкам, готовым к отгрузке в 3PL1.
3. 3PL2 формирует список грузомест, которые готовы к отгрузке, в виде PICKUP-анонса и
   отправляет анонс в Avito по API 3PL интеграции. В PICKUP-анонсе помимо информации по запланированным к отгрузке
   посылкам должна быть информация откуда и кем должен быть забран анонс.
3. Avito отправляет, полученный анонс по API интеграции в 3PL2, которая была указана, как получатель анонса.
4. 3PL1 ожидает заявленной в PICKUP-анонсе партии посылок. По факту приезда транспортного средства 3PL1, осуществляется первичная приемка по грузоместам на СЦ 3PL2.
5. 3PL2 отправляет в Avito по API 3PL интеграции трек по анонсу, что анонс доставлен.
6. 3PL2 отправляет в Avito треки по доставленным посылкам.
7. 3PL1 отправляет в Avito по API 3PL интеграции трек по анонсу, что анонс получен.
8. 3PL1 осуществляет вторичную приемку по посылкам. По принятым посылкам в Avito по API 3PL интеграции отправляется трек
   статус, что посылка принята.
9. После вторичной приемки всех посылок, 3PL1 отправляет в Avito по API 3PL интеграции трек статус по анонсу, что
   вторичная приемка посылок по анонсу завершена.

#### Отмена анонсов

Для упрощения схемы инфообмена, мы не предусматриваем возможности редактирования и корректировки уже отправленных
(созданных) анонсов. При этом мы закладываем возможность отмены анонса. Если 3PL1 после отправки анонса в
Avito понимает, что анонс не будет исполнен (например ТС сошло с маршрута) или анонс требует корректировок (например,
выявлено, что заявленный анонс не соответствует фактически отправляемым грузоместам и посылкам), то 3PL должна
отправить в Avito по [методу API](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/TrackAnnouncement) трек по анонсу, что анонс отменен. И в случае необходимости создать новый
анонс с актуальными данными, сгенерировав новый идентификатор анонса.

Резюме:
1. 3PL1 или 3PL2 отправляет в Avito по API 3PL интеграции трек статус по анонсу, что анонс отменен.
2. Avito отправляет запрос по API интеграции в 3PL2 или 3PL1 соответственно, который информирует, что переданный ей ранее анонс отменен.

> [!IMPORTANT]
> Не допускается отмена анонса после получения трек статусов по анонсу, что анонс доставлен, получен или по анонсу
> произведена вторичная приемка.

### Методы API на стороне Avito

#### Метод создания анонса /delivery/announcements/create

[OpenAPI-описание метода создания анонса](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/CreateAnnouncement).

Анонс содержит список грузомест. В случае, когда грузоместо состоит из нескольких посылок, API предоставляет возможность задать номер пломбы для грузоместа, идентификатор грузоместа (штрихкод, наклеенный на грузоместо) и список посылок, входящих в это грузоместо. Если же грузоместо состоит из одной посылки, предполагается, что дополнительной упаковки нет, и в таком случае не требуется передавать номер пломбы, в качестве идентификатора грузоместа следует передавать штрихкод единственной посылки.

Контракты анонсов одинаковы для 'DELIVERY' и 'PICKUP' анонсов.

<details>
<summary>Пример запроса на создание анонса в Avito на прямом потоке </summary>

```json
{
  "announcementID": "317ed882-0565-4267-8f66-210ee4b31fef",
  "barcode": "77778828991978",
  "sender": {
    "type": "3PL",
    "name": "ООО Логсис",
    "phones": [
      "8-800-300-00-00"
    ],
    "email": "mail@logsis.ru",
    "delivery": {
      "type": "SORTING_CENTER",
      "sortingCenter": {
        "provider": "logsis",
        "id": "399201",
        "accuracy": "EXACT"
      }
    }
  },
  "receiver": {
    "type": "3PL",
    "name": "ООО СДЭК",
    "phones": [
      "8-800-200-00-00"
    ],
    "email": "mail@cdek.ru",
    "delivery": {
      "type": "SORTING_CENTER",
      "sortingCenter": {
        "provider": "cdek",
        "id": "3710",
        "accuracy": "EXACT"
      }
    }
  },
  "announcementType": "DELIVERY",
  "date": "2025-05-20T09:30:00.52Z",
  "packages": [
    {
      "id": "00001234567890",
      "sealID": "1234-5678",
      "parcelIDs": [
        "P000123",
        "P000124"
      ]
    },
    {
      "id": "00001234567891",
      "parcelIDs": [
        "P000125",
        "P000126"
      ]
    },
    {
      "id": "00001234567892",
      "parcelIDs": [
        "P000127"
      ]
    }
  ]
}

```
- `announcementID` \– UUID V4 идентификатор анонса, генерируется на стороне инициатора анонса (3PL1).
- `barcode` \– уникальный штрихкод анонса. Должен быть напечатан на бумажных сопроводительных документах (акте
приема-передачи). Данный штрихкод необходимо использовать для установки соответствия принимаемой партии
грузомест/посылок с анонсом переданным в электронном виде через инфообмен.
- `sender` \– данные об отправителе анонса (3PL1). Откуда будут отправлены грузоместа с посылками.
- `receiver` \– данные получателя анонса (3PL2). Куда будут доставлены грузоместа с посылками.
- announcementType \– тип анонса DELIVERY - означает анонс о доставке посылок от отправителя (3PL1) получателю (3PL2),
где доставку осуществляет отправитель анонса (3PL1).
- `date` \– дата и время создания анонса в формате RFC 3339 в UTC.
- `packages` \– список грузомест. Грузоместо имеет свой идентификатор `id` штрихкода, идентификатор пломбы `sealID` и список
идентификаторов посылок Avito `parcelIDs`. Поле `sealID` опционально и может отсутствовать в случае, когда посылка
является грузоместом (например, когда габариты посылки не позволяют упаковать ее в мешок и поставить пломбу). В данном
случае в поле id в качестве идентификатора грузоместа необходимо передать штрихкод посылки.

</details>

<details>
<summary>Пример запроса на создание анонса в Avito на возвратном потоке </summary>

```json
{
  "announcementID": "319ed882-0565-4267-8f66-210ee4b31fef",
  "barcode": "77778828991979",
  "sender": {
    "type": "3PL",
    "name": "ООО СДЭК",
    "phones": [
      "8-800-200-00-00"
    ],
    "email": "mail@cdek.ru",
    "delivery": {
      "type": "SORTING_CENTER",
      "sortingCenter": {
        "provider": "cdek",
        "id": "3710",
        "accuracy": "EXACT"
      }
    }
  },
  "receiver": {
    "type": "3PL",
    "name": "ООО Логсис",
    "phones": [
      "8-800-300-00-00"
    ],
    "email": "mail@logsis.ru",
    "delivery": {
      "type": "SORTING_CENTER",
      "sortingCenter": {
        "provider": "logsis"
      }
    }
  },
  "announcementType": "PICKUP",
  "date": "2025-05-20T09:30:00.52Z",
  "packages": [
    {
      "id": "00001234567893",
      "parcelIDs": [
        "P000127"
      ]
    }
  ]
}

```
- `announcementID` \– UUID V4 идентификатор анонса, генерируется на стороне инициатора анонса (3PL1).
- `barcode` \– уникальный штрихкод анонса. Должен быть напечатан на бумажных сопроводительных документах (акте
  приема-передачи). Данный штрихкод необходимо использовать для установки соответствия принимаемой партии
  грузомест/посылок с анонсом переданным в электронном виде через инфообмен.
- `sender` \– данные об отправителе анонса (3PL1). Откуда будут отправлены грузоместа с посылками.
- `receiver` \– данные получателя анонса (3PL2). Куда будут доставлены грузоместа с посылками.
- announcementType \– тип анонса DELIVERY - означает анонс о доставке посылок от отправителя (3PL1) получателю (3PL2),
  где доставку осуществляет отправитель анонса (3PL1).
- `date` \– дата и время создания анонса в формате RFC 3339 в UTC.
- `packages` \– список грузомест. Грузоместо имеет свой идентификатор `id` штрихкода, идентификатор пломбы `sealID` и список
  идентификаторов посылок Avito `parcelIDs`. Поле `sealID` опционально и может отсутствовать в случае, когда посылка
  является грузоместом (например, когда габариты посылки не позволяют упаковать ее в мешок и поставить пломбу). В данном
  случае в поле id в качестве идентификатора грузоместа необходимо передать штрихкод посылки.

</details>

> [!IMPORTANT]
> В поле `receiver.delivery.sortingCenter.provider` указывается СД, выступающая получателем. Тег СД передаётся в методе создания посылки.

#### Метод трекинга анонса /delivery/announcements/track

OpenAPI-описание метода [здесь](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/TrackAnnouncement).

<details>
<summary>Пример запроса на трекинг анонса</summary>

```json
{
  "announcementID": "55fefb84-fa30-47ee-bf29-9c860823ea79",
  "date": "2023-09-20T10:00:00.52Z",
  "event": "ACCEPTANCE_DONE"
}
```

- announcementID - UUID V4 идентификатор анонса, по которому передается события трекинга.
- date - дата и время события в формате RFC 3339 в UTC, ожидаем реальное время, когда произошло событие, а не время
  отправки трека.
- event - событие, которое произошло по анонсу.

</details>

Возможные события по анонсу:
События, которые может передавать служба доставки инициатор анонса:

- `CANCELLED`. Анонс отменен и исполнен не будет. Отмена анонса возможна, до получения события DELIVERED или событий по
  первичной/вторичной приемке от 3PL2.
- `DELIVERED`. Анонс был доставлен в 3PL2.

События, которые может передавать СД-получатель посылок по анонсу:

- `RECEIVED`. По анонсу была произведена первичная приемка.
- `ACCEPTANCE_DONE`. По анонсу была произведена вторичная приемка.

#### Обработка ответов

<details>
<summary>Пример ответа</summary>

```json
{
  "data": {
    "status": "success"
  }
}
```

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Текст ошибки"
  }
}
```

</details>

В случае успешного выполнения запроса метод вернет HTTP-код 200 с объектом `data` и успешным статусом.

Если при создании анонса произошла ошибка бизнес-логики (например анонс с переданным идентификатором уже создан) метод
вернет HTTP-код 200 с объектом `error`, где будет указан код ошибки и ее текстовое описание.

Возможные коды ошибок и рекомендованная реакция на них представлена ниже (список не окончательный и может
расшириться в ходе реализации системы и тестирования интеграции):

- `VALIDATION_ERROR`. Делать повторный запрос без изменения параметров запроса смысла нет. Для повторного запроса
  необходимо внести корректировки и заполнить все требуемые по спецификации поля.
  Если запрос составлен корректно, но получена ошибка валидации запроса, необходимо сообщить об этом в интеграционном
  чате.
- `ANNOUNCE_ID_EXISTS`. Необходимо сгенерировать новый идентификатор анонса и повторить запрос. Если это повторный
  запрос на создание анонса, то делать ничего не надо.
- `INVALID_PARCELS`. Делать повторный запрос без изменения параметров запроса смысла нет. Ошибка говорит о том, что в
  анонсе заявлены посылки которых нет в системе Avito или они не относятся к СД инициатору анонса. Необходимо проверить
  принадлежность посылок к Avito Доставке и правильность указания идентификаторов.
- `CANCEL_FORBIDDEN`. Необходимо перестать присылать события отмены в трекинг анонса, так как отмена анонса уже
  невозможна.
- `ANNOUNCE_NOT_FOUND`. Делать повторный запрос без изменения параметров запроса смысла нет. Необходимо проверить
  корректность передаваемого идентификатора анонса.
- `INVALID_EVENT`. Делать повторный запрос без изменения параметров запроса смысла нет. Необходимо проверить
  корректность передаваемого события в трекинг анонсов.

При возникновении инфраструктурных ошибок (сетевая ошибка при межсервисном взаимодействии, ошибка доступа к БД) метод
вернет HTTP-код 500 с полем `error`. На данный код ответа необходимо предусмотреть повторные попытки вызова метода с теми
же параметрами. Рекомендуемая политика повторных попыток – раз в 1-5 минут в течение 1 часа.

В случае отсутствия токена авторизации или невалидного токена, метод вернет HTTP-код 401 и 403 соответственно. При
получении данных кодов ответа, необходимо обновить токен авторизации и вставить его в заголовок запроса.

### Методы API на стороне службы доставки, участвующей в инфообмене
Рассмотренные ниже методы должны быть реализованы на стороне службы доставки.

#### Метод получения анонса - /createAnnouncement
[OpenAPI-описание метода](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/CreateAnnouncement3PL).

Нефункциональные требования:
- Максимальное время ответа – 5с.
- Метод должен быть синхронным. Успешный ответ на запрос свидетельствует о том, что запрашиваемая операция выполнена.
- Доступность метода – 99% (за исключением заранее оговоренных регламентных работ).
- Интенсивность запросов, гарантированно не приводящая к деградации - 100 запросов в минуту.
- Размер тела запроса с анонсом на 1000 посылок равен примерно 150 килобайт. Это надо учитывать, если на стороне СД есть
настройки ограничения на размер тела запроса, и закладывать с запасом. Рекомендуем обрабатывать запросы с размером тела
запроса не более 10 мегабайт.
- Обработчик запроса должен быть идемпотентным. В случае повторного запроса на получение анонса, если анонс с переданным
`announcementID` уже был принят, необходимо вернуть HTTP-200 код ответа без ошибки. Не должно происходить обновления
данных в уже принятом анонсе.

<details>
<summary>Пример запроса на создание анонса в СД</summary>

```json
{
  "announcementID": "55fefb84-fa30-47ee-bf29-9c860823ea79",
  "barcode": "00009876543210",
  "sender": {
    "type": "3PL",
    "name": "ExMail",
    "phones": [
      "8-800-200-00-00"
    ],
    "email": "mail@exmail.ru",
    "delivery": {
      "type": "SORTING_CENTER",
      "sortingCenter": {
        "provider": "exmail",
        "id": "010",
        "accuracy": "EXACT"
      }
    }
  },
  "receiver": {
    "type": "3PL",
    "name": "Почта России",
    "phones": [
      "8-800-300-00-00"
    ],
    "email": "mail@pochta.ru",
    "delivery": {
      "type": "SORTING_CENTER",
      "sortingCenter": {
        "provider": "pochta",
        "id": "19310",
        "accuracy": "EXACT"
      }
    }
  },
  "announcementType": "DELIVERY",
  "date": "2023-09-20T10:00:00.52Z",
  "packages": [
    {
      "id": "00001234567890",
      "sealID": "1234-5678",
      "parcels": [
        {
          "id": "P000777",
          "barcode": "000012345",
          "senderID": "P000776",
          "senderBarcode": "123450000"
        }
      ]
    }
  ]
}
```

Параметры запроса аналогичны методу создания анонса на стороне Avito, который рассмотрен выше. Основное отличие
заключается в том, что внутри объекта описывающего грузоместо, посылки представлены не списком идентификаторов, а
представляют собой список объектов внутри которых есть поля:

- id - идентификатор посылки Avito в системе получателя анонса (3PL2).
- barcode - штрихкод посылки в системе получателя анонса (3PL2).
- senderID - идентификатор посылки Avito в системе инициатора анонса (3PL1).
- senderBarcode - штрихкод посылки в системе инициатора анонса (3PL1).

</details>

> [!IMPORTANT]
> Ниже перечислены возможные корнер-кейсы, которые необходимо учитывать при реализации метода /createAnnouncement и 
> уметь обрабатывать. Обратите на них пристальное внимание. В описании корнер-кейсов участвуют стейкхолдеры 3PL1 и 3PL2,
> именование, в данном контексте, означает, что 3PL1 - сторона отправляющая анонс, 3PL2 - сторона принимающая анонс. Корнер-кейсы, если это 
> не оговорено явно, имеют место как на прямом движении, так и на возвратном.

1\. В анонсе может быть заявлено грузоместо или посылка, которая по каким-то причинам фактически не была отгружена в
3PL2. При обнаружении такой ситуации или после разбора инцидента 3PL1 может подготовить к отгрузке выявленную
недостачу и заявить в новом анонсе совместно со следующей партией грузомест и посылок, при этом не меняя маркировку
грузоместа.

Исходя из этого, необходимо предусмотреть, что грузоместа и посылки с одинаковыми идентификаторами могут быть заявлены в
нескольких анонсах.

2\. В случае, когда посылка передается без грузоместа, т.е. посылка сама по себе является грузоместом, то объект с
данными по такой посылке в массиве packages будет выглядеть следующим образом:

<details>
<summary>Пример</summary>

```json
{
  "packages": [
    {
      "id": "123450000",
      "parcels": [
        {
          "id": "P000777",
          "barcode": "000012345",
          "senderID": "P000776",
          "senderBarcode": "123450000"
        }
      ]
    }
  ]
}
```

</details>

В поле id грузоместа будет передан штрих-код посылки первого плеча, значение которого будет продублировано в поле
senderBarcode. Поле sealID будет отсутствовать.

Необходимо это учесть, чтобы при первичной и вторичной приемке при сканировании ШК посылки была возможность сопоставить
данную посылку с данными по грузоместам и посылкам в анонсе.

3\. Возможна ситуация, когда 3PL1 подготовит к передаче в 3PL2 и заявит в анонсе посылку, которая не
была зарегистрирована как посылка следующего плеча в 3PL2.

Это может произойти если:
- Не был передан терминал сдачи посылки.
- Терминал сдачи посылки не работает на выдачу или закрыт.
- Ошибка при расчете маршрута.
- Ошибка при попытке зарегистрировать посылку в СД.

Проблемы с регистрацией таких посылок обрабатываются вручную, поэтому есть вероятность, что на момент получения анонса
посылка все еще может быть не зарегистрирована. В данном случае мы будем вынуждены передавать в анонсе по
таким посылкам пустые поля id и barcode для объекта в массиве parcels.

<details>
<summary>Пример объекта в массиве packages в запросе</summary>

```json
{
  "packages": [
    {
      "id": "00001234567890",
      "sealID": "1234-5678",
      "parcels": [
        {
          "id": "",
          "barcode": "",
          "senderID": "P000776",
          "senderBarcode": "123450000"
        }
      ]
    }
  ]
}
```

</details>

Необходимо регламентировать процесс вторичной приемки таких посылок и запускать процесс обработки по флоу проблемы
идентификации.

4\. 3PL1 может ошибочно заявить в анонсе и фактически отгрузить в 3PL2 посылки которые не относятся к Avito или
предназначены для другого 3PL. Такие посылки будут представлены в анонсе пересылаемом в 3PL2 в том же виде, как п. 3.
без указания id и barcode посылки в 3PL2.

#### Метод отмены анонса - /cancelAnnouncement
OpenAPI-описание метода [здесь](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/CancelAnnouncement3PL).

Метод отмены анонса предназначен для информирования 3PL2, что ожидать доставки по ранее переданному анонсу не надо, и
носит уведомительный характер.

Нефункциональные требования:
- Максимальное время ответа – 3с.
- Метод должен быть синхронным. Успешный ответ на запрос свидетельствует о том, что запрашиваемая операция выполнена.
- Доступность метода – 99% (за исключением заранее оговоренных регламентных работ).
- Интенсивность запросов, гарантированно не приводящая к деградации - 100 RPM.
- Обработчик запрос должен быть идемпотентным. В случае повторного запроса отмены анонса, если анонс с переданным
`announcementID` уже был отменен, необходимо вернуть HTTP-200 код ответа без ошибки.

<details>
<summary>Пример</summary>

```json
{
  "announcementID": "55fefb84-fa30-47ee-bf29-9c860823ea79",
  "reason": "CANCELED_BY_DELIVERY_PROVIDER"
}
```

Параметры запроса:

- `announcementID` - UUID V4 идентификатор анонса, который необходимо отменить.
- `reason` - опциональное поле с дополнительной информацией об инициаторе отмены. Возможные значения:
  - `CANCELED_BY_DELIVERY_PROVIDER`. Отмена со стороны 3PL1.
  - `CANCELED_BY_AVITO` – отмена со стороны Avito.

</details>

#### Ответы методов

<details>
<summary>Пример</summary>

```json
{
  "data": {
    "status": "success"
  }
}
```

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Текст ошибки"
  }
}
```

</details>

В случае успешного выполнения запроса метод вернет HTTP-код 200 c объектом data и успешным статусом.

#### Обработка ошибок

**HTTP 200**

В случае, если в процессе обработки запроса от Avito произошла какая-то ошибка бизнес-логики, то следует вернуть
HTTP-код 200 с полем `error`.
В теле ответа такой ошибки должен содержаться код ошибки, описанный в спецификации по которому Avito будет понимать
стоит ли отправлять запрос повторно или это не имеет смысла.

Возможные коды ошибок и рекомендованная реакция на них представлена в таблице (список не окончательный и может
расшириться в ходе реализации системы и тестирования интеграции):

- `VALIDATION_ERROR`. Делать повторный запрос без изменения параметров запроса смысла нет. Для повторного запроса
  необходимо внести корректировки и заполнить все требуемые по спецификации поля.
  Если запрос составлен корректно, но получена ошибка валидации запроса, необходимо сообщить об этом в интеграционном
  чате.

Если код ошибки предполагает повтор, то у таких ошибок в спецификации специально будет оговорена стратегия повторных
запросов. Например:

- Раз в 1-5 минут.
- Не более 1 часа с момента первой попытки.

**HTTP 500**

В случае, если в процессе обработки запроса от Avito произошла какая-то непредвиденная ошибка и имеет смысл сделать
повтор, метод должен вернуть HTTP-код 500 с полем error и соответствующим кодом ошибки в теле ответа, если такой есть в
спецификации. Если нет, возвращайте `INTERNAL_SERVER_ERROR`.

Примеры подобных ошибок:

- Сетевая ошибка между внутренними сервисами СД.
- Ошибка выполнения запроса к базе данных.

Оба эти примера объединяет то, что это не ошибки бизнес-логики, а какие-то инфраструктурные проблемы, которые рано или
поздно закончатся, и повторный запрос будет успешным.

На любую 500-ую ошибку Avito будет делать ограниченное количество повторов. На текущий момент стратегия повторов такая (
может меняться без предварительного согласования):

- Раз в 1-5 минут.
- Не более 1 часа с момента первой попытки.

# Создание посылки

## Назначение метода создания посылки
Через API-метод создания посылки Avito сообщает службе доставки:
- Кто будет отправителем;
- Откуда посылка "поедет";
- Кто будет получателем;
- Куда посылка "поедет";
- Что будет в посылке;
- Прочие специфические опции, касающиеся доставки посылки.

> [!IMPORTANT]
> Метод создания посылки имплементируется на стороне службы доставки.
>
> Через один метод создаются посылки с разными свойствами, которые подробно рассматриваются ниже.

## Спецификация метода создания посылки
Спецификация метода API находится [здесь](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/createParcel).

## Обработка ошибок
Напомним, что метод создания посылки реализуется на стороне службы доставки. Поэтому повторные запросы при необходимости будет выполнять Avito.
Политика повторов работает на основе кодов ошибок, которые обработчик метода создания посылки может вернуть.

### HTTP 200
В случае, если в процессе обработки запроса от Avito произошла какая-то ошибка бизнес-логики, то следует вернуть
HTTP-код 200 с полем `error` и соответствующим кодом ошибки в теле ответа.

> [!NOTE]
> Обратите внимание, что внутренние инфраструктурные ошибки не относятся к ошибкам бизнес-логики. Например, если
> у вас внутри не получилось создать посылку, потому что случилась сетевая ошибка, нужно вернуть HTTP-код 500. Подробнее
> про это в разделе "HTTP 500" ниже.

<details>
<summary>Пример ответа с ошибкой</summary>

```json
{
 "error": {
   "code": "TERMINAL_UNAVAILABLE",
   "message": "receiver terminal is permanently closed"
 }
}
```

</details>

Возможные ошибки:
- `VALIDATION_ERROR` – содержимое запроса некорректно. Например, длина товара в посылке превышает допустимые лимиты,
или какое-то обязательное поле отсутствует.
- `UNSUPPORTED_PARAM_ERROR` – в запросе получен неподдерживаемый параметр. Например, вы не поддерживаете кросс-доставку,
а Avito ошибочно пытается у вас создать кросс-доставочную посылку.
- `TERMINAL_UNAVAILABLE` – терминал, указанный в запросе, недоступен для создания посылки. Например, ПВЗ, выбранный
покупателем на момент создания посылки, закрылся навсегда.
- `SORTING_CENTER_UNAVAILABLE` – сортировочный центр, указанный в запросе, недоступен для создания посылки. Это
кросс-доставочная ошибка, которая может возникнуть, когда давно произошла смена сортировочного центра, а Avito по какой-то
продолжает создавать посылки в него. При реализации возврата этой ошибки обязательного проговорите механику
переключения сортировочных центров с инженерами Avito.

> [!IMPORTANT]
> Все перечисленны ошибки – "**терминальные**", т.е. не имеет смысла повторять запрос, так как будет получен такой же результат.
> Получение любой такой ошибки при создании посылки приводит к автоматической отмене соответствующего заказа на Avito,
> поэтому мы внимательно следим за их количеством.
>
> В нормальном режиме таких ошибок совсем не должно быть, или их должно быть исчезающе мало.

### HTTP 500
В случае, если в процессе обработки запроса от Avito произошла какая-то непредвиденная ошибка и имеет смысл сделать повтор,
метод должен вернуть HTTP-код 500 с полем `error` и кодом `INTERNAL_SERVER_ERROR`.

Примеры ошибок, когда нужно вернуть HTTP-код 500 + `INTERNAL_SERVER_ERROR`:
- Сетевая ошибка между вашими внутренними сервисами СД.
- Ошибка выполнения запроса к вашей базе данных.

Оба эти примера объединяет то, что это не ошибки бизнес-логики, а какие-то инфраструктурные проблемы, которые рано или
поздно закончатся, и повторный запрос будет успешным.

На любую 500-ую ошибку Avito делает ограниченное количество повторов. На текущий момент стратегия повторов такая
(может меняться без предварительного согласования):
- Раз в 1 минуту.
- Не более 6 часов с момента первой попытки.

## SLA по методу создания посылки
Этим SLA должен соответствовать ваш обработчик.

- Максимальное время ответа – 5 секунд.
- Интенсивность запросов, гарантированно не приводящая к деградации – 200 RPM (запросы в минуту).
- Доступность метода – 99% (за исключением заранее оговоренных регламентных работ).
- Максимальная запланированная недоступность (в том числе для проведения регламентных работ) – не более 1 раза в неделю
  и не дольше трех часов (требуется заблаговременное согласование времени проведения работ с инженерами Avito – минимум за 3 рабочих дня до проведения работ).

> [!IMPORTANT]
> Метод создания посылки – синхронный. Мы ожидаем, что служба доставки в течение 5 секунд создаст нужные Avito
> dispatchNumber и trackingNumber и вернет их.

## Идемпотентность метода создания посылки

> [!IMPORTANT]
> Ваш обработчик запроса на создание посылки должен быть **[идемпотентным](https://ru.wikipedia.org/wiki/%D0%98%D0%B4%D0%B5%D0%BC%D0%BF%D0%BE%D1%82%D0%B5%D0%BD%D1%82%D0%BD%D0%BE%D1%81%D1%82%D1%8C)**.

Ключом идемпотентности считаем `parcelID`. В случае, если происходит повторная попытка создания посылки
(посылка с таким `parcelID` была успешно создана ранее), то необходимо вернуть HTTP-код 200 без ошибки, а в полях
ответа указать данные ранее созданной посылки.

Пример:
- Avito делает запрос в службу доставки на создание посылки с `parcelID` "P00037988".
- Служба доставки на своей стороне все нужное для создания посылки сделала.
- Служба доставки начинает передавать ответ на запрос.
- В момент передачи ответа на стороне Avito или на стороне службы доставки происходит сетевая ошибка.

Получается, что посылка у службы доставки создана, но Avito об этом не знает – для нас посылка как бы не была создана.
В таком случае Avito сделает повторный запрос на создание посылки с `parcelID` "P00037988", и в этот раз нужно вернуть
уже имеющиеся `dispatchNumber`, `trackingNumber`, `barcodes`, а не создавать новые.

**Когда идемпотентность может быть полезна? От чего она защищает?**

Идемпотентность крайне важна в курьерских сценариях, когда при создании условной посылки на точку забора направляется
настоящий курьер. Если обработчик запроса будет неидемпотентным, то в ситуациях, подобных описанной выше, на точку будет
отправляться N курьеров, а не один.

> [!NOTE]
> Avito гарантирует, что запросы с одним и тем же `parcelID` не будут отправляться в службу доставки с
> задержкой менее 10 секунд.

## Разбор полей запроса
В этом разделе рассказываем про "физический смысл" полей в запросе на создание посылки, и возможные значения
внутри полей.

<details>
<summary>Пример обычного запроса на создание посылки</summary>

```json
{
  "orderID": "37476980088635974",
  "parcelID": "P00037988",
  "items": [
    {
      "id": 2639716187,
      "title": "Подставки",
      "description": "Подставки с рекламой,  в наборе 17 штук.",
      "cost": 30000,
      "quantity": 1,
      "breadcrumbs": [
        {
          "name": "Москва"
        },
        {
          "name": "Хобби и отдых"
        },
        {
          "name": "Коллекционирование"
        },
        {
          "name": "Модели"
        }
      ],
      "dimensions": {
        "accuracy": "APPROXIMATE",
        "values": [
          40,
          15,
          30
        ]
      },
      "weight": {
        "accuracy": "APPROXIMATE",
        "value": 1000
      },
      "imagesUrls": {
        "listing": "//01-img-staging-proxy.k.avito.ru/image/1/1.3D5hCra-cNdXo7LSVQnoRGUFohLVqXbT1Sl4FdCpdN_VoXI.4Q-_IforWBTgJ_4VUeJcI9o4Vj4p2CBZPZbcP7ISH0s",
        "list": [
          "//01-img-staging-proxy.k.avito.ru/image/1/1.3D5hCra-cNdXo7LSVQnoRGUFohLVqXbT1Sl4FdCpdN_VoXI.4Q-_IforWBTgJ_4VUeJcI9o4Vj4p2CBZPZbcP7ISH0s"
        ]
      }
    }
  ],
  "sender": {
    "type": "PRIVATE",
    "phones": [
      "79999999999"
    ],
    "email": "email4321@avito-test.ru",
    "name": "the_best_seller_in_the_world",
    "delivery": {
      "type": "TERMINAL",
      "terminal": {
        "provider": "pochta",
        "id": "117525",
        "accuracy": "APPROXIMATE"
      },
      "completenessAndIntegrity": [
        "DIRECT_FLOW",
        "RETURN_FLOW"
      ]
    }
  },
  "receiver": {
    "type": "PRIVATE",
    "phones": [
      "79999999999"
    ],
    "email": "email1234@avito-test.ru",
    "name": "Иванов Иван Иванович",
    "delivery": {
      "type": "TERMINAL",
      "terminal": {
        "provider": "pochta",
        "id": "119296",
        "accuracy": "EXACT"
      },
      "completenessAndIntegrity": [
        "DIRECT_FLOW"
      ]
    }
  },
  "payment": {
    "items": {
      "status": "PAID",
      "cost": 30000
    },
    "delivery": {
      "status": "PAID",
      "costWithoutVat": 10000
    }
  },
  "options": {
    "return": {
      "refused": {
        "action": "RETURN_TO_DEPARTURE_POINT"
      },
      "unclaimed": {
        "action": "RETURN_TO_DEPARTURE_POINT",
        "after": {
          "unit": "DAY",
          "value": 14
        }
      },
      "returned": {
        "action": "DESTROY",
        "after": {
          "unit": "DAY",
          "value": 14
        }
      }
    },
    "tags": [
      "C2C"
    ]
  }
}
```

</details>

### "orderID"
В этом поле Avito указывает номер **заказа**. Это поле добавлено для будущей реализации многоместности / консолидации.
Сейчас ни то, ни другое не поддерживается, поэтому обрабатывать / использовать это поле пока не нужно.

### "directOrderID"
В этом опциональном поле Avito указывает номер **прямого заказа**. Поле необходимо для случаев частичного возврата для
некоторых служб доставки. Так как в случае частичного возврата создается новое отправление, то для связи с прямым 
службе доставки может понадобиться данное поле. При прямом отправлении поле не передается.

### "parcelID"
Номер посылки. Это главный идентификатор основной сущности, по которой Avito работает со службой доставки по части
процессинга – **посылки**.

Примечания:
- Идентификатор посылки в prod-окружении имеет вид `P00037988`. Его легко узнать по префиксу `P000`.
- В тестовом окружении добавляется префикс `S-`, то есть идентификатор приобретает итоговый вид `S-P00037988`.
- У возвратных посылок есть суффикс `R`. Идентификатор выглядит так `P00037988R`.
- Regexp для идентификатора посылки: `^([A-Z]-)?P[a-zA-Z0-9]{3}(\d{1,16}|\d{1,15}R)$`.

Avito дает гарантию уникальности `parcelID`, т.е. не могут быть созданы разные посылки с одним и тем же идентификатором.
Обратите внимание, что имеем в виду именно **разные** посылки. Повторные запросы на регистрацию уже зарегистрированной
посылки могут приходить, на этот случай ваш обработчик должен быть идемпотентным (см. соответствующий раздел выше).

Идентификатор посылки `parcelID` используется во многих других интеграциях. Например, службы доставки по `parcelID`
присылают треки, реальный ПВЗ сдачи, реальные ВГХ и т.д. Или по `parcelID` Avito просит службу доставки запретить
прием посылки, сменить ФИО, запретить выдачу. Сохраняйте у себя в БД этот идентификатор, чтобы по нему можно было в
дальнейшем работать.

### "barcodes"
Если вам неинтересна кросс-доставка, то раздел можно пропустить и перейти к "items".

В `barcodes` Avito передает штрихкоды других служб доставок, которые относятся к создаваемой посылке. Это нужно для того
чтобы 3PL2 могла связать пришедшую коробку от 3PL1 с посылкой, которую Avito создает этим запросом.

`barcodes` – массив. Это сделано на случай, если коробка посылки в случае каких-либо грядущих сложных схем доставки приедет вся обклеенная штрихкодами.
Чтобы повысить вероятность распознавания посылки приемщиком, Avito передает в запросе все известные штрихкоды.

Подробнее про процесс передачи посылки от 3PL1 к 3PL2 рассказываем в разделе "[Механика работы кросс-доставки](http://localhost:3100/api-catalog/delivery-sandbox/documentation#info/mehanika_raboty_kross-dostavki)".

### "items"
В `items` собрана информация по товарам в посылке.

<details>
<summary>Пример items</summary>

```json
[
  {
    "id": 2639716187,
    "title": "Подставки",
    "description": "Подставки с рекламой,  в наборе 17 штук.",
    "cost": 30000,
    "quantity": 1,
    "breadcrumbs": [
      {
        "name": "Москва"
      },
      {
        "name": "Хобби и отдых"
      },
      {
        "name": "Коллекционирование"
      },
      {
        "name": "Модели"
      }
    ],
    "dimensions": {
      "accuracy": "APPROXIMATE",
      "values": [
        40,
        15,
        30
      ]
    },
    "weight": {
      "accuracy": "APPROXIMATE",
      "value": 1000
    },
    "imagesUrls": {
      "listing": "//01-img-staging-proxy.k.avito.ru/image/1/1.3D5hCra-cNdXo7LSVQnoRGUFohLVqXbT1Sl4FdCpdN_VoXI.4Q-_IforWBTgJ_4VUeJcI9o4Vj4p2CBZPZbcP7ISH0s",
      "list": [
        "//01-img-staging-proxy.k.avito.ru/image/1/1.3D5hCra-cNdXo7LSVQnoRGUFohLVqXbT1Sl4FdCpdN_VoXI.4Q-_IforWBTgJ_4VUeJcI9o4Vj4p2CBZPZbcP7ISH0s"
      ]
    }
  }
]

```

</details>

Обратите внимание, что поле `items` – массив. В посылке может быть несколько единиц одного товара или несколько разных товаров.
Посылки, которые содержат несколько товаров, мы называем "корзинными". У подобных посылок есть свои особенности по
операционной части, их стоит уточнить и согласовать с операционными менеджерами Avito.

> [!IMPORTANT]
> В процессе обработки запроса на создание посылки с несколькими товарами вы должны проверять, что все товары "влезают"
> в одну посылку. Если вы понимаете, что товары из посылки в совокупности превышают максимальный вес или габариты, то
> возвращайте ошибку `VALIDATION_ERROR` с поясняющим текстом.
>
> Обязательно провалидируйте алгоритм, который считает общие габариты товаров, с инженерами Avito. Обращаем внимание, что
> простое сложение измерений товаров в посылке не дает корректные итоговые габариты посылки.

Описание полей элемента из массива `items`:
- `id` – идентификатор товара на Avito.
- `title` – название товара.
- `description` – описание товара.
- `cost` – стоимость одной единицы товара в копейках.
- `quantity` – количество единиц товара.
- `breadcrumbs` – категории товара. Используется для проверки целостности и комплектности посылки.
- `dimensions` – габариты товара.
  - Avito не знает точных габаритов товаров, поэтому в поле `accuracy` мы всегда
    передаем значение `APPROXIMATE`, т.е. указываем на то, что габариты примерные.
  - Габариты передаются в таком порядке: длина, высота, ширина. В случае, если не имеет значения пространственное положение коробки, их можно у себя внутри
    отсортировать от большего к меньшему.
  - Габариты передаются в сантиметрах.
- `weight` – вес товара.
  - Аналогично габаритам Avito не знает точный вес товара, поэтому в поле `accuracy` мы всегда передаем
    значение `APPROXIMATE`.
  - Вес передаем в граммах.
- `imagesUrls` – картинки объявления.
  - Картинки могут отсутствовать, это нормальная ситуация. Реакцию на посылки, в которых
    нет картинок, согласуйте с операционными менеджерами Avito.
  - По умолчанию CDN Avito отдает картинку в webp. При необходимости
    через заголовок 'Accept: image/jpeg' можно запросить в jpeg или png. Вернется картинка либо в jpg, либо в png, это
    зависит от схемы хранения картинки.
- `imagesUrls.listing` – главная картинка.
- `imagesUrls.list` – второстепенные картинки.
- `tags` – дополнительные признаки товара. Признаки товара могут определять дополнительные услуги, оказываемые 
    при приеме или выдаче посылки. На текущий момент поддерживается только один признак - `TRY_ON`, который означает, 
    что возможна примерка в ПВЗ.

> [!IMPORTANT]
> Дополнительные признаки товара влияют на конкретный товар, а не всю посылку. Например, в посылке может быть два товара, 
> один примерять можно, другой нельзя.

### "sender" и "receiver"
Объекты описывают отправителя и получателя посылки. Рассматриваем их вместе, т.к. их структура идентична.

<details>
<summary>Пример части запроса с отправителем</summary>

```json
{
  "sender": {
    "type": "PRIVATE",
    "phones": [
      "79999999999"
    ],
    "email": "email4321@avito-test.ru",
    "name": "the_best_seller_in_the_world",
    "delivery": {
      "type": "TERMINAL",
      "terminal": {
        "provider": "pochta",
        "id": "117525",
        "accuracy": "APPROXIMATE"
      },
      "completenessAndIntegrity": [
        "DIRECT_FLOW",
        "RETURN_FLOW"
      ]
    }
  }
}
```

</details>

`type` – тип отправителя или получателя. Отправителем или получателем посылки могут быть:
- `PRIVATE` – частное физическое лицо.
- `LEGAL` – юридическое лицо (в B2C-доставке).
- `3PL` – служба доставки (в кросс-доставке).

`phones` – список контактных телефонов отправителя / получателя.

> [!IMPORTANT]
> Формат номеров телефонов может быть произвольным. Добавлять блокирующую валидацию на них нельзя.

`email` – электронная почта. Здесь гарантируем корректность формата.

`name` – имя отправителя или получателя. Если клиент – частное лицо, то здесь будет ФИО. Если юридическое лицо или
служба доставки – наименование организации.

> [!IMPORTANT]
> Формат имени отправителя может быть произвольным.
>
> Процесс оформления заказа на Avito устроен таким образом, что только получатель посылки указывает
настоящее и полное ФИО (Avito это контролирует), но ФИО отправителя мы не знаем. Мы знаем его никнейм, который он
> указал при регистрации на сайте.
>
> Добавлять блокирующую на то, что Avito передает в имени отправителя настоящее ФИО нельзя.
>
> В имени отправителя могут быть произвольные символы / эмодзи. Блокировать из-за них создание посылки нельзя.

`delivery` – объект с информацией о доставке. Для отправителя он описывает механику **приема** посылки. Для получателя
описывает механику **выдачи** посылки.

`delivery.type` – тип доставки. Показывает тип терминала из / в который осуществляется доставка. Возможные значения:
- `TERMINAL` – пункт приема или выдачи заказов.
- `SORTING_CENTER` – сортировочный центр (для кросс-доставки).
- `COURIER` – доставка курьером.

Если в `delivery.type` указан `TERMINAL`, то будет заполнен объект `delivery.terminal`, содержащий данные по терминалу.
Если в `delivery.type` указан `COURIER`, то будет заполнен объект `delivery.courier`, содержащий детали курьерской доставки.

<details>
<summary>Пример заполненного терминала</summary>

```json
{
  "type": "TERMINAL",
  "terminal": {
    "provider": "pochta",
    "id": "117525",
    "accuracy": "APPROXIMATE"
  }
}
```

</details>

`delivery.terminal.provider` – служба доставки "владелец" терминала. "Владельцем" всегда являетесь вы.

`delivery.terminal.id` – ваш идентификатор терминала.

`delivery.terminal.accuracy` – точность указываемого терминала.
На текущий момент Avito не может точно знать в какой терминал отправитель придет отправлять посылку, поэтому для отправителя
в поле `delivery.terminal.accuracy` всегда будет значение `APPROXIMATE`. Для получателя ситуация обратная – Avito точно
знает куда везти посылку получателю, поэтому для получателя в `delivery.terminal.accuracy` всегда будет `EXACT`.

Если в `delivery.type` указан `SORTING_CENTER`, то будет заполнен объект `delivery.sortingCenter`, содержащий данные по
сортировочному центру. Структура и содержимое полей почти полностью совпадает с терминалом. Исключение –
поле `delivery.sortingCenter.provider`. Если посылка кросс-доставочная, посылка едет по Плечу 1 (определение см. в разделе
про кросс-доставку), то владельцем сортировочного центра будет другая служба доставки.

Если в `delivery.type` указан `COURIER`, то будет заполнен объект `delivery.courier`, содержащий данные для курьерской
доставки.

<details>
<summary>Пример заполненных данных курьерской доставки</summary>

```json
{
  "type": "COURIER",
  "courier": {
    "provider": "pecom-t2d",
    "address": {
      "addressRow": "Москва, ул. Лесная, 20с2",
      "details": {
        "house": "20с2",
        "floor": "4",
        "porch": "2",
        "flat": "23"
      },
      "coordinates": {
        "latitude": 55.779003,
        "longitude": 37.591746
      }
    },
    "dateTimeInterval": {
      "start": "2024-07-05T12:04:05Z",
      "end": "2024-07-05T15:04:05Z"
    },
    "options": {
      "deliveryType": "DELIVERY_TO_DOOR",
      "deliveryConfirmationType": "PHONE",
      "elevatorAvailable": true,
      "comment": "Позвоните как подъедете"
    }
  }
}
```

</details>

`delivery.courier.provider` – служба доставки, которая будет осуществлять курьерскую доставку.

`delivery.courier.address.addressRow` – адрес, выбранный пользователем.

`delivery.courier.address.details` - объект с деталями адреса пользователя, разделенными на отдельные поля.

`delivery.courier.address.details.house` – номер дома, корпуса, строения пользователя.

`delivery.courier.address.details.floor` – номер этажа пользователя. Не заполняется, если дом частный.

`delivery.courier.address.details.porch` – номер подъезда пользователя. Не заполняется, если дом частный.

`delivery.courier.address.details.flat` – номер квартиры пользователя. Не заполняется, если дом частный.

`delivery.courier.address.coordinates` – координаты пользователя.

`delivery.courier.address.coordinates.latitude` – географическая широта пользователя, в градусах.

`delivery.courier.address.coordinates.longitude` – географическая долгота пользователя, в градусах.

`delivery.courier.dateTimeInterval` - интервал для курьерской доставки.

`delivery.courier.dateTimeInterval.start` - начало интервала курьерской доставки в формате RFC3339.
`delivery.courier.dateTimeInterval.end` - конец интервала курьерской доставки в формате RFC3339.

`delivery.courier.options` - дополнительные опции курьерской доставки.

`delivery.courier.options.deliveryType` - тип курьерской доставки.
Возможные значения:
- `DELIVERY_TO_DOOR` – доставка до двери. Пока передается всегда только эта опция.
- `DELIVERY_TO_PORCH` – доставка до подъезда.

`delivery.courier.options.elevatorAvailable` - наличие лифта в доме, способного поднять посылку.

`delivery.courier.options.comment` - комментарий для курьера, оставленный пользователем.

`delivery.courier.options.deliveryConfirmationType` - способ связи с пользователем для подтверждения курьерской доставки.
Возможные значения:
- `PHONE` – по телефону. Пока передается всегда только эта опция.

`delivery.completenessAndIntegrity` определяет, где осуществляется проверка целостности и комплектности вложений посылки.
Возможные значения:
- `DIRECT_FLOW` – на прямом потоке. Для отравителя это на приеме посылки, а для получателя на выдаче.
- `RETURN_FLOW` – на возвратном. Для отправителя это на выдаче возврата.

`delivery.secondPartyLogist.provider` задает код службы доставки в системе Авито. Используется для идентификации служб доставки во внешних системах. В частности, применяется в кросс-доставке для формирования анонса. Примеры кодов: `pochta`, `delivery-service-name`.

### "payment"

Объект с информацией об общей стоимости товаров и доставки в посылке.

<details>
<summary>Пример payment</summary>

```json
{
  "payment": {
    "items": {
      "status": "PAID",
      "cost": 30000
    },
    "delivery": {
      "status": "PAID",
      "costWithoutVat": 10000
    }
  }
}
```

</details>

`payment.items.cost` показывает, сколько стоят все вложенные в посылку товары в копейках.

`payment.delivery.costWithoutVat` показывает, сколько стоит доставка посылки без НДС для получателя в копейках.

Обратите внимание, что у товаров `payment.items` и у доставки `payment.delivery` есть статус. Он может быть:
- `PAID` – значит, что уже все оплачено.
- `ON_DELIVERY` – значит, что покупатель должен заплатить при выдаче. Этот статус используется в COD-посылках (см.
  "[Оплата при получении](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/oplata_pri_poluchenii)").
- `PAY_ON_DELIVERY` – значит, что деньги при получении товара покупателем будут списаны с карты (СБП или кошелька), 
привязанной в приложении Авито. Статус используется в POD-посылках(см. "[Оплата при получении списанием с карты покупателя](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/oplata_pri_poluchenii_spisaniem_s_karty_pokupatelya")).

### "options"

<details>
<summary>Пример содержимого базовых опций</summary>

```json
{
  "options": {
    "return": {
      "refused": {
        "action": "RETURN_TO_DEPARTURE_POINT"
      },
      "unclaimed": {
        "action": "RETURN_TO_DEPARTURE_POINT",
        "after": {
          "unit": "DAY",
          "value": 14
        }
      },
      "returned": {
        "action": "DESTROY",
        "after": {
          "unit": "DAY",
          "value": 14
        }
      }
    },
    "tags": [
      "C2C"
    ]
  }
}
```

</details>

#### Опции возвратов

`options.return` определяет политику возвратов.

> [!NOTE]
> На текущий момент вполне нормальна ситуация, когда политики возвратов зафиксированы в договоре между Avito и службой
> доставки, и они не могут меняться для отдельно взятой посылки. В таком случае обработка опций возвратов не имеет смысла,
> "хардкод" на вашей стороне вполне оправдан.

Внутри объекта `options.return` есть дочерние структуры, описывающие поведение в разных ситуациях. Какие могут быть структуры:
- `options.return.refused` определяет алгоритм действий в случае отказа получателя от посылки.
- `options.return.unclaimed` определяет алгоритм действий в случае невостребования посылки получателем.
- `options.return.returned` определяет алгоритм действий в случае доставки возврата в точку получения возврата отправителем.

У каждой структуры есть `action` – действие, которое нужно выполнить, и опциональный дополнительный контекст, нужный для
выполнения этого действия. Что может быть в `action`:
- `DISABLED` – возврат недоступен.
- `DESTROY` – утилизировать.
- `RETURN_TO_DEPARTURE_POINT` – вернуть в точку отправки.
- `RETURN_TO_RECEIVER` – вернуть специально заданному получателю в объекте `options.return.receiver`.
- `MOVE_TO_ON_DEMAND_STORAGE` – отправить на склад временного хранения.

Например, объект `options.return.unclaimed` из примера выше ниже нужно читать так: если через 14 дней после доставки посылка оказалась
невостребованной получателем, то нужно вернуть её в точку отправки.

Или объект `options.return.returned` из примера выше означает: через 14 дней после возврата в точку получения отправителем посылку
нужно утилизировать.

#### package

`package` содержит информацию по совокупному весу и габаритам всех товаров в посылке.

<details>
<summary>Пример заполнения совокупных ВГХ</summary>

```json
{
  "dimensions": {
    "accuracy": "APPROXIMATE",
    "values": [
      40,
      15,
      30
    ]
  },
  "weight": {
    "accuracy": "APPROXIMATE",
    "value": 1000
  }
}
```

</details>

Описание полей элемента из объекта `package`:
- `dimensions` – совокупные габариты всех товаров в посылке.
  - Avito не знает точных итоговых габаритов всех товаров, поэтому в поле `accuracy` мы всегда
    передаем значение `APPROXIMATE`, т.е. указываем на то, что габариты примерные.
  - Габариты передаются в таком порядке: длина, высота, ширина. В случае, если не имеет значения пространственное положение коробки, их можно у себя внутри
    отсортировать от большего к меньшему.
  - Габариты передаются в сантиметрах.
- `weight` – совокупный вес всех товаров в посылке.
  - Аналогично габаритам Avito не знает точный вес всех товаров, поэтому в поле `accuracy` мы всегда передаем
    значение `APPROXIMATE`.
  - Вес передаем в граммах.

#### Теги

Теги – список специфичных особенностей посылки.

На определенные значения в тегах можно завязывать логику. Те теги, которые вас, как службу доставки, не интересуют, игнорируйте.
Список может постоянно пополняться.

> [!IMPORTANT]
> Нельзя добавлять валидацию, блокирующую создание посылки, на неизвестные вам теги.

Список возможных тегов:
- `CART` – корзинная посылка, которая содержит в себе несколько товаров.
- `C2C` – посылка C2C.
- `B2C` – посылка B2C.
- `RETURN` – возвратная посылка.
- `X_DELIVERY` – посылка кросс-доставочная.
- `X_DELIVERY_FIRST_LEG` – кросс-доставочная посылка первого плеча.
- `X_DELIVERY_LAST_LEG` – кросс-доставочная посылка последнего плеча.
- `KGT` – крупногабаритный товар.

## Разбор полей ответа

### Успешный ответ

<details>
<summary>Пример успешного ответа</summary>

```json
{
  "data": {
    "dispatchNumber": "80512198042480",
    "trackingNumber": "80512198042480"
  }
}
```

</details>

`dispatchNumber` – номер службы доставки, который отправитель использует для отправки посылки, а получатель для получения.

`trackingNumber` – номер службы доставки, который отправитель и получатель используют для отслеживания посылки.

> [!IMPORTANT]
> `dispatchNumber` и `trackingNumber` должны быть уникальными. Они не должны повторяться для разных посылок.
>
> У одной посылки `dispatchNumber` и `trackingNumber` могут быть одинаковыми.

### Ответ с ошибкой

<details>
<summary>Пример ответа с ошибкой</summary>

```json
{
 "error": {
   "code": "TERMINAL_UNAVAILABLE",
   "message": "receiver terminal is permanently closed"
 }
}
```

</details>

Если при обработке запроса случилась ошибка, то мы ожидаем, что в ответе будет присутствовать объект `error`, а объекта
`data` не будет.

`error.code` – поле для специальных кодов ошибок, на которые Avito умеет реагировать. Список возможных кодов перечислен в разделе
"[Обработка ошибок](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/obrabotka_oshibok)".

`error.message` – поле для поясняющего ошибку сообщения. Содержимое этого поля должно быть человекочитаемым, чтобы инженеры
Avito и службы доставки по нему хотя бы примерно могли понять, что пошло не так.

# Трекинг

## Назначение метода трекинга

Через метод трекинга служба доставки сообщает Avito о наступлении определенных событий, происходящих с посылкой в
реальном мире.

Например, Avito интересует факт принятия посылки у отправителя или готовность посылки к вручению получателю.

## Спецификация по методу трекинга

Спецификация метода API находится [здесь](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/tracking).

Перед чтением раздела "Механика работы" рекомендуем ознакомиться с форматом запроса. Физический смысл и назначение полей
описаны в спецификации.

<details>
<summary>Пример запроса</summary>
```json
{
  "orderId": "P000123",
  "avitoStatus": "IN_TRANSIT",
  "avitoEventType": "RECEIVED_ON_SENDER_TERMINAL",
  "providerEventCode": "2",
  "comment": "",
  "location": "Москва",
  "date": "2023-07-12T10:00:00+03:00"
}
```
</details>

## Политика повторов в трекинге

> [!IMPORTANT]
> Повторяйте запрос, если в ответе от Avito был получен HTTP-код 500.
> 
> Рекомендуемая частота повторных попыток – один раз в 1-5 минут.
>
> Повторные попытки следует выполнять не дольше 24 часов.

<br/>

> [!IMPORTANT]
> В случае получения перечисленных ниже ошибок с HTTP-кодом 200 повторы выполнять не требуется, так как эти ошибки постоянные.

| HTTP-код | Код ошибки                     | Возможный текст ошибки                        |
|----------|--------------------------------|-----------------------------------------------|
| 200      | ORDER_ID_INVALID               | Could not found order by id and provider name |
| 200      | ORDER_ID_INVALID               | Incorrect order id                            |
| 200      | TRACKING_INVALID               | Failed to get tracking data from request      |

<br/>

> [!IMPORTANT]
> Реализуйте "досыл" пропущенных статусов.
> 
> Для понимания требования рекомендуем сначала ознакомиться с разделом "[Механика работы трекинга](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/mehanika_raboty_trekinga)",
> и обратить внимание на граф статусов посылки и возможные переходы из статуса в статус.
> 
> Если в ответе от Avito вы получаете HTTP-код 200 и статус "forbidden" в `data.status`, то это значит, что вы выполняете
> запрещенный переход. Ориентируясь на содержимое поля `data.details` можно понять, в каком сейчас статусе находится
> посылка в Avito, и, сопоставив с графом переходов, дослать пропущенные статусы.
>
> Если по каким-то причинам, которые оговорены с Avito, "досыл" не реализуется, то политика повторов,
> в случае получения "forbidden" должна быть точно такой же, как в случае получения от Avito HTTP 500.
> Бесконечно присылать невалидные переходы не нужно.

<br/>

## SLA по трекингу
Задержки на передачу треков в Avito не должны превышать 10 минут в 99% треков.

Задержкой называем разность x - y, где:
- x – текущее время, когда Avito обрабатывает входящий трек.
- y – время, когда событие произошло в реальном мире.

Пример: получатель забрал посылку в `01.09.23 12:00`. В Avito соответствующий трек должен быть передан не позднее `01.09.23 12:10`.

## Механика работы трекинга
При реализации трекинга посылки важно понимать концепцию статусов и событий.

### Статусы
Статус – это обобщенное состояние посылки в определенный момент времени.

Возможные статусы посылки:

- `CONFIRMED` – посылка зарегистрирована в службе доставки, но еще не принята от отправителя.
- `IN_TRANSIT` – посылка принята службой доставки у отправителя и начала движение к получателю.
- `ON_DELIVERY` – посылка готова к выдаче получателю.
- `DELIVERED` – посылка выдана получателю.
- `IN_TRANSIT_RETURN` – посылка начала обратное движение. Например, оказалась не востребована, или получатель отказался
  от неё.
- `ON_DELIVERY_RETURN` – посылка готова к выдаче на обратном движении отправителю.
- `RETURNED` – посылка получена отправителем.
- `LOST` – посылка утеряна.
- `DESTROYED` – посылка утилизирована.

Статусы можно разделить на:

- Статусы прямого движения. В этих статусах посылка движется от отправителя к получателю.
- Статусы обратного движения. В этих статусах посылка движется от получателя к отправителю.
- Терминальные. Из этих статусов в другие статусы переходы невозможны (забегая вперед, у этих статусов нет "исходящих"
  стрелок на графе переходов).
- "Проблемные" статусы. Означают разные внештатные ситуации, которые могут произойти с посылкой.

Посылка Avito по части статусов представляет собой [конечный автомат](https://ru.wikipedia.org/wiki/%D0%9A%D0%BE%D0%BD%D0%B5%D1%87%D0%BD%D1%8B%D0%B9_%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%B0%D1%82),
который может менять свой статус согласно графу переходов:
<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/parcel-statuses-graph.png" />

Обратите внимание, что граф – направленный. Переходы возможны только из статусов, из которых исходит стрелка, в статусы,
в которые стрелка входит. Если Avito получит трек со статусом, в который переход не предусмотрен, то этот трек принят не
будет.

Пример:

- Посылка на стороне Avito находится в статусе `IN_TRANSIT`.
- Служба доставки присылает статус `RETURNED`.
- Avito вернет ответ, в котором указано, что переход запрещен, и что посылка находится в статусе `IN_TRANSIT`.

<details>
<summary>Пример ответа</summary>
```json
{
  "data": {
    "status": "forbidden",
    "details": {
      "from": "IN_TRANSIT"
    }
  }
}
```
</details>

Полем `data.details.from` служба доставки может пользоваться для того, чтобы дослать пропущенные статусы. Из
статуса `IN_TRANSIT` в `RETURNED` можно выстроить такую последовательность, глядя в это поле:

- `IN_TRANSIT` -> `RETURNED` = `forbidden`
- `IN_TRANSIT` -> `IN_TRANSIT_RETURN` = `success`
- `IN_TRANSIT_RETURN` -> `RETURNED` = `forbidden`
- `IN_TRANSIT_RETURN` -> `ON_DELIVERY_RETURN` = `success`
- `ON_DELIVERY_RETURN` -> `RETURNED` = `success`

Рекомендуем сразу при интеграции предусмотреть "досыл" пропущенных статусов. Если по каким-то причинам (которые оговорены 
с Avito) "досыл" статусов не будет реализован, то политика повторов, в случае получения `"forbidden"` на невалидный 
переход должна быть точно [такой же](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/politika_povtorov_v_trekinge), 
как в случае получения от Avito HTTP 500. Не нужно бесконечно присылать невалидные переходы.

### События
Статус всегда сопровождается событием. Можно сказать, события – это триггеры, которые переводят посылку в определенный
статус. События могут передаваться в любом порядке, если обратного не оговорено с Avito.

Ниже сопоставление статус-событие. В пару к статусу добавлены события, с которыми этот статус имеет смысл присылать.
Одно и то же событие может соответствовать нескольким статусам. Список событий в дальнейшем может расширяться.

Задача службы доставки при интеграции сопоставить свои внутренние события на пары "статус" + "событие" Avito.

**CONFIRMED**

- `GOODS_CHECK_PASSED` – проверка целостности и комплектности пройдена.
- `GOODS_CHECK_FAILED` – проверка целостности и комплектности не пройдена.
- `DIMENSIONS_CHECK_FAILED` – проверка ВГХ посылки не пройдена.

**IN_TRANSIT**

- `RECEIVED_ON_SENDER_TERMINAL` – посылка получена на терминале отправителя.
- `READY_TO_BE_DEPARTED_FROM_TRANSIT_TERMINAL` – посылка готова к отправке с транзитного терминала.
- `RECEIVED_AT_TRANSIT_TERMINAL` – посылка получена на транзитном терминале.
- `DEPARTED_FROM_TRANSIT_TERMINAL`– посылка отправлена с транзитного терминала.
- `ARRIVED_AT_RECEIVER_CITY` – посылка прибыла в город получателя.

**ON_DELIVERY**

- `RECEIVED_ON_RECEIVER_TERMINAL` – посылка прибыла на терминал получателя.
- `GOODS_CHECK_PASSED` – см. в секции CONFIRMED.
- `GOODS_CHECK_FAILED` – см. в секции CONFIRMED.
- `STORE_TERM_EXTENDED` – срок хранения посылки продлен.
- `STORE_TERM_FINISHED` – срок хранения посылки закончился. Применимо для СД, где посылка какое-то время находится в ПВЗ после истечения срока хранения.
- `PARCEL_IS_TAKEN_BY_COURIER_FOR_DELIVERY` – курьер забрал посылку и повез получателю.
- `FAILED_DELIVERY_ATTEMPT` – неудачная попытка доставки посылки до получателя.

**DELIVERED**

- `ACCEPTED_BY_RECEIVER` – посылка принята получателем.

**IN_TRANSIT_RETURN**

- `REFUSAL_BY_RECEIVER` – получатель отказался от посылки.
- `STORE_TERM_FINISHED` – срок хранения посылки закончился.
- `DELIVERY_IMPOSSIBLE_DUE_TO_OTHER_REASONS` – иные обстоятельства, которые воспрепятствовали вручению посылки
  получателю. В будущем, если у Avito возникнет необходимость уточнить эти обстоятельства, из общего класса "иных"
  обстоятельств может выделиться какое-то конкретное событие. Например, "Отказ в выпуске таможней". Для того чтобы была
  возможность разобраться, что произошло, присылайте с этим событием свой `providerEventCode` и, по возможности,
  комментарий.
- `RETURN_RECEIVED_AT_TRANSIT_TERMINAL` – посылка на обратном движении прибыла на транзитный терминал.
- `RETURN_READY_TO_BE_DEPARTED_FROM_TRANSIT_TERMINAL` – посылка на обратном движении готова к отправке с транзитного
  терминала.
- `RETURN_DEPARTED_FROM_TRANSIT_TERMINAL`– посылка на обратном движении отправлена с транзитного терминала.
- `ARRIVED_AT_SENDER_CITY` – посылка прибыла в город отправителя.
- `CANCELLED_BY_SENDER` – отправитель отменил доставку посылки на прямом движении, посылка разворачивается.
- `DELIVERY_ATTEMPTS_LIMIT_REACHED` - закончились попытки доставки посылки до получателя.
- `RETURN_ARRIVED_AT_RECEIVER_TERMINAL`- посылка возвращается в терминал получателя в случае отказа или если она осталась невостребованной.
- `RETURN_DEPARTED_FROM_RECEIVER_TERMINAL`- посылка была отправлена обратно отправителю из терминала получателя.

**ON_DELIVERY_RETURN**

- `RETURN_RECEIVED_ON_SENDER_TERMINAL` – посылка на обратном движении получена на терминале отправителя.
- `GOODS_CHECK_PASSED` – см. в секции CONFIRMED.
- `GOODS_CHECK_FAILED` – см. в секции CONFIRMED.
- `RETURN_REFUSAL_BY_SENDER` – отправитель отказался от посылки на обратном движении.
- `RECEIVED_AT_ON_DEMAND_STORAGE` – посылка получена на складе временного хранения.

**RETURNED**

- `RETURN_ACCEPTED_BY_SENDER` – посылка на обратном движении принята отправителем.

**LOST**

- `LOST_BY_CARRIER` – посылка утеряна службой доставки.

**DESTROYED**

- `DESTROYED_BY_AVITO_REQUEST` – посылка утилизирована по истечению оговоренного с Avito срока хранения.
- `DESTROYED_BY_SENDER_REQUEST` – посылка утилизирована по запросу отправителя.

### Примеры
Примеры ниже приведены для того, чтобы проиллюстрировать механику работы. В реальных посылках последовательность
треков может отличаться в зависимости от конкретной ситуации. Главное, чтобы сохранялась последовательность статусов, а
последовательность событий также может отличаться от посылки к посылке.

Обратите внимание на схемы движения посылок, примеры запросов и примеры цепочек статусов.

#### ПВЗ-доставка
Простейший сценарий, в котором отправитель относит посылку в свой ПВЗ. Служба доставки везет посылку из этого ПВЗ в ПВЗ
получателя.

Пусть отправитель находится в Москве, а получатель – в Санкт-Петербурге.

##### Прямое движение
Прямое движение – самый штатный случай, когда отправитель отправил посылку, а получатель её успешно получил.

Пусть маршрут движения посылки будет таким:

`ПВЗ отправителя в Москве` -> `СЦ в Москве` -> `СЦ в Санкт-Петербурге` -> `ПВЗ получателя в Санкт-Петербурге`

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/tracking-direct-flow.png" />

На картинке цифрами отмечены этапы. Ниже – расшифровка физического смысла этапа и соответствующего ему трека.

1\. ЦиК пройден.

<details>
<summary>Пример</summary>
```json
{
  "orderId": "P000123",
  "avitoStatus": "CONFIRMED",
  "avitoEventType": "GOODS_CHECK_PASSED",
  "providerEventCode": "1",
  "comment": "",
  "location": "Москва",
  "date": "2023-07-12T10:00:00+03:00"
}
```
</details>

2\. Посылка принята к отправке на терминале отправителя.

<details>
<summary>Пример</summary>
```json
{
  "orderId": "P000123",
  "avitoStatus": "IN_TRANSIT",
  "avitoEventType": "RECEIVED_ON_SENDER_TERMINAL",
  "providerEventCode": "2",
  "comment": "",
  "location": "Москва",
  "date": "2023-07-12T10:00:00+03:00"
}
```
</details>

3\. Посылка покинула терминал отправителя.

<details>
<summary>Пример</summary>
```json
{
  "orderId": "P000123",
  "avitoStatus": "IN_TRANSIT",
  "avitoEventType": "DEPARTED_FROM_TRANSIT_TERMINAL",
  "providerEventCode": "3",
  "comment": "",
  "location": "Москва",
  "date": "2023-07-12T11:00:00+03:00"
}
```
</details>

4\. Посылка прибыла в сортировочный центр.

<details>
<summary>Пример</summary>
```json
{
  "orderId": "P000123",
  "avitoStatus": "IN_TRANSIT",
  "avitoEventType": "RECEIVED_AT_TRANSIT_TERMINAL",
  "providerEventCode": "4",
  "comment": "",
  "location": "Москва",
  "date": "2023-07-12T12:00:00+03:00"
}
```
</details>

5\. Посылка покинула сортировочный центр.

<details>
<summary>Пример</summary>
```json
{
  "orderId": "P000123",
  "avitoStatus": "IN_TRANSIT",
  "avitoEventType": "DEPARTED_FROM_TRANSIT_TERMINAL",
  "providerEventCode": "5",
  "comment": "",
  "location": "Москва",
  "date": "2023-07-12T13:00:00+03:00"
}
```
</details>

6\. Посылка прибыла в город получателя.

<details>
<summary>Пример</summary>
```json
{
  "orderId": "P000123",
  "avitoStatus": "IN_TRANSIT",
  "avitoEventType": "ARRIVED_AT_RECEIVER_CITY",
  "providerEventCode": "6",
  "comment": "",
  "location": "Санкт-Петербург",
  "date": "2023-07-12T14:00:00+03:00"
}
```
</details>

7\. Посылка прибыла в сортировочный центр.

<details>
<summary>Пример</summary>
```json
{
  "orderId": "P000123",
  "avitoStatus": "IN_TRANSIT",
  "avitoEventType": "RECEIVED_AT_TRANSIT_TERMINAL",
  "providerEventCode": "7",
  "comment": "",
  "location": "Санкт-Петербург",
  "date": "2023-07-12T15:00:00+03:00"
}
```
</details>

8\. Посылка покинула сортировочный центр.

<details>
<summary>Пример</summary>
```json
{
  "orderId": "P000123",
  "avitoStatus": "IN_TRANSIT",
  "avitoEventType": "DEPARTED_FROM_TRANSIT_TERMINAL",
  "providerEventCode": "8",
  "comment": "",
  "location": "Санкт-Петербург",
  "date": "2023-07-12T16:00:00+03:00"
}
```
</details>

9\. Посылка прибыла в терминал получателя.

<details>
<summary>Пример</summary>
```json
{
  "orderId": "P000123",
  "avitoStatus": "ON_DELIVERY",
  "avitoEventType": "RECEIVED_ON_RECEIVER_TERMINAL",
  "providerEventCode": "9",
  "comment": "",
  "location": "Санкт-Петербург",
  "date": "2023-07-12T17:00:00+03:00"
}
```
</details>

10\. ЦиК пройден.

<details>
<summary>Пример</summary>
```json
{
  "orderId": "P000123",
  "avitoStatus": "ON_DELIVERY",
  "avitoEventType": "GOODS_CHECK_PASSED",
  "providerEventCode": "10",
  "comment": "",
  "location": "Санкт-Петербург",
  "date": "2023-07-12T18:00:00+03:00"
}
```
</details>

11\. Посылка принята получателем.

<details>
<summary>Пример</summary>
```json
{
  "orderId": "P000123",
  "avitoStatus": "DELIVERED",
  "avitoEventType": "ACCEPTED_BY_RECEIVER",
  "providerEventCode": "11",
  "comment": "",
  "location": "Санкт-Петербург",
  "date": "2023-07-12T18:00:00+03:00"
}
```
</details>

Итого, цепочка статусов посылки на прямом движении в ПВЗ-доставке:
<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/tracking-direct-flow-parcel-statuses-graph.png" />

##### Обратное движение

Обратное движение – тоже штатный случай, когда отправитель отправил посылку, а получатель, например, отказался от
посылки на ПВЗ или не пришёл за ней вовсе.

Пусть маршрут движения посылки будет таким:

`ПВЗ отправителя в Москве` -> `СЦ в Москве` -> `СЦ в Санкт-Петербурге` -> `ПВЗ получателя в Санкт-Петербурге` ->
`СЦ в Санкт-Петербурге` -> `СЦ в Москве` -> `ПВЗ отправителя в Москве`

Посылка, получается, проделала точно такой же обратный путь. В реальном мире он может быть и не таким, построение
маршрута даётся на откуп службе доставки.

Для того чтобы не загромождать схему, опустим участок прямого движения от ПВЗ отправителя в ПВЗ получателя, и
проиллюстрируем только участок обратного движения, который начинается с отказа получателем от посылки.

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/tracking-return-flow.png" />

1\. Получатель отказался от получения посылки на ПВЗ или не пришел вовсе.

<details>
<summary>Пример (отказался)</summary>
```json
{
  "orderId": "P000123",
  "avitoStatus": "IN_TRANSIT_RETURN",
  "avitoEventType": "REFUSAL_BY_RECEIVER",
  "providerEventCode": "1",
  "comment": "",
  "location": "Санкт-Петербург",
  "date": "2023-07-12T10:00:00+03:00"
}
```
</details>

<details>
<summary>Пример (не пришел вовсе)</summary>
```json
{
  "orderId": "P000123",
  "avitoStatus": "IN_TRANSIT_RETURN",
  "avitoEventType": "STORE_TERM_FINISHED",
  "providerEventCode": "1",
  "comment": "",
  "location": "Санкт-Петербург",
  "date": "2023-07-12T10:00:00+03:00"
}
```
</details>

2\. Посылка покинула терминал получателя.

<details>
<summary>Пример</summary>
```json
{
  "orderId": "P000123",
  "avitoStatus": "IN_TRANSIT_RETURN",
  "avitoEventType": "RETURN_DEPARTED_FROM_TRANSIT_TERMINAL",
  "providerEventCode": "2",
  "comment": "",
  "location": "Санкт-Петербург",
  "date": "2023-07-12T11:00:00+03:00"
}
```
</details>

3\. Посылка прибыла на сортировочный центр.

<details>
<summary>Пример</summary>
```json
{
  "orderId": "P000123",
  "avitoStatus": "IN_TRANSIT_RETURN",
  "avitoEventType": "RETURN_RECEIVED_AT_TRANSIT_TERMINAL",
  "providerEventCode": "3",
  "comment": "",
  "location": "Санкт-Петербург",
  "date": "2023-07-12T12:00:00+03:00"
}
```
</details>

4\. Посылка покинула сортировочный центр.

<details>
<summary>Пример</summary>
```json
{
  "orderId": "P000123",
  "avitoStatus": "IN_TRANSIT_RETURN",
  "avitoEventType": "RETURN_DEPARTED_FROM_TRANSIT_TERMINAL",
  "providerEventCode": "4",
  "comment": "",
  "location": "Санкт-Петербург",
  "date": "2023-07-12T13:00:00+03:00"
}
```
</details>

5\. Посылка прибыла в город отправителя.

<details>
<summary>Пример</summary>
```json
{
  "orderId": "P000123",
  "avitoStatus": "IN_TRANSIT_RETURN",
  "avitoEventType": "ARRIVED_AT_SENDER_CITY",
  "providerEventCode": "5",
  "comment": "",
  "location": "Москва",
  "date": "2023-07-12T14:00:00+03:00"
}
```
</details>

6\. Посылка прибыла на сортировочный центр.

<details>
<summary>Пример</summary>
```json
{
  "orderId": "P000123",
  "avitoStatus": "IN_TRANSIT_RETURN",
  "avitoEventType": "RETURN_RECEIVED_AT_TRANSIT_TERMINAL",
  "providerEventCode": "6",
  "comment": "",
  "location": "Москва",
  "date": "2023-07-12T15:00:00+03:00"
}
```
</details>

7\. Посылка покинула сортировочный центр.

<details>
<summary>Пример</summary>
```json
{
  "orderId": "P000123",
  "avitoStatus": "IN_TRANSIT_RETURN",
  "avitoEventType": "RETURN_DEPARTED_FROM_TRANSIT_TERMINAL",
  "providerEventCode": "7",
  "comment": "",
  "location": "Москва",
  "date": "2023-07-12T16:00:00+03:00"
}
```
</details>

8\. Посылка прибыла в терминал отправителя.

<details>
<summary>Пример</summary>
```json
{
  "orderId": "P000123",
  "avitoStatus": "ON_DELIVERY_RETURN",
  "avitoEventType": "RETURN_RECEIVED_ON_SENDER_TERMINAL",
  "providerEventCode": "8",
  "comment": "",
  "location": "Москва",
  "date": "2023-07-12T17:00:00+03:00"
}
```
</details>

9\. ЦиК пройден.

<details>
<summary>Пример</summary>
```json
{
  "orderId": "P000123",
  "avitoStatus": "ON_DELIVERY_RETURN",
  "avitoEventType": "GOODS_CHECK_PASSED",
  "providerEventCode": "9",
  "comment": "",
  "location": "Москва",
  "date": "2023-07-12T18:00:00+03:00"
}
```
</details>

10\. Отправитель принял посылку.

<details>
<summary>Пример</summary>
```json
{
  "orderId": "P000123",
  "avitoStatus": "RETURNED",
  "avitoEventType": "RETURN_ACCEPTED_BY_SENDER",
  "providerEventCode": "10",
  "comment": "",
  "location": "Москва",
  "date": "2023-07-12T18:00:00+03:00"
}
```
</details>

Итого, цепочка статусов посылки на обратном движении в ПВЗ-доставке:
<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/tracking-return-flow-parcel-statuses-graph.png" />

##### Утилизация
Утилизация посылки – внештатная ситуация, которая происходит в случае, если:
- Посылка вернулась в ПВЗ отправителя.
- Отправитель не забрал посылку или вовсе от неё отказался.
- Истек оговоренный с Avito срок хранения посылки.

Аналогично, чтобы не загромождать схему, опустим участок прямого и обратного движения, и проиллюстрируем только процесс
утилизации:

<img style="max-width:50%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/tracking-utilization.png" />

1\. Посылка отправлена на склад временного хранения.

<details>
<summary>Пример</summary>
```json
{
  "orderId": "P000123",
  "avitoStatus": "ON_DELIVERY_RETURN",
  "avitoEventType": "RECEIVED_AT_ON_DEMAND_STORAGE",
  "providerEventCode": "1",
  "comment": "Отправитель отказался от получения",
  "location": "Москва",
  "date": "2023-07-12T10:00:00+03:00"
}
```
</details>

2\. Истек срок хранения посылки.

<details>
<summary>Пример</summary>
```json
{
  "orderId": "P000123",
  "avitoStatus": "DESTROYED",
  "avitoEventType": "DESTROYED_BY_AVITO_REQUEST",
  "providerEventCode": "2",
  "comment": "Истек срок хранения",
  "location": "Москва",
  "date": "2023-07-12T11:00:00+03:00"
}
```
</details>

Итого, цепочка статусов посылки при утилизации в ПВЗ-доставке:
<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/tracking-utilization-parcel-statuses-graph.png" />

### FAQ

**Вопрос**

Можно ли не присылать локацию `location`?

**Ответ**

Локацию крайне желательно присылать всегда, т.к. Avito транслирует пользователю местоположение посылки. Местоположение
посылки никто, кроме СД, точнее не знает. Но если нет технической возможности во всех треках указывать локацию, то можно
присылать пустую строку.

# Запрет приема посылки
Запрет приема посылки – операция, которую выполняет Avito в службе доставки, когда Avito нужно у себя отменить заказ пользователей.
Запрет приема подразумевает, что если отправитель придет отправлять посылку в ПВЗ / постамат, то служба доставки гарантированно
не будет принимать посылку.

Служба доставки реализует у себя [метод](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/prohibitOrderAcceptance), который будет вызывать Avito.

### Схема работы
<details>
<summary>Детальная схема запрета приема</summary>

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/prohibit-parcel-acceptance.png" />

Замечания по схеме:
- Метод запрета приема на стороне СД – синхронный. Мы ожидаем, что СД синхронно либо разрешит отмену, либо ответит 
соответствующей ошибкой.

</details>

### Нефункциональные и функциональные требования
Нефункциональные требования:
- Максимальное время ответа - 3с.
- Количество запросов, гарантировано не приводящее к деградации – 300 RPM.
- Доступность метода – 99% (за исключением заранее оговоренных регламентных работ).
- Максимальная запланированная недоступность (проведение регламентных работ) - не более 3х часов в неделю (требуется 
заблаговременное согласование времени проведения работ - минимум за 3 рабочих дня до проведения работ).

В случае, если в процессе отмены заказа произошла непредвиденная ошибка и повторная попытка отмены может привести к успеху, 
вызов метода должен вернуть HTTP 500 ошибку.

В случае, если по каким-то причинам посылка не может быть отменена (например, она уже принята на ПВЗ),
метод должен вернуть 200 HTTP-код ответа с описанием ошибки отмены заказа.
Справочник кодов ошибок отмены заказа:
- `ALREADY_RECEIVED` - посылка уже была принята от продавца и запрет её приёма невозможен.
- `NOT_FOUND` - посылка не найдена.

Метод должен быть идемпотентным. В случае, если происходит повторная попытка отмены посылки (посылка была успешно отменена ранее),
метод должен вернуть 200 HTTP-код ответа без ошибки, как в случае если бы посылка отменялась первый раз.

### Альтернативная схема работы запрета приема (находится в разработке)
Описанная выше схема предполагает синхронный поход в службу доставки для запрета приема посылки. 
Накопленный опыт, полученный за счет обратной связи от служб доставки показал, что процесс запрета приема может быть растянутым во времени, что 
в свою очередь создает трудности для соблюдения описанных выше нефункциональных требований.
Чтобы устранить этот недостаток и сделать процесс запрета приема более эффективным в разработку запускается асинхронный метод запрета приема, основанный на системе заявок.
Подробнее о том как работает асинхронный запрет приема можно ознакомиться в разделе ["Изменение свойств посылок"](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/izmenenie_svoystv_posylok).
Там же можно найти контракт для реализации асинхронного запрета приема.

# Отмена посылки
Отмена посылки – операция, которую выполняет Avito в службе доставки, когда Avito нужно у себя отменить (**находящийся в пути**) заказ пользователя.
Отмена посылки подразумевает, что везти посылку до получателя/выдавать посылку не надо, а надо вернуть ее отправителю. Т.е. посылка должна перейти из текущего статуса в статус `IN_TRANSIT_RETURN`. Посылка в момент отмены может находится в статусах `IN_TRANSIT` или `ON_DELIVERY`.
Главное отличие от "[Запрета приема посылки](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/zapret_priema_posylki)" это то, что посылка уже была принята на ПВЗ, то есть уже в пути.

Служба доставки реализует у себя [метод](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/cancelParcel), который будет вызывать Avito.

### Схема работы
<details>
<summary>Детальная схема отмены</summary>

<img style="max-width:100%" src="https://avito.st/static/ims/627e6728-a932-48d1-95ec-8bbbb3a671d2_cancel_parcel_common_934x1042.png" />

Замечания по схеме:
- Метод отмены – синхронный. Мы ожидаем, что СД синхронно либо разрешит отмену, либо ответит
  соответствующей ошибкой.
- На данный момент поле `actor` может принимать только значение `receiver`.
- Avito после успешного ответа от СД меняет в своей системе статус посылки на `IN_TRANSIT_RETURN`.
- Последующий трек от СД должен быть с статусом `IN_TRANSIT_RETURN` и event'ом `CANCELLED_BY_RECEIVER_REQUEST`" (в случае если actor=receiver).
- После отмены статусы прямого движения будут отклонены с ошибкой FORBIDDEN, валидно будет обрабатываться цепочка статусов начиная с `IN_TRANSIT_RETURN`.

</details>

### Нефункциональные и функциональные требования
Нефункциональные требования:
- Максимальное время ответа - 10с.
- Количество запросов, гарантировано не приводящее к деградации – 300 RPM.
- Доступность метода – 99% (за исключением заранее оговоренных регламентных работ).
- Максимальная запланированная недоступность (проведение регламентных работ) - не более 3х часов в неделю (требуется
  заблаговременное согласование времени проведения работ - минимум за 3 рабочих дня до проведения работ).

В случае, если в процессе отмены посылки произошла непредвиденная ошибка и повторная попытка отмены может привести к успеху,
вызов метода должен вернуть HTTP 500 ошибку.

В случае, если по каким-то причинам посылка не может быть отменена (например, она уже выдана получателю),
метод должен вернуть 200 HTTP-код ответа с описанием ошибки отмены заказа.
Справочник кодов ошибок отмены заказа:
- `FORBIDDEN` - посылка не может быть отменена.
- `NOT_FOUND` - посылка не найдена, проставляется в случае если посылки нет в системе СД. (В текущем сценарии такой ситуации быть не должно, так как Avito отменяет существующие посылки)

Метод должен быть идемпотентным. В случае, если происходит повторная попытка отмены посылки (посылка была успешно отменена ранее),
метод должен вернуть 200 HTTP-код ответа без ошибки, как в случае если бы посылка отменялась первый раз.

# Корзина
“Корзиной” называем ситуацию, когда в посылке содержится несколько разных товаров, либо несколько единиц одного товара.
“Корзинный” запрос на создание посылки отличается от обычного тем, что в поле `items` будет указано больше одного товара, 
либо товар будет один, но с `count` больше единицы.

> [!IMPORTANT]
> В Корзине все товары принимаются к отправке вместе, либо не принимаются совсем.
>
> При отказе от корзинной посылки в ПВЗ (агентский возврат) получатель отказывается от всех товаров. Получатель в ПВЗ 
> не может одну часть товаров из посылки забрать, а другую вернуть.

Корзина доступна как в C2C-сценарии, так и в B2C.

## Прямой поток
На прямом потоке доставка корзинной посылки ничем не отличается от доставки обычной посылки.

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/cart-flow-direct.png" />

1. Отправитель относит посылку PARCEL в ПВЗ сдачи 3PL PUDO 1. В одной посылке лежит несколько товаров. Например, две 
пары туфель, и рубашка.
2. Посылка едет в ПВЗ получения 3PL PUDO 2 к получателю.
3. Получатель забирает посылку.

<details>
<summary>Пример запроса на создание корзинной посылки</summary>

```json
{
  "orderID": "37476980088635974",
  "parcelID": "P00037988",
  "items": [
    {
      "id": 2204179715,
      "title": "Туфли",
      "description": "Красивые туфли.",
      "cost": 30000,
      "quantity": 2,
      "breadcrumbs": [
        {
          "name": "Москва"
        },
        {
          "name": "Личные вещи"
        },
        {
          "name": "Одежда и обувь"
        },
        {
          "name": "Женская обувь"
        }
      ],
      "dimensions": {
        "accuracy": "APPROXIMATE",
        "values": [
          20,
          10,
          20
        ]
      },
      "weight": {
        "accuracy": "APPROXIMATE",
        "value": 2000
      },
      "imagesUrls": {
        "listing": "//01-img-staging-proxy.k.avito.ru/image/1/1.3PR4nLa-cB1ONbIYTNfF6AyL4tDPP3YZzL9438k_dBXEN3I.eyc4L4JP0aJyZ-QLKjsx5_5Gj1eYGxLg5H6aApfN0v8",
        "list": [
          "//01-img-staging-proxy.k.avito.ru/image/1/1.3PR4nLa-cB1ONbIYTNfF6AyL4tDPP3YZzL9438k_dBXEN3I.eyc4L4JP0aJyZ-QLKjsx5_5Gj1eYGxLg5H6aApfN0v8"
        ]
      }
    },
    {
      "id": 2204316124,
      "title": "Рубашка",
      "description": "Красивая рубашка.",
      "cost": 30000,
      "quantity": 1,
      "breadcrumbs": [
        {
          "name": "Москва"
        },
        {
          "name": "Личные вещи"
        },
        {
          "name": "Одежда и обувь"
        },
        {
          "name": "Мужская одежда"
        }
      ],
      "dimensions": {
        "accuracy": "APPROXIMATE",
        "values": [
          20,
          10,
          20
        ]
      },
      "weight": {
        "accuracy": "APPROXIMATE",
        "value": 2500
      },
      "imagesUrls": {
        "listing": "//01-img-staging-proxy.k.avito.ru/image/1/1.3N25zLa-cDSPZbIxja_lxKPzl_UNb3YwDe949ghvdDwFZ3I.IW57t1OcSJZs2doGZJWE0DJSaePenMe_q8FOD9mFmBQ",
        "list": [
          "//01-img-staging-proxy.k.avito.ru/image/1/1.3N25zLa-cDSPZbIxja_lxKPzl_UNb3YwDe949ghvdDwFZ3I.IW57t1OcSJZs2doGZJWE0DJSaePenMe_q8FOD9mFmBQ"
        ]
      }
    }
  ],
  "sender": {
    "type": "PRIVATE",
    "phones": [
      "79999999999"
    ],
    "email": "email4321@avito-test.ru",
    "name": "the_best_seller_in_the_world",
    "delivery": {
      "type": "TERMINAL",
      "terminal": {
        "provider": "pochta",
        "id": "117525",
        "accuracy": "APPROXIMATE"
      },
      "completenessAndIntegrity": [
        "DIRECT_FLOW",
        "RETURN_FLOW"
      ]
    }
  },
  "receiver": {
    "type": "PRIVATE",
    "phones": [
      "79999999999"
    ],
    "email": "email1234@avito-test.ru",
    "name": "Иванов Иван Иванович",
    "delivery": {
      "type": "TERMINAL",
      "terminal": {
        "provider": "pochta",
        "id": "119296",
        "accuracy": "EXACT"
      },
      "completenessAndIntegrity": [
        "DIRECT_FLOW"
      ]
    }
  },
  "payment": {
    "items": {
      "status": "PAID",
      "cost": 90000
    },
    "delivery": {
      "status": "PAID",
      "costWithoutVat": 10000
    }
  },
  "options": {
    "return": {
      "refused": {
        "action": "RETURN_TO_DEPARTURE_POINT"
      },
      "unclaimed": {
        "action": "RETURN_TO_DEPARTURE_POINT",
        "after": {
          "unit": "DAY",
          "value": 14
        }
      },
      "returned": {
        "action": "DESTROY",
        "after": {
          "unit": "DAY",
          "value": 14
        }
      }
    },
    "tags": [
      "C2C",
      "CART"
    ]
  }
}
```

Особенности:
- В поле `items` несколько элементов.
- В поле `items.count` содержимое > 1.
- В `options.tags` есть тег `CART`.

</details>

## Обратный поток (агентский возврат)
При отказе от “корзинной” посылки в ПВЗ (агентский возврат) получатель отказывается **от всех товаров**. Аналогично 
агентскому возврату в стандартном C2C-сценарии возврат осуществляется под тем же номером посылки Avito, который был на 
прямом потоке.

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/cart-flow-return.png" />

1. Отправитель относит посылку PARCEL в ПВЗ сдачи 3PL PUDO 1. В одной посылке лежит несколько товаров. Например, две 
пары туфель и рубашка.
2. Посылка едет в ПВЗ получения 3PL PUDO 2 к получателю.
3. Получатель на ПВЗ отказывается от посылки.
4. Посылка PARCEL начинает обратное движение к отправителю в 3PL PUDO 1. Посылка содержит те же товары, что были в ней 
на прямом потоке.
5. Отправитель забирает возврат.

## Обратный поток (клиентский + частичный возврат)
Клиентский возврат в Корзине доступен только в B2C-сценарии, но в будущем он появится и в C2C-сценарии. В B2C-сценарии 
покупатель имеет право сделать возврат части товаров из посылки после получения. У клиентского возврата есть некоторые 
особенности, и они описаны в разделе "[Клиентский возврат](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/klientskie_vozvraty)". 
Эти особенности актуальны и для корзинных посылок.

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/cart-flow-return-client-partial.png" />

1. Отправитель относит посылку PARCEL в ПВЗ сдачи 3PL PUDO 1. В одной посылке лежит несколько товаров. Например, две 
пары туфель и рубашка.
2. Посылка едет в ПВЗ получения 3PL PUDO 2 к Получателю.
3. Получатель забирает посылку.
4. Получатель решил вернуть часть товаров из посылки (одну пару туфель и рубашку), и инициировал создание отдельной возвратной посылки PARCEL 2. Получатель отнес возвратную PARCEL 2 в 3PL PUDO 2.
5. Посылка едет в 3PL PUDO 1, в который изначальный Отправитель отправил посылку PARCEL.
6. Отправитель забирает возврат. Если не забирает, то посылка утилизируется.

<details>
<summary>Пример запроса на создание возвратной корзинной посылки с частичным возвратом</summary>

```json
{
  "orderID": "37476980088635974",
  "parcelID": "P00037988",
  "items": [
    {
      "id": 2204179715,
      "title": "Туфли",
      "description": "Красивые туфли.",
      "cost": 30000,
      "quantity": 1,
      "breadcrumbs": [
        {
          "name": "Москва"
        },
        {
          "name": "Личные вещи"
        },
        {
          "name": "Одежда и обувь"
        },
        {
          "name": "Женская обувь"
        }
      ],
      "dimensions": {
        "accuracy": "APPROXIMATE",
        "values": [
          20,
          10,
          20
        ]
      },
      "weight": {
        "accuracy": "APPROXIMATE",
        "value": 2000
      },
      "imagesUrls": {
        "listing": "//01-img-staging-proxy.k.avito.ru/image/1/1.3PR4nLa-cB1ONbIYTNfF6AyL4tDPP3YZzL9438k_dBXEN3I.eyc4L4JP0aJyZ-QLKjsx5_5Gj1eYGxLg5H6aApfN0v8",
        "list": [
          "//01-img-staging-proxy.k.avito.ru/image/1/1.3PR4nLa-cB1ONbIYTNfF6AyL4tDPP3YZzL9438k_dBXEN3I.eyc4L4JP0aJyZ-QLKjsx5_5Gj1eYGxLg5H6aApfN0v8"
        ]
      }
    },
    {
      "id": 2204316124,
      "title": "Рубашка",
      "description": "Красивая рубашка.",
      "cost": 30000,
      "quantity": 1,
      "breadcrumbs": [
        {
          "name": "Москва"
        },
        {
          "name": "Личные вещи"
        },
        {
          "name": "Одежда и обувь"
        },
        {
          "name": "Мужская одежда"
        }
      ],
      "dimensions": {
        "accuracy": "APPROXIMATE",
        "values": [
          20,
          10,
          20
        ]
      },
      "weight": {
        "accuracy": "APPROXIMATE",
        "value": 2500
      },
      "imagesUrls": {
        "listing": "//01-img-staging-proxy.k.avito.ru/image/1/1.3N25zLa-cDSPZbIxja_lxKPzl_UNb3YwDe949ghvdDwFZ3I.IW57t1OcSJZs2doGZJWE0DJSaePenMe_q8FOD9mFmBQ",
        "list": [
          "//01-img-staging-proxy.k.avito.ru/image/1/1.3N25zLa-cDSPZbIxja_lxKPzl_UNb3YwDe949ghvdDwFZ3I.IW57t1OcSJZs2doGZJWE0DJSaePenMe_q8FOD9mFmBQ"
        ]
      }
    }
  ],
  "sender": {
    "type": "PRIVATE",
    "phones": [
      "79999999999"
    ],
    "email": "email1234@avito-test.ru",
    "name": "Иванов Иван Иванович",
    "delivery": {
      "type": "TERMINAL",
      "terminal": {
        "provider": "pochta",
        "id": "117525",
        "accuracy": "APPROXIMATE"
      },
      "completenessAndIntegrity": [
        "DIRECT_FLOW",
        "RETURN_FLOW"
      ]
    }
  },
  "receiver": {
    "type": "LEGAL",
    "phones": [
      "79999999999"
    ],
    "email": "email4321@avito-test.ru",
    "name": "ИП Сергеев С.С.",
    "delivery": {
      "type": "TERMINAL",
      "terminal": {
        "provider": "pochta",
        "id": "119296",
        "accuracy": "EXACT"
      },
      "completenessAndIntegrity": [
        "DIRECT_FLOW"
      ]
    }
  },
  "payment": {
    "items": {
      "status": "PAID",
      "cost": 60000
    },
    "delivery": {
      "status": "PAID",
      "costWithoutVat": 10000
    }
  },
  "options": {
    "return": {
      "refused": {
        "action": "DESTROY",
        "after": {
          "unit": "DAY",
          "value": 14
        }
      },
      "unclaimed": {
        "action": "DESTROY",
        "after": {
          "unit": "DAY",
          "value": 14
        }
      }
    },
    "tags": [
      "B2C",
      "CART",
      "RETURN"
    ]
  }
}
```

Особенности:
- По части “корзинности” те же, что и в C2C.
- В `receiver.type` будет значение LEGAL (юридическое лицо), если это частичный возврат в B2C-сценарии.
- В `options.tags` есть теги `B2C` и `RETURN`.
- Если в возвратной посылке будет один товар (одна единица), то тег `CART` будет в запросе отсутствовать. 
Запрос будет выглядеть как обычный клиентский B2C-возврат.

</details>

# Возвраты

## Агентские возвраты
Агентский возврат – возврат без выдачи посылки получателю. Возможен в двух случаях:
- Получатель отказался от получения посылки в пункте получения при проверке.
- Получатель не пришел за посылкой вовсе, она оказалась невостребованной.

В случае агентского возврата по посылке должны приходить "возвратные" статусы `IN_TRANSIT_RETURN`, `ON_DELIVERY_RETURN`,
`RETURNED`. Номер посылки при этом не меняется.

Агентские возвраты есть во всех сценариях доставки. Везде есть свои нюансы, поэтому, чтобы узнать как работает
агентский возврат в C2C-ПВЗ, кросс-доставке или в других сценариях, обратитесь к детализированным схемам доставки по сценарию 
в документации.

## Клиентские возвраты
Клиентский возврат – возврат, который инициирует получатель после того, как посылка ему была выдана. Возможностью
клиентского возврата управляет Avito, позволяя или не позволяя получателю инициировать создание новой возвратной посылки.

Можно сказать, что клиентские возвраты – это отдельная опция, которую Avito может предоставлять получателю. Для службы
доставки клиентский возврат выглядит как обычная посылка, но с некоторыми особенностями в поле `options`:
- В поле `return` указана политика возврата, направленная на то, чтобы возвратная посылка в случае невостребования / отказа 
изначальным отправителем-продавцом не возвращалась получателю, а утилизировалась.
- Есть тег `RETURN`.

Возможность клиентского возврата по умолчанию доступна, например, в [B2C-ПВЗ сценарии](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/B2C-PVZ_scenarij).

> [!IMPORTANT]
> Для того, чтобы Avito могло создать возвратную посылку критически необходимо проставлять ПВЗ реальной сдачи продавцом
> через соответствующий [метод](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/setOrderRealAddress).
> Именно этот ПВЗ Avito будет указывать в качестве точки получения при создании возвратной посылки.

<br />

> [!IMPORTANT]
> Возвратная посылка в случае невостребования / отказа изначальным отправителем-продавцом не должна уезжать обратно получателю-покупателю. Avito будет указывать специальные параметры в запросе. См. примеры.

## Частичные возвраты
Частичный возврат возможен в случае, если получатель на прямом потоке получал [корзинную](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/korzina) 
посылку, в которой было несколько товаров / единиц одного товара.

Частичные возвраты возможны только через клиентский возврат, возможностью осуществить который управляет Avito. Поэтому 
частичные возвраты полностью "прозрачны" для службы доставки. Она даже не узнает о том, что это возврат части товаров, а
не обыкновенный полный клиентский возврат.

# Оплата при получении
Оплата при получении – опциональная услуга, которая предоставляется получателю посылки. Физический смысл вытекает из её
названия: получатель платит за доставку и товар только тогда, когда хочет забрать посылку. В остальном отличий по части
интеграции по API нет.

Avito сообщает службе доставки о том, что посылка будет с оплатой при получении, через объект `payment` в запросе
на [создание посылки](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/createParcel) ([описание](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/sozdanie_posylki)).

```json
{
  "payment": {
    "items": {
      "status": "ON_DELIVERY",
      "cost": 30000
    },
    "delivery": {
      "status": "ON_DELIVERY",
      "cost": 20000,
      "costWithoutVat": 10000
    }
  }
}
```

В `items.status` и `delivery.status` указан статус `ON_DELIVERY`, который означает что оплату за товары в посылке и за
доставку в посылке нужно взять с получателя при выдаче посылки.

В объекте `delivery` Avito еще будет указывать дополнительный параметр `delivery.cost`, т.е. полную стоимость, включая
НДС, которую нужно будет взять с получателя.

В объекте `options.tags` будет дополнительный тег `COD`.

<details>
<summary>Пример запроса на создание C2C COD-посылки</summary>

```json
{
  "orderID": "37476980088635974",
  "parcelID": "P00037988",
  "items": [
    {
      "id": 2639716187,
      "title": "Подставки",
      "description": "Подставки с рекламой,  в наборе 17 штук.",
      "cost": 30000,
      "quantity": 1,
      "breadcrumbs": [
        {
          "name": "Москва"
        },
        {
          "name": "Хобби и отдых"
        },
        {
          "name": "Коллекционирование"
        },
        {
          "name": "Модели"
        }
      ],
      "dimensions": {
        "accuracy": "APPROXIMATE",
        "values": [
          40,
          15,
          30
        ]
      },
      "weight": {
        "accuracy": "APPROXIMATE",
        "value": 1000
      },
      "imagesUrls": {
        "listing": "//01-img-staging-proxy.k.avito.ru/image/1/1.3D5hCra-cNdXo7LSVQnoRGUFohLVqXbT1Sl4FdCpdN_VoXI.4Q-_IforWBTgJ_4VUeJcI9o4Vj4p2CBZPZbcP7ISH0s",
        "list": [
          "//01-img-staging-proxy.k.avito.ru/image/1/1.3D5hCra-cNdXo7LSVQnoRGUFohLVqXbT1Sl4FdCpdN_VoXI.4Q-_IforWBTgJ_4VUeJcI9o4Vj4p2CBZPZbcP7ISH0s"
        ]
      }
    }
  ],
  "sender": {
    "type": "PRIVATE",
    "phones": [
      "79999999999"
    ],
    "email": "email4321@avito-test.ru",
    "name": "the_best_seller_in_the_world",
    "delivery": {
      "type": "TERMINAL",
      "terminal": {
        "provider": "pochta",
        "id": "117525",
        "accuracy": "APPROXIMATE"
      },
      "completenessAndIntegrity": [
        "DIRECT_FLOW",
        "RETURN_FLOW"
      ]
    }
  },
  "receiver": {
    "type": "PRIVATE",
    "phones": [
      "79999999999"
    ],
    "email": "email1234@avito-test.ru",
    "name": "Иванов Иван Иванович",
    "delivery": {
      "type": "TERMINAL",
      "terminal": {
        "provider": "pochta",
        "id": "119296",
        "accuracy": "EXACT"
      },
      "completenessAndIntegrity": [
        "DIRECT_FLOW"
      ]
    }
  },
  "payment": {
    "items": {
      "status": "ON_DELIVERY",
      "cost": 30000
    },
    "delivery": {
      "status": "ON_DELIVERY",
      "cost": 20000,
      "costWithoutVat": 10000
    }
  },
  "options": {
    "return": {
      "refused": {
        "action": "RETURN_TO_DEPARTURE_POINT"
      },
      "unclaimed": {
        "action": "RETURN_TO_DEPARTURE_POINT",
        "after": {
          "unit": "DAY",
          "value": 14
        }
      },
      "returned": {
        "action": "DESTROY",
        "after": {
          "unit": "DAY",
          "value": 14
        }
      }
    },
    "tags": [
      "C2C",
      "COD"
    ]
  }
}
```

</details>

> [!IMPORTANT]
> Если по посылке с оплатой при получении от вас приходит трек со статусом `DELIVERED`, Avito считает, что оплата состоялась.

# Оплата при получении списанием с карты покупателя
В варианте оплаты при получении описанном выше, предполагается, что оплата производится в пункте выдаче с помощью платежного
терминала или наличного расчета.

Отличие данного варианта в том, что списание происходит с карты покупателя, прикрепленной в Avito. Выдача товара покупателю
производится в том случае, если средства были успешно списаны с карты покупателя.

Avito сообщает службе доставки о том, что посылка будет с оплатой при получении, через объект `payment` в запросе
на [создание посылки](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/createParcel) ([описание](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/sozdanie_posylki)).

```json
{
  "payment": {
    "items": {
      "status": "PAY_ON_DELIVERY",
      "cost": 30000
    },
    "delivery": {
      "status": "PAY_ON_DELIVERY",
      "cost": 20000,
      "costWithoutVat": 10000
    }
  }
}
```
В `items.status` и `delivery.status` указан статус `PAY_ON_DELIVERY`, который означает, что оплата за товары в посылке и за
доставку в посылке будет списана с карты покупателя при попытке получения посылки в ПВЗ.

Важно отметить, что в отличие от предыдущего варианта, в объекте `options.tags` не будет дополнительного тега.

> [!IMPORTANT]
> Данный механизм пока находится в разработке, и на первых этапах не будет работать для внешних служб доставок, информация по
> интеграции будет дополняться по мере необходимости

# Проверка целостности и комплектности
Проверка целостности и комплектности – процесс, в котором сотрудник СД проверяет, что в посылке лежат те товары, действительно
заявленные в запросе на создание посылки. Проверку стоит проводить, опираясь на название в `items.title`, описание в
`items.description` и фотографии в `items.imagesUrls`.

Служба доставки сообщает Avito об успешности / неуспешности прохождения ЦиК через метод [трекинга](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/tracking).
Треки ЦиК содержат события `GOODS_CHECK_PASSED` и `GOODS_CHECK_FAILED`. Эти события – информационные, они должны идти в 
паре с текущим статусом посылки и не влиять на него, потому что ЦиК во всех случаях предваряет какое-то действие 
(например, приём к отправке), но сам по себе ЦиК не является действием, которое может изменить статус посылки.

##### Пример. ЦиК на приеме

Посылка находится в статусе `CONFIRMED`. Т.е. готова к отправке. Возможны две ситуации.

- СД присылает `CONFIRMED` и `GOODS_CHECK_PASSED` (ЦиК пройден).
- Затем `IN_TRANSIT` и `RECEIVED_ON_SENDER_TERMINAL` (отправитель отправил).

или

- СД присылает `CONFIRMED` и `GOODS_CHECK_FAILED` (ЦиК не пройден).
- После Avito не ожидает никакого другого статуса, т.к. по бизнес-процессу прием к отправке посылки с некорректным
  вложением невозможен.

##### Пример. ЦиК на выдаче

Посылка находится в статусе `ON_DELIVERY`. Т.е. готова к выдаче.

- СД присылает `ON_DELIVERY` и `GOODS_CHECK_PASSED` (ЦиК пройден).
- Затем `DELIVERED` и `ACCEPTED_BY_RECEIVER` (получатель принял посылку).

или

- СД присылает `ON_DELIVERY` и `GOODS_CHECK_FAILED` (ЦиК не пройден).
- Затем `DELIVERED` и `ACCEPTED_BY_RECEIVER` (если получатель пожелал забрать несмотря на то, что пришло не то)
  или `IN_TRANSIT_RETURN` и `REFUSAL_BY_RECEIVER` (если получатель отказался забирать).

##### ЦиК на выдаче возврата

Посылка (заказ) находится в статусе `ON_DELIVERY_RETURN`. Т.е. возврат готов к выдаче.

- СД присылает `ON_DELIVERY_RETURN` и `GOODS_CHECK_PASSED` (ЦиК пройден).
- Затем `RETURNED` и `RETURN_ACCEPTED_BY_SENDER` (если отправитель забрал возврат).

или

- СД присылает `ON_DELIVERY_RETURN` и `GOODS_CHECK_FAILED` (ЦиК не пройден).
- Затем `ON_DELIVERY_RETURN` и `RETURN_REFUSAL_BY_SENDER` (если отправитель отказался от получения возврата).

# Изменение свойств посылок

## Назначение

В настоящий момент функциональность изменения свойств посылок используется для следующих сценариев:
- Изменение ФИО и номера телефона получателя (сценарий `changeReceiver`), что позволяет предоставить возможность получения посылки другому лицу при отсутствии поддержки получения по штрих-коду.
- Продления срока хранения посылки на ПВЗ вручения (сценарий `extendParcelStorage`), что позволяет отсрочить отправку посылки в обратном направлении.
- Запрет выдачи посылки на ПВЗ вручения (сценарий `prohibitParcelReceive`), что позволяет запретить выдачу посылки получателю например в случае признания посылки утерянной.
- Запрет приема посылки на ПВЗ приема (сценарий `prohibitParcelAcceptance`) позволяет запретить прием посылки от отправителя в случае отмены заказа на стороне Avito (сценарий находится в разработке).

Функциональность для изменения свойств посылок работает в асинхронном режиме, то есть предполагается что для изменения данных в посылке службе доставки требуется время, и состоит из двух методов, жонглируя параметрами которых можно обеспечивать работу описанных выше сценариев:

- метод `/changeParcel` - реализуется на стороне СД и предназначен для создания заявок на изменение данных ([спецификация](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/ChangeParcels)).
- метод `/changeParcelResult` - реализован на стороне Avito и предназначен для отправки результатов исполнения заявок ([спецификация](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/ChangeParcelResult)).

## Терминология

- Транзакция - один запрос для изменения свойств посылок. Транзакция может включать в себя одну или несколько заявок, которые объединены общим процессом внутри Avito. Так как заявки связаны общим процессом необходимо либо взять в работу все заявки из запроса, либо не брать ни одной.
- Заявка - составная часть транзакции. Заявка связана с ранее зарегистрированной в СД посылкой и содержит информацию о том, какие свойства посылки необходимо изменить.

## Примеры запросов

### Примеры заявок для сценария смены получателя посылки (changeReceiver)
<details>
<summary>Создаем транзакцию с одной заявкой</summary>
```json
{
    "type": "changeReceiver",
    "applications": [
        {
            "id": "42b8d1f8-6718-476c-8ebf-8b297abb607b",
            "parcelID": "P0001",
            "receiver": {
                "name": "Иванов И.И.",
                "phones": [
                    "89008007060"
                ]
            }
        }
    ]
}
```
</details>

<details>
<summary>Подтверждаем ранее зарегистрированную заявку</summary>
```json
{ 
    "id": "42b8d1f8-6718-476c-8ebf-8b297abb607b", 
    "status": "approved"
}
```
</details>


<details>
<summary>Регистрируем транзакцию с двумя заявками</summary>
```json
{
    "type": "changeReceiver",
    "applications": [
        {
            "id": "42b8d1f8-6718-476c-8ebf-8b297abb607b",
            "parcelID": "P0001",
            "receiver": {
                "name": "Иванов И.И.",
                "phones": [
                    "89008007060"
                ]
            }
        },
        {
            "id": "8af50371-8d7f-4716-b642-6482272c5f00",
            "parcelID": "P0002",
            "receiver": {
                "name": "Иванов И.И.",
                "phones": [
                    "89008007060"
                ]
            }
        }
    ]
}
```
</details>


Пример подтверждения транзакции с двумя и более заявками не отличается от ранее представленного так как процесс регистрации проходит транзакция целиком, а процесс подтверждения каждая заявка по отдельности.
То есть для примера выше необходимо обработать обе заявки и для каждой прислать отдельный запрос-подтверждение.

<details>
<summary>Подтверждаем первую заявку</summary>
```json
{ 
    "id": "42b8d1f8-6718-476c-8ebf-8b297abb607b", 
    "status": "approved"
}
```
</details>

<details>
<summary>Подтверждаем вторую заявку</summary>
```json
{ 
    "id": "8af50371-8d7f-4716-b642-6482272c5f00", 
    "status": "approved"
}
```
</details>

<hr />

### Примеры заявок для сценария продления срока хранения посылки (extendParcelStorage)
Продление срока хранения посылки - операция, которую выполняет Avito в службе доставки, по инициативе пользователя (продавца или покупателя), для продления срока хранения.
Сроком продления по умолчанию 7 календарных дней, но контракт сценария продления позволяет корректировать это значение в большую или меньшую сторону в зависимости от внутренних процессов на стороне службы доставки. 
Для кастомизации продления необходимо в запросе changeParcelResult передать параметр `storageExtendedTo` с указанием даты до которой выполнено продление.
Дату продления необходимо передавать по стандарту RFC 3339 с указанием часов и минут. Если служба доставки не использует привязку к часам/минутам в процессе продления можно использовать константное время - `23:59:59`, что будет означать продление до конца суток.

<details>
<summary>Создаем транзакцию с одной заявкой</summary>
```json
{
    "type": "extendParcelStorage",
    "applications": [
        {
            "id": "42b8d1f8-6718-476c-8ebf-8b297abb607b",
            "parcelID": "P0001",
        }
    ]
}
```
</details>

<details>
<summary>Подтверждаем ранее зарегистрированную заявку</summary>
```json
{ 
    "id": "42b8d1f8-6718-476c-8ebf-8b297abb607b", 
    "status": "approved"
    "options": {
        "storageExtendedTo": "2024-07-20T23:59:59.52Z"    
    }
}
```
</details>

Также как для сценария смены получателя, транзакция сценария продления срока хранения может содержать более одной заявки.

<hr />

### Примеры заявок для запрета выдачи посылки в ПВЗ вручения (prohibitParcelReceive)
Запрет выдачи посылки – операция, которую выполняет Avito в службе доставки, когда Avito нужно у себя признать посылку утерянной. 
Запрет выдачи гарантирует, что если получатель придет получать посылку на ПВЗ/постамат, то служба доставки не будет выдавать посылку.

<details>
<summary>Создаем транзакцию с одной заявкой</summary>
```json
{
    "type": "prohibitParcelReceive",
    "applications": [
        {
            "id": "42b8d1f8-6718-476c-8ebf-8b297abb607b",
            "parcelID": "P0001",
        }
    ]
}
```
</details>

<details>
<summary>Подтверждаем ранее зарегистрированную заявку</summary>
```json
{ 
    "id": "42b8d1f8-6718-476c-8ebf-8b297abb607b", 
    "status": "approved"
}
```
</details>

По аналогии с примерами выше заявок внутри транзакции может быть больше одной.

<hr />

### Примеры заявок для запрета приема посылки в ПВЗ отправления (prohibitParcelAcceptance)
В настоящий момент данный тип заявки находится в разработке, но внешний контракт будет иметь вид как в примерах ниже.
Запрет приема посылки – операция, которую выполняет Avito в службе доставки, когда Avito нужно у себя отменить заказ пользователей. Запрет приема подразумевает, что если отправитель придет отправлять посылку в ПВЗ / постамат, то служба доставки гарантированно не будет принимать посылку.
Данный тип заявки по своей сути является асинхронным аналогом синхронного метода [запрета приема](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/zapret_priema_posylki).

<details>
<summary>Создаем транзакцию с одной заявкой</summary>
```json
{
    "type": "prohibitParcelAcceptance",
    "applications": [
        {
            "id": "42b8d1f8-6718-476c-8ebf-8b297abb607b",
            "parcelID": "P0001",
        }
    ]
}
```
</details>

<details>
<summary>Подтверждаем ранее зарегистрированную заявку</summary>
```json
{ 
    "id": "42b8d1f8-6718-476c-8ebf-8b297abb607b", 
    "status": "approved"
}
```
</details>

<details>
<summary>Отклоняем ранее зарегистрированную заявку</summary>
```json
{ 
    "id": "42b8d1f8-6718-476c-8ebf-8b297abb607b", 
    "status": "declined",
    "reason": "already_received"
}
```
</details>

Так же как и в примерах выше внутри одной транзакции может быть больше одной заявки.

Физический смысл и назначение полей описаны в спецификации методов.

## Правила и ограничения

Для максимальной согласованности данных между Avito и СД в вопросе изменения свойств посылок необходимо зафиксировать ряд ограничений и правил работы с заявками.

### Ограничение на направление движения посылки

Для понимания этого ограничения необходимо погрузиться в контекст и разобраться с тем, как меняются роли пользователей в зависимости от направления движения посылки.
У каждой зарегистрированной в СД посылки может быть только 1 отправитель и только 1 получатель, т.е.:
- Агентский возврат: если посылки была отправлена `Пользователем 1` из населенного пункта `А` в населенный пункт `Б` для `Пользователя 2`, а `Пользователь 2` не явился для получения или отказался в момент приема после чего посылка поехала назад в населенный пункт `А`. Это обстоятельство не меняет роли отправителя и получателя посылки. `Пользователь 1` все еще отправитель, а `Пользователь 2` получатель, несмотря на то, что направление движения изменилось.
- Клиентский возврат: если посылка была отправлена `Пользователем 1` из населенного пункта `A` в населенный пункт `Б` для `Пользователя 2` и `Пользователь 2` принял посылку от СД, но после проверки дома решил вернуть купленные товары, то в таком случае в СД будет зарегистрирована специальная возвратная посылка, взамен прямой, и роли пользователей меняются на противоположные.

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/change_parcel_roles_rule.png" />
Теперь, понимая роли пользователей и как они могут меняться в следствии движения посылки, рассмотрим ограничения на сценарии:
1. Сценарий `changeReceiver` возможен только для любого получателя посылки. В первом случае это всегда `Пользователь 2`, а во втором случае это сначала `Пользователь 2`, а затем, после того как возврат поехал в новой посылке, `Пользователь 1`. При этом сценарий не доступен для отправителя, вне зависимости от направления движения.
2. Сценарий `extendParcelStorage` доступен для любой посылки, ожидающей вручения на ПВЗ/в постамате, для которой продление ранее не выполнялось. Продление срока хранения можно выполнить один раз для прямого и один раз для возвратного потока (как для клиентского, так и для агентского возврата)
3. Сценарий `prohibitParcelReceive` может быть применён для любого получателя посылки, т.к. утеря может случиться как на прямом движении посылки, так и на каждом из двух типов возвратов.
4. Сценарий `prohibitParcelAcceptance` может быть применён для любой посылки, которая не начала своего движения от отправителя к получателю. Например: когда `Пользователем 1` еще не отнес посылку в пункт приема или `Пользователем 2` еще не отнес возврат в пункт приема.

### Ограничение на обработку транзакции
 
 В подкатегории "Примеры запросов" есть описание этого ограничения: если в транзакции передано несколько заявок, то необходимо принять в работу все перечисленные заявки, или полностью отклонять транзакцию.
 Требование обусловлено тем, что заявки внутри транзакции всегда связаны внутренним процессом внутри Avito, то есть для Avito все N-заявок внутри транзакции одно целое и непринятие одной перечеркивает те, что могут быть приняты в работу.

> [!IMPORTANT]
> Процесс обработки запроса на регистрацию заявок должен содержать только валидации проверки входящего контракта!
> Т.е можно отклонять заявки на этапе регистрации, если не передан обязательный параметр для данного типа заявки или переданный тип заявки не поддерживается на стороне СД.
> Нельзя на этапе регистрации выполнять проверки бизнес-логики, как например существование в системе СД посылки с переданным номером. Такие проверки необходимо выполнять в процессе обработки заявки и результат отправлять через ответный запрос.

 После того как транзакция со всеми заявками внутри успешно зарегистрирована результаты по заявкам необходимо отправлять отдельными запросами. Рассмотрим это ограничение на примере сценария changeReceiver.
 <img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/change_parcel_transaction_rule.png" />

### Ограничение на состояние посылки

### Для сценария changeParcel

Смена получателя посылки может быть произведена строго до момента вручения или отправки посылки на возврат, то есть
когда посылка находится в статусе `IN_TRANSIT` (в пути) или `ON_DELIVERY` (находится на ПВЗ и ожидает вручения). 

### Для сценария extendParcelStorage

Продление срока хранения возможно только в статусе `ON_DELIVERY` (находится на ПВЗ и ожидает вручения), т.е. после фактического поступления посылки в ПВЗ вручения.

### Для сценария prohibitParcelReceive

Процесс запрета выдачи на ПВЗ вручения может быть запущен для любого статуса из которого возможен переход в статус LOST. Проверить возможность такого перехода можно обратившись к [графу переходов](https://al-29957-developers.k.avito.ru/api-catalog/delivery-sandbox/documentation#info/mehanika_raboty_trekinga)

Данные ограничения реализованы на стороне Avito (заявки для посылок в других статусах не должны поступать в СД). 
Но в том случае, если между Avito и службой доставки произошел рассинхрон в части отправки статусов, возможны случаи попыток регистрации заявок для посылок в неподходящих для сценария статусах.

### Для сценария prohibitParcelAcceptance

Процесс запрета приема посылки может быть выполнен:
- до момента сдачи продавцом посылки в ПВЗ отправки.
- до момента сдачи покупателем клиентского возврата в ПВЗ отправки.


### Вытеснение заявок

Данный тип ограничения в большей степени относится к сценарию changeReceiver, так как помимо номера посылки в службу доставки так же передаются данные нового получателя. 
В сценариях `extendParcelStorage`, `prohibitParcelReceive` и `prohibitParcelAcceptance` таких данных нет, но принципом вытеснения можно руководствоваться в случае нештатных ситуаций, например: если поступило несколько заявок для продления срока хранения (или запретом выдачи) с одинаковым `parcelID` и разными `id` заявки, скорее всего причина этому сбой и исполнять стоит последнюю из поступивших, аннулировав предыдущие.
Заявки носят вытесняющий характер, то есть новая поступившая заявка аннулирует ранее созданную.
Данное ограничение проще разобрать на примере:
1. Avito регистрирует транзакцию с одной заявкой для посылки P0001.

<details>
<summary>Пример</summary>
```json
{
    "type": "changeReceiver",
    "applications": [
        {
            "id": "42b8d1f8-6718-476c-8ebf-8b297abb607b",
            "parcelID": "P0001",
            "receiver": {
                "name": "Иванов И.И.",
                "phones": [
                    "89008007060"
                ]
            }
        }
    ]
}
```
</details>

2. Avito регистрирует новую транзакцию с тем же типом и номером посылки P0001. При этом id заявки и данные получателя отличаются от ранее созданной заявки.

<details>
<summary>Пример</summary>
```json
{
    "type": "changeReceiver",
    "applications": [
        {
            "id": "a6679531-e755-4148-8545-570217635d2b",
            "parcelID": "P0001",
            "receiver": {
                "name": "Петров П.П.",
                "phones": [
                    "89001002030"
                ]
            }
        }
    ]
}
```
</details>

3. Ожидается аннулирование заявки из п.1.
<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/change_parcel_update_rule.png" />

# Песочница

Для тестирования интеграции с Avito партнерская служба доставки может использовать "Песочницу".

"Песочницей" называем набор API-методов, работающих только в тестовой (staging) среде, позволяющих партнерской службе
доставки самостоятельно "триггерить" Avito на выполнение некоторых действий в службе доставки, то есть самой в себе.

Пример такого действия – создание посылки, т.к. в процессе создания посылки Avito выполняет запрос в API партнера, а не 
наоборот. Если представить, что Песочницы не существует, то чтобы по-честному протестировать интеграцию инженерам из 
службы доставки надо попросить инженеров Avito "понажимать на своей стороне кнопки", чтобы Avito в конечном итоге 
выполнило определенный запрос на определенный URL партнера, за которым стоит обработчик по созданию посылок. Песочница 
помогает исключить из процесса тестирования момент, когда инженеры друг с другом договариваются о времени тестирования, 
и позволяет инженерам из службы доставки выполнять его в удобное для себя время. То есть инженер СД сам выполняет 
[запрос на создание тестовой посылки](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/CreateSandboxParcelV1),
и в конечном итоге Avito придет с запросом в тестовый контур партнера.

Что можно "триггерить" через Песочницу на текущий момент:
- Создание тестовых посылок.
- Запрет приема тестовых посылок.
- Продление срока хранения заказа
- Изменение свойств тестовых посылок.
- Создание тестовых анонсов для кросс-доставки.

> [!TIP]
> Для выполнения запросов в Песочницу генерите токен с помощью пары client_id + client_secret, полученной для тестового
> (staging) окружения.

## Создание тестовых посылок

Базовый метод Песочницы, позволяющий создать основную сущность "Посылка", по которой Avito и партнерская служба доставки
взаимодействуют.

OpenAPI-контракт метода расположен [здесь](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/CreateSandboxParcelV2).

Метод запускает процесс создания тестовой посылки. При успешном выполнении в ответе должен быть идентификатор заказа 
(orderID), по которому можно получить ID зарегистрированной посылки с помощью соответствующего [метода](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/v1getRegisteredParcelID).

<br/>

Механика работы приведена на диаграмме.

<img style="max-width:100%" src="https://avito.st/static/ims/82bc9b5c-c46f-417f-ac58-1227857b5fae_sandbox_creating_parcels_common_1108x753.png" />

> [!TIP]
> Обратите внимание, что по умолчанию посылка не будет зарегистрирована у вас в системе. Если это необходимо,
> используйте параметр options.registrationUrl.

<br/>

> [!IMPORTANT]
> Обратите внимание, что посылка создается не синхронно! В ответ на вызов метода /v1/getRegisteredParcelID какое-то
> время можно получать ошибку NOT_REGISTERED. В этом случае надо немного подождать и повторить попытку получения ID
> посылки.

### Возможности метода

#### Регистрация посылок внутри вашей системы
Ссылку можно передавать в поле `options.registrationUrl`.

Передавайте сюда URL, ведущий на реализованный в вашей системе [метод регистрации посылки](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/createParcel).

На `registrationUrl` Avito сделает запрос на создание посылки. Тем самым посылка будет создана в вашей системе.

<details>
<summary>Пример</summary>
```json
{
  "options": {
    "registrationUrl": "https://staging.delivery-partner.ru/createParcel"
  }
}
```
</details>

#### Создание B2C посылок
Описание работы B2C расположено [здесь](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/b2c-pvz_scenariy).

В поле `tags` необходимо передавать `B2C`.

Если необходимо добавить конкретный ИНН пользователю - необходимо добавить `sender.inn` поле.

<details>
<summary>Пример</summary>
```json
{
  sender: {
    inn: "123456789012"
  },
  "tags": ["B2C"]
}
```
</details>  

#### Создание кросс-доставочных посылок
Описание работы кросс-доставки FBS расположено [здесь](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/kross-dostavka).

В поле `tags` необходимо передавать 2 тега:
- `X_DELIVERY` и `X_DELIVERY_LAST_LEG`: создаст посылку на последнем плече.

<details>
<summary>Пример с указанным плечом</summary>
```json
{
  "tags": ["X_DELIVERY", "X_DELIVERY_LAST_LEG"]
}
```
</details>  

#### Создание корзинной посылки
Описание работы "Корзины" расположено [здесь](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/korzina).

Чтобы создать корзинную посылку, передавайте в `tags` `["CART"]`, а также необходимо выполнить 1 из условий:
- Количество товаров items больше 1.
- Указано количество товара items.quantity больше 1.

<details>
<summary>Пример 1 условие</summary>
```json
{
  "tags": ["CART"],
  "items": [
    {"quantity": 1},
    {"quantity": 1}
  ]
}
```
</details> 

<details>
<summary>Пример 2 условие</summary>
```json
{
  "tags": ["CART"],
  "items": [
    {"quantity": 2}
  ]
}
```
</details>

#### Создание посылки в сценарии C2C терминал-дверь
Описание работы "C2C Терминал-Дверь" расположено [здесь](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/c2c_terminal-dver_scenariy).

Чтобы создать посылку терминал-дверь, передавайте в `tags` `["T2D"]`.

<details>
<summary>Пример</summary>
```json
{
  "tags": ["T2D"]
}
```
</details>

Также вы можете изменять параметры сценария (подробнее читайте в описании полей [здесь](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/CreateSandboxParcelV2)).

**Важно**: передавая ```receiver.delivery.courier.address```, вы должны также передавать ```receiver.delivery.courier.dateTimeInterval``` (либо не передавайте оба объекта).

<details>
<summary>Пример</summary>
```json
{
  "tags": ["T2D"],
  "receiver": {
    "delivery": {
      "courier": {
        "address": {
          "addressRow": "Санкт-Петербург, ул. Обручевых, д. 6, подъезд 5, этаж 2, кв. 512",
          "details": {
            "house": "6",
            "floor": "2",
            "porch": "5",
            "flat": "512"
          },
          "coordinates": {
            "latitude": 55.756133,
            "longitude": 37.620492
          }
        },
        "dateTimeInterval": {
          "start": "2025-03-02T12:14:29+03:00",
          "end": "2025-03-05T12:14:29+03:00"
        },
        "options": {
          "elevatorAvailable": false,
          "comment": "Комментария для курьера."
        }
      }
    }
  }
}
```
</details>

### Пример использования
1. Создание посылки. Вызываете метод создания тестовой посылки и получаете `orderID`.
2. Получение ID посылки. Используя `orderID`, [запрашиваете](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/v1getRegisteredParcelID) ID посылки. Если посылка еще не зарегистрирована,
   вы получите ошибку `NOT_REGISTERED`. В этом случае подождите и повторите запрос.
3. Тестирование трекинга. С полученным ID посылки вызываете [метод](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/tracking) трекинга для проверки его работы.

## Запрет приема тестовых посылок

Метод Песочницы, позволяющий партнерской службе доставки инициировать 
[запрет приема](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/prohibitOrderAcceptance) 
ранее созданной тестовой посылки.

OpenAPI-контракт метода расположен [здесь](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/v1CancelParcel).

Механика работы приведена на диаграмме.

<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/sandbox-parcel-prohibit-acceptance.png" />

> [!IMPORTANT]
> Обратите внимание, что метод будет работать только для тестовых посылок, созданных с помощью [метода](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/CreateSandboxParcelV2).

## Продление срока хранения заказа

Метод Песочницы, позволяющий партнерской службе доставки инициировать продление срока хранения ранее созданной тестовой посылки.

OpenAPI-контракт метода расположен [здесь](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/v1changeParcel).

POST запрос на URL [/delivery-sandbox/v1/changeParcel](https://api.avito.ru/delivery-sandbox/v1/changeParcel) необходимо делать с указанием `type=extendParcelStorage`.
Пример запроса находится [здесь](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/primery_zaprosov).

> [!IMPORTANT]
> Обратите внимание, что метод будет работать только для тестовых посылок, созданных с помощью [метода](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/CreateSandboxParcelV2).

## Изменение свойств тестовых посылок

Метод Песочницы, позволяющий партнерской службе доставки инициировать
[изменение](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/ChangeParcels)
ранее созданной тестовой посылки.

OpenAPI-контракт метода расположен [здесь](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/v1changeParcel).

Механика работы Песочницы для сценариев приведена на диаграммах ниже. Общая механика работы процесса описана
[здесь](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/izmenenie_svoystv_posylok).

<details>
<summary>Сценарий изменения ФИО и номера телефона получателя посылки.</summary>
<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/sandbox-parcel-change-data.png" />
</details>

<details>
<summary>Сценарий запрета выдачи посылки в ПВЗ вручения.</summary>
<img style="max-width:100%" src="https://www.avito.st/s/avito/components/api-description/delivery/images/prophibit_parcel_receive_scheme.png" />
</details>

> [!IMPORTANT]
> Обратите внимание, что метод будет работать только для тестовых посылок, созданных с помощью [метода](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/CreateSandboxParcelV2).

## Создание тестовых анонсов для кросс-доставки
TO BE DESCRIBED.

# Авторизация
## Доступ к методам Avito
Для доступа к вызовам методов API, которые реализованы на стороне Avito, необходимо 
получить токен авторизации с помощью [метода](https://developers.avito.ru/api-catalog/auth/documentation#operation/getAccessToken). 
Секреты для авторизации `client_id` и `client_secret` вам дадут инженеры Avito.

Полученный токен необходимо передавать в заголовке `Authorization: Bearer <token>`.

Токен имеет определенный срок жизни (на данный момент это 24 часа). Рекомендуется запрашивать токен 1 раз и использовать
его в течении срока жизни во всех воркерах, которые делают запросы в Avito. Нет необходимости получать токен для каждого
отдельного запроса.

## Доступ к методам СД
Доступ к методам СД осуществляется через **единый** **постоянный** токен, который Avito передает в заголовке 
`Authorization: Bearer <token>`.

Должна быть предусмотрена возможность безопасной смены токена авторизации по требованию Avito в течении одного рабочего дня. 
В случае, если при вызове метода был передан неверный токен, должен вернуться HTTP-код 401.

# Часто совершаемые ошибки

## Ошибки в создании посылок

**Излишние VALIDATION_ERROR-ы**

`VALIDATION_ERROR` означает, что содержимое запроса некорректно. Например, длина товара в посылке превышает допустимые лимиты,
или какое-то обязательное поле отсутствует.

`VALIDATION_ERROR` – "**терминальная**" ошибка, т.е. не имеет смысла повторять запрос, так как будет получен такой же результат.
Получение любой такой ошибки при создании посылки приводит к автоматической отмене соответствующего заказа на Avito.

Нельзя возвращать ошибку `VALIDATION_ERROR`, если случилась внутренняя инфраструктурная ошибка или какая-то другая ошибка,
повторный запрос по которой может привести к успеху.

**Излишняя валидация номеров телефонов**

Формат номеров телефонов может быть произвольным. Добавлять блокирующую валидацию на какой-то конкретный формат номера нельзя.

**Излишняя валидация имени отправителя**

Добавлять блокирующую на то, что Avito передает в имени отправителя настоящее ФИО нельзя.  Формат имени отправителя 
может быть произвольным.

В имени отправителя могут быть произвольные символы / эмодзи. Блокировать из-за них создание посылки нельзя.

Процесс оформления заказа на Avito устроен таким образом, что только получатель посылки указывает
настоящее и полное ФИО (Avito это контролирует), но ФИО отправителя мы не знаем. Мы знаем его никнейм, который он
указал при регистрации на сайте.

**Игнорирование требований идемпотентности к обработчикам**

Обратите внимание на требование идемпотентности, которые предъявляются к обработчикам, реализуемых на вашей стороне. 
Предусматривайте её с самого старта, т.к. это поможет сделать интеграцию более надежной в условиях походов друг в друга по
сети.

Особенно плохой будет реализация обработчика, который будет отдавать терминальную ошибку `VALIDATION_ERROR` на повторные
запросы.

**Путаница с orderID и parcelID**

В поле `orderID` Avito указывает номер **заказа**. Это поле добавлено для будущей реализации многоместности / консолидации.
Сейчас ни то, ни другое не поддерживается, поэтому обрабатывать / использовать это поле пока не нужно.

`parcelID` – номер посылки. Это главный идентификатор основной сущности, по которой Avito работает со службой доставки по части
процессинга – **посылки**. Со службами доставки мы работаем по **посылкам**. Avito создает посылку в службе доставки, 
Avito запрещает прием посылки, по посылке СД присылает треки, настоящий ПВЗ сдачи, ВГХ и стоимость доставки.

**Некорректный алгоритм определения итоговых габаритов**

В процессе обработки запроса на создание посылки с несколькими товарами вы должны проверять, что все товары "влезают"
в одну посылку. Если вы понимаете, что товары из посылки в совокупности превышают максимальный вес или габариты, то
возвращайте ошибку `VALIDATION_ERROR` с поясняющим текстом. 

Из этого всего следует, что у вас должен быть какой-то алгоритм, который считает итоговые габариты посылки по вложенным
в нее товарам. Обязательно провалидируйте алгоритм, который считает общие габариты товаров, с инженерами Avito. 
Обращаем внимание, что простое сложение измерений товаров в посылке не дает корректные итоговые габариты посылки.

**Нетолерантность к отсутствию картинок**

Картинки в запросе на создание посылки могут отсутствовать, это нормальная ситуация. Реакцию на посылки, в которых
нет картинок, согласуйте с операционными менеджерами Avito.

**Нетолерантность к новым тегам**

В поле `options.tags` Avito может без предварительного уведомления добавлять новые теги. Реагируйте только на известные
вам теги. Если вы видите в запросе незнакомые или ничего для вас незначащие теги, то игнорируйте их, а не отбивайте запрос
с ошибкой.

**Неуникальные dispatchNumber / trackingNumber**

`dispatchNumber` и `trackingNumber` должны быть уникальными. Они не должны повторяться для разных посылок.

Но у одной посылки `dispatchNumber` и `trackingNumber` могут быть одинаковыми.

Единственное исключение из этого правила – постаматный сценарий, где `dispatchNumber` – это код для закладки или получения
посылки в постамате. Этот код у постаматных служб доставок, как правило, аннулируется после закрытия посылки и может
выдаваться повторно.

**Жесткий рейтлимитер на стороне СД**

На стороне СД может быть настроен [рейтлимитер](https://en.wikipedia.org/wiki/Rate_limiting) на входящие от Avito запросы. 
Не делайте настройки рейтлимитера слишком жесткими, оставляйте приличный запас сверху от нормального фона запросов. Он
пригодится, например, в случае восстановлений после аварий, когда на стороне Avito скопилась большая очередь на создание посылок.
Avito будет с большой интенсивностью её "разбирать" и рейтлимитер не должен сильно снижать скорость её "разбора".

**В ответе возвращать одновременно объект data и объект error**

В теле ответа должен быть либо объект `data` либо `error`.

```json
{
  "data": {
    "dispatchNumber": "80512198042480",
    "trackingNumber": "80512198042480"
  }
}
```

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Текст ошибки"
  }
}
```

## Ошибки в трекинге

**Ранний IN_TRANSIT_RETURN при истечении срока хранения**

Первый статус `IN_TRANSIT_RETURN`  означает, что посылка начала движение обратно к отправителю. Первый `IN_TRANSIT_RETURN` 
нужно присылать в тот момент, когда получатель гарантированно не сможет забрать посылку. 

Поэтому если мы говорим о случае, когда истекает срок хранения, то здесь можно присылать два разных трека: 
- `IN_TRANSIT_RETURN` \+ `STORE_TERM_FINISHED` если гарантируется, что получатель не сможет забрать посылку.
- `ON_DELIVERY` \+ `STORE_TERM_FINISHED` если после окончания срока хранения посылка еще какое-то время доступна для 
получения. Например, она доступна до тех пор, пока не приедет транспорт и не повезет посылку в сортировочный центр.

**Ранний ON_DELIVERY**

Статус `ON_DELIVERY` означает, что посылка готова к выдаче получателю. При получении трека с этим статусом Avito явно
ему сообщает, что можно идти посылку забирать.

Не присылайте `ON_DELIVERY`, если посылка только прибыла в город получения, но еще недоступна для выдачи.

**Ранний DELIVERED**

Статус `DELIVERED` означает, что посылка выдана получателю. Это терминальный статус, после которого посылка "закрывается".
После статуса `DELIVERED` не может идти возвратный статус `IN_TRANSIT_RETURN`. Если посылка выдана, то [агентский возврат](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/agentskie_vozvraty)
становится невозможен, получатель может запросить только [клиентский возврат](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/klientskie_vozvraty) 
через Avito.

**Ранний DELIVERED в оплате при получении**

Присылайте `DELIVERED` только тогда, когда покупатель произвел оплату.

**Ранний IN_TRANSIT_RETURN**

Статус `IN_TRANSIT_RETURN` означает, что посылка возвращается к своему отправителя. Этот статус у посылки возникает
в случае [агентского возврата](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#info/agentskie_vozvraty). 
Выдача, т.е. статус `DELIVERED`, после агентского возврата невозможен. Если посылка находится в Avito в статусе 
`IN_TRANSIT_RETURN`, то треки с `DELIVERED` приниматься не будут.

## Прочие ошибки

**Прием посылки после того, как Avito по ней вызывал метод запрета приема**

Служба доставки должна гарантировать, что не будет принимать посылку у отправителя, если до этого Avito вызвало 
[метод запрета приема](https://developers.avito.ru/api-catalog/delivery-sandbox/documentation#operation/prohibitOrderAcceptance).
