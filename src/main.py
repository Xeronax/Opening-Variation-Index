from anytree import Node, RenderTree
import chess
from position import PositionNode

board = chess.Board()
board.push_uci("e2e4")
board.push_uci("e7e5")
root_position: PositionNode = PositionNode(board, True)
for pre, _, node in RenderTree(root_position):
    print("%s%s - [%f]" % (pre, node.name, node.eval))

# print(RenderTree(root_position))

exit(code=None)
