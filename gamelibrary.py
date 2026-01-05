import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import os
import subprocess
import sys



# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GAMES_DIR = os.path.join(BASE_DIR, "games")
ICONS_DIR = os.path.join(BASE_DIR, "icons")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS scores (
    player TEXT PRIMARY KEY,
    wins INTEGER DEFAULT 0
)
""")

conn.commit()

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

# ---------------- GAME LIST ----------------
GAMES = [
    ("Guess", "guessthenumber"),
    ("Connect 4", "connect4"),
    ("Ping Pong", "pingpong"),
    ("Tic Tac Toe", "tictactoe"),
    ("Snake", "snake"),
    ("Asteroids", "asteroids"),
    ("Flappy", "flappybird"),
    ("Dots", "dotsandboxes"),
    ("Wordle", "wordle"),
    ("Maze", "mazegame"),
    ("Smash keys", "smashkeys"),
    ("Memory game","memorygame")]

# ---------------- MAIN APP ----------------
class ArcadeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Competitive Arcade")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)

        self.images = {}
        self.player1 = ""
        self.player2 = ""

        self.main = tk.Frame(root, bg="#f4f4f4")
        self.main.pack(expand=True, fill="both")

        self.show_login()

    # ---------------- UTILITY ----------------
    def clear(self):
        for w in self.main.winfo_children():
            w.destroy()

    # ---------------- LOGIN ----------------
    def show_login(self):
        self.clear()
        self.root.configure(bg="#f4f4f4")
        self.main.configure(bg="#f4f4f4")

        tk.Label(self.main, text="Login", font=("Arial", 26, "bold"), bg="#f4f4f4").pack(pady=30)
        tk.Label(self.main, text="Username", bg="#f4f4f4").pack()
        self.user = tk.Entry(self.main, font=("Arial", 14), width=25)
        self.user.pack(pady=10)

        tk.Label(self.main, text="Password", bg="#f4f4f4").pack()
        self.pwd = tk.Entry(self.main, font=("Arial", 14), show="*", width=25)
        self.pwd.pack(pady=10)

        tk.Button(self.main, text="Login", width=20, bg="#4CAF50", fg="white", command=self.login).pack(pady=10)
        tk.Button(self.main, text="Create Account", bg="#f4f4f4", fg="blue", command=self.show_signup).pack()

    def login(self):
        u = self.user.get()
        p = hash_password(self.pwd.get())
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
        if cursor.fetchone():
            self.show_player_entry()
        else:
            messagebox.showerror("Error", "Invalid login")

    # ---------------- SIGNUP ----------------
    def show_signup(self):
        self.clear()
        tk.Label(self.main, text="Sign Up", font=("Arial", 26, "bold")).pack(pady=30)
        self.new_user = tk.Entry(self.main, font=("Arial", 14), width=25)
        self.new_user.pack(pady=10)
        self.new_pwd = tk.Entry(self.main, font=("Arial", 14), show="*", width=25)
        self.new_pwd.pack(pady=10)

        tk.Button(self.main, text="Create Account", width=20, command=self.signup).pack(pady=10)
        tk.Button(self.main, text="Back", command=self.show_login).pack()

    def signup(self):
        try:
            cursor.execute(
                "INSERT INTO users VALUES (NULL, ?, ?)",
                (self.new_user.get(), hash_password(self.new_pwd.get()))
            )
            conn.commit()
            messagebox.showinfo("Success", "Account created")
            self.show_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")

    # ---------------- PLAYER ENTRY ----------------
    def show_player_entry(self):
        self.clear()
        tk.Label(self.main, text="Enter Player Names", font=("Arial", 26, "bold")).pack(pady=30)

        tk.Label(self.main, text="Player 1").pack()
        self.p1_entry = tk.Entry(self.main, font=("Arial", 14), width=25)
        self.p1_entry.pack(pady=10)

        tk.Label(self.main, text="Player 2").pack()
        self.p2_entry = tk.Entry(self.main, font=("Arial", 14), width=25)
        self.p2_entry.pack(pady=10)

        tk.Button(self.main, text="Continue", width=20, command=self.save_players).pack(pady=20)

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
        self.root.configure(bg="#1e1e2e")
        self.main.configure(bg="#1e1e2e")

        tk.Label(self.main, text="🎮 GAME ARCADE", font=("Arial", 28, "bold"),
                 bg="#1e1e2e", fg="white").pack(pady=15)

        tk.Label(self.main, text=f"{self.player1}  vs  {self.player2}",
                 font=("Arial", 16), bg="#1e1e2e", fg="white").pack(pady=5)

        cursor.execute("SELECT wins FROM scores WHERE player=?", (self.player1,))
        p1 = cursor.fetchone()
        p1_score = p1[0] if p1 else 0

        cursor.execute("SELECT wins FROM scores WHERE player=?", (self.player2,))
        p2 = cursor.fetchone()
        p2_score = p2[0] if p2 else 0

        tk.Label(
            self.main,
            text=f"{self.player1}: {p1_score} wins   |   {self.player2}: {p2_score} wins",
            font=("Arial", 14, "bold"),
            bg="#1e1e2e",
            fg="#FFD700"
        ).pack(pady=8)

        grid = tk.Frame(self.main, bg="#1e1e2e")
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

            tk.Label(card, text=name, fg="white",
                     bg="#2a2a3d", font=("Arial", 16, "bold")).pack(pady=5)

# ---------------- RUN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    ArcadeApp(root)
    root.mainloop()

