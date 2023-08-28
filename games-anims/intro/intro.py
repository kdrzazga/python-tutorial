import math
import sys
import pygame
import threading

class Intro:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.CENTER_X, self.CENTER_Y = self.WIDTH // 4, self.HEIGHT // 3
        self.RADIUS = 0.05
        self.NUM_CIRCLES = 450
        self.LOW_LIMIT = self.HEIGHT * 60 // 100
        self.BG_COLOR = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (200, 44, 44)
        self.LIGHT_YELLOW = (255, 255, 150)

        self.bitmap = pygame.image.load('resources/bkgnd.png')

        pygame.init()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Light Point")

        self.light_point = pygame.Surface((1, 1))
        self.light_point.fill(self.WHITE)

        self.running = True

        self.game_thread = threading.Thread(target=self.main_loop)
        self.text_thread = threading.Thread(target=self.write_text_thread)

        self.game_thread.start()
        self.text_thread.start()

    def draw_ray_ring(self, screen, color, center, radius, transparency):
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
                pygame.draw.rect(screen, new_color, (100 + x_int, 50 + y_int, thickness, thickness))

    def main_loop(self):
        clock = pygame.time.Clock()
        alpha = 0
        while self.running:
            self.screen.blit(self.bitmap, (100, 50))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            alpha = (alpha + 3) % 360
            horiz_radius = 7
            vert_radius = 3
            dx = horiz_radius * math.sin(math.radians(alpha))
            dy = vert_radius * math.cos(math.radians(alpha))

            self.CENTER_X += dx
            self.CENTER_Y += dy

            self.screen.fill(self.BG_COLOR, (0, 0, self.WIDTH, self.HEIGHT - 40))

            for i in range(self.NUM_CIRCLES, 50, -1):
                r = max(0, self.LIGHT_YELLOW[0] - i * 0.6)
                g = max(0, self.LIGHT_YELLOW[1] - i * 1.9)
                b = max(0, self.LIGHT_YELLOW[2] - i * 0.5)
                color = (r, g, b)
                radius = self.RADIUS + i
                transparency = 250
                self.draw_ray_ring(self.screen, color, (self.CENTER_X, self.CENTER_Y), radius, transparency)

            self.screen.blit(self.light_point, (self.CENTER_X, self.CENTER_Y))

            pygame.display.flip()

            clock.tick(5)

        pygame.quit()
        sys.exit()

    def write_text_thread(self):
        font = pygame.font.Font(None, 36)
        text = "           Black hole sun, won't you come         "
        text_surface_low = font.render(text, True, self.RED)
        text_surface_hi = font.render("Black hole sun, won't you come And wash away the rain? Black hole sun, won't you come? Won't you come? Black hole sun, won't you come               ", True, self.RED)
        text_x = self.WIDTH
        text_x_hi = self.WIDTH
        
        while self.running:
            self.screen.fill(self.BG_COLOR, (0, self.HEIGHT - 70, self.WIDTH, 70))
        
            text_width = text_surface_low.get_width()
            text_x -= 5  # Adjust the scrolling speed by changing this value
            text_x_hi -= 3
        
            if text_x + text_width < -40:
                text_x = self.WIDTH
                text_x_hi = self.WIDTH
        
            self.screen.blit(text_surface_low, (text_x, self.HEIGHT - 30))
            self.screen.blit(text_surface_hi, (text_x_hi, self.HEIGHT - 70))
            pygame.display.flip()
            pygame.time.delay(4)
        

if __name__ == "__main__":
    intro = Intro()
    intro.game_thread.join()
    intro.text_thread.join()
