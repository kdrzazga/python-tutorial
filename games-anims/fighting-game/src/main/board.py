import arcade

from src.main.constants import Constants

class Board:
    
    def __init__(self):
        self.top_image = arcade.load_texture("resources/top.png")
        self.middle_image = arcade.load_texture("resources/middle.png")
        self.arena_image = arcade.load_texture("resources/arena.png")
        self.bottom_image = arcade.load_texture("resources/bottom.png")
    
    def draw(self):
        y_offset = 0

        arcade.draw_texture_rectangle(Constants.SCREEN_WIDTH // 2, Constants.SCREEN_HEIGHT - self.top_image.height // 2 , self.top_image.width, self.top_image.height, self.top_image)
        y_offset += self.top_image.height

        arcade.draw_texture_rectangle(Constants.SCREEN_WIDTH // 2,  Constants.SCREEN_HEIGHT - y_offset - self.middle_image.height //2, self.middle_image.width, self.middle_image.height, self.middle_image)
        y_offset += self.middle_image.height

        arcade.draw_texture_rectangle(Constants.SCREEN_WIDTH // 2,  Constants.SCREEN_HEIGHT - y_offset - self.arena_image.height //2, self.arena_image.width, self.arena_image.height, self.arena_image)
        y_offset += self.arena_image.height

        arcade.draw_texture_rectangle(Constants.SCREEN_WIDTH // 2,  Constants.SCREEN_HEIGHT - y_offset - self.bottom_image.width // 2, self.bottom_image.width, self.bottom_image.height, self.bottom_image)
