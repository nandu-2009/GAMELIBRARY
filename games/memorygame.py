import tkinter as tk
import random

# ---------------- CONFIG ----------------
GRID_SIZE = 3
FLASH_COLOR = "#a6e3ff"
NORMAL_COLOR = "#2f7dd1"
BG_COLOR = "#2d8bd4"

# ---------------- GAME CLASS ----------------
class SequenceGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sequence Memory Duel")
        self.root.geometry("600x650")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)

        self.players = ["Player 1", "Player 2"]
        self.current_player = 0
        self.scores = [0, 0]

        self.sequence = []
        self.user_input = []
        self.buttons = []
        self.accepting_input = False

        # ---------- UI ----------
        tk.Label(
            root, text="SEQUENCE MEMORY",
            font=("Arial", 28, "bold"),
            bg=BG_COLOR, fg="white"
        ).pack(pady=15)

        self.turn_label = tk.Label(
            root, text="Player 1's Turn",
            font=("Arial", 18),
            bg=BG_COLOR, fg="white"
        )
        self.turn_label.pack()

        self.level_label = tk.Label(
            root, text="Level: 1",
            font=("Arial", 18, "bold"),
            bg=BG_COLOR, fg="white"
        )
        self.level_label.pack(pady=5)

        self.status = tk.Label(
            root, text="Watch the sequence",
            font=("Arial", 18),
            bg=BG_COLOR, fg="white"
        )
        self.status.pack(pady=10)

        self.grid = tk.Frame(root, bg=BG_COLOR)
        self.grid.pack(pady=(10, 30))

        self.create_grid()
        self.root.after(1200, self.start_round)

    # ---------------- GRID ----------------
    def create_grid(self):
        for i in range(GRID_SIZE * GRID_SIZE):
            btn = tk.Button(
                self.grid,
                width=9,
                height=4,
                bg=NORMAL_COLOR,
                relief="flat",
                state="disabled",
                command=lambda i=i: self.tile_click(i)
            )
            btn.grid(
                row=i // GRID_SIZE,
                column=i % GRID_SIZE,
                padx=18,
                pady=18
            )
            self.buttons.append(btn)

    # ---------------- GAME FLOW ----------------
    def start_round(self):
        self.accepting_input = False
        self.user_input.clear()
        self.status.config(text="Watch the sequence", fg="white")

        self.turn_label.config(
            text=f"{self.players[self.current_player]}'s Turn"
        )
        self.level_label.config(
            text=f"Level: {len(self.sequence) + 1}"
        )

        self.sequence.append(random.randint(0, GRID_SIZE * GRID_SIZE - 1))
        self.flash_sequence()

    def flash_sequence(self):
        self.disable_buttons()
        for i, idx in enumerate(self.sequence):
            self.root.after(i * 650, lambda x=idx: self.flash_tile(x))
        self.root.after(len(self.sequence) * 650 + 300, self.enable_input)

    def flash_tile(self, index):
        btn = self.buttons[index]
        btn.config(bg=FLASH_COLOR)
        self.root.after(300, lambda: btn.config(bg=NORMAL_COLOR))

    def enable_input(self):
        self.accepting_input = True
        self.status.config(text="Repeat the sequence")
        self.enable_buttons()

    # ---------------- INPUT ----------------
    def tile_click(self, index):
        if not self.accepting_input:
            return

        self.user_input.append(index)

        if self.user_input[-1] != self.sequence[len(self.user_input) - 1]:
            self.end_turn()
            return

        if len(self.user_input) == len(self.sequence):
            self.correct_move()

    def correct_move(self):
        self.accepting_input = False
        self.status.config(text="✔ CORRECT!", fg="#b6ffb6")
        self.disable_buttons()
        self.root.after(900, self.start_round)

    def end_turn(self):
        self.accepting_input = False
        level_reached = len(self.sequence) - 1
        self.scores[self.current_player] = level_reached

        self.status.config(
            text=f"❌ WRONG! Reached Level {level_reached}",
            fg="#ffd6d6"
        )
        self.disable_buttons()
        self.root.after(1500, self.next_player)

    def next_player(self):
        self.sequence.clear()
        self.user_input.clear()

        if self.current_player == 0:
            self.current_player = 1
            self.root.after(800, self.start_round)
        else:
            self.show_winner()

    # ---------------- END GAME ----------------
    def show_winner(self):
        p1, p2 = self.scores

        if p1 > p2:
            result = "🏆 Player 1 Wins!"
        elif p2 > p1:
            result = "🏆 Player 2 Wins!"
        else:
            result = "🤝 IT'S A TIE!"

        self.status.config(text=result, fg="yellow")
        self.level_label.config(
            text=f"Final Scores → P1: {p1} | P2: {p2}"
        )

    # ---------------- UTILS ----------------
    def disable_buttons(self):
        for b in self.buttons:
            b.config(state="disabled")

    def enable_buttons(self):
        for b in self.buttons:
            b.config(state="normal")

# ---------------- RUN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    SequenceGame(root)
    root.mainloop()

