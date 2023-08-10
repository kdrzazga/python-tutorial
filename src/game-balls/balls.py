import pygame
import random
import math
import time

pygame.init()

offset_y = -5  # Define the offset
BALL_COUNT = 5

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Ball properties
ball_diameter = 21  # Adjusted size
ball_radius = ball_diameter // 2
ball_colors = [(173, 216, 230), (255, 255, 0), (155, 255, 155), (211, 22, 22)]

# Initialize clock for controlling frame rate
clock = pygame.time.Clock()

balls = []

BACKGROUND_COLOR = (74, 74, 73)
GRAVITY = 9.8
HEIGHT = screen_height - ball_diameter  # Adjust for ball's size

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

def calculate_trajectory(angle_degrees, initial_speed):
    angle_radians = math.radians(angle_degrees)
    time_of_flight = (2 * initial_speed * math.sin(angle_radians)) / GRAVITY

    trajectory_points = []
    time_interval = 0.05
    t = 0.0

    while t <= time_of_flight:
        x = initial_speed * math.cos(angle_radians) * t
        y = HEIGHT - (initial_speed * math.sin(angle_radians) * t - 0.5 * GRAVITY * t ** 2)
        trajectory_points.append((x, y))
        t += time_interval

    return trajectory_points

def create_ball():
    x = 0 if random.random() < 0.5 else screen_width
    y = HEIGHT - offset_y  # Adjust y position based on offset
    angle = random.uniform(30, 45)  # Angle in degrees
    initial_speed = random.uniform(80, 130) - angle
    trajectory = calculate_trajectory(angle, initial_speed)
    color = random.choice(ball_colors)
    ball = Ball(x, y, trajectory, color)
    balls.append(ball)

def draw_balls():
    for ball in balls:
        pygame.draw.circle(screen, ball.color, (int(ball.x), int(ball.y + offset_y)), ball_radius)
        
def clear_balls():
    for ball in balls:
        pygame.draw.circle(screen, BACKGROUND_COLOR, (int(ball.x), int(ball.y + offset_y)), ball_radius)

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(BACKGROUND_COLOR)  # Clear the screen
        
        if len(balls) < BALL_COUNT:  # Create fewer balls
            create_ball()
        
        draw_balls()
        
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
        clock.tick(140)  # Limit the frame rate to 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
