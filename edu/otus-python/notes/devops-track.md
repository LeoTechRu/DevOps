# DevOps Track

Выжимка из курса `Python Developer. Basic` только по темам, которые дают практическую пользу для DevOps/SRE/automation-стека.

## 1. База для automation

- `7` Работа с файлами // ДЗ
  - полезно для CLI-утилит, локальных агентов, генерации конфигов, log processing.
- `11-15` Модули, тесты, встроенная библиотека
  - это фундамент для скриптов, служебных утилит и внутренних automation-tools.

## 2. HTTP, API и сервисная логика

- `16-21`
  - HTTP/API, FastAPI, роутеры, валидация тела запроса.
  - Это прямая база для служебных API, webhook handlers, probe/bridge сервисов.

Связанные артефакты в архиве:

- `homework-repo/homework_04/` — async API + БД
- `homework-repo/homework_05/` — первое FastAPI-приложение

## 3. Контейнеризация и app runtime

- `23` Docker // ДЗ
- `34` docker compose, сети контейнеров, nginx, gunicorn/uvicorn

Это уже не «язык ради языка», а старт production-мышления:

- сборка образа;
- связка приложения и БД;
- конфигурация через окружение;
- проксирование и запуск в более реалистичном контуре.

Связанные артефакты в архиве:

- `homework-repo/homework_03/` — ранний Docker-кейс
- `homework-repo/homework_06/` — FastAPI + БД + `docker-compose` + `nginx`

Отдельно:

- `python/labs/fastapi-compose-notes/` — альтернативный lab на ту же тему, выделенный из legacy `studyPython/homework_05/`.

## 4. Базы данных и миграции

- `25` SQL и реляционные БД
- `26-29` SQLAlchemy, связи, alembic, сложные отношения
- `32-33` асинхронная работа API с БД

Это критично для backend-инженерии, интеграционных сервисов и любых automation-платформ, где есть:

- state;
- event storage;
- migrations;
- data integrity;
- rollback thinking.

Связанные артефакты в архиве:

- `homework-repo/homework_04/` — async SQLAlchemy + API
- `homework-repo/homework_06/` — web + DB integration

## 5. Django как база для “админских” внутренних систем

- `36-45`
  - Django, ORM, формы, CBV, pytest, Celery, Redis.

Это особенно полезно не как “делать сайты”, а как:

- быстро собирать внутренние admin-панели;
- делать CRUD для операторских сущностей;
- выносить фоновые задачи в очередь;
- тестировать service-layer и Django views.

Связанные артефакты в архиве:

- `homework-repo/homework_07/`
- `homework-repo/homework_08/`
- `homework-repo/homework_12/` — задачи Celery

## 6. CI/CD блок, который реально нужен дальше

- `48` GitHub Actions // ДЗ
- `49` GitLab CI // ДЗ
- `50` GitLab CD

Это самый прямой мост из курса в `DevOps`:

- пайплайны запуска тестов;
- автоматизация сборки;
- работа с registry;
- артефакты;
- базовый deploy flow.

Связанные артефакты в архиве:

- `homework-repo/.github/workflows/`
- `homework-repo/.gitlab-ci.yml`

## Практический вывод

Для текущей траектории в `DevOps` курс полезен не как “ещё один Python-курс”, а как набор ступеней:

1. скрипты и файловая автоматизация;
2. API и backend-сервисы;
3. контейнеризация;
4. БД и миграции;
5. фоновые задачи;
6. CI/CD.

Именно поэтому этот архив лежит в `python/courses/`, а не в безымянной свалке `BasePython`.
