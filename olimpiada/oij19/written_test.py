import math
import sys

tab = []
for i in range(1000):
    tab.append([])
    for j in range(1000):
        tab[i].append(0)

print(sys.getsizeof(tab))

integers = (0, 255, 31000, 2 * math.pow(10, 9))

for i in integers:
    print(sys.getsizeof(i))

integer = 2
float_number = 2.1
double_number = 0.00000000000000000000000000000000001
boolean_variable = True
char = 'a'
string3_var = "abc"
string19_var = "Litwo Ojczyzno moja"

print("\nSizes of integer, float, double, bool:")
print(sys.getsizeof(integer))
print(sys.getsizeof(float_number))
print(sys.getsizeof(double_number))
print(sys.getsizeof(boolean_variable))
print(sys.getsizeof(char))
print(sys.getsizeof(string3_var))
print(sys.getsizeof(string19_var))

print('17th letter of alphabet is r')
print(chr(ord('a') + 17))
