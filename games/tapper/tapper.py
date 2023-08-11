import logging
import pygame
import time
import sys

#from balls import BallsHelper, Ball
from board import Board
from bartender import Player
from drawer import Drawer

def main():

    pygame.init()
    screen = pygame.display.set_mode((Drawer.width, Drawer.window_height))
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    clock = pygame.time.Clock()

    mp3_file = "resources/os.mid"
    pygame.mixer.music.load(mp3_file)
    pygame.mixer.music.play(-1)  # -1: infinite loop

    running = True
    screen.fill((0,0,0))  # Clear the screen
    
    board = Board()
    drawer = Drawer(board.player)
    drawer.draw_sprite(board.player)
    drawer.draw_background()
    #info(screen)

    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.mixer.music.stop()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] or keys[ord('w')]:
                drawer.clear_bartender(board.player)
                board.move_player_up()
                drawer.draw_sprite(board.player)
            elif keys[pygame.K_DOWN] or keys[ord('s')]:
                drawer.clear_bartender(board.player)
                board.move_player_down()
                drawer.draw_sprite(board.player)
            elif keys[pygame.K_LEFT] or keys[ord('a')]:
                drawer.clear_bartender(board.player)
                board.move_player_left()
                drawer.draw_sprite(board.player)
            elif keys[pygame.K_RIGHT] or keys[ord('d')]:
                drawer.clear_bartender(board.player)
                board.move_player_right()
                drawer.draw_sprite(board.player)
 #           
 #           BallsHelper.draw_balls(screen)
 #           pygame.display.flip()  # Update the screen #           
 #           time.sleep(0.005)
 #           BallsHelper.clear_balls(screen)
 #           drawer.clear_sprite()
            drawer.draw_sprite(board.player)           

            clock.tick(4)  # Limit the frame rate to 60 FPS

    except KeyboardInterrupt:
        pygame.mixer.music.stop()
        pygame.quit()

if __name__ == "__main__":
    main()