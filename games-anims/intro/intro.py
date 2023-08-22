import pygame
import math
import sys

print("\nUse cursor keys to move the light point")

WIDTH, HEIGHT = 800, 600
CENTER_X, CENTER_Y = WIDTH // 4, HEIGHT // 3
RADIUS = 1
NUM_CIRCLES = 450
BG_COLOR = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_YELLOW = (255, 255, 150)

bitmap = pygame.image.load('resources/pb2.png')

def draw_circle(screen, color, center, radius, transparency):
    thickness = 2 #radius // 6    
    #pygame.draw.circle(screen, LIGHT_YELLOW, (100 + CENTER_X, 50 + CENTER_Y), 3)
    
    for angle in range(0, 360, 2):
        x = radius * math.sin(math.radians(angle)) + center[0]
        y = radius * math.cos(math.radians(angle)) + center[1]

        x_int, y_int = int(round(x)), int(round(y))
        
        bitmap_color = None
        
        if 0 <= x_int < bitmap.get_width() and 0 <= y_int < bitmap.get_height():
            bitmap_color = bitmap.get_at((x_int, y_int))
        
        r = int(color[0])
        g = int(color[1])
        b = int(color[2])
        
        new_color = (r, g, b, transparency)
        
        if bitmap_color != (0, 0, 0):
            pygame.draw.rect(screen, new_color, (100 + x_int, 50 + y_int, thickness, thickness))

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Light Point")

light_point = pygame.Surface((1, 1))
light_point.fill(WHITE)

running = True
clock = pygame.time.Clock()
alpha = 0
while running:
    screen.blit(bitmap, (100, 50))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    alpha = (alpha + 3) % 360
    horiz_radius = 7
    vert_radius = 3
    dx = horiz_radius * math.sin(math.radians(alpha))
    dy = vert_radius * math.cos(math.radians(alpha))

    CENTER_X += dx
    CENTER_Y += dy

    screen.fill(BG_COLOR)

    for i in range(NUM_CIRCLES, 0, -1):
        r = max(0, LIGHT_YELLOW[0] - i * 0.6)
        g = max(0, LIGHT_YELLOW[1] - i * 0.9)
        b = max(0, LIGHT_YELLOW[2] - i * 1.5)
        color = (r, g, b)
        radius = RADIUS + i
        transparency = 250
        draw_circle(screen, color, (CENTER_X, CENTER_Y), radius, transparency)

    screen.blit(light_point, (CENTER_X, CENTER_Y))

    pygame.display.flip()

    clock.tick(199)

pygame.quit()
sys.exit()
