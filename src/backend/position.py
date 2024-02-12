import chess
import chess.engine
import os
from dotenv import load_dotenv
from typing import Optional, List

load_dotenv()
stockfish = os.getenv("STOCKFISH_PATH")


TIME_LIMIT = 15
MATE_VALUE = 100


class Position:

    def __init__(self, board: chess.Board | str):

        # Simple Attributes
        self.board: chess.Board = board if isinstance(board, chess.Board) else chess.Board(board)
        self.previous_move = self.name = normal_name(board)
        self.line: str = board.root().variation_san(board.move_stack)
        self.fen: str = board.fen()
        self.legal_moves: list = list(board.legal_moves)
        self.response_distribution: Optional[List[Position]] = None
        self.eval: float = self.get_eval()

    def get_responses(self) -> list:
        if not self.response_distribution:
            self.response_distribution = []
            for move in self.legal_moves:
                new_board: chess.Board = self.board.copy()
                new_board.push(move)
                self.response_distribution.append(Position(new_board))
        self.response_distribution.sort(key=lambda position: position.eval)
        return self.response_distribution

    def get_eval(self, time_limit: float = 0.1) -> float:
        analysis = engine.analyse(self.board, chess.engine.Limit(time_limit))
        return evaluate_score(self.board, analysis)

    def print(self) -> None:
        print("------" + self.previous_move + "------")
        print(self.board)
        print("Position Eval: ", self.eval)
        for move in self.response_distribution:
            move.print()

    def __iter__(self) -> list:
        return self.response_distribution


def evaluate_score(board, analysis) -> float:
    if board.turn == chess.WHITE:
        return analysis["score"].white().score(mate_score=MATE_VALUE) / 100
    return analysis["score"].black().score(mate_score=MATE_VALUE) / 100


def normal_name(board: chess.Board) -> str:
    try:
        temp_board: chess.Board = board.copy()
        current_move: chess.Move = temp_board.pop()
        return temp_board.san(current_move)
    except IndexError:
        print("Handled IndexError")
        return "Starting Position"


engine = chess.engine.SimpleEngine.popen_uci(stockfish)
