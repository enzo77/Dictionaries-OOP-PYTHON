import pygame
from constants import WIDTH, HEIGHT
from paddle import Paddle
from ball import Ball


# ------------------------------------------------------------
# GAME CLASS
# ------------------------------------------------------------

class PongGame:
    def __init__(self):
        self.paddle1 = Paddle(30, HEIGHT // 2)
        self.paddle2 = Paddle(WIDTH - 40, HEIGHT // 2)
        self.ball = Ball()
        self.score1 = 0
        self.score2 = 0

    def reset_game(self):
        self.paddle1 = Paddle(30, HEIGHT // 2)
        self.paddle2 = Paddle(WIDTH - 40, HEIGHT // 2)
        self.ball = Ball()
        self.score1 = 0
        self.score2 = 0

    def update_paddles(self, keys):
        if keys[pygame.K_w]:
            self.paddle1.move_up()
        if keys[pygame.K_s]:
            self.paddle1.move_down()
        if keys[pygame.K_UP]:
            self.paddle2.move_up()
        if keys[pygame.K_DOWN]:
            self.paddle2.move_down()

    def handle_collisions(self):
        if self.ball.rect.colliderect(self.paddle1.rect):
            self.ball.bounce_x()
        if self.ball.rect.colliderect(self.paddle2.rect):
            self.ball.bounce_x()

    def update_ball(self):
        self.ball.update()

        self.handle_collisions()

        rect_ball = self.ball.rect
        if rect_ball.left <= 0:
            self.score2 += 1
            self.ball.reset()
        elif rect_ball.right >= WIDTH:
            self.score1 += 1
            self.ball.reset()

    def draw_scene(self, screen, font):
        # Background color
        screen.fill((0, 0, 0))

        # Players
        pygame.draw.rect(screen, (255, 255, 255), self.paddle1.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.paddle2.rect)

        # Ball
        pygame.draw.ellipse(screen, (255, 255, 255), self.ball.rect)

        # GUI
        pygame.draw.aaline(screen, (255, 255, 255), (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
        score_text = font.render(f"{self.score1}     {self.score2}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

        # Updates the full display surface to the screen
        pygame.display.flip()