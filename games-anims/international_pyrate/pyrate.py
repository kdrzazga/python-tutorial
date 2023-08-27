import time

import pygame
from lib.balls import BallsHelper
from lib.info import info

from drawer import Drawer
from player import Player


def main():
    pygame.init()
    screen = pygame.display.set_mode((BallsHelper.screen_width, BallsHelper.screen_height))

    clock = pygame.time.Clock()

    mp3_file = "resources/RobH.mp3"
    pygame.mixer.music.load(mp3_file)
    pygame.mixer.music.play(-1)  # -1: infinite loop

    running = True
    screen.fill(BallsHelper.BACKGROUND_COLOR)  # Clear the screen
    drawer = Drawer()
    player = Player()
    drawer.draw_sprite(player)
    drawer.draw_background()
    info(screen)

    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.mixer.music.stop()

            if len(BallsHelper.balls) < BallsHelper.BALL_COUNT:  # Create fewer balls
                BallsHelper.create_ball()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[ord('a')]:
                player.set_direction('left')
            elif keys[pygame.K_RIGHT] or keys[ord('d')]:
                player.set_direction('right')
            elif keys[ord('q')]:
                player.set_direction('top left')
            elif keys[ord('e')]:
                player.set_direction('top right')

            BallsHelper.draw_balls(screen)
            pygame.display.flip()  # Update the screen

            time.sleep(0.005)
            BallsHelper.clear_balls(screen)
            drawer.clear_sprite()
            drawer.draw_sprite(player)

            for ball in BallsHelper.balls:
                roll_speed = -3 if ball.id % 3 == 0 else 3
                if ball.index < len(ball.trajectory):
                    x, ball.y = ball.trajectory[ball.index]
                    ball.x = BallsHelper.screen_width - x if ball.id % 3 == 0 else x
                    ball.index += 1
                else:
                    if not ball.rolling:
                        ball.rolling = True
                        ball.trajectory = [(ball.x, ball.y)]
                    else:
                        ball.x += roll_speed

                        if ball.x >= BallsHelper.screen_width + BallsHelper.ball_diameter or ball.x < 0:
                            BallsHelper.balls.remove(ball)

            clock.tick(140)

    except KeyboardInterrupt:
        pygame.mixer.music.stop()
        pygame.quit()


if __name__ == "__main__":
    main()
