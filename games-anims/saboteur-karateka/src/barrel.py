from src.sprite import Sprite


class Barrel(Sprite):
    initial_position = (813, 357)

    def __init__(self):
        x = Barrel.initial_position[0]
        y = Barrel.initial_position[1]
        super().__init__(x, y, "barrel")
        self.active = False
        self.walk_phase = 'w1'
        self.oritentation = 'vertical'
        self.path = "src/resources/barrelw1.png"

    def get_sprite_path(self):
        return "src/resources/barrel" + self.walk_phase + ".png"

    def move(self):
        if self.active:
            if self.counter == 0:
                if self.oritentation == 'vertical':
                    self.step_down()
                else:
                    self.move_left()

            self.counter += 1
            if self.counter >= self.anim_counter_threshold:
                self.counter = 0
