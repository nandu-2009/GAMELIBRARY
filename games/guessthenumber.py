

import tkinter as Tk
from tkinter import messagebox
import random
import sys
from game_db import record_win, get_players

player1, player2 = get_players()

root = Tk.Tk()
root.title("Guess The Number - 2 Player")

# Center window
x = (root.winfo_screenwidth() // 2) - 400
y = (root.winfo_screenheight() // 2) - 300
root.geometry(f"800x600+{x}+{y}")

# ---------------- GAME VARIABLES ----------------
secret_p1 = random.randint(1, 100)
secret_p2 = random.randint(1, 100)

current_player = 1
attempts_p1 = 0
attempts_p2 = 0

# ---------------- GAME LOGIC ----------------
def check_guess():
    global attempts_p1, attempts_p2, current_player

    guess = entry_guess.get()

    if not guess.isdigit():
        messagebox.showwarning("Invalid Input", "Please enter a valid number!")
        return

    guess = int(guess)

    if current_player == 1:
        attempts_p1 += 1
        secret = secret_p1
    else:
        attempts_p2 += 1
        secret = secret_p2

    if guess < secret:
        label_result.config(text="Too Low!", fg="blue")
    elif guess > secret:
        label_result.config(text="Too High!", fg="orange")
    else:
        messagebox.showinfo(
            "Correct!",
            f"Player {current_player} guessed their number in "
            f"{attempts_p1 if current_player == 1 else attempts_p2} attempts!"
        )
        switch_player()

    entry_guess.delete(0, Tk.END)

def switch_player():
    global current_player

    if current_player == 1:
        current_player = 2
        label_turn.config(text="Player 2's Turn", fg="purple")
        label_result.config(text="Player 2: Guess your number!")
    else:
        declare_winner()

def declare_winner():
    if attempts_p1 < attempts_p2:
        winner = "Player 1"
        record_win(player1)
    elif attempts_p2 < attempts_p1:
        winner = "Player 2"
        record_win(player2)
    else:
        winner = "It's a Tie!"

    messagebox.showinfo(
        "Game Over",
        f"Player 1 Attempts: {attempts_p1}\n"
        f"Player 2 Attempts: {attempts_p2}\n\n"
        f"Winner: {winner}"
    )
    reset_game()

def reset_game():
    global secret_p1, secret_p2, attempts_p1, attempts_p2, current_player

    secret_p1 = random.randint(1, 100)
    secret_p2 = random.randint(1, 100)
    attempts_p1 = 0
    attempts_p2 = 0
    current_player = 1

    label_turn.config(text="Player 1's Turn", fg="green")
    label_result.config(
        text="A number between 1 and 100 has been chosen",
        fg="darkblue"
    )
    entry_guess.delete(0, Tk.END)

# ---------------- UI ----------------
label_title = Tk.Label(
    root,
    text="Guess The Number (2 Players)",
    font=("Courier", 32, "bold")
)
label_title.pack(pady=10)

label_turn = Tk.Label(
    root,
    text="Player 1's Turn",
    font=("Courier", 22, "bold"),
    fg="green"
)
label_turn.pack(pady=10)

label_instruction = Tk.Label(
    root,
    text="Enter your guess:",
    font=("Courier", 18)
)
label_instruction.pack()

entry_guess = Tk.Entry(
    root,
    width=25,
    font=("Courier", 16)
)
entry_guess.pack(pady=10)

btn_guess = Tk.Button(
    root,
    text="Check Guess",
    command=check_guess,
    font=("Courier", 18)
)
btn_guess.pack(pady=10)

label_result = Tk.Label(
    root,
    text="A number between 1 and 100 has been chosen",
    font=("Courier", 18),
    fg="darkblue"
)
label_result.pack(pady=20)

btn_exit = Tk.Button(
    root,
    text="Exit",
    command=root.destroy,
    font=("Courier", 18, "bold"),
    fg="red"
)
btn_exit.pack(pady=10)

root.mainloop()

