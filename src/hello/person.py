class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello. I am {self.name}."


class Employee(Person):

    def __init__(self, name, age, job_title):
        super().__init__(name, age)
        self.job_title = job_title
