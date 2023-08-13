import pygame
import sys
import random

pygame.init()

screen_width = 800
screen_height = 600

BLACK = (0,0,0)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Cloud Effect")

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(5, 20)
        self.color = (200, 200, 200)

    def move(self):
        self.x += random.randint(-1, 1)
        self.y += random.randint(-1, 1)

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

particles = [Particle(screen_width // 2, screen_height // 2) for _ in range(200)]

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(white)

    for particle in particles:
        particle.move()
        particle.draw()

    pygame.display.flip()

    clock.tick(90)

pygame.quit()
sys.exit()
