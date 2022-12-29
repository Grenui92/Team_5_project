class Note:
    def __init__(self, name: str, tags: list, text: str):
        self.name = name
        self.tags = tags
        self.text = text

    def __str__(self):
        return f"Note Name: {self.name}\n" \
               f"\tNote tags: {[tag for tag in self.tags] if self.tags else 'Empty'}\n" \
               f"\tNote text: {self.text}"

    def add_to_note(self, text: list):
        """Додавання тексту до текстового поля нотатки"""

        for piece in text:
            if piece.startswith("#"):
                self.tags.append(piece)
        self.text += " " + " ".join(text)
        return f"The text to note '{self.name}' is added"

    def clear_text(self):
        """Очищення текстового поля нотатки"""

        self.text = ""
        return f"The Note '{self.name}' is clear"

    def clear_tags(self):
        """Очищення списку тегів нотатки"""

        self.tags.clear()
        return f"The tags note '{self.name}' is clear"
