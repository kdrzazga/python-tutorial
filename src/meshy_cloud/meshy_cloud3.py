import pygame
import sys
import math

from PIL import Image, ImageDraw, ImageFont

from cloud import Cloud

pygame.init()

screen_width = 800
screen_height = 600

BACKGROUND = (1, 1, 254)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Meshy Cloud")

ellipse_center = (screen_width // 2, screen_height // 2)
ellipse_width = 200
ellipse_height = 100

rectangle_size = 15

running = True
clock = pygame.time.Clock()

clouds = [Cloud(350, 390, ellipse_width, ellipse_height, screen, screen_width, screen_height),
          Cloud(250, 430, ellipse_width // 2, ellipse_height, screen, screen_width, screen_height),
          Cloud(150, 530, 88, 60, screen, screen_width, screen_height)]

cloud_index = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND)

    clouds[cloud_index].draw()
    
    clouds[0].move_left(5)
    
    cloud_index = (cloud_index + 1 ) % len(clouds)

    clock.tick(2)

pygame.quit()
sys.exit()
