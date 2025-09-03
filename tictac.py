import tkinter as tk
from tkinter import messagebox
import random

current_player = "X"
board = [""] * 9
game_mode = None

def check_winner():
    win_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for a, b, c in win_combinations:
        if board[a] == board[b] == board[c] != "":
            return board[a]
    return None

def minimax(board, depth, is_maximizing):
    winner = check_winner()
    if winner == "X":
        return -1
    elif winner == "O":
        return 1
    elif "" not in board:
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, depth + 1, False)
                board[i] = ""
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax(board, depth + 1, True)
                board[i] = ""
                best_score = min(score, best_score)
        return best_score

def ai_move():
    best_score = -float("inf")
    move = None
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, 0, False)
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i
    if move is not None:
        board[move] = "O"
        buttons[move].config(text="O", state="disabled")
        check_game_over()

def button_click(index):
    global current_player
    if board[index] == "":
        board[index] = current_player
        buttons[index].config(text=current_player, state="disabled")
        if check_game_over():
            return
        current_player = "O" if current_player == "X" else "X"
        if game_mode == "ai" and current_player == "O":
            ai_move()
            current_player = "X"
            check_game_over()

def check_game_over():
    winner = check_winner()
    if winner:
        messagebox.showinfo("Game Over", f"Player {winner} wins!")
        reset_game()
        return True
    elif "" not in board:
        messagebox.showinfo("Game Over", "It's a draw!")
        reset_game()
        return True
    return False

def reset_game():
    global current_player, board
    current_player = "X"
    board = [""] * 9
    for btn in buttons:
        btn.config(text="", state="normal")

def set_mode(mode):
    global game_mode
    game_mode = mode
    mode_frame.pack_forget()
    game_frame.pack()

root = tk.Tk()
root.title("Tic-Tac-Toe")

mode_frame = tk.Frame(root)
mode_frame.pack()

tk.Label(mode_frame, text="Choose Game Mode", font=("Arial", 14)).pack(pady=10)
tk.Button(mode_frame, text="Human vs Human", font=("Arial", 12),
          command=lambda: set_mode("human")).pack(pady=5)
tk.Button(mode_frame, text="Human vs AI", font=("Arial", 12),
          command=lambda: set_mode("ai")).pack(pady=5)

game_frame = tk.Frame(root)
buttons = []
for i in range(9):
    btn = tk.Button(game_frame, text="", font=("Arial", 24),
                    width=5, height=2, command=lambda i=i: button_click(i))
    btn.grid(row=i // 3, column=i % 3)
    buttons.append(btn)

root.mainloop()