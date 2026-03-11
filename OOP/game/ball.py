import pygame
from constants import WIDTH, HEIGHT, BALL_SIZE, BALL_SPEED


# ------------------------------------------------------------
# BALL CLASS
# ------------------------------------------------------------

class Ball:
    def __init__(self):
        cx = WIDTH // 2 - BALL_SIZE // 2
        cy = HEIGHT // 2 - BALL_SIZE // 2
        self.rect = pygame.Rect(cx, cy, BALL_SIZE, BALL_SIZE)
        self.dx = BALL_SPEED
        self.dy = BALL_SPEED

    def reset(self):
        cx = WIDTH // 2 - BALL_SIZE // 2
        cy = HEIGHT // 2 - BALL_SIZE // 2
        self.rect.center = (cx, cy)
        self.dx = BALL_SPEED
        self.dy = BALL_SPEED

    def update(self):
        # Move ball
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Bounce top/bottom
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.bounce_y()

    def bounce_x(self):
        self.dx = -self.dx

    def bounce_y(self):
        self.dy = -self.dy