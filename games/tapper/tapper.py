import logging
import pygame
import time
import sys

#from balls import BallsHelper, Ball
#from info import info
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
    drawer = Drawer()
    player = Player()
    drawer.draw_sprite(player)
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
                player.move_up()
            elif keys[pygame.K_DOWN] or keys[ord('s')]:
                player.move_down()
            elif keys[pygame.K_LEFT] or keys[ord('a')]:
                player.move_left()
 #           
 #           BallsHelper.draw_balls(screen)
 #           pygame.display.flip()  # Update the screen
 #           
 #           time.sleep(0.005)
 #           BallsHelper.clear_balls(screen)
 #           drawer.clear_sprite()
            drawer.draw_sprite(player)           

            clock.tick(4)  # Limit the frame rate to 60 FPS

    except KeyboardInterrupt:
        pygame.mixer.music.stop()
        pygame.quit()

if __name__ == "__main__":
    main()