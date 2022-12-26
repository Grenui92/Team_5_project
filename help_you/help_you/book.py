class ContactBook(UserDict):
    def __init__(self, file_path=path.join("database", "contact_book")):
        super().__init__()
        self.file_path = f"{file_path}.bin"

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
        return f"ContactBook database in '{self.file_path}'"

    def load_from_file(self):
        """Завантаження Книги контактів з бінарного файлу """

        with open(self.file_path, "rb") as file:
            self.data = pickle.load(file)
        return f"ContactBook loaded from '{self.file_path}'"

class NoteBook(UserDict):
    def __init__(self):
        super().__init__()
        self.file_path = path.join("database", "note_book.bin")

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
        return f"NoteBook database in '{self.file_path}'"

    def load_from_file(self):
        """Завантаження Книги контактів з бінарного файлу"""

        with open(self.file_path, "rb") as file:
            self.data = pickle.load(file)
        return f"NoteBook loaded from '{self.file_path}'"