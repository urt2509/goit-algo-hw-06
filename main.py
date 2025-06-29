from collections import UserDict


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

    # done
    def find_phone(self, phone: str):

        for item in self.phones:
            if item.value == phone:
                return item
        return None

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        found_phone = self.find_phone(phone)
        if found_phone:
            self.phones.remove(found_phone)
            return self.phones
        raise ValueError(f"The phone {phone} is not found")

    def edit_phone(self, phone: str, new_phone: str):
        found_phone = self.find_phone(phone)
        if not found_phone:
            raise ValueError(f"The phone {phone} is not found")

        self.remove_phone(phone)
        self.add_phone(new_phone)

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

    def __str__(self):
        return "\n".join(f"{name}:{record}" for name, record in self.data.items())
