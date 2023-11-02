from datetime import datetime, timedelta
import json
from phonebook import AddressBook, Record
from helper import (
    COMMANDS_DESCRIPTION,
    get_suggestions,
    validate_args
)


# Dictionary with working days for sort operation
days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday"}


# Parse input on spaces
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


# Add contact with phone or add new phone to existing one
@validate_args(2, "add")
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
@validate_args(2, "add-birthday")
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
@validate_args(3, "change")
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
@validate_args(2, "remove-phone")
def remove_phone(args, book):
    name, phone = args
    record = book.find(name)
    if record:
        if record.remove_phone(phone):
            return f"Phone number {phone} removed"
        else:
            return f"Phone number {phone} not found"


# Show phones for contact
@validate_args(1, "phone")
def show_phone(args, book):
    name = args[0]
    record = book.find(name)

    if record:
        res = f"{name}: " + ",".join([ph.value for ph in record.phones])
        return res
    else:
        raise IndexError("Contact not found.")


# Delete contact from book
@validate_args(1, "delete")
def delete_contact(args, book):
    name = args[0]
    res = book.delete(name)
    return f"Contact {res if res else 'not'} deleted"


# Show contact birthday
@validate_args(1, "show-birthday")
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)

    if record:
        res = f"{name} birthday: {record.birthday.value if 'birthday' in record.__dict__ else 'NA'}"
        return res
    else:
        raise IndexError("Contact not found.")


# Get birthday for next 7 days from date value
@validate_args(1, "birthdays")
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
@validate_args([0, 1], "load")
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
@validate_args([0, 1], "write")
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


def show_help(args, book):
    return "\n".join(COMMANDS_DESCRIPTION.values())


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
    "help": show_help,
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
            suggested_commands = get_suggestions(command)
            if len(suggested_commands):
                print(
                    "Invalid command. Maybe you mean one of these:\n" +
                    suggested_commands
                )
            else:
                print("Invalid command.")


if __name__ == "__main__":
    main()
