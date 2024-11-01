import random
import tkinter as tk
from tkinter import messagebox
import math

def flip():
    return random.choice(['player', 'com'])

w_player = flip()
game_board = [' ' for _ in range(9)]

def empty_spots(board):
    return [i for i, spot in enumerate(board) if spot == ' ']

def valid_move(board, x):
    return board[x] == ' '

def move(board, x, player):
    if valid_move(board, x):
        board[x] = player
        return True
    return False

def check_win(board, player):
    win_config = [
        [board[0], board[1], board[2]],
        [board[3], board[4], board[5]],
        [board[6], board[7], board[8]],
        [board[0], board[3], board[6]],
        [board[1], board[4], board[7]],
        [board[2], board[5], board[8]],
        [board[0], board[4], board[8]],
        [board[2], board[4], board[6]],
    ]
    return [player, player, player] in win_config

def evaluate(board):
    if check_win(board, 'X'):
        return 1
    elif check_win(board, 'O'):
        return -1
    return 0

def game_over(board):
    return check_win(board, 'X') or check_win(board, 'O') or len(empty_spots(board)) == 0

def minimax(board, depth, maxPlayer):
    if depth == 0 or game_over(board):
        return -1, evaluate(board)
    
    if maxPlayer:
        value = -math.inf
        pos = -1
        for point in empty_spots(board):
            board[point] = 'X'
            _, score = minimax(board, depth - 1, False)
            board[point] = ' '
            if score > value:
                value = score
                pos = point
        return pos, value
    else:
        value = math.inf
        pos = -1
        for point in empty_spots(board):
            board[point] = 'O'
            _, score = minimax(board, depth - 1, True)
            board[point] = ' '
            if score < value:
                value = score
                pos = point
        return pos, value

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("틱택토")
        self.buttons = [tk.Button(self.root, text=' ', font='Arial 20', width=5, height=2, command=lambda i=i: self.on_click(i)) for i in range(9)]
        for i, button in enumerate(self.buttons):
            button.grid(row=i//3, column=i%3)
        self.player = 'X' if w_player == 'player' else 'O'
        self.com = 'O' if self.player == 'X' else 'X'
        self.turn = 'com' if self.com == 'X' else 'player'
        self.update_status()
        if self.turn == 'com':
            self.com_move()

    def update_status(self):
        if game_over(game_board):
            winner = 'X' if check_win(game_board, 'X') else 'O' if check_win(game_board, 'O') else '무승부'
            if winner != '무승부':
                messagebox.showinfo("게임 종료", f"{self.turn} 패배!")
            else:
                messagebox.showinfo("게임 종료", "무승부!")
            self.root.quit()
        else:
            status = "player" if self.turn == 'player' else "COM"
            self.root.title(f"틱택토 - {status}")
            

    def on_click(self, index):
        if self.turn == 'player' and valid_move(game_board, index):
            move(game_board, index, self.player)
            self.buttons[index].config(text=self.player)
            self.turn = 'com'
            self.update_status()
            self.com_move()

    def com_move(self):
        if not game_over(game_board):
            self.root.after(500, self.make_com_move)


    def make_com_move(self):
        index, _ = minimax(game_board, 9, self.com == 'X')
        move(game_board, index, self.com)
        self.buttons[index].config(text=self.com)
        self.turn = 'player'
        self.update_status()

root = tk.Tk()
app = TicTacToe(root)
root.mainloop()

