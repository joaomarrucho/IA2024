import tkinter as tk
from tkinter import messagebox
import math
import random

class Connect4:
    def __init__(self):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]  # Tabuleiro 6x7 vazio
        self.current_player = 'X'  # Começa com jogador X

    def is_valid_move(self, column):
        return 0 <= column < 7 and self.board[0][column] == ' '  # Verifica se a coluna está dentro dos limites e não está cheia

    def make_move(self, column):
        if self.is_valid_move(column):
            for row in range(5, -1, -1):  # Começa da parte inferior da coluna
                if self.board[row][column] == ' ':
                    self.board[row][column] = self.current_player
                    break
            self.current_player = 'O' if self.current_player == 'X' else 'X'  # Alterna para o próximo jogador
            return True
        return False

    def check_winner(self):
        for row in range(6):
            for col in range(7):
                if self.board[row][col] != ' ':
                    # Verifica horizontal
                    if col + 3 < 7 and self.board[row][col] == self.board[row][col+1] == self.board[row][col+2] == self.board[row][col+3]:
                        return self.board[row][col]
                    # Verifica vertical
                    if row + 3 < 6 and self.board[row][col] == self.board[row+1][col] == self.board[row+2][col] == self.board[row+3][col]:
                        return self.board[row][col]
                    # Verifica diagonal \
                    if row + 3 < 6 and col + 3 < 7 and self.board[row][col] == self.board[row+1][col+1] == self.board[row+2][col+2] == self.board[row+3][col+3]:
                        return self.board[row][col]
                    # Verifica diagonal /
                    if row + 3 < 6 and col - 3 >= 0 and self.board[row][col] == self.board[row+1][col-1] == self.board[row+2][col-2] == self.board[row+3][col-3]:
                        return self.board[row][col]
        return None

    def is_board_full(self):
        return all(self.board[0][i] != ' ' for i in range(7))  # Verifica se o topo de cada coluna está preenchido

class Connect4AI:
    def __init__(self):
        self.max_depth = 4  # Profundidade máxima da busca

    def get_next_move(self, board):
        return self.a_star(board)

    def evaluate_segment(self, segment):
        count_x = segment.count('X')
        count_o = segment.count('O')

        if count_x == 4:
            return 512
        elif count_o == 4:
            return -512
        elif count_o == 3 and count_x == 0:
            return -50
        elif count_o == 2 and count_x == 0:
            return -10
        elif count_o == 1 and count_x == 0:
            return -1
        elif count_x == 1 and count_o == 0:
            return 1
        elif count_x == 2 and count_o == 0:
            return 10
        elif count_x == 3 and count_o == 0:
            return 50
        else:
            return 0

    def evaluate_board(self, board):
        total_score = 0
        # Check horizontal segments
        for row in range(6):
            for col in range(4):
                segment = board[row][col:col+4]
                total_score += self.evaluate_segment(segment)
        # Check vertical segments
        for col in range(7):
            for row in range(3):
                segment = [board[row+i][col] for i in range(4)]
                total_score += self.evaluate_segment(segment)
        # Check diagonal segments (top-left to bottom-right)
        for row in range(3):
            for col in range(4):
                segment = [board[row+i][col+i] for i in range(4)]
                total_score += self.evaluate_segment(segment)
        # Check diagonal segments (top-right to bottom-left)
        for row in range(3):
            for col in range(3, 7):
                segment = [board[row+i][col-i] for i in range(4)]
                total_score += self.evaluate_segment(segment)

        return total_score

    def a_star(self, board):
        valid_moves = [col for col in range(7) if board[0][col] == ' ']  # Obtém todas as colunas não cheias
        best_move = None
        best_score = -math.inf
        for move in valid_moves:
            new_board = self.make_move(board, move, 'X')
            score = self.minimax(new_board, 0, False)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def minimax(self, board, depth, is_maximizing):
        winner = self.check_winner(board)
        if winner == 'X':
            return 512 - depth
        elif winner == 'O':
            return -512 + depth
        elif winner == 'Draw':
            return 0
        if depth == self.max_depth:
            return self.evaluate_board(board)
        if is_maximizing:
            max_eval = -math.inf
            for col in range(7):
                if self.is_valid_move(board, col):
                    new_board = self.make_move(board, col, 'X')
                    eval = self.minimax(new_board, depth + 1, False)
                    max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = math.inf
            for col in range(7):
                if self.is_valid_move(board, col):
                    new_board = self.make_move(board, col, 'O')
                    eval = self.minimax(new_board, depth + 1, True)
                    min_eval = min(min_eval, eval)
            return min_eval

    def is_valid_move(self, board, column):
        return board[0][column] == ' '

    def make_move(self, board, column, player):
        new_board = [row[:] for row in board]
        for row in range(5, -1, -1):
            if new_board[row][column] == ' ':
                new_board[row][column] = player
                break
        return new_board

    def check_winner(self, board):
        # Check horizontal
        for row in range(6):
            for col in range(4):
                if board[row][col] != ' ' and board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3]:
                    return board[row][col]
        # Check vertical
        for col in range(7):
            for row in range(3):
                if board[row][col] != ' ' and board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col]:
                    return board[row][col]
        # Check diagonal \
        for row in range(3):
            for col in range(4):
                if board[row][col] != ' ' and board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3]:
                    return board[row][col]
        # Check diagonal /
        for row in range(3):
            for col in range(3, 7):
                if board[row][col] != ' ' and board[row][col] == board[row+1][col-1] == board[row+2][col-2] == board[row+3][col-3]:
                    return board[row][col]
        # Check for draw
        if all(board[0][i] != ' ' for i in range(7)):
            return 'Draw'
        return None

class Connect4GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Connect 4")
        self.mode = None
        self.algorithm = None
        self.canvas = None
        self.current_player_label = None
        self.game = None
        self.ai = None
        self.draw_mode_selection()

    def draw_mode_selection(self):
        self.root.geometry("300x200")
        label = tk.Label(self.root, text="Selecione o modo de jogo:")
        label.pack()
        button_human_vs_human = tk.Button(self.root, text="Humano vs Humano", command=lambda: self.start_game("Humano vs Humano", None))
        button_human_vs_human.pack()
        button_human_vs_astar = tk.Button(self.root, text="Humano vs A* AI", command=lambda: self.start_game("Humano vs IA", "A*"))
        button_human_vs_astar.pack()
        button_human_vs_mcts = tk.Button(self.root, text="Humano vs MCTS AI", command=lambda: self.start_game("Humano vs IA", "MCTS"))
        button_human_vs_mcts.pack()

    def start_game(self, mode, algorithm):
        self.mode = mode
        self.algorithm = algorithm
        self.root.geometry("800x800")
        self.canvas = tk.Canvas(self.root, width=700, height=600)
        self.canvas.pack()
        self.game = Connect4()
        self.ai = Connect4AI() if self.mode == "Humano vs IA" else None
        self.draw_board()
        self.canvas.bind("<Button-1>", self.click_event)
        self.current_player_label = tk.Label(self.root, text=f'Jogador atual: {self.game.current_player}')
        self.current_player_label.pack()
        if self.mode == "Humano vs IA" and self.game.current_player == 'X':
            self.ai_make_move()

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(6):
            for col in range(7):
                x1, y1 = col * 100, row * 100
                x2, y2 = x1 + 100, y1 + 100
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue")
                if self.game.board[row][col] == 'X':
                    self.canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill="red")
                elif self.game.board[row][col] == 'O':
                    self.canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill="yellow")
        self.root.update()

    def click_event(self, event):
        if self.mode == "Humano vs Humano" or (self.mode == "Humano vs IA" and self.game.current_player == 'X'):
            column = event.x // 100
            if self.game.make_move(column):
                self.draw_board()
                winner = self.game.check_winner()
                if winner:
                    if winner == 'Draw':
                        messagebox.showinfo("Resultado", "Empate!")
                    else:
                        messagebox.showinfo("Resultado", f"O jogador {winner} venceu!")
                    self.root.destroy()
                    return
                self.current_player_label.config(text=f'Jogador atual: {self.game.current_player}')
                if self.mode == "Humano vs IA":
                    self.ai_make_move()

    def ai_make_move(self):
        if self.algorithm == "A*":
            column = self.ai.get_next_move(self.game.board)
        else:
            # Implementação para o MCTS
            pass
        if self.game.make_move(column):
            self.draw_board()
            winner = self.game.check_winner()
            if winner:
                if winner == 'Draw':
                    messagebox.showinfo("Resultado", "Empate!")
                else:
                    messagebox.showinfo("Resultado", f"O jogador {winner} venceu!")
                self.root.destroy()
                return
            self.current_player_label.config(text=f'Jogador atual: {self.game.current_player}')

if __name__ == "__main__":
    game = Connect4GUI()
    game.root.mainloop()
