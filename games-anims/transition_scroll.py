import pygame
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
LIGHT_BLUE = (96, 96, 192)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Scroll and Fill")

def scroll_right():
    scroll_distance = 0
    scroll_speed = 1 / 3
    c64half_x = - SCREEN_WIDTH // 2
    screenshot = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    screenshot.blit(screen, (0, 0))
    
    bitmap = pygame.Surface((3 * SCREEN_WIDTH // 2, SCREEN_HEIGHT))    
    bitmap.blit(c64half, (0, 0))
    bitmap.blit(screenshot, (SCREEN_WIDTH // 2 - 1, 0))
    while c64half_x < 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                        
        screen.blit(bitmap, (c64half_x, 0))
        pygame.display.flip()

        c64half_x += scroll_speed
        scroll_distance += scroll_speed

        if scroll_distance >= SCREEN_WIDTH:
            break

def scroll_and_fill():
    screenshot = None
    scroll_distance = 0
    
    running = True

    TOTAL_DISTANCE = 12
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screenshot = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        screenshot.blit(screen, (0, 0))

        if scroll_distance < TOTAL_DISTANCE:
            scroll_distance += 1
            screen.fill(LIGHT_BLUE)
            screen.blit(screenshot, (0, -scroll_distance))
            
        if scroll_distance == TOTAL_DISTANCE:
            scroll_right()
            running = False

        pygame.display.flip()
        clock.tick(9)

if __name__ == "__main__":
    background_image = pygame.image.load("demo2/src/main/resources/amiga.png")
    screen.blit(background_image, (0, 0))
    pygame.display.flip()

    c64half = pygame.image.load("demo2/src/main/resources/c64half.png")

    pygame.time.delay(2000) 
    scroll_and_fill()
    pygame.time.delay(5000)
    
    pygame.quit()
    sys.exit()
