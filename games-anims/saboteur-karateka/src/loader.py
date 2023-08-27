import pygame
import random
import time
import sys

from src.constants import Constants

class BitmapPiece:
    
    def __init__(self, x, y, surface):
        self.x = x
        self.y = y
        self.surface = surface

class Loader:


    def __init__(self, screen):
        self.bitmap_image = pygame.image.load("src/resources/board.png")
        self.screen = screen
        self.frames_per_second = 19
    
        self.rect_horiz_count = 20
        self.rect_vert_count = 20        
        self.cycles = 0
        

    def draw_background(self):
        self.screen.blit(self.bitmap_image, (0, 0))
        pygame.display.flip()


    def create_tiles(self):
        tiles = []

        rect_width = Constants.screen_width // self.rect_horiz_count
        rect_height = Constants.screen_height // self.rect_vert_count

        for y in range(self.rect_vert_count):
            for x in range(self.rect_horiz_count):
                rect_x, rect_y = x * rect_width, y * rect_height
                surface = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
                tiles.append(surface)

        return tiles


    def create_partial_bitmaps(self, tiles, current_frame):
        part_bitmaps = []
        random.shuffle(tiles)
    
        for i in range(current_frame, min(current_frame + self.frames_per_second, len(tiles))):
            surface = tiles[i]
            sub_bitmap = self.bitmap_image.subsurface(surface)
            part_bitmaps.append(BitmapPiece(surface.x, surface.y, sub_bitmap))
        
        return part_bitmaps

    def main(self):
        clock = pygame.time.Clock()
    
        current_frame = 0    
        bg_load_running = True        
        tiles = self.create_tiles()
    
        while bg_load_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    bg_load_running = False
    
            part_bitmaps = self.create_partial_bitmaps(tiles, current_frame)
    
            while len(part_bitmaps) > 0:
                random_part = part_bitmaps.pop()
                self.screen.blit(random_part.surface, (random_part.x, random_part.y))
    
            pygame.display.flip()
    
            current_frame += self.frames_per_second
            if current_frame >= len(tiles):
                current_frame = 0
                
            clock.tick(self.frames_per_second)
            if self.cycles == 100:
                self.draw_background()
                print('Image loaded')
                time.sleep(2)
                bg_load_running = False
            else:    
                self.cycles += 1
