import arcade

from src.main.project_globals import Constants, Globals

class Intro:
    
    def __init__(self):
        self.intro_pic_path = "\\resources\\intro.png"
        self.image = arcade.load_texture(Globals.root_dir + "\\..\\.." + self.intro_pic_path)

    def show(self):
        
        arcade.draw_texture_rectangle(Constants.SCREEN_WIDTH // 2,
                                      Constants.SCREEN_HEIGHT - self.image.height // 2 + 120,
                                      self.image.width, self.image.height, self.image)
