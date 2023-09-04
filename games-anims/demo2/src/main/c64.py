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
        time.sleep(6)
        

class C64(Computer):

    line_size = 18

    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.location = (52, 77)
        self.font_path = "src/main/resources/C64_Pro_Mono-STYLE.ttf"
        self.caption_font = ImageFont.truetype(self.font_path, 18)
        self.cursor = Cursor(self.location)
        self.one_letter = Image.new("RGB", (C64.line_size, C64.line_size), Constants.BLUE)#Constants.LIGHT_BLUE)
        self.draw = ImageDraw.Draw(self.one_letter)
        self.caption_surface = pygame.image.fromstring(self.one_letter.tobytes(), self.one_letter.size, self.one_letter.mode)
        
    
    def draw_background(self):
        self.screen.fill(Constants.LIGHT_BLUE)
        background_bitmap = Utils.load_background("src/main/resources/c64slim.png")
        self.screen.blit(background_bitmap, self.location)
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


    def write(self, letter):
        point = self.cursor.get_screen_position()
        pygame.draw.rect(self.screen, Constants.BLUE, (point, (C64.line_size, C64.line_size)))
        
        self.draw.text((0, 0), letter, font=self.caption_font, fill = Constants.LIGHT_BLUE)
        self.screen.blit(self.caption_surface, point)
        
        pygame.display.update()
        self.cursor.move_right()
        
    def writeline(self, text):
        caption_text = "PRESS PLAY ON TAPE"
        
        caption_image = Image.new("RGB", (self.cursor.get_screen_position()[0], C64.line_size), Constants.BLUE)
        
        draw = ImageDraw.Draw(caption_image)
        draw.text((0, 0), caption_text, font=self.caption_font, fill=Constants.BLUE)

        caption_surface = pygame.image.fromstring(caption_image.tobytes(), caption_image.size, caption_image.mode)
        self.screen.blit(caption_surface, self.cursor.get_screen_position())
        pygame.display.flip()
        self.cursor.move_right()
