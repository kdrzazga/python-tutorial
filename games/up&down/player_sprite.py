class Player:

    def __init__(self):
        self.position = 'up'
        self.width = 55
        self.height = 55

    def up(self):
        self.position = 'up'

    def down(self):
        self.position = 'down'
