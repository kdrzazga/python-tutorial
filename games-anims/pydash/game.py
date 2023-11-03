import logging

from factory import create_standard_board

class Game:
    
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] - %(message)s')

        self.board = create_standard_board()
        