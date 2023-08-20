from factory import BoardFactory

symbols = {'road' : '#', 'soil' : '.', 'meadow' : ','}

def draw(board):
    for row in board.cells:
        for cell in row:
            print(symbols[cell.ground], end='')
        print()
        

create_spiral = BoardFactory()
create_spiral.create_spiral_board(9, 10, 0, 20)
draw(create_spiral.board)
    