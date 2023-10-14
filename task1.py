def input_error(func):
    def inner(*args, **kwargs):
        try:            
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name"
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Contact not found"

    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts):
    name, phone = args
    if name not in contacts.keys():
        contacts[name] = phone
        return "Contact added."
    else:
        return "Contact already exists"

@input_error
def change_contact(args, contacts):
    name, phone = args
    if name in contacts.keys():
        contacts[name] = phone
        return "Contact updated."
    else:
        raise IndexError

@input_error
def show_phone(args, contacts):
    name = args[0]
    if name in contacts.keys():
        return f"{name}: {contacts[name]}"
    else:
        raise IndexError

def show_all(args,contacts):
    #res=""
    #for key,value in contacts.items():
    return "\n".join([f"{key}: {value}" for key,value in contacts.items()])

actions={'add':add_contact,
         'change':change_contact,
         'phone':show_phone,
         'all':show_all}

def main():
    contacts = {}
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
            print(actions[command](args,contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
    
