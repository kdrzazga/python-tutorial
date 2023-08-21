from factory import BoardFactory
from board import Board

symbols = {'road' : '#', 'soil' : '.', 'meadow' : ','}

def draw(board):
    for i, row in enumerate(board.cells):
        for cell in row:
            print(symbols[cell.ground], end='')
        print('  ' + str(i))
    
    for i in range(board.num_columns):
        print(str(i % 10), end = '')

create_spiral = BoardFactory()
create_spiral.create_spiral_board(9, 10, 0, 20)
draw(create_spiral.board)
