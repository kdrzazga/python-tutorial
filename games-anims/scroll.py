import pygame
import sys

pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Text Scrolling Animation")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Font and initial text
font = pygame.font.Font(None, 72)
text = "Scrolling Text Animation"
text_surface = font.render(text, True, black)
text_rect = text_surface.get_rect()
text_rect.topleft = (0, 100)

clock = pygame.time.Clock()
scroll_speed = 2
size_change_rate = 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Scroll the text to the right
    text_rect.x += scroll_speed
    
    # Decrease font size
    if font.size(text)[0] > 8:
        font = pygame.font.Font(None, font.size(text)[0] - size_change_rate)

    screen.fill(white)
    screen.blit(text_surface, text_rect)

    pygame.display.flip()
    clock.tick(60)
