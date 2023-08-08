import pygame
import os

from player import Player
from enemy import Enemy
from board import Board
from PIL import Image, ImageDraw, ImageFont

BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
WHITE = (250, 250, 250)
YELLOW = (238, 238, 119)

class Drawer:

    platform_path = "resources/floor.png"
    ladder_path = "resources/ladder.png"
    
    width = 800
    window_height = 600
    board_height = window_height * 90 //100
    cell_width = width // Board.sizeX
    cell_height = board_height // Board.sizeY
    
    title = "ULTIMATE WIZARD"

    def __init__(self):
        self.window = pygame.display.set_mode((Drawer.width, Drawer.window_height))
        self.clock = pygame.time.Clock()
        self.font_path = os.path.join("resources", "font.ttf")
        self.caption_font = ImageFont.truetype(self.font_path, 12)
        self.caption_font2 = ImageFont.truetype(self.font_path, 16)
        self.caption_text_height = 12*3
        self.caption_text_background = BLACK
        self.caption_text_color1 = YELLOW
        self.caption_text_color3 = WHITE
        self.caption_text_color2 = CYAN

        pygame.display.set_caption(Drawer.title)

    def draw_board(self, board):
        self.draw_sprite(Player.sprite_path, board.player.x, board.player.y)
        self.draw_sprite(Enemy.sprite_path, board.enemy.x, board.enemy.y)   

        for cell_x, cell_y in board.ladders:
            print("Ladder:", str(cell_x), str(cell_y))
            self.draw_sprite(Drawer.ladder_path, cell_x, cell_y)        
        
        for cell_x, cell_y in board.platforms:
            print("Platform:", str(cell_x), str(cell_y))
            self.draw_platform(cell_x, cell_y)
            
        board.move_down(board.player)
        board.move_down(board.enemy)

    def draw_platform(self, x, y):
        platform_bitmap = pygame.image.load(Drawer.platform_path)
    
        x = x * Drawer.cell_width
        y = (y + 1) * Drawer.cell_height - 8 #height of platform is supposed to be drawn on the bottom of cell
    
        self.window.blit(platform_bitmap, (x, y))
        pygame.display.update() 
    
    def draw_sprite(self, sprite_path, x, y):
        sprite_bitmap = pygame.image.load(sprite_path).convert_alpha()
    
        x = x * Drawer.cell_width
        y = y * Drawer.cell_height
    
        self.window.blit(sprite_bitmap, (x, y))
        pygame.display.update()    

    def draw_info(self, info):
        caption_image = Image.new("RGB", (self.width, self.caption_text_height), self.caption_text_background)
        
        draw = ImageDraw.Draw(caption_image)
        draw.text((10, 0), info.title, font=self.caption_font2, fill=self.caption_text_color1)
        draw.text((85 * Drawer.width // 100, 0), "SCORE:", font=self.caption_font, fill=self.caption_text_color2)
        draw.text((85 * Drawer.width // 100, 15), str(info.score), font=self.caption_font, fill=self.caption_text_color2)
        draw.text((50 * Drawer.width // 100, 0), "SPELLS:", font=self.caption_font, fill=self.caption_text_color3)
        draw.text((50 * Drawer.width // 100, 15), str(info.spells), font=self.caption_font, fill=self.caption_text_color3)

        caption_surface = pygame.image.fromstring(caption_image.tobytes(), caption_image.size, caption_image.mode)
        self.window.blit(caption_surface, (0, Drawer.board_height))
        pygame.display.update()
    
    def main_loop(self, board, info):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        
        pygame.display.update()
        self.clock.tick(150)
        