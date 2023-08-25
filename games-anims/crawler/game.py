class Field:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.revealed = False

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.fields = [[Field(x, y) for y in range(height)] for x in range(width)]

class Player:
    def __init__(self, x, y, radius=2):
        self.x = x
        self.y = y
        self.radius = radius

class Game:
    def __init__(self, board_width, board_height, player_x, player_y):
        self.board = Board(board_width, board_height)
        self.player = Player(player_x, player_y)
    
    def start(self):
        print("Game started!")
    
    def reveal(self):
        for x in range(self.player.x - self.player.radius, self.player.x + self.player.radius + 1):
            for y in range(self.player.y - self.player.radius, self.player.y + self.player.radius + 1):
                if 0 <= x < self.board.width and 0 <= y < self.board.height:
                    self.board.fields[x][y].revealed = True
    
        for x in range(self.board.width):
            for y in range(self.board.height):
                if not (self.player.x - self.player.radius <= x <= self.player.x + self.player.radius and
                        self.player.y - self.player.radius <= y <= self.player.y + self.player.radius):
                    self.board.fields[x][y].revealed = False


