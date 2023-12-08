import logging
import time
import copy
import sys

import pygame

from src.main.bouncing_ball import BallAnimation
from src.main.factory import create_computer
from src.main.scroll import Scroll
from src.main.scrolling_transition import ScrollingTransition
from src.main.utils import Utils, Constants, ClearScreen


class Demo:

    def __init__(self, fullscreen=False, key_paused=False):
        self.screen = None
        self.key_paused = key_paused

        if fullscreen:
            self.screen = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT),
                                                  pygame.FULLSCREEN | pygame.DOUBLEBUF)
            pygame.mouse.set_pos((Constants.WIDTH - 1, Constants.HEIGHT - 1))
        else:
            self.screen = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT), pygame.DOUBLEBUF)

        if self.key_paused:
            self.wait_key_pressed()

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

        for karateka in [self.c64.karateka, self.c64.karatekaGreen, self.c64.karatekaRed, self.c64.karatekaCyan,
                         self.c64.karatekaYellow, self.c64.karatekaBrown, self.c64.karatekaPurple]:
            logging.info("Karateka " + str(karateka.id) + " color " + str(karateka.color))
        logging.info("Demo start")
        self.start_time = time.time()

    def phase0(self):
        print("phase 0 - setup")
        pygame.time.delay(1500)
        ClearScreen.tile_screen(self.screen, Constants.LIGHT_BLUE)
        pygame.time.delay(500)
        self.c64.handle_cursor(3500)

    def phase1(self):
        print("phase 1 - loading")

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

        self.c64.start_walking_sounds()
        for _ in range(28):
            self.c64.walk_karateka(self.green, 31, bulk_walk=True)
            self.c64.walk_karateka(self.red, 31, bulk_walk=True)
            self.c64.walk_karateka(self.cyan, 868 // 28, bulk_walk=True)
        self.c64.stop_walking_sounds()

        self.c64.karatekaGreen.step_right()
        self.c64.karatekaGreen.punch()

        self.c64.walk_karateka(self.white, 200)
        self.c64.karatekaGreen.step_right()
        self.c64.kick(self.white, 1200)
        self.c64.karateka.step_right()

        self.c64.start_walking_sounds()
        for _ in range(28):
            self.c64.walk_karateka(self.red, 580 // 28, bulk_walk=True)
            self.c64.walk_karateka(self.white, 1800 // 28, bulk_walk=True)
        self.c64.stop_walking_sounds()

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

        self.c64.start_walking_sounds()
        for _ in range(18):
            self.c64.walk_karateka(self.white, 1250 // 18, bulk_walk=True)
            self.c64.walk_karateka(self.cyan, 500 // 18, bulk_walk=True)
        self.c64.stop_walking_sounds()

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

        self.c64.start_walking_sounds()
        for _ in range(10):
            self.c64.walk_karateka(self.white, 33, bulk_walk=True)
            self.c64.walk_karateka(self.cyan, 36, bulk_walk=True)
        self.c64.stop_walking_sounds()
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
        self.c64.walk_karateka(self.cyan, 3800)

        pygame.time.delay(1000)
        self.c64.clear_sprite(self.green)
        self.c64.draw_karateka()
        self.c64.karatekaGreen.visible = False

        pygame.time.delay(1000)
        self.c64.karatekaRed.visible = False
        self.c64.draw_karateka()

    def phase5(self):
        print("phase 5 - bouncing ball")
        pygame.time.delay(1000)
        self.c64.toggle_karatekas1('on')
        ball_animation = BallAnimation(self.screen, self.c64.get_catwalk_rect(), Constants.BLUE, 1200)
        ball_animation.bounce(self.c64, karateka=True)
        self.c64.toggle_karatekas1('off')

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

        self.c64.start_walking_sounds()
        for _ in range(30):
            self.amiga.walk_karateka(self.white, 50, bulk_walk=True)
            self.amiga.walk_karateka(self.cyan, 53, bulk_walk=True)
        self.c64.stop_walking_sounds()

        self.amiga.punch(self.cyan, 500)
        self.amiga.question_mark()
        pygame.time.delay(1000)
        self.amiga.dropping(1200)
        self.amiga.kill_karateka(self.white)
        self.amiga.kill_karateka(self.cyan)

    def phase7(self):
        print("phase 7 - yet another bouncing ball")
        ball_animation = BallAnimation(self.screen, self.amiga.get_catwalk_rect(), Constants.AMIGA_BLUE, 147)
        ball_animation.bounce(self.amiga, honda=False)
        pygame.time.delay(4000)

    def phase8(self):
        print("phase 8 - honda arrives")
        self.amiga.activate_honda(1000)
        pygame.time.delay(1500)
        self.amiga.walk_honda(2700)
        pygame.time.delay(900)
        self.amiga.honda.step_left()
        self.amiga.walk_honda(3800)
        self.amiga.fall_honda(2750)
        self.amiga.walk_honda(1)
        pygame.time.delay(1000)

    def phase9(self):
        print("phase 9 - partial return to c64")
        scrolling_transition = ScrollingTransition(self.screen)
        scrolling_transition.run()
        # self.amiga.clear_karateka(self.amiga.honda)
        self.amiga.honda.x += scrolling_transition.max_distance
        self.amiga.honda.y -= 76
        self.amiga.walk_honda(3600, over_window=False)
        self.amiga.honda.step_right()
        self.amiga.walk_honda(1900, over_window=False)
        self.amiga.honda.step_left()
        self.amiga.walk_honda(19, over_window=False)
        pygame.time.delay(6000)

    def phase10(self):
        print("phase 10 - 3rd bouncing ball")
        self.c64.toggle_karatekas1('off')
        rect = self.c64.get_catwalk_rect()
        rect.x = 0
        ball_animation = BallAnimation(self.screen, rect, Constants.BLUE, 255)
        ball_animation.bounce(self.amiga)
        self.c64.toggle_karatekas1('off')

    def phase11(self):
        print("phase 11 - honda, you don't belong here !!!")
        self.c64.honda = copy.copy(self.amiga.honda)
        pygame.time.delay(300)

        self.c64.writeline("HONDA !!")
        self.c64.writeline("You don't")
        self.c64.writeline("belong here!!!")
        self.amiga.play_honda_sound()
        pygame.time.delay(4000)

        for _ in range(5):
            self.c64.cursor.move_up()
        for _ in range(5):
            self.c64.writeline(14 * ' ')

        self.c64.cursor.move_up()
        self.c64.writeline("adjusting")
        self.c64.writeline("resolution:")
        self.c64.writeline("320 x 200")
        pygame.time.delay(2000)
        self.amiga.blur_honda()

    def phase12(self):
        print("phase 12 - transition")
        pygame.time.delay(500)
        ClearScreen.tile_screen(self.screen, Constants.LIGHT_BLUE)

    def phase_finish(self):
        print("Final phase")
        self.amiga.toggle_karatekas1('off')
        self.amiga.toggle_karatekas2('off')
        self.amiga.clear_screen(Scroll.BG_COLOR)

        scroll_instance = Scroll(self.screen, Constants.WIDTH, canvas_height=368, scroll_speed=5)
        scroll_instance.run(36000)

        elapsed_time_seconds = time.time() - self.start_time
        elapsed_minutes = int(elapsed_time_seconds // 60)
        elapsed_seconds = int(elapsed_time_seconds % 60)

        print(f"Demo duration: {elapsed_minutes}:{elapsed_seconds}")

    def run(self):

        self.phase0()  # tiling
        self.phase1()  # loading
        self.phase2()  # ik+
        self.phase3()  # ik+
        self.phase4()  # ik+
        self.phase5()  # bounce
        self.phase6()  # amiga
        self.phase7()  # bounce
        self.phase8()  # honda
        self.phase9()  # amiga -> c64
        self.phase10()  # bounce
        self.phase11()  # erasing honda
        self.phase12()  # tiling
        self.phase_finish()

        if self.key_paused:
            ClearScreen.tile_screen(self.screen, Constants.LIGHT_BLUE)
            self.wait_key_pressed()

        print("BYE !")

    @staticmethod
    def wait_key_pressed():
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    running = False


if __name__ == "__main__":
    fullscreen = False
    looped = False
    key_paused = False

    if len(sys.argv) > 1:
        help_display = 'help' in sys.argv or '-h' in sys.argv or 'h' in sys.argv
        looped = 'loop' in sys.argv
        fullscreen = 'fullscreen' in sys.argv or 'fs' in sys.argv
        key_paused = 'key-paused' in sys.argv or 'kp' in sys.argv

        if help_display:
            for info in ("demo parameters:", "loop - runs demo in loop", "fullscreen - it's obvious"
                         , "fs - same as above", "help - displays this help", "-h - same as above"
                         , "h - same as above", "key-paused - forces pressing SPACE key to start"
                         , "kp - same as above", "", "DEFAULT RUN: python demo2.py fs kp"):
                print(info)

            print("\nBYE !")
            sys.exit(0)

    pygame.init()

    if looped:
        while True:
            Demo(fullscreen, key_paused).run()

    Demo(fullscreen, key_paused).run()

    pygame.quit()
