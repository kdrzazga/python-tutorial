import pygame
import math
import sys
import random

class Animation:
    def __init__(self, screen, outer_text, inner_text):
        
        self.screen = screen
        self.WIDTH, self.HEIGHT = screen.get_width(), screen.get_height()
        
        self.CENTER = (self.WIDTH // 2, self.HEIGHT // 2)
        self.RAYS_COUNT = 100
        self.RAY_LENGTH = 300

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255, 122, 0)

        
        pygame.display.set_caption("Ray Animation")

        self.clock = pygame.time.Clock()
        self.direction_forward = True
        self.draw_rays = True
        self.animation_progress = 0.0
        self.outer_text = outer_text
        self.inner_text = inner_text
        self.dots = []
        
        self.counter = 0
        self.fill_screen = False
        self.fill_counter = 0

    def draw_rays_on_screen(self, surface, center, count, length, direction):
        min_angle = int(44 * self.animation_progress)
        max_angle = 360 + int(44 * self.animation_progress)
        angle_step = 360 // count

        outer_text_index = 0
        inner_text_index = 0

        for angle in range(min_angle, max_angle, angle_step):
            radians = math.radians(angle)
            dx = length * math.cos(radians)
            dy = length * math.sin(radians)
            start_point = (center[0] + dx * (0.8 - self.animation_progress), center[1] + dy * (0.8 - self.animation_progress))
            
            if direction:
                end_point = (center[0] + dx * self.animation_progress, center[1] + dy * self.animation_progress)
            else:
                end_point = (center[0] + dx * (1 - self.animation_progress), center[1] + dy * (1 - self.animation_progress))
            
            text_i = self.inner_text[inner_text_index % len(self.inner_text)]
            inner_text_index += 1
            
            text_o = self.outer_text[outer_text_index % len(self.outer_text)]
            outer_text_index += 1

            font = pygame.font.Font(None, int(12 + 12 * self.animation_progress))
            text_surface = font.render(text_i, True, self.YELLOW)
            text_rect = text_surface.get_rect(center=start_point)
            surface.blit(text_surface, text_rect)
            
            font2 = pygame.font.Font(None, 36)
            text_surface2 = font2.render(text_o, True, self.WHITE)
            text_rect2 = text_surface2.get_rect(center=end_point)
            surface.blit(text_surface2, text_rect2)

        if self.counter > 100:
            for _ in range(5):
                self.dots.append((int(self.WIDTH * random.uniform(0.5, 1.0)), int(self.HEIGHT * random.uniform(0, 1.0))))

        if self.counter > 170:
            for _ in range(self.counter):
                self.dots.append((int(self.WIDTH * random.uniform(0, 1.0)), int(self.HEIGHT * random.uniform(0, 1.0))))
                
    def run(self):
        while self.fill_counter < 420:  # Approximately 7 seconds at 60 FPS
            if not self.fill_screen:
                self.screen.fill(self.BLACK)
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    

            if self.draw_rays:
                self.draw_rays_on_screen(self.screen, self.CENTER, self.RAYS_COUNT, self.RAY_LENGTH, self.direction_forward)

                for dot in self.dots:
                    pygame.draw.circle(self.screen, self.WHITE, dot, 2)

                self.CENTER = (self.WIDTH // 2, self.HEIGHT // 2 + int(0.45 * self.WIDTH * math.sin(self.animation_progress * math.pi)))
                self.animation_progress += 0.04
                if self.animation_progress > 1.85:
                    self.animation_progress = 0.0

                if self.counter > 240:
                    break
            self.counter += 1
    
            pygame.display.flip()
            self.clock.tick(240)
