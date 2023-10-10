import logging

import pygame
from src.main.computer import Computer
from src.main.utils import Utils, Constants


class Amiga(Computer):
    h = 70
    window_x = 160 - 3

    def __init__(self, screen):
        super().__init__(Constants.AMIGA_BLUE, Constants.BLUE)
        self.screen = screen

        self.background_bitmap = Utils.load_background("src/main/resources/amiga.png")
        self.window_bitmap = pygame.image.load("src/main/resources/window2.png")
        self.streetfigher_icon_bitmap = pygame.image.load("src/main/resources/sf.png")

    def draw_background(self):
        self.screen.blit(self.background_bitmap, (0, 0))
        pygame.display.flip()

    def draw_window(self):
        self.screen.blit(self.window_bitmap, (self.window_x, self.h))
        pygame.display.flip()
        self.draw_street_fighter_icon()

    def draw_street_fighter_icon(self):
        self.screen.blit(self.streetfigher_icon_bitmap, (191 - 3, self.h + 27))
        pygame.display.flip()

    def draw(self, duration_ms):
        start_time = pygame.time.get_ticks()
        self.draw_background()
        self.draw_window()

        while pygame.time.get_ticks() - start_time <= duration_ms:
            pass

    def dropping(self, duration_ms):
        start_time = pygame.time.get_ticks()
        acceleration = 0
        while pygame.time.get_ticks() - start_time <= duration_ms:
            self.draw_background()
            self.draw_sprite(self.karateka)
            self.draw_sprite(self.karatekaCyan)
            self.draw_window()
            if pygame.time.get_ticks() - start_time <= duration_ms - 500:
                self.question_mark()
            acceleration += 0.3
            self.h += int(1 + acceleration)

            if self.window_hit_bottom():
                self.h -= int(1 + acceleration)
                break

            self.clock.tick(36)

    def activate_honda(self, duration_ms):
        start_time = pygame.time.get_ticks()
        self.honda.y = self.h - self.stand_sequence[0].get_height() //2 + 10
        self.draw_honda()
        pygame.display.flip()

        pygame.time.delay(duration_ms)
            
    def fall_honda(self, duration_ms):
        start_time = pygame.time.get_ticks()        
        self.honda.walk_phase = "fall"
        while pygame.time.get_ticks() - start_time <= duration_ms:
            self.draw_honda()
            self.honda.y +=3
            self.honda.x -=1
            
            self.clock.tick(26)

    def blur_honda(self):
        pygame.time.delay(3000)
        self.clear_karateka(self.honda)
        pixelled_honda = self.change_resolution(self.stand_sequence[0], 0)
        x = self.honda.x
        y = self.honda.y

        width = pixelled_honda.get_width()
        height = pixelled_honda.get_height()
        
        self.screen.blit(pixelled_honda, (x, y))
        pygame.display.update()
        pygame.time.delay(3000)

    def window_hit_bottom(self):
        wh = self.window_bitmap.get_height()
        bh = self.background_bitmap.get_height()

        logging.info("self.h = %d, window height = %d, bitmap height =  %d", self.h, wh, bh)

        return wh + self.h > bh - 22

    def get_catwalk_rect(self):
        x = -10
        y = self.background_bitmap.get_height() - 88
        width = self.window_x + 3
        height = 88

        return pygame.Rect(x, y, width, height)
        
    def honda_deflects_ball(self, x):
        self.honda.y = 485
        self.honda.punch()
        self.draw_honda(Constants.BLUE)

    def play_honda_sound(self):
        punch_sound = pygame.mixer.Sound("src/main/resources/honda/honda.mp3")
        punch_sound.play()