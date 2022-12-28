from datetime import datetime
from re import IGNORECASE, search


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
    def normalize_phone(value):
        phone = search(r'(^\+\d{12}$)|(^0\d{9}$)', value)
        if phone:
            if len(phone.string) == 13:
                return f"{phone.string}"
            elif len(phone.string) == 10:
                return f"+38{phone.string}"
        else:
            raise ValueError("Phone number must be just 12 or 10 digits")

    @Field.value.setter
    def value(self, value):
        self._value = self.normalize_phone(value)


class Email(Field):

    @staticmethod
    def verify_email(value):
        """Верифікація введеного e-mail користувача"""

        email = search(r"^[a-z0-9._-]{2,64}@\w{2,}[.]\w{2,3}$", value, flags=IGNORECASE)
        if email:
            return email.group()
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
            raise ValueError("Invalid format birthday. Program wait dd.mm.yyyy format. Try again.")
        else:
            today = datetime.now().date()
            birthday = datetime.strptime(value, "%d.%m.%Y").date()
            if birthday > today:
                raise ValueError("That date has not yet come.")
            else:
                return birthday

    @Field.value.setter
    def value(self, value):
        self._value = self.verify_birthday(value)

class Address(Field):
    @staticmethod
    def verify_address(value):
        """Верифікація введеної адреси. Повинна складатися мінімум з 2 символів """
        address = search(r'^[a-zA-Z0-9,-/ ]+$', value)
        if address:
            return address.group()
        else:
            raise ValueError("Address must be longer than 1 letter")

    @Field.value.setter
    def value(self, value):
        self._value = self.verify_address(value)
