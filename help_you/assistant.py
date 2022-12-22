from collections import UserDict


class Field():
    def __init__(self, value):
        self._value = value


class Phone(Field):
    pass


class Name(Field):
    pass


class Birthday(Field):
    pass


class Email(Field):
    pass


class Address(Field):
    pass


class Record():
    """Записи та їх функціонал"""

    def __init__(self, name: str, birthday: Birthday,
                 note: Note, phones: list = [],
                 emails: list = [], address: list = [],
                 ) -> None:
        pass


class NoteBook(UserDict):
    """Словник нотаток в форматі {name_of_note: Note}, який можем 
    зберігати та викачувати з бінарного файлу file_path
    """

    def __init__(self, file_path: str = r'.\notebook.bin'):
        self.file_path = file_path

    def iterator(self):
        """Повертає генератор по нотаткам"""
        pass

    def save_to_file(self):
        pass

    def load_from_file(self):
        pass


class ContactBook(UserDict):
    """Словник контактів в форматі {name_of_contact: Contact}, який можем 
    зберігати та викачувати з бінарного файлу file_path
    """

    def __init__(self, file_path: str = r'.\contactsbook.bin'):
        self.file_path = file_path

    def iterator(self):
        """Повертає генератор по контактам"""
        pass

    def save_to_file(self):
        pass

    def load_from_file(self):
        pass


class NotesWork():
    """Функціонал нотаток"""

    def __init__(self, notebook: NoteBook):
        self.notebook = notebook

    def create(self):
        pass

    def add_values(self):
        pass

    def show_all(self):
        pass

    def delete_all(self):
        pass

    def save_to_file(self):
        pass

    def load_from_file(self):
        pass

    def edit_information(self):
        pass

    def search_in(self):
        pass

    def sorted_by_tags(self):
        pass


class ContactsWork():
    """Функціонал контактів"""

    def __init__(self, contact_book: ContactBook):
        self.contact_book = contact_book


class UserInterface():
    """Функціонал роботи з користувачем"""

    def user_input(self: None) -> str:
        pass

    def parse_user_text(self: str) -> list:
        pass

    def handler(self):
        pass

    def show_results(self):
        pass

    def good_bye(self):
        pass

    def help_me(self):
        pass

    def instructions():
        pass

    def main(self):
        pass
