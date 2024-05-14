from addressbook import AddressBook
from record import Record
import pickle

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except IndexError as e:
            return str(e)
        except KeyError as e:
            return str(e)
        except Exception as e:
            return "Unexpected error"
    return inner

def format_upcoming_birthday(record, congratulation_date):
    return f"Contact: {record.name}, congratulation date: {congratulation_date.strftime('%d.%m.%Y')}"

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(book: AddressBook, args):
    name, phone = args    
    record = book.find(name)
    message = "Contact updated."
    if not record:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    record.add_phone(phone)  

    return message

@input_error
def get_phone(book: AddressBook, args):
    name = args[0]
    record = book.find(name, strict=True)
    return ", ".join(str(phone) for phone in record.phones)

@input_error
def change_contact(book: AddressBook, args):
    name, phone_to_edit, phone = args
    record = book.find(name, strict=True)
    record.edit_phone(phone_to_edit, phone)

    return "Contact changed."

def all(book: AddressBook):
    return "\n".join(str(record) for record in book.data.values())

@input_error
def add_birthday(book: AddressBook, args):
    name, birthday = args  
    record = book.find(name, strict=True)
    record.add_birthday(birthday)
    return "Birthday added."

@input_error
def show_birthday(book: AddressBook, args):
    name = args[0]
    record = book.find(name, strict=True)
    return str(record.birthday)

def birthdays(book: AddressBook):
    return "\n".join(format_upcoming_birthday(*item) for item in book.get_upcoming_birthdays())


def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(book, args))
        elif command == "change":
            print(change_contact(book, args))
        elif command == "phone":
            print(get_phone(book, args))
        elif command == "all":
            print(all(book))
        elif command == "add-birthday":
            print(add_birthday(book, args))
        elif command == "show-birthday":
            print(show_birthday(book, args))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()