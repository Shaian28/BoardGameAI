import checkers as ch
import Tree

board = ch.Checkers()
board.print_board()

start_place = [{"B1": [(2, 1), "Man"], "B2": [(4, 1), "Man"], "B3": [(6, 1), "Man"], "B4": [(8, 1), "Man"],
                "B5": [(1, 2), "Man"], "B6": [(3, 2), "Man"], "B7": [(5, 2), "Man"], "B8": [(7, 2), "Man"],
                "B9": [(2, 3), "Man"], "B10": [(4, 3), "Man"], "B11": [(6, 3), "Man"], "B12": [(8, 3), "Man"]},
               {"R1": [(1, 8), "Man"], "R2": [(3, 8), "Man"], "R3": [(5, 8), "Man"], "R4": [(7, 8), "Man"],
                "R5": [(2, 7), "Man"], "R6": [(4, 7), "Man"], "R7": [(6, 7), "Man"], "R8": [(8, 7), "Man"],
                "R9": [(1, 6), "Man"], "R10": [(3, 6), "Man"], "R11": [(5, 6), "Man"], "R12": [(7, 6), "Man"]}]

root = Tree.Node(start_place)
_, theChosenOne = Tree.H_minimax(root, 6)
child = root.children[theChosenOne]
changePiece = Tree.compare_dicts(root.state[0], child.state[0])
currentMove = root.state[0][changePiece]
nextMove = child.state[0][changePiece]
if(ch.is_valid_move(currentMove, nextMove)):
    ch.move_piece(currentMove, nextMove)
    board.print_board()
