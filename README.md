# FacePass: Система учёта рабочего времени с анти-фродом

### Используемые методы API Tevian:
- /api/v1/galleries: Создание базы данных сотрудников.

- /api/v1/faces (POST): Добавление сотрудника в базу. API вернет face_id, который мы свяжем с именем сотрудника в своей БД.

- /api/v1/search: Отправка фото с камеры, API ищет совпадение по всей базе сотрудников.

### Список сервисов:
 - Biometric Service (Wrapper). Работает напрямую с API Tevian.
 
 - Employee Core Service. Учет сотрудников, расписаний и логов прохода.

 - Notification Service. Отправка алертов в Telegram/Email (опоздания, попытки взлома).
 
 - Frontend (Client) — Визуальная часть (Админка + Терминал).

### Стек

Python 3.11+

FastAPI

PostgreSQL

SQLAlchemy (Async) + Alembic (для миграций)

RabbitMQ

pydantic-settings (конфиги), aio-pika (RabbitMQ), httpx (запросы к Tevian), pytest (тесты).
