import re
import difflib


COMMANDS_DESCRIPTION = {
    # command
    "contact-add": "contact-add <contact_name> <phone_number> - " +
    "Adds contact with a phone number. Phone number must be 10 digits",
    # command
    "contact-delete": "contact-delete <id> - " +
    "Deletes contact data from book",
    # command
    "contact-add-name": "contact-add-name <firstname> ... <lastname> - " +
    "Adds name to existing contact",
    # command
    "contact-add-email": "contact-add-email <id> <email> - " +
    "Adds contact email",
    # command
    "contact-add-address": "contact-add-address <id> <address_parapm_1> ..." +
    "<address_param_8> - Add address with up to 8 parts",
    # command
    "contact-change-name": "contact-change-name <id> <firstname> " +
    "... <lastanme> - Changes name of existing contact by ID",
    # command
    "contact-change": "contact-change <contact_name> <old_phone_number> " +
    "<new_phone_number> - Change existing phone number for existing contact",
    # command
    "contact-add-birthday": "contact-add-birthday <contact_name> <date> - " +
    "Add birthday data for existing contact or new contact " +
    "with birthday only. Date format DD.MM.YYYY",
    # command
    "contact-phone": "contact-phone <contact_name> - " +
    "Displays phones for contact",
    # command
    "contact-remove-phone": "contact-remove-phone <contact_name>" +
    " <phone_number> - Removes the phone number.",
    # command
    "contact-show-birthday": "contact-show-birthday <contact_name> - " +
    "Display birthday data for contact.",
    # command
    "birthdays": "birthdays <date> - Shows birtdays for next 7 days from" +
    " selected date. Date format DD.MM.YYYY",
    # command
    "all": "all - Shows all available contacts.",
    # command
    "book-load": "book-load <filename> - loads data from json file. " +
    "Default filename - data.bin",
    # command
    "book-write": "book-write <filename> - writes book data into file. " +
    "Default filename - data.bin",
    # command
    "note-add": "note-add <title> <text> - Add a new note",
    # command
    "hello": "hello - Get a greeting",
    # command
    "close": "close - Exit the program",
    # command
    "exit": "exit - Exit the program",
    # command
    "note-add": "'<note title>' '<note text>' - Add a note with the name",
}


# Function decorator for validating function arguments
def validate_args(expected_arg_len, command):
    def decorator(func):
        def wrapper(*args):
            args_optional = isinstance(expected_arg_len, list)
            if ((args_optional and (len(args[0]) not in expected_arg_len)) or
                    (not args_optional and len(args[0]) != expected_arg_len)):
                return (
                    "{:<7} {:<34} {}".format(
                        '[error]',
                        "Invalid command format. Please use:",
                        COMMANDS_DESCRIPTION[command]))
            try:
                return func(*args)
            except BaseException as e:
                return str(e)
        return wrapper
    return decorator

# Function decorator for validating complex function arguments
def validate_complex_args(expected_arg_len, command):
    def decorator(func):
        def wrapper(*args):
            list_of_values = args[0]
            if len(list_of_values) <= 1:
                return (
                    "{:<7} {:<34} {}".format(
                        '[error]',
                        "Invalid command format. Please use:",
                        COMMANDS_DESCRIPTION[command]))
            elif len(list_of_values) == 2:
                pass
            else:
                string_for_regexp = ' '.join(list_of_values)
                matches = re.findall(r"'(.*?)'", string_for_regexp)
                if len(matches) != expected_arg_len:
                    return (
                        "{:<7} {:<34} {}".format(
                            '[error]',
                            "Invalid command format. Please use:",
                            COMMANDS_DESCRIPTION[command]))
            try:
                return func(*args)
            except BaseException as be:
                return str(be)
        return wrapper
    return decorator

# Find suggested commands
def get_suggestions(command):
    options = COMMANDS_DESCRIPTION.keys()

    def find_suggestions_by_part(command_part):
        # retrieve all commands where current command is substring
        suggestions = list(filter(lambda cmd: command_part in cmd, options))
        # retrieve up to 3 commands with get_close_matches
        suggestions += difflib.get_close_matches(command_part, options)
        return suggestions

    suggested_commands = []
    command_parts = command.split('-')
    for part in command_parts:
        suggested_commands += find_suggestions_by_part(part)

    unique_suggestions = set(suggested_commands)
    result = {key: COMMANDS_DESCRIPTION[key] for key in unique_suggestions}

    return "\n".join(result.values())
