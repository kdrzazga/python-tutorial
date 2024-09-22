import math
from enum import Enum

import arcade
from src.main.project_globals import Globals, Constants


class GameState(Enum):
    INTRO = 1
    FIGHT = 2
    KO_HONDA = 3
    KO_KARATEKA = 4
    END = 5


def check_distance(karateka_x: int, honda_x: int, karateka_width, honda_width):
    d = math.fabs(honda_x - karateka_x)
    fighter_width = honda_width if d < 0 else karateka_width
    d -= fighter_width // 2
    #print(f"Distance {d}")
    return d <= Constants.REQUIRED_HIT_DISTANCE


def load_reward_pic():
    image = arcade.load_texture(Globals.root_dir + "\\..\\..\\" + "barbara.PNG")
    return image


class MovesRegistry:
    def __init__(self):
        self.img_dict = {}
        self.index = 0

    def next(self):
        self.index = (self.index + 1) % len(self.img_dict)
        return self.img_dict[self.index]


class HondaMovesRegistry(MovesRegistry):
    def __init__(self):
        super().__init__()
        files = ["\\resources\\honda_stand.png",
                 "\\resources\\honda_step3.png",
                 "\\resources\\honda_step1.png"]

        self.img_dict = {}

        for i, path in enumerate(files):
            image = arcade.load_texture(Globals.root_dir + "\\..\\.." + path)
            self.img_dict[i] = image


class KaratekaMovesRegistry(MovesRegistry):
    def __init__(self):
        super().__init__()
        files = ["\\resources\\k.png",
                 "\\resources\\kw1.png",
                 "\\resources\\kw2.png"]

        self.img_dict = {}

        for i, path in enumerate(files):
            image = arcade.load_texture(Globals.root_dir + "\\..\\.." + path)
            self.img_dict[i] = image
