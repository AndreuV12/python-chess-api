from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db import engine, Base, get_db
from app.models import User

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()  # Obtener todos los usuarios
    return users
