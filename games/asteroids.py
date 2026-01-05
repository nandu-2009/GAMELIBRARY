import pygame
import random
import sys
from game_db import record_win, get_players

player1, player2 = get_players()

pygame.init()

# ---------------- CONSTANTS ----------------
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_SPEED = 7
BULLET_SPEED = 10
STAR_COUNT = 100

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

# ---------------- CLASSES ----------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50,40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT-50))
        self.speed = PLAYER_SPEED
        self.health = 100
        self.max_health = 100
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 250

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)


def show_player_transition(player_num):
    screen.fill(BLACK)

    title = big_font.render(f"PLAYER {player_num}", True, WHITE)
    msg = font.render("Get Ready!", True, YELLOW)
    inst = font.render("Press ANY KEY to Start", True, WHITE)

    screen.blit(title, (WIDTH//2 - title.get_width()//2, 220))
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, 280))
    screen.blit(inst, (WIDTH//2 - inst.get_width()//2, 340))

    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40,40))
        self.image.fill(RED)
        self.rect = self.image.get_rect(
            center=(random.randint(40, WIDTH-40), -40)
        )
        self.speed = random.randint(2,4)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5,15))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(x,y))

    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()

class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.randint(1,3)

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), 2)

# ---------------- UI FUNCTIONS ----------------
def draw_health_bar(surface, x, y, health, max_health):
    fill = (health / max_health) * 100
    pygame.draw.rect(surface, GREEN, (x, y, fill, 10))
    pygame.draw.rect(surface, WHITE, (x, y, 100, 10), 2)

def show_start_screen():
    screen.fill(BLACK)

    title = big_font.render("SPACE SHOOTER", True, WHITE)
    rules1 = font.render("Arrow Keys  -  Move", True, WHITE)
    rules2 = font.render("SPACE       -  Shoot", True, WHITE)
    rules3 = font.render("2 Players take turns", True, WHITE)
    rules4 = font.render("Higher score wins", True, WHITE)
    start = font.render("Press ANY KEY to Start", True, YELLOW)

    screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))
    screen.blit(rules1, (WIDTH//2 - rules1.get_width()//2, 260))
    screen.blit(rules2, (WIDTH//2 - rules2.get_width()//2, 300))
    screen.blit(rules3, (WIDTH//2 - rules3.get_width()//2, 340))
    screen.blit(rules4, (WIDTH//2 - rules4.get_width()//2, 380))
    screen.blit(start, (WIDTH//2 - start.get_width()//2, 460))

    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# ---------------- GAME SETUP ----------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter - 2 Player")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

stars = [Star() for _ in range(STAR_COUNT)]

def reset_round():
    global all_sprites, enemies, bullets, player, score
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    score = 0

# ---------------- GAME STATE ----------------
current_player = 1
score = 0
score_p1 = 0
score_p2 = 0
game_over = False

reset_round()
show_start_screen()

# ---------------- MAIN LOOP ----------------
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player.shoot()
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r and game_over:
                current_player = 1
                score_p1 = score_p2 = 0
                game_over = False
                reset_round()

    if not game_over:
        all_sprites.update()
        for star in stars:
            star.update()

        if random.randint(1, 80) == 1:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        score += len(hits) * 10

        hits = pygame.sprite.spritecollide(player, enemies, True)
        for hit in hits:
            player.health -= 20
            if player.health <= 0:
                if current_player == 1:
                    score_p1 = score
                    current_player = 2
                    reset_round()
                    show_player_transition(2)
                else:
                    score_p2 = score
                    game_over = True

    # ---------------- DRAW ----------------
    screen.fill(BLACK)
    for star in stars:
        star.draw(screen)

    all_sprites.draw(screen)

    if not game_over:
        draw_health_bar(screen, 10, 10, player.health, player.max_health)
        screen.blit(font.render(f"Score: {score}", True, WHITE), (650, 10))
        screen.blit(font.render(f"Player {current_player}", True, WHITE), (10, 30))
    else:
        title = big_font.render("GAME OVER", True, RED)
        p1 = font.render(f"Player 1 Score: {score_p1}", True, WHITE)
        p2 = font.render(f"Player 2 Score: {score_p2}", True, WHITE)

        if score_p1 > score_p2:
            winner = "Player 1 Wins!"
            record_win(player1)
        elif score_p2 > score_p1:
            winner = "Player 2 Wins!"
            record_win(player2)
        else:
            winner = "It's a Tie!"

        win = font.render(winner, True, WHITE)
        restart = font.render("Press R to Restart", True, WHITE)

        screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))
        screen.blit(p1, (WIDTH//2 - p1.get_width()//2, 250))
        screen.blit(p2, (WIDTH//2 - p2.get_width()//2, 290))
        screen.blit(win, (WIDTH//2 - win.get_width()//2, 340))
        screen.blit(restart, (WIDTH//2 - restart.get_width()//2, 400))

    pygame.display.flip()

pygame.quit()
sys.exit()

