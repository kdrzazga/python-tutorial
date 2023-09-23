from collections import deque
from itertools import cycle


class Sprite:

    def __init__(self, x, y, name):
        self.path = ""
        self.x = x
        self.y = y
        self.width = 2
        self.height = 2
        self.visible = True
        self.active = True
        self.moveable = True
        self.name = name
        self.kick_phase = ''
        self.walk_phase = ''
        self.walk_phases = deque(['w1', 'w2', 'w3'], maxlen=3)
        self._cyclic_iterator = cycle(self.walk_phases)
        self.counter = 0
        self.anim_counter_threshold = 1
        self.step_delay_counter = 0
        self.looking_right = True
        self.color = (255, 0, 0)

    def stand(self):
        self.kick_phase = ''
        self.walk_phase = ''

    def kick(self):
        if self.moveable and self.visible:
            self.kick_phase = '_kick'
            self.walk_phase = '_kick'

    def punch(self):
        if self.moveable and self.visible:
            self.kick_phase = '_punch'
            self.walk_phase = '_punch'

    def step(self):
        if self.looking_right:
            self.step_right()
        else:
            self.step_left()

    def step_right(self):
        self.looking_right = True

        if self.moveable:
            self.x += 4
            self.step_common()

    def step_left(self):
        self.looking_right = False

        if self.moveable:
            self.x -= 4
            self.step_common()

    def step_common(self):
        self.kick_phase = ''
        self.step_delay_counter += 1
        if self.step_delay_counter % 3 == 0:
            self.walk_phase = next(self._cyclic_iterator)

        if self.step_delay_counter > 300:
            self.step_delay_counter = 0

    def reset(self):
        pass

    def move(self):
        pass

    def step_down(self):
        self.y += 4

    def turn_left(self):
        pass

    def turn_right(self):
        pass

    def activate(self):
        self.active = True

    def disable_move(self):
        self.moveable = False

    def get_sprite_path(self):
        return ""
