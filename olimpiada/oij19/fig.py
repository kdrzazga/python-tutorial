# https://sio2.mimuw.edu.pl/c/oij19-1/p/fig/
import math
# unfinished

def find_path(field_count):
    potential_square_side = math.ceil(math.sqrt(field_count))
    rectangle_side = field_count // potential_square_side

    rest = field_count - potential_square_side * rectangle_side

    print(potential_square_side, rectangle_side, potential_square_side * rectangle_side, rest)


print(find_path(10))