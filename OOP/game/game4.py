import pygame


# -----------------------
# GAME CONSTANTS
# -----------------------
WIDTH = 800
HEIGHT = 600

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 6

BALL_SIZE = 20
BALL_SPEED = 5

FONT_SIZE = 36


# ------------------------------------------------------------
# ENTITY CLASS
# ------------------------------------------------------------

class Entity:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)


# ------------------------------------------------------------
# PADDLE CLASS
# ------------------------------------------------------------

class Paddle(Entity):
    def __init__(self, x, y_center):
        y = y_center - PADDLE_HEIGHT // 2
        super().__init__(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED

    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed

    def move_down(self):
        if self.rect.bottom < HEIGHT:
            self.rect.y += self.speed


# ------------------------------------------------------------
# HUMAN PADDLE CLASS
# ------------------------------------------------------------

class HumanPaddle(Paddle):
    def __init__(self, x, y_center, up_key, down_key):
        super().__init__(x, y_center)
        self.up_key = up_key
        self.down_key = down_key

    def update(self, keys):
        if keys[self.up_key]:
            self.move_up()
        if keys[self.down_key]:
            self.move_down()


# ------------------------------------------------------------
# AI PADDLE CLASS
# ------------------------------------------------------------

class AIPaddle(Paddle):
    def update(self, ball):
        if ball.rect.centery < self.rect.centery:
            self.move_up()
        elif ball.rect.centery > self.rect.centery:
            self.move_down()


# ------------------------------------------------------------
# BALL CLASS
# ------------------------------------------------------------

class Ball(Entity):
    def __init__(self):
        x = WIDTH // 2 - BALL_SIZE // 2
        y = HEIGHT // 2 - BALL_SIZE // 2
        super().__init__(x, y, BALL_SIZE, BALL_SIZE)
        self.dx = BALL_SPEED
        self.dy = BALL_SPEED

    def draw(self, screen):
        pygame.draw.ellipse(screen, (255, 255, 255), self.rect)

    def reset(self, direction):
        x = WIDTH // 2 - BALL_SIZE // 2
        y = HEIGHT // 2 - BALL_SIZE // 2
        self.rect.x = x
        self.rect.y = y
        self.dx = BALL_SPEED * direction
        self.dy = BALL_SPEED

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.bounce_y()

    def bounce_x(self):
        self.dx = -self.dx

    def bounce_y(self):
        self.dy = -self.dy


# ------------------------------------------------------------
# GAME CLASS
# ------------------------------------------------------------

class PongGame:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong Engine Style")
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.clock = pygame.time.Clock()

        self.left_paddle = HumanPaddle(30, HEIGHT // 2, pygame.K_w, pygame.K_s)
        self.right_paddle = AIPaddle(WIDTH - 40, HEIGHT // 2)
        self.ball = Ball()

        self.entities = [self.left_paddle, self.right_paddle, self.ball]

        self.left_score = 0
        self.right_score = 0

    def handle_collisions(self):
        if self.ball.rect.colliderect(self.left_paddle.rect):
            self.ball.bounce_x()
        if self.ball.rect.colliderect(self.right_paddle.rect):
            self.ball.bounce_x()

    def handle_score(self):
        if self.ball.rect.left <= 0:
            self.right_score += 1
            self.ball.reset(direction=1)
        elif self.ball.rect.right >= WIDTH:
            self.left_score += 1
            self.ball.reset(direction=-1)

    def update(self):
        keys = pygame.key.get_pressed()

        self.left_paddle.update(keys)
        self.right_paddle.update(self.ball)
        self.ball.update()

        self.handle_collisions()
        self.handle_score()

    def draw(self):
        self.screen.fill((0, 0, 0))

        for entity in self.entities:
            entity.draw(self.screen)

        pygame.draw.aaline(self.screen, (255, 255, 255), (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        score_text = self.font.render(f"{self.left_score}     {self.right_score}", True, (255, 255, 255))
        self.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

        pygame.display.flip()

    def run(self):
        print("Player: W (up), S (down)")
        print("Right paddle: AI")
        print("Press ESC to quit.")

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False

            self.update()
            self.draw()

            self.clock.tick(60)

        pygame.quit()


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":
    game = PongGame()
    game.run()