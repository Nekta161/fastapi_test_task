from sqlalchemy.orm import Session
from . import models


def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_items(db: Session, skip: int = 0, limit: int = 10, name: str = None):
    query = db.query(models.Item)
    if name:
        query = query.filter(models.Item.name.contains(name))
    return query.offset(skip).limit(limit).all()


def create_item(db: Session, item: dict):
    db_item = models.Item(**item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, item_data: dict):
    db_item = get_item(db, item_id)
    if db_item:
        for key, value in item_data.items():  # ✅ Исправлено: .items()
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int):
    db_item = get_item(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item