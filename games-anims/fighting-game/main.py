import arcade

from src.main.board import Board
from src.main.fighter import Honda
from src.main.project_globals import Constants


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, "Barbara & Ian")
        self.board = Board()
        self.fighter = Honda(self.board.arena_offset)
        self.key_state = {arcade.key.D: False, arcade.key.A: False}

    def on_draw(self):
        arcade.start_render()
        self.board.draw()
        self.fighter.draw()

    def update(self, delta_time):
        self.fighter.update()

        if self.key_state.get(arcade.key.D, True):
            self.fighter.move_right()
            print('key RIGHT pressed (D)')

        if self.key_state.get(arcade.key.A, True):
            self.fighter.move_left()
            print('key LEFT pressed (A)')

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.fighter.start_punch()
        elif key == arcade.key.D or key == arcade.key.A:
            self.key_state[key] = True

    def on_key_release(self, key, modifiers):
        self.fighter.state = "idle"
        if key == arcade.key.D or key == arcade.key.A:
            self.key_state[key] = False


def main():
    MyGame()
    arcade.run()


if __name__ == "__main__":
    main()
