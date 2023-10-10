import logging
import pygame
import random
import math

from PIL import Image, ImageDraw, ImageFont
from collections import deque
from itertools import cycle


class Scroll:
    BG_COLOR = (124, 112, 218)

    def __init__(self, screen, canvas_width, canvas_height, scroll_speed):
        self.image_path = "src/main/resources/eod.png"

        self.caption_font = ImageFont.truetype("src/main/resources/AGENCYR.ttf", 20)
        self.texts = deque(["written in python", "", "this demo is tribute to 8- and 16-bit games", "esp. to INTERNATIONAL KARATE", "", "greetings to K&A", "including Pan Areczek", ""], maxlen=9)
        self.text_color = (255, 0, 0)
        self.current_text = ""
        self._cyclic_iterator = cycle(self.texts)
        self.counter = 500
        self.square_size = 0
        self.cover_flag = False
        
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.scroll_speed = scroll_speed
        self.background_x = 0

        self.screen = screen
        self.clock = pygame.time.Clock()

        self.background_bitmap = pygame.image.load(self.image_path)
        self.double_bitmap_width = self.background_bitmap.get_width() * 2
        self.header_height = 40
        self.double_bitmap = pygame.Surface((self.double_bitmap_width, self.canvas_height))
        self.double_bitmap.blit(self.background_bitmap, (0, 0))
        self.double_bitmap.blit(self.background_bitmap, (self.background_bitmap.get_width(), 0))

        self.initial_dbl_bitmap = self.double_bitmap

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def update_display(self):
        self.background_x -= self.scroll_speed
        if self.background_x <= -self.background_bitmap.get_width():
            self.background_x = 0

        height_offset = (self.canvas_height - self.canvas_height / 2) * (
                    1 + math.sin(pygame.time.get_ticks() / 1000)) + 250
        height_offset = int(height_offset)

        self.double_bitmap = pygame.transform.scale(self.initial_dbl_bitmap, (self.double_bitmap_width, height_offset))

        desired_height = 560
        trimmed_image = pygame.Surface((self.double_bitmap.get_width(), desired_height))
        pygame.Surface.blit(trimmed_image, self.double_bitmap, (0, 0), (0, 0, self.double_bitmap.get_width(), desired_height))

        self.screen.fill(self.BG_COLOR)
        
        caption_surface = self.create_caption_surface(600, 50)
        
        self.screen.blit(caption_surface, (0, 0))
        self.screen.blit(self.double_bitmap, (self.background_x, self.header_height))

        pygame.display.flip()
        self.clock.tick(76)

    def create_caption_surface(self, width, height):
        font = pygame.font.Font(None, 36)
        rendered_text = font.render(self.get_text(), True, self.text_color)
        
        caption_surface = pygame.Surface((width, height))
        caption_surface.fill(self.BG_COLOR)
        caption_surface.blit(rendered_text, (10, 10))

        if self.cover_flag:
            caption_surface = self.create_text_cover(caption_surface)
        return caption_surface

    def get_color(self):
        return random.choice([(255, 0, 0), (0, 255, 0), (255, 255, 255), (255, 255, 0), (255, 0, 255)])

    def create_text_cover(self, caption_surface):
        self.adapt_square_size()
        spacing = 36
        for x in range(10, caption_surface.get_width(), spacing):
            for y in range(10, caption_surface.get_height(), spacing):
                pygame.draw.rect(caption_surface, self.BG_COLOR, (x, y, self.square_size //7, self.square_size //7))
        return caption_surface        

    def adapt_square_size(self):
        if self.square_size < 390 :
            self.square_size += 3
        else:
            self.square_size = 0

    def get_text(self):
        counter_max = 1499
        self.counter += 1
        if self.counter >= counter_max:
            self.counter = 0

        if self.counter % 100 == 0:
            self.cover_flag = True
            logging.info("Covering text")        
        
        if self.counter % 200 == 0:
            self.text_color = self.get_color()
            self.current_text = next(self._cyclic_iterator)
            logging.info("Covering done. Text changed to : %s", self.current_text)
            self.cover_flag = False
            self.square_size = 0
        
        return self.current_text

    def run(self, duration_ms):
        start_time = pygame.time.get_ticks()

        while pygame.time.get_ticks() - start_time <= duration_ms:
            running = self.handle_events()
            self.update_display()
            
        logging.info("END OF DEMO scrolling done")


if __name__ == "__main__":
    pygame.init()
    canvas_width = 800
    screen = pygame.display.set_mode((canvas_width, 600))
    pygame.display.set_caption("EoD")

    scroll_instance = Scroll(screen, canvas_width, canvas_height=368, scroll_speed=5)
    while True:
        scroll_instance.run(33000)

    pygame.quit()
