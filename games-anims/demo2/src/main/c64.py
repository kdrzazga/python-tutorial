import time
import pygame
import logging

from src.main.utils import Utils, Constants
from src.main.computer import Computer

from PIL import Image, ImageDraw, ImageFont

class Cursor:


    def __init__(self, screen_position):
        self.position = (0, 6)
        self.on = True
        self.screen_position = screen_position


    def blink_color(self):
        return Constants.LIGHT_BLUE if self.on else Constants.BLUE


    def get_screen_position(self):
        return (self.screen_position[0] + self.position[0] * C64.line_size, self.screen_position[1] + self.position[1] * C64.line_size)


    def move_right(self):
        new_position = (self.position[0] + 1, self.position[1])
        self.position = new_position
        pygame.time.delay(1000)


    def move_down(self):
        new_position = (self.position[0], self.position[1] + 1)
        self.position = new_position
        logging.info("Cursor position %d, %d", new_position[0], new_position[1])


class C64(Computer):

    line_size = 18

    def __init__(self, screen):
        super().__init__(Constants.BLUE, Constants.LIGHT_BLUE)
        self.screen = screen
        self.screenshot = None
        self.location = (52, 77)
        self.background_bitmap = Utils.load_background("src/main/resources/c64slim.png")        
        self.font_path = "src/main/resources/C64_Pro_Mono-STYLE.ttf"
        self.caption_font = ImageFont.truetype(self.font_path, 18)
        self.cursor = Cursor(self.location)
        self.one_letter = Image.new("RGB", (C64.line_size, C64.line_size), Constants.BLUE)#Constants.LIGHT_BLUE)
        self.draw = ImageDraw.Draw(self.one_letter)
        self.caption_surface = pygame.image.fromstring(self.one_letter.tobytes(), self.one_letter.size, self.one_letter.mode)


    def draw_background(self):
        self.screen.fill(Constants.LIGHT_BLUE)        
        self.screen.blit(self.background_bitmap, self.location)
        pygame.display.flip()


    def blink_cursor(self):
        self.cursor.on = not self.cursor.on
        pygame.draw.rect(self.screen, self.cursor.blink_color(), (self.cursor.get_screen_position(), (C64.line_size, C64.line_size)))

        pygame.display.flip()


    def handle_cursor(self, duration_ms):
        start_time = pygame.time.get_ticks()
        self.draw_background()

        while pygame.time.get_ticks() - start_time <= duration_ms:            
            self.blink_cursor()
            
            self.clock.tick(40)


    def toggle_screen(self, duration_ms):
        self.take_screenshot()
        self.screen.fill(Constants.LIGHT_BLUE)
        pygame.display.flip()
        pygame.time.delay(duration_ms)
        
        self.screen.blit(self.screenshot, (0, 0))
        pygame.display.flip()
        
    
    def take_screenshot(self):
        self.screenshot = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        self.screenshot.blit(self.screen, (0, 0))


    def writeline(self, caption_text):
        caption_image = Image.new("RGB", (20 * len(caption_text), C64.line_size), Constants.BLUE)

        draw = ImageDraw.Draw(caption_image)
        draw.text((0, 0), caption_text, font=self.caption_font, fill=Constants.LIGHT_BLUE)

        caption_surface = pygame.image.fromstring(caption_image.tobytes(), caption_image.size, caption_image.mode)
        self.screen.blit(caption_surface, self.cursor.get_screen_position())
        pygame.display.flip()
        self.cursor.move_down()


    def punch(self, duration_ms):
        self.karateka.punch()
        self.draw_sprite()
        pygame.time.delay(duration_ms)


    def open_passage(self, duration_ms):
        height = 76
        position = (self.location[0] + self.background_bitmap.get_width() - 10, self.location[1] + self.background_bitmap.get_height() - height)
        logging.info("Opening portal at %d, %d", position[0], position[1])
        pygame.draw.rect(self.screen, Constants.BLUE, (position, (64, height)))
        pygame.display.flip()
        pygame.time.delay(duration_ms)
        
    
    def get_catwalk_rect(self):
        x1 = self.location[0]
        y1 = self.location[1] + self.background_bitmap.get_height() - 80
        x2 = 2 * self.location[0] + self.background_bitmap.get_width() + 5
        y2 = 80

        return pygame.Rect(x1, y1, x2, y2)
