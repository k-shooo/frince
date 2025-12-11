import tkinter as tk
from tkinter import messagebox
import random
import copy

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        root.title("Tic-Tac-Toe (X O X)")

        self.mode = tk.StringVar(value="PvP")
        self.human_symbol = tk.StringVar(value="X")
        self.scores = {"X": 0, "O": 0, "Draws": 0}

        self.create_widgets()
        self.new_game()

    def create_widgets(self):
        top = tk.Frame(self.root)
        top.pack(padx=10, pady=8)

        tk.Label(top, text="Mode:").grid(row=0, column=0, sticky="w")
        mode_menu = tk.OptionMenu(top, self.mode, "PvP", "PvC", command=self.on_mode_change)
        mode_menu.grid(row=0, column=1, sticky="w")

        tk.Label(top, text="Human:").grid(row=0, column=2, sticky="w", padx=(10, 0))
        human_menu = tk.OptionMenu(top, self.human_symbol, "X", "O")
        human_menu.grid(row=0, column=3, sticky="w")

        self.status_label = tk.Label(self.root, text="Welcome to Tic-Tac-Toe!", font=("Segoe UI", 12))
        self.status_label.pack(pady=(4, 8))

        board_frame = tk.Frame(self.root)
        board_frame.pack(padx=10, pady=6)

        self.buttons = [[None]*3 for _ in range(3)]
        for r in range(3):
            for c in range(3):
                b = tk.Button(board_frame, text="", width=6, height=3,
                              font=("Segoe UI", 20, "bold"),
                              command=lambda rr=r, cc=c: self.on_click(rr, cc))
                b.grid(row=r, column=c, padx=4, pady=4)
                self.buttons[r][c] = b

        ctrl = tk.Frame(self.root)
        ctrl.pack(pady=(8,10))

        self.restart_btn = tk.Button(ctrl, text="Restart Game", command=self.new_game)
        self.restart_btn.pack(side="left", padx=6)

        reset_scores_btn = tk.Button(ctrl, text="Reset Scores", command=self.reset_scores)
        reset_scores_btn.pack(side="left", padx=6)

        info_btn = tk.Button(ctrl, text="About", command=self.show_about)
        info_btn.pack(side="left", padx=6)

        self.score_label = tk.Label(self.root, text=self.score_text(), font=("Segoe UI", 10))
        self.score_label.pack(pady=(6, 12))

    def on_mode_change(self, *_):
        if self.mode.get() == "PvP":
            pass
        self.new_game()

    def show_about(self):
        messagebox.showinfo("About", "Tic-Tac-Toe (X O X)\n\nPlay 2-player locally or vs an unbeatable AI.\nMade with Tkinter.")

    def score_text(self):
        return f"Scores — X: {self.scores['X']}   O: {self.scores['O']}   Draws: {self.scores['Draws']}"

    def reset_scores(self):
        self.scores = {"X":0, "O":0, "Draws":0}
        self.score_label.config(text=self.score_text())
        self.new_game()

    def new_game(self):
        self.board = [['']*3 for _ in range(3)]
        self.game_over = False
        self.turn = "X"
        for r in range(3):
            for c in range(3):
                btn = self.buttons[r][c]
                btn.config(text="", state="normal", bg="SystemButtonFace")
        self.status_label.config(text=f"Turn: {self.turn}")
        if self.mode.get() == "PvC" and self.human_symbol.get() == "O":
            self.root.after(200, self.ai_move)

    def on_click(self, r, c):
        if self.game_over:
            return
        if self.board[r][c] != "":
            return
        if self.mode.get() == "PvC":
            human = self.human_symbol.get()
            if self.turn != human:
                return

        self.place_mark(r, c, self.turn)
        winner, line = self.check_winner(self.board)
        if winner:
            self.finish_game(winner, line)
            return
        if self.is_board_full(self.board):
            self.finish_game(None, None)  
            return
        self.turn = "O" if self.turn == "X" else "X"
        self.status_label.config(text=f"Turn: {self.turn}")
        if not self.game_over and self.mode.get() == "PvC" and self.turn != self.human_symbol.get():
            self.root.after(200, self.ai_move)

    def place_mark(self, r, c, mark):
        self.board[r][c] = mark
        btn = self.buttons[r][c]
        btn.config(text=mark)

    def finish_game(self, winner, line):
        self.game_over = True
        if winner is None:
            self.status_label.config(text="Draw!")
            self.scores["Draws"] += 1
        else:
            self.status_label.config(text=f"{winner} wins!")
            self.scores[winner] += 1
            if line:
                for (r,c) in line:
                    self.buttons[r][c].config(bg="#90EE90")
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(state="disabled")
        self.score_label.config(text=self.score_text())

    def ai_move(self):
        if self.game_over:
            return
        ai_mark = "O" if self.human_symbol.get() == "X" else "X"
        best_move = self.find_best_move(self.board, ai_mark)
        if best_move:
            r,c = best_move
            self.place_mark(r, c, ai_mark)
        winner, line = self.check_winner(self.board)
        if winner:
            self.finish_game(winner, line)
            return
        if self.is_board_full(self.board):
            self.finish_game(None, None)
            return

        self.turn = "O" if ai_mark == "X" else "X"
        self.status_label.config(text=f"Turn: {self.turn}")

    def is_board_full(self, board):
        return all(board[r][c] != "" for r in range(3) for c in range(3))

    def check_winner(self, board):
        lines = []
        for r in range(3):
            lines.append([(r,0),(r,1),(r,2)])
        for c in range(3):
            lines.append([(0,c),(1,c),(2,c)])
        lines.append([(0,0),(1,1),(2,2)])
        lines.append([(0,2),(1,1),(2,0)])

        for line in lines:
            vals = [board[r][c] for (r,c) in line]
            if vals[0] != "" and vals.count(vals[0]) == 3:
                return vals[0], line
        return None, None

    def find_best_move(self, board, ai_mark):
        human_mark = "O" if ai_mark == "X" else "X"

        def minimax(b, player):
            winner, _ = self.check_winner(b)
            if winner == ai_mark:
                return 10
            elif winner == human_mark:
                return -10
            elif self.is_board_full(b):
                return 0

            moves = []
            for r in range(3):
                for c in range(3):
                    if b[r][c] == "":
                        nb = copy.deepcopy(b)
                        nb[r][c] = player
                        score = minimax(nb, "O" if player == "X" else "X")
                        moves.append(((r,c), score))
            if player == ai_mark:
                best = max(moves, key=lambda x: x[1])
                return best[1]
            else:
                best = min(moves, key=lambda x: x[1])
                return best[1]

        best_score = -9999
        best_move = None
        for r in range(3):
            for c in range(3):
                if board[r][c] == "":
                    nb = copy.deepcopy(board)
                    nb[r][c] = ai_mark
                    score = minimax(nb, human_mark)
                    if score > best_score or (score == best_score and random.random() > 0.5):
                        best_score = score
                        best_move = (r, c)
        return best_move

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.resizable(False, False)
    root.mainloop()