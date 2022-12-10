import sys
from collections import deque

WIDTH = 640
HEIGHT = 240 * 2
PADDLE1 = Rect((20, 20), (15, 50))
PADDLE2 = Rect((WIDTH - 35, 20), (15, 50))
PADDLE_COLOR1 = deque([0, 200, 0])
PADDLE_COLOR2 = deque([0, 200, 0])
BLUE = 128, 128, 255

BALL_SERVE = (WIDTH / 2, HEIGHT / 2)
BALL = Rect(BALL_SERVE, (30, 30))
VELOCITY = [4, -3]
SCORE = [0, 0]

MODE = "play"


def draw():
    screen.fill((128, 0, 0))
    screen.draw.filled_rect(PADDLE1, PADDLE_COLOR1)
    screen.draw.filled_rect(PADDLE2, PADDLE_COLOR2)
    screen.draw.filled_rect(BALL, BLUE)
    screen.draw.text(
        f"{SCORE[0]} : {SCORE[1]}",
        ((WIDTH / 2) - 35, 20),
        color="pink",
        fontname="pix2",
        fontsize=64,
    )


def flash1():
    PADDLE_COLOR1.rotate(1)


def flash2():
    PADDLE_COLOR2.rotate(1)


def update_paddle(paddle, up, down):
    global MODE
    if MODE == "play":
        delta = 4

        if up and delta < paddle.y < HEIGHT:
            paddle.y -= delta
        if down and 0 < paddle.bottom < HEIGHT - delta:
            paddle.y += delta

    if MODE == "win":
        MODE = "won"
        if SCORE[0] > SCORE[1]:
            paddle_color = PADDLE_COLOR1
            clock.schedule_interval(flash1, 0.2)
        else:
            paddle_color = PADDLE_COLOR2
            clock.schedule_interval(flash2, 0.2)
        clock.schedule(sys.exit, 3)


def update_ball():
    if MODE == "play":
        if BALL.top <= 0:
            VELOCITY[1] = abs(VELOCITY[1])
            sounds.boing.play()

        if BALL.bottom >= HEIGHT:
            sounds.boing.play()
            VELOCITY[1] = -abs(VELOCITY[1])

        if BALL.left <= 0 or WIDTH <= BALL.right:
            sounds.yeah.play()
            BALL.center = BALL_SERVE
            VELOCITY[0] *= -1

        thwack(PADDLE1)
        thwack(PADDLE2)

        BALL.move_ip(VELOCITY)
    else:
        # game is over
        BALL.y = -100
        VELOCITY[:] = [0, 0]



def update_score():
    if MODE == "play":
        if BALL.left <= 0:
            SCORE[1] += 1
        if WIDTH <= BALL.right:
            SCORE[0] += 1


def update_win():
    global MODE
    if MODE == "play":
        if max(SCORE) >= 2:
            MODE = "win"


def thwack(paddle):
    if BALL.colliderect(paddle):
        sounds.thwack.play()
        VELOCITY[0] *= -1
        VELOCITY[1] = (BALL.centery - paddle.centery) / 6


def update():
    update_paddle(PADDLE1, keyboard.q, keyboard.a)
    update_paddle(PADDLE2, keyboard.p, keyboard.l)

    update_ball()

    update_score()

    update_win()
