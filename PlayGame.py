# Python libraries
import numpy as np
import random

# Our own modules
import checkers as ch
import Tree

# Determining the AI's turn
def AI_turn(state, validMove = True):
    # The root of the tree
    root = Tree.Node(state)
    # The depth.limited minimax with depth 4 (2 turns)
    _, theChosenOne = Tree.H_minimax(root, 4)
    # The chosen child for the next move
    child = root.children[theChosenOne] if validMove else random.choice(root.children)
    # The piece that was changed
    changePiece = Tree.compare_dicts(root.state[0], child.state[0])
    # The current and next move
    currentMove = root.state[0][changePiece][0]
    nextMove = child.state[0][changePiece][0] if len(root.multiKill) == 0 else root.legalMove[changePiece][0]

    # Returnung the current and next move
    return (currentMove[1], currentMove[0]), (nextMove[1], nextMove[0])#currentMove, nextMove

# Determining the player's turn
def player_turn():
    # Getting the start and end move
    start = input("Choose the piece you want to move as (column, row):\n")
    end = input("Choose the move you want to make as (column, row):\n")

    # Get the start move as a tuple
    (sx, sy) = start.split(",")
    (sx, sy) = (int(sx), int(sy))

    # Get the end move as a tuple
    (ex, ey) = end.split(",")
    (ex, ey) = (int(ex), int(ey))

    # Return the start and end move
    return (sy, sx), (ey, ex)#(sx, sy), (ex, ey)

# Making a move
def move(start, end, state, player):
    # Get all the placement of the pieces of either AI or player
    piecePlaces = [x[0] for x in list(state[1 if player else 0].values())]
    # Check if the move is valid before implementing it
    if(board.is_valid_move(start, end)) and (start[1], start[0]) in piecePlaces:
        # Move the piece and update the board
        board.move_piece(start, end)
        board.print_board()

        # Tell the game that the move is valid
        return True
    # When the move isn't valid
    else:
        # Tell which move is invalid
        print(f"{(start[1], start[0])} --> {(end[1], end[0])} is an invalid move")

        # Tell the game that the move is invalid
        return False

# Updating the pieces setup and role for the AI
def update_state(checker):
    # Getting the coordinates
    blackManX, blackManY = np.where(checker.board == 'b')
    redManX, redManY = np.where(checker.board == 'r')
    blackKingX, blackKingY = np.where(checker.board == 'B')
    redKingX, redKingY = np.where(checker.board == 'R')

    # Combining them together
    blackMan = [(int(item1), int(item2)) for item1, item2 in zip(blackManY, blackManX)]#zip(blackManX, blackManY)]
    redMan = [(int(item1), int(item2)) for item1, item2 in zip(redManY, redManX)]#zip(redManX, redManY)]
    blackKing = [(int(item1), int(item2)) for item1, item2 in zip(blackKingY, blackKingX)]#zip(blackKingX, blackKingY)]
    redKing = [(int(item1), int(item2)) for item1, item2 in zip(redKingY, redKingX)]#zip(redKingX, redKingY)]
    
    # Initialising the dictionaries
    blackState = {}
    redState = {}

    # Giving each key the right value
    for idx, place in enumerate(blackMan):
        blackState[f"B{idx + 1}"] = [place, "Man"]
        endIdx = idx
    for idx, place in enumerate(blackKing):
        blackState[f"B{idx + endIdx}"] = [place, "King"]
    for idx, place in enumerate(redMan):
        redState[f"R{idx + 1}"] = [place, "Man"]
        endIdx = idx
    for idx, place in enumerate(redKing):
        redState[f"R{idx + endIdx}"] = [place, "King"]
    
    # Making the state
    state = [blackState, redState]

    # Returning the state
    return state

# Test to see the game has ended
def terminal_test(killCondition, nodeState):
    # Making a node out of the state
    node = Tree.Node(nodeState)
    
    # All the pieces
    AIPieces = len(list(node.state[0].keys()))
    playerPieces = len(list(node.state[1].keys()))

    # All the legal moves
    node.legal_moves(True)
    AILegalMove = len(node.legalMove)
    node.legal_moves(False)
    playerLegalMove = len(node.legalMove)

    # The condition for terminal game
    if killCondition > 40 or AIPieces == 0 or playerPieces == 0 or AILegalMove == 0 or playerLegalMove == 0:
        if killCondition > 40 or AILegalMove == 0 or playerLegalMove == 0:
            print("The game is a draw")
        elif AIPieces == 0:
            print("The AI won")
        elif playerPieces == 0:
            print("You won")
        
        # End the game
        return False
    
    # Continue the game
    return True

# The board being played on
board = ch.Checkers()
board.print_board()

# The state of the board
state = update_state(board)

# Keeping track of the game
turn = 0
kill = 0

# The game being played
while terminal_test(turn - kill, state):
    # Updating the turn
    turn += 1
    print(f"Turn {turn}:\tAI's turn")

    # The AI's turn
    AIStart, AIEnd = AI_turn(state)
    while not move(AIStart, AIEnd, state, False):
        AIStart, AIEnd = AI_turn(state, False)

    # Checking if the game hasn't ended before the turn ends
    state = update_state(board)
    if not terminal_test(turn - kill, state):
        break
    
    # Displaying the turn number
    print(f"Turn {turn}:\tPlayer's turn")
    
    # The player's turn
    playerStart, playerEnd = player_turn()
    while not move(playerStart, playerEnd, state, True):
        playerStart, playerEnd = player_turn()
    
    # Check if a kill happened this turn
    if abs(AIStart[0] - AIEnd[0]) > 1 or abs(AIStart[1] - AIEnd[1]) > 1 or abs(playerStart[0] - playerEnd[0]) > 1 or abs(playerStart[1] - playerEnd[1]) > 1:
        kill = turn
    
    # Updating the state
    state = update_state(board)
