import pygame

from level_manager import LevelManager

BLACK = (0, 0, 0)
BLUE = (1, 1, 254)

pygame.init()

level_mgr = LevelManager()

canvas_width = 1202
canvas_height = 600
screen = pygame.display.set_mode((canvas_width, canvas_height))
pygame.display.set_caption("atari LOCO")

railroad_bitmap = pygame.image.load("resources/railroad.png")
loco_bitmap = pygame.image.load("resources/loco.png")

double_bitmap_width = railroad_bitmap.get_width() * 2
double_bitmap = pygame.Surface((double_bitmap_width, railroad_bitmap.get_height()))
double_bitmap.blit(railroad_bitmap, (0, 0))
double_bitmap.blit(railroad_bitmap, (railroad_bitmap.get_width(), 0))

background_x = 0
running = True
clock = pygame.time.Clock()
scroll_speed = 5

screen.fill(BLACK)
blue_rect1 = pygame.Rect(0, 0, 500, 294)
pygame.draw.rect(screen, BLUE, blue_rect1)
blue_rect2 = pygame.Rect(canvas_width - 400, 0, canvas_width, 294)
pygame.draw.rect(screen, BLUE, blue_rect2)
    
    
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
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
