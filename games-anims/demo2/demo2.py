import logging
import pygame
import sys

from src.main.amiga import Amiga
from src.main.c64 import C64

class Demo:

    def __init__(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.c64 = C64(self.screen)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
    def phase1(self):
        print("phase 1")
        self.c64.handle_cursor(35)
        for line in ("LOAD", " ", "PRESS PLAY ON TAPE"):
            self.c64.writeline(line)
        
        self.c64.toggle_screen(25)
        
        for line in ("LOADING", "READY", "RUN"):
            self.c64.writeline(line)
        
        self.c64.draw_sprite()
        pygame.time.delay(1000)
        self.c64.walk_karateka1(5000)
        self.c64.open_passage(2500)

        
    def phase2(self):
        print("phase 2")

        
    def phase3(self):
        print("phase 3")
        a = Amiga(self.screen)
        a.draw(2500)
        a.dropping(6500)
        pygame.time.delay(4000)


    def phase4(self):
        print("phase 4")


    def run(self):
        pygame.init()
        
        self.phase1()
        self.phase2()
        self.phase3()        
        self.phase4()        
        print("BYE !")
        
        pygame.quit()

if __name__ == "__main__":
   
    Demo().run()