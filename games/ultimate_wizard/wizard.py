from board import Board
from drawer import Drawer

drawer = Drawer()
board = Board()

drawer.draw_board(board)
drawer.draw_info(board.player)
drawer.main_loop(board)
