import pygame
import sys

pygame.init()

width, height = 2724, 200
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Transparent Pixel Check")

image_path = "image.png"
image = pygame.image.load(image_path).convert_alpha()
image_rect = image.get_rect()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_x, mouse_y = pygame.mouse.get_pos()

    if image_rect.collidepoint(mouse_x, mouse_y):
        pixel_color = image.get_at((mouse_x - image_rect.x, mouse_y - image_rect.y))
        if pixel_color.a == 0:
            print("Pixel [", mouse_x, mouse_y,"] is transparent")
        else:
            print("Pixel [", mouse_x, mouse_y,"] is NOT transparent")

    screen.fill((0, 0, 0))
    screen.blit(image, image_rect)
    pygame.display.flip()

pygame.quit()
sys.exit()
