import pygame
import random
import sys
from game_db import record_win, get_players

player1, player2 = get_players()


pygame.init()

# -------------------- SETTINGS --------------------
WIDTH, HEIGHT = 640, 700
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = (HEIGHT - 60) // GRID_SIZE

FPS = 60
MOVE_DELAY = 120  # ms between moves

# Colors
DARK_GREEN = (87, 138, 52)
LIGHT_GREEN = (170, 215, 81)
LIGHT_GREEN_2 = (162, 209, 73)
SNAKE_BLUE = (66, 133, 244)
BALL_RED = (234, 67, 53)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two Player Snake")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)
big_font = pygame.font.SysFont("arial", 40)

# -------------------- DRAWING --------------------
def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = LIGHT_GREEN if (x + y) % 2 == 0 else LIGHT_GREEN_2
            pygame.draw.rect(
                screen,
                color,
                (x * GRID_SIZE, y * GRID_SIZE + 60, GRID_SIZE, GRID_SIZE),
            )

def draw_top_bar(score, player):
    pygame.draw.rect(screen, DARK_GREEN, (0, 0, WIDTH, 60))
    text = font.render(f"Player {player} Score: {score}", True, WHITE)
    screen.blit(text, (20, 15))

def draw_snake(snake, direction):
    radius = GRID_SIZE // 2

    # Draw body (back to front for smooth overlap)
    for segment in reversed(snake):
        cx = segment[0] * GRID_SIZE + radius
        cy = segment[1] * GRID_SIZE + radius + 60
        pygame.draw.circle(screen, SNAKE_BLUE, (cx, cy), radius)

    # Head
    head = snake[0]
    hx = head[0] * GRID_SIZE + radius
    hy = head[1] * GRID_SIZE + radius + 60
    pygame.draw.circle(screen, SNAKE_BLUE, (hx, hy), radius)

    # Eyes
    eye_offset = 5
    if direction == (1, 0):  # right
        eyes = [(hx + eye_offset, hy - 4), (hx + eye_offset, hy + 4)]
    elif direction == (-1, 0):  # left
        eyes = [(hx - eye_offset, hy - 4), (hx - eye_offset, hy + 4)]
    elif direction == (0, -1):  # up
        eyes = [(hx - 4, hy - eye_offset), (hx + 4, hy - eye_offset)]
    else:  # down
        eyes = [(hx - 4, hy + eye_offset), (hx + 4, hy + eye_offset)]

    for ex, ey in eyes:
        pygame.draw.circle(screen, WHITE, (ex, ey), 3)
        pygame.draw.circle(screen, BLACK, (ex, ey), 1)

def random_food(snake):
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1),
               random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake:
            return pos

# -------------------- GAME --------------------
def wait_for_space(player):
    while True:
        screen.fill(DARK_GREEN)
        title = big_font.render(f"Player {player}", True, WHITE)
        prompt = font.render("Press SPACE when ready", True, WHITE)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 260))
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 320))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

def play_game(player_number):
    wait_for_space(player_number)

    snake = [(5, 5), (4, 5), (3, 5)]
    direction = (1, 0)
    food = random_food(snake)
    score = 0
    last_move = pygame.time.get_ticks()

    while True:
        clock.tick(FPS)
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_s and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_a and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_d and direction != (-1, 0):
                    direction = (1, 0)

        if now - last_move >= MOVE_DELAY:
            last_move = now
            hx, hy = snake[0]
            dx, dy = direction
            new_head = (hx + dx, hy + dy)

            if (
                new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
                new_head in snake
            ):
                return score

            snake.insert(0, new_head)

            if new_head == food:
                score += 1
                food = random_food(snake)
            else:
                snake.pop()

        # Draw
        screen.fill(BLACK)
        draw_top_bar(score, player_number)
        draw_grid()

        pygame.draw.circle(
            screen,
            BALL_RED,
            (
                food[0] * GRID_SIZE + GRID_SIZE // 2,
                food[1] * GRID_SIZE + GRID_SIZE // 2 + 60,
            ),
            GRID_SIZE // 2 - 2,
        )

        draw_snake(snake, direction)
        pygame.display.flip()

def show_winner(score1, score2):
    screen.fill(DARK_GREEN)

    if score1 > score2:
        result = f"{player1} Wins!"
        record_win(player1)
    elif score2 > score1:
        result = f"{player2} Wins!"
        record_win(player2)
    else:
        result = "It's a Draw!"

    title = big_font.render(result, True, WHITE)
    scores = font.render(f"{player1}: {score1}   {player2}: {score2}", True, WHITE)
    prompt = font.render("Press R to Restart or ESC to Quit", True, WHITE)

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 240))
    screen.blit(scores, (WIDTH // 2 - scores.get_width() // 2, 300))
    screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 340))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# -------------------- MAIN LOOP --------------------
while True:
    score1 = play_game(1)
    score2 = play_game(2)
    show_winner(score1, score2)

