import pygame
import sys
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


# --- Configuration ---
WIDTH, HEIGHT = 500, 600
GRID_SIZE = 3  # 3x3 boxes (4x4 dots)
CELL_SIZE = 100
OFFSET = 100
DOT_RADIUS = 6
LINE_WIDTH = 6
SNAP_DIST = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (220, 50, 50)
BLUE  = (50, 50, 220)
GRAY  = (200, 200, 200)

class DotsAndBoxes:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Dots and Boxes")
        self.font = pygame.font.SysFont("Arial", 28, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 18, bold=True)
        self.reset_game()

    def reset_game(self):
        self.turn = 1 # 1 = Red (You), 2 = Blue (Me)
        self.h_lines = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE + 1)]
        self.v_lines = [[0 for _ in range(GRID_SIZE + 1)] for _ in range(GRID_SIZE)]
        self.boxes = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.scores = {1: 0, 2: 0}
        self.game_over = False

    def draw_dotted_line(self, start, end, color):
        """Draws a dashed/dotted line for the hover preview."""
        dist = ((start[0]-end[0])**2 + (start[1]-end[1])**2)**0.5
        dl = 10 # Dash length
        for i in range(0, int(dist), dl * 2):
            s = [start[0] + (end[0]-start[0]) * i / dist, start[1] + (end[1]-start[1]) * i / dist]
            e = [start[0] + (end[0]-start[0]) * (i+dl) / dist, start[1] + (end[1]-start[1]) * (i+dl) / dist]
            pygame.draw.line(self.screen, color, s, e, 2)

    def get_hover_line(self, mouse_pos):
        mx, my = mouse_pos
        # Check Horizontal
        for r in range(GRID_SIZE + 1):
            for c in range(GRID_SIZE):
                x = OFFSET + c * CELL_SIZE
                y = OFFSET + r * CELL_SIZE
                rect = pygame.Rect(x, y - SNAP_DIST, CELL_SIZE, SNAP_DIST * 2)
                if rect.collidepoint(mx, my) and self.h_lines[r][c] == 0:
                    return ('h', r, c)
        # Check Vertical
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE + 1):
                x = OFFSET + c * CELL_SIZE
                y = OFFSET + r * CELL_SIZE
                rect = pygame.Rect(x - SNAP_DIST, y, SNAP_DIST * 2, CELL_SIZE)
                if rect.collidepoint(mx, my) and self.v_lines[r][c] == 0:
                    return ('v', r, c)
        return None

    def check_box(self, type, r, c):
        made_box = False
        to_check = []
        if type == 'h':
            if r > 0: to_check.append((r-1, c))
            if r < GRID_SIZE: to_check.append((r, c))
        else:
            if c > 0: to_check.append((r, c-1))
            if c < GRID_SIZE: to_check.append((r, c))

        for br, bc in to_check:
            if self.h_lines[br][bc] and self.h_lines[br+1][bc] and \
               self.v_lines[br][bc] and self.v_lines[br][bc+1]:
                self.boxes[br][bc] = self.turn
                self.scores[self.turn] += 1
                made_box = True
        return made_box

    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            hover = self.get_hover_line(mouse_pos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    if hover:
                        type, r, c = hover
                        if type == 'h': self.h_lines[r][c] = self.turn
                        else: self.v_lines[r][c] = self.turn
                        
                        if not self.check_box(type, r, c):
                            self.turn = 2 if self.turn == 1 else 1
                        
                        if self.scores[1] + self.scores[2] == GRID_SIZE**2:
                            self.game_over = True

                # Restart Button Click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(WIDTH//2-50, 530, 100, 40).collidepoint(mouse_pos):
                        self.reset_game()

            # --- DRAWING ---
            self.screen.fill(WHITE)
            
            # Scoreboard
            txt_you = self.font.render(f"You: {self.scores[1]}", True, RED)
            txt_me = self.font.render(f"Me: {self.scores[2]}", True, BLUE)
            self.screen.blit(txt_you, (OFFSET, 30))
            self.screen.blit(txt_me, (WIDTH - OFFSET - 80, 30))

            # Boxes and Text
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    if self.boxes[r][c] != 0:
                        label = "You" if self.boxes[r][c] == 1 else "Me"
                        color = RED if self.boxes[r][c] == 1 else BLUE
                        txt = self.font.render(label, True, color)
                        self.screen.blit(txt, (OFFSET + c*CELL_SIZE + 25, OFFSET + r*CELL_SIZE + 35))

            # Hover Preview
            if hover and not self.game_over:
                t, r, c = hover
                color = RED if self.turn == 1 else BLUE
                if t == 'h':
                    self.draw_dotted_line((OFFSET+c*CELL_SIZE, OFFSET+r*CELL_SIZE), 
                                         (OFFSET+(c+1)*CELL_SIZE, OFFSET+r*CELL_SIZE), color)
                else:
                    self.draw_dotted_line((OFFSET+c*CELL_SIZE, OFFSET+r*CELL_SIZE), 
                                         (OFFSET+c*CELL_SIZE, OFFSET+(r+1)*CELL_SIZE), color)

            # Permanent Lines
            for r in range(GRID_SIZE + 1):
                for c in range(GRID_SIZE):
                    if self.h_lines[r][c]:
                        color = RED if self.h_lines[r][c] == 1 else BLUE
                        pygame.draw.line(self.screen, color, (OFFSET+c*CELL_SIZE, OFFSET+r*CELL_SIZE), 
                                         (OFFSET+(c+1)*CELL_SIZE, OFFSET+r*CELL_SIZE), LINE_WIDTH)
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE + 1):
                    if self.v_lines[r][c]:
                        color = RED if self.v_lines[r][c] == 1 else BLUE
                        pygame.draw.line(self.screen, color, (OFFSET+c*CELL_SIZE, OFFSET+r*CELL_SIZE), 
                                         (OFFSET+c*CELL_SIZE, OFFSET+(r+1)*CELL_SIZE), LINE_WIDTH)

            # Dots
            for r in range(GRID_SIZE + 1):
                for c in range(GRID_SIZE + 1):
                    pygame.draw.circle(self.screen, BLACK, (OFFSET+c*CELL_SIZE, OFFSET+r*CELL_SIZE), DOT_RADIUS)

            # Restart Button
            pygame.draw.rect(self.screen, GRAY, (WIDTH//2-50, 530, 100, 40), border_radius=5)
            btn_txt = self.small_font.render("RESTART", True, BLACK)
            self.screen.blit(btn_txt, (WIDTH//2-38, 540))

            # End Game Message
            if self.game_over:
                winner = "Red Wins!" if self.scores[1] > self.scores[2] else "Blue Wins!"
                if self.scores[1] == self.scores[2]: winner = "It's a Draw!"
                win_txt = self.font.render(winner, True, BLACK)
                self.screen.blit(win_txt, (WIDTH//2 - 60, 480))

            pygame.display.flip()

if __name__ == "__main__":
    game = DotsAndBoxes()
    game.run()
