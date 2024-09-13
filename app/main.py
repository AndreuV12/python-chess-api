from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import engine
from app.models import Base

from app.services.stockfish import ChessAnalysisService
from app.routers import user

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

app.include_router(user.router, prefix="/api", tags=["users"])


@app.get("/")
def read_root():
    return {"message": "Hello World"}


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
