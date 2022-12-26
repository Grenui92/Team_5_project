from book import Book
from os import path
from .note import Note
from typing import ClassVar



class WorkNote:

    def __init__(self):
        self.note_book = Book(path.join("database", "notes"))
        try:
            self.note_book.load_from_file()
        except FileNotFoundError:
            self.note_book.save_to_file()

    def create(self, *args) -> str:
        if args[0] in self.note_book:
            return f"Note with name '{args[0]} already exist."
        elif not args[0] or not args[1]:
            raise ValueError("You can't create empty note.")
        else:
            tags = []
            for word in args[1]:
                if word.startswith('#'):
                    tags.append(word)
            text = " ".join(args[1])
            self.note_book[args[0]] = Note(args[0], tags, text)
            return f"Note with name {args[0]} successfully created."

    def show_all(self, *_):
        all_notes = []
        for note in self.note_book.data.values():
            all_notes.append(str(note))

        return all_notes if all_notes else 'Notes is empty'

    def show_one(self, *args):
        return str(self.note_book[args[0]])

    def show_page(self, *args):
        """Ітеруємось по записам і формуєм рядок з контактами по n штук на сторінку"""
        result = []
        for page in self.note_book.iterator(int(args[0])):
            result_str = ""
            for record in page:
                result_str += str(self.note_book[record]) + "\n"
            result.append(f"\nPage Start\n{result_str}Page End")
        return result

    def delete_all(self):
        answer = input("You about to delete all notes in notebook. You shure? Y/N")
        if answer == 'Y':
            self.note_book.data = {}
            return "Note book now clean"
        else:
            return "Not deleted"

    def delete_one(self, *args):
        name = args[0]
        if name in self.note_book.data:
            del self.note_book.data[name]
            return f"Note {name} is deleted"
        else:
            return f"Note {name} is not in notebook"

    def save_to_file(self):
        return self.note_book.save_to_file()

    def load_from_file(self):
        return self.note_book.load_from_file()

    def edit_information(self, *args):
        try:
            name = args[0]
            values = args[1]
        except IndexError:
            raise IndexError("You can't edit note without new information.")
        note: Note = self.note_book.data[name]
        note.clear_text()
        note.clear_tags()
        return note.add_to_note(" ".join(values))

    def edit_name(self, *args):
        try:
            name = args[0]
            new_name = args[1][0]
        except IndexError:
            raise IndexError(f"Please enter 'old_name' and 'new_name'")
        record: Note = self.note_book[name]
        record.name = new_name
        self.note_book[new_name] = record
        del self.note_book[name]
        return f"{name}'s name has been changed to {new_name}"

    def search_in(self, search_data, *_):
        result = []

        for value in self.note_book.values():
            if search_data in (value.name, *value.tags, *value.text.split()):
                result.append(value)
        return result

    def sorted_by_tags(self, *args):

        tags = [args[0], *args[1]]
        matched_records = []

        for note in self.note_book.data.values():
            matched_tags = 0
            for tag in note.tags:
                if tag in tags:
                    matched_tags += 1
            matched_records.append(f'Matches:{matched_tags}\n'
                                   f'{str(note)}')
        return sorted(matched_records, reverse=True) if matched_records else "Matches not found"

    def add_values(self, *args):
        note: Note = self.note_book[args[0]]
        value = args[1]
        note.add_to_note(value)
        return f"Value {value} is added to {args[0]}"
