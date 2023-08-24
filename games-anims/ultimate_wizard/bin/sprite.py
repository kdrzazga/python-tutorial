class Sprite:

    def __init__(self, x, y, name):
        self.path = ""
        self.x = x
        self.y = y
        self.active = True
        self.name = name

    def get_sprite_path(self):
        return ""

    def punch(self):
        pass
        
    def kick(self):
        pass