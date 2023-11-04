from collections import UserDict
import re


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
            "^(0[1-9]|[1,2][0-9]|3[0-1])\\.(0[1-9]|1[0-2])\\.(19\\d\\d|20\\d\\d)$",
                v):
            self.__value = v
        else:
            raise ValueError("Date must be the following format: DD.MM.YYYY.")


class Email(Field):
    # реалізація класу
    def __init__(self, Field):
        self.__value = None
        self.value = Field

    @property
    def value(self):
        return self.__value

    # Verification for valid email
    @value.setter
    def value(self, v):
        if re.search(
            "^((?!\\.)[\\w\\-_.]*[^.])(@\\w+)(\\.\\w+(\\.\\w+)?[^.\\W])$", v
        ):
            self.__value = v
        else:
            raise ValueError("Date must be the following format: DD.MM.YYYY.")


class Address(Field):
    # реалізація класу
    def __init__(self, Field):
        self.__value = None
        self.value = Field

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, v):
        self.__value = v


class Email(Field):
    # реалізація класу
    def __init__(self, Field):
        self.__value = None
        self.value = Field

    @property
    def value(self):
        return self.__value

    # Verification for valid email
    @value.setter
    def value(self, v):
        if re.search(
            "^((?!\\.)[\\w\\-_.]*[^.])(@\\w+)(\\.\\w+(\\.\\w+)?[^.\\W])$", v
        ):
            self.__value = v
        else:
            raise ValueError


class Address(Field):
    # реалізація класу
    def __init__(self, Field):
        self.__value = None
        self.value = Field

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, v):
        self.__value = v


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
        if re.search("^\\d{10}$", v):
            self.__value = v
        else:
            raise ValueError("Phone must be 10 digits long.")


class Record:
    count = 1

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        #self.email = None
        #self.address = None
        self.id = Record.count
        Record.count += 1

    def set_name(self, new_name):
        self.name = Name(new_name)

    def add_birthday(self, value):
        field = Birthday(value)
        self.birthday = field

    def add_phone(self, value):
        field = Phone(value)
        self.phones.append(field)

    def add_email(self, value):
        field = Email(value)
        self.email = field

    def add_address(self, value):
        field = Address(value)
        self.address = field

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
        return f"Record id: {self.id}, Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones) if len(self.phones) else 'NA'}, birthday: {self.birthday if 'birthday' in self.__dict__ else 'NA'}, " \
            f"address: {self.address if 'address' in self.__dict__ else 'NA'}, email: {self.email if 'email' in self.__dict__ else 'NA'} "
        # if p.value is not None


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.id] = record
        return record

    # Search before any other operation
    def find(self, name):
        for k, n in self.data.items():
            if n.name.value == name:
                return self.data[k]
        return None

    def delete(self, id):
        res = None
        for n in self.data.keys():
            if n == int(id):
                res = n
        if res:
            del self.data[res]
        return res

    def show_birthday(self, id):
        rec = self.find(id)
        if rec:
            print(f"{rec.name} birthday: {rec.birthday}")

    def __str__(self):
        book_str = ''
        for id, record in self.data.items():
            book_str += str(record) + "\n"
        return book_str
