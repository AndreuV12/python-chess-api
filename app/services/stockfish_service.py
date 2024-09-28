import chess
import chess.engine

from app.config import get_settings


def get_score_and_mate_in(result):
    mate_in = result["score"].mate() if result["score"].is_mate() else None
    if mate_in:
        return None, mate_in
    centipawns = result["score"].relative.score()
    score = -centipawns if result["score"].turn == chess.BLACK else centipawns
    return score, None


class ChessAnalysisService:
    def __init__(self):
        settings = get_settings()
        self.stockfish_path = settings.STOCKFISH_PATH
        self.engine = chess.engine.SimpleEngine.popen_uci(
            self.stockfish_path
        )  # Inicia el motor aquí

    def __del__(self):
        self.engine.quit()

    def analyze_position(self, fen, num_moves=3, pv_deep=3, depth=20):
        print("depth", depth, "variants", num_moves)
        board = chess.Board(fen)
        results = self.engine.analyse(
            board, chess.engine.Limit(depth=depth), multipv=num_moves
        )
        best_moves = []
        for result in results:
            move = result["pv"][0]
            score, mate_in = get_score_and_mate_in(result)
            pv = [move.uci() for move in result["pv"][1 : pv_deep + 1]]
            best_moves.append(
                {"uci": move.uci(), "score": score, "mate_in": mate_in, "pv": pv}
            )

        return best_moves

    def evaluate_move(self, fen, move_uci, depth=10):
        board = chess.Board(fen)
        move = chess.Move.from_uci(move_uci)
        board.push(move)
        info = self.engine.analyse(board, chess.engine.Limit(depth=depth))
        score = info["score"].relative.score(mate_score=10000)  # Igualar el uso
        return score


if __name__ == "__main__":
    # Crear una instancia del servicio de análisis
    chess_service = ChessAnalysisService()

    # Definir la posición FEN para el Gambito de Dama
    # fen = "rnbqkbnr/ppp1pppp/8/8/2pP4/8/PP2PPPP/RNBQKBNR w KQkq - 0 3"

    fen = "rnbqkbnr/ppp1pppp/8/8/2pP4/1Q6/PP2PPPP/RNB1KBNR b KQkq - 1 3"
    # Analizar la posición
    analysis_result = chess_service.analyze_position(fen=fen, depth=18)
    print("Análisis de la posición del Gambito de Dama:")
    print(analysis_result)
