from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.db import engine, Base, get_db
from app.models import User

from app.services.position import create_initial_position
from app.services.stockfish import ChessAnalysisService

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
Base.metadata.create_all(bind=engine)
analysis_service = ChessAnalysisService()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()  # Obtener todos los usuarios
    return users


@app.get("/position/")
def get_initial_position():
    pos = create_initial_position()
    return pos


@app.get("/analisis")
def get_analisis():
    """
    Endpoint para analizar una posición de ajedrez en formato FEN.

    :param fen: Notación FEN de la posición a analizar proporcionada en la URL.
    :return: Análisis de la posición, incluyendo evaluación y mejor jugada.
    """
    fen = "rnbqkbnr/pppppppp/8/4P3/4k3/8/PPPP1PPP/R1BQKBNR w KQkq - 0 1"
    result = analysis_service.analyze_position(fen)
    return result
