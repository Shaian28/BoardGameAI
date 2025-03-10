import numpy as np

class Checkers:
    def __init__(self):
        self.board = self.initialize_board()
        self.current_player = "black"

    def initialize_board(self):
        board = np.zeros((8, 8), dtype=str)
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row, col] = "b"
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row, col] = "r"
        return board

    def print_board(self):
        for row in range(8):
            print(" ".join(self.board[row]))
        print()

    def is_valid_move(self, start, end):
        sx, sy = start
        ex, ey = end
        piece = self.board[sx, sy]
        if piece == "":
            return False
        if self.board[ex, ey] != "":
            return False
        if piece == "b" and (ex - sx != 1 or abs(ey - sy) != 1):
            return False
        if piece == "r" and (sx - ex != 1 or abs(ey - sy) != 1):
            return False
        return True

    def move_piece(self, start, end):
        if self.is_valid_move(start, end):
            sx, sy = start
            ex, ey = end
            self.board[ex, ey] = self.board[sx, sy]
            self.board[sx, sy] = ""
            self.current_player = "red" if self.current_player == "black" else "black"
        else:
            print("Invalid move")

    def play(self):
        moves = [((2, 1), (3, 2)), ((5, 2), (4, 3)), ((3, 2), (5, 4))]  # Example moves
        for start, end in moves:
            self.print_board()
            print(f"{self.current_player}'s turn: Moving from {start} to {end}")
            self.move_piece(start, end)

if __name__ == "__main__":
    game = Checkers()
    game.play()
