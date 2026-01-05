import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GAMES_DIR = os.path.join(BASE_DIR, "games")
ICONS_DIR = os.path.join(BASE_DIR, "icons")

# Game list
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
    ("Memory game", "memorygame")
]

# UI Colors
BG_COLOR = "#1e1e2e"
FG_COLOR = "white"
ACCENT_COLOR = "#FFD700"
BUTTON_BG = "#4CAF50"
BUTTON_FG = "white"