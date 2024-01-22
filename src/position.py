import chess
import chess.engine
from anytree import NodeMixin

TIME_LIMIT = 15
MATE_VALUE = 1000


class PositionNode(NodeMixin):

    def __init__(self, board: chess.Board, branch_analysis: bool = False, response_analysis: bool = False, parent=None,
                 children=None):

        # Simple Attributes
        self.board: chess.Board = board
        self.previous_move = self.name = normal_name(board)
        self.line: str = board.root().variation_san(board.move_stack)
        self.legal_moves: list = list(board.legal_moves)
        self.response_distribution: list = []
        if response_analysis:
            self.response_distribution = analyze_position(self)  # Evaluate all possible responses for current position
        self.response_distribution.sort(key=lambda move: move.score)
        self.eval: float = self.get_eval()
        self.turn_num: int = board.fullmove_number
        self.parent: PositionNode = parent

        print("Initialized Position: " + self.line)

        # Evaluate all possible next positions
        if branch_analysis:
            print("Starting Child Evals")
            for move in self.legal_moves:
                new_board = self.board.copy()
                new_board.push(move)
                PositionNode(new_board, False, True, self)

    def print(self):
        print("------" + self.previous_move + "------")
        print("Turn #: ", self.turn_num)
        print(self.board)
        print("Position Eval: ", self.eval)
        for move in self.response_distribution:
            move.print()

    def get_eval(self) -> float:
        analysis = engine.analyse(self.board, chess.engine.Limit(0.1))
        return evaluate_score(self.board, analysis)

    def __iter__(self):
        return self.response_distribution


class AnalyzedMove:

    def print(self):
        print(self.move_str)
        print(self.score)

    def __init__(self, move, score, move_str):
        self.move = move
        self.score = score
        self.move_str = move_str


def analyze_position(position) -> list:
    response_distribution = []
    for move in position.legal_moves:
        temp_board = position.board.copy()
        temp_board.push(move)
        analysis = engine.analyse(temp_board, chess.engine.Limit(.1))
        print("Analyzed response and got: ", analysis)
        new_move = create_move(temp_board, analysis)
        response_distribution.append(new_move)
    return response_distribution


def evaluate_score(board, analysis) -> float:
    if board.turn == chess.WHITE:
        return analysis["score"].white().score(mate_score=MATE_VALUE) / 100
    return analysis["score"].black().score(mate_score=MATE_VALUE) / 100


def create_move(board, analysis) -> AnalyzedMove:
    temp_board = board.copy()
    score = evaluate_score(temp_board, analysis)
    try:
        current_move = temp_board.pop()
    except IndexError:
        # print("Handled IndexError")
        current_move = chess.Move.null()
    move_str = normal_name(temp_board)
    return AnalyzedMove(current_move, score, move_str)


def normal_name(board: chess.Board) -> str:
    try:
        temp_board = board.copy()
        current_move: chess.Move = temp_board.pop()
        return temp_board.san(current_move)
    except IndexError:
        print("Handled IndexError")
        return "Starting Position"


engine = chess.engine.SimpleEngine.popen_uci(r"C:\Users\tauru\Downloads\OVI\Opening-Variation-Index\src\stockfish.exe")
