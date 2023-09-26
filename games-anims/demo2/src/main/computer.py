import pygame

from collections import deque

from src.main.karateka import Karateka
from src.main.utils import Constants, Utils, ClearScreen


class Computer:
    karatekaGreen = Karateka(300, Constants.KARATEKA_Y, Constants.GREEN, True)
    karatekaRed = Karateka(460, Constants.KARATEKA_Y, Constants.RED, True)
    karatekaCyan = Karateka(590, Constants.KARATEKA_Y, Constants.CYAN, True)
    karatekaYellow = Karateka(490, Constants.KARATEKA_Y, Constants.YELLOW, False)
    karatekaBrown = Karateka(380, Constants.KARATEKA_Y, Constants.BROWN, False)
    karatekaPurple = Karateka(610, Constants.KARATEKA_Y, Constants.PURPLE, False)

    def __init__(self, bg_color1, bg_color2):
        self.clock = pygame.time.Clock()
        self.bg_color = bg_color1
        self.karateka = None # will be created in factory
        self.superfrog = None # will be created in factory
        self.location = (0, 0)
        self.sprite_bitmap = None
        self.qm_bitmap = pygame.image.load("src/main/resources/qm.png").convert_alpha()
        pygame.mixer.init()
        self.walking_sound = pygame.mixer.Sound("src/main/resources/steps.wav")
        self.clock = pygame.time.Clock()
        self.jump_bitmap = pygame.image.load("src/main/resources/honda/honda_jump.png").convert_alpha()
        self.fall_bitmap = pygame.image.load("src/main/resources/honda/honda_fall.png").convert_alpha()

        punch_low_right_bitmap = pygame.image.load("src/main/resources/honda/honda_punch_lr.png").convert_alpha()
        punch_low_left_bitmap = pygame.image.load("src/main/resources/honda/honda_punch_ll.png").convert_alpha()
        punch_high_right_bitmap = pygame.image.load("src/main/resources/honda/honda_punch_hr.png").convert_alpha()
        punch_high_left_bitmap = pygame.image.load("src/main/resources/honda/honda_punch_hl.png").convert_alpha()
        honda1_bitmap = pygame.image.load("src/main/resources/honda/honda1.png").convert_alpha()
        honda2_bitmap = pygame.image.load("src/main/resources/honda/honda2.png").convert_alpha()
        honda3_bitmap = pygame.image.load("src/main/resources/honda/honda3.png").convert_alpha()
        step1_bitmap = pygame.image.load("src/main/resources/honda/honda_step1.png").convert_alpha()
        step2_bitmap = pygame.image.load("src/main/resources/honda/honda_step2.png").convert_alpha()

        self.stand_sequence = deque((honda1_bitmap, honda2_bitmap, honda1_bitmap, honda2_bitmap, honda1_bitmap,
                                     honda1_bitmap, honda2_bitmap, honda1_bitmap, honda2_bitmap, honda1_bitmap,
                                     honda3_bitmap))
        self.walk_sequence = deque((step1_bitmap, honda1_bitmap, step2_bitmap))
        self.punch_sequence = deque((honda1_bitmap, punch_low_right_bitmap, honda2_bitmap, punch_low_left_bitmap,
                                     honda1_bitmap, punch_high_right_bitmap, honda2_bitmap, punch_high_left_bitmap ))


    def clear_sprite(self, sprite_index):
        karateka = self.get_karatekas_array()[sprite_index]
        self.clear_karateka(karateka)

    def clear_karateka(self, karateka):
        y = karateka.y - self.sprite_bitmap.get_height() / 2

        pygame.draw.rect(self.screen, self.bg_color,
                         ((karateka.x - karateka.width // 2 - 15, y - 10), (karateka.width + 20, karateka.height + 10)))

    def draw_sprite(self, sprite):
        path = sprite.get_sprite_path()
        normal_sprite_bitmap = pygame.image.load(path).convert_alpha()
        flipped_sprite_bitmap = pygame.transform.flip(normal_sprite_bitmap, True, False)

        self.sprite_bitmap = normal_sprite_bitmap if sprite.looking_right else flipped_sprite_bitmap
        if sprite.color is not None:
            self.sprite_bitmap = Utils.color_bitmap(self.sprite_bitmap, sprite.color)

        x = sprite.x - self.sprite_bitmap.get_width() / 2
        y = sprite.y - self.sprite_bitmap.get_height() / 2

        sprite.width = self.sprite_bitmap.get_width()
        sprite.height = self.sprite_bitmap.get_height()

        self.screen.blit(self.sprite_bitmap, (x, y))
        pygame.display.update()

    def draw_superfrog(self):
        self.draw_sprite(self.superfrog)

    def draw_karateka(self):
        for karateka in self.get_karatekas_array():
            if karateka.visible:                
                self.draw_sprite(karateka)

    def start_walking_sounds(self):
        self.walking_sound.play(-1)

    def stop_walking_sounds(self):
        self.walking_sound.stop()

    def walk_karateka(self, index, duration_ms, open_pass=False, bulk_walk=False):
        karateka = self.get_karatekas_array()[index]

        if not bulk_walk:
            self.start_walking_sounds()

        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time <= duration_ms:
            karateka.step()
            self.clear_sprite(index)

            if open_pass:
                self.open_passage(1)
            self.draw_karateka()
            self.clock.tick(32)

        if not bulk_walk:
            self.stop_walking_sounds()

    def punch(self, karateka_index, duration_ms):
        self.clear_sprite(karateka_index)
        k = self.get_karatekas_array()[karateka_index]
        k.punch()

        self.draw_karateka()
        punch_sound = pygame.mixer.Sound("src/main/resources/chuja.mp3")
        punch_sound.play()
        pygame.time.delay(duration_ms)
        self.clear_sprite(karateka_index)
        k.stand()

    def check_ball_kill(self, ball_x):
        for index, karateka in enumerate(self.get_karatekas_array()):
            if karateka.walk_phase != 'lying':
                if ball_x >= karateka.x and ball_x <= karateka.x + 30:
                    karateka.step_left()
                    self.clear_karateka(karateka)
                    self.kill_karateka(index)

    def kill_karateka(self, sprite_index):
        karateka = self.get_karatekas_array()[sprite_index]

        karateka.walk_phase = 'lying'
        karateka.y += 24
        self.draw_sprite(karateka)

    def question_mark(self):
        x = self.karateka.x + self.sprite_bitmap.get_width() / 2
        y = self.karateka.y - self.sprite_bitmap.get_height() / 2

        self.draw_karateka()
        self.screen.blit(self.qm_bitmap, (x, y))

        pygame.display.update()

    def toggle_karatekas1(self, on_off):
        visibility = on_off == 'on'
        for karateka in (self.karatekaGreen, self.karatekaRed, self.karatekaCyan):
            karateka.visible = visibility

    def toggle_karatekas2(self, on_off):
        visibility = on_off == 'on'
        for karateka in (self.karatekaYellow, self.karatekaBrown, self.karatekaPurple):
            karateka.visible = visibility

    def clear_screen(self, color):
        ClearScreen.tile_screen(self.screen, color)

    def get_bg_color(self):
        return self.bg_color

    def get_karatekas_array(self):
        return [self.karateka, self.karatekaGreen, self.karatekaRed, self.karatekaCyan, self.karatekaYellow, self.karatekaBrown, self.karatekaPurple]

    def get_karateka(self, color):
        return [k for k in self.get_karatekas_array() if k.color == color]

    def get_karateka_index(self, color):
        karatekas = self.get_karatekas_array()
        try:
            return karatekas.index(next(k for k in karatekas if k.color == color))
        except StopIteration:
            return -1  # Color not found
