# FastAPI Тестовое задание 

## Описание
CRUD API для управления товарами с использованием FastAPI, PostgreSQL, Docker.

## Эндпоинты
- 'POST /items/' - Создать
- 'GET /items/' - Список(с пагинацией и фильтром 'name')
- 'GET /items/{id}' - Получить
- 'PUT /items/{id}' - Обновить
- 'DELETE /items/{id}' - Удалить 

## Запуск
```bash
docker-compose up --build