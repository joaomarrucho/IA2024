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
        if all(self.board[0][i] != ' ' for i in range(7)):
            return 'Draw'
        return None
    
    def is_board_full(self):
        return all(self.board[0][i] != ' ' for i in range(7))  # Verifica se o topo de cada coluna está preenchido


class Connect4AI:
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.max_depth = 4  # Profundidade máxima da busca

    def get_next_move(self, board):
        if self.algorithm == "A*":
            return self.search(board)
        elif self.algorithm == "MCTS":
            return self.mcts(board)

    def evaluate_segment(self, segment):
        count_x = segment.count('X')
        count_o = segment.count('O')

        if count_x == 4:
            return -512
        elif count_o == 4:
            return 512
        elif count_o == 3 and count_x == 0:
            return 50
        elif count_o == 2 and count_x == 0:
            return 10
        elif count_o == 1 and count_x == 0:
            return 1
        elif count_x == 1 and count_o == 0:
            return -1
        elif count_x == 2 and count_o == 0:
            return -10
        elif count_x == 3 and count_o == 0:
            return -50
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

    def search(self, board):
        return self._search(board, 0, -math.inf, math.inf, True)

    def _search(self, board, depth, alpha, beta, maximizing_player):
        winner = Connect4().check_winner()
        if winner == 'X':
            return 512 - depth
        elif winner == 'O':
            return -512 + depth
        elif winner == 'Draw':
            return 0

        if depth == self.max_depth:
            return self.evaluate_board(board)

        if maximizing_player:
            max_eval = -math.inf
            max_col = None  # Variável para armazenar a coluna com a maior avaliação
            for col in range(7):
                if self.is_valid_move(board, col):
                    new_board = self.make_move(board, col, 'O')
                    eval = self._search(new_board, depth + 1, alpha, beta, False)
                    if eval > max_eval:  # Se a nova avaliação for maior que a atual máxima
                        max_eval = eval
                        max_col = col
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            if depth == 0:  # Se for a primeira chamada da função (nível de profundidade 0)
                return max_col  # Retorna a coluna escolhida pela IA
            return max_eval
        else:
            min_eval = math.inf
            for col in range(7):
                if self.is_valid_move(board, col):
                    new_board = self.make_move(board, col, 'X')
                    eval = self._search(new_board, depth + 1, alpha, beta, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
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
    
    def mcts(self, board):
        root = Node(board, 'O', self.algorithm)  
        for _ in range(1000):  
            node = root
            while not node.is_terminal():
                if not node.is_fully_expanded():
                    node = node.expand()
                    break
                else:
                    node = node.select_child()
            winner = node.simulate()
            node.backpropagate(winner)
        
        # Depois de realizar a simulação, precisamos determinar qual é o melhor movimento
        # O melhor movimento é aquele que leva ao filho com a maior quantidade de vitórias
        best_child = max(root.children, key=lambda x: x.wins)
        # Para determinar a coluna desse movimento, precisamos encontrar o índice do filho na lista de filhos da raiz
        column = root.children.index(best_child)
        return column

        
class Node:
    def __init__(self, board, player, algorithm, parent=None):
        self.board = board
        self.player = player
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.algorithm = algorithm

    def is_fully_expanded(self):
        return len(self.children) == 7  

    def select_child(self):
        ucb_values = []
        for child in self.children:
            if child.visits == 0:
                ucb_values.append(float('inf'))  # Assign a high value to UCB if visits is zero to prioritize unexplored nodes
            else:
                ucb = child.wins / child.visits + math.sqrt(2 * math.log(self.visits) / child.visits)
                ucb_values.append(ucb)
        max_ucb_index = ucb_values.index(max(ucb_values))
        return self.children[max_ucb_index] if self.children else None



    def expand(self):
        for column in range(7):
            if self.board[0][column] == ' ':
                new_board = Connect4AI(self.algorithm).make_move(self.board, column, self.player)  # Corrigido
                new_player = 'X' if self.player == 'O' else 'O'
                print(f"Expanding to column {column}")
                print("New Board:")
                for row in new_board:
                    print(row)
                self.children.append(Node(new_board, new_player, self))
        return random.choice(self.children)

    def simulate(self):
        sim_board = self.board
        sim_player = self.player
        while Connect4().check_winner() is None and not Connect4().is_board_full():  # Correção aqui
            available_columns = [col for col in range(7) if sim_board[0][col] == ' ']  # Correção aqui
            if available_columns:
                column = random.choice(available_columns)  # Correção aqui
                sim_board = Connect4AI(self.algorithm).make_move(sim_board, column, sim_player)  
                sim_player = 'X' if sim_player == 'O' else 'O'
            else:
                break  # Nenhuma coluna disponível, encerra a simulação
        winner = Connect4().check_winner()
        if winner == 'O':
            return 1
        elif winner == 'X':
            return -1
        else:
            return 0

    def backpropagate(self, result):
        self.visits += 1
        if self.player == 'O':
            self.wins += result
        else:
            self.wins -= result
        if self.parent:
            self.parent.backpropagate(result)

    def is_terminal(self):
        return Connect4().check_winner() is not None or all(self.board[0][i] != ' ' for i in range(7))

    def best_child(self):
        if self.visits == 0:
            return random.choice(self.children)
        else:
            ucb_values = []
            for child in self.children:
                if child.visits == 0:
                    ucb_values.append(float('inf'))  # Atribuir um valor infinito para priorizar nós não explorados
                else:
                    ucb = child.wins / child.visits + math.sqrt(2 * math.log(self.visits) / child.visits)
                    ucb_values.append(ucb)
            return self.children[ucb_values.index(max(ucb_values))] if self.children else None


            



class Connect4GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Connect 4")
        self.mode = None
        self.algorithm = None
        self.canvas = None
        self.current_player_label = None
        self.score_label_player = None
        self.score_label_ai = None
        self.game = None
        self.ai = None
        self.reset_button = None
        self.draw_menu = True
        self.active_game = False  

    def draw_mode_selection(self):
        if self.draw_menu:
            for widget in self.root.winfo_children():
                widget.destroy()
            self.root.geometry("300x90")
            label = tk.Label(self.root, text="Selecione o modo de jogo:")
            label.pack()
            button_human_vs_human = tk.Button(self.root, text="Humano vs Humano", command=lambda: self.start_game("Humano vs Humano"))
            button_human_vs_human.pack()
            button_human_vs_ai = tk.Button(self.root, text="Humano vs IA", command=self.draw_algorithm_selection)
            button_human_vs_ai.pack()
            self.draw_menu = False

    def draw_algorithm_selection(self):
        self.mode = "Humano vs IA"
        self.root.geometry("300x190")
        for widget in self.root.winfo_children():
            widget.destroy()
        label = tk.Label(self.root, text="Selecione o algoritmo para a IA:")
        label.pack()
        button_astar = tk.Button(self.root, text="A*", command=lambda: self.start_game("A*"))
        button_astar.pack()
        button_mcts = tk.Button(self.root, text="MCTS", command=lambda: self.start_game("MCTS"))
        button_mcts.pack()

    def start_game(self, algorithm):
        self.algorithm = algorithm
        self.root.geometry("800x850")
        self.canvas = tk.Canvas(self.root, width=700, height=600)
        self.canvas.pack()
        self.game = Connect4()
        self.ai = Connect4AI(self.algorithm) if self.mode == "Humano vs IA" else None
        self.draw_board()
        self.canvas.bind("<Button-1>", self.click_event)
        self.current_player_label = tk.Label(self.root, text=f'Jogador atual: {self.game.current_player}')
        self.current_player_label.pack()
        if self.algorithm == "A*":
            self.score_label_player = tk.Label(self.root, text=f'Total score jogador: {self.ai.evaluate_board(self.game.board)}')
            self.score_label_player.pack()
            self.score_label_ai = tk.Label(self.root, text=f'Total score IA: {self.ai.evaluate_board(self.game.board)}')
            self.score_label_ai.pack()
        if self.mode == "Humano vs IA" and self.game.current_player == 'O' and self.algorithm == "A*":
            self.ai_make_move()
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_game)
        self.reset_button.pack()
        self.active_game = True


    def reset_game(self):
        self.canvas.destroy()
        self.current_player_label.destroy()
        if self.score_label_player:
            self.score_label_player.destroy()
        if self.score_label_ai:
            self.score_label_ai.destroy()
        self.reset_button.destroy()
        self.draw_menu = True
        self.draw_mode_selection()

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(6):
            for col in range(7):
                x0 = col * 100
                y0 = row * 100
                x1 = x0 + 100
                y1 = y0 + 100
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="blue")
                if self.game.board[row][col] == 'X':
                    self.canvas.create_oval(x0+10, y0+10, x1-10, y1-10, fill="red")
                elif self.game.board[row][col] == 'O':
                    self.canvas.create_oval(x0+10, y0+10, x1-10, y1-10, fill="yellow")

    def click_event(self, event):
        if self.active_game:
            if not self.game.is_board_full():
                column = event.x // 100
                if self.game.make_move(column):
                    self.draw_board()
                    winner = self.game.check_winner()
                    if winner:
                        self.show_winner(winner)
                    elif self.game.is_board_full():
                        messagebox.showinfo("Resultado", "O jogo empatou!")
                        self.active_game = False
                    else:
                        if self.mode == "Humano vs IA" and self.game.current_player == 'O':
                            self.ai_make_move()  
                        else:
                            self.current_player_label.config(text=f'Jogador atual: {self.game.current_player}')
                        if self.algorithm == "A*":
                            self.score_label_player.config(text=f'Total score jogador: {self.ai.evaluate_board(self.game.board)}')
            else:
                messagebox.showinfo("Resultado", "O jogo empatou!")
                self.active_game = False

    def ai_make_move(self):
        if self.active_game:
            if self.mode == "Humano vs IA" and self.algorithm == "A*":
                column = self.ai.get_next_move(self.game.board)
                if self.game.make_move(column):
                    self.draw_board()
                    winner = self.game.check_winner()
                    if winner:
                        self.show_winner(winner)
                    elif self.game.is_board_full():
                        messagebox.showinfo("Resultado", "O jogo empatou!")
                        self.active_game = False
                    else:
                        self.current_player_label.config(text=f'Jogador atual: {self.game.current_player}')
                        self.score_label_ai.config(text=f'Total score IA: {self.ai.evaluate_board(self.game.board)}')
            elif self.mode == "Humano vs IA" and self.algorithm == "MCTS":
                column = self.ai.get_next_move(self.game.board)
                if self.game.make_move(column):
                    self.draw_board()
                    winner = self.game.check_winner()
                    if winner:
                        self.show_winner(winner)
                    elif self.game.is_board_full():
                        messagebox.showinfo("Resultado", "O jogo empatou!")
                        self.active_game = False
                    else:
                        self.current_player_label.config(text=f'Jogador atual: {self.game.current_player}')

    def show_winner(self, winner):
        self.draw_board()
        if winner != 'Draw':
            messagebox.showinfo("Resultado", f'O jogador {winner} ganhou!')
        else:
            messagebox.showinfo("Resultado", "O jogo empatou!")
        self.active_game = False

    def start(self):
        self.draw_mode_selection()
        self.root.mainloop()

if __name__ == "__main__":
    game = Connect4GUI()
    game.start()
