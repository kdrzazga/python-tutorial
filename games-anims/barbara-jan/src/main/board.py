import arcade

from src.main.project_globals import Constants


class Board:

    MIN_X = 520
    MAX_X = 1712

    def __init__(self):
        y_offset = 0
        self.top_image = arcade.load_texture("resources/top.png")
        self.top_offset = y_offset

        y_offset += self.top_image.height
        self.throne_image = arcade.load_texture("resources/throne.png")
        self.throne_offset = y_offset

        y_offset += self.throne_image.height
        self.arena_image = arcade.load_texture("resources/arena.png")
        self.arena_offset = y_offset

        y_offset += self.arena_image.height
        self.bottom_image = arcade.load_texture("resources/bottom.png")
        self.bottom_offset = y_offset

    def draw(self):
        arcade.draw_texture_rectangle(Constants.SCREEN_WIDTH // 2,
                                      Constants.SCREEN_HEIGHT - self.top_offset - self.top_image.height // 2,
                                      self.top_image.width, self.top_image.height, self.top_image)

        arcade.draw_texture_rectangle(Constants.SCREEN_WIDTH // 2,
                                      Constants.SCREEN_HEIGHT - self.throne_offset - self.throne_image.height // 2,
                                      self.throne_image.width, self.throne_image.height, self.throne_image)

        arcade.draw_texture_rectangle(Constants.SCREEN_WIDTH // 2,
                                      Constants.SCREEN_HEIGHT - self.arena_offset - self.arena_image.height // 2,
                                      self.arena_image.width, self.arena_image.height, self.arena_image)

        arcade.draw_texture_rectangle(Constants.SCREEN_WIDTH // 2,
                                      Constants.SCREEN_HEIGHT - self.bottom_offset - self.bottom_image.width // 2,
                                      self.bottom_image.width, self.bottom_image.height, self.bottom_image)

    def apply_boundaries(self, fighter):
        if fighter.x >= Board.MAX_X:
            fighter.x = Board.MAX_X - fighter.speed
        elif fighter.x <= Board.MIN_X:
            fighter.x = Board.MIN_X + fighter.speed