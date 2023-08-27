import pygame
import math
import sys

from src.constants import Constants

class LightPointAnimation:
    def __init__(self, screen):
        self.screen = screen
        self.counter = 0
        self.CENTER_X, self.CENTER_Y = Constants.WIDTH // 4, Constants.HEIGHT // 3
        self.RADIUS = 0.05
        self.NUM_CIRCLES = 450
        self.LOW_LIMIT = Constants.HEIGHT * 60 // 100
        self.BG_COLOR = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.LIGHT_YELLOW = (255, 255, 150)

        self.bitmap = pygame.image.load('src/resources/bkgnd.png')

        pygame.display.set_caption("Light Point")

        self.light_point = pygame.Surface((1, 1))
        self.light_point.fill(self.WHITE)

        self.clock = pygame.time.Clock()
        self.alpha = 0
        
        self.running = True

    def draw_ray_ring(self, color, center, radius, transparency):
        thickness = 2
        
        for angle in range(0, 360, 1):
            x = radius * math.sin(math.radians(angle)) + center[0]
            y = radius * math.cos(math.radians(angle)) + center[1]

            x_int, y_int = int(round(x)), int(round(y))
            
            bitmap_color = None
            
            if 0 <= x_int < self.bitmap.get_width() and 0 <= y_int < self.bitmap.get_height():
                bitmap_color = self.bitmap.get_at((x_int, y_int))
            
            r = int(color[0])
            g = int(color[1])
            b = int(color[2])
            
            new_color = (r, g, b, transparency)
            
            if bitmap_color != (0, 0, 0) and y_int < self.LOW_LIMIT:
                pygame.draw.rect(self.screen, new_color, (100 + x_int, 50 + y_int, thickness, thickness))

    def run(self):
        while self.running:
            self.screen.blit(self.bitmap, (100, 50))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.alpha = (self.alpha + 3) % 360
            horiz_radius = 7
            vert_radius = 3
            dx = horiz_radius * math.sin(math.radians(self.alpha))
            dy = vert_radius * math.cos(math.radians(self.alpha))

            self.CENTER_X += dx
            self.CENTER_Y += dy

            self.screen.fill(self.BG_COLOR)

            for i in range(self.NUM_CIRCLES, 0, -1):
                r = max(0, self.LIGHT_YELLOW[0] - i * 0.6)
                g = max(0, self.LIGHT_YELLOW[1] - i * 0.9)
                b = max(0, self.LIGHT_YELLOW[2] - i * 1.5)
                color = (r, g, b)
                radius = self.RADIUS + i
                transparency = 250
                self.draw_ray_ring(color, (self.CENTER_X, self.CENTER_Y), radius, transparency)

            self.screen.blit(self.light_point, (self.CENTER_X, self.CENTER_Y))

            pygame.display.flip()

            self.clock.tick(199)
            
            if self.counter == 100:
                self.running = False
            
            self.counter += 1


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
    animation = LightPointAnimation(screen)
    animation.run()
    pygame.quit()
    sys.exit()
    