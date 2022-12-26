from os import path

from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter

from .decorator import input_error
from .file_sorter import sort_targets


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


class WorkContact():
    def __init__(self, book_bin_path=r"help_you\help_you\save\contact_book.bin"):
        """При ініціалізації відкриваєм бінарний файл з якого
        створюєм нову книжку. Якщо файл пустий - створюєм
        порожню книжку"""
        if path.getsize(path=book_bin_path) > 0:
            self.create(path=book_bin_path)
        else:
            self.create()

    """Методи приймають розпарсені дані від користувача args"""

    def save_to_file(self):
        self.contacts_book.save_to_file()

    def load_from_file(self):
        self.contacts_book.load_from_file()

    def create(self, *args, path=None) -> str:
        # !! ContactsBook при ініціалізації повинен мати можливість бути пустим
        name = args[0] if args[0] else None
        self.contacts_book = ContactBook(path)

        if self.contacts_book.file_path:
            self.contacts_book.load_from_file()
        else:
            self.contacts_book.data.update({name: Record()})

        return f"{str(self.contacts_book.data[name])}"

    def show_all(self) -> str:
        """Створює рядок з інформацією про кожен контакт"""

        records = list(self.contacts_book.data.values())
        rec_info = f'{str(records[0])}'

        for record in records[1:]:
            # !! В рекордс добавити __str__ який повертає строку з інформацією про рекорд
            rec_info.join('\n' + f'{str(record)}')

        return rec_info

    def show_one(self, *args: list) -> str:
        name = args[0]
        return f'{name}: {str(self.contacts_book.data[name])}' if name in self.contacts_book.data\
            else f'Contact {name} is not founded'

    def show_page(self, *args):
        """Ітеруємось по записам і формуєм рядок з контактами по n штук на сторінку"""
        n = args[0]
        page_count = n+1
        page_iterator = self.contacts_book.iterator(n)
        splited_contacts = 'Contacts:\n'

        for page in page_iterator:
            for record in page:
                splited_contacts.join(
                    f"{record}: {self.contacts_book.data[record]}")
            splited_contacts.join(f'____{page_count}____')
            page_count += 1

        splited_contacts.join("END")

        return splited_contacts

    def delete_all(self):
        answer = input(
            f'You about to delete all records in book. You shure? Y/N')
        if answer == 'Y':
            self.contacts_book.data = {}
            return 'Contacts book now clean'
        else:
            return 'Not deleted'

    def delete_one(self, *args: list):
        name = args[0]
        if name in self.contacts_book.data:
            del self.contacts_book.data[name]
            return f"Contact {name} is deleted"
        else:
            f"Contact {name} is not in book"

    def add_values(self, *args):
        name = args[0]
        field = args[1][0]
        value = args[1][1]

        records_fields_methods = {'phones': self.contacts_book.data[name].add_phone,
                                  'emails': self.contacts_book.data[name].add_email,
                                  'address': self.contacts_book.data[name].add_address,
                                  'birhday': self.contacts_book.data[name].set_birthday,
                                  'note': self.contacts_book.data[name].add_note
                                  }
        records_fields_methods[field](value)

        return f"Value {value} is added to {name}"

    def search_in(self, *args: list):
        value = args[0]
        matched_contacts = {}

        for contact in self.contacts_book.data.values():
            if value in self.contacts_book.data:
                matched_contacts.update(contact)

        return str(matched_contacts) if matched_contacts else 'No matches in contacts'

    def edit_information(self, *args):
        name = args[0]
        command = args[1][0]
        field = args[1][1]
        values = args[1][2:]

        if name in self.contacts_book.data:
            return self.contacts_book.data[name].edit_contact_information(command, field, values)
        else:
            return "This contact doesn't exist!"

    def sorted_by_tags(self, *args):
        tags = args[0].extend(args[1])
        matched_tags = 0
        matched_records = ''

        for contact in self.contacts_book.data.values():
            for tag in contact.note.tags:
                if tag in tags:
                    matched_tags += 1
                    one_match = str(contact)
            matched_records.join(f"matches: {matched_tags}\n")
            matched_records.join(f'{str(one_match)} \n')

        return matched_records if matched_records else "Matches not found"

    def show_nearest_birthdays(self, *args):
        n = args[1]
        n_days_birthday = ''

        for contact in self.contacts_book.values():
            if contact.days_to_bday <= n:
                n_days_birthday.join(
                    f"Days to {contact.name}'s birthday : {contact.days_to_bday} days \n")

        return n_days_birthday if n_days_birthday else f'No birthdays in nearest {n} days'

    def days_to_birthday_for_one(self, *args):
        name = args[0]
        return self.contacts_book.data[name].days_to_birthday()

    def days_to_birthday_for_all(self):
        bdays = ''

        for contact in self.contacts_book.data.values():
            bdays.join(
                f"Days to {contact.name}'s birthday: {contact.days_to_birthday()} \n")

        return bdays if bdays else 'There is no birthdays in contacts'

    def edit_name(self, *args):
        name = args[0]
        new_name = args[1]
        if new_name in self.contacts_book.data:
            self.contacts_book.data[new_name] = self.contacts_book.data.pop[name]
            return f"{name}'s name has been changed to {new_name}"
        else:
            return f'{name} not in contacts'


class UserInterface:

    def __init__(self):
        self.book = WorkContact()
        self.notes = WorkNote()
        self.commands = {"help": self.__help_me,
                         "instruction": self.__instructions,

                         "create_contact": self.book.create,
                         "show_contact_book": self.book.show_all,
                         "show_contact": self.book.show_one,
                         "show_contact_page": self.book.show_page,
                         "clear_contact_book": self.book.delete_all,
                         "delete_contact": self.book.delete_one,
                         "add_to_contact": self.book.add_values,
                         "edit_contact": self.book.edit_information,
                         "edit_contact_name": self.book.edit_name,
                         "search_in_contacts": self.book.search_in,
                         "sort_contacts_by_tags": self.sorted_by_tags,

                         "show_birthdays": self.book.show_nearest_birthdays,
                         "days_to_birthday": self.book.days_to_birthday,
                         "show_days_to_birthday_for_all": self.book.days_to_birthday_for_all,

                         "create_note": self.notes.create,
                         "show_note_book": self.notes.show_all,
                         "show_note": self.notes.show_one,
                         "show_note_page": self.notes.show_page,
                         "clear_note_book": self.notes.delete_all,
                         "delete_note": self.notes.delete_one,
                         "add_to_note": self.notes.add_values,
                         "edit_note": self.notes.edit_information,
                         "edit_note_name": self.notes.edit_name,
                         "search_in_notes": self.notes.search_in,
                         "sorted_notes_by_tags": self.notes.sorted_by_tags,

                         "file_sorter": self.__file_sorter,

                         "exit": self.__good_bye}

    def main(self):
        """Основна функція. Приймаємо текст, парсимо його, передаємо в хендлер. Виводимо результат."""
        while True:
            print("\nCommand 'help' will help you.")
            data = self.__input_user_text()
            command, name, data = self.__parse_user_text(data)
            result = self.__handler(command=command, name=name, data=data)
            self.__show_results(result)

    """MAIN"""

    @staticmethod
    @input_error
    def __parse_user_text(text: str) -> list:
        """Обробка тексту. У нас по суті є два типи команд - ті щоскладаються лише з команди, це такі як show_all & delete_all для них створено
        іф. Хендлер зажди приймає три параметри й щоб не робити зайвих перевірок і іншого - ми в нього завжди будемо передавати три аргументи,
        просто коли потрібно вони будуть порожні, а в методах не потрібні аргументи можна ховати просто в *_, другий тип - це ті в
        яких вже йде більше інформації. Як бачите - елемент з першим індексом це завжди команда. Він завжди існує. Другий елемент - це ім'я в 90%
        випадків. Лише у команді show_pages другий елемент буде не ім'я запису з яким ми взаємодіємо, а цифра кількості користувачів на сторінці.
        Треба мати це на увазі.
        У аргументі дата зберігається все інше. Це список, звідти можна витягнути все що завгодно по індексу."""

        data = text.split()
        if len(data) == 1:
            return [data[0], "", ""]
        else:
            return [data[0], data[1], data[2:]]

    @input_error
    def __handler(self, command: str, name: str, data) -> str | list:
        """Перевірка команди на наявність в нашому словнику і відповідно виклик функції, якщо команда існує, або рейз помилки. Ця помилка обрана,
        щоб відокремитися від KeyError. Коли декоратор ловить цей Warning - він має запускати процес аналізу і підказки команд."""

        if command in self.commands:
            return self.commands[command](name, data)
        else:
            raise Warning(command)

    @input_error
    def __input_user_text(self) -> str:
        """Просто зчитує текст."""
        commands_completer = self.commands
        users = {k: None for k in self.book.book}
        input_completer = NestedCompleter.from_nested_dict(
            {k: users for k in commands_completer})
        data = prompt('"Please enter what do you want to do: ',
                      completer=input_completer)
        return data

    @staticmethod
    @input_error
    def __show_results(result: str | list):
        """Виводить результат запросу користувача. Вдалий чи не вдалий - все одно виводить. Навіть декоратор якщо ловить помилку - він не принтує
        рядок, а ретюрнить його сюди. Всі принти мають виконуватися саме тут. І ніде більше в програмі. Окрім FileSorter"""

        if isinstance(result, list):
            for row in result:
                print(row)
        else:
            print(result)

    @input_error
    def __good_bye(self, *_):
        print(self.book.save_to_file())
        print(self.notes.save_to_file())
        exit("Bye")

    @staticmethod
    def __help_me(*_) -> str:
        return "If you want to know how to use this script - use command 'instruction' with:\n" \
               "'contacts' - to read about ContactBook commands.\n" \
               "'notes' - to read about NoteBook.\n" \
               "'file' - to read about FileSorter.\n" \
               "Or use 'exit' if you want to leave."

    @staticmethod
    @input_error
    def __instructions(category: str, *_) -> str:
        """Обирає який файл інструкцій відкрити відповідно до команди користувача."""

        match category:  # працює лише на пайтон 3.10+
            case "contacts":
                main_path = path.join("instructions", "contact_book.txt")
            case "file":
                main_path = path.join("instructions", "file_sorter.txt")
            case "notes":
                main_path = path.join("instructions", "note_book.txt")
            case _:
                raise ValueError(f"I can't find instruction for {category}.")
        with open(main_path, "r") as file:
            result = file.read()
        return result

    """END MAIN"""

    """FILE SORTER"""

    @staticmethod
    @input_error
    def __file_sorter(path_for_sorting: str, path_for_sorting_2: list):
        if path_for_sorting_2:
            sort_targets([path_for_sorting, *path_for_sorting_2])
            return f"Folders {path_for_sorting} and {','.join(path_for_sorting_2)} successfully sorted."
        else:
            sort_targets(path_for_sorting)
            return f"Folder {path_for_sorting} successfully sorted."

    """END FILE SORTER"""
