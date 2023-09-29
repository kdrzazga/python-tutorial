import logging
import sys

import pygame


class Ball:

    def __init__(self, screen, boundaries, initial_x, initial_y, radius, initial_velocity_y, bounce_wall_x):
        self.screen = screen
        self.radius = radius

        self.x = initial_x + boundaries.x + radius + 8
        self.y = initial_y

        self.rect = boundaries
        self.rect.x += self.radius

        self.velocity_y = initial_velocity_y
        self.GRAVITY = 1
        self.BOUNCE_FACTOR = 0.9
        self.bounce_wall_x = bounce_wall_x
        self.vector = 1

        self.bounce_sound = pygame.mixer.Sound("src/main/resources/bounce.wav")
        self.deflect_sound = pygame.mixer.Sound("src/main/resources/deflect.wav")

    def move(self):
        self.x += self.vector * 5
        self.y += self.velocity_y
        self.velocity_y += self.GRAVITY

        if self.y + self.radius >= self.rect.height:
            self.y = self.rect.height - self.radius
            self.velocity_y *= -self.BOUNCE_FACTOR
            logging.info("bounce")
            self.bounce_sound.play()

        if self.x >= self.bounce_wall_x:
            self.vector *= -1
            logging.info("deflect")
            self.deflect_sound.play()

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

        self.ball = Ball(self.screen, boundaries, 0, self.rect.height - self.BALL_RADIUS, self.BALL_RADIUS, -10,
                         bounce_wall)

    def clear(self):
        x = self.ball.x - 1 * self.ball.radius
        y = self.rect.y + self.ball.y - 1* self.ball.radius
        w = 2 * self.ball.radius 
        h = 2 * self.ball.radius
        pygame.draw.rect(self.screen, self.BG_COLOR, ((x, y), (w, h)))

    def bounce(self, computer, karateka=False):
        while 0 < self.ball.x + self.BALL_RADIUS < self.rect.width:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.clear()
            self.ball.move()
            if karateka:
                computer.check_ball_kill(self.ball.x)
            else:
                computer.honda_deflects_ball(self.ball.x)

            self.clear()
            self.ball.draw()
            if karateka:
                computer.draw_karateka()

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
    animation = BallAnimation(screen, area_rect, (0, 123, 255), 1200)
    animation.run()
