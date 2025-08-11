from sqlalchemy import Column, Integer, String, Numeric
from .database import Base
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(225), nullable=True)
    price = Column(Numeric(12,4), nullable=False)