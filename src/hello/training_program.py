import json
import pickle
from enum import Enum

phonebook = {}


def save_json(file):
    json.dump(phonebook, file)


def load_json(file):
    return json.load(file)


def save_pickle(file):
    pickle.dump(phonebook, file)


def load_pickle(file):
    return pickle.load(file)


class FileFormat(Enum):
    JSON = (save_json, load_json)
    PICKLE = (save_pickle, load_pickle)

    def __new__(cls, save_method, load_method):
        obj = object.__new__(cls)
        obj._save = save_method
        obj._load = load_method
        return obj

    def get_filename(self):
        return f'obj.{self.name.lower()}'

    def save(self):
        fname = self.get_filename()
        print("Saving", fname)
        with open(fname, "wb" if self == FileFormat.PICKLE else "w") as file:
            self._save(file)

    def load(self):
        fname = self.get_filename()
        print("Reading", fname)
        with open(fname, "rb" if self == FileFormat.PICKLE else "r") as file:
            return self._load(file)


format = FileFormat.JSON
phonebook = format.load()


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

    chosen_option = input("Choose option: ").lower().strip()

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
            format.save()
            break
