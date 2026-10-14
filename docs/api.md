## Развёртывание
1. docker compose up — приложение на http://localhost:5000.
2. Альтернатива: python app.py с настроенным .env.
 
## Переменные окружения (.env)
 
| Переменная | Назначение |
|---|---|
| SECRET_KEY | подпись JWT-токенов |
| DATABASE_URL | строка подключения к PostgreSQL |
 
## Роли и права
См. docs/security.md (таблица ролей с наследованием).
 
## Резервное копирование
pg_dump -U postgres accessevent > backup.sql
Восстановление: psql -U postgres accessevent < backup.sql
 
## Типовые проблемы
1. Порт 5000 занят — остановите предыдущий процесс.
2. connection refused — служба PostgreSQL не запущена (services.msc).
3. password authentication failed — пароль в .env не совпадает с БД.
4. Контейнер не видит базу — проверьте db:5432 в DATABASE_URL.
5. Тесты стёрли данные — запускались без TESTING=1 (в эталоне исправлено).
# API AccessEvent
 
| Метод | URL | Доступ | Вход (JSON) | Ответы |
|---|---|---|---|---|
| POST | /api/register | гость | username, email, password, role | 201 / 400 |
| POST | /api/login | гость | email, password | 200 token / 401 |
| GET | /api/events | все | - | 200 список |
| GET | /api/events/<id> | все | - | 200 / 404 |
| POST | /api/events | organizer, admin | title, event_date, ... | 201 / 400 / 401 / 403 |
| DELETE | /api/events/<id> | organizer, admin | - | 200 / 403 |
| GET | /api/health | все | - | 200 {"status":"ok"} |
| POST | /api/events/<id>/register | авторизованный | - | 201 / 400 |
| GET | /api/my/registrations | авторизованный | - | 200 |
| PATCH | /api/registrations/<id> | organizer, admin | status | 200 / 400 / 403 |
| GET | /api/notifications | авторизованный | - | 200 |
| POST | /api/notifications/read | авторизованный | - | 200 |
| GET | /api/events/<id>/messages | все | - | 200 |
| POST | /api/events/<id>/messages | авторизованный | message | 201 / 400 |
| GET | /api/events/<id>/reviews | все | - | 200 |
| POST | /api/events/<id>/reviews | авторизованный | rating, comment | 201 / 400 |
 
### Примеры
POST /api/register:
{"username": "anna", "email": "anna@mail.ru", "password": "Passw0rd!", "role": "user"}
Ответ: {"message": "Пользователь создан", "user_id": 1}
 
POST /api/events:
{"title": "Кинопросмотр", "event_date": "2026-12-01 12:00", "is_inclusive": true}
Ответ: {"message": "Мероприятие создано", "event_id": 1}
 
POST /api/events/1/messages:
{"message": "Здравствуйте!"}
Ответ: {"message": "Сообщение отправлено", "message_id": 1}
