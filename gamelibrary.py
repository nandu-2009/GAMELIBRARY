import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import sys
from database import Database
from config import GAMES_DIR, ICONS_DIR, GAMES, BG_COLOR, FG_COLOR, ACCENT_COLOR, BUTTON_BG, BUTTON_FG

# ---------------- MAIN APP ----------------
class ArcadeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Competitive Arcade")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)

        self.db = Database()
        self.images = {}
        self.player1 = ""
        self.player2 = ""

        self.main = tk.Frame(root, bg=BG_COLOR)
        self.main.pack(expand=True, fill="both")

        self.show_login()

    # ---------------- UTILITY ----------------
    def clear(self):
        for w in self.main.winfo_children():
            w.destroy()

    # ---------------- LOGIN ----------------
    def show_login(self):
        self.clear()
        self.root.configure(bg=BG_COLOR)
        self.main.configure(bg=BG_COLOR)

        tk.Label(self.main, text="Login", font=("Arial", 26, "bold"), bg=BG_COLOR, fg=FG_COLOR).pack(pady=30)
        tk.Label(self.main, text="Username", bg=BG_COLOR, fg=FG_COLOR).pack()
        self.user = tk.Entry(self.main, font=("Arial", 14), width=25)
        self.user.pack(pady=10)

        tk.Label(self.main, text="Password", bg=BG_COLOR, fg=FG_COLOR).pack()
        self.pwd = tk.Entry(self.main, font=("Arial", 14), show="*", width=25)
        self.pwd.pack(pady=10)

        tk.Button(self.main, text="Login", width=20, bg=BUTTON_BG, fg=BUTTON_FG, command=self.login).pack(pady=10)
        tk.Button(self.main, text="Create Account", bg=BG_COLOR, fg="blue", command=self.show_signup).pack()

    def login(self):
        u = self.user.get()
        p = self.pwd.get()
        if self.db.authenticate_user(u, p):
            self.show_player_entry()
        else:
            messagebox.showerror("Error", "Invalid login")

    # ---------------- SIGNUP ----------------
    def show_signup(self):
        self.clear()
        tk.Label(self.main, text="Sign Up", font=("Arial", 26, "bold"), bg=BG_COLOR, fg=FG_COLOR).pack(pady=30)
        self.new_user = tk.Entry(self.main, font=("Arial", 14), width=25)
        self.new_user.pack(pady=10)
        self.new_pwd = tk.Entry(self.main, font=("Arial", 14), show="*", width=25)
        self.new_pwd.pack(pady=10)

        tk.Button(self.main, text="Create Account", width=20, bg=BUTTON_BG, fg=BUTTON_FG, command=self.signup).pack(pady=10)
        tk.Button(self.main, text="Back", command=self.show_login).pack()

    def signup(self):
        username = self.new_user.get()
        password = self.new_pwd.get()
        if self.db.create_user(username, password):
            messagebox.showinfo("Success", "Account created")
            self.show_login()
        else:
            messagebox.showerror("Error", "Username already exists")

    # ---------------- PLAYER ENTRY ----------------
    def show_player_entry(self):
        self.clear()
        tk.Label(self.main, text="Enter Player Names", font=("Arial", 26, "bold"), bg=BG_COLOR, fg=FG_COLOR).pack(pady=30)

        tk.Label(self.main, text="Player 1", bg=BG_COLOR, fg=FG_COLOR).pack()
        self.p1_entry = tk.Entry(self.main, font=("Arial", 14), width=25)
        self.p1_entry.pack(pady=10)

        tk.Label(self.main, text="Player 2", bg=BG_COLOR, fg=FG_COLOR).pack()
        self.p2_entry = tk.Entry(self.main, font=("Arial", 14), width=25)
        self.p2_entry.pack(pady=10)

        tk.Button(self.main, text="Continue", width=20, bg=BUTTON_BG, fg=BUTTON_FG, command=self.save_players).pack(pady=20)

    def save_players(self):
        self.player1 = self.p1_entry.get().strip()
        self.player2 = self.p2_entry.get().strip()
        if not self.player1 or not self.player2:
            messagebox.showerror("Error", "Enter both player names")
            return
        self.show_library()

    # ---------------- GAME LAUNCH ----------------
    def launch_game(self, game):
        path = os.path.join(GAMES_DIR, f"{game}.py")
        if not os.path.exists(path):
            messagebox.showerror("Missing", path)
            return

        subprocess.Popen(
            [sys.executable, path, self.player1, self.player2],
            cwd=GAMES_DIR
        )

    # ---------------- GAME LIBRARY ----------------
    def show_library(self):
        self.clear()
        self.root.configure(bg=BG_COLOR)
        self.main.configure(bg=BG_COLOR)

        tk.Label(self.main, text="🎮 GAME ARCADE", font=("Arial", 28, "bold"),
                 bg=BG_COLOR, fg=FG_COLOR).pack(pady=15)

        tk.Label(self.main, text=f"{self.player1}  vs  {self.player2}",
                 font=("Arial", 16), bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)

        self.score_label = tk.Label(
            self.main,
            text=self.get_score_text(),
            font=("Arial", 14, "bold"),
            bg=BG_COLOR,
            fg=ACCENT_COLOR
        )
        self.score_label.pack(pady=8)

        tk.Button(self.main, text="Refresh Scores", command=self.refresh_scores,
                  bg=BUTTON_BG, fg=BUTTON_FG).pack(pady=5)

        grid = tk.Frame(self.main, bg=BG_COLOR)
        grid.pack(expand=True, fill="both", padx=30, pady=30)

        COLS = 4
        ROWS = (len(GAMES) + COLS - 1) // COLS

        for c in range(COLS):
            grid.grid_columnconfigure(c, weight=1)
        for r in range(ROWS):
            grid.grid_rowconfigure(r, weight=1)

        for i, (name, key) in enumerate(GAMES):
            r, c = divmod(i, COLS)

            card = tk.Frame(grid, bg="#2a2a3d", bd=3, relief="raised")
            card.grid(row=r, column=c, padx=20, pady=20, sticky="nsew")
            card.grid_propagate(False)

            icon = os.path.join(ICONS_DIR, f"{key}.png")
            if os.path.exists(icon):
                img = tk.PhotoImage(file=icon)
                self.images[key] = img
                tk.Button(
                    card,
                    image=img,
                    bg="#2a2a3d",
                    bd=0,
                    command=lambda g=key: self.launch_game(g)
                ).pack(expand=True, pady=10)

            tk.Label(card, text=name, fg=FG_COLOR,
                     bg="#2a2a3d", font=("Arial", 16, "bold")).pack(pady=5)

    def get_score_text(self):
        p1_score = self.db.get_player_score(self.player1)
        p2_score = self.db.get_player_score(self.player2)
        return f"{self.player1}: {p1_score} wins   |   {self.player2}: {p2_score} wins"

    def refresh_scores(self):
        self.score_label.config(text=self.get_score_text())

# ---------------- RUN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    ArcadeApp(root)
    root.mainloop()

