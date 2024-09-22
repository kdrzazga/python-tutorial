import os
import sys

import arcade

SHAPES = [
    [[1, 1],
     [1, 1]],  # Square
    [[0, 1, 0],
     [1, 1, 1]],  # T-shape
    [[1, 1, 0],
     [0, 1, 1]],  # Z-shape
    [[0, 1, 1],
     [1, 1, 0]],  # S-shape
    [[1, 0, 0],
     [1, 1, 1]],  # L-shape
    [[0, 0, 1],
     [1, 1, 1]],  # J-shape
    [[1],
     [1],
     [1],
     [1]]  # Line
]


def restart_program():
    print("Restarting TETRIS ...")
    os.execv(sys.executable, ['python'] + sys.argv)


class Constants:
    SCREEN_WIDTH = 300
    SCREEN_HEIGHT = 600
    BLOCK_SIZE = 30
    BOARD_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
    BOARD_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

    BLACK = arcade.color.BLACK
    WHITE = arcade.color.WHITE
    COLORS = [arcade.color.RED, arcade.color.GREEN, arcade.color.BLUE, arcade.color.YELLOW,
              arcade.color.CYAN, arcade.color.MAGENTA, arcade.color.ORANGE]
