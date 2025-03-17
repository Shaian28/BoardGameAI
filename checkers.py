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
        sx, sy = start
        ex, ey = end
        piece = self.board[sx, sy]
        if piece == " ":
            return False  # No piece at start position
        if self.board[ex, ey] != " ":
            return False  # Destination must be empty
        
        direction = 1 if piece.lower() == "b" else -1  # Black moves down, Red moves up
        is_king = piece.isupper()

        # Regular move (diagonal by 1 step)
        if abs(ex - sx) == 1 and abs(ey - sy) == 1:
            if is_king or (ex - sx == direction):
                return True

        # Capture move (jumping over opponent)
        if abs(ex - sx) == 2 and abs(ey - sy) == 2:
            mid_x, mid_y = (sx + ex) // 2, (sy + ey) // 2
            mid_piece = self.board[mid_x, mid_y]
            if mid_piece.lower() in ["b", "r"] and mid_piece.lower() != piece.lower():
                return True
        
        return False

    def move_piece(self, start, end):
        if self.is_valid_move(start, end):
            sx, sy = start
            ex, ey = end
            piece = self.board[sx, sy]

            # Move piece
            self.board[ex, ey] = piece
            self.board[sx, sy] = " "

            # Remove captured piece if it was a jump
            if abs(ex - sx) == 2:
                mid_x, mid_y = (sx + ex) // 2, (sy + ey) // 2
                self.board[mid_x, mid_y] = " "

            # Promote to king if reaching opponent's back row
            if (ex == 7 and piece == "b") or (ex == 0 and piece == "r"):
                self.board[ex, ey] = piece.upper()

            # Switch turn
            self.current_player = "red" if self.current_player == "black" else "black"
        else:
            print("Invalid move!")

    def play(self):
        moves = [((2, 1), (3, 2)), ((5, 2), (4, 3)), ((3, 2), (5, 4)), ((5, 4), (3, 2))]  # Example moves
        for start, end in moves:
            self.print_board()
            print(f"{self.current_player}'s turn: Moving from {start} to {end}")
            self.move_piece(start, end)

if __name__ == "__main__":
    game = Checkers()
    game.play()
