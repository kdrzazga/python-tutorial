import random

import pygame
from pygame import Surface
from pygame.locals import *

pygame.init()


class Tile:

    def __init__(self, x, y, bitmap: Surface):
        self.x = x
        self.y = y
        self.bitmap = bitmap


class Globals:
    LIGHT_BLUE = (96, 96, 192)
    WHITE = (155, 155, 155)
    RED = (155, 0, 0)
    GREEN = (0, 155, 0)
    CYAN = (0, 155, 155)
    BROWN = (85, 22, 8)
    PURPLE = (100, 30, 100)
    YELLOW = (155, 155, 0)
    BLUE = (32, 0, 128)
    color_index = 0


def color_bitmap(bitmap, color):
    old_color = (255, 255, 255)
    new_image = bitmap.copy()

    width, height = bitmap.get_size()

    for x in range(width):
        for y in range(height):
            pixel_color = bitmap.get_at((x, y))
            if pixel_color == old_color:
                new_image.set_at((x, y), color)
    return new_image


def get_next_color() -> tuple[int, int, int]:
    available_colors: tuple = (
        Globals.GREEN, Globals.WHITE, Globals.CYAN, Globals.RED, Globals.YELLOW, (34, 177, 76), Globals.PURPLE,
        Globals.BROWN)
    Globals.color_index = (Globals.color_index + 1) % len(available_colors)
    return available_colors[Globals.color_index]


BITMAP_SIZE = 700
TILE_SIZE = BITMAP_SIZE // 175
TILES_PER_ROW = 175
TILES_PER_COL = 175
TOTAL_TILES = TILES_PER_ROW * TILES_PER_COL

screen = pygame.display.set_mode((BITMAP_SIZE, BITMAP_SIZE))
bitmap_surface = pygame.image.load('tree.bmp').convert()
pygame.display.set_caption("Animating Tiles")

bitmap_surface = pygame.transform.scale(bitmap_surface, (BITMAP_SIZE, BITMAP_SIZE))

tiles: list[Tile] = []
for i in range(TILES_PER_ROW):
    for j in range(TILES_PER_COL):
        tile_surface = Surface((TILE_SIZE, TILE_SIZE))
        tile_surface.blit(bitmap_surface, (0, 0), (i * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        tiles.append(Tile(i, j, tile_surface))

tiles_backup: list[Tile] = tiles.copy()
running = True
clock = pygame.time.Clock()

fps = 1500
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    random_tile_index = random.randint(0, len(tiles) - 1)
    random_tile: Tile = tiles[random_tile_index]
    if len(tiles) > 1:
        tiles.remove(random_tile)
    else:
        tiles = tiles_backup.copy()
        print("Tiles list recovered.")

    random_tile.bitmap = color_bitmap(random_tile.bitmap, get_next_color())
    screen.blit(random_tile.bitmap, (random_tile.x * TILE_SIZE, random_tile.y * TILE_SIZE))

    pygame.display.flip()
    clock.tick(fps)
    fps += 150

    if fps > 10000:
        fps = 10000

pygame.quit()
