import re
from datetime import datetime, date
from collections import UserDict, defaultdict


class IncorrectTagException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"Incorrect tag: {self.message}"


class IncorrectTitleException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"Incorrect title: {self.message}"


class IncorrectTextException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"Incorrect text: {self.message}"


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Title(Field):
    def __init__(self, title: str):
        Title.is_valid_title(title)
        super().__init__(title)

    @staticmethod
    def is_valid_title(self, title: str):
        title_min_length = 3
        title_max_length = 50
        if not title:
            raise IncorrectTitleException("the required title is missing")
        if not title_min_length <= len(title) <= title_max_length:
            raise IncorrectTitleException(
                f"the title must be {title_min_length} to {title_max_length} characters long ")


class Tag(Field):
    def __init__(self, tag: str):
        Tag.is_valid_tag(tag)
        super().__init__(tag)

    def update_value(self, new_value: str):
        self.is_valid_tag(new_value)
        self.value = new_value

    @staticmethod
    def is_valid_tag(tag: str):
        tag_min_length = 3
        tag_max_length = 20
        pattern = r'^[a-zA-Z0-9-_]+$'
        if not tag:
            raise IncorrectTagException("the required tag is missing")
        if not re.match(pattern, tag):
            raise IncorrectTagException(f"the tag must contain only letters, numbers and symbols '_' and '-'")
        if not tag_min_length <= len(tag) <= tag_max_length:
            raise IncorrectTagException(
                f"the tag must be {tag_min_length} to {tag_max_length} characters long ")


class Text(Field):
    def __init__(self, text: str):
        Text.is_valid_text(text)
        super().__init__(text)

    @staticmethod
    def is_valid_text(self, text: str):
        text_min_length = 0
        text_max_length = 256
        if not text:
            raise IncorrectTextException("missing required text")
        if not text_min_length <= len(text) <= text_max_length:
            raise IncorrectTagException(
                f"the text must be {text_min_length} to {text_max_length} characters long ")


class Record:
    record_auto_id = 0

    def __init__(self, title):
        Record.record_auto_id += 1
        self.record_auto_id = Record.record_auto_id
        self.title: Title = title
        self.text: Text = None
        self.tags: list[Tag] = []


    def __str__(self):
        return f"Id: {self.record_auto_id}, Title: {self.title}, Tags: {', '.join(p for p in self.tags)}, Text: {self.text}"

    def add_tag(self, tag: Tag):
        self.tags.append(tag)

    def remove_tag(self, tag: Tag):
        found = list(filter(lambda p: str(p) == str(tag), self.tags))
        for i in found:
            self.tags.remove(i)


class NotePad(UserDict):
    def __init__(self):
        self.data = list()

    def add_record(self, record: Record):
        self.data.append(record)

    def find_by_title(self, title: Title):
        result = list(filter(lambda record: str(record.title).lower()
                             == str(title).lower(), self.data))
        return result[0] if result else None

    def delete(self, title: Title):
        result = self.find_by_title(title)
        if result:
            self.data.remove(result)


# The debugging section. It will be the last to be deleted.
notepad = NotePad()

record1 = Record("MyTitle-1")
record2 = Record("MyTitle-2")
print(record1)
print(record2)

tag1 = Tag('tag-1')
tag2 = Tag('ta')
tag3 = Tag('')

print(record1)
notepad.add_record(record1)