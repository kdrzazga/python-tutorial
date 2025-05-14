# https://sio2.mimuw.edu.pl/c/oij14-1/p/par/
from datetime import datetime


def is_number_even_digit(number: int):
    number_str = str(number)

    for i in range(0, len(number_str)):
        digit = int(number_str[i])
        if digit % 2 != 0:
            return False
    return True


def find_even_digit_numbers(amount: int):
    n = 2
   # even_digit_numbers = []
    even_digit_number = 0

    while amount > 0:
        if is_number_even_digit(n):
            #even_digit_numbers.append(n)
            even_digit_number = n
            amount -= 1
        n += 1
    return even_digit_number


N = input('Give number: ')

print(datetime.now())
#for nmbr in find_even_digit_numbers(int(N)):
#    print(nmbr)

print(find_even_digit_numbers(int(N)))

print(datetime.now())