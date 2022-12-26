from fields import Name, Phone, Birthday, Email, Address

from datetime import datetime


class Record:
    def __init__(self, name: str, phone=None, email=None, address=None, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone else []
        self.emails = [Email(email)] if email else []
        self.addresses = [Address(address)] if address else []
        self.birthday = Birthday(birthday) if birthday else "Birthday not set"

    def __str__(self):
        return f"Name: {self.name.value}\n" \
               f"\tphones: {[phone.value for phone in self.phones] if self.phones else self.phones}\n" \
               f"\temails: {[email.value for email in self.emails] if self.emails else self.emails}\n" \
               f"\taddress: {[address.value for address in self.addresses] if self.addresses else self.addresses}\n" \
               f"\tbirthday: {self.birthday.value if isinstance(self.birthday, Birthday) else self.birthday}"

    def add_phone(self, new_phone: str):
        """Додавання номеру телефону. Проходить перевірку дублікатів при наявності інших номерів """

        new_phone = Phone(new_phone)
        if not self.phones:
            self.phones.append(new_phone)
            return f"Phone '{new_phone.value}' is added"
        else:
            for phone in self.phones:
                if phone.value == new_phone.value:
                    return f"Phone {new_phone.value} already exist."
            self.phones.append(new_phone)
            return f"Phone {new_phone.value} successfully added to contact {self.name.value}"

    def change_phone(self, old_phone: str, new_phone: str):
        """Зміна номеру телефону на новий"""

        old_phone = Phone(old_phone)
        new_phone = Phone(new_phone)

        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return f"Phone '{old_phone}' is changed"
        return f"Phone '{old_phone}' is not in AddressBook. Try again!"

    def remove_phone(self, del_phone: str):
        """Видалення номеру телефону """

        del_phone = Phone(del_phone)
        for phone in self.phones:
            if phone.value == del_phone:
                self.phones.remove(phone)
                return f"Phone '{del_phone}' is delete"
        return f"Phone '{del_phone}' is not in AddressBook. Try again!"

    def set_birthday(self, birthday: str):
        """Встановлення дати народження """

        if isinstance(self.birthday, Birthday):
            return f"The date of birthday already exist in contact '{self.name.value}'"
        self.birthday = Birthday(birthday)
        return f"Date of birthday is added to the contact '{self.name.value}'"

    def change_birthday(self, new_birthday):
        """Зміна дати народження """

        self.birthday = new_birthday
        return f"Date of birthday '{self.name}' is changed: '{new_birthday}'"

    def remove_birthday(self):
        """Видалення дати народження контакту """
        if self.birthday:
            self.birthday = "Birthday not set."
            return f"Date of birthday is deleted"
        return f"This contact does not have a date of birth"

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
            return f"Address '{new_address.value}' is added"
        for address in self.addresses:
            if address.value == new_address.value:
                return f"Address '{new_address.value}' already exist in AddressBook. Try again!"
        self.addresses.append(new_address)
        return f"Address '{new_address.value}' is added"

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
        old = val[0]

        if command == "change":
            new = val[1]
            if field == "birthday":
                self.birthday = Birthday(new)
            point = self.__dict__[field]
            for entry in point:
                if old == entry.value:
                    entry.value = new
                    return f"{old} successfully changed to {new}"
            raise KeyError(f"I can't find old value {old}")
        if command == "del":
            if field == "birthday":
                self.birthday = "Birthday not set"
                return f"Birthday {old} successfully deleted for contact {self.name.value}."
            point = self.__dict__[field]
            for entry in point:
                if old == entry.value:
                    point.remove(old)
                    return f"{old} successfully deleted from {field}"
            raise KeyError(f"I can't find old value {old}")
