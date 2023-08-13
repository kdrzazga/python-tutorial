import pygame
import sys
import math

pygame.init()

screen_width = 800
screen_height = 600

black = (0, 0, 0)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Meshy Cloud")

ellipse_center = (screen_width // 2, screen_height // 2)
ellipse_width = 200
ellipse_height = 100

rectangle_size = 1

running = True
clock = pygame.time.Clock()


def is_inside_ellipse(x, y):
    return ((x - ellipse_center[0]) / ellipse_width) ** 2 + ((y - ellipse_center[1]) / ellipse_height) ** 2 <= 1


def draw_mesh_rect(x, y):
    for i in range(rectangle_size):
        for j in range(rectangle_size):
            pixel_x = x + i
            pixel_y = y + j
            if is_inside_ellipse(pixel_x, pixel_y):
                if (pixel_x + pixel_y) % 2 == 0:
                    pygame.draw.rect(screen, (255, 255, 255), (pixel_x, pixel_y, 1, 1))


def meshy_ellipse_high():
    for x in range(ellipse_center[0] - ellipse_width, ellipse_center[0] + ellipse_width + 1, rectangle_size):
        for y in range(ellipse_center[1] - ellipse_height, ellipse_center[1] + ellipse_height + 1, rectangle_size):
            if is_inside_ellipse(x, y):
                if (x + y) % (rectangle_size * 2) == 0:
                    pygame.draw.rect(screen, (255, 255, 255), (x, y - ellipse_height, rectangle_size, rectangle_size))
            else:
                screen.set_at((x, y - ellipse_height), (255, 255, 255))
                continue

    pygame.display.flip()


def meshy_ellipse_low():
    for x in range(ellipse_center[0] - ellipse_width, ellipse_center[0] + ellipse_width + 1, rectangle_size):
        for y in range(ellipse_center[1] - ellipse_height, ellipse_center[1] + ellipse_height + 1, rectangle_size):
            draw_mesh_rect(x, y)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)

    meshy_ellipse_high()
    # meshy_ellipse_low()

    rectangle_size = (rectangle_size + 1) % 28 + 1
    clock.tick(8)

pygame.quit()
sys.exit()
