import pygame

from src.main.utils import Utils

class Amiga:

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
    
    def draw_background(self):
        background_bitmap = Utils.load_background("src/main/resources/amiga.png")
        self.screen.blit(background_bitmap, (0, 0))
        pygame.display.flip()
        
        
    def run(self, duration_ms):
        start_time = pygame.time.get_ticks()
        self.draw_background()
        
        while pygame.time.get_ticks() - start_time <= duration_ms:        
            
            self.clock.tick(60)
        