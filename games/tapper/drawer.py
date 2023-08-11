import logging
import pygame
import os

from PIL import Image, ImageDraw, ImageFont

BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
WHITE = (250, 250, 250)
YELLOW = (238, 238, 119)
BACKGROUND = (172, 234, 140)

class Size:

    def __init__(self, width, height):
        self.width = width
        self.height = height

class Drawer:

    width = 1280
    window_height = 800
    initial_sprite_pos = (window_height * 83) // 100

    title = "TAPPER"

    def __init__(self, player):
        self.sprite_bitmap = pygame.image.load(player.get_sprite_path()).convert_alpha()
        self.window = pygame.display.set_mode((Drawer.width, Drawer.window_height))
        self.clock = pygame.time.Clock()
        self.bartender_size = Size(self.sprite_bitmap.get_width(), self.sprite_bitmap.get_height())
        
        pygame.display.set_caption(Drawer.title)

    def draw_background(self):
        background_bitmap = pygame.image.load("resources/background.png")

        bitmap = pygame.Surface((background_bitmap.get_width(), background_bitmap.get_height()))
        bitmap.blit(background_bitmap, (0, 0))

        self.window.blit(bitmap, (0, 0))
        pygame.display.flip()

    def draw_sprite(self, player):
        self.sprite_bitmap = pygame.image.load(player.get_sprite_path()).convert_alpha()

        x = self.sprite_bitmap.get_width()/2 - 5
        y = Drawer.initial_sprite_pos - self.sprite_bitmap.get_height()/2 + 5

        self.window.blit(self.sprite_bitmap, (x, y))
        pygame.display.update()

    def clear_bartender(self, player):
        x = 67
        y = Drawer.initial_sprite_pos - self.sprite_bitmap.get_height()/2 + 5

        pygame.draw.rect(self.window, BACKGROUND, (x, y, 69, self.bartender_size.height))
