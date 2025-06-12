from functools import wraps
from collections import UserDict

PATH = "./contacts.txt"


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        self.name = name
        super().__init__(name)


class Phone(Field):
    def __init__(self, number):
        if not (number.isdigit() and len(number) == 10):
            raise ValueError("The phone must have 10 numbers")
        super().__init__(number)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, number: Phone):
        phone = number if isinstance(number, Phone) else Phone(number)
        self.phones.append(phone)

    def remove_phone(self, phone: Phone):
        # self.phones = list(filter(lambda p: p.value != phone.value, self.phones))
        self.phones = [p for p in self.phones if p.value != phone.value]
        return self.phones

    def find_phone(self, phone: Phone):
        for item in self.phones:
            if item.value == phone.value:
                return item

    def edit_phone(self, phone: Phone, new_phone: Phone):
        for index, p in enumerate(self.phones):
            if p.value == phone.value:
                self.phones[index] = new_phone
            return self.phones

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {';'.join(p.value for p in self.phones)}"


class AddressBook(UserDict):

    def add_record(self, record: Record):

        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str):
        del self.data[name]


# ----------


# decorator
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Please, enter name and phone"
        except FileNotFoundError:
            return f"File not found"
        except Exception:
            return "Please, enter a command."

    return inner


def get_contact_info(path: str = PATH) -> dict | None:
    with open(path, "r", encoding="utf-8") as file:
        contacts = {}
        for line in file:
            elements = line.strip().split(":", 1)
            if len(elements) == 2:
                key, value = elements
                contacts[key] = value
            else:
                pass
    return contacts


@input_error
def parse_input(user_input):

    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def save_contact(contact):
    path = PATH
    with open(path, "a+", encoding="utf-8") as file:
        name, phone = contact
        file.seek(0)
        file.write(f"{name}: {phone} \n")


@input_error
def update_contact(contact):
    path = PATH
    name, phone = contact
    contacts = get_contact_info(path)
    name = name.strip()
    phone = phone.strip()
    contacts[name] = phone
    with open(path, "w", encoding="utf-8") as file:
        for name in contacts:
            file.write(f"{name}:{contacts[name]}\n")


@input_error
def add_contact(args, path: str = PATH):
    name, phone = args
    contacts = get_contact_info(path)
    if name in contacts:
        return f"Contact {name} is already exists"
    else:
        contact = name, phone
        contacts[name] = phone
        save_contact(contact)
        return "Contact added."


@input_error
def change_contact(args, path: str = PATH):
    name, phone = args
    contacts = get_contact_info(path)
    if name in contacts:
        contact = name, phone
        update_contact(contact)
        return "Contact updated."
    else:
        return f"There is no contact {name}"


@input_error
def show_phone(args, path: str = PATH):
    name, *args = args
    contacts = get_contact_info(path)
    if name in contacts:
        return contacts.get(name)
    else:
        return f"There is no contact {name}"


@input_error
def show_all():
    path = PATH
    contacts = get_contact_info(path)
    if len(contacts):
        return f"{contacts}"
    else:
        return "There are no contacts"


@input_error
def bot_main(path: str = PATH):

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        if command in ["exit", "close"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args))
        elif command == "change":
            print(change_contact(args))
        elif command == "phone":
            print(show_phone(args))
        elif command == "all":
            print(show_all())
        else:
            print("Invalid command.")


if __name__ == "__main__":
    # bot_main()
    pass

    # Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі

print(book)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

# Видалення запису Jane
book.delete("Jane")
