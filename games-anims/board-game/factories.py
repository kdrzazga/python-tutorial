from board import Board
from globals import Constants, BoardTile


class BoardFactory:

    @staticmethod
    def create_room1():
        b = Board()

        for x in range(0, 2 * Constants.BOARD_WIDTH // 3):
            b.tiles[Constants.BOARD_HEIGHT - 3][x] = BoardTile.PLATFORM

        b.tiles[Constants.BOARD_HEIGHT - 5][0] = BoardTile.PLATFORM
        b.tiles[Constants.BOARD_HEIGHT - 5][1] = BoardTile.PLATFORM

        for x in range(2 * Constants.BOARD_WIDTH // 3, Constants.BOARD_WIDTH):
            b.tiles[Constants.BOARD_HEIGHT // 2 - 3][x] = BoardTile.PLATFORM

        for y in range(4, 12):
            b.tiles[Constants.BOARD_HEIGHT - y][7] = BoardTile.LADDER

        return b
