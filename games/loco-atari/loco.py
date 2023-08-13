import logging
import pygame

from level_manager import LevelManager
from cloud import Cloud

def keys_input():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN] or keys[pygame.K_SPACE] or keys[pygame.K_RSHIFT] or keys[pygame.K_RALT] \
        or keys[pygame.K_RCTRL]:
        logging.info("key pressed")
        cloud = Cloud(canvas_width // 2, 100, 100, 50, screen, canvas_width, canvas_height)
        cloud.draw()

BLACK = (0, 0, 0)
BLUE = (1, 1, 254)

pygame.init()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

level_mgr = LevelManager()

canvas_width = 1202
canvas_height = 600
screen = pygame.display.set_mode((canvas_width, canvas_height))
pygame.display.set_caption("atari LOCO")

railroad_bitmap = pygame.image.load("resources/railroad.png")
loco_bitmap = pygame.image.load("resources/loco.png")

double_bitmap_width = railroad_bitmap.get_width() * 2
double_bitmap = pygame.Surface((double_bitmap_width, railroad_bitmap.get_height()))
double_bitmap.blit(railroad_bitmap, (0, 0)) #constant background
double_bitmap.blit(railroad_bitmap, (railroad_bitmap.get_width(), 0)) #animated background

background_x = 0
running = True
clock = pygame.time.Clock()
scroll_speed = 5

screen.fill(BLACK)
blue_rectLB = pygame.Rect(0, 91, 530, 183)
pygame.draw.rect(screen, BLUE, blue_rectLB)  # constant background
blue_rectR = pygame.Rect(canvas_width - 472, 0, canvas_width, 294)
pygame.draw.rect(screen, BLUE, blue_rectR)   # constant background


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(loco_bitmap, (0,182))
    pygame.display.update()
    screen.blit(double_bitmap, (background_x, 294))    

    background_x -= scroll_speed
    if background_x <= -railroad_bitmap.get_width():
        background_x = 0

    keys_input()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
