from datetime import datetime

from contact_classes.fields import Name, Phone, Email, Address, Birthday


class Record:
    def __init__(self, name: str, phone=None, email=None, address=None, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone else []
        self.emails = [Email(email)] if email else []
        self.addresses = Address(address) if address else "Address not set"
        self.birthday = Birthday(birthday) if birthday else "Birthday not set"

    def __str__(self):
        return f"Name: {self.name.value}\n" \
               f"\tphones: {[phone.value for phone in self.phones] if self.phones else self.phones}\n" \
               f"\temails: {[email.value for email in self.emails] if self.emails else self.emails}\n" \
               f"\taddress: {self.addresses.value if isinstance(self.addresses, Address) else self.addresses}\n" \
               f"\tbirthday: {self.birthday.value if isinstance(self.birthday, Birthday) else self.birthday}"

    def add_phone(self, new_phone: str):
        """Додавання номеру телефону. Проходить перевірку дублікатів при наявності інших номерів """

        new_phone = Phone(new_phone)
        if not self.phones:
            self.phones.append(new_phone)
            return f"Phone '{new_phone.value}' is added"
        for phone in self.phones:
            if phone.value == new_phone.value:
                return f"Phone {new_phone.value} already exist."
        self.phones.append(new_phone)
        return f"Phone {new_phone.value} successfully added to contact {self.name.value}"

    def set_birthday(self, birthday: str):
        """Встановлення дати народження """
        if isinstance(self.birthday, Birthday):
            return f"The date of birthday already exist in contact '{self.name.value}'"
        self.birthday = Birthday(birthday)
        return f"Date of birthday is added to the contact '{self.name.value}'"

    def add_email(self, new_email: str):
        """Додавання електронної пошти контакту. Проходить перевірку дублікатів при наявності інших e-mail """

        new_email = Email(new_email)
        if not self.emails:
            self.emails.append(new_email)
            return f"Email '{new_email.value}' is added"

        for email in self.emails:
            if email.value == new_email.value:
                return f"E-mail '{new_email.value}' already exist in AddressBook. Try again!"
        self.emails.append(new_email)
        return f"E-mail '{new_email.value}' is added"

    def set_address(self, new_address: str):
        """Додавання адреси контакту. Проходить перевірку дублікатів при наявності інших адрес """
        if isinstance(self.addresses, Address):
            return "Address already exist."
        else:
            self.addresses = Address(new_address)
            return f"Address '{new_address}' is added."

    def days_to_birthday(self):
        """Визначення кількості днів до дня народження """
        today = datetime.now().date()
        if isinstance(self.birthday, Birthday):
            birthday = self.birthday.value.replace(year=today.year)
            delta = (birthday - today).days if birthday > today else (birthday.replace(birthday.year + 1) - today).days
            return delta
        else:
            return "Birthday not set"

    def edit_information_contact(self, command, field, val):
        """"Редагування(заміна ти видалення) полів контакту"""
        old = val[0]
        if field not in self.__dict__:
            return "Wrong field information."
        if command == "change":
            new = " ".join(val)
            if field == "addresses":
                self.addresses = Address(new)
                return f"Address successfully change to {new} for contact {self.name.value}."
            if field == "birthday":
                self.birthday = Birthday(new)
                return f"Birthday successfully change to {new} for contact {self.name.value}."
            new = val[1]
            point = self.__dict__[field]
            for entry in point:
                if old == entry.value:
                    entry.value = new
                    return f"{old} successfully changed to {new}."
            return f"I can't find old value {old}."
        elif command == "del":
            if field == "birthday":
                self.birthday = "Birthday not set"
                return f"Birthday successfully deleted for contact {self.name.value}."
            elif field == "addresses":
                self.addresses = "Address not set"
                return f"Address successfully deleted for contact {self.name.value}."
            point = self.__dict__[field]
            for entry in point:
                if old == entry.value:
                    point.remove(entry)
                    return f"{old} successfully deleted from {field}."
            return f"I can't find old value {old}."
        return f"Wrong command '{command}'."
