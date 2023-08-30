import random
import sys
import pygame

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(5, 20)
        self.color = (200, 200, 200)

    def move(self):
        self.x += random.randint(-1, 1)
        self.y += random.randint(-1, 1)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

class CloudEffectApp:
    def __init__(self, screen):
        self.screen = screen
        self.BLACK = (0, 0, 0)
        self.particles = [Particle(screen.get_width() // 2, screen.get_height() // 2) for _ in range(200)]
        self.clock = pygame.time.Clock()
        self.counter = 1600
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(self.BLACK)

            for particle in self.particles:
                particle.move()
                particle.draw(self.screen)

            pygame.display.flip()

            if self.counter <= 0:
                self.running = False
            self.counter -= 1
            
            self.clock.tick(170)
