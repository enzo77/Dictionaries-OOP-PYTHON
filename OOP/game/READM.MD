```mermaid
classDiagram
    class Paddle {
        - pygame.Rect rect
        - int speed
        + move_up()
        + move_down()
    }
    class Ball {
        - pygame.Rect rect
        - int dx
        - int dy
        + update()
        + bounce_x()
        + bounce_y()
        + reset()
    }
    class PongGame {
        - Paddle paddle1
        - Paddle paddle2
        - Ball ball
        - int score1
        - int score2
        + reset_game()
        + update_paddles(keys)
        + handle_collisions()
        + update_ball()
        + draw_scene(screen, font)
    }
    Paddle <|-- PongGame : has
    Ball <|-- PongGame : has

    ```