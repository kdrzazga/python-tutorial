import arcade

from globals import Constants, BoardTile


class Board:
    def __init__(self):
        self.tiles = [[BoardTile.EMPTY for _ in range(Constants.BOARD_WIDTH)] for _ in range(Constants.BOARD_HEIGHT)]
        for x in range(0, Constants.BOARD_WIDTH):
            self.tiles[0][x] = BoardTile.PLATFORM

        self.platform_image = arcade.load_texture("platform.png")
        self.ladder_image = arcade.load_texture("ladder.png")

    def is_ladder_above_or_at(self, board_position):
        x, y = board_position[0], board_position[1]  # Check the current tile

        # Check current tile
        if 0 <= x < Constants.BOARD_WIDTH and 0 <= y < Constants.BOARD_HEIGHT:
            if self.tiles[y][x] == BoardTile.LADDER:
                return True

        # Now check the tile directly above
        y = board_position[1] + 1
        if 0 <= x < Constants.BOARD_WIDTH and 0 <= y < Constants.BOARD_HEIGHT:
            return self.tiles[y][x] == BoardTile.LADDER

    def is_ladder_below_or_at(self, board_position):
        x, y = board_position[0], board_position[1]  # Check the current tile

        # Check current tile
        if 0 <= x < Constants.BOARD_WIDTH and 0 <= y < Constants.BOARD_HEIGHT:
            if self.tiles[y][x] == BoardTile.LADDER:
                return True

        # Now check the tile directly below
        y = board_position[1] - 1
        if 0 <= x < Constants.BOARD_WIDTH and 0 <= y < Constants.BOARD_HEIGHT:
            return self.tiles[y][x] == BoardTile.LADDER

        return False

    def draw(self):
        for row in range(Constants.BOARD_HEIGHT):
            for col in range(Constants.BOARD_WIDTH):
                tile = self.tiles[row][col]

                color = (35, 15, 15)
                x = col * Constants.TILE_WIDTH + Constants.TILE_WIDTH // 2 + 1
                y = row * Constants.TILE_HEIGHT + Constants.TILE_HEIGHT // 2 + 1
                arcade.draw_rectangle_outline(x, y, Constants.TILE_WIDTH, Constants.TILE_HEIGHT, color)
                if tile == BoardTile.PLATFORM:
                    arcade.draw_texture_rectangle(x, y,
                                                  self.platform_image.width, self.platform_image.height,
                                                  self.platform_image)
                elif tile == BoardTile.LADDER:
                    arcade.draw_texture_rectangle(x, y,
                                                  self.ladder_image.width, self.ladder_image.height,
                                                  self.ladder_image)
