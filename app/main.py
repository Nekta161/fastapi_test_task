from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from . import schemas, crud, models, database
import time
from sqlalchemy.exc import OperationalError

app = FastAPI(
    title="API Управления Товарами",
    description="CRUD API для управления товарами с поддержкой фильтрации и пагинации.",
    version="1.0.0"
)

# Ждём, пока PostgreSQL станет доступен
while True:
    try:
        database.engine.connect()
        print("Подключение к базе данных установлено")
        break
    except OperationalError:
        print("Ожидание PostgreSQL (БД ещё не готова)")
        time.sleep(2)

# Создаём таблицы, если ещё не созданы
models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items/", response_model=schemas.ItemResponse, status_code=201, summary="Создать товар")
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    Создаёт новый товар.
    - **name**: Название (обязательно)
    - **description**: Описание (необязательно)
    - **price**: Цена (обязательно)
    """
    return crud.create_item(db, item.dict())


@app.get("/items/", response_model=List[schemas.ItemResponse], summary="Получить список товаров")
def list_items(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Сколько записей пропустить"),
    limit: int = Query(10, ge=1, le=100, description="Максимальное количество записей"),
    name: str = Query(None, description="Фильтр по названию (частичное совпадение)")
):
    """
    Возвращает список товаров с пагинацией и опциональной фильтрацией по названию.
    """
    return crud.get_items(db, skip=skip, limit=limit, name=name)


@app.get("/items/{item_id}", response_model=schemas.ItemResponse, summary="Получить товар по ID")
def get_item(item_id: int, db: Session = Depends(get_db)):
    """
    Возвращает товар по его ID.
    Если не найден — возвращает ошибку 404.
    """
    db_item = crud.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return db_item


@app.put("/items/{item_id}", response_model=schemas.ItemResponse, summary="Обновить товар")
def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    """
    Обновляет данные товара по ID.
    Все поля опциональны.
    """
    db_item = crud.update_item(db, item_id, item.dict())
    if not db_item:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return db_item


@app.delete("/items/{item_id}", response_model=schemas.ItemResponse, summary="Удалить товар")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    Удаляет товар по ID.
    Возвращает удалённый объект.
    """
    db_item = crud.delete_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return db_item