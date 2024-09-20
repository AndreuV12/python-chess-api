from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.dependencies.db import engine
from app.models import Base

from app.routers import user_router, opening_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],  # La URL donde está corriendo tu app de Vue.js
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los headers
)

app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(opening_router.router, prefix="/openings", tags=["openings"])
