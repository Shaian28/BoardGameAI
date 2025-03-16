import copy

# Class for all nodes given to a state
class Node:
    # Initialise the Node class
    def __init__(self, state, parent = None):
        # The current state, should be a dictionary for each piece location
        self.state = state
        # The previous state, should be another object of the Node class
        self.parent = parent

    # Determine the legal moves for each piece (haven't made a move for consecutive kills)
    def legal_moves(self, AI_turn = True):
        # Copy the current piece placement
        self.legalMove = copy.deepcopy(self.state[0 if AI_turn else 1])
        # Store the already occupied spaces
        allyOccupancy = [elem[0] for elem in list(self.state[0 if AI_turn else 1].values())]
        enemyOccupancy = [elem[0] for elem in list(self.state[1 if AI_turn else 0].values())]

        # Iterate through the pieces and places of the pieces
        for piece, (place, role) in self.state[0 if AI_turn else 1].items():
            # When it is AI's turn
            if AI_turn:
                # All the legal movement for man
                if role == "Man":
                    moveList = [(place[0] - 1, place[1] + 1), (place[0] + 1, place[1] + 1),
                                (place[0] - 2, place[1] + 2), (place[0] + 2, place[1] + 2)]
                # All the legal movement for king
                elif role == "King":
                    moveList = [(place[0] - 1, place[1] - 1), (place[0] - 1, place[1] + 1),
                                (place[0] + 1, place[1] - 1), (place[0] + 1, place[1] + 1),
                                (place[0] - 2, place[1] - 2), (place[0] - 2, place[1] + 2),
                                (place[0] + 2, place[1] - 2), (place[0] + 2, place[1] + 2)]
                # All the legal movement for dead
                else:
                    moveList = []
            # When it is the players turn
            else:
                # All the legal movement for man
                if role == "Man":
                    moveList = [(place[0] - 1, place[1] - 1), (place[0] + 1, place[1] - 1),
                                (place[0] - 2, place[1] - 2), (place[0] + 2, place[1] - 2)]
                # All the legal movement for king
                elif role == "King":
                    moveList = [(place[0] - 1, place[1] - 1), (place[0] - 1, place[1] + 1),
                                (place[0] + 1, place[1] - 1), (place[0] + 1, place[1] + 1),
                                (place[0] - 2, place[1] - 2), (place[0] - 2, place[1] + 2),
                                (place[0] + 2, place[1] - 2), (place[0] + 2, place[1] + 2)]
                # All the legal movement for dead
                else:
                    moveList = []

            # Initialise tiles and counters
            tiles = []
            allyCounter = []
            enemyCounter = []

            # Iterate through the rows and coloumns of the piece
            for idx, (col, row) in enumerate(moveList):
                # Check if there is no wall blocking
                if col > 0 and col < 8 and row > 0 and row < 8:
                    # Ignore spaces with black pieces
                    if (col, row) in allyOccupancy:
                        allyCounter.append(idx)
                        continue
                    # Ignore spaces with red pieces
                    elif (col, row) in enemyOccupancy:
                        enemyCounter.append(idx)
                        continue

                    # Jump over a red pieces
                    if idx > len(moveList) / 2 - 1 and idx - len(moveList) / 2 not in enemyCounter:
                        continue
                    # Don't jump over black pieces
                    elif idx - len(moveList) / 2 in allyCounter:
                        continue

                    # Append the non-filtered tiles from move set
                    tiles.append((col, row))

            # Store the legal moves
            self.legalMove[piece] = [tiles, role]

    # Generate next states of the Node class
    def generate_child(self, AI_turn = True):
        # The initialisation next state
        self.children = []
        # Run all the legal moves
        self.legal_moves(AI_turn)

        # Go through all the legal moves done by the pieces
        for piece, (move, role) in self.legalMove.items():
            # Continue if there is no legal moves for the piece
            if len(move) == 0:
                continue
            # Go through all the places, the legal moves brings the piece
            for place in move:
                # Update the map to the new place
                newState = self.update_places(piece, place, role, AI_turn = AI_turn)
                # Create the child
                child_node = Node(newState, parent = self)
                # Append the child in the list
                self.children.append(child_node)
        
        # Return all the children of the node
        return self.children
        

    # Determining the best move for the current state
    def best_move(self):
        allyOccupancy = [elem[0] for elem in list(self.state[0].values()[0])]
        enemyOccupancy = [elem[0] for elem in list(self.state[1].values()[0])]
        allyRole = [elem[0] for elem in list(self.state[0].values()[1])]
        enemyRole = [elem[0] for elem in list(self.state[1].values()[1])]
        setupState = 1
        scanList = [(3, 3), (3, 3), (1, 3), (1, 3),
                    (2, 2), (2, 2),
                    (3, 1), (3, 1), (1, 1), (1, 1),
                    (2, 0), (2, 0),
                    (3, 1), (3, 1), (1, 1), (1, 1),
                    (2, 2), (2, 2),
                    (3, 3), (3, 3), (1, 3), (1, 3)]
        bestMove = []

        # All setups with O as AI and X as opponent (mirrored setups counts)
        # Setup = 1      Setup = 2       Setup = 3       Setup = 4       Setup = 5       Setup = 6       Setup = 7      Setup = 8       Setup = 9        Setup = 10       Setup = 11       Setup = 12       Setup = 13       Setup = 14       Setup = 15       Setup = 16   
        # | | | | | |    | | | | | |     | | | | | |     | | | | | |     | | | | | |     | | | | | |     | | | | | |     | | | | | |     | | | | | |      | | | | | |      | | | | | |      | | | | | |      | | | | | |      | | | | | |      |O| | | | |      | | | | | |  
        # | | | | | |    | | | | | |     | | | | | |     | | | | | |     | |O| |O| |     | | |O| | |     | |O| | | |     | | | | | |     | | | | | |      | | | | | |      | | | | | |      | | | | | |      | | | | | |     O| | | | | |      | |O| | | |      | |O| | | |  
        # | | |O| | |    | | |O| | |     | | | |O| |     | |O| | | |     | | | | | |     | | | | | |     | | |X| | |     | | |X| | |     | | |X| | |      | | | | |O|      | | | | | |      | | | | | |      | | | | | |      |O| |O| | |      | | |O| |O|      |X| |X| | |  
        # | | | | | |    | |X| | | |     | | | | | |     | | |X| | |     | |X| | | |     | |X| |X| |     | | | | | |     | | | | | |     | | | | | |      | | | | | |X     | | | | | |      | | | |O| |      | | | | | |      | | | | | |      | | | | | |      | | | | | |  
        # | | | | | |    | | | | | |     | |X| | | |     | | | |X| |     | | | | | |     | | | | | |     | | |X| | |     | | |O| | |     | | |O| | |      | | | | | |      | | |O| | |      | | | | | |      | | |O| | |      |X| |X| | |      | | |X| |X|      | | | | |X|  
        # | | | | | |    | | | | | |     | | | | | |     | | | | | |     | | | | | |     | | | | | |     | | | | | |     | | | | | |     | | | | | |      | | | | | |      |_|_|_|_|_|      |_|X|_|_|_|      | |X| | | |      | | | | | |      | | | | | |      | | | | | |  
        #                                                                The right one                                                   Opponent is king There is a wall                                                     The middle one   Same as before
        for piece, (place, role) in self.state[0].items():
            allyCounter = []
            enemyCounter = []
            outOfBound = []
            setupState = []
            for (x, y) in scanList:
                col = place[0] + x
                row = place[1] + y
                if (col, row) in enemyOccupancy:
                    pieceRole = enemyRole[enemyOccupancy.index((col, row))]
                    enemyCounter.append((x, y), pieceRole)
                elif (col, row) in allyOccupancy:
                    pieceRole = allyRole[allyOccupancy.index((col, row))]
                    allyCounter.append((x, y), pieceRole)
                elif col > 0 and col < 8 and row > 0 and row < 8:
                    outOfBound.append((x, y), "Wall")
                else:
                    continue
            
            # Make it so that the priority is appended instead of the setup
            # Jump forward over an enemy at left side
            if (piece[0] - 2, piece[1] + 2) in self.legalMove[piece]:
                # Setup 2
                if (-1, 1) in enemyCounter:
                    setupState.append((2, 1))
                # Setup 7
                if (-1, 1) in enemyCounter: #...
                    setupState.append((7, 1))
                # Setup 16
                if (-1, 1) in enemyCounter and (1, 1) in enemyCounter and ((-3, 3) in enemyCounter or (-1, 3) in enemyCounter): #...
                    setupState.append((16, 1))
            # Jump forward over an enemy at right side
            if (piece[0] + 2, piece[1] + 2) in self.legalMove[piece]:
                # Setup 2
                if (1, 1) in enemyCounter:
                    setupState.append((2, 2))
                # Setup 7
                if (1, 1) in enemyCounter: #...
                    setupState.append((7, 2))
                # Setup 16
                if (-1, 1) in enemyCounter and (1, 1) in enemyCounter and ((3, 3) in enemyCounter or (1, 3) in enemyCounter): #...
                    setupState.append((16, 2))
            # Jump backward over an enemy at left side
            if (piece[0] - 2, piece[1] - 2) in self.legalMove[piece]:
                # Setup 2
                if (-1, -1) in enemyCounter:
                    setupState.append((2, 3))
            # Jump backward over an enemy at right side
            if (piece[0] + 2, piece[1] - 2) in self.legalMove[piece]:
                # Setup 2
                if (1, -1) in enemyCounter:
                    setupState.append((2, 4))
            # Move forward at right side
            if (piece[0] - 1, piece[1] + 1) in self.legalMove[piece]:
                # Setup 1
                setupState.append((1, 5))
                # Setup 3
                if (-2, 2) in enemyCounter or (0, 2) in enemyCounter:
                    setupState.append((3, 5))
                # Setup 4
                if (1, 1) in enemyCounter and (2, 2) in enemyCounter:
                    setupState.append((4, 5))
                # Setup 5
                if (0, 2) in enemyCounter and (-2, 0) in allyCounter:
                    setupState.append((5, 5))
                # Setup 6
                if (-2, 2) in enemyCounter and (2, 2) in enemyCounter:
                    setupState.append((6, 5))
                # Setup 9
                if ((-2, -2) in enemyCounter or (0, -2) in enemyCounter or (2, -2) in enemyCounter) and enemyRole == "King":
                    setupState.append((9, 5))
                # Setup 10
                if (1, 1) in enemyCounter and (2, 2) in outOfBound:
                    setupState.append((10, 5))
                # Setup 11
                if (-2, 2) in outOfBound or (0, 2) in outOfBound or (2, 2) in outOfBound:
                    setupState.append((11, 5))
                # Setup 12
                if (2, 2) in enemyCounter and ((-3, 3) in outOfBound or (-1, 3) in outOfBound or (0, 3) or (1, 3) in outOfBound in outOfBound or (3, 3) in outOfBound):
                    setupState.append((12, 5))
                # Setup 13
                if (1, 1) in enemyCounter and ((-2, 2) in outOfBound or (0, 2) in outOfBound or (2, 2) in outOfBound):
                    setupState.append((13, 5))
                # Setup 14
                if (-1, 1) in enemyCounter and (1, 1) in enemyCounter and (-2, -2) in allyCounter and (-1, -1) in allyCounter and (1, -1) in allyCounter and (-3, -3) in outOfBound:
                    setupState.append((14, 5))
                # Setup 15
                if (-1, 1) in enemyCounter and (1, 1) in enemyCounter and (-3, -3) in allyCounter and (-2, -2) in allyCounter and (-1, -1) in allyCounter and (1, -1) in allyCounter:
                    setupState.append((15, 5))
            # Move forward at left side
            if (piece[0] + 1, piece[1] + 1) in self.legalMove[piece]:
                # Setup 1
                setupState.append((1, 6))
                # Setup 3
                if (2, 2) in enemyCounter or (0, 2) in enemyCounter:
                    setupState.append((3, 6))
                # Setup 4
                if (-1, 1) in enemyCounter and (-2, 2) in enemyCounter:
                    setupState.append((4, 6))
                # Setup 5
                if (0, 2) in enemyCounter and (2, 0) in allyCounter:
                    setupState.append((5, 6))
                # Setup 6
                if (-2, 2) in enemyCounter and (2, 2) in enemyCounter:
                    setupState.append((6, 6))
                # Setup 9
                if ((-2, -2) in enemyCounter or (0, -2) in enemyCounter or (2, -2) in enemyCounter) and enemyRole == "King":
                    setupState.append((9, 6))
                # Setup 10
                if (-1, 1) in enemyCounter and (-2, 2) in outOfBound:
                    setupState.append((10, 6))
                # Setup 11
                if (-2, 2) in outOfBound or (0, 2) in outOfBound or (2, 2) in outOfBound:
                    setupState.append((11, 6))
                # Setup 12
                if (-2, 2) in enemyCounter and ((-3, 3) in outOfBound or (-1, 3) in outOfBound or (0, 3) or (1, 3) in outOfBound in outOfBound or (3, 3) in outOfBound):
                    setupState.append((12, 6))
                # Setup 13
                if (-1, 1) in enemyCounter and ((-2, 2) in outOfBound or (0, 2) in outOfBound or (2, 2) in outOfBound):
                    setupState.append((13, 6))
                # Setup 14
                if (1, 1) in enemyCounter and (-1, 1) in enemyCounter and (2, -2) in allyCounter and (1, -1) in allyCounter and (-1, -1) in allyCounter and (3, -3) in outOfBound:
                    setupState.append((14, 6))
                # Setup 15
                if (1, 1) in enemyCounter and (-1, 1) in enemyCounter and (3, -3) in allyCounter and (2, -2) in allyCounter and (1, -1) in allyCounter and (-1, -1) in allyCounter:
                    setupState.append((15, 6))
            # Move backward at left side
            if (piece[0] - 1, piece[1] - 1) in self.legalMove[piece]:
                # Setup 1
                setupState.append((1, 7))
                # Setup 8
                if ((-2, -2) in enemyCounter or (0, -2) in enemyCounter) and enemyRole == "Man":
                    setupState.append((8, 7))
            # Move backward at right side
            if (piece[0] + 1, piece[1] - 1) in self.legalMove[piece]:
                # Setup 1
                setupState.append((1, 8))
                # Setup 8
                if ((0, -2) in enemyCounter or (2, -2) in enemyCounter) and enemyRole == "Man":
                    setupState.append((8, 8))

            bestMove.append(setupState[setupState.index(min(setupState[0]))])
        
        chosenMove = bestMove[bestMove.index(min(bestMove[0]))]

        return chosenMove
            
            

    
    # Updating the placement given in the state
    def update_places(self, piece, place, role, AI_turn = True):
        # Make a copy of the state
        newState = copy.deepcopy(self.state)
        # Place the new position and role
        newState[0 if AI_turn else 1][piece] = [place, role]

        # Return the new state
        return newState

# The H-minimax strategy with aplha-beta pruning (https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#Pseudocode)
def H_minimax(node, depth, maximizingPlayer = True, alpha = float('-inf'), beta = float('inf')):
    # Generate the children of the node
    children = node.generate_child(maximizingPlayer)
    
    # If the limited depth has been reached
    if depth == 0 or len(children) == 0:
        # Evalute the heuristic value
        return len(node.state[0]) - len(node.state[1])

    # If player is max
    if maximizingPlayer:
        # Set alpha to -infinty
        value = float('-inf')
        # Go through every child in the state
        for child in children:
            # Evaluate the childs minimax value decide the max value to set alpha
            eval = H_minimax(child, depth - 1, False, alpha, beta)
            value = max(value, eval)
            # Break out of loop if beta is the smaller number
            if value > beta:
                break
            # Update alpha
            alpha = max(alpha, value)

    # If the player is min
    else:
        # Set beta to -infinty
        value = float('inf')
        # Go through every child in the state
        for child in children:
            # Evaluate the childs minimax value decide the min value to set beta
            eval = H_minimax(child, depth - 1, True, alpha, beta)
            value = min(value, eval)
            # Break out of loop if alpha is the bigger number
            if value < alpha:
                break
            # Update beta
            beta = min(beta, value)

    # Return the final value
    return value

if __name__ == "__main__":
    # The initial position of the pieces
    start_place = [{"B1": [(2, 1), "Man"], "B2": [(4, 1), "Man"], "B3": [(6, 1), "Man"], "B4": [(8, 1), "Man"],
                    "B5": [(1, 2), "Man"], "B6": [(3, 2), "Man"], "B7": [(5, 2), "Man"], "B8": [(7, 2), "Man"],
                    "B9": [(2, 3), "Man"], "B10": [(4, 3), "Man"], "B11": [(6, 3), "Man"], "B12": [(8, 3), "Man"]},
                   {"R1": [(2, 8), "Man"], "R2": [(4, 8), "Man"], "R3": [(6, 8), "Man"], "R4": [(8, 8), "Man"],
                    "R5": [(1, 7), "Man"], "R6": [(3, 7), "Man"], "R7": [(5, 7), "Man"], "R8": [(7, 7), "Man"],
                    "R9": [(2, 6), "Man"], "R10": [(4, 6), "Man"], "R11": [(6, 6), "Man"], "R12": [(8, 6), "Man"]}]

    # The original node
    root = Node(start_place)
    H_minimax(root, 3)
