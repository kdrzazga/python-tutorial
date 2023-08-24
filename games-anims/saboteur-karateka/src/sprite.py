from collections import deque
from itertools import cycle

class Sprite:
    
    def __init__(self, x, y, name):
        self.path = ""
        self.x = x
        self.y = y
        self.active = True
        self.name = name
        self.walk_phase = ''
        self.walk_phases = deque(['w1', 'w2', 'w3'], maxlen=3)
        self._cyclic_iterator = cycle(self.walk_phases)


    def stand(self):
        self.walk_phase = ''


    def step_right(self):
        self.x += 4
        self.walk_phase = next(self._cyclic_iterator)


    def get_sprite_path(self):
        return ""
