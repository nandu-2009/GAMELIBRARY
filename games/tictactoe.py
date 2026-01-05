import tkinter as tk
import sys
from game_db import record_win, get_players

player1, player2 = get_players()


root = tk.Tk()
root.title("Tic Tac Toe")
root.resizable(False, False)

current = "X"
board = [""] * 9
buttons = []
game_over = False

def check_win():
    global game_over
    wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]

    for a, b, c in wins:
        if board[a] == board[b] == board[c] != "":
            winner = player1 if board[a] == "X" else player2
            record_win(winner)
            status.config(text=f"{board[a]} wins")
            disable()
            game_over = True
            return

    if "" not in board:
        status.config(text="Draw")
        game_over = True

def click(i):
    global current
    if board[i] != "" or game_over:
        return

    board[i] = current
    buttons[i].config(text=current)

    check_win()
    if game_over:
        return

    current = "O" if current == "X" else "X"
    status.config(text=f"{current} turn")

def disable():
    for b in buttons:
        b.config(state="disabled")

def restart():
    global board, current, game_over
    board = [""] * 9
    current = "X"
    game_over = False
    status.config(text="X turn")
    for b in buttons:
        b.config(text="", state="normal")

grid = tk.Frame(root)
grid.pack(pady=10)

for i in range(9):
    btn = tk.Button(
        grid,
        text="",
        font=("Arial", 32),
        width=3,
        height=1,
        command=lambda i=i: click(i)
    )
    btn.grid(row=i//3, column=i%3)
    buttons.append(btn)

status = tk.Label(root, text="X turn", font=("Arial", 14))
status.pack(pady=5)

tk.Button(root, text="Restart", command=restart).pack(pady=5)

root.mainloop()
