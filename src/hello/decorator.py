def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func("Jasiu")
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_hello(name):
    print("Hello,", name)

say_hello()
