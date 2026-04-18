import arcade

from arcade.color import WHITE, BLACK
from common import Globals
from stage1 import Stage1
from stage2 import Stage2


class MainStage(arcade.Window):

    def __init__(self):
        super().__init__(Globals.WIDTH, Globals.HEIGHT, "DEMO")
        self.stage2 = None
        self.set_fullscreen(Globals.fullscreen)
        self.timer = 0
        self.stage1 = Stage1()

    def on_draw(self):
        self.clear(BLACK)

        if self.timer < 233:
            self.stage1.on_draw(self.timer)

        if self.timer//1 == 200.0:
            if not Stage2.ACTIVE:
                self.stage2 = Stage2(self.timer)
        elif 200 < self.timer < 446:
            self.stage2.on_draw(self.timer)

        # print(self.timer, end=' ')
        self.timer += 0.167


if __name__ == "__main__":
    window = MainStage()
    arcade.run()
