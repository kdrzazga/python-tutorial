import enum


class Constants:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    TILE_WIDTH = 52
    TILE_HEIGHT = 46
    BOARD_WIDTH = 15
    BOARD_HEIGHT = 12


class BoardTile(enum.Enum):
    EMPTY = 0
    PLATFORM = 1
    LADDER = 2
