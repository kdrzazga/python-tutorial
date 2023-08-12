import math
import random

import pygame


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
    offset_y = -5  # Define the offset
    BALL_COUNT = 5

    # Screen dimensions
    screen_width = 800
    screen_height = 600
    # Ball properties
    ball_diameter = 21  # Adjusted size
    ball_radius = ball_diameter // 2
    ball_colors = [(173, 216, 230), (255, 255, 0), (155, 255, 155), (211, 22, 22)]
    balls = []

    BACKGROUND_COLOR = (74, 74, 73)
    GRAVITY = 9.8

    HEIGHT = screen_height - ball_diameter

    @staticmethod
    def calculate_trajectory(angle_degrees, initial_speed, deflect_x=None): # TODO deflect_x does not work
        angle_radians = math.radians(angle_degrees)
        time_of_flight = (2 * initial_speed * math.sin(angle_radians)) / BallsHelper.GRAVITY

        if deflect_x is None:
            start_time = 0.0
            end_time = time_of_flight
        else:
            deflect_time = deflect_x / (initial_speed * math.cos(angle_radians))
            start_time = 0.0
            end_time = time_of_flight + deflect_time

        trajectory_points = []
        time_interval = 0.05

        for t in BallsHelper._frange(start_time, end_time, time_interval):
            if t <= time_of_flight:
                x = initial_speed * math.cos(angle_radians) * t
                y = BallsHelper.HEIGHT - (initial_speed * math.sin(angle_radians) * t - 0.5 * BallsHelper.GRAVITY * t ** 2)
            else:
                deflected_t = t - time_of_flight
                x = deflect_x + initial_speed * math.cos(angle_radians) * deflected_t
                y = BallsHelper.HEIGHT - (initial_speed * math.sin(angle_radians) * time_of_flight -
                                          0.5 * BallsHelper.GRAVITY * time_of_flight ** 2 +
                                          initial_speed * math.sin(angle_radians) * deflected_t -
                                          0.5 * BallsHelper.GRAVITY * deflected_t ** 2)

            trajectory_points.append((x, y))

        return trajectory_points

    @staticmethod
    def _frange(start, end, step):
        while start <= end:
            yield start
            start += step
    
    @staticmethod
    def create_ball():
        x = 0 if random.random() < 0.5 else BallsHelper.screen_width
        y = BallsHelper.HEIGHT - BallsHelper.offset_y  # Adjust y position based on offset
        angle = random.uniform(35, 42)
        initial_speed = random.uniform(80, 130) - angle  # subtracting angle allows to avoid high altitudes and lobs
        trajectory = BallsHelper.calculate_trajectory(angle, initial_speed)
        color = random.choice(BallsHelper.ball_colors)
        ball = Ball(x, y, trajectory, color)
        BallsHelper.balls.append(ball)

    @staticmethod
    def draw_balls(screen):
        for ball in BallsHelper.balls:
            pygame.draw.circle(screen, ball.color, (int(ball.x), int(ball.y + BallsHelper.offset_y)), BallsHelper.ball_radius)

    @staticmethod
    def clear_balls(screen):
        for ball in BallsHelper.balls:
            pygame.draw.circle(screen, BallsHelper.BACKGROUND_COLOR, (int(ball.x), int(ball.y + BallsHelper.offset_y)), BallsHelper.ball_radius)
