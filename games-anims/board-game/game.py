import enum

import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_WIDTH = 52
TILE_HEIGHT = 46
BOARD_WIDTH = 15
BOARD_HEIGHT = 12


class BoardTile(enum.Enum):
    EMPTY = 0
    PLATFORM = 1
    LADDER = 2


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("fighter.png")
        self.append_texture(self.texture)
        self.width = TILE_WIDTH
        self.height = TILE_HEIGHT
        self.center_x = TILE_WIDTH // 2
        self.center_y = TILE_HEIGHT // 2
        self.speed = 1
        self.board_position = [0, 0]

    def update(self):
        if arcade.key.UP in self.keys and self.center_y < SCREEN_HEIGHT - self.height:
            self.center_y += self.speed
        if arcade.key.DOWN in self.keys and self.center_y > self.height // 2:
            self.center_y -= self.speed

        # Move horizontally with "left" and "right" keys
        if arcade.key.LEFT in self.keys and self.center_x > self.width // 2:
            self.center_x -= self.speed
        if arcade.key.RIGHT in self.keys and self.center_x < SCREEN_WIDTH - self.width // 2:
            self.center_x += self.speed

        # Snap to the closest tile
        self.board_position[0] = round(self.center_x / TILE_WIDTH)
        self.board_position[1] = round(self.center_y / TILE_HEIGHT)

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        super().draw()
        arcade.draw_texture_rectangle(self.center_x, self.center_y,
                                      self.texture.width, self.texture.height,
                                      self.texture)


class Board:
    def __init__(self):
        self.tiles = [[BoardTile.EMPTY for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        # Create some platforms for testing
        for x in range(5, BOARD_WIDTH - 1):
            self.tiles[10][x] = BoardTile.PLATFORM
        self.tiles[BOARD_HEIGHT - 1][10] = BoardTile.LADDER

        self.platform_image = arcade.load_texture("platform.png")

    def draw(self):
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                tile = self.tiles[row][col]
                # Use WHITE for empty tiles or define your own color with alpha
                color = (235, 15, 15)
                x = col * TILE_WIDTH + TILE_WIDTH // 2 + 1
                y = row * TILE_HEIGHT + TILE_HEIGHT // 2 + 1
                arcade.draw_rectangle_outline(x, y, TILE_WIDTH, TILE_HEIGHT, color)
                if tile == BoardTile.PLATFORM:
                    arcade.draw_texture_rectangle(x, y,
                                                  self.platform_image.width, self.platform_image.height,
                                                  self.platform_image)


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Platform Game")
        self.player = Player()
        self.board = Board()
        self.player.keys = set()

    def on_draw(self):
        arcade.start_render()
        self.board.draw()
        self.player.draw()

    def update(self, delta_time):
        self.player.update()

    def on_key_press(self, key, modifiers):
        self.player.keys.add(key)

    def on_key_release(self, key, modifiers):
        if key in self.player.keys:
            self.player.keys.remove(key)
        print(self.player.board_position)


if __name__ == "__main__":
    window = Game()
    arcade.run()
