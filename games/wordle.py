import random
import pygame
pygame.init()
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


#function to open and read file
def load_dict(file_name):
    file = open(file_name)
    words = file.readlines()
    file.close()
    return [word[:5].upper() for word in words]

#choosing a word from the library
dict_guessing = load_dict("words.txt")
dict_answers = load_dict("answers.txt")
answer = random.choice(dict_answers)

#game state
input = ""
guesses_p1 = []
guesses_p2 = []
current_player = 1
winner = None
gameover = False

#layout
WIDTH = 900
HEIGHT = 700
margin = 10
t_margin = 130

square_size = 60
board_width = 5*square_size + 4*margin

#center boards
gap = 60
p1_x = WIDTH//2 - board_width - gap//2
p2_x = WIDTH//2 + gap//2

#colors
grey = (70,70,80)
green = (6,214,160)
yellow = (255,209,102)

#fonts
font = pygame.font.SysFont("arial", square_size, bold=True)
font_small = pygame.font.SysFont("arial", 24, bold=True)

pygame.display.set_caption("WORDLE - TWO PLAYER")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#letter colouring
def letter_colour(guess, j):
    letter = guess[j]

    if letter == answer[j]:
        return green

    answer_letters = list(answer)
    guess_letters = list(guess)

    for i in range(5):
        if guess_letters[i] == answer_letters[i]:
            answer_letters[i] = None
            guess_letters[i] = None

    used = 0
    for i in range(j):
        if guess_letters[i] == letter and letter in answer_letters:
            used += 1

    if used < answer_letters.count(letter):
        return yellow

    return grey

#draw board
def draw_board(guesses, start_x, active):
    y = t_margin
    for i in range(6):
        x = start_x
        for j in range(5):
            square = pygame.Rect(x, y, square_size, square_size)
            pygame.draw.rect(screen, grey, square, 2)

            if i < len(guesses):
                colour = letter_colour(guesses[i], j)
                pygame.draw.rect(screen, colour, square)
                letter = font.render(guesses[i][j], False, (255,255,255))
                screen.blit(letter, letter.get_rect(center=square.center))

            elif active and i == len(guesses) and j < len(input):
                letter = font.render(input[j], False, grey)
                screen.blit(letter, letter.get_rect(center=square.center))

            x += square_size + margin
        y += square_size + margin

#main loop
animating = True
while animating:
    screen.fill("white")

    #titles
    p1 = font_small.render("PLAYER 1", False, grey)
    p2 = font_small.render("PLAYER 2", False, grey)
    screen.blit(p1, (p1_x + board_width//2 - p1.get_width()//2, 90))
    screen.blit(p2, (p2_x + board_width//2 - p2.get_width()//2, 90))

    turn = font_small.render(f"TURN: PLAYER {current_player}", False, grey)
    screen.blit(turn, (WIDTH//2 - turn.get_width()//2, 40))

    draw_board(guesses_p1, p1_x, current_player == 1)
    draw_board(guesses_p2, p2_x, current_player == 2)

    if gameover:
        if winner:
            msg = f"PLAYER {winner} WINS!"
        else:
            msg = "DRAW!"

        text = font_small.render(msg, False, grey)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT - 90))

        ans = font_small.render("ANSWER: " + answer, False, grey)
        screen.blit(ans, (WIDTH//2 - ans.get_width()//2, HEIGHT - 60))

        restart = font_small.render("PRESS R TO RESTART", False, grey)
        screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT - 30))

    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            animating = False

        elif event.type == pygame.KEYDOWN:

            if gameover and event.key == pygame.K_r:
                input = ""
                guesses_p1 = []
                guesses_p2 = []
                current_player = 1
                winner = None
                gameover = False
                answer = random.choice(dict_answers)

            elif not gameover:

                if event.key == pygame.K_BACKSPACE:
                    input = input[:-1]

                elif event.key == pygame.K_RETURN:
                    if len(input) == 5 and input in dict_guessing:

                        if current_player == 1:
                            guesses_p1.append(input)
                            if input == answer:
                                winner = 1
                                record_win(player1)
                                gameover = True
                            current_player = 2
                        else:
                            guesses_p2.append(input)
                            if input == answer:
                                winner = 2
                                record_win(player2)
                                gameover = True
                            current_player = 1

                        input = ""

                        if len(guesses_p1) == 6 and len(guesses_p2) == 6:
                            gameover = True

                elif len(input) < 5 and event.unicode.isalpha():
                    input += event.unicode.upper()

    pygame.display.flip()

pygame.quit()
