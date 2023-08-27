import sys

import pygame

pygame.init()

screen_width = 800
screen_height = 600

BLACK = (0, 0, 0)
WHITE = (250, 250, 250)

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


def draw_mesh_rect():
    for x in range(ellipse_center[0] - ellipse_width, ellipse_center[0] + ellipse_width + 1, rectangle_size):
        for y in range(ellipse_center[1] - ellipse_height, ellipse_center[1] + ellipse_height + 1, rectangle_size):
            if (x + y) % 2 == 0:
                pygame.draw.rect(screen, WHITE, (x, y + ellipse_height, rectangle_size, rectangle_size))


def meshy_ellipse_high():
    for x in range(ellipse_center[0] - ellipse_width, ellipse_center[0] + ellipse_width + 1, rectangle_size):
        for y in range(ellipse_center[1] - ellipse_height, ellipse_center[1] + ellipse_height + 1, rectangle_size):
            if is_inside_ellipse(x, y):
                if (x + y) % (rectangle_size * 2) == 0:
                    pygame.draw.rect(screen, WHITE, (x, y - ellipse_height, rectangle_size, rectangle_size))
            else:
                screen.set_at((x, y - ellipse_height), WHITE)
                continue

    pygame.display.flip()


def meshy_ellipse_low():
    draw_mesh_rect()

    for x in range(ellipse_center[0] - ellipse_width, ellipse_center[0] + ellipse_width + 1, rectangle_size):
        for y in range(ellipse_center[1] - ellipse_height, ellipse_center[1] + ellipse_height + 1, rectangle_size):
            if not is_inside_ellipse(x, y):
                if (x + y) % (rectangle_size * 2) != 0:
                    pygame.draw.rect(screen, BLACK, (x, y + ellipse_height, 56 - rectangle_size, 56 - rectangle_size))
                continue
    pygame.display.flip()


def write_rect_size(rectangle_size):
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    text_surface = font.render("rect = " + str(rectangle_size), True, WHITE)
    screen.blit(text_surface, (50, 50))
    pygame.display.flip()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    meshy_ellipse_high()
    meshy_ellipse_low()

    write_rect_size(rectangle_size)

    rectangle_size = (rectangle_size + 1) % 28 + 1
    clock.tick(1)

pygame.quit()
sys.exit()
