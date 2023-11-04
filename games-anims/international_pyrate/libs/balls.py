import pygame
import random
import math
import time


class Ball:
    count = 0

    def __init__(self, x, y, trajectory, color, rolling=False):
        self.x = x
        self.y = y
        self.trajectory = trajectory
        self.index = 0
        self.color = color
        self.rolling = rolling
        self.id = Ball.count
        Ball.count += 1

class BallsHelper:

    screen_width = 800
    screen_height = 600
    balls = []
    BACKGROUND_COLOR = (74, 74, 73)
    BALL_COUNT = 5
    
    ball_diameter = 21
    ball_radius = ball_diameter // 2
    ball_colors = [(173, 216, 230), (255, 255, 0), (155, 255, 155), (211, 22, 22)]
    
    clock = pygame.time.Clock()  
    
    GRAVITY = 9.8
    HEIGHT = screen_height - ball_diameter
    offset_y = -5
        
    def __init__(self):
        pygame.init()        
        screen = pygame.display.set_mode((screen_width, screen_height))


    def calculate_trajectory(angle_degrees, initial_speed):
        angle_radians = math.radians(angle_degrees)
        time_of_flight = (2 * initial_speed * math.sin(angle_radians)) / BallsHelper.GRAVITY
    
        trajectory_points = []
        time_interval = 0.05
        t = 0.0
    
        while t <= time_of_flight:
            x = initial_speed * math.cos(angle_radians) * t
            y = BallsHelper.HEIGHT - (initial_speed * math.sin(angle_radians) * t - 0.5 * BallsHelper.GRAVITY * t ** 2)
            trajectory_points.append((x, y))
            t += time_interval
    
        return trajectory_points
    
    def create_ball():
        x = 0 if random.random() < 0.5 else BallsHelper.screen_width
        y = BallsHelper.HEIGHT - BallsHelper.offset_y  # Adjust y position based on offset
        angle = random.uniform(30, 45)  # Angle in degrees
        initial_speed = random.uniform(80, 130) - angle
        trajectory = BallsHelper.calculate_trajectory(angle, initial_speed)
        color = random.choice(BallsHelper.ball_colors)
        ball = Ball(x, y, trajectory, color)
        BallsHelper.balls.append(ball)
    
    def draw_balls(screen):
        for ball in BallsHelper.balls:
            pygame.draw.circle(screen, ball.color, (int(ball.x), int(ball.y + BallsHelper.offset_y)), BallsHelper.ball_radius)
    
    def clear_balls(screen):
        for ball in BallsHelper.balls:
            pygame.draw.circle(screen , BallsHelper.BACKGROUND_COLOR, (int(ball.x), int(ball.y + BallsHelper.offset_y)), BallsHelper.ball_radius)
    
    def main(self):
        running = True
        while running:
            for event in pygame.event.get(self):
                if event.type == pygame.QUIT:
                    running = False
    
            screen.fill(BACKGROUND_COLOR)  # Clear the screen
    
            if len(balls) < BALL_COUNT:  # Create fewer balls
                create_ball()
    
            draw_balls(BallsHelper.screen)
    
            for ball in balls:
                roll_speed = -3 if ball.id % 3 == 0 else 3 
                if ball.index < len(ball.trajectory):
                    x, ball.y = ball.trajectory[ball.index]
                    ball.x = screen_width - x  if ball.id % 3 == 0 else x 
                    ball.index += 1
                else:
                    if not ball.rolling:
                        ball.rolling = True
                        ball.trajectory = [(ball.x, ball.y)]
                    else:
                        ball.x += roll_speed 
    
                        if ball.x >= screen_width + ball_diameter or ball.x < 0:
                            balls.remove(ball)
    
            pygame.display.flip()  # Update the screen
    
            time.sleep(0.001)
            clear_balls()
            BallsHelper.clock.tick(140)  # Limit the frame rate to 60 FPS
    
        pygame.quit()

if __name__ == "__main__":
    BallsHelper.main()
    