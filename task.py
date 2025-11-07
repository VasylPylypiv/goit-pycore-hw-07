from address_book import Phone, Birthday, Record, AddressBook


def input_error(func):
    def wrapper(args, book):
        try:
            if args and not args:
                raise ValueError("Input cannot be empty")
            return func(args, book)
        except ValueError as e:
            return f"Error: {str(e)}"
        except AttributeError:
            return "Error: Contact not found."
        except Exception:
            return "Invalid input. Please try again"
    return wrapper


@input_error
def add_birthday(args, book):
    name, birthday, *_ = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}"
    else:
        raise ValueError(f"Contact {name} not found")


@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if record and record.birthday:
        return f"Birthday for {name}: {record.birthday}"
    elif record:
        return f"No birthday set for {name}"
    else:
        raise ValueError(f"Contact {name} not found")


@input_error
def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "No upcoming birthdays in the next week"
    result = "Upcoming birthdays in the next week:\n"
    for birthday in upcoming_birthdays:
        result += f"{birthday['name']}: {birthday['congratulation_date']}\n"
    return result


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return f"Phone number updated for {name}"
    else:
        raise ValueError(f"Contact {name} not found")


@input_error
def show_phone(args, book):
    name, *_ = args
    record = book.find(name)
    if record:
        return '; '.join(str(p) for p in record.phones)
    else:
        raise ValueError(f"Contact {name} not found")


@input_error
def show_all_contacts(args, book):
    if not book.data:
        return "No contacts found"
    return "\n".join(str(record) for record in book.data.values())


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ").strip().lower()

        if not user_input:
            print("Input cannot be empty. Please try again.")
            continue

        command, *args = user_input.split()

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all_contacts(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()