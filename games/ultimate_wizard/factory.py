player_moves1=['l','u','u','u','u','l','l','l','l','l','l','l','l','l','l']
enemy_moves1=['r','r','r','r','r','r','u','u','u','u','u','l']

def create_player_moves():
    return player_moves1

def create_enemy_moves():
    return enemy_moves1

def create_platforms(sizeX):
    platforms = []
    
    for x in range(sizeX // 2 - 3):
        platforms.append((x, 3))
        
    for x in range(sizeX // 2 - 2, sizeX):
        platforms.append((x, 5))
        
    for x in range(sizeX // 5):
        platforms.append((x, x + 6))
        platforms.append((sizeX - x - 1, x + 6))
    
    for x in range(sizeX):
        platforms.append((x, 9))       
        platforms.append((x, 1))
        
    return platforms
    
def create_ladders(sizeY):
    ladders = []
    
    for y in range(sizeY):
        ladders.append((3, y))
        ladders.append((15, y))

    for y in range(2 * sizeY//3, sizeY):
        ladders.append((8, y))
    
    return ladders
