class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello. I am {self.name}."


class Employee(Person):
    def __int__(self, name, age, job_title):
        super().__init__(name, age)
        self.job_title = job_title