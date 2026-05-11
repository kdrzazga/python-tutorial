import arcade

from arcade.color import BLACK
from lib.common import Globals
from stage1 import Stage1
from stage2 import Stage2
from stage3 import Stage3
from stage4 import Stage4
from stage5 import Stage5
from stage6 import Stage6


class MainStage(arcade.Window):

    def __init__(self):
        super().__init__(Globals.WIDTH, Globals.HEIGHT, "DEMO")
        self.stage6 = None
        self.stage4 = None
        self.stage3 = None
        self.stage2 = None
        self.set_fullscreen(Globals.fullscreen)
        self.timer = 0
        self.stage1 = Stage1()

    def on_draw(self):
        self.clear(BLACK)

        if self.timer < 200:
            self.stage1.on_draw(self.timer)

        if self.timer//1 == 200.0:
            if not Stage2.ACTIVE:
                self.stage2 = Stage2(self.timer)
        elif 200 < self.timer < Stage3.START_TIMER:
            self.stage2.on_draw(self.timer)

        elif self.timer//1 == Stage3.START_TIMER:
            self.stage3 = Stage3()
        elif Stage3.START_TIMER < self.timer < Stage4.START_TIMER:
            self.stage3.on_draw(self.timer)

        elif self.timer//1 == Stage4.START_TIMER:
            self.stage4 = Stage4()
        elif Stage4.START_TIMER < self.timer < Stage5.START_TIMER:
            self.stage4.on_draw(self.timer)

        elif self.timer//1 == Stage5.START_TIMER:
            self.stage5 = Stage5()
        elif Stage5.START_TIMER < self.timer < Stage6.START_TIMER:
            self.stage5.on_draw(self.timer)

        elif self.timer//1 == Stage6.START_TIMER:
            self.stage6 = Stage6()
        elif Stage6.START_TIMER < self.timer:
            self.stage6.on_draw(self.timer)

        # print(self.timer, end=' ')
        self.timer += Globals.TIMER_INC


if __name__ == "__main__":
    window = MainStage()
    arcade.run()
