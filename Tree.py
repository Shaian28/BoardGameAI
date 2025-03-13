import copy

# Class for all nodes given to a state
class Node:
    # Initialise the Node class
    def __init__(self, state, parent = None):
        # The current state, should be a dictionary for each piece location
        self.state = state
        # The previous state, should be another object of the Node class
        self.parent = parent
        # Calculate all the legal moves for each pieces
        self.legal_moves()

    # Determine the legal moves for each piece
    def legal_moves(self):
        # Copy the current piece placement
        self.legalMove = copy.deepcopy(self.state[0])

        # Store the already occupied spaces
        blackOccupancy = [elem[0] for elem in list(self.state[0].values())]
        redOccupancy = [elem[0] for elem in list(self.state[1].values())]

        # Iterate through the pieces and places of the pieces
        for piece, place in self.state[0].items():
            # All the legal movement (assuming king and jump)
            moveList = [(place[0][0] - 1, place[0][1] + 1), (place[0][0] + 1, place[0][1] + 1), (place[0][0] - 2, place[0][1] + 2),
                        (place[0][0] + 2, place[0][1] + 2)] if place[1] == "Man" else [(place[0][0] - 1, place[0][1] - 1),
                        (place[0][0] - 1, place[0][1] + 1), (place[0][0] + 1, place[0][1] - 1), (place[0][0] + 1, place[0][1] + 1),
                        (place[0][0] - 2, place[0][1] - 2), (place[0][0] - 2, place[0][1] + 2), (place[0][0] + 2, place[0][1] - 2),
                        (place[0][0] + 2, place[0][1] + 2)]

            # Initialise tiles and counters
            tiles = []
            blackCounter = []
            redCounter = []

            # Iterate through the rows and coloumns of the piece
            for idx, (row, col) in enumerate(moveList):
                # Check if there is no wall blocking
                if row > 0 and row < 8 and col > 0 and col < 8:
                    # Ignore spaces with black pieces
                    if (row, col) in blackOccupancy:
                        blackCounter.append(idx)
                        continue
                    # Ignore spaces with red pieces
                    elif (row, col) in redOccupancy:
                        redCounter.append(idx)
                        continue

                    # Jump over a red pieces
                    if idx > len(moveList) / 2 - 1 and idx - len(moveList) / 2 not in redCounter:
                        continue
                    # Don't jump over black pieces
                    elif idx - len(moveList) / 2 in blackCounter:
                        continue

                    # Append the non-filtered tiles from move set
                    tiles.append((row, col))

            # Store the legal moves
            self.legalMove[piece] = tiles

    # Generate next states of the Node class
    def generate_child(self, child):
        # The initialisation next state
        children = []
        

    # Determining the best move for the current state
    def best_move(self):
        self.chosenPiece = "B12"                        # Example
        self.chosenMove = self.action["B12"][0]         # Example
    
    # Updating the placement given in the state
    def update_places(self, piece, place):
        newState = copy.deepcopy(self.state)
        newState[0][piece] = place
        return newState

# The H-minimax strategy with aplha-beta pruning (https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#Pseudocode)
def H_minimax(node, depth, maximizingPlayer = True, alpha = float('-inf'), beta = float('inf')):
    # If the limited depth has been reached
    if depth == 0 or not node.children:
        # Evalute the heuristic value
        return len(node.state[0]) - len(node.state[1])

    # If player is max
    if maximizingPlayer:
        # Set alpha to -infinty
        value = float('-inf')
        # Go through every child in the state
        for child in node.children:
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
        for child in node.children:
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
    root.legal_moves()
    print(root.legalMove)
    
