import pygame
import sys
import math

pygame.init()

# Constants
GRAVITY = 9.81  # Adjust as needed
WIDTH, HEIGHT = 800, 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reverse Parabola")

look_right = True
point = (400, 400)
height = 200
length = 150
y_stop = 600
duration_ms = 5000

start_time = pygame.time.get_ticks()

# Function to calculate the parabolic trajectory
def calculate_trajectory(angle_degrees, initial_speed):
    angle_radians = math.radians(angle_degrees)
    time_of_flight = (2 * initial_speed * math.sin(angle_radians)) / GRAVITY
    max_height = (initial_speed ** 2) * (math.sin(angle_radians) ** 2) / (2 * GRAVITY)
    distance = (initial_speed ** 2) * math.sin(2 * angle_radians) / GRAVITY

    trajectory_points = []
    time_interval = 0.05
    t = 0.0

    while t <= time_of_flight:
        x = initial_speed * math.cos(angle_radians) * t
        y = HEIGHT - (initial_speed * math.sin(angle_radians) * t - 0.5 * GRAVITY * t ** 2)
        trajectory_points.append((x, y))
        t += time_interval

    return trajectory_points

trajectory = calculate_trajectory(45, 10)  # Example angle and initial speed

while pygame.time.get_ticks() - start_time <= duration_ms:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))

    if look_right:
        for x, y in trajectory:
            if x <= point[0] + length:
                pygame.draw.circle(screen, (255, 255, 255), (point[0] + int(x), point[1] - int(y)), 1)
            else:
                break
    else:
        for x, y in reversed(trajectory):
            if x >= 0:
                pygame.draw.circle(screen, (255, 255, 255), (point[0] - int(x), point[1] - int(y)), 1)
            else:
                break

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
