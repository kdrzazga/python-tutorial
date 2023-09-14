import logging
import sys

import pygame

from src.main.bouncing_ball import BallAnimation
from src.main.factory import create_computer
from src.main.scroll import Scroll
from src.main.utils import Utils, Constants, ClearScreen


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
        karateka_color = Utils.get_next_color()
        self.c64 = create_computer("C64", self.screen, karateka_color)
        self.amiga = create_computer("Amiga", self.screen, karateka_color)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def phase0(self):
        print("phase 0 - setup")
        ClearScreen.tile_screen(self.screen, Constants.LIGHT_BLUE)

    def phase1(self):
        pygame.time.delay(3500)
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

    def phase2(self):
        print("phase 2 - c64 - fighters come")
        self.c64.toggle_karatekas('off')
        self.c64.play_ik_sound()
        self.c64.draw_karateka()
        pygame.time.delay(2200)
        self.c64.question_mark()
        pygame.time.delay(1000)

        self.c64.walk_karateka(0, 1950)
        self.c64.question_mark()
        pygame.time.delay(1000)
        self.c64.walk_karateka(0, 500)

        self.c64.karateka.step_left()
        self.c64.karateka.step_left()
        self.c64.walk_karateka(0, 1900)
        self.c64.toggle_karatekas('on')
        self.c64.draw_karateka()

        self.c64.play_ik_sound()
        self.c64.question_mark()
        pygame.time.delay(1000)

    def phase3(self):
        print("phase 3 - c64 fight")
        self.c64.clear_sprite(2)  # karateka3, index 2 , RED
        self.c64.karateka3.step_left()

        self.c64.clear_sprite(3)  # karateka4, index 3 , YELLOW
        self.c64.karateka4.step_left()

        self.c64.karateka.step_right()
        self.c64.walk_karateka(0, 200)  # karateka, index 0 , WHITE
        pygame.time.delay(200)
        self.c64.clear_sprite(0)
        self.c64.kick(0, 1200)
        self.c64.karateka.step_right()
        for _ in range(28):
            self.c64.walk_karateka(2, 580 // 28)
            self.c64.walk_karateka(0, 1800 // 28)

        self.c64.clear_sprite(2)
        self.c64.kick(2, 1200)
        pygame.time.delay(200)
        self.c64.clear_sprite(2)
        self.c64.clear_sprite(1)
        self.c64.karateka2.step_left()  # karateka2, index 1 , CYAN
        self.c64.kill_karateka(1)
        self.c64.draw_karateka()
        self.c64.karateka3.step_right()
        self.c64.walk_karateka(2, 500)

        self.c64.clear_sprite(3)
        self.c64.punch(3, 500)
        self.c64.karateka4.stand()

        self.c64.karateka4.step_right()
        self.c64.walk_karateka(3, 300)
        self.c64.clear_sprite(0)

        self.c64.kick(0, 1200)
        self.c64.clear_sprite(0)
        self.c64.karateka.stand()
        # self.c64.draw_karateka()
        self.c64.karateka4.step_left()
        self.c64.clear_sprite(3)
        self.c64.clear_sprite(1)
        self.c64.punch(3, 500)
        self.c64.clear_sprite(0)
        self.c64.karateka.step_left()
        for _ in range(18):
            self.c64.walk_karateka(0, 1250 // 18)
            self.c64.walk_karateka(3, 500 // 18)

        self.c64.karateka.step_right()
        self.c64.clear_sprite(0)
        self.c64.kick(0, 1200)
        self.c64.clear_sprite(2)
        self.c64.punch(2, 500)
        self.c64.draw_karateka()

        for i in (0, 2, 3, 2, 3, 0, 0):
            self.c64.walk_karateka(2, 23)
            self.c64.clear_sprite(i)
            self.c64.kick(i, 1200)
            if i + 1 < 4 and i + 1 != 1:
                self.c64.clear_sprite(i + 1)
                self.c64.punch(i + 1, 500)
            self.c64.walk_karateka(3, 23)
        pygame.time.delay(1000)
        self.c64.walk_karateka(0, 2200)
        self.c64.karateka.step_left()
        self.c64.clear_sprite(0)
        self.c64.kick(0, 1200)
        self.c64.walk_karateka(3, 250)
        self.c64.punch(3, 500)
        self.c64.draw_karateka()
        self.c64.clear_sprite(2)
        self.c64.kill_karateka(2)
        self.c64.draw_karateka()
        self.c64.karateka4.step_right()

        values = (0, 3, 3, 0, 3, 0)
        for i in range(0, len(values), 2):
            j = values[i]
            k = values[i + 1]

            logging.info("Karateka indices j=%d k=%d", j, k)
            self.c64.walk_karateka(j, 23)
            self.c64.walk_karateka(k, 28)
            self.c64.draw_karateka()
            self.c64.clear_sprite(j)
            self.c64.punch(j, 400)
            self.c64.walk_karateka(j, 5)
            self.c64.walk_karateka(k, 5)
            self.c64.clear_sprite(j)
            self.c64.kick(k, 1200)
            self.c64.walk_karateka(j, 5)
            self.c64.walk_karateka(k, 5)
            self.c64.draw_karateka()

        self.c64.karateka.step_right()

        self.c64.walk_karateka(0, 300)

        for _ in range(10):
            self.c64.walk_karateka(0, 30)
            self.c64.walk_karateka(3, 33)
        self.c64.draw_karateka()

        # leaving
        pygame.time.delay(1000)
        self.c64.walk_karateka(0, 500)
        self.c64.clear_sprite(0)
        self.c64.punch(0, 500)
        self.c64.walk_karateka(0, 1200, True)
        self.c64.walk_karateka(3, 2100)

        pygame.time.delay(1500)
        self.c64.clear_sprite(1)
        self.c64.karateka2.visible = False
        self.c64.draw_karateka()

        pygame.time.delay(700)
        self.c64.karateka2.visible = False
        self.c64.draw_karateka()

    def phase4(self):
        print("phase 4 - bouncing ball")
        pygame.time.delay(1000)
        ball_animation = BallAnimation(self.screen, self.c64.get_catwalk_rect(), Constants.BLUE, 1200)
        ball_animation.bounce()

    def phase5(self):
        print("phase 5 - amiga")
        self.amiga.draw(25)
        self.amiga.toggle_karatekas('off')
        self.amiga.karateka4.visible = True
        self.amiga.karateka4.x = -40
        self.amiga.karateka4.y = self.amiga.karateka.y
        self.amiga.draw_karateka()
        pygame.time.delay(200)

        self.amiga.walk_karateka(0, 1400)
        for _ in range(30):
            self.amiga.walk_karateka(0, 50)
            self.amiga.walk_karateka(3, 53)
        self.amiga.punch(3, 500)
        self.amiga.question_mark()
        pygame.time.delay(1000)
        self.amiga.dropping(1200)
        self.amiga.kill_karateka(0)
        self.amiga.kill_karateka(3)

    def phase6(self):
        print("phase 6 - yet another bouncing ball")
        ball_animation = BallAnimation(self.screen, self.amiga.get_catwalk_rect(), Constants.AMIGA_BLUE, 147)
        ball_animation.bounce()
        pygame.time.delay(4000)

    def phase7(self):
        print("phase 7 - superfrog arrives")

    def phase_finish(self):
        print("Final phase")
        self.amiga.toggle_karatekas('off')
        self.amiga.clear_screen(Scroll.BG_COLOR)

        scroll_instance = Scroll(self.screen, self.WIDTH, canvas_height=368, scroll_speed=5)
        scroll_instance.run(23000)

    def run(self):

        self.phase0()
        self.phase1()
        self.phase2()
        self.phase3()
        self.phase4()
        self.phase5()
        self.phase6()
        self.phase7()
        self.phase_finish()
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
