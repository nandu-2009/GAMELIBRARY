import turtle
import time
import sys
from game_db import record_win, get_players

player1, player2 = get_players()


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
PADDLE_SPEED = 10

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
ball.hideturtle()
BALL_SPEED_X = 3
BALL_SPEED_Y = 3
ball.dx = BALL_SPEED_X
ball.dy = BALL_SPEED_Y

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
    f"{player1} :  W / S\n{player2} :  ↑ / ↓\n\n   First to 5 Wins",
    align="center",
    font=("Courier", 22, "bold")
)

#Keys dictionary
keys = {
    "w": False,
    "s": False,
    "Up": False,
    "Down": False
}

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
        left_paddle.sety(y + PADDLE_SPEED)

def left_paddle_down():
    y = left_paddle.ycor()
    if y > -240:
        left_paddle.sety(y - PADDLE_SPEED)

def right_paddle_up():
    y = right_paddle.ycor()
    if y < 250:
        right_paddle.sety(y + PADDLE_SPEED)

def right_paddle_down():
    y = right_paddle.ycor()
    if y > -240:
        right_paddle.sety(y - PADDLE_SPEED)

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


def key_press(key):
    keys[key] = True

def key_release(key):
    keys[key] = False

screen.listen()
for key in keys:
    screen.onkeypress(lambda k=key: key_press(k), key)
    screen.onkeyrelease(lambda k=key: key_release(k), key)
screen.onkeypress(start_game, "space")


def exit_game():
    screen.bye()

# Main game loop
while True:
    screen.update()

    if not screen.game_started:
        continue

    time.sleep(0.01)

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

    # Right paddle collision
    if (
        ball.dx > 0 and
        ball.xcor() >= 330 and
        ball.xcor() <= 350 and
        abs(ball.ycor() - right_paddle.ycor()) <= 60
    ):
        ball.setx(330)          # push ball outside paddle
        ball.dx *= -1

    # Left paddle collision
    if (
        ball.dx < 0 and
        ball.xcor() <= -330 and
        ball.xcor() >= -350 and
        abs(ball.ycor() - left_paddle.ycor()) <= 60
    ):
        ball.setx(-330)         # push ball outside paddle
        ball.dx *= -1

    #On Pressing the key
    if screen.game_started:
        if keys["w"]:
            left_paddle_up()
        if keys["s"]:
            left_paddle_down()
        if keys["Up"]:
            right_paddle_up()
        if keys["Down"]:
            right_paddle_down()

    # Win condition
    if score_p1 == 5 or score_p2 == 5:
        if score_p1 == 5:
            record_win(player1)
        else:
            record_win(player2)
        score_display.clear()
        winner = player1 if score_p1 == 5 else player2
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
