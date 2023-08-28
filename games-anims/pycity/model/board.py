from collections import deque

from cell import Cell


class Board:

    cell_types = ['soil', 'road', 'meadow']


    def __init__(self):
        self.num_rows = 19
        self.num_columns = 21
        self.cells = [[Cell(x, y) for y in range(self.num_columns)] for x in range(self.num_rows)]


    def get_route(self, x1, y1, x2, y2):
        if not self.is_valid_position(x1, y1) or not self.is_valid_position(x2, y2):
            return None
        
        visited = [[False] * self.num_columns for _ in range(self.num_rows)]
        visited[x1][y1] = True
        queue = deque([(x1, y1, [])])
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        while queue:
            x, y, path = queue.popleft()
            
            if x == x2 and y == y2:
                return path
            
            for dx, dy in moves:
                new_x, new_y = x + dx, y + dy
                if self.is_valid_position(new_x, new_y) and not visited[new_x][new_y] and self.cells[new_x][new_y].road:
                    visited[new_x][new_y] = True
                    queue.append((new_x, new_y, path + [(new_x, new_y)]))
        
        return None

    
    def is_valid_position(self, x, y):
        return 0 <= x < self.num_rows and 0 <= y < self.num_columns and self.cells[x][y].ground == 'road'
        