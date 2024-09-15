import arcade
from src.main.board import Board
from src.main.fighter import Honda
from src.main.constants import Constants

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, "Barbara & Ian")
        self.board = Board()
        self.fighter = Honda(self.board.arena_offset)

    def on_draw(self):
        arcade.start_render()
        self.board.draw()
        self.fighter.draw()

    def update(self, delta_time):
        self.fighter.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.fighter.start_punch()

def main():
    game = MyGame()
    arcade.run()

if __name__ == "__main__":
    main()
    