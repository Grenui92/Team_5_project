from os import path
from collections import UserDict
import pickle


class Note:
    def __init__(self, name: str, tags: list, text: str):
        self.name = name
        self.tags = tags
        self.text = text

    def add_to_note(self, text: str):
        """Додавання тексту до текстового поля нотатки"""

        for piece in text:
            if piece.startswith("#"):
                self.tags.append(piece)
        self.text += text + " "
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
        if isinstance(search_data, str):
            search_data = list(search_data)
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


class WorkNote:

    def __init__(self, note_book_bin_path=r"help_you\help_you\save\note_book.bin"):
        """При ініціалізації відкриваєм бінарний файл з якого
        створюєм новий нотатник. Якщо файл пустий - створюєм
        порожній"""
        if path.getsize(note_book_bin_path) > 0:
            self.create(path=note_book_bin_path)
        else:
            self.create()

    def create(self, *args, path=None) -> str:
        name = args[0]
        text = args[1]
        self.note_book = NoteBook(file_path=path)

        if self.note_book.file_path:
            self.note_book.load_from_file()
        else:
            self.note_book.data.update({name: Note(name=name,
                                        text=text,
                                        tags=self.search_tags(text))})

        return f"{str(self.note_book.data[name])}"

    def show_all(self):
        all_notes = ''
        for note in self.note_book.data.values():
            all_notes.join(str(note)+'\n')

        return all_notes if all_notes else 'Notes is empty'

    def show_one(self, *args):
        name = args[0]

        return str(self.note_book.data[name])

    def show_page(self, *args):
        """Ітеруємось по записам і формуєм рядок з контактами по n штук на сторінку"""
        n = args[0]
        page_count = n+1
        page_iterator = self.note_book.iterator(n)
        splited_notes = 'notes:\n'

        for page in page_iterator:
            for record in page:
                splited_notes.join(
                    f"{record}: {self.note_book.data[record]}")
            splited_notes.join(f'____{page_count}____')
            page_count += 1

        splited_notes.join("END")

        return splited_notes

    def delete_all(self):
        answer = input(
            f'You about to delete all notes in notebook. You shure? Y/N')
        if answer == 'Y':
            self.note_book.data = {}
            return 'Note book now clean'
        else:
            return 'Not deleted'

    def delete_one(self, *args):
        name = args[0]
        if name in self.note_book.data:
            del self.note_book.data[name]
            return f"Note {name} is deleted"
        else:
            f"Note {name} is not in notebook"

    def save_to_file(self):
        self.note_book.save_to_file()

    def load_from_file(self):
        self.note_book.load_from_file()

    def edit_information(self, *args):
        name = args[0]
        field = args[1][1]
        values = args[1][2:]

        if name in self.note_book.data:
            return self.note_book.data[name].edit_note_information(field, values)
        else:
            return "This contact doesn't exist!"

    def edit_name(self, *args):
        name = args[0]
        new_name = args[1]
        self.note_book.data[new_name] = self.note_book.data.pop(name)

        return f"{name}'s name has been changed to {new_name}"

    def search_in(self, args):
        value = args[0]
        matches = ''
        for note in self.note_book.data.values():
            if value in (note.name, note.text) or value in note.tags:
                matches.join(str(note))

        return matches

    def sorted_by_tags(self, *args):
        tags = args[0].extend(args[1])
        matched_tags = 0
        matched_records = ''

        for note in self.note_book.data.values():
            for tag in note.tags:
                if tag in tags:
                    matched_tags += 1
                    one_match = str(note)
            matched_records.join(f"matches: {matched_tags}\n")
            matched_records.join(f'{str(one_match)} \n')

        return matched_records if matched_records else "Matches not found"

    def add_values(self, *args):
        name = args[0]
        field = args[1][0]
        value = args[1][1:]

        note_fields_methods = {'name': self.note_book[name].name,
                               'text': self.note_book.data[name].text,
                               'tags': self.note_book.data[name].tags
                               }

        if field == 'text':
            note_fields_methods[field] += value[0]
        elif field == 'name':
            note_fields_methods[field] = value[0]
        elif field == 'tags':
            note_fields_methods[field].append(
                tag for tag in value if tag.startswith('#'))

        return f"Value {value} is added to {name}"

    @staticmethod
    def search_tags(text):
        words = text.split(' ')
        tags = []
        for word in words:
            if word.startswith('#'):
                tags.append(word)
        return tags
