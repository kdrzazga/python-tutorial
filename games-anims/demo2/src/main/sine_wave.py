import pygame
import sys
from collections import deque

class SineWaveAnimation:
    WIDTH, HEIGHT = 800, 600
    SCREEN_SIZE = (WIDTH, HEIGHT)
    WAVE_HEIGHT = HEIGHT // 4
    LINE_HEIGHT = 1
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        pygame.display.set_caption("Sine Wave Animation")

        self.background_image = pygame.image.load("resources/c64.png")
        self.background_image = pygame.transform.scale(self.background_image, self.SCREEN_SIZE)

        self.shift_table = 4*(1,) + 7*(2,) + 8*(3,) + 2*(0,) + 4*(-1,) + 7*(-2,) + 8*(-3,) + 2*(0,)
        self.shift_deque = deque(self.shift_table)

        self.clock = pygame.time.Clock()
        self.running = True

    def get_cyclical_value(self):
        self.shift_deque.rotate(-1)
        return self.shift_deque[0]

    def run_animation(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.blit(self.background_image, (0, 0))
            modified_image = self.background_image.copy()

            for y in range(0, self.WAVE_HEIGHT, self.LINE_HEIGHT):
                shift = self.get_cyclical_value()
                print(y, shift)
                subimage_rect = pygame.Rect(12, y, self.WIDTH - 24, self.LINE_HEIGHT)
                sub_image = self.background_image.subsurface(subimage_rect)
                modified_rect = subimage_rect.move(shift, 0)
                modified_image.blit(sub_image, modified_rect)

            self.screen.blit(modified_image, (0, 0))
            pygame.display.flip()

            self.clock.tick(3)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    animation = SineWaveAnimation()
    animation.run_animation()
