import pygame
from constants import HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED


# ------------------------------------------------------------
# PADDLE CLASS
# ------------------------------------------------------------

class Paddle:
    def __init__(self, x, y_center):
        y = y_center - PADDLE_HEIGHT // 2
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED

    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed

    def move_down(self):
        if self.rect.bottom < HEIGHT:
            self.rect.y += self.speed