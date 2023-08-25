import logging
import pygame
import time
import sys

from src.grapher import Grapher
from src.constants import Constants
from src.sprite import Sprite
from src.saboteur import Saboteur
from src.karateka import Karateka
from src.factory import create_saboteur, create_karateka, create_kong

class SaboteurKarateka():

    def __init__(self):
        self.redraw = False
        self.walking = False        
        self.running = True
        self.grapher = Grapher()        
        self.sprites = [create_saboteur(), create_karateka(), create_kong()]


    def handle_keyboard(self):
        keys = pygame.key.get_pressed()
    
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        dp = keys[ord('p')] - keys[ord('o')]

        self.redraw = True

        if dx > 0:
            if not self.walking:
                self.walking = True
                self.sprites[0].step_right()
                self.sprites[1].step_right()
                
            else:
                self.walking = False
                #self.sprites[0].stand()
                #self.sprites[1].stand()
    
        if dy < 0 :
            self.sprites[0].kick()
            self.sprites[1].kick()
    
        if dp > 0 :
            self.sprites[0].punch()
            self.sprites[1].punch()

    def display(self):
        pygame.display.flip()
                
        time.sleep(0.005)
        if self.redraw:
            self.redraw = False
            self.grapher.draw_background()

        for sprite in self.sprites:    
            self.grapher.draw_sprite(sprite)

            
    def play_music(self):
        mp3_file = "src/resources/RobH.mp3"
        pygame.mixer.music.load(mp3_file)
        pygame.mixer.music.play(-1)


    def main(self):
        pygame.init()
        
        self.play_music()
        
        screen = pygame.display.set_mode((Constants.screen_width, Constants.screen_height))
        screen.fill(Constants.BACKGROUND_COLOR)
        
        self.grapher.draw_background()
    
        for sprite in self.sprites:    
            self.grapher.draw_sprite(sprite)
        
        clock = pygame.time.Clock()
        
        try:
            while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        pygame.mixer.music.stop()
                
                self.handle_keyboard()
                self.display()    
                
                clock.tick(20)
    
        except KeyboardInterrupt:
            pygame.mixer.music.stop()
            pygame.quit()


if __name__ == "__main__":
    SaboteurKarateka().main()
