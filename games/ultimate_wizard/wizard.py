from board import Board
from drawer import Drawer
from info import Info

drawer = Drawer()
board = Board()
info = Info()

drawer.draw_board(board)
drawer.draw_info(info)
drawer.main_loop(board, info)
