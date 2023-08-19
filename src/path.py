def find_area(matrix, x, y, a_count):
    def is_valid_move(nx, ny, visited):
        return 0 <= nx < len(matrix) and 0 <= ny < len(matrix[0]) and matrix[nx][ny] == 'a' and (nx, ny) not in visited
    
    def dfs(nx, ny, count, visited):
        if count > a_count:
            return []
        
        visited.add((nx, ny))
        paths = [(nx, ny)]
        
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = nx + dx, ny + dy
            if is_valid_move(new_x, new_y, visited):
                paths.extend(dfs(new_x, new_y, count + 1, visited))
        
        return paths
    
    if matrix[x][y] != 'a':
        return []
    
    visited = set()
    paths = dfs(x, y, 1, visited)
    return paths

# Example usage
matrix = [
    ['a', 'a', 'b', 'a'],
    ['b', 'a', 'a', 'b'],
    ['a', 'b', 'a', 'a'],
    ['a', 'b', 'a', 'b'],
    ['a', 'b', 'a', 'b'],
    ['a', 'b', 'a', 'b'],
    ['a', 'b', 'a', 'b'],
    ['a', 'b', 'a', 'b']
]

x, y = 1, 2
a_count = 3

result = find_area(matrix, x, y, a_count)

print ("Start: ", x, y)

print(result)
