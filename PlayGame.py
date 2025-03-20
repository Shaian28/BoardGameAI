import checkers as ch
import Tree

# Determining the AI's turn
def AI_turn(state):
    root = Tree.Node(state)
    _, theChosenOne = Tree.H_minimax(root, 4)
    child = root.children[theChosenOne]
    changePiece = Tree.compare_dicts(root.state[0], child.state[0])
    currentMove = root.state[0][changePiece][0]
    nextMove = child.state[0][changePiece][0]

    return currentMove, nextMove

# Determining the player's turn
def player_turn():
    print("Choose the piece you want to move as (column, row)")
    start = input()
    print("Choose the move you want to make as (column, row)")
    end = input()

    (sx, sy) = start.split(", ")
    (sx, sy) = (int(sx), int(sy))

    (ex, ey) = end.split(", ")
    (ex, ey) = (int(ex), int(ey))

    return (sx, sy), (ex, ey)

# Making a move
def move(start, end):
    # Check if the move is valid before implementing it
    if(board.is_valid_move(start, end)):
        board.move_piece(start, end)
        board.print_board()
        return True
    # When the move is invalid
    else:
        print("Invalid move")
        return False

# Updating the pieces setup and role for the AI
def update_state():
    return 0

# Test to see the game has ended
def terminal_test():
    return True

# The board being played on
board = ch.Checkers()
board.print_board()

# Initial state
initial_state = [{"B1": [(1, 0), "Man"], "B2": [(3, 0), "Man"], "B3": [(5, 0), "Man"], "B4": [(7, 0), "Man"],
                  "B5": [(0, 1), "Man"], "B6": [(2, 1), "Man"], "B7": [(4, 1), "Man"], "B8": [(6, 1), "Man"],
                  "B9": [(1, 2), "Man"], "B10": [(3, 2), "Man"], "B11": [(5, 2), "Man"], "B12": [(7, 2), "Man"]},
                 {"R1": [(0, 7), "Man"], "R2": [(2, 7), "Man"], "R3": [(4, 7), "Man"], "R4": [(6, 7), "Man"],
                  "R5": [(1, 6), "Man"], "R6": [(3, 6), "Man"], "R7": [(5, 6), "Man"], "R8": [(7, 6), "Man"],
                  "R9": [(0, 5), "Man"], "R10": [(2, 5), "Man"], "R11": [(4, 5), "Man"], "R12": [(6, 5), "Man"]}]

# The game being played
turn = 0
while terminal_test():
    # The AI's turn
    start, end = AI_turn(initial_state if turn == 0 else update_state())
    print((start, end))
    while not move(start, end):
        start, end = AI_turn(initial_state if turn == 0 else update_state())
    
    # The player's turn
    start, end = player_turn()
    while not move(start, end):
        start, end = player_turn()
    
    # Updating the turn
    turn += 1
