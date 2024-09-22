import random

import arcade

from lib import SHAPES, Constants, restart_program


class Tetris(arcade.Window):
    def __init__(self):
        super().__init__(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, "Tetris")
        self.set_update_rate(1 / 2)  # Set a timer to control updates (like falling down)

        # Game state
        self.board = [[0 for _ in range(Constants.BOARD_WIDTH)] for _ in range(Constants.BOARD_HEIGHT)]
        self.current_shape = self.new_shape()
        self.current_x = Constants.BOARD_WIDTH // 2 - len(self.current_shape[0]) // 2
        self.current_y = 0

    def new_shape(self):
        idx = random.randint(0, len(SHAPES) - 1)
        return SHAPES[idx], Constants.COLORS[idx]

    def collide(self, offset_x, offset_y, shape=None):
        if shape is None:
            shape, _ = self.current_shape

        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    if (y + self.current_y + offset_y >= Constants.BOARD_HEIGHT or
                            x + self.current_x + offset_x < 0 or
                            x + self.current_x + offset_x >= Constants.BOARD_WIDTH or
                            self.board[y + self.current_y + offset_y][x + self.current_x + offset_x]):
                        return True
        return False

    def freeze(self):
        shape, color = self.current_shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.board[y + self.current_y][x + self.current_x] = color
        self.clear_lines()
        self.current_shape = self.new_shape()
        self.current_x = Constants.BOARD_WIDTH // 2 - len(self.current_shape[0]) // 2
        self.current_y = 0
        if self.collide(0, 0):
            print("Game over")
            arcade.exit()

    def clear_lines(self):
        lines_to_clear = []
        for y in range(Constants.BOARD_HEIGHT):
            if all(self.board[y]):
                lines_to_clear.append(y)
        for y in lines_to_clear:
            del self.board[y]
            self.board.insert(0, [0 for _ in range(Constants.BOARD_WIDTH)])

    def rotate_shape(self):
        shape, color = self.current_shape
        rotated_shape = [list(row) for row in zip(*shape[::-1])]
        if not self.collide(0, 0, rotated_shape):
            self.current_shape = (rotated_shape, color)

    def drop(self):
        if not self.collide(0, 1):
            self.current_y += 1
        else:
            self.freeze()

    def move(self, direction):
        if not self.collide(direction, 0):
            self.current_x += direction

    def on_draw(self):
        arcade.start_render()

        self.draw_static_board()
        self.draw_current_shape()

    def draw_current_shape(self):
        shape, color = self.current_shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    arcade.draw_rectangle_filled(
                        (x + self.current_x) * Constants.BLOCK_SIZE + Constants.BLOCK_SIZE // 2,
                        Constants.SCREEN_HEIGHT - (
                                (y + self.current_y) * Constants.BLOCK_SIZE + Constants.BLOCK_SIZE // 2),
                        Constants.BLOCK_SIZE - 1,
                        Constants.BLOCK_SIZE - 1,
                        color
                    )

    def draw_static_board(self):
        for y in range(Constants.BOARD_HEIGHT):
            for x in range(Constants.BOARD_WIDTH):
                if self.board[y][x]:
                    arcade.draw_rectangle_filled(
                        x * Constants.BLOCK_SIZE + Constants.BLOCK_SIZE // 2,
                        Constants.SCREEN_HEIGHT - (y * Constants.BLOCK_SIZE + Constants.BLOCK_SIZE // 2),
                        Constants.BLOCK_SIZE - 1,
                        Constants.BLOCK_SIZE - 1,
                        self.board[y][x]
                    )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.move(-1)
        elif key == arcade.key.RIGHT:
            self.move(1)
        elif key == arcade.key.DOWN:
            self.drop()
        elif key == arcade.key.UP:
            self.rotate_shape()

    def update(self, delta_time):
        self.drop()


if __name__ == "__main__":
    game = Tetris()
    arcade.run()
