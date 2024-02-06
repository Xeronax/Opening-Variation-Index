import chess
import ovi_db
from position import Position


board = chess.Board()
board.push_uci("e2e4")
board.push_uci("e7e5")
root_position: Position = Position(board)

ovi_db.print_db()

exit(code=None)
