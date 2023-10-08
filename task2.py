def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def add_contact(args, contacts):
    if len(args)<2:
        return "Not enough data"
    name, phone = args
    contacts[name] = phone
    return "Contact added."

def change_contact(args, contacts):
    if len(args)<2:
        return "Not enough data"
    name, phone = args
    contacts[name] = phone
    return "Contact changed."

def show_phone(args, contacts):
    if len(args)!=1:
        return "Not enough data"
    name = args[0]    
    if name in contacts.keys():
        return f"{name}: {contacts[name]}"
    else:
        return f"Contact {name} not exists"

def show_all(contacts):
    for key,value in contacts.items():
        print(f"{key}: {value} ")

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
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            show_all(contacts)
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()