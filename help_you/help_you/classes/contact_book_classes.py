from collections import UserDict
import pickle
from datetime import datetime
from re import search, IGNORECASE
from os import path


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
        if phone:
            if len(phone.string) == 12:
                return f"+{phone.string}"
            elif len(phone.string) == 10:
                return f"+38{phone.string}"
        else:
            raise ValueError("Phone number must be just 12 or 10 digits")

    @Field.value.setter
    def value(self, value):
        self._value = self.verify_phone(value)


class Email(Field):

    @staticmethod
    def verify_email(value):
        """Верифікація введеного e-mail користувача"""

        email = search(
            r"^[a-z0-9._-]{2,64}@\w{2,}[.]\w{2,3}$", value, flags=IGNORECASE)
        if email:
            return email
        else:
            raise ValueError(
                "Е-mail must contain letters, numbers and symbols [._-]")

    @Field.value.setter
    def value(self, value):
        self._value = self.verify_email(value)


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
        if address:
            return address
        else:
            raise ValueError("Аddress must be longer than 1 letter")

    @Field.value.setter
    def value(self, value):
        self._value = self.verify_address(value)


class Record:
    def __init__(self, name: str, phone=None, email=None, address=None, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone else []
        self.emails = [Email(email)] if email else []
        self.addresses = [Address(address)] if address else []
        self.birthday = Birthday(birthday) if birthday else None

    def __str__(self):
        string = f'name: {self.name.value}\n\
                    phones: {[phone.value for phone in self.phones]}\n\
                    emails: {[email.value for email in self.emails]}\n\
                    birthday: {self.birthday.value}\n\''
        # notes: \nnote:{self.note.name}\n\
        #         text:{self.note.text}\n\
        #         tags:{self.note.tags}'
        return string

    def add_phone(self, new_phone: str):
        """Додавання номеру телефону. Проходить перевірку дублікатів при наявності інших номерів """

        new_phone = Phone(new_phone)
        if not self.phones:
            self.phones.append(new_phone)
            return f"Phone '{new_phone}' is added"
        else:
            for phone in self.phones:
                if phone.value == new_phone.value:
                    return f"Phone {new_phone.value} already exist."
            self.phones.append(new_phone)
            return f"Phone {new_phone} successfully added to contact {self.name}"

    def change_phone(self, old_phone: str, new_phone: str):
        """Зміна номеру телефону на новий"""

        old_phone = Phone.verify_phone(old_phone)
        new_phone = Phone.verify_phone(new_phone)

        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return f"Phone '{old_phone}' is changed"
        return f"Phone '{old_phone}' is not in AddressBook. Try again!"

    def remove_phone(self, del_phone: str):
        """Видалення номеру телефону """

        del_phone = Phone.verify_phone(del_phone)
        for phone in self.phones:
            if phone.value == del_phone:
                self.phones.remove(phone)
                return f"Phone '{del_phone}' is delete"
        return f"Phone '{del_phone}' is not in AddressBook. Try again!"

    def set_birthday(self, birthday: str):
        """Встановлення дати народження """

        if self.birthday:
            return f"The date of birthday already exist in contact '{self.name}'"
        else:
            self.birthday = Birthday(birthday)
            return f"Date of birthday is added to the contact '{self.name}'"

    def change_birthday(self, new_birthday):
        """Зміна дати народження """

        self.birthday = new_birthday
        return f"Date of birthday '{self.name}' is changed: '{new_birthday}'"

    def remove_birthday(self):
        """Видалення дати народження контакту """
        if self.birthday:
            self.birthday = None
            return f"Date of birthday is deleted"
        return f"This contact does not have a date of birth"

    def add_email(self, new_email: str):
        """Додавання електронної пошти контакту. Проходить перевірку дублікатів при наявності інших e-mail """

        new_email = Email(new_email)
        if not self.emails:
            self.emails.append(new_email)
            return f"Email '{new_email}' is added"
        else:
            for email in self.emails:
                if email.value == new_email.value:
                    return f"E-mail '{new_email}' already exist in AddressBook. Try again!"
            self.emails.append(new_email)
            return f"E-mail '{new_email}' is added"

    def change_email(self, old_email: str, new_email: str):
        """Заміна електронної пошти контакту """

        for email in self.emails:
            if email.value == old_email:
                email.value = new_email
                return f"E-mail '{old_email}' is changed"
        return f"E-mail '{old_email}' is not in AddressBook. Try again!"

    def remove_email(self, del_email: str):
        """Видалення електронної пошти контакту """

        for email in self.emails:
            if email.value == del_email:
                self.emails.remove(email)
                return f"E-mail '{del_email}' is delete"
        return f"E-mail '{del_email}' is not in AddressBook. Try again!"

    def add_address(self, new_address: str):
        """Додавання адреси контакту. Проходить перевірку дублікатів при наявності інших адрес """

        new_address = Address(new_address)
        if not self.addresses:
            self.addresses.append(new_address)
            return f"Address '{new_address}' is added"
        else:
            for address in self.addresses:
                if address.value == new_address.value:
                    return f"Address '{new_address}' already exist in AddressBook. Try again!"
            self.addresses.append(new_address)
            return f"Address '{new_address}' is added"

    def change_address(self, old_address: str, new_address: str):
        """Заміна адреси контакту """

        for address in self.addresses:
            if address.value == old_address:
                address.value = new_address
                return f"Address '{old_address}' is changed"
        return f"Address '{old_address}' is not in AddressBook. Try again!"

    def remove_address(self, del_address: str):
        """Видалення адреси контакту """
        for address in self.addresses:
            if address.value == del_address:
                self.addresses.remove(address)
                return f"Address '{del_address}' is delete"
        return f"Phone '{del_address}' is not in AddressBook. Try again!"

    def days_to_birthday(self):
        """Визначення кількості днів до дня народження """
        today = datetime.now().date()
        birthday = self.birthday.value.replace(year=today.year)
        delta = (birthday - today).days if birthday > today else (
            birthday.replace(birthday.year + 1) - today).days
        return delta

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
                    self.remove_phone(val[0]) if Phone.verify_phone(
                        val[0]) else None
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
    def __init__(self):
        super().__init__()
        self.file_path = path.join("save", "contact_book.bin")

    def iterator(self, n: int):
        """Пагінація - посторінковий вивід Контактної книги """
        page = []
        for i in self.data.keys():
            page.append(i)
            if len(page) == n:
                yield page
                page = []
        if page:
            yield page

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
