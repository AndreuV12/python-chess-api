from sqlalchemy import Column, Integer, String
from app.db import Base  # Asegúrate de que `Base` se importa desde `db.py`


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
