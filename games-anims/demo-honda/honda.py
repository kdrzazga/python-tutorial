import logging
import pygame
import sys

from collections import deque


class Demo:
    BLACK = (0, 0, 0)

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.WIDTH, self.HEIGHT = 527, 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("HONDA Demo")
        self.clock = pygame.time.Clock()
        self.jump_bitmap = pygame.image.load("resources/honda_jump.png").convert_alpha()
        self.fall_bitmap = pygame.image.load("resources/honda_fall.png").convert_alpha()

        punch_low_right_bitmap = pygame.image.load("resources/honda_punch_lr.png").convert_alpha()
        punch_low_left_bitmap = pygame.image.load("resources/honda_punch_ll.png").convert_alpha()
        punch_high_right_bitmap = pygame.image.load("resources/honda_punch_hr.png").convert_alpha()
        punch_high_left_bitmap = pygame.image.load("resources/honda_punch_hl.png").convert_alpha()
        honda1_bitmap = pygame.image.load("resources/honda1.png").convert_alpha()
        honda2_bitmap = pygame.image.load("resources/honda2.png").convert_alpha()
        honda3_bitmap = pygame.image.load("resources/honda3.png").convert_alpha()
        step1_bitmap = pygame.image.load("resources/honda_step1.png").convert_alpha()
        step2_bitmap = pygame.image.load("resources/honda_step2.png").convert_alpha()

        self.stand_sequence = deque((honda1_bitmap, honda2_bitmap, honda1_bitmap, honda2_bitmap, honda1_bitmap,
                                     honda1_bitmap, honda2_bitmap, honda1_bitmap, honda2_bitmap, honda1_bitmap,
                                     honda3_bitmap))
        self.walk_sequence = deque((step1_bitmap, honda1_bitmap, step2_bitmap))
        self.punch_sequence = deque((honda1_bitmap, punch_low_right_bitmap, honda2_bitmap, punch_low_left_bitmap,
                                     honda1_bitmap, punch_high_right_bitmap, honda2_bitmap, punch_high_left_bitmap ))

        self.y_max = self.HEIGHT - 5 - self.jump_bitmap.get_height()

    def phase1(self):
        logging.info("PHASE 1 - fall")
        y = -self.jump_bitmap.get_height() - 5
        while y <= self.y_max:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            self.screen.fill(Demo.BLACK)

            y += 1
            bitmap = self.jump_bitmap if y > 3 * self.y_max // 8 else self.fall_bitmap
            offset = 70 if y > 3 * self.y_max // 8 else 0
            self.screen.blit(bitmap, (offset, y))

            pygame.display.flip()
            self.clock.tick(150)

    def phase2(self):
        logging.info("PHASE 2 - stand")
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time <= 10000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            self.stand_sequence.rotate(-1)
            self.screen.fill(Demo.BLACK)
            bitmap = self.stand_sequence[0]
            self.screen.blit(bitmap, (0, self.HEIGHT - 5 - bitmap.get_height()))

            pygame.display.flip()
            self.clock.tick(3)

    def phase3(self):
        logging.info("PHASE 3 - walk")
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time <= 12000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            self.walk_sequence.rotate(-1)
            self.screen.fill(Demo.BLACK)
            bitmap = self.walk_sequence[0]
            self.screen.blit(bitmap, (0, self.HEIGHT - 5 - bitmap.get_height()))

            pygame.display.flip()
            self.clock.tick(3)

    def phase4(self):
        logging.info("PHASE 4 - punch")
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time <= 13000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            self.punch_sequence.rotate(-1)
            self.screen.fill(Demo.BLACK)
            bitmap = self.punch_sequence[0]
            self.screen.blit(bitmap, (0, self.HEIGHT - 5 - bitmap.get_height()))

            pygame.display.flip()
            self.clock.tick(3)

    def run(self):
        pygame.init()

        self.phase1()
        self.phase2()
        self.phase3()
        self.phase4()
        logging.info("BYE !")

        pygame.quit()


if __name__ == "__main__":
    Demo().run()
