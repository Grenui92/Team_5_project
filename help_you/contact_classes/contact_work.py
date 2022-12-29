from book import Book
from contact_classes.fields import Phone, Email, Address, Birthday
from contact_classes.record import Record


class WorkContact:

    def __init__(self, path):

        self.contacts_book = Book(path)
        try:
            print(self.contacts_book.load_from_file())
        except FileNotFoundError:
            self.contacts_book.save_to_file()

    def save_to_file(self):
        return self.contacts_book.save_to_file()

    def load_from_file(self):
        return self.contacts_book.load_from_file()

    def create(self, name: str, *_) -> str:
        """Створюємо новий запис в книгу, якщо запису з таким ім'ям не існує."""
        if not name:
            raise ValueError("You can't create empty contact.")
        if name in self.contacts_book:
            return f"Contact with name '{name} already exist."
        else:
            self.contacts_book[name] = Record(name)
            return f"Contact with name {name} successfully created."

    def show_all(self, *_) -> list:
        """Створює рядок з інформацією про кожен контакт"""
        rec_info = []
        for record in self.contacts_book.values():
            rec_info.append(str(record))
        return rec_info if rec_info else "ContactBook is empty."

    def show_one(self, name: str, *_) -> str:
        """Виводить інформацію про один конкретний контакт"""
        if not name:
            raise ValueError("You can't search empty contact-name.")
        return f"{str(self.contacts_book[name]) if name in self.contacts_book else f'Contact {name} is not found.'}"

    def show_page(self, number_of_contacts: str, *_) -> list:
        """Ітеруємось по записам і формуєм сторінку з контактами по number_of_contacts штук на сторінку"""
        if number_of_contacts:
            n = int(number_of_contacts)
        else:
            n = 5
        result = []
        for page in self.contacts_book.iterator(n):
            result_str = []
            for record in page:
                result_str.append(str(self.contacts_book[record]))
            result.extend(["Page Start", *result_str, "Page End"])
        return result

    def delete_all(self, *_):
        """Видаляє ВСІ записи з контактної книги"""
        answer = input(
            f"You about to delete all records in book. You sure? Y/N: ")
        if answer == 'Y':
            self.contacts_book.data = {}
            return 'Contacts book now clean'
        else:
            return 'Not deleted'

    def delete_one(self, name: str, *_):
        """Видаляє один конкретний контакт з книги"""
        if not name:
            raise ValueError("You can't delete empty contact.")
        if name in self.contacts_book:
            del self.contacts_book[name]
            return f"Contact {name} is deleted"
        else:
            return f"Contact {name} is not in book"

    def add_values(self, name: str, args: list):
        """Додає інформацію до конкретного контактну у вказане поле"""
        try:
            field = args[0]
            information = args[1:]
        except IndexError:
            return "You can't add to contact empty information."
        if not field or not information:
            return "You can't add to contact empty information."
        records_fields_methods = {'phones': self.contacts_book[name].add_phone,
                                  'emails': self.contacts_book[name].add_email,
                                  'addresses': self.contacts_book[name].set_address,
                                  'birthday': self.contacts_book[name].set_birthday}
        if field not in records_fields_methods:
            return f"Wrong field '{field}'."
        return records_fields_methods[field](" ".join(information))

    def search_in(self, search_data: str, *_) -> list:
        """Пошук заданого фрагмента у контактах"""
        if not search_data:
            raise ValueError("Empty search information")
        result = []
        for value in self.contacts_book.values():
            search_target = [value.name.value,
                             *[phone.value for phone in value.phones if isinstance(phone, Phone)],
                             *[email.value for email in value.emails if isinstance(email, Email)],
                             *[value.birthday.value if isinstance(value.birthday, Birthday) else None]]
            if isinstance(value.addresses, Address):
                search_target.extend(value.addresses.value.split())
            if search_data in (search_target):
                result.append(value)
        return result

    def edit_information(self, name: str, args: list) -> str:
        """Редагує інформацію у вказаному полі вказаного контакт. Command може приймати два значення - change & del. Change відповідає за
        заміну інформації. Del - видаляє її."""

        try:
            command, field, values = args[0], args[1], [args[2], *args[3:]]
        except IndexError:
            return "You can't edit contact with empty information."
        if name in self.contacts_book:
            return self.contacts_book[name].edit_information_contact(command, field, values)
        else:
            return "This contact doesn't exist!"

    def show_nearest_birthdays(self, days: str, *_) -> list:
        """Показує у кого з контактів відбудеться день народження протягом найблищчих days днів"""
        try:
            n = int(days)
        except ValueError:
            n = 5

        n_days_birthday = []
        for contact in self.contacts_book.values():
            if isinstance(contact.birthday, Birthday) and contact.days_to_birthday() <= n:
                n_days_birthday.append(f"Days to {contact.name.value}'s birthday : {contact.days_to_birthday()} days \n")
        return n_days_birthday if n_days_birthday else f'No birthdays in nearest {n} days'

    def days_to_birthday_for_one(self, name: str, *_) -> str:
        """Показує скільки днів до дня народження конкретного контакту"""
        return f"Days to birthday for {name} = {self.contacts_book.data[name].days_to_birthday()}"

    def days_to_birthday_for_all(self, *_) -> list:
        """Показує скільки днів до дня народження всіх контактів"""
        birthdays = []
        for contact in self.contacts_book.values():
            birthdays.append(f"Days to {contact.name.value}'s birthday: {contact.days_to_birthday()}")
        return birthdays if birthdays else 'There is no birthdays in contacts'

    def edit_name(self, name: str, args: list) -> str:
        """Змінює ім'я запису. Змінює як ім'я-ключ контакту, так і в самому контакті"""
        try:
            new_name = args[0]
        except IndexError:
            raise IndexError("You can't edit name with empty information.")
        record: Record = self.contacts_book[name]
        record.name.value = new_name
        self.contacts_book[new_name] = record
        del self.contacts_book[name]
        return f"{name}'s name has been changed to {new_name}"
