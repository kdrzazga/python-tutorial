import logging
import pygame
import sys

from src.main.utils import Constants

class ScrollingTransition:
    TOTAL_DISTANCE = 12

    def __init__(self, screen):
        self.screen = screen
        self.screenshot = None
        self.clock = pygame.time.Clock()
        self.c64half = pygame.image.load("src/main/resources/c64half.png")

    def scroll_right(self):
        scroll_distance = 0
        scroll_speed = 1 / 6
        c64half_x = -Constants.WIDTH // 2
        self.screenshot = pygame.Surface((Constants.WIDTH, Constants.HEIGHT))
        self.screenshot.blit(self.screen, (0, 0))

        bitmap = pygame.Surface((3 * Constants.WIDTH // 2, Constants.HEIGHT))
        bitmap.blit(self.c64half, (0, 0))
        bitmap.blit(self.screenshot, (Constants.WIDTH // 2 - 1, 0))

        while c64half_x < 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(bitmap, (c64half_x, 0))
            pygame.display.flip()

            c64half_x += scroll_speed
            scroll_distance += scroll_speed

            if scroll_distance >= Constants.WIDTH:
                break
            pygame.time.delay(2)

    def scroll_and_fill(self):
        scroll_distance = 0
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screenshot = pygame.Surface((Constants.WIDTH, Constants.HEIGHT))
            self.screenshot.blit(self.screen, (0, 0))

            if scroll_distance < self.TOTAL_DISTANCE:
                scroll_distance += 1
                self.screen.fill(Constants.LIGHT_BLUE)
                self.screen.blit(self.screenshot, (0, -scroll_distance))

            if scroll_distance == self.TOTAL_DISTANCE:
                self.scroll_right()
                running = False

            pygame.display.flip()
            self.clock.tick(18)

    def draw_background(self, path):
        background_image = pygame.image.load(path)
        self.screen.blit(background_image, (0, 0))
        pygame.display.flip()
        
    def run(self):
        self.scroll_and_fill()
        pygame.time.delay(2000)
        logging.info("Scrolling transition done")

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
    pygame.display.set_caption("Scroll and Fill")
    scrolling_transition = ScrollingTransition(screen)
    scrolling_transition.draw_background("src/main/resources/amiga.png")
    scrolling_transition.run()

    pygame.quit()
    sys.exit()
