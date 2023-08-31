import pygame

class Constants:
    LIGHT_BLUE = (96, 96, 192)
    BLUE = (32, 0, 128)
    SCREEN_WIDTH = 800-2*52
    SCREEN_HEIGHT = 400

class Utils:

    @staticmethod
    def load_background(path):
        return pygame.image.load(path)
