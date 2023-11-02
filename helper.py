import difflib


COMMANDS_DESCRIPTION = {
    "all": "all - Shows all available contacts.",
    "load": "load <filename> - loads data from json file. " +
    "Default filename - data.bin",
    "write": "write <filename> - writes book data into file. " +
    "Default filename - data.bin",
    "add": "add <contact_name> <phone_number> - " +
    "Adds contact with a phone number. Phone number must be 10 digits",
    "change": "change <contact_name> <old_phone_number> <new_phone_number>" +
    " - Change existing phone number for existing contact",
    "add-birthday": "add-birthday <contact_name> <date> - " +
    "Add birthday data for existing contact or new contact " +
    "with birthday only. Date format DD.MM.YYYY",
    "phone": "phone <contact_name> - Displays phones for contact",
    "remove-phone": "remove-phone <contact_name> <phone_number> - " +
    "Removes the phone number.",
    "show-birthday": "show-birthday <contact_name> - " +
    "Display birthday data for contact.",
    "birthdays": "birthdays <date> - Shows birtdays for next 7 days from" +
    " selected date. Date format DD.MM.YYYY",
    "delete": "delete <contact_name> - Deletes contact data from book.",
    "hello": "hello - Get a greeting",
    "close": "close - exit the program",
    "exit": "exit - exit the program",
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
