def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def add_contact(args, contacts):
    if len(args)<2:
        return "Not enough data"
    name, phone = args
    if name not in contacts.keys():
        contacts[name] = phone
        return "Contact added."
    else:
        return "Contact already exists"

def change_contact(args, contacts):
    if len(args)<2:
        return "Not enough data"
    name, phone = args
    if name in contacts.keys():
        contacts[name] = phone
        return "Contact updated."
    else:
        return "Contact not exists."

def show_phone(args, contacts):
    if len(args)!=1:
        return "Not enough data"
    name = args[0]    
    if name in contacts.keys():
        return f"{name}: {contacts[name]}"
    else:
        return f"Contact {name} not exists"

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
    
