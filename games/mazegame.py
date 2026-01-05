import pygame
import time
import os
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


# 1. Configuration
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 650 
PLAYER_SIZE = 8
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
P1_COLOR = (255, 50, 50) 
P2_COLOR = (50, 50, 255) 
TEXT_COLOR = (200, 200, 200)

class MazeGame:
    def __init__(self, maze_img_path):
        pygame.init()
        
        # Verify file exists
        if not os.path.exists(maze_img_path):
            print(f"Error: Could not find '{maze_img_path}' in the folder.")
            pygame.quit()
            sys.exit()

        try:
            # Load the image. If convert() fails due to format mismatch, 
            # we catch the error to prevent the crash.
            self.maze_img = pygame.image.load(maze_img_path)
            self.maze_img = pygame.transform.scale(self.maze_img, (600, 600))
        except pygame.error as e:
            print(f"Pygame Load Error: {e}")
            print("Try opening the image in Paint and saving it as a true PNG or JPG.")
            pygame.quit()
            sys.exit()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2-Player Maze Race")
        self.font = pygame.font.SysFont("Verdana", 20)
        self.clock = pygame.time.Clock()

    def is_wall(self, x, y):
        """Checks if any part of the player hits a black pixel."""
        if x < 0 or x + PLAYER_SIZE >= 600 or y < 0 or y + PLAYER_SIZE >= 600:
            return True
            
        corners = [(x, y), (x + PLAYER_SIZE, y), (x, y + PLAYER_SIZE), (x + PLAYER_SIZE, y + PLAYER_SIZE)]
        for cx, cy in corners:
            color = self.maze_img.get_at((int(cx), int(cy)))
            # If the red value of the pixel is low, we consider it a 'black' wall
            if color[0] < 60: 
                return True
        return False

    def play_turn(self, player_num, color):
        px, py = 5, 45 # Adjusted starting point for your maze layout
        start_time = time.time()
        
        running = True
        while running:
            self.screen.fill(BLACK)
            self.screen.blit(self.maze_img, (0, 0))
            elapsed = time.time() - start_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            speed = 3
            if keys[pygame.K_w]: dy = -speed
            if keys[pygame.K_s]: dy = speed
            if keys[pygame.K_a]: dx = -speed
            if keys[pygame.K_d]: dx = speed

            if not self.is_wall(px + dx, py):
                px += dx
            if not self.is_wall(px, py + dy):
                py += dy

            # Check Win Condition (Bottom-right exit)
            if px > 585 and py > 550:
                return round(elapsed, 2)

            pygame.draw.rect(self.screen, color, (px, py, PLAYER_SIZE, PLAYER_SIZE))
            info = self.font.render(f"PLAYER {player_num} | Time: {elapsed:.2f}s", True, TEXT_COLOR)
            self.screen.blit(info, (20, 615))
            
            pygame.display.flip()
            self.clock.tick(FPS)

    def wait_for_ready(self, message):
        waiting = True
        while waiting:
            self.screen.fill(BLACK)
            txt = self.font.render(message, True, WHITE)
            sub_txt = self.font.render("Press SPACE to Start", True, TEXT_COLOR)
            self.screen.blit(txt, (SCREEN_WIDTH//2 - 150, 300))
            self.screen.blit(sub_txt, (SCREEN_WIDTH//2 - 100, 340))
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False

    def run(self):
        self.wait_for_ready("PLAYER 1: Get Ready!")
        p1_score = self.play_turn(1, P1_COLOR)
        
        self.wait_for_ready(f"P1 Time: {p1_score}s. PLAYER 2: Ready?")
        p2_score = self.play_turn(2, P2_COLOR)

        self.screen.fill(BLACK)
        winner = "Player 1 Wins!" if p1_score < p2_score else "Player 2 Wins!"
        if p1_score == p2_score: winner = "It's a Tie!"
        
        if p1_score < p2_score:
            record_win(player1)
        elif p2_score < p1_score:
            record_win(player2)
        
        res_text = self.font.render(f"P1: {p1_score}s | P2: {p2_score}s", True, WHITE)
        win_text = self.font.render(winner, True, (0, 255, 0))
        
        self.screen.blit(res_text, (200, 250))
        self.screen.blit(win_text, (230, 300))
        pygame.display.flip()
        time.sleep(5)
        pygame.quit()

if __name__ == "__main__":
    # Updated to match your exact file name
    game = MazeGame("maze.png")
    game.run()
