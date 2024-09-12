from app.schemas.piece import ChessPiece, PieceName, PieceColor
from app.schemas.position import Position, Coordinade

initial_position = {
    Coordinade.A1: ChessPiece(name=PieceName.ROOK, color=PieceColor.WHITE),
    Coordinade.B1: ChessPiece(name=PieceName.KNIGHT, color=PieceColor.WHITE),
    Coordinade.C1: ChessPiece(name=PieceName.BISHOP, color=PieceColor.WHITE),
    Coordinade.D1: ChessPiece(name=PieceName.QUEEN, color=PieceColor.WHITE),
    Coordinade.E1: ChessPiece(name=PieceName.KING, color=PieceColor.WHITE),
    Coordinade.F1: ChessPiece(name=PieceName.BISHOP, color=PieceColor.WHITE),
    Coordinade.G1: ChessPiece(name=PieceName.KNIGHT, color=PieceColor.WHITE),
    Coordinade.H1: ChessPiece(name=PieceName.ROOK, color=PieceColor.WHITE),
    # Peones en la fila 2
    Coordinade.A2: ChessPiece(name=PieceName.PAWN, color=PieceColor.WHITE),
    Coordinade.B2: ChessPiece(name=PieceName.PAWN, color=PieceColor.WHITE),
    Coordinade.C2: ChessPiece(name=PieceName.PAWN, color=PieceColor.WHITE),
    Coordinade.D2: ChessPiece(name=PieceName.PAWN, color=PieceColor.WHITE),
    Coordinade.E2: ChessPiece(name=PieceName.PAWN, color=PieceColor.WHITE),
    Coordinade.F2: ChessPiece(name=PieceName.PAWN, color=PieceColor.WHITE),
    Coordinade.G2: ChessPiece(name=PieceName.PAWN, color=PieceColor.WHITE),
    Coordinade.H2: ChessPiece(name=PieceName.PAWN, color=PieceColor.WHITE),
    # Peones en la fila 7 para el oponente
    Coordinade.A7: ChessPiece(name=PieceName.PAWN, color=PieceColor.BLACK),
    Coordinade.B7: ChessPiece(name=PieceName.PAWN, color=PieceColor.BLACK),
    Coordinade.C7: ChessPiece(name=PieceName.PAWN, color=PieceColor.BLACK),
    Coordinade.D7: ChessPiece(name=PieceName.PAWN, color=PieceColor.BLACK),
    Coordinade.E7: ChessPiece(name=PieceName.PAWN, color=PieceColor.BLACK),
    Coordinade.F7: ChessPiece(name=PieceName.PAWN, color=PieceColor.BLACK),
    Coordinade.G7: ChessPiece(name=PieceName.PAWN, color=PieceColor.BLACK),
    Coordinade.H7: ChessPiece(name=PieceName.PAWN, color=PieceColor.BLACK),
    # Piezas en la fila 8 para el oponente
    Coordinade.A8: ChessPiece(name=PieceName.ROOK, color=PieceColor.BLACK),
    Coordinade.B8: ChessPiece(name=PieceName.KNIGHT, color=PieceColor.BLACK),
    Coordinade.C8: ChessPiece(name=PieceName.BISHOP, color=PieceColor.BLACK),
    Coordinade.D8: ChessPiece(name=PieceName.QUEEN, color=PieceColor.BLACK),
    Coordinade.E8: ChessPiece(name=PieceName.KING, color=PieceColor.BLACK),
    Coordinade.F8: ChessPiece(name=PieceName.BISHOP, color=PieceColor.BLACK),
    Coordinade.G8: ChessPiece(name=PieceName.KNIGHT, color=PieceColor.BLACK),
    Coordinade.H8: ChessPiece(name=PieceName.ROOK, color=PieceColor.BLACK),
}


def create_initial_position() -> Position:
    return Position(position=initial_position)
