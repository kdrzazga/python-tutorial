import logging
import pygame
import os

#from helper import random_move, random_move_mostly_up
#from player import Player
#from enemy import Enemy
#from board import Board
from PIL import Image, ImageDraw, ImageFont

BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
WHITE = (250, 250, 250)
YELLOW = (238, 238, 119)


class Drawer:

    width = 800
    window_height = 600
    sprite_pos = window_height * 70 // 100

    title = "INTERNATION PYRATE"

    def __init__(self):
        self.window = pygame.display.set_mode((Drawer.width, Drawer.window_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(Drawer.title)

    def draw_background(self):
        background_bitmap = pygame.image.load("resources/board.png")

        double_bitmap = pygame.Surface((background_bitmap.get_width(), background_bitmap.get_height()))
        double_bitmap.blit(background_bitmap, (0, 0))
        double_bitmap.blit(background_bitmap, (background_bitmap.get_width(), 0))

        self.window.blit(double_bitmap, (0, 0))
        pygame.display.flip()

    def draw_sprite(self, player):
        sprite_bitmap = pygame.image.load(player.sprite_path).convert_alpha()

        x = Drawer.width/2 - sprite_bitmap.get_width()/2
        y = Drawer.sprite_pos - sprite_bitmap.get_width()/2

        self.window.blit(sprite_bitmap, (x, y))
        pygame.display.update()
        