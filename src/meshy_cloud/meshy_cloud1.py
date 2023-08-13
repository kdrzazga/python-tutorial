import sys

import pygame

pygame.init()

screen_width = 800
screen_height = 600

black = (0, 0, 0)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Meshy Cloud")

ellipse_center = (screen_width // 2, screen_height // 2)
ellipse_width = 200
ellipse_height = 100

running = True
clock = pygame.time.Clock()


def is_inside_ellipse(x, y):
    return ((x - ellipse_center[0]) / ellipse_width) ** 2 + ((y - ellipse_center[1]) / ellipse_height) ** 2 <= 1


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)

    for x in range(ellipse_center[0] - ellipse_width, ellipse_center[0] + ellipse_width + 1):
        for y in range(ellipse_center[1] - ellipse_height, ellipse_center[1] + ellipse_height + 1):
            if is_inside_ellipse(x, y):
                if (x + y) % 2 == 0:
                    screen.set_at((x, y), (255, 255, 255))
            else:
                continue

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
