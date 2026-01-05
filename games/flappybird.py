import pygame
import random
import sys
from game_db import record_win, get_players

player1, player2 = get_players()

pygame.init()

# ---------------- SETUP ----------------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird - 2 Player")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

SKY = (135, 206, 235)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 200, 0)

# ---------------- GAME VARIABLES ----------------
bird_x = 150
bird_y = HEIGHT // 2
bird_radius = 15
gravity = 0.4
velocity = 0

pipe_width = 60
pipe_gap = 160
pipe_speed = 3
pipes = []

current_player = 1
score = 0
score_p1 = 0
score_p2 = 0

game_started = False
game_over = False

# ---------------- FUNCTIONS ----------------
def create_pipe():
    height = random.randint(120, 420)
    pipes.append({
        "x": WIDTH,
        "top": height - pipe_gap // 2,
        "bottom": height + pipe_gap // 2
    })

def reset_round():
    global bird_y, velocity, pipes, score, game_started
    bird_y = HEIGHT // 2
    velocity = 0
    pipes.clear()
    score = 0
    game_started = False
    create_pipe()

def end_turn():
    global current_player, score_p1, score_p2, game_over
    if current_player == 1:
        score_p1 = score
        current_player = 2
        reset_round()
    else:
        score_p2 = score
        game_over = True

# Initial pipe
create_pipe()

# ---------------- MAIN LOOP ----------------
running = True
while running:

    # -------- EVENTS --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_started and not game_over:
                    game_started = True
                velocity = -7

            if event.key == pygame.K_r:
                current_player = 1
                score_p1 = 0
                score_p2 = 0
                game_over = False
                reset_round()

    # -------- GAME OVER SCREEN --------
    if game_over:
        screen.fill(SKY)

        title = big_font.render("GAME OVER", True, BLACK)
        p1 = font.render(f"{player1} Score: {score_p1}", True, BLACK)
        p2 = font.render(f"{player2} Score: {score_p2}", True, BLACK)

        if score_p1 > score_p2:
            winner = f"{player1} Wins!"
            record_win(player1)
        elif score_p2 > score_p1:
            winner = f"{player2} Wins!"
            record_win(player2)
        else:
            winner = "It's a Tie!"

        win_text = font.render(winner, True, BLACK)
        restart = font.render("Press R to Restart", True, BLACK)

        screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))
        screen.blit(p1, (WIDTH//2 - p1.get_width()//2, 260))
        screen.blit(p2, (WIDTH//2 - p2.get_width()//2, 300))
        screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, 360))
        screen.blit(restart, (WIDTH//2 - restart.get_width()//2, 420))

        pygame.display.update()
        clock.tick(60)
        continue

    # -------- START SCREEN --------
    if not game_started:
        screen.fill(SKY)

        title = big_font.render("FLAPPY BIRD", True, BLACK)
        player_text = font.render(f"Player {current_player}'s Turn", True, BLACK)
        inst1 = font.render("Press SPACE to Start / Fly", True, BLACK)
        inst2 = font.render("Avoid the Pipes", True, BLACK)

        screen.blit(title, (WIDTH//2 - title.get_width()//2, 160))
        screen.blit(player_text, (WIDTH//2 - player_text.get_width()//2, 260))
        screen.blit(inst1, (WIDTH//2 - inst1.get_width()//2, 320))
        screen.blit(inst2, (WIDTH//2 - inst2.get_width()//2, 360))

        pygame.display.update()
        clock.tick(60)
        continue

    # -------- GAME LOGIC --------
    velocity += gravity
    bird_y += velocity

    # Move pipes
    for pipe in pipes:
        pipe["x"] -= pipe_speed

    if pipes[-1]["x"] < 200:
        create_pipe()

    if pipes[0]["x"] < -pipe_width:
        pipes.pop(0)
        score += 1

    # -------- COLLISIONS --------
    if bird_y <= 0 or bird_y >= HEIGHT:
        end_turn()

    for pipe in pipes:
        if bird_x + bird_radius > pipe["x"] and bird_x - bird_radius < pipe["x"] + pipe_width:
            if bird_y - bird_radius < pipe["top"] or bird_y + bird_radius > pipe["bottom"]:
                end_turn()

    # -------- DRAW --------
    screen.fill(SKY)

    pygame.draw.circle(screen, YELLOW, (bird_x, int(bird_y)), bird_radius)

    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, (pipe["x"], 0, pipe_width, pipe["top"]))
        pygame.draw.rect(screen, GREEN, (pipe["x"], pipe["bottom"], pipe_width, HEIGHT))

    score_text = font.render(f"Score: {score}", True, BLACK)
    player_text = font.render(f"Player {current_player}", True, BLACK)

    screen.blit(score_text, (10, 10))
    screen.blit(player_text, (10, 40))

    pygame.display.update()
    clock.tick(60)
