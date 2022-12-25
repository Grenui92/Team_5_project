import pickle
from collections import UserDict
from re import findall
from os import path


class Note:
    def __init__(self, name: str, tags: list, text: str):
        self.name = name
        self.tags = tags
        self.text = text

    def add_to_note(self, text: str):
        """Додавання тексту до текстового поля нотатки"""

        self.text += text
        return f"The text to note '{self.name}' is added"

    def clear_text(self):
        """Очистка текстового поля нотатки"""

        self.text = ""
        return f"The Note '{self.name}' is clear"

    def clear_tags(self):
        """Очистка списку тегів нотатки"""

        self.tags.clear()
        return f"The tags note '{self.name}' is clear"


class NoteBook(UserDict):
    def __init__(self):
        super().__init__()
        self.file_path = path.join("save", "note_book.bin")

    def search_in_notes(self, search_data: str):
        """Пошук заданого фрагменту у нотатках"""

        result = []
        for key, value in self.data.items():
            search = findall(search_data, f"{self.data[key]}")
            if search:
                result.append(f"{self.data[key]}")
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
