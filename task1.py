from collections import UserDict
import operator
from datetime import datetime, timedelta, date
import re
import json

# Dictionary with working days for sort operation
days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday"}


# Decorate some access errors
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name"
        except ValueError:
            return "Give me name, phone or date please."
        except IndexError:
            return "Contact not found"

    return inner


# Parse input on spaces
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


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


# Add contact with phone or add new phone to existing one
@input_error
def add_contact(args, book):
    name, phone = args
    new_record = book.find(name)
    res = ""
    if not new_record:
        new_record = Record(name)
        book.add_record(new_record)
        res += "Contact added. "
    found_phone = new_record.find_phone(phone)
    if not found_phone:
        new_record.add_phone(phone)
        res += "Phone added."
    return res


# Add birthday to contact or contact with birthday
@input_error
def add_birthday(args, book):
    name, birthday = args
    new_record = book.find(name)
    res = ""
    if not new_record:
        new_record = Record(name)
        book.add_record(new_record)
        res += "Contact added. "
    new_record.add_birthday(birthday)
    res += "Birthday added. "
    return res


# Change phone number
@input_error
def change_contact(args, book):
    name, phone1, phone2 = args
    record = book.find(name)
    if record:
        if record.edit_phone(phone1, phone2):
            return "Contact updated."
        else:
            return "Contact not updated"
    else:
        raise IndexError


# Remove phone from contact
@input_error
def remove_phone(args, book):
    name, phone = args
    record = book.find(name)
    if record:
        if record.remove_phone(phone):
            return f"Phone number {phone} removed"
        else:
            return f"Phone number {phone} not found"


# Show phones for contact
@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)

    if record:
        res = f"{name}: " + ",".join([ph.value for ph in record.phones])
        return res
    else:
        raise IndexError


# Delete contact from book
@input_error
def delete_contact(args, book):
    name = args[0]
    res = book.delete(name)
    return f"Contact {res if res else 'not'} deleted"


# Show contact birthday
@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)

    if record:
        res = f"{name} birthday: {record.birthday.value if 'birthday' in record.__dict__ else 'NA'}"
        return res
    else:
        raise IndexError


# Get birthday for next 7 days from date value
@input_error
def get_birthdays_per_week(args, book):
    date_str = args[0] if len(args) != 0 else str(datetime.today().strftime("%d.%m.%Y"))
    today = datetime.strptime(date_str, "%d.%m.%Y").date()

    users = [
        {
            "name": key.value,
            "birthday": datetime.strptime(value.birthday.value, "%d.%m.%Y"),
        }
        for key, value in book.items()
        if "birthday" in value.__dict__
    ]
    res = {}

    for user in users:
        name = user["name"]
        birthday = user["birthday"].date()  # Convert to date type
        birthday_this_year = birthday.replace(year=today.year)
        if birthday_this_year < today:
            birthday_this_year = birthday.replace(year=today.year + 1)
        delta_days = (birthday_this_year - today).days
        if delta_days < 7:
            set_day = 0
            if birthday_this_year.weekday() > 4:
                if (
                    birthday_this_year - today
                ).days + 7 - birthday_this_year.weekday() < 7:  # Don't greet if greetings day on days after now+7
                    set_day = 0
                else:
                    continue
            else:
                set_day = birthday_this_year.weekday()
            if days[set_day] not in res.keys():
                res[days[set_day]] = [user["name"]]
            else:
                res[days[set_day]].append(user["name"])

    res2 = {}  # sorted starting from current date
    output_message = ""
    for i in range(7):
        sh = (today + timedelta(i)).weekday()
        if sh not in [5, 6]:
            if days[sh] in res.keys():
                res2[days[sh]] = res[days[sh]]
                message = ", ".join(res[days[sh]])
                # print(f'{days[sh]}: {message}')
                output_message += f"{days[sh]}: {message} \n"

    return output_message


# Display all contracts data
def show_all(args, book):
    # res=""
    # for key,value in contacts.items():
    return "\n".join([f"{key}: {value}" for key, value in book.items()])


# load from json file, name as param
@input_error
def load_data(args, book):
    filename = args[0] if len(args) != 0 else "data.bin"

    with open(filename, "r") as fh:
        book_state = json.load(fh)
        for ln in book_state:
            new_record = Record(ln["name"])
            if "phone" in ln.keys():
                for ph in ln["phone"]:
                    new_record.add_phone(ph)
            if "birthday" in ln.keys():
                new_record.add_birthday(ln["birthday"])
            book.add_record(new_record)
    return "Book loaded"


# Write to json file, name as param
@input_error
def write_data(args, book):
    filename = args[0] if len(args) != 0 else "data.bin"

    contacts = []
    for record in book.data.values():
        contact = {}
        contact["name"] = record.name.value
        phones = []
        for ph in record.phones:
            phones.append(ph.value)
        contact["phone"] = phones
        if "birthday" in record.__dict__:
            contact["birthday"] = record.birthday.value
        contacts.append(contact)

    with open(filename, "w") as fh:
        json.dump(contacts, fh)
    return "Book written"


# Available operations on contacts
actions = {
    "add": add_contact,
    "change": change_contact,
    "remove-phone": remove_phone,
    "phone": show_phone,
    "delete": delete_contact,
    "all": show_all,
    "load": load_data,
    "write": write_data,
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": get_birthdays_per_week,
}

book = AddressBook()


def main():
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        if user_input:
            command, *args = parse_input(user_input)
        else:
            continue

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command in actions.keys():
            print(actions[command](args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
