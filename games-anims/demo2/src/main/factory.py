from src.main.amiga import Amiga
from src.main.c64 import C64
from src.main.karateka import Karateka
from src.main.utils import Constants


def create_computer(computer_type, screen, karateka_color):
    if computer_type == "C64":
        computer = C64(screen)
        computer.karateka = Karateka(99, Constants.KARATEKA_Y, karateka_color, True)
    else:
        computer = Amiga(screen)
        computer.karateka = Karateka(-29, 560, karateka_color, True)

    return computer
