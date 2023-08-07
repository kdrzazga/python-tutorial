import pygame

from player import Player
from enemy import Enemy

class Drawer:
    
    width = 800
    window_height = 600
    board_height = window_height * 86 //100
    title = "ULTIMATE WIZARD"

    def __init__(self):
        self.window = pygame.display.set_mode((Drawer.width, Drawer.window_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(Drawer.title)

    def draw_board(self, board):
        self._draw_player(board.player)
        self._draw_enemy(board.enemy)

    def _draw_player(self, player):
        player_bitmap = pygame.image.load(Player.sprite_path).convert_alpha()
        image_width, image_height = player_bitmap.get_size()
        self.window.blit(player_bitmap, (player.x, player.y))
        pygame.display.update()
        
    def _draw_enemy(self, player):
        player_bitmap = pygame.image.load(Enemy.sprite_path).convert_alpha()
        image_width, image_height = player_bitmap.get_size()
        self.window.blit(player_bitmap, (player.x, player.y))
        pygame.display.update()
        
    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        
        pygame.display.update()
        self.clock.tick(150)
        