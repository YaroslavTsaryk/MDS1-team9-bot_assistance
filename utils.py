from collections import UserDict
from datetime import datetime, timedelta
import re
import json
import difflib

# Dictionary with working days for sort operation
days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday"}


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Birthday(Field):
    # реалізація класу
    def __init__(self, Field):
        self.__value = None
        self.value = Field

    @property
    def value(self):
        return self.__value

    # Verification for current and previous century, 12 months, 31 days
    @value.setter
    def value(self, v):
        if re.search(
            "^(0[1-9]|[1,2][0-9]|3[0-1])\.(0[1-9]|1[0-2])\.(19\d\d|20\d\d)$", v
        ):
            self.__value = v
        else:
            raise ValueError


class Name(Field):
    # реалізація класу
    def __init__(self, Field):
        self.value = Field


class Phone(Field):
    # реалізація класу
    def __init__(self, Field):
        self.__value = None
        self.value = Field

    @property
    def value(self):
        return self.__value

    # Phone length 10 digits
    @value.setter
    def value(self, v):
        if re.search("^\d{10}$", v):
            self.__value = v
        else:
            raise ValueError


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_birthday(self, value):
        field = Birthday(value)
        self.birthday = field

    def add_phone(self, value):
        field = Phone(value)
        self.phones.append(field)

    def remove_phone(self, value):
        res = ""
        for ph in self.phones:
            if ph.value == value:
                res = ph
        if res:
            self.phones.remove(res)
            return True
        else:
            return False

    def edit_phone(self, old_value, new_value):
        for ph in self.phones:
            if ph.value == old_value:
                ph.value = new_value
                return True
        return False

    def find_phone(self, value):
        for ph in self.phones:
            if ph.value == value:
                return ph
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday if 'birthday' in self.__dict__ else 'NA'} "  # if p.value is not None


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name] = record
        return record

    # Search before any other operation
    def find(self, name):
        for n in self.data.keys():
            if n.value == name:
                return self.data[n]
        return None

    def delete(self, name):
        res = None
        for n in self.data.keys():
            if n.value == name:
                res = n
        if res:
            del self.data[res]
        return res

    def show_birthday(self, name):
        rec = self.find(name)
        if rec:
            print(f"{rec.name} birthday: {rec.birthday}")
