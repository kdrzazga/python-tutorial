import pygame
import sys

from src.cube import CubeRotation
from src.cloud_fog import CloudEffectApp
from src.rings import Animation
from src.lib import ClearScreen

class Demo:

    def __init__(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def phase1(self):
        print("PHASE 1")
        outer_text = "ORTER   "
        inner_text = "  46 ERODOMMOC"
        app = Animation(self.screen, outer_text, inner_text)
        app.run()
    
    def phase2(self):
        print("PHASE 2")
        app = CubeRotation(self.screen)
        app.run()

    def phase3(self):
        print("PHASE 3")
        cloud_effect = CloudEffectApp(self.screen)
        cloud_effect.run()

    def run(self):
        pygame.init()
        
        self.phase1()
        ClearScreen.tile_screen(self.screen, (255, 255, 255))
        self.phase2()
        ClearScreen.tile_screen(self.screen, (255, 255, 255))
        self.phase3()
        ClearScreen.tile_screen(self.screen, (255, 255, 255))        
        print("BYE !")
        
        pygame.quit()

if __name__ == "__main__":
   
    Demo().run()
