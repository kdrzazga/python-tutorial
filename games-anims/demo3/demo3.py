import logging
import pygame
import time
import sys

from src.main.utils import Utils, Constants, ClearScreen
from src.main.c64 import C64

class Demo:

    def __init__(self, fullscreen=False):        
        self.screen = None
        self.computer = None
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        if fullscreen:
            self.screen = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF)
            pygame.mouse.set_pos((Constants.WIDTH - 1, Constants.HEIGHT - 1))
        else:
            self.screen = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT), pygame.DOUBLEBUF)

    def phase1(self):
        print("phase 1")
        self.computer = C64(self.screen)
        pygame.time.delay(2500)
        self.computer.handle_cursor(3500)
        for line, duration in (
                ("LOAD \"*\",8,1", 1000), (" ", 0), ("PRESS PLAY ON TAPE", 2000), ("OK", 200), (" ", 0), ("SEARCHING", 100)):
            self.computer.writeline(line)
            pygame.time.delay(duration)

        self.computer.toggle_screen(1500)    

    def run(self):

        self.phase1()
        print("BYE !")


if __name__ == "__main__":
    pygame.init()
    fullscreen = False

    if len(sys.argv) > 1:
        looped = 'loop' in sys.argv
        fullscreen = 'fullscreen' in sys.argv or 'fs' in sys.argv

        if looped:
            while True:
                Demo(fullscreen).run()

    Demo(fullscreen).run()

    pygame.quit()
