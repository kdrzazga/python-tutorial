# https://sio2.mimuw.edu.pl/c/oij14-1/p/ser/

heart = (
    ' @@@   @@@ ',
    '@   @ @   @',
    '@    @    @',
    '@         @',
    ' @       @ ',
    '  @     @  ',
    '   @   @   ',
    '    @ @    ',
    '     @     ')


def write_heart():
    for line in heart:
        print(line)


N = input('How many hearts should be written? ')
for _ in range(int(N)):
    write_heart()
