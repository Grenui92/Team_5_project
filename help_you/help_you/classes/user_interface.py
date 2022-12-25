from os import path
from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter
from decorator import input_error

class WorkContact:
    pass


class WorkNote:
    pass


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
                         "show_all_birthdays": self.book.days_to_birthday_for_all,

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
    @input_error
    @staticmethod
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
        input_completer = NestedCompleter.from_nested_dict({k: users for k in commands_completer})
        data = prompt('"Please enter what do you want to do: ', completer=input_completer)
        return data

    @input_error
    @staticmethod
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

    @input_error
    @staticmethod
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

    @input_error
    @staticmethod
    def __file_sorter(path_for_sorting: str, *_):
        one_time = FileSorter(path_for_sorting)
        one_time.job()

    """END FILE SORTER"""
