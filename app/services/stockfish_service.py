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

    # def evaluate_move(fen, move):

    #     fen = data.get("fen")  # Recibe la posición en FEN
    #     move_uci = data.get("move")  # Movimiento en formato UCI (ej: "e2e4")

    #     # Crear el tablero a partir del FEN
    #     board = chess.Board(fen)

    #     # Convertir el movimiento desde UCI (Universal Chess Interface) a un movimiento válido
    #     move = chess.Move.from_uci(move_uci)

    #     # Asegurarse de que el movimiento es legal en la posición
    #     if move not in board.legal_moves:
    #         return jsonify({"error": "Movimiento ilegal"}), 400

    #     # Realizar el movimiento
    #     board.push(move)

    #     # Evaluar la nueva posición después de realizar el movimiento
    #     info = engine.analyse(board, chess.engine.Limit(time=1.0))
    #     score = info["score"].relative.score(mate_score=10000) / 100  # Conversión de centipawns a peones

    #     return jsonify({"evaluation_after_move": score})
