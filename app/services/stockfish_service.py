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
        self.engine = chess.engine.SimpleEngine.popen_uci(self.stockfish_path)

    def __del__(self):
        self.engine.quit()

    def get_move_name(self, fen, move_uci):
        board = chess.Board(fen)
        move = chess.Move.from_uci(move_uci)
        return board.san(move)

    def analyze_position(self, fen, num_moves=3, depth=20):
        print("depth", depth, "variants", num_moves)
        board = chess.Board(fen)
        results = self.engine.analyse(
            board, chess.engine.Limit(depth=depth), multipv=num_moves
        )
        best_moves = []
        for result in results:
            move = result["pv"][0]
            move_uci = move.uci()
            score, mate_in = get_score_and_mate_in(result)
            best_moves.append(
                {
                    "name": self.get_move_name(fen, move_uci),
                    "uci": move_uci,
                    "score": score,
                    "mate_in": mate_in,
                }
            )
        return best_moves
