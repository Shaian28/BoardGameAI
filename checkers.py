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

    def is_valid_move(self, start, end):
        x1, y1 = start
        x2, y2 = end
        piece = self.board[x1, y1]
        if piece == " " or self.board[x2, y2] != " ":
            return False  # Must move a piece and land on an empty square
        
        direction = 1 if piece.lower() == "b" else -1  # Normal move direction
        is_king = piece.isupper()

        # One-step move for kings (forward and backward, per American rules)
        if abs(x2 - x1) == 1 and abs(y2 - y1) == 1:
            if is_king or (x2 - x1 == direction):
                return True  # Simple move forward

        # Capture move (mandatory if possible)
        if abs(x2 - x1) == 2 and abs(y2 - y1) == 2:
            mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
            mid_piece = self.board[mid_x, mid_y]
            if mid_piece.lower() in ["b", "r"] and mid_piece.lower() != piece.lower():
                return True  # Valid capture

        return False

    def move_piece(self, start, end):
        x1, y1 = start
        x2, y2 = end
        piece = self.board[x1, y1]
        self.board[x2, y2] = piece
        self.board[x1, y1] = " "

        if abs(x2 - x1) == 2:  # Capture move
            mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
            self.board[mid_x, mid_y] = " "

            if self.has_more_jumps((x2, y2)):
                self.print_board()
                new_end = self.get_player_input_single((x2, y2))
                self.move_piece((x2, y2), new_end)
                return

        if (x2 == 7 and piece == "b") or (x2 == 0 and piece == "r"):
            self.board[x2, y2] = piece.upper()  # Promote to king

        self.current_player = "red" if self.current_player == "black" else "black"

    def has_more_jumps(self, position):
        x, y = position
        piece = self.board[x, y]
        if piece == " ":
            return False

        directions = [(1, -1), (1, 1), (-1, -1), (-1, 1)] if piece.isupper() else [(1, -1), (1, 1)] if piece == "b" else [(-1, -1), (-1, 1)]

        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            mx, my = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8 and self.board[nx, ny] == " ":
                if self.board[mx, my].lower() in ["b", "r"] and self.board[mx, my].lower() != piece.lower():
                    return True
        return False

    def get_player_input(self):
        while True:
            try:
                move = input(f"Type your move (Format: StartRow StartColumn EndRow EndColumn): ").split()
                if len(move) != 4:
                    raise ValueError("Invalid input format!")
                start, end = (int(move[0]), int(move[1])), (int(move[2]), int(move[3]))
                if self.is_valid_move(start, end):
                    return start, end
                else:
                    print(f"{start} --> {end} is an invalid move")
            except ValueError as e:
                print(e)

    def get_player_input_single(self, start):
        while True:
            try:
                move = input(f"Continue jump from {start} (format: EndRow EndColumn): ").split()
                if len(move) != 2:
                    raise ValueError("Invalid input format!")
                end = (int(move[0]), int(move[1]))
                if self.is_valid_move(start, end):
                    return end
                else:
                    print("Invalid move! Try again.")
            except ValueError as e:
                print(e)

    def play(self):
        while True:
            self.print_board()
            start, end = self.get_player_input()
            self.move_piece(start, end)

if __name__ == "__main__":
    game = Checkers()
    game.play()
