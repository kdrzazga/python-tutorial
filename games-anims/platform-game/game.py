from enum import Enum, auto

import arcade

from board import Board
from factories import BoardFactory
from globals import Constants


class PlayerState(Enum):
    STANDING = auto()
    RUNNING = auto()
    FALLING = auto()


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("fighter.png")
        self.append_texture(self.texture)
        self.width = Constants.TILE_WIDTH
        self.height = Constants.TILE_HEIGHT
        self.center_x = Constants.TILE_WIDTH // 2
        self.center_y = Constants.TILE_HEIGHT - 8
        self.speed = 2 * Constants.GRAVITY
        self.board_position = [0, 0]
        self.state = PlayerState.STANDING

    def update(self, board: Board):
        self.conditional_falling(board)
        match self.state:
            case PlayerState.STANDING:
                self.update_running(board)
            case PlayerState.RUNNING:
                self.update_running(board)
            case PlayerState.FALLING:
                print("Falling")

        self.snap_to_board_tile()

    def conditional_falling(self, board: Board) -> None:
        below_position = [self.board_position[0], self.board_position[1] - 1]
        if not board.is_platform_at(below_position):
            self.center_y -= Constants.GRAVITY
        else:
            self.state = PlayerState.STANDING
            self.center_y = (self.board_position[
                                 1] * Constants.TILE_HEIGHT) + Constants.TILE_HEIGHT - 8

    def update_running(self, board: Board) -> None:
        if arcade.key.UP in self.keys and self.center_y < Constants.SCREEN_HEIGHT - self.height:
            if board.is_ladder_above_or_at(self.board_position):
                self.center_y += self.speed  # Move up if there's a ladder above
            else:
                print("jump")

        elif arcade.key.DOWN in self.keys and self.center_y < Constants.SCREEN_HEIGHT - self.height:
            if board.is_ladder_below_or_at(self.board_position):
                self.center_y -= self.speed  # Move down if there's a ladder above

        if arcade.key.LEFT in self.keys and self.center_x > self.width // 2:
            self.center_x -= self.speed
        elif arcade.key.RIGHT in self.keys and self.center_x < Constants.SCREEN_WIDTH - self.width // 2:
            self.center_x += self.speed

    def snap_to_board_tile(self) -> None:
        self.board_position[0] = round(self.center_x / Constants.TILE_WIDTH)
        self.board_position[1] = round(self.center_y / Constants.TILE_HEIGHT)

    def draw(self, *, filter=None, pixelated=None, blend_function=None) -> None:
        super().draw()
        arcade.draw_texture_rectangle(self.center_x, self.center_y,
                                      self.texture.width, self.texture.height,
                                      self.texture)


class Game(arcade.Window):
    def __init__(self):
        super().__init__(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, "Platform Game")
        self.player = Player()
        self.board = BoardFactory.create_room1()
        self.player.keys = set()

    def on_draw(self):
        arcade.start_render()
        self.board.draw()
        self.player.draw()

    def update(self, delta_time):
        self.player.update(self.board)

    def on_key_press(self, key, modifiers):
        self.player.keys.add(key)

    def on_key_release(self, key, modifiers):
        if key in self.player.keys:
            self.player.keys.remove(key)
        print(self.player.board_position)


if __name__ == "__main__":
    window = Game()
    arcade.run()
