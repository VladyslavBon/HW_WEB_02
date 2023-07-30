from collections import UserDict
from datetime import datetime
from pickle import dump, load
from re import search

class Field:
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

class Name(Field):
    pass

class Address(Field):
    @Field.value.setter
    def value(self, value):
        if not value:
            self._value = value
        else:
            self._value = value

class Phone(Field):
    @Field.value.setter
    def value(self, value):
        if not value:
            self._value = value
        else:
            new_value = (
                value.removeprefix("+")
                .replace("(", "")
                .replace(")", "")
                .replace("-", "")
                .replace(" ", "")
            )
            if len(new_value) in [10, 12] and new_value.isdigit():
                self._value = new_value
            else:
                self._value = ""
                print("Invalid phone number. It contain only 10 or 12 digits.")
        
class Email(Field):
    @Field.value.setter
    def value(self, value):
        if not value:
            self._value = value
        else:
            new_value = search(r"[a-zA-Z0-9_.]+@[a-zA-Z]+[.][a-zA-Z]{2,}", value)
            if new_value:
                self._value = new_value.group()
            else:
                self._value = ""
                print("Invalid email.")
        
class Birthday(Field):
    @Field.value.setter
    def value(self, value):
        if not value:
            self._value = value
        else:
            try:
                datetime.strptime(value, "%d.%m.%Y")
                self._value = value
            except ValueError:
                self._value = ""
                print("Invalid birthday format. Please use DD.MM.YYYY")

class Record:
    def __init__(self, name: Name, phone: Phone = "", email: Email = "", birthday: Birthday = "", address: Address = ""):
        self.name = name
        self.phones = [phone]
        self.email = email
        self.birthday = birthday
        self.address = address

    def days_to_birthday(self):
        if self.birthday:
            current_datetime = datetime.now().date()
            d, m, y = self.birthday.value.split(".")
            birthday_date = datetime(year=int(y), month=int(m), day=int(d))
            new_datetime = birthday_date.replace(year=current_datetime.year).date()
            difference = new_datetime - current_datetime
            return difference

    def add_phone(self, phone):
        self.phones.append(phone)

    def delete_phone(self, phone):
        for i, number in enumerate(self.phones):
            if phone == number:
                self.phones.pop(i)

    def change_phone_num(self, old_phone, new_phone):
        for i, number in enumerate(self.phones):
            if old_phone == number:
                self.phones[i] = new_phone

class AddressBook(UserDict):
    def add_record(self, record):
        self.data.update({record.name.value: record})

class AddressBookBot:
    def __init__(self):
        try:
            with open("data.bin", "rb") as fh:
                self.ab = load(fh)
        except FileNotFoundError:
            self.ab = AddressBook()

    def add(self):
        self.name = Name(input("Enter name: ").strip().title())
        self.phone = Phone(input("Enter phone: ").strip())
        self.email = Email(input("Enter email: ").strip())
        self.birthday = Birthday(input("Enter birthday: ").strip())
        self.address = Address(input("Enter address: ").strip())
        # try:
        if self.name.value not in self.ab.data:
            record = Record(self.name, self.phone, self.email, self.birthday, self.address)
            self.ab.add_record(record)
        else:
            print("This contact already added.")
        #     self.ab[self.name.value].add_phone(self.phone)
        # except UnboundLocalError:
        #     pass
    
    def when_birthday(self):
        name = input("Enter cantact's name: ").strip().title()
        if name in self.ab.data:
            days_to_birthday = str(self.ab[name].days_to_birthday()).split(",")
            print(f"{days_to_birthday[0]} to {name}'s birthday")
        else:
            print("No contact with this name.")

    def show_all(self):
        for rec in self.ab.data.values():
                print(rec.name.value, "|", [x.value for x in rec.phones], "|", rec.email.value, "|", rec.birthday.value, "|", rec.address.value, "|")

    def save(self):
        with open("data.bin", "wb") as fh:
                dump(self.ab, fh)

    def search(self):
        search = input("Enter any piece of information for searching: ").strip().lower()
        for rec in self.ab.data.values():
            if search in rec.name.value.lower() or search in rec.phones[:].value or search in rec.email.value or search in rec.birthday.value or search in rec.address.value:
                print(rec.name.value, "|", [x.value for x in rec.phones], "|", rec.email.value, "|", rec.birthday.value, "|", rec.address.value, "|")
            else:
                print('No matches')
    
def address_book_main():
    abd = AddressBookBot()
    print("please write 'info' to get instructson about adressbook comands")

    while True:
        string = input('Enter command to AddressBook: ').lower()
        
        if string in ["good bye", "close", "exit"]:
            abd.save()
            print("You went to Personal Helper")
            break

        elif string == "info":
            print("Enter 'add (name) (phone)' to add contact's name and phone")
            print("Enter 'show all' to show all contacts in Address Book")

        elif string == "show all":
            abd.show_all()

        elif string.startswith("add"):
            abd.add()
        
        elif string.startswith("birthday"):
            abd.when_birthday()

        elif string.startswith("search"):
            abd.search()
            
if __name__ == "__main__":
    address_book_main()