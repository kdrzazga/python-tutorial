import arcade

from src.main.project_globals import Globals, Constants


def check_distance(karateka_x: int, honda_x: int, karateka_width, honda_width):
    d = honda_x - karateka_x   
    fighter_width = honda_width if d < 0 else karateka_width    
    d -= fighter_width // 2
    print(f"Distance {d}")
    return d <= Constants.REQUIRED_HIT_DISTANCE
    
    
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