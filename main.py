#!/usr/bin/env python3

import os
import re
import sys
import json
from datetime import datetime, timedelta
from app.phonebook import AddressBook, Record
from app.notepad import (
    Record as NoteRecord,
    NotePad,
    Title,
    Text,
    Tag
)
from app.helper import (
    COMMANDS_DESCRIPTION,
    validate_complex_args,
    detect_input_type,
    get_suggestions,
    validate_args,
    parse_command
)


# Dictionary with working days for sort operation
DAYS = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: 'Saturday',
    6: 'Sunday'}


# Parse input on spaces
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


# Add contact with phone or add new phone to existing one
@validate_args(2, "contact-add")
def add_contact_phone(args, book):
    id, phone = args
    if int(id) in book.data.keys():
        new_record = book[int(id)]
    else:
        return "Id not exists"
    res = ""
    found_phone = new_record.find_phone(phone)
    if not found_phone:
        new_record.add_phone(phone)
        res += "Phone added."
    return res


@validate_args([1, 2, 3, 4], "contact-add-name")
def add_contact_name(args, book):
    name = " ".join(args)
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
    new_name = " ".join(name)
    if int(id) in book.data.keys():
        if book.find(new_name):
            return "Name already in use"
        else:
            record = book[int(id)]
    else:
        return "Id not exists"
    res = ""
    if record:
        record.set_name(new_name)
        res = f"Contact name '{record.name.value}' set for id = {record.id}"
    return res


# Add birthday to contact or contact with birthday
@validate_args(2, "contact-add-birthday")
def add_birthday(args, book):
    id, birthday = args
    new_record = book[int(id)]
    res = ""
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
    id, *address = args
    if int(id) in book.data.keys():
        record = book[int(id)]
    else:
        return "Id not exists"
    record.add_address(" ".join(address))
    return f"Address {record.address} added to record {id}"


# Change phone number
@validate_args(3, "contact-change-phone")
def change_contact(args, book):
    id, phone1, phone2 = args
    record = book[int(id)]
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
    id, phone = args
    if int(id) in book.data.keys():
        record = book[int(id)]
    else:
        return "Id not exists"
    if record:
        if record.remove_phone(phone):
            return f"Phone number {phone} removed"
        else:
            return f"Phone number {phone} not found"


# Show phones for contact
@validate_args(1, "contact-phone")
def show_phone(args, book):
    name = " ".join(args)
    record = book.find(name)

    if record:
        res = f"{name}: " + ",".join([ph.value for ph in record.phones])
        return res
    else:
        raise IndexError("Contact not found.")


# Delete contact from book
@validate_args(1, "contact-delete")
def delete_contact(args, book):
    id = args[0]
    res = book.delete(id)
    return f"Contact {res if res else 'not'} deleted"


# Show contact birthday
@validate_args([1, 2, 3], "contact-show-birthday")
def show_birthday(args, book):
    name = " ".join(args)
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

            # add entry to internal greet list
            greet_date_str = greet_date.strftime("%d.%m.%Y")
            present = False
            for i in range(len(res)):
                if greet_date_str in res[i].values():
                    present = True
                    break
            if not present:
                new = {}
                new['date'] = greet_date_str
                new['weekday'] = DAYS[set_day]
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
    if not len(book.items()):
        return "{:<7} {}".format("[info]", "There are no contacts yet.")
        
    
    return "\n".join([f"{value}\n" for key, value in book.items()])


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
    command = ' '.join(args)
    title, text = parse_command(command)
    if notepad.find_record_by_title(Title(title)) is None:
        note_record = NoteRecord(Title(title))
        note_record.add_text(Text(text))
        notepad.add_record(note_record)
        return ("{:<7} Note added.".format('[ok]'))
    else:
        return (
            "{:<7} A note with the title [{}] exists".format(
                '[info]', title))


@validate_complex_args(2, "note-edit")
def note_edit(args, notepad):
    command = ' '.join(args)
    title, text = parse_command(command)
    record = notepad.find_record_by_title(Title(title))
    if record is None:
        return (
            "{:<7} A note with the title [{}] doesn't exists".format(
                '[info]', title))
    else:
        record.edit_text(Text(text))
        return ("{:<7} Note edited.".format('[ok]'))


@validate_complex_args(1, "note-delete")
def note_delete(args, notepad):
    command = ' '.join(args + ['MOCK'])
    title, _ = parse_command(command)
    if notepad.delete(Title(title)):
        return ("{:<7} Note deleted.".format('[ok]'))
    else:
        return (
            "{:<7} A note with the title [{}] doesn't exists".format(
                '[info]', title))


@validate_complex_args(2, "note-add-tag")
def note_add_tag(args, notepad):
    command = ' '.join(args)
    title, tag = parse_command(command)
    record_title = notepad.find_record_by_title(Title(title))
    if record_title is None:
        return (
            "{:<7} A note with the title [{}] doesn't exists".format(
                '[info]', title))
    else:
        record_tag = notepad.find_record_by_tag(Tag(tag))
        if record_tag is not None:
            return (
                "{:<7} This tag [{}] already exists".format(
                    '[info]', tag))
        else:
            record_title.add_tag(Tag(tag))
            return ("{:<7} Tag added.".format('[ok]'))


def note_get_all(_, notepad):
    if len(notepad.data) != 0:
        return "\n".join(["{:<7} {:<1} {}".format('[ok]', '-', single_record)
                         for single_record in notepad.data])
    else:
        return ("{:<7} {}".format('[info]', 'There are no notes.'))


def note_get_all_sorted(_, notepad):
    if len(notepad.data) != 0:
        sorted_notes = sorted(
            notepad.data,
            key=lambda x:
            len(x.tags),
            reverse=True
        )
        return "\n".join(["{:<7} {:<1} {}".format('[ok]', '-', single_record)
                         for single_record in sorted_notes])
    else:
        return ("{:<7} {}".format('[info]', 'There are no notes.'))


@validate_complex_args(1, "note-get")
def note_get(args, notepad):
    command = ' '.join(args + ['MOCK'])
    value, _ = parse_command(command)

    value, value_type = detect_input_type(value)
    if value_type == 'int':
        new_value = int(value)
    elif value_type == 'str':
        new_value = str(value)
    else:
        return ("{:<7} {}".format("[error]", "Unknown type of input value."))

    def handle_record_title(title):
        record = notepad.find_record_by_title(Title(title))
        if record is None:
            return (
                "{:<7} A note with the title [{}] doesn't exists".format(
                    '[info]', title))
        else:
            return ("{:<7} {:<1} {}".format('[ok]', '-', record))

    def handle_record_id(id):
        record = notepad.find_record_by_id(int(id))
        if record is None:
            return (
                "{:<7} A note with the id [{}] doesn't exists".format(
                    '[info]', id))
        else:
            return ("{:<7} {:<1} {}".format('[ok]', '-', record))

    type_handlers = {
        int: handle_record_id,
        str: handle_record_title,
    }

    handler = type_handlers.get(type(new_value))
    return handler(new_value)


@validate_complex_args(1, "note-get-tag")
def note_get_tag(args, notepad):
    command = ' '.join(args + ['MOCK'])
    tag, _ = parse_command(command)

    record = notepad.find_record_by_tag(Tag(tag))
    if record is None:
        return (
            "{:<7} A notes with the tag [{}] doesn't exists".format(
                '[info]', tag))
    else:
        return "\n".join(["{:<7} {:<1} {}".format('[ok]', '-', single_record)
                         for single_record in record])


@validate_complex_args(2, "note-rename")
def note_rename(args, notepad):
    command = ' '.join(args)
    title, new_title = parse_command(command)

    record = notepad.find_record_by_title(Title(title))
    if record is None:
        return (
            "{:<7} A note with the title [{}] doesn't exists".format(
                '[info]', title))
    else:
        record = notepad.find_record_by_title(Title(new_title))
        if record is not None:
            return ("{:<7} {}".format('[error]', 'A note with this name already exists.'))
        else:
            record.rename_title(Title(new_title))
            return ("{:<7} {}".format('[ok]', 'Note renamed.'))


@validate_complex_args(1, "note-search")
def note_search(args, notepad):
    command = ' '.join(args + ['MOCK'])
    pattern, _ = parse_command(command)

    record = notepad.find_record_by_text(pattern)
    if record is None:
        return (
            "{:<7} A notes with the pattern [{}] doesn't exists".format(
                '[info]', pattern))
    else:
        return "\n".join(["{:<7} {:<1} {}".format('[ok]', '-', single_record)
                         for single_record in record])


@validate_complex_args(2, "note-delete-tag")
def note_delete_tag(args, notepad):
    command = ' '.join(args)
    title, tag = parse_command(command)
    record = notepad.find_record_by_title(Title(title))
    if record is None:
        return (
            "{:<7} A note with the title [{}] doesn't exists".format(
                '[info]', title))
    else:
        record = notepad.find_record_by_tag(Tag(tag))
        if record is None:
            return (
                "{:<7} The tag [{}] doesn't exists".format(
                    '[info]', tag))
        else:
            for i in record:
                i.remove_tag(Tag(tag))
            return ("{:<7} Tag deleted.".format('[ok]'))


# load notes from json file, name as param
@validate_args([0, 1], "note-load")
def load_notes_data(args, notepad):
    filename = args[0] if len(args) != 0 else "notes.bin"

    with open(filename, "r") as fh:
        book_state = json.load(fh)
        for ln in book_state:
            new_record = NoteRecord(Title(ln["title"]))
            if "tags" in ln.keys():
                for tag in ln["tags"]:
                    new_record.add_tag(Tag(tag))
            if "text" in ln.keys():
                new_record.add_text(Text(ln["text"]))
            notepad.add_record(new_record)
    return "Notes loaded"

# Write to json file, name as param


@validate_args([0, 1], "note-write")
def write_notes_data(args, notepad):
    filename = args[0] if len(args) != 0 else "notes.bin"

    notes = []
    for record in notepad.data:
        note = {}
        note["title"] = record.title.value
        tags = []
        if len(record.tags):
            for tag in record.tags:
                tags.append(tag.value)
            note["tags"] = tags
        if "text" in record.__dict__:
            note["text"] = record.text.value
        notes.append(note)

    with open(filename, "w") as fh:
        json.dump(notes, fh)
    return "Notes written"


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
    "contacts-all": show_all,
    "contact-add-phone": add_contact_phone,
    "contact-add-name": add_contact_name,
    "contact-change-name": change_contact_name,
    "contact-change-phone": change_contact,
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
    "hello": hello,
    "exit": exit,
    "close": exit
}

notepad_actions = {
    "note-add": note_add,
    "note-edit": note_edit,
    "note-rename": note_rename,
    "note-delete": note_delete,
    "note-add-tag": note_add_tag,
    "note-get-tag": note_get_tag,
    "note-delete-tag": note_delete_tag,
    "note-get-all": note_get_all,
    "note-get": note_get,
    "note-search": note_search,
    "my-debug": debug_input,
    "note-sort": note_get_all_sorted,
    "notes-write": write_notes_data,
    "notes-load": load_notes_data,
}


def main():
    TEST_MODE = False
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
                print(f'[INPUT] {user_input}')
                test_line += 1
            else:
                user_input = input(
                    "{:<7} {}".format(
                        "[*]", "Enter a command: "))
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
                        "{:<7} {}".format(
                            "[info]",
                            "Invalid command. Maybe you mean one of these:\n" +
                            suggested_commands
                        ),
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
