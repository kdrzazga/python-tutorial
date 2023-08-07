import pygame

from player import Player
from enemy import Enemy
from board import Board

class Drawer:
    
    width = 800
    window_height = 600
    board_height = window_height * 86 //100
    cell_width = width // Board.sizeX
    cell_height = board_height // Board.sizeY
    
    title = "ULTIMATE WIZARD"

    def __init__(self):
        self.window = pygame.display.set_mode((Drawer.width, Drawer.window_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(Drawer.title)

    def draw_board(self, board):
        self.draw_sprite(Player.sprite_path, board.player.x, board.player.y)
        self.draw_sprite(Enemy.sprite_path, board.enemy.x, board.enemy.y)
    
    def draw_sprite(self, sprite_path, x, y):
        sprite_bitmap = pygame.image.load(sprite_path).convert_alpha()
    
        x = x * Drawer.cell_width
        y = y * Drawer.cell_height
    
        self.window.blit(sprite_bitmap, (x, y))
        pygame.display.update()    
        
    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        
        pygame.display.update()
        self.clock.tick(150)
        