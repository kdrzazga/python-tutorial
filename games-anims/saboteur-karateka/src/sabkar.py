import logging
import pygame
import time
import sys

from src.grapher import Grapher
from src.constants import Constants
from src.sprite import Sprite
from src.saboteur import Saboteur
from src.karateka import Karateka
from src.factory import create_saboteur, create_karateka, create_kong, create_barrel

class SaboteurKarateka():

    def __init__(self, screen):
        self.screen = screen
        self.redraw = False
        self.walking = False        
        self.running = True
        self.grapher = Grapher()        
        self.sprites = [create_saboteur(), create_karateka(), create_kong(), create_barrel()]
        
        for info_line in self.info():
            print(info_line)

    def animate(self):
        self.sprites[3].move()
        if self.sprites[3].y > Constants.screen_height or self.sprites[3].x < 0:
            self.sprites[3] = create_barrel() #creating new object to reset
            self.sprites[2].turn_right()

    def handle_keyboard(self):
        keys = pygame.key.get_pressed()
    
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        dp = keys[ord('p')] - keys[ord('o')]
        ddonkey = keys[ord('k')] - keys[ord('l')]

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
            
        if ddonkey > 0:
            self.sprites[2].turn_left()
            self.sprites[3].activate()
            
        elif ddonkey < 0:
            self.sprites[2].turn_right()
            

    def display(self):                
        time.sleep(0.005)
        if self.redraw:
            self.redraw = False
            self.grapher.draw_background()

        for sprite in self.sprites:    
            self.grapher.draw_sprite(sprite)
        
        pygame.display.flip()

            
    def play_music(self):
        mp3_file = "src/resources/RobH.mp3"
        pygame.mixer.music.load(mp3_file)
        pygame.mixer.music.play(-1)


    def main(self):
        self.play_music()
        self.screen.fill(Constants.BACKGROUND_COLOR)
        
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
                
                self.animate()                
                self.handle_keyboard()
                self.display()    
                
                clock.tick(Constants.fps)
    
        except KeyboardInterrupt:
            pygame.mixer.music.stop()


    def info(self):
        return ["left keys - moving sprites", "p - punch", "k l - donkey kong control"]

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((Constants.screen_width, Constants.screen_height))
    SaboteurKarateka(screen).main()    
    pygame.quit()