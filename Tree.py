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
        # Store the already occupied spaces and roles
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
                if col > 0 and col < 9 and row > 0 and row < 9:
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
        # Run all the legal moves
        self.legal_moves(AI_turn)

        # The initialisation of next state
        self.children = []
        # Go through all the legal moves done by the pieces
        for piece, (move, role) in self.legalMove.items():
            # Get the piece and initialise the death counter
            piecePlace = self.state[0 if AI_turn else 1][piece]
            deathCounter = 0
            # Continue if there is no legal moves for the piece
            if len(move) == 0:
                continue
            # Go through all the places, the legal moves brings the piece
            for place in move:
                # Check if a kill condition has been met
                if abs(piecePlace[0][0] - place[0]) > 1 or abs(piecePlace[0][1] - place[1]) > 1:
                   deathCounter = (piecePlace[0][1] + (place[0] - piecePlace[0][0]) // 2, piecePlace[0][1] + (place[1] - piecePlace[0][1]) // 2)
                # Update the map to the new place
                newState = self.update_places(piece, place, role, AI_turn = AI_turn, death = deathCounter)
                # Create the child
                child_node = Node(newState, parent = self)
                # Append the child in the list
                self.children.append(child_node)
        
        # Return all the children of the node
        return self.children
        
    # Determining the best move for the current state
    def best_move(self):
        # Store the already occupied spaces and roles
        allyOccupancy = [elem[0] for elem in list(self.state[0].values())]
        enemyOccupancy = [elem[0] for elem in list(self.state[1].values())]
        allyRole = [elem[1] for elem in list(self.state[0].values())]
        enemyRole = [elem[1] for elem in list(self.state[1].values())]

        # The best move for the state
        bestMove = []
        # Scanning areas relative to the piece
        scanList = [(-3, -3), (-1, -3), (1, -3), (3, -3),
                    (-2, -2), (0, -2), (2, -2),
                    (-3, -1), (-1, -1), (1, -1), (3, -1),
                    (-2, 0), (2, 0),
                    (-3, 1), (-1, 1), (1, 1), (3, 1),
                    (-2, 2), (0, 2), (2, 2),
                    (-3, 3), (-1, 3), (1, 3), (3, 3)]

        # All setups with O as AI and X as opponent (mirrored setups counts)
        # Setup = 1      Setup = 2       Setup = 3       Setup = 4       Setup = 5       Setup = 6       Setup = 7      Setup = 8       Setup = 9        Setup = 10       Setup = 11       Setup = 12       Setup = 13       Setup = 14       Setup = 15       Setup = 16       Setup = 17
        # | | | | | |    | | | | | |     | | | | | |     | | | | | |     | | | | | |     | | | | | |     | | | | | |     | | | | | |     | | | | | |      | | | | | |      | | | | | |      | | | | | |      | | | | | |      | | | | | |      |O| | | | |      | | | | | |      | | | | | | 
        # | | | | | |    | | | | | |     | | | | | |     | | | | | |     | |O| |O| |     | | | | | |     | |O| | | |     | | | | | |     | | | | | |      | | | | | |      | | | | | |      | | | | | |      | | | | | |     O| | | | | |      | |O| | | |      | |O| | | |      | | | | | | 
        # | | |O| | |    | | |O| | |     | | | |O| |     | |O| | | |     | | | | | |     | | |O| | |     | | |X| | |     | | |X| | |     | | |X| | |      | | | | |O|      | | | | | |      | | | | | |      | | | | | |      |O| |O| | |      | | |O| |O|      |X| |X| | |      |O| | | | | 
        # | | | | | |    | |X| | | |     | | | | | |     | | |X| | |     | |X| | | |     | |X| |X| |     | | | | | |     | | | | | |     | | | | | |      | | | | | |X     | | | | | |      | | | |O| |      | | | | | |      | | | | | |      | | | | | |      | | | | | |      | | | | | | 
        # | | | | | |    | | | | | |     | |X| | | |     | | | |X| |     | | | | | |     |X| | | |X|     | | |X| | |     | | |O| | |     | | |O| | |      | | | | | |      | | |O| | |      | | | | | |      | | |O| | |      |X| |X| | |      | | |X| |X|      | | | | |X|      |X| | | | | 
        # | | | | | |    | | | | | |     | | | | | |     | | | | | |     | | | | | |     | | | | | |     | | | | | |     | | | | | |     | | | | | |      | | | | | |      |_|_|_|_|_|      |_|X|_|_|_|      | |X| | | |      | | | | | |      | | | | | |      | | | | | |      | | | | | | 
        #                                                                The right one                                                   Opponent is king There is a wall                                                     The middle one   Same as before
        # Iterate through the pieces and places of the pieces
        for piece, (place, _) in self.state[0].items():
            if len(self.legalMove[piece][0]) == 0:
                bestMove.append((0, float('inf'), place))
                continue
            else:
                # Initialise counters and setup state for each piece
                allyCounter = []
                enemyCounter = []
                allyCounterRole = []
                enemyCounterRole = []
                outOfBound = []
                setupState = []
                
                # Scan through the are 3 tiles ahead
                for (x, y) in scanList:
                    # Getting coloumn and row of the board
                    col = place[0] + x
                    row = place[1] + y
                    
                    # The detected enemies in the scan area
                    if (col, row) in enemyOccupancy:
                        enemyCounter.append((x, y))
                        enemyCounterRole.append(enemyRole[enemyOccupancy.index((col, row))])
                    # The detected allies in the scan area
                    elif (col, row) in allyOccupancy:
                        allyCounter.append((x, y))
                        allyCounterRole.append(allyRole[allyOccupancy.index((col, row))])
                    # The detected walls in the scan area
                    elif col < 1 or col > 8 or row < 1 or row > 8:
                        outOfBound.append((x, y))

                # Jump forward over an enemy at left side
                if (place[0] - 2, place[1] + 2) in self.legalMove[piece][0]:
                    # Setup 2
                    if (-1, 1) in enemyCounter:
                        setupState.append((2, 3, (place[0] - 2, place[1] + 2)))
                    # Setup 7
                    if (-1, 1) in enemyCounter: #...
                        setupState.append((7, 2, (place[0] - 2, place[1] + 2)))
                    # Setup 16
                    if (-1, 1) in enemyCounter and (1, 1) in enemyCounter and ((-3, 3) in enemyCounter or (-1, 3) in enemyCounter): #...
                        setupState.append((16, 1, (place[0] - 2, place[1] + 2)))
                # Jump forward over an enemy at right side
                if (place[0] + 2, place[1] + 2) in self.legalMove[piece][0]:
                    # Setup 2
                    if (1, 1) in enemyCounter:
                        setupState.append((2, 3, (place[0] + 2, place[1] + 2)))
                    # Setup 7
                    if (1, 1) in enemyCounter: #...
                        setupState.append((7, 2, (place[0] + 2, place[1] + 2)))
                    # Setup 16
                    if (-1, 1) in enemyCounter and (1, 1) in enemyCounter and ((3, 3) in enemyCounter or (1, 3) in enemyCounter): #...
                        setupState.append((16, 1, (place[0] + 2, place[1] + 2)))
                # Jump backward over an enemy at left side
                if (place[0] - 2, place[1] - 2) in self.legalMove[piece][0]:
                    # Setup 2
                    if (-1, -1) in enemyCounter:
                        setupState.append((2, 2, (place[0] - 2, place[1] - 2)))
                # Jump backward over an enemy at right side
                if (place[0] + 2, place[1] - 2) in self.legalMove[piece][0]:
                    # Setup 2
                    if (1, -1) in enemyCounter:
                        setupState.append((2, 2, (place[0] + 2, place[1] - 2)))
                # Move forward at right side
                if (place[0] - 1, place[1] + 1) in self.legalMove[piece][0]:
                    # Setup 1
                    if (-2, 2) not in enemyCounter and (0, 2) not in enemyCounter:
                        setupState.append((1, 12, (place[0] - 1, place[1] + 1)))
                    # Setup 3
                    if (2, 2) in enemyCounter and (0, 2) not in enemyCounter:
                        setupState.append((3, 11, (place[0] - 1, place[1] + 1)))
                    # Setup 4
                    if (1, 1) in enemyCounter and (2, 2) in enemyCounter and (-2, 2) not in enemyCounter:
                        setupState.append((4, 6, (place[0] - 1, place[1] + 1)))
                    # Setup 5
                    if (0, 2) in enemyCounter and (-2, 2) not in enemyCounter and (-2, 0) in allyCounter:
                        setupState.append((5, 10, (place[0] - 1, place[1] + 1)))
                    # Setup 9
                    if (((-2, -2) in enemyCounter and enemyCounterRole[enemyCounter.index((-2, -2))] == "King") or ((0, -2) in enemyCounter and enemyCounterRole[enemyCounter.index((0, -2))] == "King") or ((2, -2) in enemyCounter and enemyCounterRole[enemyCounter.index((2, -2))] == "King")) and (-2, 2) in enemyCounter:
                        setupState.append((9, 11, (place[0] - 1, place[1] + 1)))
                    # Setup 10
                    if (1, 1) in enemyCounter and (2, 2) in outOfBound and (-2, 2) not in enemyCounter:
                        setupState.append((10, 6, (place[0] - 1, place[1] + 1)))
                    # Setup 11
                    if (-2, 2) in outOfBound and (0, 2) in outOfBound and (2, 2) in outOfBound:
                        setupState.append((11, 7, (place[0] - 1, place[1] + 1)))
                    # Setup 12
                    if (2, 2) in enemyCounter and (0, 2) in enemyCounter and ((-3, 3) in outOfBound and (-1, 3) in outOfBound and (1, 3) in outOfBound and (3, 3) in outOfBound):
                        setupState.append((12, 8, (place[0] - 1, place[1] + 1)))
                    # Setup 13
                    if (1, 1) in enemyCounter and ((-2, 2) in outOfBound or (0, 2) in outOfBound or (2, 2) in outOfBound):
                        setupState.append((13, 4, (place[0] - 1, place[1] + 1)))
                    # Setup 14
                    if (-2, 2) in enemyCounter and (0, 2) in enemyCounter and (-2, 0) in allyCounter and (1, -1) in allyCounter and (2, -2) in outOfBound:
                        setupState.append((14, 9, (place[0] - 1, place[1] + 1)))
                    # Setup 15
                    if (-2, 2) in enemyCounter and (0, 2) in enemyCounter and (-2, 0) in allyCounter and (1, -1) in allyCounter and (2, -2) in allyCounter:
                        setupState.append((15, 9, (place[0] - 1, place[1] + 1)))
                    # Setup 17
                    if (0, 2) in enemyCounter and (-2, 0) in outOfBound:
                        setupState.append((17, 10, (place[0] - 1, place[1] + 1)))
                # Move forward at left side
                if (place[0] + 1, place[1] + 1) in self.legalMove[piece][0]:
                    # Setup 1
                    if (2, 2) not in enemyCounter and (0, 2) not in enemyCounter:
                        setupState.append((1, 12, (place[0] + 1, place[1] + 1)))
                    # Setup 3
                    if (-2, 2) in enemyCounter and (0, 2) not in enemyCounter:
                        setupState.append((3, 11, (place[0] + 1, place[1] + 1)))
                    # Setup 4
                    if (-1, 1) in enemyCounter and (-2, 2) in enemyCounter and (2, 2) not in enemyCounter:
                        setupState.append((4, 6, (place[0] + 1, place[1] + 1)))
                    # Setup 5
                    if (0, 2) in enemyCounter and (2, 2) not in enemyCounter and (2, 0) in allyCounter:
                        setupState.append((5, 10, (place[0] + 1, place[1] + 1)))
                    # Setup 9
                    if (((-2, -2) in enemyCounter and enemyCounterRole[enemyCounter.index((-2, -2))] == "King") or ((0, -2) in enemyCounter  and enemyCounterRole[enemyCounter.index((0, -2))] == "King") or ((2, -2) in enemyCounter and enemyCounterRole[enemyCounter.index((2, -2))] == "King")) and (2, 2) in enemyCounter:
                        setupState.append((9, 11, (place[0] + 1, place[1] + 1)))
                    # Setup 10
                    if (-1, 1) in enemyCounter and (-2, 2) in outOfBound and (2, 2) not in enemyCounter:
                        setupState.append((10, 6, (place[0] + 1, place[1] + 1)))
                    # Setup 11
                    if (-2, 2) in outOfBound and (0, 2) in outOfBound and (2, 2) in outOfBound:
                        setupState.append((11, 7, (place[0] + 1, place[1] + 1)))
                    # Setup 12
                    if (-2, 2) in enemyCounter and (0, 2) in enemyCounter and ((-3, 3) in outOfBound and (-1, 3) in outOfBound and (1, 3) in outOfBound and (3, 3) in outOfBound):
                        setupState.append((12, 8, (place[0] + 1, place[1] + 1)))
                    # Setup 13
                    if (-1, 1) in enemyCounter and ((-2, 2) in outOfBound or (0, 2) in outOfBound or (2, 2) in outOfBound):
                        setupState.append((13, 4, (place[0] + 1, place[1] + 1)))
                    # Setup 14
                    if (0, 2) in enemyCounter and (2, 2) in enemyCounter and (2, 0) in allyCounter and (-1, -1) in allyCounter and (-2, -2) in outOfBound:
                        setupState.append((14, 9, (place[0] + 1, place[1] + 1)))
                    # Setup 15
                    if (0, 2) in enemyCounter and (2, 2) in enemyCounter and (2, 0) in allyCounter and (-1, -1) in allyCounter and (-2, -2) in allyCounter:
                        setupState.append((15, 9, (place[0] + 1, place[1] + 1)))
                    # Setup 17
                    if (0, 2) in enemyCounter and (2, 0) in outOfBound:
                        setupState.append((17, 10, (place[0] + 1, place[1] + 1)))
                # Move backward at left side
                if (place[0] - 1, place[1] - 1) in self.legalMove[piece][0]:
                    # Setup 1
                    if (-2, -2) not in enemyCounter or (0, -2) not in enemyCounter:
                        setupState.append((1, 12, (place[0] - 1, place[1] - 1)))
                    # Setup 6
                    if (-1, 1) in enemyCounter and (1, 1) in enemyCounter and (-2, 2) in enemyCounter and (2, 2) in enemyCounter:
                        setupState.append((6, 5, (place[0] - 1, place[1] - 1)))
                    # Setup 8
                    if ((-2, -2) in enemyCounter and enemyCounterRole[enemyCounter.index((-2, -2))] == "Man") or ((0, -2) in enemyCounter and enemyCounterRole[enemyCounter.index((0, -2))] == "Man"):
                        setupState.append((8, 10, (place[0] - 1, place[1] - 1)))
                # Move backward at right side
                if (place[0] + 1, place[1] - 1) in self.legalMove[piece][0]:
                    # Setup 1
                    if (2, -2) not in enemyCounter or (0, -2) not in enemyCounter:
                        setupState.append((1, 12, (place[0] + 1, place[1] - 1)))
                    # Setup 6
                    if (-1, 1) in enemyCounter and (1, 1) in enemyCounter and (-2, 2) in enemyCounter and (2, 2) in enemyCounter:
                        setupState.append((6, 5, (place[0] + 1, place[1] - 1)))
                    # Setup 8
                    if ((0, -2) in enemyCounter and enemyCounterRole[enemyCounter.index((0, -2))] == "Man") or ((2, -2) in enemyCounter and enemyCounterRole[enemyCounter.index((2, -2))] == "Man"):
                        setupState.append((8, 10, (place[0] + 1, place[1] - 1)))

                # Finding the best move for the piece
                if len(setupState) == 0:
                    bestMove.append((0, float('inf'), place))
                else:
                    tupleList = [tup[1] for tup in setupState]
                    bestMove.append(setupState[tupleList.index(min(tupleList))])
                    
        # Finding the best move for the state given as (setup, priority, direction)
        priorityList = [tup[1] for tup in bestMove]
        idx = priorityList.index(min(priorityList))
        chosen = bestMove[idx]
        chosenPiece = list(self.state[0].keys())[idx]

        # The heuristic score for minimax
        score = (13 - chosen[1]) + (len(self.state[0]) - len(self.state[1]))

        return score, (chosenPiece, chosen[2])
    
    # Updating the placement given in the state
    def update_places(self, piece, place, role, AI_turn = True, death = None):
        # Make a copy of the state
        self.newState = copy.deepcopy(self.state)
        # Giving the new role
        if AI_turn:
            if place[1] == 8:
                newRole = "King"
            else:
                newRole = role
        else:
            if place[1] == 0:
                newRole = "King"
            else:
                newRole = role
        
        # Update the death in the turn
        if death is not None:
            # Store the already occupied spaces
            allyOccupancy = [elem[0] for elem in list(self.state[0].values())]
            enemyOccupancy = [elem[0] for elem in list(self.state[1].values())]
            
            # If the death is an ally
            if death in allyOccupancy:
                # Find the piece and replace its role
                idx = allyOccupancy.index(death)
                self.newState[0].pop(list(self.state[0].keys())[idx])
            # If the death is an enemy
            elif death in enemyOccupancy:
                # Find the piece and replace its role
                idx = enemyOccupancy.index(death)
                self.newState[1].pop(list(self.state[1].keys())[idx])
        
        # Place the new position and role
        self.newState[0 if AI_turn else 1][piece] = [place, newRole]

        # Return the new state
        return self.newState

# The H-minimax strategy with aplha-beta pruning (https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#Pseudocode)
def H_minimax(node, depth, maximizingPlayer = True, alpha = float('-inf'), beta = float('inf')):
    # Generate the children of the node
    children = node.generate_child(maximizingPlayer)
    
    # If the limited depth has been reached
    if depth == 0 or len(children) == 0:
        # Evalute the heuristic value
        try:
            score, chosen = node.best_move()
        except:
            score = float('inf')
            chosen = 0

        # Return the node score
        return score, chosen

    # The chosen child
    childIdx = 0

    # If player is max
    if maximizingPlayer:
        # Set alpha to -infinty
        value = float('inf')
        # Go through every child in the state
        for idx, child in enumerate(children):
            # Evaluate the childs minimax value decide the max value to set alpha
            eval, _ = H_minimax(child, depth - 1, False, alpha, beta)
            if value < eval:
                value = eval
                childIdx = idx
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
        for idx, child in enumerate(children):
            # Evaluate the childs minimax value decide the min value to set beta
            eval, _ = H_minimax(child, depth - 1, True, alpha, beta)
            if value > eval:
                value = eval
                childIdx = idx
            # Break out of loop if alpha is the bigger number
            if value < alpha:
                break
            # Update beta
            beta = min(beta, value)

    # Return the final value
    return value, childIdx

if __name__ == "__main__":
    # The initial position of the pieces
    #start_place = [{"B1": [(2, 1), "Man"], "B2": [(4, 1), "Man"], "B3": [(6, 1), "Man"], "B4": [(8, 1), "Man"],
    #                "B5": [(1, 2), "Man"], "B6": [(3, 2), "Man"], "B7": [(5, 2), "Man"], "B8": [(7, 2), "Man"],
    #                "B9": [(2, 3), "Man"], "B10": [(4, 3), "Man"], "B11": [(6, 3), "Man"], "B12": [(8, 3), "Man"]},
    #               {"R1": [(2, 8), "Man"], "R2": [(4, 8), "Man"], "R3": [(6, 8), "Man"], "R4": [(8, 8), "Man"],
    #                "R5": [(1, 7), "Man"], "R6": [(3, 7), "Man"], "R7": [(5, 7), "Man"], "R8": [(7, 7), "Man"],
    #                "R9": [(2, 6), "Man"], "R10": [(4, 6), "Man"], "R11": [(6, 6), "Man"], "R12": [(8, 6), "Man"]}]

    # Testing setups
    start_place = [{"B1": [(7, 5), "Man"]},
                   {"R1": [(7, 7), "Man"]}]

    # The original node
    root = Node(start_place)
    # The amount of steps taken in minimax, this should be an even number over 0
    step = 10

    # Normal minimax operation
    if step > 0:
        _, theChosenOne = H_minimax(root, step)
        child = root.children[theChosenOne]
        print(root.state)
        print(child.state)
    # Only checking the next step
    else:
        _, theChosenOne = H_minimax(root, 0)
        root.update_places(theChosenOne[0], theChosenOne[1], root.state[0][theChosenOne[0]][1])
        print(root.state)
        print(root.newState)
    