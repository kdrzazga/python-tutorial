phonebook = {}


def read_name_decorator(func):
    def wrapper():
        name = input("Enter name")
        func(name)
    return wrapper


def read_data_decorator(func):
    def wrapper():
        name = input("Enter name")
        phone = input("Enter phone")
        func(name, phone)
    return wrapper


def contact_exists(contact):
    return contact in phonebook


@read_data_decorator
def create_contact(name, phone):
    phonebook[name] = phone


@read_name_decorator
def find_contact(name):
    if contact_exists(name):
        print(phonebook[name])
    else:
        print("Name not found")


@read_data_decorator
def update_contact(name, new_number):
    if contact_exists(name):
        phonebook[name] = new_number
    else:
        print("Name not found")


@read_name_decorator
def delete_contact(name):
    if contact_exists(name):
        del phonebook[name]
    else:
        print("Name not found")


options = 'c - create', 'f - find', 'u - update', 'd - delete', 'e - exit'

while True:
    for line in options:
        print("\t" + line)

    chosen_option = input("Choose option: ")

    match chosen_option:
        case 'c':
            create_contact()
        case 'f':
            find_contact()
        case 'u':
            update_contact()
        case 'd':
            delete_contact()
        case 'e':
            break
