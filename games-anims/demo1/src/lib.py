import pygame

class ClearScreen:

    @staticmethod
    def create_screen_tiles(width: int, height: int) -> set[tuple[int, int, int, int]]:
        tiles = set()
        tile_size = 50
        for y in range(0, height, tile_size):
            for x in range(0, width, tile_size):
                tiles.add((x, y, tile_size, tile_size))
        
        return tiles

    @staticmethod
    def tile_screen(screen, color: tuple[int, int, int]):
        clock = pygame.time.Clock()
        tiles: set[tuple[int, int, int, int]] = ClearScreen.create_screen_tiles(screen.get_width(), screen.get_height())
        while len(tiles) > 0:
            pygame.draw.rect(screen, color, tiles.pop())
            pygame.display.flip()
            clock.tick(240)    
