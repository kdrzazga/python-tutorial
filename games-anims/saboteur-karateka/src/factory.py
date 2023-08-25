from src.saboteur import Saboteur
from src.karateka import Karateka
from src.donkeykong import DonkeyKong

def create_saboteur():
    return Saboteur(200, 700)
    

def create_karateka():
    return Karateka(300, 700)


def create_kong():
    return DonkeyKong()
