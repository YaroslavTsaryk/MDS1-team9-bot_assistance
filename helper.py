import difflib


COMMANDS_DESCRIPTION = {
    "load-book":"load-book - load data from json file. Default filename - data.bin",
    "load-book":"load-book <filename> - load data from specified json file",
    "write-book":"write-book - write book data into file. Default filename - data.bin",
    "write-book":"write-book <filename> - write data to cpecified json file",
    "add-contact-name":"add-contact-name <long name>- add new contact long name",
    "change-contact-name":"change-contact-name <id> <long name>- change contact long name by id",
    "add-contact":"add-contact <contact_name> <phone_number> - Add contact with a phone number. Phone number must be 10 digits",
    "change-contact":"change-contact <contact_name> <old_phone_number> <new_phone_number> - Change existing phone number for existing contact",
    "add-birthday":"add-birthday <contact_name> <date> - Add birthday data for existing contact or new contact with birthday only. Date format DD.MM.YYYY",
    "add-email":"add-email <id> <email> - add email to contact by id",
    "change-email":"change-email <id> <email> - change email for contact by id",
    "add-address":"add-address <id> <address all string> - add address to contact by id",
    "change-address":"change-address <id> <address all string> - change address for contact by id",
    "phone":"phone <contact_name> - Display phones for contact",
    "show-birthday":"show-birthday <contact_name> - Display birthday data for contact",
    "birthdays":"birthdays <days from today> - Show birtdays for the next specified number of days, 7 days if no argument given",    
    "delete-contact":"delete-contact <contact_name> - Delete contact data from book",
    "hello":"hello - get a greeting",
    "close":"close or exit - exit the program",
    "exit":"close or exit - exit the program"

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
