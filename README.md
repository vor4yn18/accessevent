# AccessEvent — платформа инклюзивных мероприятий
 
Веб-сервис для поиска и организации мероприятий, доступных людям
с нарушениями слуха: визуальные уведомления, текстовый чат, фильтр
инклюзивных событий.
 
## Стек
| Слой | Технологии |
|---|---|
| Backend | Python 3.11, Flask, SQLAlchemy |
| Frontend | Jinja2, HTML/CSS/JS |
| БД | PostgreSQL 16 |
| CI/CD | GitHub Actions, Docker, GHCR |
 
## Запуск
1. docker compose up — затем открыть http://localhost:5000
2. Или вручную: python -m venv venv; pip install -r requirements.txt;
   настроить .env; python app.py
 
## Тесты
pip install -r requirements.txt && pytest -v
 
## Структура проекта
routes/ — API; models.py — 8 таблиц; templates/ — интерфейс;
docs/ — вся документация; tests/ — pytest.
 
## Документация
- docs/tz.md — техническое задание
- docs/architecture.md, docs/schema.sql, docs/er_diagram.png
- docs/security.md — роли и JWT
- docs/test_cases.md, docs/bug_reports.md
- docs/user_manual.md, docs/admin_manual.md, docs/api.md
- docs/assessment.md — SWOT и модернизация
- docs/presentation.pptx — презентация защиты
 
## Docker-образ
ghcr.io/ВАШ_ЛОГИН/accessevent:latest
