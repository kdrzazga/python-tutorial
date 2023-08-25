import pygame

CYAN = (0, 255, 255)
BLACK = (0, 0, 0)

pygame.init()

class UI:
    def __init__(self, game):
        self.game = game
        self.cell_size = 20
        self.player_image = pygame.image.load("resources/player.png")

        screen_width = game.board.width * self.cell_size
        screen_height = game.board.height * self.cell_size
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Game UI")

    def draw_field(self, field):
        x = field.x * self.cell_size
        y = field.y * self.cell_size
        pygame.draw.rect(self.screen, CYAN, (x, y, self.cell_size, self.cell_size))
        pygame.draw.rect(self.screen, BLACK, (x + 3, y + 3, self.cell_size - 6, self.cell_size - 6))

    def draw(self):
        self.screen.fill((255, 255, 255))

        for x in range(self.game.board.width):
            for y in range(self.game.board.height):
                field = self.game.board.fields[x][y]
                if field.revealed:
                    self.draw_field(field)
