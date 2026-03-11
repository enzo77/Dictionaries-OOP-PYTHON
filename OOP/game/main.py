import pygame
from constants import WIDTH, HEIGHT, FONT_SIZE
from game import PongGame


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
        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
        if keys[pygame.K_SPACE]:
            game.reset_game()

        # Logic
        game.update_paddles(keys)
        game.update_ball()

        # Render
        game.draw_scene(screen, font)

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()