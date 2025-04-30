from sqlalchemy.orm import Session
from . import models, schemas

def get_items(db: Session, skip: int = 0, limit: int = 10, search: str = ""):
    query = db.query(models.Item)
    if search:
        query = query.filter(models.Item.name.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item