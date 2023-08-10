import logging
import pygame
import sys

from scrolling import scroll
from drawer import Drawer
from player import Player
from balls import BallsHelper # ,init_balls

log_level = logging.INFO
if len(sys.argv) > 1 and (sys.argv[1] == "--debug" or sys.argv[1] == "-d"):
    log_level = logging.DEBUG
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
icon = pygame.image.load("resources/c64.ico")
pygame.display.set_icon(icon)

mp3_file = "resources/RobH.mp3"
pygame.mixer.music.load(mp3_file)
pygame.mixer.music.play(-1)  # -1: infinite loop

drawer = Drawer()
player = Player()
drawer.draw_sprite(player)

clock = pygame.time.Clock()
drawer.draw_background()
#init_balls()

running = True

try:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.mixer.music.stop()
                pygame.quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[ord('a')]:
            player.set_direction('left')
        elif keys[pygame.K_RIGHT] or keys[ord('d')]:
            player.set_direction('right')
        elif keys[ord('q')]:
            player.set_direction('top left')
        elif keys[ord('e')]:
            player.set_direction('top right')

        BallsHelper.clear_balls(drawer.window)
        BallsHelper.draw_balls(drawer.window)
        drawer.clear_sprite()
        drawer.draw_sprite(player)
        pygame.display.update()
        scroll(drawer.window)
        clock.tick(40)

except KeyboardInterrupt:
    pygame.mixer.music.stop()
    pygame.quit()
