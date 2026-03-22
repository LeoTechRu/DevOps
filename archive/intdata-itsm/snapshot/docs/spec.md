# ITSM Module — архитектурный план

## Цели
- Предоставить единый код для работы с тикетами, событиями и Flowable между модулями Nexus (клиентский фронт) и CRM (рабочее место специалистов).
- Сохранить хранение данных в общих схемах PostgreSQL (`nexus_itil`) без дублирования логики и миграций.
- Чётко разделить ответственность: модуль `itsm` предоставляет примитивы, Nexus и CRM реализуют UI/API на своей стороне.

## Структура пакета `itsm`
```
itsm/
├── __init__.py           # экспорт enums, DTO и сервисов
├── enums.py              # ITSMTicketStatus, ITSMTicketPriority, ITSMEventType
├── dto.py                # Pydantic-схемы для обмена между модулями
├── models.py             # SQLAlchemy таблицы, маппинг на схему nexus_itil
├── repository.py         # CRUD / запросы к тикетам и событиям
├── flowable/client.py    # Общий Flowable REST-клиент + датакласс FlowableConfig
└── acl.py                # Константы разрешений и роли (client, specialist, manager)
```

## Компоненты
### 1. Enums (`enums.py`)
- Уже перенесены из Nexus. Используются в моделях, DTO и UI.

### 2. DTO (`dto.py`)
- `Ticket` — модель ответа (public_id, title, status, priority, para, created_by, due_at, meta, events, visibility).
- `TicketCreate` / `TicketUpdate` — входные данные (используются Nexus и CRM).
- `TicketEvent` — история (event_type, payload, actor, created_at, visibility).
- `TicketQuery` — параметры фильтрации (status, priority, created_by, assigned_to, audience, limit/offset).
- DTO основаны на Pydantic v1 (совместимость с существующим кодом).

### 3. Models (`models.py`)
- SQLAlchemy декларации `ITSMTicket` и `ITSMTicketEvent` переезжают из `nexus/api/models.py` в модуль `itsm`.
- Таблицы по-прежнему находятся в схеме `itsm_tickets`, `itsm_ticket_events` (`schema="nexus_itil"` если захотим указать явно).
- Подключаемся к Base из `shared.db` (дальнейшая задача — выделить собственный Base/AppConfig внутри `itsm`, либо продолжать использовать общий, пока это оправдано).
- Nexus и CRM будут ссылаться на эти модели через `itsm`, evitando duplication.

### 4. Repository (`repository.py`)
- Функции: `list_tickets`, `get_ticket_by_id`, `get_ticket_by_public_id`, `create_ticket`, `update_ticket`, `add_event`, `filter_by_subject`, `filter_by_account`.
- Асинхронные функции работают с `AsyncSession`, совместимы с текущим `itsm.db.async_session()` (или внешними сессиями, передаваемыми извне).
- Реализует бизнес-правила видимости: клиент видит только свои тикеты и события с `visibility in {client, public}`.

### 5. Flowable Client (`flowable/client.py`)
- Клиент вынесен из Nexus; конфигурация формируется через `itsm.config.build_flowable_config` (base_url, auth, process_key).
- Nexus и CRM передают параметры через `ITSMSettings` (env или DI), что упрощает отключение Flowable на dev.

### 6. ACL (`acl.py`)
- Константы разрешений/ролей: `PERM_CLIENT_READ`, `PERM_CLIENT_WRITE`, `PERM_SPECIALIST_MANAGE`, `PERM_MANAGER_REPORTS`.
- Хелперы для проверки доступа (например, `can_view_ticket(subject, roles, ticket)`), чтобы избежать дублирования логики между модулями.

## API контракт Nexus ↔ CRM
- **Nexus**:
  - REST `/api/nexus/v1/itsm/*` сохраняет клиентские операции (create, update self, fetch own tickets).
  - CLI `nexusctl` вызывает те же эндпоинты / фасады `itsm`.
  - Wiki/knowledge база работает отдельно, но может ссылаться на `itsm.dto.Ticket` для контекста.
- **CRM**:
  - Новый эндпоинт (например, `/api/crm/v1/itsm/*`) или UI в CRM для специалистов.
  - Использует репозиторий из `itsm` для выдачи списков тикетов, назначений, эскалаций.
  - Может интегрироваться с CRM объектами (аккаунты, подписки) через пара-ключи (`para_container_type/id`).
- **Общий транспорт**: GitHub Project синхронизация остаётся в Nexus (`nexusctl`), но CRM может инициировать обновления через фасады модуля `itsm` (хуки/интеграции).

## Миграции и схема
- Миграции перемещены в `itsm/db/migrations`; Nexus больше не хранит ITSM-таблицы.
- Требуется добавить явную схему в моделях (например, `__table_args__ = (schema="nexus_itil", ...)`) — сверить с текущими миграциями.
- После переноса моделей нужно убедиться, что alembic видит изменения (возможно, обновить импорты в миграционных env).

## Последовательность работ
1. (Выполнено) Создать `itsm/dto.py`, `repository.py`, `flowable/client.py`, `acl.py`, вынести модели в `itsm/models.py`.
2. Обновить Nexus: перевести все вызовы на `itsm` (REST фасады, CLI, webhook) и удалить временные прокси после миграции.
3. Подготовить CRM: добавить зависимость на `itsm`, реализовать сервис специалистов поверх репозитория.
4. Расширить тесты: unit для репозитория, интеграционные для Nexus/CRM, smoke Flowable.
5. Документация: держать в актуальном состоянии README, паспорт объектов и runbook.

## Риски
- Разделение моделей может затронуть alembic (нужно обеспечить корректный импорт Base).
- Потенциальные расхождения при одновременных изменениях Nexus/CRM — нужна версия itsm и фиксирование зависимостей.
- ACL-требования: отсутствие общего сервиса доступа может привести к дублированию — важно развивать общий helper прямо в `itsm.acl` и синхронизировать его с `/id`.

## Открытые вопросы
- Нужен ли общий слой для вложений/файлов (S3/MinIO) уже сейчас или вынести позже?
- Следует ли выделить отдельные BPMN для специалистов (CRM) модуля или использовать единый процесс с разными заданиями?
- Как проводить совместное тестирование Flowable (где хранить тестовые диаграммы, как запускать smoke в CI)?
