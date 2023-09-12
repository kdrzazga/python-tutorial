import logging
import pygame

from src.main.utils import Utils, Constants
from src.main.computer import Computer

class Amiga(Computer):

    def __init__(self, screen):
        super().__init__(Constants.AMIGA_BLUE, Constants.BLUE)
        self.screen = screen
        
        self.h = 70        
        self.background_bitmap = Utils.load_background("src/main/resources/amiga.png")
        self.window_bitmap = pygame.image.load("src/main/resources/window2.png")
        self.window_x = 160-3
        self.superfrog_icon_bitmap = pygame.image.load("src/main/resources/sf.png")
        self.superfrog_jump_bitmap = pygame.image.load("src/main/resources/sf-jump.png")
        self.superfrog_stand_bitmap = pygame.image.load("src/main/resources/sf-stand.png")
        
    
    def draw_background(self):
        self.screen.blit(self.background_bitmap, (0, 0))
        pygame.display.flip()
        

    def draw_window(self):
        self.screen.blit(self.window_bitmap, (self.window_x, self.h))
        pygame.display.flip()


    def draw_superfrog_icon(self):
        self.screen.blit(self.superfrog_icon_bitmap, (191-3, self.h + 27))
        pygame.display.flip()


    def draw(self, duration_ms):
        start_time = pygame.time.get_ticks()
        self.draw_background()
        self.draw_window()
        self.draw_superfrog_icon()

        while pygame.time.get_ticks() - start_time <= duration_ms:
            pass


    def dropping(self, duration_ms):
        start_time = pygame.time.get_ticks()
        acceleration = 0
        while pygame.time.get_ticks() - start_time <= duration_ms:        
            self.draw_background()
            self.draw_sprite(self.karateka)
            self.draw_sprite(self.karateka4)
            self.draw_window()
            self.draw_superfrog_icon()
            if pygame.time.get_ticks() - start_time <= duration_ms - 500:
                self.question_mark()
            acceleration += 0.3
            self.h += int(1 + acceleration)
            
            if self.window_hit_bottom():
                break
            
            self.clock.tick(36)

    
    def activate_superfrog(self, duration_ms):
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time <= duration_ms: 
            #TODO
            self.clock.tick(60)


    def window_hit_bottom(self):
        wh = self.window_bitmap.get_height()
        bh = self.background_bitmap.get_height()
        
        logging.info("self.h = %d, window height = %d, bitmap height =  %d", self.h, wh, bh)
        
        return wh + self.h > bh - 22

        
    def get_catwalk_rect(self):
        x = -10 
        y = self.background_bitmap.get_height() - 88
        width = self.window_x + 3
        height = 88
        
        return pygame.Rect(x, y, width, height)
