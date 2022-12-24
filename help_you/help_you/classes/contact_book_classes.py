from collections import UserDict
import pickle
from datetime import datetime
from re import search, IGNORECASE


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    pass


class Phone(Field):
    @staticmethod
    def verify_phone(value):
        phone = search(r'(^\d{12}$)|(^0\d{9}$)', value)
        if not phone:
            raise ValueError("Phone number must be 12 or 10 digits")

    @Field.value.setter
    def value(self, value):
        self.verify_phone(value)
        self._value = value


class Email(Field):

    @staticmethod
    def verify_email(value):
        """Верифікація введеного e-mail користувача"""

        email = search(r"^[a-z0-9._-]{2,64}@\w{2,}[.]\w{2,3}$", value, flags=IGNORECASE)
        if not email:
            raise ValueError("Е-mail must contain letters, numbers and symbols [._-]")

    @Field.value.setter
    def value(self, value):
        self.verify_email(value)
        self._value = value


class Birthday(Field):

    @staticmethod
    def verify_birthday(value):
        """Верифікація введеної дати народження користувача. Очікується формат ХХ.ХХ.ХХХХ або Х.Х.ХХХХ """

        birthday = search(r"^\d{1,2}\.\d{1,2}\.\d{4}$", value)
        if not birthday:
            raise ValueError("Invalid format birthday")
        else:
            today = datetime.now().date()
            birthday = datetime.strptime(value, "%d.%m.%Y").date()
            if birthday > today:
                raise ValueError("That date has not yet come")
            else:
                return birthday

    @Field.value.setter
    def value(self, value):
        self._value = self.verify_birthday(value)


class Address(Field):
    @staticmethod
    def verify_address(value):
        """Верифікація введеної адреси. Повинна складатися мінімум з 2 символів """

        address = search(r'^[a-z0-9,-/]{2,}$', value)
        if not address:
            raise ValueError("Аddress must be longer than 1 letter")

    @Field.value.setter
    def value(self, value):
        self.verify_address(value)
        self._value = value


class Note:
    def __init__(self, name=None, tags=None, text=None):
        self.name = ""
        self.tags = []
        self.text = ""

    def add_content(self):
        pass

    def clear_text(self):
        pass

    def clear_tags(self):
        pass


class Record:
    def __init__(self, name: str, phone=None, email=None, address=None, birthday=None, note=None):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.addresses = []
        self.birthday = None
        self.note = None

        if phone:
            self.add_phone(phone)

        if birthday:
            self.set_birthday(birthday)

        if email:
            self.add_email(email)

        if address:
            self.add_address(address)

        if note:
            self.add_note(note)

    def add_phone(self, new_phone):
        """Додавання номеру телефону. Проходить перевірку дублікатів при наявності інших номерів """

        new_phone = Phone(new_phone)
        if not self.phones:
            self.phones.append(new_phone)
            return f"Phone '{new_phone}' is added"
        else:
            for phone in self.phones:
                if phone.value != new_phone.value:
                    self.phones.append(new_phone)
                    return f"Phone '{new_phone}' is added"
                else:
                    return f"Phone '{new_phone}' already exist in Contact. Try again!"

    def change_phone(self, old_phone, new_phone):
        """Зміна номеру телефону на новий """

        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return f"Phone '{old_phone}' is changed"
        return f"Phone '{old_phone}' is not in AddressBook. Try again!"

    def remove_phone(self, del_phone):
        """Видалення номеру телефону """
        for phone in self.phones:
            if phone == del_phone:
                self.phones.remove(phone)
                return f"Phone '{del_phone}' is delete"
        return f"Phone '{del_phone}' is not in AddressBook. Try again!"

    def set_birthday(self, birthday):
        """Встановлення дати народження """

        if self.birthday:
            return f"The date of birthday already exist in contact '{self.name}'"
        else:
            self.birthday = Birthday(birthday)
            return f"Date of birthday is added to the contact '{self.name}'"

    def change_birthday(self, new_birth):
        """Зміна дати народження """

        self.birthday = new_birth
        return f"Date of birthday '{self.name}' is changed: '{new_birth}'"

    def remove_birthday(self):
        """Видалення дати народження контакту """
        if self.birthday:
            self.birthday = None
            return f"Date of birthday is deleted"
        return f"This contact does not have a date of birth"

    def add_email(self, new_email):
        """Додавання електронної пошти контакту. Проходить перевірку дублікатів при наявності інших e-mail """

        new_email = Email(new_email)
        if not self.emails:
            self.emails.append(new_email)
            return f"Email '{new_email}' is added"
        else:
            for email in self.emails:
                if email.value != new_email.value:
                    self.emails.append(new_email)
                    return f"E-mail '{new_email}' is added"
                else:
                    return f"E-mail '{new_email}' already exist in AddressBook. Try again!"

    def change_email(self, old_email, new_email):
        """Заміна електронної пошти контакту """

        for email in self.emails:
            if email.value == old_email:
                email.value = new_email
                return f"E-mail '{old_email}' is changed"
        return f"E-mail '{old_email}' is not in AddressBook. Try again!"

    def remove_email(self, del_email):
        """Видалення електронної пошти контакту """

        for email in self.emails:
            if email == del_email:
                self.phones.remove(email)
                return f"E-mail '{del_email}' is delete"
        return f"E-mail '{del_email}' is not in AddressBook. Try again!"

    def add_address(self, new_address):
        """Додавання адреси контакту. Проходить перевірку дублікатів при наявності інших адрес """

        new_address = Address(new_address)
        if not self.addresses:
            self.addresses.append(new_address)
            return f"Address '{new_address}' is added"
        else:
            for address in self.addresses:
                if address.value != new_address.value:
                    self.addresses.append(new_address)
                    return f"Address '{new_address}' is added"
                else:
                    return f"Address '{new_address}' already exist in AddressBook. Try again!"

    def change_address(self, old_address, new_address):
        """Заміна адреси контакту """

        for address in self.addresses:
            if address.value == old_address:
                address.value = new_address
                return f"Address '{old_address}' is changed"
        return f"Address '{old_address}' is not in AddressBook. Try again!"

    def remove_address(self, del_address):
        """Видалення адреси контакту """
        for address in self.addresses:
            if address == del_address:
                self.addresses.remove(address)
                return f"Address '{del_address}' is delete"
        return f"Phone '{del_address}' is not in AddressBook. Try again!"

    def days_to_birthday(self):
        """Визначення кількості днів до дня народження """
        today = datetime.now().date()
        birthday = self.birthday.value.replace(year=today.year)
        delta = (birthday - today).days if birthday > today else (birthday.replace(birthday.year + 1) - today).days
        return delta

    def add_note(self, note):
        pass

    def edit_information_contact(self, command, field, val):
        """"Редагування(заміна ти видалення) полів контакту"""

        if command == "change":
            for i in val:
                phone = (
                    self.change_phone(val[0], val[1])
                    if Phone.verify_phone(val[0]) and Phone.verify_phone(val[1])
                    else None
                )
                birthday = (
                    self.change_birthday(val[0])
                    if Birthday.verify_birthday(val[0])
                    else None
                )
                address = (
                    self.change_address(val[0], val[1])
                    if Address.verify_address(val[0]) and Address.verify_address(val[1])
                    else None
                )
                email = (
                    self.change_email(val[0], val[1])
                    if Email.verify_email(val[0]) and Email.verify_email(val[1])
                    else None
                )
        elif command == "del":
            for i in val:
                phone = (
                    self.remove_phone(val[0]) if Phone.verify_phone(val[0]) else None
                )
                birthday = (
                    self.remove_birthday()
                    if Birthday.verify_birthday(val[0])
                    else None
                )
                address = (
                    self.remove_address(val[0])
                    if Address.verify_address(val[0])
                    else None
                )
                email = (
                    self.remove_email(val[0])
                    if Email.verify_email(val[0])
                    else None
                )
        else:
            raise ValueError(f"Command '{command}' is missing")


class ContactBook(UserDict):
    def __init__(self, file_path=None):
        super().__init__()
        self.file_path = ""
        self.count = 0

    def iterator(self, n):
        """Пагінація - посторінковий вивід Контактної книги """

        contacts_in_page = list(self.data.keys())
        if self.count >= len(contacts_in_page):
            raise StopIteration("This is the end of ContactBook")
        result_list = contacts_in_page[self.count: min(self.count + n, len(contacts_in_page))]
        for i in result_list:
            self.count += 1
        yield result_list

    def save_to_file(self):
        """Збереження Книги контактів у бінарний файл """

        with open(self.file_path, "wb") as file:
            pickle.dump(self.data, file)
        return f"ContactBook save in '{self.file_path}'"

    def load_from_file(self):
        """Завантаження Книги контактів з бінарного файлу """

        with open(self.file_path, "rb") as file:
            self.data = pickle.load(file)
        return f"ContactBook loaded from '{self.file_path}'"
