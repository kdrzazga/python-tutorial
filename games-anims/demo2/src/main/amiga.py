import pygame

from src.main.utils import Utils

class Amiga:

    def __init__(self, screen):
        self.screen = screen
        
        self.h = 70        
        self.background_bitmap = Utils.load_background("src/main/resources/amiga.png")
        self.window_bitmap = pygame.image.load("src/main/resources/window2.png")
        self.superfrog_bitmap = pygame.image.load("src/main/resources/sf.png")
        
        self.clock = pygame.time.Clock()
        
    
    def draw_background(self):
        self.screen.blit(self.background_bitmap, (0, 0))
        pygame.display.flip()
        

    def draw_window(self):
        self.screen.blit(self.window_bitmap, (60, self.h))
        pygame.display.flip()


    def draw_superfrog(self):
        self.screen.blit(self.superfrog_bitmap, (91, self.h + 27))
        pygame.display.flip()


    def draw(self, duration_ms):
        start_time = pygame.time.get_ticks()
        self.draw_background()
        self.draw_window()
        self.draw_superfrog()

        while pygame.time.get_ticks() - start_time <= duration_ms:
            pass


    def dropping(self, duration_ms):
        start_time = pygame.time.get_ticks()
        acceleration = 0
        while pygame.time.get_ticks() - start_time <= duration_ms:        
            self.draw_background()
            self.draw_window()
            self.draw_superfrog()
            acceleration += 0.3
            self.h += int(1 + acceleration)
            
            if self.window_hit_bottom():
                break
            
            self.clock.tick(36)

    
    def window_on_bottom(self, duration_ms):
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time <= duration_ms: 
        
            self.clock.tick(60)

    
    def activate_superfrog(self, duration_ms):
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time <= duration_ms: 
        
            self.clock.tick(60)


    def window_hit_bottom(self):
        wh = self.window_bitmap.get_height()
        bh = self.background_bitmap.get_height()
        
        print("self.h, self.h, bh = ", self.h, wh, bh)
        
        return wh + self.h > bh