from src.barrel import Barrel
from src.donkeykong import DonkeyKong
from src.karateka import Karateka
from src.saboteur import Saboteur


def create_saboteur():
    return Saboteur(200, 650)
    

def create_karateka():
    return Karateka(300, 650)


def create_kong():
    return DonkeyKong()


def create_barrel():
    return Barrel()
