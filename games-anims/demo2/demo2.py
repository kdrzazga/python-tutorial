import logging

import pygame
import sys

from src.main.bouncing_ball import BallAnimation
from src.main.factory import create_computer
from src.main.utils import Constants


class Demo:

    def __init__(self, fullscreen=False):
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = None
        
        if fullscreen:
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
            pygame.mouse.set_pos((self.WIDTH - 1, self.HEIGHT - 1))
        else:
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Ni Komodor Ni Amiga Demo")
        self.c64 = create_computer("C64", self.screen)
        self.amiga = create_computer("Amiga", self.screen)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def phase1(self):
        print("phase 1 - c64")
        self.c64.handle_cursor(3500)
        for line, duration in (
        ("LOAD", 1000), (" ", 0), ("PRESS PLAY ON TAPE", 2000), ("OK", 200), (" ", 0), ("SEARCHING", 100)):
            self.c64.writeline(line)
            pygame.time.delay(duration)

        self.c64.toggle_screen(1500)

        for line, duration in (("FOUND INTER.KARATE+", 500), ("LOADING", 350)):
            self.c64.writeline(line)
            pygame.time.delay(duration)

        self.c64.toggle_screen(4500)

        for line, duration in (("READY", 2000), ("RUN", 150)):
            self.c64.writeline(line)
            pygame.time.delay(duration)

        self.c64.play_ik_sound()
        self.c64.draw_karateka()
        pygame.time.delay(2200)
        self.c64.question_mark(False)
        pygame.time.delay(1000)

        self.c64.walk_karateka(1950)
        self.c64.question_mark(False)
        pygame.time.delay(1000)

        self.c64.karateka.step_left()
        self.c64.walk_karateka(1000)
        self.c64.question_mark(False)
        pygame.time.delay(1000)

        self.c64.karateka.step_right()
        self.c64.walk_karateka(4000)
        self.c64.clear_sprite()
        self.c64.punch(1000)
        self.c64.walk_karateka(1000, True)

    def phase2(self):
        print("phase 2 - bouncing ball")
        pygame.time.delay(1000)
        ball_animation = BallAnimation(self.screen, self.c64.get_catwalk_rect(), Constants.BLUE, 1200)
        ball_animation.bounce()

    def phase3(self):
        print("phase 3 - amiga")
        self.amiga.draw(25)
        self.amiga.draw_karateka()
        pygame.time.delay(500)

        self.amiga.walk_karateka(2400)
        self.amiga.question_mark(off=False)
        pygame.time.delay(1000)
        self.amiga.dropping(1200)
        self.amiga.kill_karateka()

    def phase4(self):
        print("phase 4 - yet another bouncing ball")
        ball_animation = BallAnimation(self.screen, self.amiga.get_catwalk_rect(), Constants.AMIGA_BLUE, 147)
        ball_animation.bounce()
        pygame.time.delay(4000)

    def phase5(self):
        print("phase 4 - superfrog arrives")

    def run(self):
        pygame.init()

        self.phase1()
        self.phase2()
        self.phase3()
        self.phase4()
        self.phase5()
        print("BYE !")

        pygame.quit()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 'loop':
            while True:
                Demo(True).run()
    else:
        Demo(fullscreen=False).run()
