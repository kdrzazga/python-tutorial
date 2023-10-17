import logging

phonebook = {}


def create_contact():
    name = input("Enter name")
    phone = input("Enter phone")
    phonebook[name] = phone


def find_contact(name):
    print(phonebook[name])


def update_contact(name, new_number):
    if name in phonebook:
        phonebook[name] = new_number
    else:
        logging.error("Name not found")


def delete_contact(name):
    del phonebook[name]


options = 'c - create', 'f - find', 'u - update', 'd - delete', 'e - exit'

while True:
    for line in options:
        print("\t" + line)

    chosen_option = input("Choose option: ")

    match chosen_option:
        case 'c':
            create_contact()
        case 'f':
            name = input("Contact for name")
            find_contact(name)
        case 'u':
            name = input("Enter name")
            new_number = input("Enter new number")
            update_contact(name, new_number)
        case 'd':
            name = input("Enter name")
            delete_contact(name)
        case 'e':
            break
