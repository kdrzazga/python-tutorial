import pygame
import time

class Computer:
    
    def __init__(self):
        self.clock = pygame.time.Clock()
        

    def wait(self, duration_ms):
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time <= duration_ms: 
        
            self.clock.tick(60)
