#!/usr/bin/env python3

import os
import re
import sys
import json
from datetime import datetime, timedelta
from phonebook import AddressBook, Record
from notepad import NotePad, Record as NoteRecord, Title, Text, Tag
from helper import (
    COMMANDS_DESCRIPTION,
    validate_complex_args,
    get_suggestions,
    validate_args
)


# Dictionary with working days for sort operation
days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: 'Saturday', 6: 'Sunday'}


# Parse input on spaces
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


# Add contact with phone or add new phone to existing one
@validate_args(2, "contact-add")
def add_contact(args, book):
    name, phone = args
    new_record = book.find(name)
    res = ""
    if not new_record:
        new_record = Record(name)
        book.add_record(new_record)
        res += f"Contact with id = {new_record.id} added. "
    found_phone = new_record.find_phone(phone)
    if not found_phone:
        new_record.add_phone(phone)
        res += "Phone added."
    return res


@validate_args([1, 2, 3, 4], "contact-add-name")
def add_contact_name(args, book):
    name=" ".join(args)
    new_record = book.find(name)
    res = ""
    if not new_record:
        new_record = Record(name)
        book.add_record(new_record)
        res = f"Contact '{new_record.name.value}' with id = {new_record.id} added. "    
    return res


@validate_args([1, 2, 3, 4], "contact-change-name")
def change_contact_name(args, book):
    id, *name = args
    new_name=" ".join(name)
    record = book[int(id)]
    res = ""
    if record:
        record.set_name(new_name)
        res = f"Contact name '{record.name.value}' set for id = {record.id}"    
    return res


# Add birthday to contact or contact with birthday
@validate_args(2, "contact-add-birthday")
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


@validate_args(2, "contact-add-email")
def add_email(args, book):
    id, email = args
    record = book[int(id)]
    record.add_email(email)
    return f"Email {record.email} added to record {record.id}"


@validate_args([2, 3, 4, 5, 6, 7, 8, 9], "contact-add-address")
def add_address(args, book):
    print(args)
    id, *address = args
    print(address)
    record = book[int(id)]
    record.add_address(" ".join(address))
    return f"Address {record.address} added to record {id}"


# Change phone number
@validate_args(3, "contact-change")
def change_contact(args, book):
    name, phone1, phone2 = args
    record = book.find(name)
    if record:
        if record.edit_phone(phone1, phone2):
            return "Contact updated."
        else:
            return "Contact not updated"
    else:
        raise IndexError("Contact not found.")


# Remove phone from contact
@validate_args(2, "contact-remove-phone")
def remove_phone(args, book):
    name, phone = args
    record = book.find(name)
    if record:
        if record.remove_phone(phone):
            return f"Phone number {phone} removed"
        else:
            return f"Phone number {phone} not found"


# Show phones for contact
@validate_args(1, "contact-phone")
def show_phone(args, book):
    name = args[0]
    record = book.find(name)

    if record:
        res = f"{name}: " + ",".join([ph.value for ph in record.phones])
        return res
    else:
        raise IndexError("Contact not found.")


# Delete contact from book
@validate_args(1, "contact-delete")
def delete_contact(args, book):
    name = args[0]
    res = book.delete(name)
    return f"Contact {res if res else 'not'} deleted"


# Show contact birthday
@validate_args(1, "contact-show-birthday")
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)

    if record:
        res = f"{name} birthday: {record.birthday.value if 'birthday' in record.__dict__ else 'NA'}"
        return res
    else:
        raise IndexError("Contact not found.")

def birthday_sort_key(d):
    return datetime.strptime(d['date'], "%d.%m.%Y").timestamp()


# Get birthday for the specified number of days from date value
@validate_args([0, 1], "birthdays")
def get_birthdays(args, book):
    days_from_today = int(args[0]) if len(args) != 0 else 7
    
    today = datetime.today().date()

    users = [
        {
            "name": value.name.value,
            "birthday": datetime.strptime(value.birthday.value, "%d.%m.%Y"),
        }
        for key, value in book.items()
        if "birthday" in value.__dict__
    ]
    res = []

    for user in users:
        name = user["name"]
        birthday = user["birthday"].date()  # Convert to date type
        birthday_this_year = birthday.replace(year=today.year)
        
        if birthday_this_year < today:
            birthday_this_year = birthday.replace(year=today.year + 1)
        delta_days = (birthday_this_year - today).days
        if delta_days <= days_from_today:
            greet_date = user["birthday"].replace(year=today.year)
            set_day = birthday_this_year.weekday()
            
            #add entry to internal greet list
            greet_date_str = greet_date.strftime("%d.%m.%Y")
            present = False
            for i in range(len(res)):
                if greet_date_str in res[i].values():
                    present = True
                    break
            if not present:
                new = {}
                new['date'] = greet_date_str
                new['weekday'] = days[set_day]
                new['names'] = [name]
                res.append(new)
            else:
                res[i]['names'].append(name)

    # sorted output starting from current date
    res.sort(key=birthday_sort_key)
    output_message = ''
    for entry in res:
        names = ", ".join(n for n in entry['names'])
        output_message += f"{entry['date']}, {entry['weekday']:<10}| {names};\n" 
    output_message = output_message or "Birthdays not found"

    return output_message


# Display all contacts
def show_all(args, book):
    # res=""
    # for key,value in contacts.items():
    return "\n".join([f"{key}: {value}" for key, value in book.items()])


# load from json file, name as param
@validate_args([0, 1], "book-load")
def load_book_data(args, book):
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
            if "address" in ln.keys():
                new_record.add_address(ln["address"])
            if "email" in ln.keys():
                new_record.add_email(ln["email"])
            book.add_record(new_record)
    return "Book loaded"


# Write to json file, name as param
@validate_args([0, 1], "book-write")
def write_book_data(args, book):
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
        if "address" in record.__dict__:
            contact["address"] = record.address.value
        if "email" in record.__dict__:
            contact["email"] = record.email.value
        contacts.append(contact)

    with open(filename, "w") as fh:
        json.dump(contacts, fh)
    return "Book written"


def show_help(args, book):
    return "\n".join(COMMANDS_DESCRIPTION.values())


@validate_complex_args(2, "note-add")
def note_add(args, notepad):
    print(f"DEBUG: note_add: {args}")
    if len(args) == 2:
        title = args[0]
        text = args[1]
    if len(args) > 2:
        command = ' '.join(args)
        matches = re.findall(r"'(.*?)'", command)
        title = matches[0]
        text = matches[1]
    if notepad.find_record_by_title(Title(title)) is None:
        notepad.add_record(NoteRecord(text))
        return ("{:<7} {}".format('[ok]', 'Note added.'))
    else:
        return f"A note with the title {title} exists"

# Greeting display function
def hello(*_):
    return "{:<7} {}".format("[*]", 'How can I help you?')


# Function of generating the KeyboardInterrupt interrupt for exit
def exit(*_):
    raise KeyboardInterrupt

def debug_input(args, _):
    return args

# Available operations on contacts
actions = {
    "contact-add": add_contact,
    "contact-add-name": add_contact_name,
    "contact-change-name": change_contact_name,
    "contact-change": change_contact,
    "contact-remove-phone": remove_phone,
    "contact-phone": show_phone,
    "contact-delete": delete_contact,
    "contact-add-email": add_email,
    "contact-change-email": add_email,
    "contact-add-address": add_address,
    "contact-change-address": add_address,
    "contact-add-birthday": add_birthday,
    "contact-show-birthday": show_birthday,
    "book-load": load_book_data,
    "book-write": write_book_data,
    "birthdays": get_birthdays,
    "help": show_help,
    "all": show_all,
    "hello": hello,
    "exit": exit,
    "close": exit
}

notepad_actions = {
    "note-add": note_add,
    "my-debug": debug_input,
}


def main():
    TEST_MODE = True
    TEST_FILE = 'test_commands.txt'

    book = AddressBook()
    notepad = NotePad()

    print("{:<7} {}".format("[*]", "Welcome to the assistant bot!"))

    test_commands = None
    test_line = 0
    if TEST_MODE:
        with open(TEST_FILE, "r") as fh:
            test_commands = fh.read().splitlines()

    while True:
        try:
            if TEST_MODE:
                user_input = test_commands[test_line]
                test_line += 1
            else:
                user_input = input("{:<7} {}".format("[*]", "Enter a command: "))
            if user_input:
                command, *args = parse_input(user_input)
            else:
                continue

            if command in actions.keys():
                print(actions[command](args, book))
            elif command in notepad_actions.keys():
                print(notepad_actions[command](args, notepad))
            else:
                suggested_commands = get_suggestions(command)
                if len(suggested_commands):
                    print(
                        "Invalid command. Maybe you mean one of these:\n" +
                        suggested_commands
                    )
                else:
                    print("{:<7} {}".format("[error]", "Invalid command."))
        except (ValueError, EOFError):
            continue


# Main function
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("{:<8} {}".format("\n[*]", "Good bye!"))
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
