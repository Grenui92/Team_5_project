import pickle
from collections import UserDict
from re import findall


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

    def edit_note(self, value):
        pass

    def edit_note_name(self, old_name: str, new_name: str):
        pass


class NoteBook(UserDict):
    def __init__(self, file_path=None):
        super().__init__()
        self.file_path = ""
        self.count = 0

    def create_note(self, note):
        """Створює нову нотатку - екземпляр класу NoteBook"""

        if note.name.value not in self.data:
            self.data[note.name.value] = note
            return f"New note '{note.name.value}' is added"
        else:
            return f"This note already exist in NoteBook"

    def search_in_notes(self, search_data: str):
        """Пошук заданого фрагменту у нотатках"""

        result = []
        for key, value in self.data.items():
            search = findall(search_data, f"{self.data[key]}")
            if search:
                result.append(f"{self.data[key]}")
        return result

    def sorted_notes_by_tags(self, tags_value: list):
        """Сортування нотаток за тегами"""

        pass

    def iterator(self, n: int):
        """Пагінація - посторінковий вивід Книги нотаток"""

        notes_in_page = list(self.data.keys())
        if self.count >= len(notes_in_page):
            raise StopIteration("This is the end of NoteBook")
        result_list = notes_in_page[
            self.count: min(self.count + n, len(notes_in_page))
        ]
        for i in result_list:
            self.count += 1
        yield result_list

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
