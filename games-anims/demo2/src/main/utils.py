import pygame

class Constants:
    LIGHT_BLUE = (96, 96, 192)
    BLUE = (32, 0, 128)
    AMIGA_BLUE = (0, 96, 192)
    SCREEN_WIDTH = 800-2*52
    SCREEN_HEIGHT = 400

class Utils:

    @staticmethod
    def load_background(path):
        return pygame.image.load(path)


class ClearScreen:

    @staticmethod
    def create_screen_tiles(width, height):
        tiles = set()
        tile_size = 50
        for y in range(0, height, tile_size):
            for x in range(0, width, tile_size):
                tiles.add((x, y, tile_size, tile_size))
        
        return tiles

    @staticmethod
    def tile_screen(screen, color):
        clock = pygame.time.Clock()
        tiles = ClearScreen.create_screen_tiles(screen.get_width(), screen.get_height())
        while len(tiles) > 0:
            pygame.draw.rect(screen, color, tiles.pop())
            pygame.display.flip()
            clock.tick(240)  