from src.saboteur import Saboteur
from src.karateka import Karateka
from src.donkeykong import DonkeyKong
from src.barrel import Barrel

def create_saboteur():
    return Saboteur(200, 650)
    

def create_karateka():
    return Karateka(300, 650)


def create_kong():
    return DonkeyKong()


def create_barrel():
    return Barrel()
