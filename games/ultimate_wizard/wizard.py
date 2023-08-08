from factory import create_player_moves, create_enemy_moves
from board import Board
from drawer import Drawer

drawer = Drawer()
board = Board()

drawer.draw_board(board)
drawer.draw_info(board.player)
#drawer.main_loop(board)
drawer.main_loop_auto(board, create_player_moves(), create_enemy_moves())
