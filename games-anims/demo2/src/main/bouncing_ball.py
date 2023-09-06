import logging
import pygame
import sys

class Ball:

    def __init__(self, screen, boundaries, initial_x, initial_y, radius, initial_velocity_y, bounce_wall_x):        
        self.screen = screen
        self.radius = radius

        self.x = boundaries.x + radius + 8
        self.y = initial_y
        
        self.rect = boundaries
        self.rect.x += self.radius
        
        self.velocity_y = initial_velocity_y
        self.GRAVITY = 1
        self.BOUNCE_FACTOR = 0.9
        self.bounce_wall_x = bounce_wall_x
        self.vector = 1


    def move(self):
        self.x += self.vector * 5
        self.y += self.velocity_y
        self.velocity_y += self.GRAVITY

        if self.y + self.radius >= self.rect.height:
            self.y = self.rect.height - self.radius
            self.velocity_y *= -self.BOUNCE_FACTOR
            logging.info("bounce")

        if self.x >= self.bounce_wall_x:
            self.vector *= -1

    def reset(self):
        self.x = self.rect.x + self.radius


    def draw(self):
        pygame.draw.circle(self.screen, BallAnimation.BALL_COLOR, (self.x, int(self.y + self.rect.y)), self.radius)


class BallAnimation:

    BALL_COLOR = (255, 255, 255)

    def __init__(self, screen, boundaries, bg_color, bounce_wall):
        self.bounce_wall_x = bounce_wall
        self.rect = boundaries
        self.screen = screen
        self.BG_COLOR = bg_color
        self.BALL_RADIUS = 9

        self.ball = Ball(self.screen, boundaries, 0, self.rect.height - self.BALL_RADIUS, self.BALL_RADIUS, -10, bounce_wall)


    def clear(self):
        pygame.draw.rect(self.screen, self.BG_COLOR, ((self.rect.x, self.rect.y), (self.rect.width, self.rect.height)))

    
    def bounce(self):
        while 0 < self.ball.x + self.BALL_RADIUS < self.rect.width:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.ball.move()
            self.clear()
            self.ball.draw()
            
            pygame.display.flip()
            pygame.time.delay(64)


    def run(self):
        while True:
            self.bounce()
            self.ball.reset()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    pygame.init()
    screen = pygame.display.set_mode((800, 150))
    pygame.display.set_caption("Bouncing Ball Animation")
    area_rect = pygame.Rect(40, 50, 800 - 40, 100)
    animation = BallAnimation(screen, (area_rect), (0, 123, 255), 1200)
    animation.run()
