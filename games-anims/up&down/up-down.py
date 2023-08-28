import logging

import pygame

from player_sprite import Player

BACKGROUND = (0, 0, 0)
PLAYER_COLOR = (12, 222, 222)


def get_color(x, y):
    screenshot = pygame.Surface(screen.get_size())
    screenshot.blit(screen, (0, 0))
    return screenshot.get_at((x, y))


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

pygame.init()
pygame.key.set_repeat(0, 0)

canvas_width = 800
canvas_height = 200
screen = pygame.display.set_mode((canvas_width, canvas_height))
pygame.display.set_caption("UP and DOWN")

background_bitmap = pygame.image.load("image.png")

double_bitmap_width = background_bitmap.get_width() * 2
double_bitmap = pygame.Surface((double_bitmap_width, background_bitmap.get_height()))
double_bitmap.blit(background_bitmap, (0, 0))
double_bitmap.blit(background_bitmap, (background_bitmap.get_width(), 0))

background_x = 0

player = Player()

running = True
clock = pygame.time.Clock()
scroll_speed = 8

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[ord('w')]:
        player.up()
    elif keys[pygame.K_DOWN] or keys[ord('s')]:
        player.down()

    screen.fill(BACKGROUND)

    screen.blit(double_bitmap, (background_x, 0))

    y = 0 if player.position == 'up' else double_bitmap.get_height() - player.height - 4

    pygame.draw.rect(screen, PLAYER_COLOR, (0, y, player.width, player.height))

    background_x -= scroll_speed
    if background_x <= -background_bitmap.get_width():
        background_x = 0

    y = 0 if player.position == 'up' else double_bitmap.get_height() - 4

    pixel_color = get_color(player.width, y)

    if get_color(player.width + 1, y) != BACKGROUND:
        logging.info("COLLISION")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
