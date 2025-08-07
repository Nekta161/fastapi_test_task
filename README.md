# FastAPI Тестовое задание

## Описание
CRUD API для управления товарами с использованием:
- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL
- Docker & Docker Compose

Данные хранятся в PostgreSQL. API поддерживает создание, чтение, обновление и удаление товаров, а также пагинацию и фильтрацию по названию.

## Эндпоинты

- `POST /items/` — Создать товар
- `GET /items/` — Получить список (с пагинацией и фильтром `name`)
- `GET /items/{id}` — Получить товар по ID
- `PUT /items/{id}` — Обновить товар
- `DELETE /items/{id}` — Удалить товар

## Запуск проекта

1. Убедитесь, что установлены:
   - [Docker](https://docs.docker.com/get-docker/)
   - [Docker Compose](https://docs.docker.com/compose/install/)

2. Соберите и запустите контейнеры:
   ```bash
   docker-compose up --build