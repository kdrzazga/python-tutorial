import pygame

class Cloud:

    BACKGROUND = (1, 1, 254)
    WHITE = (254, 254, 254)

    def __init__(self, x, y, width, height, screen, screen_width, screen_height):
        self.screen = screen
        self.ellipse_center = (x, y)
        self.ellipse_width = width
        self.ellipse_height = height

        self.rectangle_size = 13

        
    def is_inside_ellipse(self, x, y):
        return ((x - self.ellipse_center[0]) / self.ellipse_width) ** 2 + ((y - self.ellipse_center[1]) / self.ellipse_height) ** 2 <= 1
    
    
    def draw_mesh_rect(self):
        for x in range(self.ellipse_center[0] - self.ellipse_width, self.ellipse_center[0] + self.ellipse_width + 1, self.rectangle_size):
            for y in range(self.ellipse_center[1] - self.ellipse_height, self.ellipse_center[1] + self.ellipse_height + 1, self.rectangle_size):
                    if (x + y) % 2 == 0:
                        pygame.draw.rect(self.screen, Cloud.WHITE, (x, y - self.ellipse_height, self.rectangle_size, self.rectangle_size))
    
    def draw(self):
        self.draw_mesh_rect()
        
        for x in range(self.ellipse_center[0] - self.ellipse_width, self.ellipse_center[0] + self.ellipse_width + 1, self.rectangle_size):
            for y in range(self.ellipse_center[1] - self.ellipse_height, self.ellipse_center[1] + self.ellipse_height + 1, self.rectangle_size):
                if not self.is_inside_ellipse(x, y):
                    if (x + y) % (self.rectangle_size * 2) != 0:
                        pygame.draw.rect(self.screen, Cloud.BACKGROUND, (x, y - self.ellipse_height, 56 - self.rectangle_size, 56 - self.rectangle_size))
                    continue
        pygame.display.flip()

    def move_left(self, shift):
        self.ellipse_center = (self.ellipse_center[0] + shift, self.ellipse_center[1])
