import pygame

pygame.init()

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

def get_color(x, y):
    screenshot = pygame.Surface(screen.get_size())
    screenshot.blit(screen, (0, 0))
    return screenshot.get_at((x, y))

running = True
clock = pygame.time.Clock()
scroll_speed = 5
soldier_anim_counter = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #GET KEY
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN] or keys[pygame.K_SPACE] or keys[pygame.K_RSHIFT] or keys[pygame.K_RALT] or keys[pygame.K_RCTRL]:
        print("JUMP to other side")

    #DRAW
    screen.fill((0, 0, 0))  # Black background

    screen.blit(double_bitmap, (background_x, 0))

    background_x -= scroll_speed
    if background_x <= -background_bitmap.get_width():
        background_x = 0

    # Example of getting the color at (0, 0)
    pixel_color = get_color(0, 0)
    print("Pixel Color:", pixel_color)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
