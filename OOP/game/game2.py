import pygame


# -----------------------
# GAME CONSTANTS
# 1.- uml de game
# 2.- game2 distribuido en varios ficheros (una clase por módulo)
# 3.- cambios sobre pong2: colores, dirección inicial ball aleatoria, objeto dinámico en medio
# 4.- juego: Catch the Falling Objects
# Implement a small game where objects fall from the top of the screen.
# The player controls a basket that moves horizontally and must catch the objects.
# 5.- juego: Atari Outlaw, https://www.youtube.com/watch?v=KaaM4SUFrR4
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
# PADDLE CLASS
# ------------------------------------------------------------

class Paddle:
    def __init__(self, x, y_center):
        y = y_center - PADDLE_HEIGHT//2
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED

    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed

    def move_down(self):
        if self.rect.bottom < HEIGHT:
            self.rect.y += self.speed


# ------------------------------------------------------------
# BALL CLASS
# ------------------------------------------------------------

class Ball:
    def __init__(self):
        cx = WIDTH//2 - BALL_SIZE//2
        cy = HEIGHT//2 - BALL_SIZE//2
        self.rect = pygame.Rect(cx, cy, BALL_SIZE, BALL_SIZE)
        self.dx = BALL_SPEED
        self.dy = BALL_SPEED
    
    def reset(self):
        cx = WIDTH//2 - BALL_SIZE//2
        cy = HEIGHT//2 - BALL_SIZE//2
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
        #Background color
        screen.fill((0, 0, 0))
		
        #Players
        pygame.draw.rect(screen, (255, 255, 255), self.paddle1.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.paddle2.rect)
        
		#Ball
        pygame.draw.ellipse(screen, (255, 255, 255), self.ball.rect)
        
		#GUI
        pygame.draw.aaline(screen, (255, 255, 255), (WIDTH//2, 0), (WIDTH//2, HEIGHT))
        score_text = font.render(f"{self.score1}     {self.score2}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))
        
		#Updates the full display surface to the screen
        pygame.display.flip()


# ------------------------------------------------------------
# MAIN GAME LOOP
# ------------------------------------------------------------

def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("My 2nd Pong :)")
    font = pygame.font.SysFont(None, FONT_SIZE)
    clock = pygame.time.Clock()

    game = PongGame()

    print("Player 1: W (up), S (down)")
    print("Player 2: ↑ (up arrow), ↓ (down arrow)")
    print("Press SPACE to restart the match.")
    print("Press ESC to quit.")

    running = True

    while running:
        #Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
        if keys[pygame.K_SPACE]:
            game.reset_game()
        
        #Logic
        game.update_paddles(keys)
        game.update_ball()

        #Render
        game.draw_scene(screen, font)

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()