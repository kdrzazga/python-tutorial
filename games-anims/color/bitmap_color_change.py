import pygame
import sys

def draw_sprite():
    path = "k.png"
    image = pygame.image.load(path).convert_alpha()

    old_color = (255, 255, 255)
    new_color = (255,0 , 0)
    new_image = image.copy()
    
    # Get the width and height of the image
    width, height = image.get_size()
    
    # Iterate through each pixel in the image
    for x in range(width):
        for y in range(height):
            pixel_color = image.get_at((x, y))  # Get the color of the current pixel
            if pixel_color == old_color:
                new_image.set_at((x, y), new_color)  # Set the new color for matching pixels

    # Display the original and modified images (optional)
    screen = pygame.display.set_mode((width * 2, height))
    screen.blit(image, (0, 0))
    screen.blit(new_image, (width, 0))
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
    
if __name__ == "__main__":
    pygame.init()
    canvas_width = 800
    cycles = 0
    screen = pygame.display.set_mode((canvas_width, 600))
    pygame.display.set_caption("EoD")
    draw_sprite()