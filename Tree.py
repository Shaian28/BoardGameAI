# Class for all nodes given to a state
class Node:
    # Initialise the Node class
    def __init__(self, state, parent = None, action = None):
        # The current state, should be a dictionary for each piece location
        self.state = state
        # The previous state, should be another object of the Node class
        self.parent = parent
        # The legal action that can be performed, should be a dictionary for each piece action
        self.action = action
        # The initialisation next state
        self.children = []

    # Add the next states of the Node class
    def add_child(self, child):
        # The next states, should be another object of the Node class
        self.children.append(child)

    # Determining the best move for the current state
    def best_move(self):
        return 0
    
    # Updating the placement given in the state
    def updatePlaces(self):
        return 0

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


# The initial position of the pieces
start_place = [{"B1": (2, 1), "B2": (4, 1), "B3": (6, 1), "B4": (8, 1),
                "B5": (2, 2), "B6": (4, 2), "B7": (6, 2), "B8": (8, 2),
                "B9": (2, 3), "B10": (4, 3), "B11": (6, 3), "B12": (8, 3)},
               {"R1": (2, 8), "R2": (4, 8), "R3": (6, 8), "R4": (8, 8),
                "R5": (2, 7), "R6": (4, 7), "R7": (6, 7), "R8": (8, 7),
                "R9": (2, 6), "R10": (4, 6), "R11": (6, 6), "R12": (8, 6)}]

# The initial actions that can be taken by each piece
start_action = {"B1": [], "B2": [], "B3": [], "B4": [],
               "B5": [], "B6": [], "B7": [], "B8": [],
               "B9": [(1, 4), (3, 4)], "B10": [(3, 4), (5, 4)], "B11": [(5, 4), (7, 4)], "B12": [(7, 4)]}

# The original node
root = Node(start_place, action = start_action)
