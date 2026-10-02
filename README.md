# QRKot

API благотворительного фонда поддержки котов. Фонд ведёт проекты и собирает на них пожертвования. Пожертвования не привязаны к конкретному проекту: сервис автоматически распределяет их по открытым проектам в порядке создания, а проект закрывается, когда нужная сумма собрана.

## Эндпоинты

- `GET /charity_project/` — публичный список проектов
- `POST /charity_project/`, `PATCH` и `DELETE /charity_project/{project_id}` — управление проектами для суперпользователя
- `POST /auth/register`, `POST /auth/jwt/login` — регистрация и вход с Bearer/JWT
- `GET`, `PATCH /users/me` и `GET`, `PATCH /users/{id}` — эндпоинты пользователей
- `POST /donation/` — пожертвование только для авторизованного пользователя
- `POST /yandex/` — загрузка отчёта о закрытых проектах на Яндекс Диске для суперпользователя

В режиме разработки API доступно по адресу http://127.0.0.1:8000.
Интерактивная документация: http://127.0.0.1:8000/docs (Swagger) и http://127.0.0.1:8000/redoc (Redoc).

## Запуск проекта

1. Создайте и активируйте виртуальное окружение, установите зависимости
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
2. Создайте и заполните `.env` файл. Для токенов задайте `QRKOT_SECRET`, а для отчётов — `QRKOT_YANDEX_DISK_TOKEN`
```bash
cp .env.example .env
```
3. Произведите миграции, будет создан файл базы `fastapi.db` с таблицами `charityproject`, `donation` и `user`
```bash
alembic upgrade head
```
4. Запустите сервер разработки
```bash
uvicorn app.main:app --reload
```

## Стек

Python 3.12, FastAPI, SQLAlchemy 2.0, Alembic, Pydantic 2