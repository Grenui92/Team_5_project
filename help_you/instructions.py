def show_instructions(command):
    match command:
        case "contacts":
            return """"create_contact NAME" - Створює контакт з іменем NAME.
Приклад: create_contact Stas
У разі успішного виконання команди повертає:
>>>"Contact with name {name} successfully created."
У разі виникнення помилки, що контакт з цим ім'ям існує:
>>>"Note with name '{name} already exist."
-----
"show_contact_book" - Показує всі контакти які є в КонтактнійКнизі зі всією інформацією про кожен контакт.
Приклад: show_contact_book
У разі успішного виконання повертає всі контакти у форматі
    Name: Stas
    phones: [x, y, s]
    emails: [x, y, s]
    address: Soborna str, 40
    birthday: 25.06.1992
-----
"show_contact NAME" - Показує контакт, який має ім'я NAME. Всю інформацію що мається в цьому контакті.
Приклад: show_contact Stas
У разі успішного виконання повертає:
    Name: Stas
    phones: [x, y, s]
    emails: [x, y, s]
    address: Soborna str, 40
    birthday: 25.06.1992
У разі якщо контакт з цим іменем не знайдено:
>>>'Contact {name} is not founded'
-----
"show_contact_page INT" - Виводить одну або кілька сторінок контактної книги. Кожна сторінка відображує певну кількість контактів і ця кількість
дорівнює INT. Якщо контактів у книзі менше або дорівнює INT - відобразить всі контакти однією сторінкою
Приклад: show_contacts_page 5
У разі успішного виконання повертає:
>>>Списки які містять П'ЯТЬ контактів в собі кожен.
Якщо INT при вводі не буде цілим числом виведе:
>>>Повідомлення про невідповідність введеної інформації до потрібного формату
-----
"clear_contact_book" - Очистить контактну книгу, видалить всі контакти.
Приклад: clear_contact_book
Має питати чи впевнені Ви, що хочете видалити всі контакти? Y/N
У разі успішного виконання повертає:
>>>'Contacts book now clean'
-----
"delete_contact NAME": - Видаляє контакт який має ім'я NAME
Приклад: delete_contact Stas
У разі успішного виконання повертає:
>>>"Contact {name} is deleted"
У разі відсутності контакту з таким ім'ям повертає:
>>>"Contact {name} is not in book"
-----
"add_to_contact NAME FIELD VALUE" - Додає у контакт який має ім'я NAME інформацію VALUE у поле FIELD
Відповідність полей і приклади значень які вони приймають:
FIELD phones - номера телефонів (+380661112233). Саме з кодом країни загальною довжиною 12 цифр і тринадцятий символ це +
FIELD emails - імейли (aaaa.ssss@ddddd.com). Імейл може складатися з букв латинського алфавіту, цифр і символів ".-_" до знаку "собака", і лише
з буков і символу крапки "." після "собаки". остання група букв має бути НЕ меншою за ТРИ символи поспіль.
FIELD addresses - адреси ("Kharkov, Ivanova str, 40/32"). Особливих вимог не має. Зберігається як звичайний текст.
FIELD birthday - день народження(2222.12.25). Приймає данні у форматі рррр.мм.дд
Приклад: add_to_contact Stas emails aaa.ssss@ddddd.com
У разі успішного виконання повертає:
>>>"Phone {new_phone.value} successfully added to contact {self.name.value}"
-----
"edit_contact NAME COMMAND FIELD OLD_VALUE NEW_VALUE" - Заміню OLD_VALUE на NEW_VALUE для контакту NAME у полі FIELD
COMMAND може приймати два значення. Або change, або del. У разі, якщо обрана команда del - значення NEW_VALUE вводити не треба
- У випадку з полями birthday and addresses - треба вводити на одне значення менше, тому що у разі виклику команди change
старе значення буде змінено на нове. У разі використання del взагалі не треба вводити ні NEW_VALUE ні OLD_VALUE бо старі данні буду просто замінено 
на "Not set
Приклад change:
edit_contact Stas change birthday 25.06.1992
edit_contact Stas change addresses Kharkiv, Maidan
Приклад del:
edit_contact Stas del birthday x (де х - це просто значення вказуюче на видалення інформації. Підійде будь яка буква)
edit_contact Stas del addresses x (де х - це просто значення вказуюче на видалення інформації. Підійде будь яка буква)

FIELD phones - номера телефонів (+380661112233). Саме з кодом країни загальною довжиною 12 цифр і тринадцятий символ це +
FIELD emails - імейли (aaaa.ssss@ddddd.com). Імейл може складатися з букв латинського алфавіту, цифр і символів ".-_" до знаку "собака", і лише
з буков і символу крапки "." після "собаки". остання група букв має бути НЕ меншою за ТРИ символи поспіль.
FIELD addresses - адреси ("Kharkov, Ivanova str, 40/32"). Особливих вимог не має. Зберігається як звичайний текст.
FIELD birthday - день народження(2222.12.25). Приймає данні у форматі рррр.мм.дд. 
Приклад: edit_contact Stas change phones +380501112233 +380667778899
         edit_contact Stas del phones +380501112233
У разі успішного виконання повертає:
>>>"{old} successfully changed to {new}"
>>>"{old} successfully deleted from {field}"
-----
"edit_contact_name OLD_NAME NEW_NAME" - Змінює ім'я контакту OLD_NAME на нове ім'я NEW_NAME
Приклад: edit_contact_name Stas Dima
У разі успішного виконання повертає:
>>>"{name}'s name has been changed to {new_name}"
-----
"search_in_contacts VALUE" - Проводить пошук у всіх полях всіх контактів згадки рядку VALUE
Приклад: search_in_contacts aaa.ssss@dddd.com - буде шукати всі контакти в яких зустрічається цей імейл і повертати ВЕСЬ контакт. Шукати буде у ВСІХ
полях, а не лише у імейл
У разі успішного виконання повертатиме:
>>>Список знайдених співпадінь
-----
"show_nearest_birthdays INT" - Показує контакти у яких день народження протягом найближчих INT днів.
Приклад: show_birthdays 5
У разі успішного виконання поверне:
>>>Список контактів з повною інформацією у яких ДН протягом найближчих 5 днів
-----
"days_to_birthday_for_one NAME" - Показує скільки днів залишилося до ДН контакту який має ім'я NAME
Приклад: days_to_birthday Dima
У разі успішного виконання поверне:
>>>"Days to birthday for {name} = days"
-----
"days_to_birthday_for_all" - Поверне кількість днів до ДН для всіх контактів
Приклад: show_days_to_birthday_for_all
У разі успішного виконання поверне:
>>>Список який міститиме в собі ось такий рядок про кожен контакт:
>>>"Days to Stas's birthday: 228"
"""
        case "notes":
            return """"create_note NAME TEXT" - Створює нотатку з іменем NAME. І заповнює її текстом TEXT. У TEXT можна відмічати слова символом # і тоді ці слова будуть
    додані в теги цієї нотатки. Вони будуть скопійовані і залишаться також у тексті.
Приклад: create_note New I want to #buy new #car.
    NAME = New
    TEXT = I want to #buy new #car
    tags = #buy #car
У разі успішного виконання повертає:
>>>"Note with name {name} successfully created."
-----
"show_note_book" - Показує всі нотатки які присутні у Книзі
Приклад: show_note_book
У разі успішного виконання повертає:
    Список Нотаток у такому форматі
        Note Name: New
        Note Tags: #buy #car
        Note Text: I want to #buy new #car
-----
"show_note NAME" - Показує одну нотатку яка має ім'я NAME
Приклад: show_note New
У разі успішного виконання поверне:
    Нотатку у такому форматі
        Note Name: New
        Note Tags: #buy #car
        Note Text: I want to #buy new #car
-----
"show_note_page INT" - Виводить одну або кілька сторінок книги нотаток. Кожна сторінка відображує певну кількість нотаток і ця кількість
дорівнює INT. Якщо нотаток у книзі менше або дорівнює INT - відобразить всі нотатки однією сторінкою
Приклад: show_note_page 5
У разі успішного виконання повертає:
>>>Списки які містять П'ЯТЬ нотаток в собі кожен.
-----
"clear_note_book" - Очистить книгу нотаток, видалить всі нотатки.
Приклад: clear_note_book
Має питати чи впевнені Ви, що хочете видалити всі нотатки? Y/N
У разі успішного виконання повертає:
>>>"Note book now clean"
-----
"delete_note NAME" - Видаляє нотатку яка має ім'я NAME
Приклад: delete_note New
У разі успішного виконання повертає:
>>>"Note {name} is deleted"
-----
"add_to_note NAME TEXT" - Додає інформацію TEXT до нотатки яка має ім'я NAME. У TEXT можна відмічати слова символом # і тоді ці слова будуть
додані в теги цієї нотатки. Вони будуть скопійовані і залишаться також у тексті.
Приклад: add_to_note New or maybe i want to #buy a #house
    Tags = old_tags + (#buy, #house)
    Text = old_text + or maybe i want to #buy a #house
    RESULT:
        Note Name = New
        Note Tags = #buy #car #house
        Note Text = I want to #buy new #car or maybe i want to #buy a #house
-----
"edit_note NAME TEXT" - Додає інформацію TEXT нотатку яка має ім'я NAME. Стару інформацію буде повністю видалено і заповнено новою.Залищиться лише ім'я
Приклад: edit_note New text My #dream - swim in the #storm
-----
"edit_note_name OLD_NAME NEW_NAME" - Змінює ім'я нотатки OLD_NAME на нове ім'я NEW_NAME
Приклад: edit_note_name New My_dream
-----
"search_in_notes VALUE" - Проводить пошук у всіх полях всіх нотаток згадки рядку VALUE
Приклад: search_in_note road - буде шукати всі нотатки в яких зустрічається це слово і повертати ВЕСЮ нотатку. Шукати буде у ВСІХ
полях, а не лише текст. Але якщо потрібно провести пошук САМЕ у тегах - використовуйте символ #
У разі успішного виконання повертає:
>>>Список співпадінь.
-----
"sorted_notes_by_tags TAG_1 TAG_2 TAG_3 ..."  - сортує книгу нотаток за кількістю співпадінь тегів нотаток з переданими тегами. Кількість тегів
не обмежена. Задавати теги для сортування треба з використанням символу #
Приклад: sorted_notes_by_tags #house #car #dream
У разі успішного виконання повертає:
    Список нотаток у яких є співпадіння хочаб з одним тегом. має бути щось типу
        "Співпадіння з тегами: 3
        Note Name: New
        Note tags: #house #car #dream
        Note text: My #dream - buy #car and #house

        "Співпадіння з тегами: 2
        Name: My_dream
        Note tags: #car #house
        Note text: I want to sell #car and #house
"""
        case "file_sorter":
            return """"file_sorter PATH" - виклик автоматичного сортувальника файлів. В змінну PATH вам треба вказати шлях до папки в середині якої буде відбуватися
сортування. Шлях може бути як абсолютним (кращий варіант, менше вірогідність помилки) так і відносним до того місця в якому ви викликали помічника.
Приклад: file_sorter C:/Users/Zver/Downloads
>"archives" - "zip", "tar", "tgz", "gz", "7zip", "7z", "iso", "rar"
>"audios" - "wav", "mp3", "ogg", "amr"
>"images" - "jpeg", "png", "jpg", "svg"
>"videos" - "avi", "mp4", "mov", "mkv"
>"documents" - "doc", "docx", "txt", "pdf", "xls", "xlsx", "ppt", "pptx", "rtf", "xml", "ini"
>"softwares" - "exe", "msi", "bat", "dll"
>"other" - all other files"""
