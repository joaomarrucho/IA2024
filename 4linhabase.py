class Connect4:
    def __init__(self):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]  # Tabuleiro 6x7 vazio
        self.current_player = 'X'  # Começa com jogador X

    def print_board(self):
        for row in self.board:
            print('|'.join(row))
        print('-------------')

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

# Exemplo de uso:
game = Connect4()

while True:
    game.print_board()
    column = int(input(f'Player {game.current_player}, escolha uma coluna (0-6): '))
    if game.make_move(column):
        winner = game.check_winner()
        if winner:
            game.print_board()
            print(f'O jogador {winner} ganhou!')
            break
        elif game.is_board_full():
            game.print_board()
            print('O jogo empatou!')
            break
    else:
        print('Movimento inválido. Tente novamente.')