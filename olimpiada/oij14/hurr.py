# https://sio2.mimuw.edu.pl/c/oij14-1/p/hur/

N = input('Give number: ')

for i in range(1, int(N)):
    if i % 7 == 0 and i % 11 == 0:
        print('Wiwat!')
    elif i % 7 == 0:
        print('Hurra!')
    elif i % 11 == 0:
        print('Super!')
    else:
        print(i)
