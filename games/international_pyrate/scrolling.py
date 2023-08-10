import pygame
import os

from PIL import Image, ImageDraw, ImageFont

global background_x

BLACK = (0, 0, 0)
ORANGE = (255, 128, 64)
WHITE = (250, 250, 250)
YELLOW = (238, 238, 119)

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

def scroll(screen):
    #screen.fill((0, 0, 0))  # Black background
    font_path = os.path.join("resources", "karate.ttf")
    caption_font = ImageFont.truetype(font_path, 15)
    caption_text_height = 13
    caption_text_background = BLACK
    caption_text_color1 = YELLOW
    caption_text_color2 = ORANGE
    
    caption_text = "INTERNATIONAL PYRATE is python tribute to c64 IK plus. controls: QAED or arrow keys."
    
    caption_image = Image.new("RGB", (750, caption_text_height), caption_text_background)
    
    draw = ImageDraw.Draw(caption_image)
    draw.text((0, 0), caption_text, font=caption_font, fill=caption_text_color2)

    caption_surface = pygame.image.fromstring(caption_image.tobytes(), caption_image.size, caption_image.mode)
    screen.blit(caption_surface, (0, 0))

    #screen.blit(caption_surface, (background_x, 0))

    #background_x -= scroll_speed
    #if background_x <= -caption_surface.get_width():
    #    background_x = 0
