import logging
import pygame
import time
import sys

from src.grapher import Grapher
from src.constants import Constants
from src.sprite import Sprite
from src.saboteur import Saboteur
from src.karateka import Karateka
from src.factory import create_saboteur, create_karateka

def main():
    pygame.init()
    screen = pygame.display.set_mode((Constants.screen_width, Constants.screen_height))

    clock = pygame.time.Clock()

    mp3_file = "src/resources/RobH.mp3"
    pygame.mixer.music.load(mp3_file)
    pygame.mixer.music.play(-1)

    running = True
    screen.fill(Constants.BACKGROUND_COLOR)
    grapher = Grapher()
    sprites = [create_saboteur(), create_karateka()]
    
    grapher.draw_background()

    for sprite in sprites:    
        grapher.draw_sprite(sprite)
    
    redraw = False
    walking = False
    
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.mixer.music.stop()
        
            keys = pygame.key.get_pressed()
        
            dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 3.5
            dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 3.5

            redraw = True
 
            if dx > 0:
                if not walking:
                    walking = True
                    sprites[0].step_right()
                    sprites[1].step_right()
                    
                else:
                    walking = False
                    #sprites[0].stand()
                    #sprites[1].stand()
        
            pygame.display.flip()
            
            time.sleep(0.005)
            if redraw:
                redraw = False
                grapher.draw_background()

            for sprite in sprites:    
                grapher.draw_sprite(sprite)

            clock.tick(20)

    except KeyboardInterrupt:
        pygame.mixer.music.stop()
        pygame.quit()


if __name__ == "__main__":
    main()
