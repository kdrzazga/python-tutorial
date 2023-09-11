from src.main.c64 import C64
from src.main.amiga import Amiga
from src.main.karateka import Karateka


def create_computer(computer_type, screen, karateka_color):
    if computer_type == "C64":
        computer = C64(screen)
        computer.karateka = Karateka(99, 480, karateka_color)
    else:
        computer = Amiga(screen)
        computer.karateka = Karateka(-29, 560, karateka_color)

    return computer
