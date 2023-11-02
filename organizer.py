from datetime import datetime, timedelta
import json
from phonebook import AddressBook, Record
from helper import (
    COMMANDS_DESCRIPTION,
    get_suggestions,
    validate_args
)


# Dictionary with working days for sort operation
days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: 'Saturday', 6: 'Sunday'}


HELP = (
    """load - load data from json file. Default filename - data.bin
load <filename> - load data from specified json file
write - write book data into file. Default filename - data.bin
write <filename> - write data to cpecified json file
add <contact_name> <phone_number> - Add contact with a phone number. Phone number must be 10 digits
change <contact_name> <old_phone_number> <new_phone_number> - Change existing phone number for existing contact
add-birthday <contact_name> <date> - Add birthday data for existing contact or new contact with birthday only. Date format DD.MM.YYYY
phone <contact_name> - Display phones for contact
show-birthday <contact_name> - Display birthday data for contact
birthdays <days from today> - Show birtdays for the next specified number of days, 7 days if no argument given
delete <contact_name> - Delete contact data from book
hello - get a greeting
close or exit - exit the program
""")

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

def birthday_sort_key(d):
    return datetime.strptime(d['date'], "%d.%m.%Y").timestamp()


# Get birthday for the specified number of days from date value
@validate_args(1, "birthdays")
def get_birthdays_per_week(args, book):
    days_from_today = int(args[0]) if len(args) != 0 else 7
    
    today = datetime.today().date()

    users = [
        {
            "name": key.value,
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
