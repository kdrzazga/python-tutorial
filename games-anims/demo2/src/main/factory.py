from src.main.c64 import C64
from src.main.amiga import Amiga
from src.main.karateka import Karateka


def create_computer(computer_type, screen):
    if computer_type == "C64":
        computer = C64(screen)
        computer.karateka = Karateka(87, 480)
    else:
        computer = Amiga(screen)
        computer.karateka = Karateka(-29, 560)

    return computer
