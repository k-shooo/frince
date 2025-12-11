import tkinter as tk

PIECE_SYMBOLS = {
    "r": "♜", "n": "♞", "b": "♝", "q": "♛", "k": "♚", "p": "♟",
    "R": "♖", "N": "♘", "B": "♗", "Q": "♕", "K": "♔", "P": "♙"
}

START_BOARD = [
    list("rnbqkbnr"),
    list("pppppppp"),
    list("        "),
    list("        "),
    list("        "),
    list("        "),
    list("PPPPPPPP"),
    list("RNBQKBNR")
]

CELL_SIZE = 70

class ChessGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game - Tkinter")
        self.canvas = tk.Canvas(root, width=8*CELL_SIZE, height=8*CELL_SIZE)
        self.canvas.pack()

        self.board = [row[:] for row in START_BOARD]
        self.turn = "white"
        self.selected = None
        self.possible_moves = []

        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(8):
            for c in range(8):
                color = "#EEEED2" if (r+c) % 2 == 0 else "#769656"
                self.canvas.create_rectangle(
                    c*CELL_SIZE, r*CELL_SIZE, (c+1)*CELL_SIZE, (r+1)*CELL_SIZE,
                    fill=color, outline=color
                )

        if self.selected:
            r, c = self.selected
            self.canvas.create_rectangle(
                c*CELL_SIZE, r*CELL_SIZE, (c+1)*CELL_SIZE, (r+1)*CELL_SIZE,
                outline="yellow", width=3
            )

        for r, c in self.possible_moves:
            self.canvas.create_oval(
                c*CELL_SIZE+CELL_SIZE/3,
                r*CELL_SIZE+CELL_SIZE/3,
                c*CELL_SIZE+2*CELL_SIZE/3,
                r*CELL_SIZE+2*CELL_SIZE/3,
                fill="yellow"
            )

        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece != " ":
                    self.canvas.create_text(
                        c*CELL_SIZE+CELL_SIZE/2,
                        r*CELL_SIZE+CELL_SIZE/2,
                        text=PIECE_SYMBOLS[piece],
                        font=("Arial", 40)
                    )

    def on_click(self, event):
        r = event.y // CELL_SIZE
        c = event.x // CELL_SIZE

        if self.selected:
            if (r, c) in self.possible_moves:
                self.move_piece(self.selected, (r, c))
                self.turn = "black" if self.turn == "white" else "white"
            self.selected = None
            self.possible_moves = []
            self.draw_board()
            return

        piece = self.board[r][c]
        if piece == " ":
            return

        if self.turn == "white" and piece.islower():
            return
        if self.turn == "black" and piece.isupper():
            return

        self.selected = (r, c)
        self.possible_moves = self.get_moves(r, c)
        self.draw_board()

    def move_piece(self, start, end):
        sr, sc = start
        er, ec = end
        self.board[er][ec] = self.board[sr][sc]
        self.board[sr][sc] = " "

    def get_moves(self, r, c):
        piece = self.board[r][c]
        moves = []

        if piece.lower() == "p":
            moves = self.pawn_moves(r, c)
        elif piece.lower() == "r":
            moves = self.straight_moves(r, c)
        elif piece.lower() == "n":
            moves = self.knight_moves(r, c)
        elif piece.lower() == "b":
            moves = self.diagonal_moves(r, c)
        elif piece.lower() == "q":
            moves = self.straight_moves(r, c) + self.diagonal_moves(r, c)
        elif piece.lower() == "k":
            moves = self.king_moves(r, c)

        filtered = []
        for rr, cc in moves:
            if piece.isupper() and (self.board[rr][cc].isupper()):
                continue
            if piece.islower() and (self.board[rr][cc].islower()):
                continue
            filtered.append((rr, cc))
        return filtered

    def pawn_moves(self, r, c):
        moves = []
        piece = self.board[r][c]
        direction = -1 if piece.isupper() else 1

        if self.in_bounds(r+direction, c) and self.board[r+direction][c] == " ":
            moves.append((r+direction, c))

        for dc in [-1, 1]:
            if self.in_bounds(r+direction, c+dc):
                target = self.board[r+direction][c+dc]
                if target != " " and target.isupper() != piece.isupper():
                    moves.append((r+direction, c+dc))

        return moves

    def straight_moves(self, r, c):
        moves = []
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        for dr, dc in directions:
            moves.extend(self.ray_moves(r, c, dr, dc))
        return moves

    def diagonal_moves(self, r, c):
        moves = []
        directions = [(1,1), (1,-1), (-1,1), (-1,-1)]
        for dr, dc in directions:
            moves.extend(self.ray_moves(r, c, dr, dc))
        return moves

    def ray_moves(self, r, c, dr, dc):
        moves = []
        piece = self.board[r][c]
        rr, cc = r+dr, c+dc
        while self.in_bounds(rr, cc):
            if self.board[rr][cc] == " ":
                moves.append((rr, cc))
            else:
                if self.board[rr][cc].isupper() != piece.isupper():
                    moves.append((rr, cc))
                break
            rr += dr
            cc += dc
        return moves

    def knight_moves(self, r, c):
        moves = []
        steps = [(2,1), (2,-1), (-2,1), (-2,-1),
                 (1,2), (1,-2), (-1,2), (-1,-2)]
        for dr, dc in steps:
            if self.in_bounds(r+dr, c+dc):
                moves.append((r+dr, c+dc))
        return moves

    def king_moves(self, r, c):
        moves = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                if self.in_bounds(r+dr, c+dc):
                    moves.append((r+dr, c+dc))
        return moves

    def in_bounds(self, r, c):
        return 0 <= r < 8 and 0 <= c < 8

root = tk.Tk()
game = ChessGame(root)
root.mainloop()
