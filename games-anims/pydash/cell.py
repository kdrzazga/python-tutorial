from enum import Enum

class CellType(Enum):
    SPACE = 1
    DIRT = 2
    WALL = 3

class Cell:
    def __init__(self, cell_type, x, y):
        self.cell_type = cell_type
        self.x = x
        self.y = y
        