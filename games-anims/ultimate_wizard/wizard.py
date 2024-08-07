import logging
import sys

from bin.factory import create_player_moves, create_enemy_moves
from board import Board
from drawer import Drawer

log_level = logging.INFO
if len(sys.argv) > 1 and (sys.argv[1] == "--debug" or sys.argv[1] == "-d"):
    log_level = logging.DEBUG
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

global drawer
drawer = Drawer()
global board
board = Board()

drawer.draw_board(board)
drawer.draw_info(board)
# drawer.main_loop(board)
drawer.main_loop_auto(board, create_player_moves(), create_enemy_moves())
