from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db import engine, Base, get_db
from app.models import User

from app.services.position import create_initial_position

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()  # Obtener todos los usuarios
    return users


@app.get("/position/")
def read_root():
    pos = create_initial_position()
    return pos
