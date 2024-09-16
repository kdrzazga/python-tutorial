import arcade

from src.main.board import Board
from src.main.fighter import Honda, Karateka
from src.main.project_globals import Constants


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, "Barbara & Ian")
        self.board = Board()
        self.honda_fighter = Honda(self.board.arena_offset)
        self.karateka_fighter = Karateka(self.board.arena_offset)
        self.key_state = {arcade.key.D: False, arcade.key.A: False, arcade.key.L: False,
                          arcade.key.J: False}

    def on_draw(self):
        arcade.start_render()
        self.board.draw()
        self.karateka_fighter.draw()
        self.honda_fighter.draw()

    def update(self, delta_time):
        self.honda_fighter.update()
        self.karateka_fighter.update()

        if self.key_state.get(arcade.key.D, True):
            self.honda_fighter.move_right()
            self.board.apply_boundaries(self.honda_fighter)

        if self.key_state.get(arcade.key.A, True):
            self.honda_fighter.move_left()
            self.board.apply_boundaries(self.honda_fighter)

        if self.key_state.get(arcade.key.L, True):
            self.karateka_fighter.move_right()
            self.board.apply_boundaries(self.karateka_fighter)

        if self.key_state.get(arcade.key.J, True):
            self.karateka_fighter.move_left()
            self.board.apply_boundaries(self.karateka_fighter)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE or key == arcade.key.LCTRL or key == arcade.key.LSHIFT:
            self.honda_fighter.start_punch()
        elif key == arcade.key.F2:
            print("Change karateka color.")
            self.karateka_fighter.change_color()
        if key == arcade.key.D or key == arcade.key.A or key == arcade.key.L or key == arcade.key.J:
            self.key_state[key] = True
        if key == arcade.key.ENTER or key == arcade.key.RCTRL or key == arcade.key.RSHIFT:
            self.karateka_fighter.start_punch()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.D or key == arcade.key.A:
            self.honda_fighter.state = "idle"

        elif key == arcade.key.L or key == arcade.key.J:
            self.karateka_fighter.state = "idle"

        self.key_state[key] = False


def main():
    MyGame()
    arcade.run()


if __name__ == "__main__":
    main()
