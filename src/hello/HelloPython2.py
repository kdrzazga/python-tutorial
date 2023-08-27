import string

from person import Employee
from person import Person


def get_data_as_tuple(p: Person) -> tuple[string, int]:
    return p.name, p.age


def get_data_as_tuple_of_3(e: Employee) -> tuple[
    string, string, int]:  # okresla zwracany typ, nic wspolnego z operatorem lambda
    return e.job_title, e.name, e.age


if __name__ == '__main__':
    person_tuple = get_data_as_tuple(Person("Marek", 33))
    print(person_tuple.__getitem__(0) + " is " + str(person_tuple.__getitem__(1)) + " years old")

    employee_tuple = get_data_as_tuple_of_3(Employee("Jasiu", 40, "Engineer"))
    print(employee_tuple[0] + " " + employee_tuple[1] + " is " + str(employee_tuple[2]) + " years old.")
