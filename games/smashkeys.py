import tkinter as tk
import random
import sys
from game_db import record_win, get_players

player1, player2 = get_players()


TARGET = 5

root = tk.Tk()
root.title("Reaction Accuracy Duel")
root.resizable(False, False)
root.geometry("500x380")

WAIT_BG = "#2c3e50"
GO_BG = "#1abc9c"
NEUTRAL = "#ecf0f1"

root.configure(bg=WAIT_BG)

p1 = 0.0
p2 = 0.0
game_over = False
round_active = False
round_timer = None

def update_ui():
    p1_bar.config(width=int(p1 * 40))
    p2_bar.config(width=int(p2 * 40))
    score.config(text=f"P1: {p1:.1f}   P2: {p2:.1f}")

def start_round():
    global round_active, round_timer
    if game_over:
        return

    round_active = False
    root.configure(bg=WAIT_BG)
    status.config(text="WAIT", bg=WAIT_BG, fg="white")

    delay = random.randint(2500, 5000)
    round_timer = root.after(delay, go_signal)

def go_signal():
    global round_active
    if game_over:
        return

    root.configure(bg=GO_BG)
    status.config(text="GO!", bg=GO_BG, fg="black")
    round_active = True

def penalize(player):
    global p1, p2
    if player == 1:
        p1 = max(0, p1 - 0.5)
    else:
        p2 = max(0, p2 - 0.5)
    update_ui()

def end_game(text):
    global game_over, round_active
    game_over = True
    round_active = False

    if round_timer:
        root.after_cancel(round_timer)

    root.configure(bg=NEUTRAL)
    status.config(text=text, bg=NEUTRAL, fg="black")

def key_press(event):
    global p1, p2, round_active

    if game_over:
        return

    key = event.keysym.lower()

    # Early press penalty (own key only)
    if not round_active:
        if key == "a":
            penalize(1)
        elif key == "l":
            penalize(2)
        return

    # Scoring after GO
    if key == "a":
        p1 += 1
    elif key == "l":
        p2 += 1
    else:
        return

    update_ui()
    round_active = False

    if p1 >= TARGET:
        end_game("Player 1 Wins!")
        record_win(player1)
        return
    if p2 >= TARGET:
        end_game("Player 2 Wins!")
        record_win(player2)
        return

    root.after(1200, start_round)

def restart():
    global p1, p2, game_over, round_active
    p1 = p2 = 0.0
    game_over = False
    round_active = False
    update_ui()
    start_round()

root.bind("<KeyPress>", key_press)

# ===== UI =====
tk.Label(
    root,
    text="REACTION ACCURACY DUEL",
    font=("Arial", 20, "bold"),
    bg=WAIT_BG,
    fg="white"
).pack(pady=10)

# Instructions (NEW)
instruction = tk.Label(
    root,
    text="Player 1 → Press A        Player 2 → Press L",
    font=("Arial", 12),
    bg=WAIT_BG,
    fg="white"
)
instruction.pack(pady=5)

bar_frame = tk.Frame(root, bg=WAIT_BG)
bar_frame.pack(pady=10)

tk.Label(bar_frame, text="P1 (A)", bg=WAIT_BG, fg="white").grid(row=0, column=0)
tk.Label(bar_frame, text="P2 (L)", bg=WAIT_BG, fg="white").grid(row=0, column=2)

p1_bg = tk.Frame(bar_frame, width=200, height=20, bg="#bdc3c7")
p1_bg.grid(row=1, column=0, padx=10)
p1_bg.pack_propagate(False)

p2_bg = tk.Frame(bar_frame, width=200, height=20, bg="#bdc3c7")
p2_bg.grid(row=1, column=2, padx=10)
p2_bg.pack_propagate(False)

p1_bar = tk.Frame(p1_bg, height=20, bg="#27ae60")
p1_bar.pack(side="left")

p2_bar = tk.Frame(p2_bg, height=20, bg="#e74c3c")
p2_bar.pack(side="left")

score = tk.Label(
    root,
    text="P1: 0.0   P2: 0.0",
    font=("Arial", 14),
    bg=WAIT_BG,
    fg="white"
)
score.pack(pady=5)

status = tk.Label(
    root,
    text="WAIT",
    font=("Arial", 24, "bold"),
    bg=WAIT_BG,
    fg="white"
)
status.pack(pady=15)

tk.Button(root, text="Restart", command=restart).pack(pady=10)

update_ui()
start_round()
root.mainloop()
