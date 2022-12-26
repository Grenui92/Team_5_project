import pickle
from collections import UserDict
from os import path


class Note:
    def __init__(self, name: str, tags: list, text: str):
        self.name = name
        self.tags = tags
        self.text = text

    def __str__(self):
        return f"Note Name: {self.name}\n" \
               f"\tNote tags: {[tag for tag in self.tags] if self.tags else self.tags}\n" \
               f"\tNote text: {self.text}"


    def add_to_note(self, text: str):
        """Додавання тексту до текстового поля нотатки"""

        for piece in text:
            if piece.startswith("#"):
                self.tags.append(piece)
        self.text += " " + text
        return f"The text to note '{self.name}' is added"

    def clear_text(self):
        """Очищення текстового поля нотатки"""

        self.text = ""
        return f"The Note '{self.name}' is clear"

    def clear_tags(self):
        """Очищення списку тегів нотатки"""

        self.tags.clear()
        return f"The tags note '{self.name}' is clear"


class NoteBook(UserDict):
    def __init__(self):
        super().__init__()
        self.file_path = path.join("save", "note_book.bin")

    def search_in_notes(self, search_data: str | list):
        """Пошук заданого фрагмента у нотатках"""
        result = []
        for value in self.data.values():
            if search_data in (value.name, *value.tags, *value.text.split()):
                result.append(value)
        return result

    def iterator(self, n: int):
        """Пагінація - посторінковий вивід Книги нотаток"""

        page = []
        for i in self.data.keys():
            page.append(i)
            if len(page) == n:
                yield page
                page = []
        if page:
            yield page

    def save_to_file(self):
        """Збереження Книги нотаток у бінарний файл"""

        with open(self.file_path, "wb") as file:
            pickle.dump(self.data, file)
        return f"NoteBook save in '{self.file_path}'"

    def load_from_file(self):
        """Завантаження Книги контактів з бінарного файлу"""

        with open(self.file_path, "rb") as file:
            self.data = pickle.load(file)
        return f"NoteBook loaded from '{self.file_path}'"
