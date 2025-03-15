import copy

# Class for all nodes given to a state
class Node:
    # Initialise the Node class
    def __init__(self, state, parent = None):
        # The current state, should be a dictionary for each piece location
        self.state = state
        # The previous state, should be another object of the Node class
        self.parent = parent

    # Determine the legal moves for each piece
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
            for idx, (row, col) in enumerate(moveList):
                # Check if there is no wall blocking
                if row > 0 and row < 8 and col > 0 and col < 8:
                    # Ignore spaces with black pieces
                    if (row, col) in allyOccupancy:
                        allyCounter.append(idx)
                        continue
                    # Ignore spaces with red pieces
                    elif (row, col) in enemyOccupancy:
                        enemyCounter.append(idx)
                        continue

                    # Jump over a red pieces
                    if idx > len(moveList) / 2 - 1 and idx - len(moveList) / 2 not in enemyCounter:
                        continue
                    # Don't jump over black pieces
                    elif idx - len(moveList) / 2 in allyCounter:
                        continue

                    # Append the non-filtered tiles from move set
                    tiles.append((row, col))

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
        allyOccupancy = [elem[0] for elem in list(self.state[0].values())]
        enemyOccupancy = [elem[0] for elem in list(self.state[1].values())]

        for piece, (place, role) in self.legalMove.items():
            for (row, col) in place:
                print("Something")
            

    
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
