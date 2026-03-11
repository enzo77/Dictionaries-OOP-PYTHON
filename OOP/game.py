# ------------------------------------------------------------
# PROJECT 5 — PONG GAME
#
# 1) Paddle representation
#       (rect, speed)
#       rect  — pygame.Rect controlling position & size
#       speed — integer with vertical speed
# 2) Ball representation
#       (rect, dx, dy)
#       rect — pygame.Rect storing the current position
#       dx   — horizontal velocity
#       dy   — vertical velocity
# 3) Game full state
#       ball, paddle1, paddle2, score1, score2
# ------------------------------------------------------------


import pygame


# -----------------------
# GAME CONSTANTS
# -----------------------
WIDTH  = 800
HEIGHT = 600

PADDLE_WIDTH  = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED  = 6

BALL_SIZE = 20
BALL_SPEED = 5

FONT_SIZE = 36


# ------------------------------------------------------------
# CREATE GAME OBJECTS
# ------------------------------------------------------------

def make_paddle(x, y_center):
    rect = pygame.Rect(x, y_center - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    return (rect, PADDLE_SPEED)


def make_ball():
    rect = pygame.Rect(
        WIDTH // 2 - BALL_SIZE // 2,
        HEIGHT // 2 - BALL_SIZE // 2,
        BALL_SIZE, BALL_SIZE
    )
    dx = BALL_SPEED
    dy = BALL_SPEED
    return (rect, dx, dy)


def reset_game():
    paddle1 = make_paddle(30,  HEIGHT // 2)
    paddle2 = make_paddle(WIDTH - 40, HEIGHT // 2)
    ball = make_ball()
    score1 = 0
    score2 = 0
    return ball, paddle1, paddle2, score1, score2


# ------------------------------------------------------------
# UPDATE FUNCTIONS
# ------------------------------------------------------------

def update_paddles(paddle1, paddle2, keys):
    rect1, speed1 = paddle1
    rect2, speed2 = paddle2

    # Move paddle 1 (W/S)
    if keys[pygame.K_w] and rect1.top > 0:
        rect1.y -= speed1
    if keys[pygame.K_s] and rect1.bottom < HEIGHT:
        rect1.y += speed1

    # Move paddle 2 (Up/Down)
    if keys[pygame.K_UP] and rect2.top > 0:
        rect2.y -= speed2
    if keys[pygame.K_DOWN] and rect2.bottom < HEIGHT:
        rect2.y += speed2

    return (rect1, speed1), (rect2, speed2)


def update_ball(ball, paddle1, paddle2):
    rect, dx, dy = ball
    p1_rect = paddle1[0]
    p2_rect = paddle2[0]

    # Move the ball
    rect.x += dx
    rect.y += dy

    # Bounce top/bottom
    if rect.top <= 0 or rect.bottom >= HEIGHT:
        dy = -dy

    # Bounce on paddles
    if rect.colliderect(p1_rect) or rect.colliderect(p2_rect):
        dx = -dx

    return (rect, dx, dy)


# ------------------------------------------------------------
# DRAWING
# ------------------------------------------------------------

def draw_scene(screen, font, ball, paddle1, paddle2, score1, score2):
    rect_ball = ball[0]
    rect1 = paddle1[0]
    rect2 = paddle2[0]

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), rect1)
    pygame.draw.rect(screen, (255, 255, 255), rect2)
    pygame.draw.ellipse(screen, (255, 255, 255), rect_ball)
    pygame.draw.aaline(screen, (255, 255, 255), (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    score_text = font.render(f"{score1}     {score2}", True, (255, 255, 255))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))

    pygame.display.flip()


# ------------------------------------------------------------
# MAIN GAME LOOP
# ------------------------------------------------------------

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My 1st Pong :)")
font = pygame.font.SysFont(None, FONT_SIZE)
clock = pygame.time.Clock()

ball, paddle1, paddle2, score1, score2 = reset_game()

print("Player 1: W (up), S (down)")
print("Player 2: ↑ (up arrow), ↓ (down arrow)")
print("Press SPACE to restart the match.")
print("Press ESC to quit.")

running = True
while running:

    # Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        running = False

    if keys[pygame.K_SPACE]:
        ball, paddle1, paddle2, score1, score2 = reset_game()

    # Logic
    paddle1, paddle2 = update_paddles(paddle1, paddle2, keys)
    ball = update_ball(ball, paddle1, paddle2)

    rect_ball, dx, dy = ball
    if rect_ball.left <= 0:
        score2 += 1
        ball = make_ball()
    elif rect_ball.right >= WIDTH:
        score1 += 1
        ball = make_ball()

    # Output
    draw_scene(screen, font, ball, paddle1, paddle2, score1, score2)

    # 60 FPS
    clock.tick(60)

pygame.quit()
