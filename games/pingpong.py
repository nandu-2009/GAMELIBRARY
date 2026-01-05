import turtle
import time
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


# Create screen
screen = turtle.Screen()
screen.title("Pong Game")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)
screen.game_started = False

# Left paddle (Player 1)
left_paddle = turtle.Turtle()
left_paddle.speed(0)
left_paddle.shape("square")
left_paddle.color("white")
left_paddle.shapesize(stretch_wid=6, stretch_len=1)
left_paddle.penup()
left_paddle.goto(-350, 0)
left_paddle.hideturtle()

# Right paddle (Player 2)
right_paddle = turtle.Turtle()
right_paddle.speed(0)
right_paddle.shape("square")
right_paddle.color("white")
right_paddle.shapesize(stretch_wid=6, stretch_len=1)
right_paddle.penup()
right_paddle.goto(350, 0)
right_paddle.hideturtle()

# Ball
ball = turtle.Turtle()
ball.speed(40)
ball.shape("circle")
ball.color("red")
ball.penup()
ball.goto(0, 0)
ball.dx = 2
ball.dy = -2
ball.hideturtle()

# Score
score_p1 = 0
score_p2 = 0

# Display score
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)

# Start Screen / Rules
start_text = turtle.Turtle()
start_text.hideturtle()
start_text.penup()
start_text.color("white")

# Title
title = turtle.Turtle()
title.hideturtle()
title.penup()
title.color("#00ffcc")
title.goto(0, 220)
title.write("   P O N G   ", align="center", font=("Courier", 36, "bold"))

# Rules text
start_text.goto(0, 40)
start_text.write(
    "Player 1 :  W  /  S\nPlayer 2 :  ↑  /  ↓\n\n    First to 5 Wins",
    align="center",
    font=("Courier", 22, "bold")
)

# Press to start message
press_text = turtle.Turtle()
press_text.hideturtle()
press_text.penup()
press_text.color("#ffdd00")
press_text.goto(0, -80)
press_text.write(
    "Press SPACE to Start",
    align="center",
    font=("Courier", 24, "bold")
)

# Paddle movement
def left_paddle_up():
    y = left_paddle.ycor()
    if y < 250:
        left_paddle.sety(y + 20)

def left_paddle_down():
    y = left_paddle.ycor()
    if y > -240:
        left_paddle.sety(y - 20)

def right_paddle_up():
    y = right_paddle.ycor()
    if y < 250:
        right_paddle.sety(y + 20)

def right_paddle_down():
    y = right_paddle.ycor()
    if y > -240:
        right_paddle.sety(y - 20)

# Start game
def start_game():
    screen.game_started = True
    start_text.clear()
    title.clear()
    press_text.clear()

    left_paddle.showturtle()
    right_paddle.showturtle()
    ball.showturtle()

    score_display.write(
        f"Player 1: {score_p1}   Player 2: {score_p2}",
        align="center",
        font=("Courier", 24, "bold")
    )

def exit_game():
    screen.bye()

# Keyboard bindings
screen.listen()
screen.onkeypress(left_paddle_up, "w")
screen.onkeypress(left_paddle_down, "s")
screen.onkeypress(right_paddle_up, "Up")
screen.onkeypress(right_paddle_down, "Down")
screen.onkeypress(start_game, "space")

# Main game loop
while True:
    screen.update()

    if not screen.game_started:
        continue

    time.sleep(0.005)

    # Move ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Top & bottom collision
    if ball.ycor() > 290 or ball.ycor() < -290:
        ball.dy *= -1

    # Right wall
    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_p1 += 1
        score_display.clear()
        score_display.write(
            f"Player 1: {score_p1}   Player 2: {score_p2}",
            align="center",
            font=("Courier", 24, "bold")
        )

    # Left wall
    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_p2 += 1
        score_display.clear()
        score_display.write(
            f"Player 1: {score_p1}   Player 2: {score_p2}",
            align="center",
            font=("Courier", 24, "bold")
        )

    # Paddle collision
    if (350 > ball.xcor() > 340) and (right_paddle.ycor() + 50 > ball.ycor() > right_paddle.ycor() - 50):
        ball.dx *= -1

    if (-350 < ball.xcor() < -340) and (left_paddle.ycor() + 50 > ball.ycor() > left_paddle.ycor() - 50):
        ball.dx *= -1

    # Win condition
    if score_p1 == 5 or score_p2 == 5:
        if score_p1 == 5:
            record_win(player1)
        else:
            record_win(player2)
        score_display.clear()
        winner = "Player 1" if score_p1 == 5 else "Player 2"
        score_display.goto(0, 0)
        score_display.write(
            f"{winner} Wins!",
            align="center",
            font=("Courier", 40, "bold")
        )
        score_display.goto(0, -40)
        score_display.write(
            "Press SPACE to Exit",
            align="center",
            font=("Courier", 24, "bold")
        )
        screen.onkeypress(exit_game, "space")
        break

