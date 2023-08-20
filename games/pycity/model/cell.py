class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ground = 'soil'
        self.power_line = False
        self.road = False
        self.quarter = None
        