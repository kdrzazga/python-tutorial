from board import Board

class BoardFactory:

    road_distance = 2


    def __init__(self):
        self.board = Board()


    def create_spiral_board(self, center_x, center_y, distant_x, distant_y):
        self._create_meadow_ring()
        self.board.cells[center_x][center_y].ground = 'road'
        self._create_spiral(center_x, center_y, distant_x, distant_y)


    def _create_spiral(self, center_x, center_y, distant_x, distant_y):
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        direction = 0
        ring_size = 1
        ring_count = 0
        current_x, current_y = center_x, center_y

        while current_x != distant_x or current_y != distant_y:
            for _ in range(ring_size):
                next_x, next_y = current_x + dx[direction], current_y + dy[direction]
                if self._is_valid_position(next_x, next_y):
                    self.board.cells[next_x][next_y].ground = 'road'
                    current_x, current_y = next_x, next_y
                else:
                    return
            direction = (direction + 1) % 4
            ring_count += 1
            if ring_count == 2:
                ring_size += BoardFactory.road_distance + 1
                ring_count = 0


    def _is_valid_position(self, x, y):
        return 0 <= x < self.board.num_rows and 0 <= y < self.board.num_columns


    def _create_meadow_ring(self):
        for x in range(self.board.num_rows):
            self.board.cells[x][0].ground = 'meadow'
            self.board.cells[x][1].ground = 'meadow'
            self.board.cells[x][self.board.num_columns - 2].ground = 'meadow'
            self.board.cells[x][self.board.num_columns - 1].ground = 'meadow'