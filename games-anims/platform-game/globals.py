from enum import Enum, auto


class Constants:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    TILE_WIDTH = 52
    TILE_HEIGHT = 46
    BOARD_WIDTH = 15
    BOARD_HEIGHT = 12
    GRAVITY = 2


class BoardTile(Enum):
    EMPTY = auto()
    PLATFORM = auto()
    LADDER = auto()
