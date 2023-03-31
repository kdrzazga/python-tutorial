from person import Person
from temperature_converter import TemperatureConverter
from counter import Counter

print('Hello')

person = Person('Hans', 44)
print(person.greet())

c = 30
f = TemperatureConverter.celsius_to_fahrenheit(c)
print(f)
print(TemperatureConverter.fahrenheit_to_celsius(f))

print("\nCounting in a loop...")
counter = Counter()
for x in range(1, 10):
    print(counter._Counter__current)  # the way to access private memeber
    counter.increment()

print("\nSumming up...")
suma = lambda a, b: a + b
print(suma(3, 5))
print(suma(7, 15))
print(suma(1, 2))

print("\nCars:")
cars = ["Ford", "Volvo", "Syrena"]
cars.append("VW")
cars.insert(2, "Fiat")

for x in cars:
    print(x)

print(id(counter))  # id of an object


def mutable_param(lst=[]):
    lst.append(1)
    lst.append(2)
    return lst


def proper_mutable_param(lst=None):
    if lst is None:
        lst = []
    lst.append(1)
    lst.append(2)
    return lst


print(mutable_param())  # gathers alrguments
print(mutable_param())
print(mutable_param())

print(proper_mutable_param())  # collects alrguments
print(proper_mutable_param())
print(proper_mutable_param())
