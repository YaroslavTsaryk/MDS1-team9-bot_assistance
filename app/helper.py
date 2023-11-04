import re
import difflib


COMMANDS_DESCRIPTION = {
    # command
    "contact-add-phone": "contact-add-phone <id> <phone_number> - " +
    "Adds a phone number to the contact by id. Phone number must be 10 digits",
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
    "contact-change-phone": "contact-change-phone <id> <old_phone_number> " +
    "<new_phone_number> - Change existing phone number for existing contact",
    # command
    "contact-add-birthday": "contact-add-birthday <id> <date> - " +
    "Add birthday data for existing contact or new contact " +
    "with birthday only. Date format DD.MM.YYYY",
    # command
    "contact-phone": "contact-phone <id> - " +
    "Displays phones for contact",
    # command
    "contact-remove-phone": "contact-remove-phone <id>" +
    " <phone_number> - Removes the phone number.",
    # command
    "contact-show-birthday": "contact-show-birthday <contact_name> - " +
    "Display birthday data for contact.",
    # command
    "birthdays": "birthdays <days> - Shows birtdays for the specified" +
    " number of days from today. By default - 7 days",
    # command
    "contacts-all": "contacts-all - Shows all available contacts.",
    # command
    "book-load": "book-load <filename> - loads data from json file. " +
    "Default filename - data.bin",
    # command
    "book-write": "book-write <filename> - writes book data into file. " +
    "Default filename - data.bin",
    # command
    "hello": "hello - Get a greeting",
    # command
    "close": "close - Exit the program",
    # command
    "exit": "exit - Exit the program",
    # command
    "note-add": "note-add '<note title>' '<note text>' - " +
    "Add a note with the name",
    # command
    "note-delete": "note-delete '<note title>' - " +
    "Delete the note with the title",
    # command
    "note-add-tag": "note-add-tag '<note title>' '<tag>' - " +
    "Add a tag to a note",
    # command
    "note-get-all": "note-get-all - Get a list of all notes",
    # command
    "note-sort": "note-sort - Sort notes by number of tags in descending order, then alphabetically by title",
    # command
    "notes-load": "notes-load <filename> - loads data from a json file. " +
    "Default filename - notes.bin",
    # command
    "notes-write": "notes-write <filename> - writes the notes to a file. " +
    "Default filename - notes.bin",
    # command
    "note-get": "note-get <id> or note-get '<title>' - Get a note entry by its unique integer identifier or by its title",
    # command
    "note-edit": "note-edit '<title>' '<new text>' - Edit a note entry by its name",
    # command
    "note-get-tag": "note-get-tag <tag> - Get a note entry (entries) by its tag",
    # command
    "note-rename": "note-rename <existing title> <new title> - Rename a note entry by its original title",
    # command
    "note-search": "note-search '<pattern>' - Search for note entries by pattern",
    # command
    "note-delete-tag": "note-delete-tag '<title>' '<tag>' - Delete a tag entry by note name",
}


def parse_command(command):
    pattern = re.compile(r"'([^']*)'|\b(\S+)\b")
    matches = pattern.findall(command)
    parsed_arguments = [m[0] or m[1] for m in matches]
    return parsed_arguments

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
            commands = args[0]
            if len(command) == 1:
                commands = ' '.join(commands + ['MOCK'])
            else:
                commands = ' '.join(commands)
            parsed_arguments = parse_command(commands)
            if len(parsed_arguments) != expected_arg_len:
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
    all_commands = COMMANDS_DESCRIPTION.keys()

    def find_suggestions_by_part(command_part):
        options = '-'.join(all_commands).split('-')
        potential_suggestions = difflib.get_close_matches(
            command_part,
            options,
            12
        )
        potential_suggestions_unique = list(set(potential_suggestions))
        # retrieve all commands where current command is substring
        suggestions = []
        for cmd_part in potential_suggestions_unique:
            suggestions += list(
                filter(lambda cmd: cmd_part in cmd, all_commands)
            )

        return suggestions

    suggested_commands = []
    command_parts = command.split('-')
    for part in command_parts:
        suggested_commands += find_suggestions_by_part(part)

    unique_suggestions = set(suggested_commands)
    result = {key: COMMANDS_DESCRIPTION[key] for key in unique_suggestions}

    return "\n".join(result.values())


# Function for determining the type of input data
def detect_input_type(value):
    try:
        int_value = int(value)
        return int_value, 'int'
    except ValueError:
        pass

    try:
        float_value = float(value)
        return float_value, 'float'
    except ValueError:
        pass

    return value, 'str'
