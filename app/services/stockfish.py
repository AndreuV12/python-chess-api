import chess
import chess.engine

from app.config import get_settings


class ChessAnalysisService:
    def __init__(self):
        """
        Inicializa el servicio de análisis de ajedrez.

        :param stockfish_path: Ruta al ejecutable de Stockfish
        """
        settings = get_settings()
        self.stockfish_path = settings.STOCKFISH_PATH

    def analyze_position(self, fen, time_limit=2):
        """
        Analiza una posición de ajedrez dada en formato FEN.

        :param fen: Notación FEN de la posición
        :param time_limit: Tiempo de análisis en segundos (opcional)
        :return: Un diccionario con la evaluación y mejor jugada
        """
        # Inicia el motor de ajedrez
        engine = chess.engine.SimpleEngine.popen_uci(self.stockfish_path)

        # Cargar el tablero con la posición en FEN
        board = chess.Board(fen)

        # Realiza el análisis de la posición
        result = engine.analyse(board, chess.engine.Limit(time=time_limit))
        print(result)
        # Extrae la evaluación y la mejor jugada
        evaluation = result["score"].relative.score()
        best_moves = [board.san(move) for move in result["pv"][:3]]

        # Cierra el motor
        engine.quit()

        return {"evaluation": evaluation, "best_moves": best_moves}
