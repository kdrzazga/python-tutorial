import pygame
from pygame import Surface, Rect


class Constants:
    WIDTH, HEIGHT = 800, 600
    LIGHT_BLUE = (96, 96, 192)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 255)
    BROWN = (185, 122, 85)
    PURPLE = (200, 130, 200)
    YELLOW = (255, 255, 0)
    BLUE = (32, 0, 128)
    AMIGA_BLUE = (0, 96, 192)
    SCREEN_WIDTH = 800 - 2 * 52
    SCREEN_HEIGHT = 400
    KARATEKA_Y = 483


class Utils:
    color_index = 0

    @staticmethod
    def get_next_color() -> tuple[int, int, int]:
        available_colors = (Constants.GREEN, Constants.WHITE, Constants.CYAN, Constants.RED, Constants.YELLOW, (34, 177, 76), Constants.PURPLE, Constants.BROWN)
        Utils.color_index = (Utils.color_index + 1) % len(available_colors)
        return available_colors[Utils.color_index]

    @staticmethod
    def load_background(path) -> Surface:
        return pygame.image.load(path)

    @staticmethod
    def color_bitmap(bitmap, color) -> Surface:
        old_color = (255, 255, 255)
        new_image: Surface = bitmap.copy()

        width, height = bitmap.get_size()

        for x in range(width):
            for y in range(height):
                pixel_color: tuple[int, int, int] = bitmap.get_at((x, y))
                if pixel_color == old_color:
                    new_image.set_at((x, y), color)
        return new_image


class ClearScreen:

    @staticmethod
    def clear(screen):
        screen = pygame.display.set_mode((screen.get_width(), screen.get_height()))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((0, 0, 100))
            pygame.display.flip()

    @staticmethod
    def create_screen_tiles(width, height) -> set:
        tiles = set()
        tile_size = 50
        for y in range(0, height, tile_size):
            for x in range(0, width, tile_size):
                tiles.add((x, y, tile_size, tile_size))

        return tiles

    @staticmethod
    def tile_screen(screen: Surface, color):
        clock = pygame.time.Clock()
        tiles: set[Rect] = ClearScreen.create_screen_tiles(screen.get_width(), screen.get_height())
        while len(tiles) > 0:
            pygame.draw.rect(screen, color, tiles.pop())
            pygame.display.flip()
            clock.tick(240)
