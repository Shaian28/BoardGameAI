# Python libraries
import copy
from collections import defaultdict

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
        current = self.state[0 if AI_turn else 1]
        self.legalMove = copy.deepcopy(current)
        moveList = copy.deepcopy(current)
        
        # Store the already occupied spaces and roles
        allyOccupancy = [elem[0] for elem in list(current.values())]
        enemyOccupancy = [elem[0] for elem in list(self.state[1 if AI_turn else 0].values())]

        # List of pieces that can kill
        killList = defaultdict(list)
        self.multiKill = []
        killCondition = False

        # Iterate through the pieces and places of the pieces
        for piece, (place, role) in current.items():
            # When it is AI's turn
            if AI_turn:
                # All the legal movement for man
                if role == "Man":
                    moveList[piece] = [(place[0] - 1, place[1] + 1), (place[0] + 1, place[1] + 1),
                                       (place[0] - 2, place[1] + 2), (place[0] + 2, place[1] + 2)]
                # All the legal movement for king
                elif role == "King":
                    moveList[piece] = [(place[0] - 1, place[1] - 1), (place[0] - 1, place[1] + 1),
                                       (place[0] + 1, place[1] - 1), (place[0] + 1, place[1] + 1),
                                       (place[0] - 2, place[1] - 2), (place[0] - 2, place[1] + 2),
                                       (place[0] + 2, place[1] - 2), (place[0] + 2, place[1] + 2)]
            # When it is the players turn
            else:
                # All the legal movement for man
                if role == "Man":
                    moveList[piece] = [(place[0] - 1, place[1] - 1), (place[0] + 1, place[1] - 1),
                                       (place[0] - 2, place[1] - 2), (place[0] + 2, place[1] - 2)]
                # All the legal movement for king
                elif role == "King":
                    moveList[piece] = [(place[0] - 1, place[1] - 1), (place[0] - 1, place[1] + 1),
                                       (place[0] + 1, place[1] - 1), (place[0] + 1, place[1] + 1),
                                       (place[0] - 2, place[1] - 2), (place[0] - 2, place[1] + 2),
                                       (place[0] + 2, place[1] - 2), (place[0] + 2, place[1] + 2)]
                    
            # Initialise tiles and counters
            allyCounter = []
            enemyCounter = []

            # Iterate through the rows and coloumns of the piece
            for idx, (col, row) in enumerate(moveList[piece]):
                # Check if there is no wall blocking
                if col > -1 and col < 8 and row > -1 and row < 8:
                    # Ignore spaces with ally pieces
                    if (col, row) in allyOccupancy:
                        allyCounter.append(idx)
                        continue
                    # Ignore spaces with enemy pieces
                    elif (col, row) in enemyOccupancy:
                        enemyCounter.append(idx)
                        continue
                    
                    # For the jumps
                    if idx >= len(moveList[piece]) / 2:
                        # Skip if no kill is allowed
                        if len(enemyCounter) == 0:
                            break
                        # Jump over enemy pieces
                        elif idx - len(moveList[piece]) / 2 in enemyCounter:
                            # Remember the kill
                            killCondition = True
                            killList[piece].append((col, row))
        
        # When pieces can kill
        if killCondition:
            # Iterate through the pieces and places of the pieces
            for piece, (place, role) in current.items():
                tiles = []
                allTiles = []
                if piece in killList.keys():
                    for addTiles in killList[piece]:
                        # It only register the first kill
                        tiles = [addTiles]
                        killedPiece = [(place[0] + (tiles[-1][0] - place[0]) // 2, place[1] + (tiles[-1][1] - place[1]) // 2)]
                        jump = True
                        while jump:
                            newKill = False
                            # When it is AI's turn
                            if AI_turn:
                                # All the legal movement for man
                                if role == "Man":
                                    moveList[piece] = [(tiles[-1][0] - 1, tiles[-1][1] + 1), (tiles[-1][0] + 1, tiles[-1][1] + 1),
                                                       (tiles[-1][0] - 2, tiles[-1][1] + 2), (tiles[-1][0] + 2, tiles[-1][1] + 2)]
                                # All the legal movement for king
                                elif role == "King":
                                    moveList[piece] = [(tiles[-1][0] - 1, tiles[-1][1] - 1), (tiles[-1][0] - 1, tiles[-1][1] + 1),
                                                       (tiles[-1][0] + 1, tiles[-1][1] - 1), (tiles[-1][0] + 1, tiles[-1][1] + 1),
                                                       (tiles[-1][0] - 2, tiles[-1][1] - 2), (tiles[-1][0] - 2, tiles[-1][1] + 2),
                                                       (tiles[-1][0] + 2, tiles[-1][1] - 2), (tiles[-1][0] + 2, tiles[-1][1] + 2)]
                            # When it is the players turn
                            else:
                                # All the legal movement for man
                                if role == "Man":
                                    moveList[piece] = [(tiles[-1][0] - 1, tiles[-1][1] - 1), (tiles[-1][0] + 1, tiles[-1][1] - 1),
                                                       (tiles[-1][0] - 2, tiles[-1][1] - 2), (tiles[-1][0] + 2, tiles[-1][1] - 2)]
                                # All the legal movement for king
                                elif role == "King":
                                    moveList[piece] = [(tiles[-1][0] - 1, tiles[-1][1] - 1), (tiles[-1][0] - 1, tiles[-1][1] + 1),
                                                       (tiles[-1][0] + 1, tiles[-1][1] - 1), (tiles[-1][0] + 1, tiles[-1][1] + 1),
                                                       (tiles[-1][0] - 2, tiles[-1][1] - 2), (tiles[-1][0] - 2, tiles[-1][1] + 2),
                                                       (tiles[-1][0] + 2, tiles[-1][1] - 2), (tiles[-1][0] + 2, tiles[-1][1] + 2)]
                            # Initialise tiles and counters
                            allyCounter = []
                            enemyCounter = []
                            
                            # Iterate through the rows and coloumns of the piece
                            for idx, (col, row) in enumerate(moveList[piece]):
                                # Check if there is no wall blocking
                                if col > -1 and col < 8 and row > -1 and row < 8:
                                    # Ignore spaces with ally pieces
                                    if (col, row) in allyOccupancy:
                                        allyCounter.append(idx)
                                        continue
                                    # Ignore spaces with enemy pieces
                                    elif (col, row) in enemyOccupancy:
                                        enemyCounter.append(idx)
                                        continue
                                    
                                    # For the jumps
                                    if idx >= len(moveList[piece]) // 2 and (idx not in enemyCounter or idx not in allyCounter):
                                        # Skip if no kill is allowed
                                        if (len(enemyCounter) == 0 and role == "Man") or (len(enemyCounter) <= 1 and role == "King"):
                                            jump = False
                                            break
                                        # Jump over enemy pieces
                                        elif idx - len(moveList[piece]) // 2 in enemyCounter and moveList[piece][idx - len(moveList[piece]) // 2] not in killedPiece:
                                            killedPiece.append((tiles[-1][0] + (col - tiles[-1][0]) // 2, tiles[-1][1] + (row - tiles[-1][1]) // 2))
                                            tiles.append((col, row))
                                            newKill = True
                                            self.multiKill.append(piece)
                                    
                                    # When there hasn't been any new kills after the previous kill
                                    if idx  == len(moveList[piece]) - 1 and not newKill:
                                        jump = False
                            
                            # When the search didn't find new kills
                            if not newKill:
                                jump = False

                        allTiles.append(tiles)
                
                maxTile = 0
                finalIdx = 0
                for idx, choose in enumerate(allTiles):
                    if len(choose) > maxTile:
                        finalIdx = idx
                # Store the legal moves
                self.legalMove[piece] = [tiles, role] if len(allTiles) == 0 else [allTiles[finalIdx], role]
        # When no pieces can kill
        else:
            # Iterate through the pieces and places of the pieces
            for piece, (place, role) in current.items():
                # Initialise tiles and counters
                tiles = []
                allyCounter = []
                enemyCounter = []
                # Iterate through the rows and coloumns of the piece
                for idx, (col, row) in enumerate(moveList[piece]):
                    # Check if there is no wall blocking
                    if col > -1 and col < 8 and row > -1 and row < 8:
                        # Ignore spaces with ally pieces
                        if (col, row) in allyOccupancy:
                            allyCounter.append(idx)
                            continue
                        # Ignore spaces with enemy pieces
                        elif (col, row) in enemyOccupancy:
                            enemyCounter.append(idx)
                            continue
                        
                        # Jump over enemy pieces
                        if idx >= len(moveList[piece]) / 2 and idx - len(moveList[piece]) / 2 not in enemyCounter:
                            continue
                        # Don't jump over ally pieces
                        elif idx - len(moveList[piece]) / 2 in allyCounter:
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
            # Get the piece and initialise
            piecePlace = self.state[0 if AI_turn else 1][piece][0]
            # Continue if there is no legal moves for the piece
            if len(move) == 0:
                continue
            # For pieces with multiple kills
            if piece in self.multiKill:
                # Initialise death counter and old placement
                deathCounter = []
                oldPlace = piecePlace
                # Go through all the places, the legal moves brings the piece
                for place in move:
                    # Check if a kill condition has been met
                    if abs(oldPlace[0] - place[0]) > 1 and abs(oldPlace[1] - place[1]) > 1:
                        deathCounter.append((oldPlace[0] + (place[0] - oldPlace[0]) // 2, oldPlace[1] + (place[1] - oldPlace[1]) // 2))
                    # Update old place
                    oldPlace = place
                # Update the map to the new place
                newState = self.update_places(piece, move[-1], role, AI_turn = AI_turn, death = deathCounter)
                # Create the child
                child_node = Node(newState, parent = self)
                # Append the child in the list
                self.children.append(child_node)
            # For pieces without multiple kills
            else:
                # Initialise death counter
                deathCounter = 0
                # Go through all the places, the legal moves brings the piece
                for place in move:
                    # Check if a kill condition has been met
                    if abs(piecePlace[0] - place[0]) > 1 and abs(piecePlace[1] - place[1]) > 1:
                        deathCounter = (piecePlace[0] + (place[0] - piecePlace[0]) // 2, piecePlace[1] + (place[1] - piecePlace[1]) // 2)
                    # Update the map to the new place
                    newState = self.update_places(piece, place, role, AI_turn = AI_turn, death = [deathCounter])
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
            if self.multiKill == piece:
                legalMove = self.legalMove[piece][0][0]
            else:
                legalMove = self.legalMove[piece][0]
            
            if len(legalMove) == 0:
                bestMove.append((0, 0, place))
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
                    elif col < 0 or col > 7 or row < 0 or row > 7:
                        outOfBound.append((x, y))
                
                # Jump forward over an enemy at left side
                if (place[0] - 2, place[1] + 2) in legalMove:
                    # Setup 2
                    if (-1, 1) in enemyCounter:
                        setupState.append((2, 10, (place[0] - 2, place[1] + 2)))
                    # Setup 7
                    if (-1, 1) in enemyCounter and piece in self.multiKill:
                        setupState.append((7, 11, (place[0] - 2, place[1] + 2)))
                    # Setup 16
                    if (-1, 1) in enemyCounter and (1, 1) in enemyCounter and piece in self.multiKill:
                        setupState.append((16, 12, (place[0] - 2, place[1] + 2)))
                # Jump forward over an enemy at right side
                if (place[0] + 2, place[1] + 2) in legalMove:
                    # Setup 2
                    if (1, 1) in enemyCounter:
                        setupState.append((2, 10, (place[0] + 2, place[1] + 2)))
                    # Setup 7
                    if (1, 1) in enemyCounter and piece in self.multiKill:
                        setupState.append((7, 11, (place[0] + 2, place[1] + 2)))
                    # Setup 16
                    if (1, 1) in enemyCounter and (-1, 1) in enemyCounter and piece in self.multiKill:
                        setupState.append((16, 12, (place[0] + 2, place[1] + 2)))
                # Jump backward over an enemy at left side
                if (place[0] - 2, place[1] - 2) in legalMove:
                    # Setup 2
                    if (-1, -1) in enemyCounter:
                        setupState.append((2, 11, (place[0] - 2, place[1] - 2)))
                # Jump backward over an enemy at right side
                if (place[0] + 2, place[1] - 2) in legalMove:
                    # Setup 2
                    if (1, -1) in enemyCounter:
                        setupState.append((2, 11, (place[0] + 2, place[1] - 2)))
                # Move forward at right side
                if (place[0] - 1, place[1] + 1) in legalMove:
                    # Setup 1
                    if (-2, 2) not in enemyCounter and (0, 2) not in enemyCounter:
                        setupState.append((1, 1, (place[0] - 1, place[1] + 1)))
                    # Setup 3
                    if (2, 2) in enemyCounter and (0, 2) not in enemyCounter:
                        setupState.append((3, 2, (place[0] - 1, place[1] + 1)))
                    # Setup 4
                    if (1, 1) in enemyCounter and (2, 2) in enemyCounter and (-2, 2) not in enemyCounter:
                        setupState.append((4, 7, (place[0] - 1, place[1] + 1)))
                    # Setup 5
                    if (0, 2) in enemyCounter and (-2, 2) not in enemyCounter and (-2, 0) in allyCounter:
                        setupState.append((5, 3, (place[0] - 1, place[1] + 1)))
                    # Setup 9
                    if (((-2, -2) in enemyCounter and enemyCounterRole[enemyCounter.index((-2, -2))] == "King") or ((0, -2) in enemyCounter and enemyCounterRole[enemyCounter.index((0, -2))] == "King") or ((2, -2) in enemyCounter and enemyCounterRole[enemyCounter.index((2, -2))] == "King")):
                        setupState.append((9, 2, (place[0] - 1, place[1] + 1)))
                    # Setup 10
                    if (1, 1) in enemyCounter and (2, 2) in outOfBound and (-2, 2) not in enemyCounter:
                        setupState.append((10, 7, (place[0] - 1, place[1] + 1)))
                    # Setup 11
                    if (-2, 2) in outOfBound and (0, 2) in outOfBound and (2, 2) in outOfBound:
                        setupState.append((11, 6, (place[0] - 1, place[1] + 1)))
                    # Setup 12
                    if (2, 2) in enemyCounter and ((-3, 3) in outOfBound and (-1, 3) in outOfBound and (1, 3) in outOfBound and (3, 3) in outOfBound):
                        setupState.append((12, 5, (place[0] - 1, place[1] + 1)))
                    # Setup 13
                    if (1, 1) in enemyCounter and ((-2, 2) in outOfBound and (0, 2) in outOfBound and (2, 2) in outOfBound):
                        setupState.append((13, 9, (place[0] - 1, place[1] + 1)))
                    # Setup 14
                    if (-2, 2) in enemyCounter and (0, 2) in enemyCounter and (-2, 0) in allyCounter and (1, -1) in allyCounter and (2, -2) in outOfBound:
                        setupState.append((14, 4, (place[0] - 1, place[1] + 1)))
                    # Setup 15
                    if (-2, 2) in enemyCounter and (0, 2) in enemyCounter and (-2, 0) in allyCounter and (1, -1) in allyCounter and (2, -2) in allyCounter:
                        setupState.append((15, 4, (place[0] - 1, place[1] + 1)))
                    # Setup 17
                    if (0, 2) in enemyCounter and (-2, 0) in outOfBound:
                        setupState.append((17, 3, (place[0] - 1, place[1] + 1)))
                # Move forward at left side
                if (place[0] + 1, place[1] + 1) in legalMove:
                    # Setup 1
                    if (2, 2) not in enemyCounter and (0, 2) not in enemyCounter:
                        setupState.append((1, 1, (place[0] + 1, place[1] + 1)))
                    # Setup 3
                    if (-2, 2) in enemyCounter and (0, 2) not in enemyCounter:
                        setupState.append((3, 2, (place[0] + 1, place[1] + 1)))
                    # Setup 4
                    if (-1, 1) in enemyCounter and (-2, 2) in enemyCounter and (2, 2) not in enemyCounter:
                        setupState.append((4, 7, (place[0] + 1, place[1] + 1)))
                    # Setup 5
                    if (0, 2) in enemyCounter and (2, 2) not in enemyCounter and (2, 0) in allyCounter:
                        setupState.append((5, 3, (place[0] + 1, place[1] + 1)))
                    # Setup 9
                    if (((-2, -2) in enemyCounter and enemyCounterRole[enemyCounter.index((-2, -2))] == "King") or ((0, -2) in enemyCounter  and enemyCounterRole[enemyCounter.index((0, -2))] == "King") or ((2, -2) in enemyCounter and enemyCounterRole[enemyCounter.index((2, -2))] == "King")):
                        setupState.append((9, 2, (place[0] + 1, place[1] + 1)))
                    # Setup 10
                    if (-1, 1) in enemyCounter and (-2, 2) in outOfBound and (2, 2) not in enemyCounter:
                        setupState.append((10, 7, (place[0] + 1, place[1] + 1)))
                    # Setup 11
                    if (-2, 2) in outOfBound and (0, 2) in outOfBound and (2, 2) in outOfBound:
                        setupState.append((11, 6, (place[0] + 1, place[1] + 1)))
                    # Setup 12
                    if (-2, 2) in enemyCounter and ((-3, 3) in outOfBound and (-1, 3) in outOfBound and (1, 3) in outOfBound and (3, 3) in outOfBound):
                        setupState.append((12, 5, (place[0] + 1, place[1] + 1)))
                    # Setup 13
                    if (-1, 1) in enemyCounter and ((-2, 2) in outOfBound and (0, 2) in outOfBound and (2, 2) in outOfBound):
                        setupState.append((13, 9, (place[0] + 1, place[1] + 1)))
                    # Setup 14
                    if (0, 2) in enemyCounter and (2, 2) in enemyCounter and (2, 0) in allyCounter and (-1, -1) in allyCounter and (-2, -2) in outOfBound:
                        setupState.append((14, 4, (place[0] + 1, place[1] + 1)))
                    # Setup 15
                    if (0, 2) in enemyCounter and (2, 2) in enemyCounter and (2, 0) in allyCounter and (-1, -1) in allyCounter and (-2, -2) in allyCounter:
                        setupState.append((15, 4, (place[0] + 1, place[1] + 1)))
                    # Setup 17
                    if (0, 2) in enemyCounter and (2, 0) in outOfBound:
                        setupState.append((17, 3, (place[0] + 1, place[1] + 1)))
                # Move backward at left side
                if (place[0] - 1, place[1] - 1) in legalMove:
                    # Setup 1
                    if (-2, -2) not in enemyCounter or (0, -2) not in enemyCounter:
                        setupState.append((1, 1, (place[0] - 1, place[1] - 1)))
                    # Setup 3
                    if ((2, 2) in enemyCounter and (0, 2) not in enemyCounter) or (((2, 2) in enemyCounter and (0, 2) not in enemyCounter)):
                        setupState.append((3, 2, (place[0] - 1, place[1] - 1)))
                    # Setup 4
                    if ((1, 1) in enemyCounter and (2, 2) in enemyCounter and (-2, 2) not in enemyCounter) or ((-1, 1) in enemyCounter and (-2, 2) in enemyCounter and (2, 2) not in enemyCounter):
                        setupState.append((4, 7, (place[0] - 1, place[1] - 1)))
                    # Setup 9
                    if (((-2, -2) in enemyCounter and enemyCounterRole[enemyCounter.index((-2, -2))] == "King") or ((0, -2) in enemyCounter and enemyCounterRole[enemyCounter.index((0, -2))] == "King") or ((2, -2) in enemyCounter and enemyCounterRole[enemyCounter.index((2, -2))] == "King")):
                        setupState.append((9, 2, (place[0] - 1, place[1] - 1)))
                    # Setup 10
                    if ((1, 1) in enemyCounter and (2, 2) in outOfBound and (-2, 2) not in enemyCounter) or ((-1, 1) in enemyCounter and (-2, 2) in outOfBound and (2, 2) not in enemyCounter):
                        setupState.append((10, 7, (place[0] - 1, place[1] - 1)))
                    # Setup 6
                    if (-1, 1) in enemyCounter and (1, 1) in enemyCounter and (-2, 2) in enemyCounter and (2, 2) in enemyCounter:
                        setupState.append((6, 8, (place[0] - 1, place[1] - 1)))
                    # Setup 8
                    if ((-2, -2) in enemyCounter and enemyCounterRole[enemyCounter.index((-2, -2))] == "Man") or ((0, -2) in enemyCounter and enemyCounterRole[enemyCounter.index((0, -2))] == "Man"):
                        setupState.append((8, 3, (place[0] - 1, place[1] - 1)))
                # Move backward at right side
                if (place[0] + 1, place[1] - 1) in legalMove:
                    # Setup 1
                    if (2, -2) not in enemyCounter or (0, -2) not in enemyCounter:
                        setupState.append((1, 1, (place[0] + 1, place[1] - 1)))
                    # Setup 3
                    if ((2, 2) in enemyCounter and (0, 2) not in enemyCounter) or (((2, 2) in enemyCounter and (0, 2) not in enemyCounter)):
                        setupState.append((3, 2, (place[0] + 1, place[1] - 1)))
                    # Setup 4
                    if ((1, 1) in enemyCounter and (2, 2) in enemyCounter and (-2, 2) not in enemyCounter) or ((-1, 1) in enemyCounter and (-2, 2) in enemyCounter and (2, 2) not in enemyCounter):
                        setupState.append((4, 7, (place[0] + 1, place[1] - 1)))
                    # Setup 9
                    if (((-2, -2) in enemyCounter and enemyCounterRole[enemyCounter.index((-2, -2))] == "King") or ((0, -2) in enemyCounter and enemyCounterRole[enemyCounter.index((0, -2))] == "King") or ((2, -2) in enemyCounter and enemyCounterRole[enemyCounter.index((2, -2))] == "King")):
                        setupState.append((9, 2, (place[0] + 1, place[1] - 1)))
                    # Setup 10
                    if ((1, 1) in enemyCounter and (2, 2) in outOfBound and (-2, 2) not in enemyCounter) or ((-1, 1) in enemyCounter and (-2, 2) in outOfBound and (2, 2) not in enemyCounter):
                        setupState.append((10, 7, (place[0] + 1, place[1] - 1)))
                    # Setup 6
                    if (-1, 1) in enemyCounter and (1, 1) in enemyCounter and (-2, 2) in enemyCounter and (2, 2) in enemyCounter:
                        setupState.append((6, 8, (place[0] + 1, place[1] - 1)))
                    # Setup 8
                    if ((0, -2) in enemyCounter and enemyCounterRole[enemyCounter.index((0, -2))] == "Man") or ((2, -2) in enemyCounter and enemyCounterRole[enemyCounter.index((2, -2))] == "Man"):
                        setupState.append((8, 3, (place[0] + 1, place[1] - 1)))

                # Finding the best move for the piece
                if len(setupState) == 0:
                    bestMove.append((0, 0, place))
                else:
                    tupleList = [tup[1] for tup in setupState]
                    bestMove.append(setupState[tupleList.index(max(tupleList))])
                    
        # Finding the best move for the state given as (setup, priority, direction)
        priorityList = [tup[1] for tup in bestMove]
        idx = priorityList.index(max(priorityList))
        chosen = bestMove[idx]
        chosenPiece = list(self.state[0].keys())[idx]

        # The heuristic score for minimax
        score = chosen[1] + (len(self.state[0]) - len(self.state[1]))
        
        return score, (chosenPiece, chosen)
    
    # Updating the placement given in the state
    def update_places(self, piece, place, role, AI_turn = True, death = None):
        # Make a copy of the state
        self.newState = copy.deepcopy(self.state)
        # Giving the new role
        if AI_turn:
            if place[1] == 7:
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
            for kill in death:
                # If the death is an ally
                if kill in allyOccupancy:
                    # Find the piece and replace its role
                    idx = allyOccupancy.index(kill)
                    self.newState[0].pop(list(self.state[0].keys())[idx])
                # If the death is an enemy
                elif kill in enemyOccupancy:
                    # Find the piece and replace its role
                    idx = enemyOccupancy.index(kill)
                    self.newState[1].pop(list(self.state[1].keys())[idx])
        
        # Place the new position and role
        self.newState[0 if AI_turn else 1][piece] = [place, newRole]
        
        # Return the new state
        return self.newState

# The H-minimax strategy with aplha-beta pruning (https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#Pseudocode)
def H_minimax(node, depth, maximizingPlayer = True, alpha = float('-inf'), beta = float('inf'), handMeDown = 0):
    # Generate the children of the node
    children = node.generate_child(maximizingPlayer)
    
    # If the limited depth has been reached
    if depth == 0 or len(children) == 0:
        # Initialize value
        chosen = 0
        # Calculate the best move
        try:
            compare_dicts(node.parent.state[0], node.state[0])
            score, chosen = node.best_move()
        # When no valid moves can be made
        except:
            score = float('-inf') if maximizingPlayer else float('inf')
        
        # Add it to the other scores
        handMeDown += score
        
        # Return the node score
        return handMeDown, chosen
    
    # The chosen child
    childIdx = 0

    # If player is max
    if maximizingPlayer:
        # Set alpha to -infinty
        value = float('-inf')
        # Go through every child in the state
        for idx, child in enumerate(children):
            # Initialize value
            chosen = 0
            # Calculate the best move
            try:
                if node.parent is not None:
                    compare_dicts(node.parent.state[0], node.state[0])
                score, chosen = node.best_move()
                handMeDown += score if child.state[0][chosen[0]][0] == chosen[1][2] else 0
            # When the childrens are dead
            except:
                score = float('-inf')
                handMeDown += score
            
            # Evaluate the childs minimax value decide the max value to set alpha
            eval, _ = H_minimax(child, depth - 1, False, alpha, beta, handMeDown)
            if value < eval:
                value = eval
                childIdx = idx
            
            # Break out of loop if beta is the smaller number
            if value > beta:
                break

            # Update alpha
            alpha = max(alpha, value)

        # Return the final value
        return value, childIdx

    # If the player is min
    else:
        # Set beta to -infinty
        value = float('inf')
        # Go through every child in the state
        for idx, child in enumerate(children):
            # Evaluate the childs minimax value decide the min value to set beta
            eval, _ = H_minimax(child, depth - 1, True, alpha, beta, handMeDown)
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

# Compare the states of the nodes to get the chosen piece and placement
def compare_dicts(dict1, dict2):
    # Go through all the keys
    for keys in dict1.keys():
        # Return the key, when there is a difference between the state
        if dict1[keys] != dict2[keys]:
            return keys

if __name__ == "__main__":
    # The setup prepared for testing
    setup = 17

    # The initial position of the pieces
    if setup == 0:
        start_place = [{"B1": [(1, 0), "Man"], "B2": [(3, 0), "Man"], "B3": [(5, 0), "Man"], "B4": [(7, 0), "Man"],
                        "B5": [(0, 1), "Man"], "B6": [(2, 1), "Man"], "B7": [(4, 1), "Man"], "B8": [(6, 1), "Man"],
                        "B9": [(1, 2), "Man"], "B10": [(3, 2), "Man"], "B11": [(5, 2), "Man"], "B12": [(7, 2), "Man"]},
                       {"R1": [(0, 7), "Man"], "R2": [(2, 7), "Man"], "R3": [(4, 7), "Man"], "R4": [(6, 7), "Man"],
                        "R5": [(1, 6), "Man"], "R6": [(3, 6), "Man"], "R7": [(5, 6), "Man"], "R8": [(7, 6), "Man"],
                        "R9": [(0, 5), "Man"], "R10": [(2, 5), "Man"], "R11": [(4, 5), "Man"], "R12": [(6, 5), "Man"]}]
    # Setup 1
    elif setup == 1:
        start_place = [{"B1": [(0, 1), "Man"], "B5": [(3, 2), "Man"], "B12": [(7, 0), "Man"]},
                       {"R1": [(0, 7), "Man"]}]
    # Setup 2
    elif setup == 2:
        start_place = [{"B1": [(0, 1), "Man"], "B5": [(3, 2), "Man"], "B12": [(7, 0), "Man"]},
                       {"R1": [(4, 3), "Man"]}]
    # Setup 3
    elif setup == 3:
        start_place = [{"B1": [(0, 1), "Man"], "B5": [(3, 2), "Man"], "B12": [(7, 0), "Man"]},
                       {"R1": [(1, 4), "Man"]}]
    # Setup 4
    elif setup == 4:
        start_place = [{"B1": [(0, 1), "Man"], "B5": [(3, 2), "Man"], "B12": [(7, 0), "Man"]},
                       {"R1": [(2, 3), "Man"], "R2": [(1, 4), "Man"]}]
    # Setup 5
    elif setup == 5:
        start_place = [{"B1": [(0, 1), "Man"], "B5": [(3, 2), "Man"], "B2": [(5, 2), "Man"], "B12": [(7, 0), "Man"]},
                       {"R1": [(3, 4), "Man"]}]
    # Setup 6
    elif setup == 6:
        start_place = [{"B1": [(0, 1), "Man"], "B5": [(3, 2), "King"], "B12": [(7, 0), "Man"]},
                       {"R1": [(2, 3), "Man"], "R2": [(1, 4), "Man"], "R3": [(4, 3), "Man"], "R4": [(5, 4), "Man"]}]
    # Setup 7
    elif setup == 7:
        start_place = [{"B1": [(0, 1), "Man"], "B5": [(3, 2), "Man"], "B12": [(7, 0), "Man"]},
                       {"R1": [(4, 3), "Man"], "R2": [(4, 5), "Man"]}]
    # Setup 8
    elif setup == 8:
        start_place = [{"B1": [(0, 1), "Man"], "B5": [(3, 4), "King"], "B12": [(7, 0), "Man"]},
                       {"R1": [(5, 2), "Man"]}]
    # Setup 9
    elif setup == 9:
        start_place = [{"B1": [(0, 1), "Man"], "B5": [(3, 4), "King"], "B12": [(7, 0), "Man"]},
                       {"R1": [(5, 2), "King"]}]
    # Setup 10
    elif setup == 10:
        start_place = [{"B1": [(0, 1), "Man"], "B5": [(1, 2), "Man"], "B12": [(7, 0), "Man"]},
                       {"R1": [(0, 3), "Man"]}]
    # Setup 11
    elif setup == 11:
        start_place = [{"B1": [(0, 1), "Man"], "B5": [(3, 6), "Man"], "B12": [(7, 0), "Man"]},
                       {"R1": [(0, 7), "Man"]}]
    # Setup 12
    elif setup == 12:
        start_place = [{"B1": [(0, 1), "Man"], "B5": [(4, 5), "Man"], "B12": [(7, 0), "Man"]},
                       {"R1": [(2, 7), "Man"]}]
    # Setup 13
    elif setup == 13:
        start_place = [{"B1": [(0, 1), "Man"], "B5": [(3, 6), "Man"], "B12": [(7, 0), "Man"]},
                       {"R1": [(2, 7), "Man"]}]
    # Setup 14
    elif setup == 14:
        start_place = [{"B1": [(0, 1), "Man"], "B5": [(1, 4), "Man"], "B2": [(3, 4), "Man"], "B3": [(0, 3), "Man"], "B12": [(7, 0), "Man"]},
                       {"R1": [(1, 6), "Man"], "R2": [(3, 6), "Man"]}]
    # Setup 15
    elif setup == 15:
        start_place = [{"B1": [(0, 1), "Man"], "B5": [(2, 3), "Man"], "B2": [(4, 3), "Man"], "B3": [(1, 2), "Man"], "B4": [(0, 1), "Man"], "B12": [(7, 0), "Man"]},
                       {"R1": [(2, 5), "Man"], "R2": [(4, 5), "Man"]}]
    # Setup 16
    elif setup == 16:
        start_place = [{"B1": [(0, 1), "Man"], "B5": [(2, 1), "Man"], "B12": [(7, 0), "Man"]},
                       {"R1": [(1, 2), "Man"], "R2": [(3, 2), "Man"], "R3": [(5, 4), "Man"]}]
    # Setup 17
    elif setup == 17:
        start_place = [{"B1": [(0, 1), "Man"], "B5": [(6, 1), "Man"], "B12": [(7, 0), "Man"]},
                       {"R1": [(6, 3), "Man"]}]

    # The original node
    root = Node(start_place)
    # The amount of steps taken in minimax, this should be an even number over 0
    step = 2

    # Normal minimax operation
    _, theChosenOne = H_minimax(root, step)
    child = root.children[theChosenOne]
    changePiece = compare_dicts(root.state[0], child.state[0])

    # Display the states and transition piece
    print(root.state)
    print(child.state)
    print(str(changePiece) + ":\t" + str(root.state[0][changePiece][0]) + " --> " + str(child.state[0][changePiece][0]))