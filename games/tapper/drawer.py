import logging
import pygame
import os

from PIL import Image, ImageDraw, ImageFont

BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
WHITE = (250, 250, 250)
YELLOW = (238, 238, 119)
BACKGROUND = (74, 74, 73)

class Drawer:

    width = 1280
    window_height = 800
    initial_sprite_pos = (window_height * 83) // 100

    title = "TAPPER"

    def __init__(self):
        self.sprite_bitmap = None
        self.window = pygame.display.set_mode((Drawer.width, Drawer.window_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(Drawer.title)

    def draw_background(self):
        background_bitmap = pygame.image.load("resources/background.png")

        double_bitmap = pygame.Surface((background_bitmap.get_width(), background_bitmap.get_height()))
        double_bitmap.blit(background_bitmap, (0, 0))
        #double_bitmap.blit(background_bitmap, (background_bitmap.get_width(), 0))

        self.window.blit(double_bitmap, (0, 0))
        pygame.display.flip()

    def draw_sprite(self, player):
        self.sprite_bitmap = pygame.image.load(player.sprite_path).convert_alpha()

        x = self.sprite_bitmap.get_width()/2 - 5
        y = Drawer.initial_sprite_pos - self.sprite_bitmap.get_height()/2 + 5
        
        self.window.blit(self.sprite_bitmap, (x, y))
        pygame.display.update()
        