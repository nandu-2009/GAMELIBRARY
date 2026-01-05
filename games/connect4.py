import numpy as np
import pygame
import sys
import math
import time
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
conn = sqlite3.connect(os.path.join(BASE_DIR, "users.db"))
cursor = conn.cursor()

def record_win(player):
    cursor.execute("""
        INSERT INTO scores(player, wins)
        VALUES (?, 1)
        ON CONFLICT(player)
        DO UPDATE SET wins = wins + 1
    """, (player,))
    conn.commit()

player1 = sys.argv[1]
player2 = sys.argv[2]

# ---------------- CONFIG ----------------
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)

# ---------------- GAME LOGIC ----------------
def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if all(board[r][c + i] == piece for i in range(4)):
                return True

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c] == piece for i in range(4)):
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True

    return False

# ---------------- DRAW ----------------
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(
                screen, BLUE,
                (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE,
                 SQUARESIZE, SQUARESIZE)
            )
            pygame.draw.circle(
                screen, BLACK,
                (int(c * SQUARESIZE + SQUARESIZE / 2),
                 int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
                RADIUS
            )

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(
                    screen, RED,
                    (int(c * SQUARESIZE + SQUARESIZE / 2),
                     height - int(r * SQUARESIZE + SQUARESIZE / 2)),
                    RADIUS
                )
            elif board[r][c] == 2:
                pygame.draw.circle(
                    screen, YELLOW,
                    (int(c * SQUARESIZE + SQUARESIZE / 2),
                     height - int(r * SQUARESIZE + SQUARESIZE / 2)),
                    RADIUS
                )
    pygame.display.update()

# ---------------- MAIN ----------------
def main():
    global screen, height

    pygame.init()

    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT + 1) * SQUARESIZE
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Connect 4")

    font = pygame.font.SysFont("monospace", 60)

    board = create_board()
    draw_board(board)

    game_over = False
    turn = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                color = RED if turn == 0 else YELLOW
                pygame.draw.circle(
                    screen, color,
                    (posx, int(SQUARESIZE / 2)),
                    RADIUS
                )
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    piece = 1 if turn == 0 else 2
                    color = RED if turn == 0 else YELLOW

                    drop_piece(board, row, col, piece)

                    if winning_move(board, piece):
                        label = font.render(
                            f"Player {piece} Wins!",
                            True, color
                        )
                        screen.blit(label, (40, 10))
                        pygame.display.update()
                        time.sleep(3)
                        game_over = True

                    draw_board(board)
                    turn = (turn + 1) % 2

    pygame.quit()
    sys.exit()

# ---------------- RUN ----------------
if __name__ == "__main__":
    main()
