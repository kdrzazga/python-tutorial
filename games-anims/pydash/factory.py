import logging

from constants import Constants
from cell import Cell, CellType
from board import Board


def create_standard_board():
    board = Board()
    board.cells = create_bottom_cells()   
    top_cells = create_top_cells()
    board.cells.extend(top_cells)
    
    logging.info("Created board with %d cells", len(board.cells))
    return board


def create_bottom_cells():
    cells = []
    for x in range(Constants.WIDTH):
        cells.append(Cell(CellType.WALL, x, Constants.HEIGHT -1))
    
    return cells


def create_top_cells():
    cells = []
    for x in range(Constants.WIDTH):
        cells.append(Cell(CellType.WALL, x, 0))
    
    return cells