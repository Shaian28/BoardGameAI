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
    # The depth-limited minimax with depth 4 (2 turns)
    _, theChosenOne = Tree.H_minimax(root, 4)
    # The chosen child for the next move
    child = root.children[theChosenOne] if validMove else random.choice(root.children)
    # The piece that was changed
    changePiece = Tree.compare_dicts(root.state[0], child.state[0])
    # The current and next move
    currentMove = root.state[0][changePiece][0]
    nextMove = child.state[0][changePiece][0] if len(root.multiKill) == 0 else root.legalMove[changePiece][0]

    # Returnung the current and next move
    return (currentMove[1], currentMove[0]), (nextMove[1], nextMove[0])

# Updating the pieces setup and role for the AI
def update_state(checker):
    # Getting the coordinates
    blackManRow, blackManColumn = np.where(checker.board == 'b')
    redManRow, redManColumn = np.where(checker.board == 'r')
    blackKingRow, blackKingColumn = np.where(checker.board == 'B')
    redKingRow, redKingColumn = np.where(checker.board == 'R')

    # Combining them together
    blackMan = [(int(item1), int(item2)) for item1, item2 in zip(blackManColumn, blackManRow)]
    redMan = [(int(item1), int(item2)) for item1, item2 in zip(redManColumn, redManRow)]
    blackKing = [(int(item1), int(item2)) for item1, item2 in zip(blackKingColumn, blackKingRow)]
    redKing = [(int(item1), int(item2)) for item1, item2 in zip(redKingColumn, redKingRow)]
    
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

# The board being played on and it's state
board = ch.Checkers()
state = update_state(board)

# Keeping track of the game
turn = 0
kill = 0

# The game being played
while terminal_test(turn - kill, state):
    # Show board
    board.print_board()

    # Updating the turn
    turn += 1
    print(f"Turn {turn}:\tAI's turn")

    # The AI's turn
    AIStart, AIEnd = AI_turn(state)
    piecePlaces = [x[0] for x in list(state[0].values())]
    while (AIStart[1], AIStart[0]) not in piecePlaces:
        print("Not your piece")
        AIStart, AIEnd = AI_turn(state, False)
    board.move_piece(AIStart, AIEnd)

    # Checking if the game hasn't ended before the turn ends
    state = update_state(board)
    if not terminal_test(turn - kill, state):
        break
    
    # Show board
    board.print_board()

    # Displaying the turn number
    print(f"Turn {turn}:\tPlayer's turn")
    
    # The player's turn
    playerStart, playerEnd = board.get_player_input()
    piecePlaces = [x[0] for x in list(state[1].values())]
    while (playerStart[1], playerStart[0]) not in piecePlaces:
        print("Not your piece")
        playerStart, playerEnd = board.get_player_input()
    board.move_piece(playerStart, playerEnd)
    
    # Check if a kill happened this turn
    if abs(AIStart[0] - AIEnd[0]) > 1 or abs(AIStart[1] - AIEnd[1]) > 1 or abs(playerStart[0] - playerEnd[0]) > 1 or abs(playerStart[1] - playerEnd[1]) > 1:
        kill = turn
    
    # Updating the state
    state = update_state(board)
