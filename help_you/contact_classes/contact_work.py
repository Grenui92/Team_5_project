from help_you.book import Book
from os import path
from help_you.contact_classes.record import Record
from help_you.contact_classes.fields import Phone, Email, Address, Birthday
class WorkContact:
    def __init__(self):
        """При ініціалізації відкриваєм бінарний файл з якого
        створюєм нову книжку. Якщо файл пустий - створюєм
        порожню книжку"""
        self.contacts_book = Book(path.join("database", "contacts"))
        try:
            print(self.contacts_book.load_from_file())
        except FileNotFoundError:
            print(self.contacts_book.save_to_file())

    """Методи приймають розпарсені дані від користувача args"""

    def save_to_file(self):
        return self.contacts_book.save_to_file()

    def load_from_file(self):
        return self.contacts_book.load_from_file()

    def create(self, *args) -> str:
        if args[0] in self.contacts_book:
            return f"Note with name '{args[0]} already exist."
        else:
            self.contacts_book[args[0]] = Record(args[0])
            return f"Contact with name {args[0]} successfully created."

    def show_all(self, *_) -> list:
        """Створює рядок з інформацією про кожен контакт"""

        records = list(self.contacts_book.values())
        rec_info = []
        for record in records:
            rec_info.append(str(record))

        return rec_info

    def show_one(self, *args: list) -> str:
        name = args[0]
        return f"{str(self.contacts_book[name]) if name in self.contacts_book else f'Contact {name} is not founded'}"

    def show_page(self, *args):
        """Ітеруємось по записам і формуєм рядок з контактами по n штук на сторінку"""
        result = []
        for page in self.contacts_book.iterator(int(args[0])):
            result_str = ""
            for record in page:
                result_str += str(self.contacts_book[record]) + "\n"
            result.append(f"\nPage Start\n{result_str}Page End")
        return result

    def delete_all(self):
        answer = input(
            f'You about to delete all records in book. You shure? Y/N')
        if answer == 'Y':
            self.contacts_book.data = {}
            return 'Contacts book now clean'
        else:
            return 'Not deleted'

    def delete_one(self, *args: list):
        name = args[0]
        if name in self.contacts_book:
            del self.contacts_book[name]
            return f"Contact {name} is deleted"
        else:
            f"Contact {name} is not in book"

    def add_values(self, *args):
        try:
            name = args[0]
            field = args[1][0]
            value = args[1][1:]
        except IndexError:
            raise IndexError("Not enough information.")

        records_fields_methods = {'phones': self.contacts_book.data[name].add_phone,
                                  'emails': self.contacts_book.data[name].add_email,
                                  'addresses': self.contacts_book.data[name].add_address,
                                  'birthday': self.contacts_book.data[name].set_birthday
                                  }
        return records_fields_methods[field](" ".join(list(value)))

    def search_in(self, search_data):

        """Пошук заданого фрагмента у нотатках"""
        result = []
        for value in self.contacts_book.values():
            if search_data in (value.name.value,
                               *[phone.value for phone in value.phones if isinstance(phone, Phone)],
                               *[email.value for email in value.emails if isinstance(email, Email)],
                               *[address.value for address in value.addresses if isinstance(address, Address)],
                               *[value.birthday.value if isinstance(value.birthday, Birthday) else "Bimba"]):
                result.append(value)
        return result

    def edit_information(self, *args):
        name = args[0]
        command = args[1][0]
        field = args[1][1]
        values = args[1][2:]

        if name in self.contacts_book.data:
            return self.contacts_book.data[name].edit_information_contact(command, field, values)
        else:
            return "This contact doesn't exist!"

    def show_nearest_birthdays(self, *args):

        n = int(args[0])
        n_days_birthday = []

        for contact in self.contacts_book.values():
            if contact.days_to_birthday() <= n:
                n_days_birthday.append(f"Days to {contact.name.value}'s birthday : {contact.days_to_birthday()} days \n")
        return n_days_birthday if n_days_birthday else f'No birthdays in nearest {n} days'

    def days_to_birthday_for_one(self, *args):
        name = args[0]
        return self.contacts_book.data[name].days_to_birthday()

    def days_to_birthday_for_all(self, *_):
        bdays = []

        for contact in self.contacts_book.data.values():
            bdays.append(f"Days to {contact.name.value}'s birthday: {contact.days_to_birthday()}")

        return bdays if bdays else 'There is no birthdays in contacts'

    def edit_name(self, *args):
        name = args[0]
        new_name = args[1]
        if new_name in self.contacts_book.data:
            return f"{name}'s name has been changed to {new_name}"
        else:
            return f'{name} not in contacts'