import logging
import sys

import pygame

from src.main.bouncing_ball import BallAnimation
from src.main.factory import create_computer
from src.main.scroll import Scroll
from src.main.scrolling_transition import ScrollingTransition
from src.main.utils import Utils, Constants, ClearScreen


class Demo:

    def __init__(self, fullscreen=False):        
        self.screen = None

        if fullscreen:
            self.screen = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF)
            pygame.mouse.set_pos((Constants.WIDTH - 1, Constants.HEIGHT - 1))
        else:
            self.screen = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT), pygame.DOUBLEBUF)

        pygame.display.set_caption("Ni Komodor Ni Amiga Demo")
        karateka_color = Utils.get_next_color()
        self.c64 = create_computer("C64", self.screen, karateka_color)
        self.amiga = create_computer("Amiga", self.screen, karateka_color)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                
        self.white = self.c64.get_karateka_index(Constants.WHITE)
        self.green = self.c64.get_karateka_index(Constants.GREEN)
        self.red = self.c64.get_karateka_index(Constants.RED)
        self.cyan = self.c64.get_karateka_index(Constants.CYAN)
        self.yellow = self.c64.get_karateka_index(Constants.YELLOW)
        self.brown = self.c64.get_karateka_index(Constants.BROWN)
        self.purple = self.c64.get_karateka_index(Constants.PURPLE)

        for karateka in [self.c64.karateka, self.c64.karatekaGreen, self.c64.karatekaRed, self.c64.karatekaCyan, self.c64.karatekaYellow, self.c64.karatekaBrown, self.c64.karatekaPurple]:
            logging.info("Karateka " + str(karateka.id) + " color " + str(karateka.color))
        logging.info("Demo start")


    def phase0(self):
        print("phase 0 - setup")
        ClearScreen.tile_screen(self.screen, Constants.LIGHT_BLUE)
        pygame.time.delay(500)
        self.c64.handle_cursor(3500)

    def phase1(self):

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
        self.c64.toggle_karatekas1('off')
        self.c64.play_ik_sound()
        self.c64.draw_karateka()
        pygame.time.delay(2200)
        self.c64.question_mark()
        pygame.time.delay(1000)

        self.c64.walk_karateka(self.white, 1950)
        self.c64.question_mark()
        pygame.time.delay(1000)
        self.c64.walk_karateka(self.white, 500)

        self.c64.karateka.step_left()
        self.c64.walk_karateka(self.white, 1900)
        self.c64.toggle_karatekas1('on')
        self.c64.draw_karateka()

        self.c64.play_ik_sound()
        self.c64.question_mark()
        pygame.time.delay(1000)
        self.c64.kick(self.white, 900)
        self.c64.karateka.step_right()

    def phase3(self):
        print("phase 3 - c64 first fight")
        self.c64.clear_sprite(self.red)
        self.c64.karatekaRed.step_left()

        self.c64.clear_sprite(self.cyan)
        self.c64.karatekaCyan.step_left()
 
        self.c64.clear_sprite(self.green)
        
        self.c64.karatekaGreen.step_left()
        self.c64.karatekaGreen.kick()

        for _ in range(28):
            self.c64.walk_karateka(self.green, 31)
            self.c64.walk_karateka(self.red, 31)
            self.c64.walk_karateka(self.cyan, 868 // 28)

        self.c64.karatekaGreen.step_right()
        self.c64.karatekaGreen.punch()
        
        self.c64.walk_karateka(self.white, 200)
        self.c64.karatekaGreen.step_right()
        self.c64.kick(self.white, 1200)
        self.c64.karateka.step_right()
        for _ in range(28):
            self.c64.walk_karateka(self.red, 580 // 28)
            self.c64.walk_karateka(self.white, 1800 // 28)

        self.c64.clear_sprite(self.red)
        self.c64.kick(self.red, 1200)
        pygame.time.delay(200)
        self.c64.clear_sprite(self.red)
        self.c64.clear_sprite(self.green)
        self.c64.karatekaGreen.step_left()
        self.c64.kill_karateka(self.green)
        self.c64.draw_karateka()
        self.c64.karatekaRed.step_right()
        self.c64.walk_karateka(self.red, 500)
        self.c64.clear_sprite(self.cyan)
        self.c64.punch(self.cyan, 500)
        self.c64.karatekaCyan.stand()

        self.c64.karatekaCyan.step_right()
        self.c64.walk_karateka(self.cyan, 300)
        self.c64.clear_sprite(self.white)

        self.c64.kick(self.white, 1200)
        self.c64.clear_sprite(self.white)
        self.c64.karateka.stand()
        # self.c64.draw_karateka()
        self.c64.karatekaCyan.step_left()
        self.c64.clear_sprite(self.cyan)
        self.c64.clear_sprite(self.green)
        self.c64.punch(self.cyan, 500)
        self.c64.clear_sprite(self.white)
        self.c64.karateka.step_left()
        for _ in range(18):
            self.c64.walk_karateka(self.white, 1250 // 18)
            self.c64.walk_karateka(self.cyan, 500 // 18)

        self.c64.karateka.step_right()
        self.c64.clear_sprite(self.white)
        self.c64.kick(self.white, 1200)
        self.c64.clear_sprite(self.red)
        self.c64.punch(self.red, 500)
        self.c64.draw_karateka()

        for i in (0, self.red, self.cyan, self.red, self.cyan, 0, 0):
            self.c64.walk_karateka(self.red, 23)
            self.c64.clear_sprite(i)
            self.c64.kick(i, 1200)
            if i + 1 < 4 and i + 1 != 1:
                self.c64.clear_sprite(i + 1)
                self.c64.punch(i + 1, 500)
            self.c64.walk_karateka(self.cyan, 23)
        pygame.time.delay(1000)
        self.c64.walk_karateka(self.white, 2200)
        self.c64.karateka.step_left()
        self.c64.walk_karateka(self.cyan, 250)
        self.c64.punch(self.cyan, 500)
        self.c64.draw_karateka()
        self.c64.clear_sprite(self.red)
        self.c64.kill_karateka(self.red)
        self.c64.draw_karateka()
        self.c64.karatekaCyan.step_right()
        
        values = (0, 3)
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
    
    def phase4(self):
        print(7 * "\n" + "phase 4 - c64 second fight and leave")

        self.c64.toggle_karatekas2('on')
        self.c64.play_ik_sound()

        self.c64.karateka.step_right()
        self.c64.walk_karateka(self.white, 270)

        for _ in range(10):
            self.c64.walk_karateka(self.white, 33)
            self.c64.walk_karateka(self.cyan, 36)
        self.c64.draw_karateka()

        for i in (4, 5, 4, 6, 5, self.white):
            self.c64.clear_sprite(i)
            self.c64.kick(i, 1200)
            self.c64.walk_karateka(i, 3)

        # leaving
        pygame.time.delay(1000)
        self.c64.walk_karateka(self.white, 210)
        self.c64.clear_sprite(self.white)
        self.c64.punch(self.white, 500)
        self.c64.walk_karateka(self.white, 1200, True)
        self.c64.walk_karateka(self.cyan, 2100)


        pygame.time.delay(1000)
        self.c64.clear_sprite(self.green)
        self.c64.draw_karateka()
        self.c64.karatekaGreen.visible = False
        
        pygame.time.delay(1000)
        self.c64.karatekaRed.visible = False
        self.c64.draw_karateka()

    def phase5(self):
        print("phase 6 - bouncing ball")
        pygame.time.delay(1000)
        ball_animation = BallAnimation(self.screen, self.c64.get_catwalk_rect(), Constants.BLUE, 1200)
        ball_animation.bounce()

    def phase6(self):
        print("phase 6 - amiga")
        self.amiga.draw(25)
        self.amiga.toggle_karatekas1('off')
        self.amiga.toggle_karatekas2('off')
        self.amiga.karatekaCyan.visible = True
        self.amiga.karatekaCyan.x = -40
        self.amiga.karatekaCyan.y = self.amiga.karateka.y
        self.amiga.draw_karateka()
        pygame.time.delay(200)

        self.amiga.walk_karateka(self.white, 1400)
        for _ in range(30):
            self.amiga.walk_karateka(self.white, 50)
            self.amiga.walk_karateka(self.cyan, 53)
        self.amiga.punch(self.cyan, 500)
        self.amiga.question_mark()
        pygame.time.delay(1000)
        self.amiga.dropping(1200)
        self.amiga.kill_karateka(self.white)
        self.amiga.kill_karateka(self.cyan)

    def phase7(self):
        print("phase 7 - yet another bouncing ball")
        ball_animation = BallAnimation(self.screen, self.amiga.get_catwalk_rect(), Constants.AMIGA_BLUE, 147)
        ball_animation.bounce()
        pygame.time.delay(4000)

    def phase8(self):
        print("phase 8 - superfrog arrives")

    def phase9(self):
        print("phase 9 - partial return to c64")
        scrolling_transition = ScrollingTransition(self.screen)
        scrolling_transition.run()

    def phase_finish(self):
        print("Final phase")
        self.amiga.toggle_karatekas1('off')
        self.amiga.toggle_karatekas2('off')
        self.amiga.clear_screen(Scroll.BG_COLOR)

        scroll_instance = Scroll(self.screen, Constants.WIDTH, canvas_height=368, scroll_speed=5)
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
        self.phase8()
        self.phase9()
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
