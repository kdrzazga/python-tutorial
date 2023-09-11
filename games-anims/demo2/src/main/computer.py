import pygame

from src.main.utils import Constants, Utils, ClearScreen
from src.main.karateka import Karateka

class Computer:

    karateka2 = Karateka(300, Constants.KARATEKA_Y, Utils.get_next_color())
    karateka3 = Karateka(460, Constants.KARATEKA_Y, Utils.get_next_color())
    karateka4 = Karateka(590, Constants.KARATEKA_Y, Utils.get_next_color())

    def __init__(self, bg_color1, bg_color2):
        self.clock = pygame.time.Clock()
        self.bg_color = bg_color1
        self.karateka = None
        self.superfrog = None
        self.location = (0, 0)
        self.sprite_bitmap = None
        self.qm_bitmap = pygame.image.load("src/main/resources/qm.png").convert_alpha()
        pygame.mixer.init()
        self.walking_sound = pygame.mixer.Sound("src/main/resources/steps.wav")

    def clear_sprite(self, sprite_index):
        karateka = [self.karateka, self.karateka2, self.karateka3, self.karateka4][sprite_index]
        y = karateka.y - self.sprite_bitmap.get_height() / 2
       
        pygame.draw.rect(self.screen, self.bg_color,
                             ((karateka.x - karateka.width //2 - 15, y - 10), (karateka.width + 20, karateka.height + 10)))

    def draw_sprite(self, sprite):
        path = sprite.get_sprite_path()
        normal_sprite_bitmap = pygame.image.load(path).convert_alpha()
        flipped_sprite_bitmap = pygame.transform.flip(normal_sprite_bitmap, True, False)

        self.sprite_bitmap = normal_sprite_bitmap if sprite.looking_right else flipped_sprite_bitmap
        if sprite.color != None:
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
        for karateka in [self.karateka, Computer.karateka2, Computer.karateka3, Computer.karateka4]:
            if karateka.visible:
                self.draw_sprite(karateka)

    def walk_karateka(self, index, duration_ms, open_pass=False):
        karateka = [self.karateka, self.karateka2, self.karateka3, self.karateka4][index]

        self.walking_sound.play(-1)
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time <= duration_ms:
            karateka.step()
            self.clear_sprite(index)

            if open_pass:
                self.open_passage(1)
            self.draw_karateka()
            self.clock.tick(32)
        self.walking_sound.stop()

    def kill_karateka(self, sprite_index):
        karateka = [self.karateka, self.karateka2, self.karateka3, self.karateka4][sprite_index]

        karateka.walk_phase = 'lying'
        karateka.y += 24
        self.draw_sprite(karateka)

    def question_mark(self, off):
        x = self.karateka.x + self.sprite_bitmap.get_width() / 2
        y = self.karateka.y - self.sprite_bitmap.get_height() / 2

        self.screen.blit(self.qm_bitmap, (x, y))
        pygame.display.update()

        if off:
            pass

    def toggle_karatekas(self, on_off):
        visibility = on_off == 'on'
        for karateka in (self.karateka2, self.karateka3, self.karateka4):
            karateka.visible = visibility

    def clear_screen(self, color):
        ClearScreen.tile_screen(self.screen, color)

    def get_bg_color(self):
        return self.bg_color
