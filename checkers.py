import numpy as np

class Checkers:
    def __init__(self):
        self.board = self.initialize_board()
        self.current_player = "black"

    def initialize_board(self):
        board = np.full((8, 8), " ", dtype=object)  # Use spaces for empty squares
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row, col] = "b"  # Black pieces
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row, col] = "r"  # Red pieces
        return board

    def print_board(self):
        print("\n  0 1 2 3 4 5 6 7")  # Column indices
        for i, row in enumerate(self.board):
            print(i, " ".join(row))  # Row index and board row
        print()

    def is_valid_move(self, path):
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            piece = self.board[x1, y1]
            if piece == " " or self.board[x2, y2] != " ":
                return False  # Must move a piece and land on an empty square

            direction = 1 if piece.lower() == "b" else -1  # Normal move direction
            is_king = piece.isupper()

            # One-step move for kings (forward and backward, per American rules)
            if abs(x2 - x1) == 1 and abs(y2 - y1) == 1:
                if is_king or (x2 - x1 == direction):
                    continue  # Simple move forward
                else:
                    return False

            # Capture move (mandatory if possible)
            if abs(x2 - x1) == 2 and abs(y2 - y1) == 2:
                mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
                mid_piece = self.board[mid_x, mid_y]
                if mid_piece.lower() in ["b", "r"] and mid_piece.lower() != piece.lower():
                    continue  # Valid capture
                else:
                    return False
            return False
        return True

    def move_piece(self, path):
        x1, y1 = path[0]
        piece = self.board[x1, y1]
        self.board[x1, y1] = " "

        for i in range(1, len(path)):
            x2, y2 = path[i]
            self.board[x2, y2] = piece
            if abs(x2 - x1) == 2:  # Capture move
                mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
                self.board[mid_x, mid_y] = " "
            x1, y1 = x2, y2

        if (x1 == 7 and piece == "b") or (x1 == 0 and piece == "r"):
            self.board[x1, y1] = piece.upper()  # Promote to king

        self.current_player = "red" if self.current_player == "black" else "black"

    def get_player_input(self):
        while True:
            try:
                move = input(f"{self.current_player}'s turn (format: x1 y1 x2 y2 ...): ").split()
                if len(move) < 4 or len(move) % 2 != 0:
                    raise ValueError("Invalid input format!")
                path = [(int(move[i]), int(move[i + 1])) for i in range(0, len(move), 2)]
                if self.is_valid_move(path):
                    return path
                else:
                    print("Invalid move! Try again.")
            except ValueError as e:
                print(e)

    def play(self):
        while True:
            self.print_board()
            path = self.get_player_input()
            self.move_piece(path)

if __name__ == "__main__":
    game = Checkers()
    game.play()
