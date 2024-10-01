import random


def random_move_mostly_up() -> str:
    moves = ['u', 'u', 'u', 'u', 'd', 'l', 'r']
    return moves[random.randint(0, len(moves) - 1)]


def random_move() -> str:
    moves = ['u', 'd', 'l', 'r']
    return moves[random.randint(0, len(moves) - 1)]
