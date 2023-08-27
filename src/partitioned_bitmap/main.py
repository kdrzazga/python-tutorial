import time

import pygame


class Main:

    def __init__(self, screen):
        self.bitmap_image = pygame.image.load("forest.png")
        self.screen = screen
        
    def draw_background(self):        
        self.screen.blit(self.bitmap_image, (0, 0))
        pygame.display.flip()
        print("Loaded background...")
        time.sleep(1)
