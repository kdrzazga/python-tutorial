import pygame

from src.main.utils import Constants


class Computer:

    def __init__(self, bg_color1, bg_color2):
        self.clock = pygame.time.Clock()
        self.bg_color = bg_color1
        self.karateka = None
        self.location = (0, 0)
        self.sprite_bitmap = None
        self.qm_bitmap = pygame.image.load("src/main/resources/qm.png").convert_alpha()
        pygame.mixer.init()
        self.walking_sound = pygame.mixer.Sound("src/main/resources/steps.wav")

    def clear_sprite(self):
        y = self.karateka.y - self.sprite_bitmap.get_height() / 2

        pygame.draw.rect(self.screen, self.bg_color,
                         ((self.location[0] + 2, y - 10), (Constants.SCREEN_WIDTH - 10, self.karateka.height + 10)))

    def draw_sprite(self):
        path = self.karateka.get_sprite_path()
        normal_sprite_bitmap = pygame.image.load(path).convert_alpha()
        flipped_sprite_bitmap = pygame.transform.flip(normal_sprite_bitmap, True, False)

        self.sprite_bitmap = normal_sprite_bitmap if self.karateka.looking_right else flipped_sprite_bitmap

        x = self.karateka.x - self.sprite_bitmap.get_width() / 2
        y = self.karateka.y - self.sprite_bitmap.get_height() / 2

        self.karateka.width = self.sprite_bitmap.get_width()
        self.karateka.height = self.sprite_bitmap.get_height()

        self.screen.blit(self.sprite_bitmap, (x, y))
        pygame.display.update()

    def walk_karateka(self, duration_ms, open_pass=False):
        self.walking_sound.play(-1)
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time <= duration_ms:
            self.karateka.step()

            y = self.karateka.y - self.sprite_bitmap.get_height() / 2

            pygame.draw.rect(self.screen, self.bg_color,
                             ((self.location[0] + 2, y - 10), (Constants.SCREEN_WIDTH - 10, self.karateka.height + 10)))

            if open_pass:
                self.open_passage(1)
            self.draw_sprite()
            self.clock.tick(32)
        self.walking_sound.stop()

    def kill_karateka(self):
        self.karateka.y += 23
        self.karateka.walk_phase = 'lying'
        self.draw_sprite()

    def question_mark(self, off):
        x = self.karateka.x + self.sprite_bitmap.get_width() / 2
        y = self.karateka.y - self.sprite_bitmap.get_height() / 2

        self.screen.blit(self.qm_bitmap, (x, y))
        pygame.display.update()

        if off:
            pass

    def get_bg_color(self):
        return self.bg_color
