player_moves1 = ['l', 'u', 'u', 'u', 'u', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l']
enemy_moves1 = ['r', 'r', 'r', 'r', 'r', 'r', 'r', 'u', 'u', 'u', 'u', 'u', 'l']


def create_player_moves():
    return player_moves1


def create_enemy_moves():
    return enemy_moves1


def create_platforms(size_y):
    platforms = []

    for x in range(size_y // 2 - 3):
        platforms.append((x, 3))

    for x in range(size_y // 2 - 2, size_y):
        platforms.append((x, 5))

    for x in range(size_y // 5):
        platforms.append((x, x + 6))
        platforms.append((size_y - x - 1, x + 6))

    for x in range(size_y):
        platforms.append((x, 9))
        platforms.append((x, 1))

    return platforms


def create_ladders(size_y):
    ladders = []

    for y in range(size_y):
        ladders.append((3, y))
        ladders.append((15, y))

    for y in range(2 * size_y // 3, size_y):
        ladders.append((8, y))

    return ladders
