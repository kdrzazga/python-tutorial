import logging
import pygame
import os

from src.constants import Constants

from PIL import Image, ImageDraw, ImageFont

BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
WHITE = (250, 250, 250)
YELLOW = (238, 238, 119)
BACKGROUND = (74, 74, 73)


class Grapher:

    initial_sprite_pos = (Constants.screen_height * 83) // 100

    title = "INTERNATIONAL PY-RATE"

    def __init__(self):
        self.sprite_bitmap = None
        self.window = pygame.display.set_mode((Constants.screen_width, Constants.screen_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(Constants.title)

    def draw_background(self):
        background_bitmap = pygame.image.load("src/resources/board.png")

        double_bitmap = pygame.Surface((background_bitmap.get_width(), background_bitmap.get_height()))
        double_bitmap.blit(background_bitmap, (0, 0))

        self.window.blit(background_bitmap, (0, 0))
        pygame.display.flip()

    def draw_sprite(self, sprite):
        path = sprite.get_sprite_path()
        self.sprite_bitmap = pygame.image.load(path).convert_alpha()

        x = sprite.x - self.sprite_bitmap.get_width()/2
        y = sprite.y - self.sprite_bitmap.get_height()/2
        
        self.window.blit(self.sprite_bitmap, (x, y))
        pygame.display.update()

    def clear_sprite(self):
        pass
        #x = Constants.screen_width/2 - self.sprite_bitmap.get_width()/2
        #y = Constants.initial_sprite_pos - self.sprite_bitmap.get_height()/2
        #pygame.draw.rect(self.window, Constants.BACKGROUND, (x, y, self.sprite_bitmap.get_width(), self.sprite_bitmap.get_height()))
